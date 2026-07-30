#!/usr/bin/env python3
"""Drive ABP S2 draft scoring with one headless cursor-agent session per Blind ID.

Produces drafts under human_sheets/drafts/<blind_id>.json.
Does NOT write official S2. Merge drafts into the scorecard with:

  python3 benchmark/s2_xlsx.py merge-drafts
  # human reviews needs_review rows, then:
  python3 benchmark/s2_xlsx.py apply
  python3 benchmark/human_sheet.py ingest --protocol abp-v1
"""

from __future__ import annotations

import argparse
import json
import select
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BENCH = Path(__file__).resolve().parent
ROOT = BENCH.parent


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def hs_paths(protocol: str) -> dict[str, Path]:
    hs = BENCH / "runs" / protocol / "human_sheets"
    return {
        "hs": hs,
        "key": hs / "mapping_key.json",
        "plans": hs / "plans",
        "drafts": hs / "drafts",
        "logs": hs / "_s2_draft_logs",
        "requests": hs / "_s2_draft_requests",
    }


PROMPT = """Use the skill at .cursor/skills/abp-s2-draft/SKILL.md to draft S2 scores for exactly one Blind ID.

This is a DRAFT only. You are not the official scorer.

Request file (read this first):
    {request_path}

Plan files (read ONLY these — do not follow symlinks outside this folder, do not open mapping_key or ANSWER_KEY):
    {plan_dir}

Write your result to exactly:
    {draft_path}

Rules:
- One Blind ID only: {blind_id}
- Non-interactive: never wait for input.
- TRUE only with a short evidence quote from the plan.
- If unsure: present=null, needs_review=true, short note — do not guess.
- Do not open mapping_key.json, ANSWER_KEY.md, or any run path with /gsd/, /openspec/, /no-tools/, /native/.
- Do not call human_sheet.py ingest.

When done, print DRAFT_OK {blind_id} or DRAFT_FAIL with a reason.
"""


def load_key(protocol: str) -> dict:
    return json.loads(hs_paths(protocol)["key"].read_text(encoding="utf-8"))


def checklist_items(fixture: str) -> list[dict]:
    if fixture == "f2":
        data = json.loads(
            (ROOT / "fixtures/todo-api-ambiguous/decision_checklist.json").read_text(
                encoding="utf-8"
            )
        )
        return [{"id": d["id"], "text": d.get("text", d["id"])} for d in data["decisions"]]
    data = json.loads(
        (ROOT / "fixtures/todo-api/gold_checklist.json").read_text(encoding="utf-8")
    )
    return [{"id": r["id"], "text": r.get("text", r["id"])} for r in data["requirements"]]


def ensure_opaque_plans(protocol: str) -> int:
    """Copy artifacts into plans/<blind_id>/ so paths do not reveal the arm."""
    p = hs_paths(protocol)
    key = load_key(protocol)
    if p["plans"].exists():
        # Replace symlinks with copies for blindness
        for child in list(p["plans"].iterdir()):
            if child.is_symlink() or child.is_dir():
                if child.is_symlink():
                    child.unlink()
                else:
                    shutil.rmtree(child)
    else:
        p["plans"].mkdir(parents=True)

    for blind_id, info in key.items():
        dest = p["plans"] / blind_id
        src = ROOT / info["run_dir"] / "artifacts"
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)
        if src.is_dir():
            for f in src.rglob("*"):
                if f.is_file():
                    rel = f.relative_to(src)
                    out = dest / rel
                    out.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, out)
        else:
            (dest / "MISSING_ARTIFACTS.txt").write_text(f"No artifacts at {src}\n")
    return len(key)


def pending_blind_ids(protocol: str, redo: bool) -> list[str]:
    p = hs_paths(protocol)
    key = load_key(protocol)
    ordered = sorted(key.items(), key=lambda kv: (kv[1]["fixture"], kv[0]))
    out = []
    for blind_id, _ in ordered:
        draft = p["drafts"] / f"{blind_id}.json"
        if redo or not draft.is_file():
            out.append(blind_id)
            continue
        try:
            data = json.loads(draft.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            out.append(blind_id)
            continue
        if data.get("blind_id") != blind_id or not isinstance(data.get("items"), list):
            out.append(blind_id)
    return out


def write_request(protocol: str, blind_id: str, model: str) -> Path:
    p = hs_paths(protocol)
    p["requests"].mkdir(parents=True, exist_ok=True)
    info = load_key(protocol)[blind_id]
    payload = {
        "blind_id": blind_id,
        "fixture": info["fixture"],
        "protocol": protocol,
        "model": model,
        "plan_dir": str((p["plans"] / blind_id).relative_to(ROOT)),
        "draft_path": str((p["drafts"] / f"{blind_id}.json").relative_to(ROOT)),
        "items": checklist_items(info["fixture"]),
        "instructions": (
            "Draft only. Cite evidence for TRUE/FALSE. "
            "If unsure leave present null with needs_review true."
        ),
    }
    path = p["requests"] / f"{blind_id}.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def agent_cmd(protocol: str, blind_id: str, model: str, sandbox: str | None) -> list[str]:
    p = hs_paths(protocol)
    req = p["requests"] / f"{blind_id}.json"
    prompt = PROMPT.format(
        request_path=req.relative_to(ROOT),
        plan_dir=(p["plans"] / blind_id).relative_to(ROOT),
        draft_path=(p["drafts"] / f"{blind_id}.json").relative_to(ROOT),
        blind_id=blind_id,
    )
    cmd = [
        "cursor-agent",
        "--print",
        "--output-format",
        "stream-json",
        "--stream-partial-output",
        "--model",
        model,
        "--force",
        "--trust",
        "--approve-mcps",
        "--workspace",
        str(ROOT),
    ]
    if sandbox:
        cmd += ["--sandbox", sandbox]
    cmd.append(prompt)
    return cmd


def live_print_sessions() -> list[int]:
    """PIDs of headless --print agent sessions only (ignore always-on workers)."""
    try:
        out = subprocess.run(
            ["pgrep", "-fl", "cursor-agent"], capture_output=True, text=True, check=False
        ).stdout
    except OSError:
        return []
    pids: list[int] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        # Background worker / helpers — never block on these
        if "worker start" in line or "cursor-agent-worker" in line:
            continue
        if "npm exec" in line:
            continue
        parts = line.split(None, 1)
        if not parts or not parts[0].isdigit():
            continue
        rest = parts[1] if len(parts) > 1 else ""
        # Only count CLI print sessions launched by this driver
        if "--print" in rest:
            pids.append(int(parts[0]))
    return pids


def live_agents() -> int:
    """Backward-compatible count used by wait_for_quiet."""
    return len(live_print_sessions())


def wait_for_quiet(max_live: int = 0, timeout: int = 30) -> None:
    """Briefly wait only for other --print sessions; skip permanent workers.

    Default max_live=0 means: wait until no other print session is alive,
    or until timeout, then proceed. Timeout is short (30s) because workers
    are ignored and a stuck session should not block the matrix for minutes.
    """
    deadline = time.monotonic() + timeout
    while True:
        live = live_print_sessions()
        if len(live) <= max_live:
            return
        left = int(deadline - time.monotonic())
        if left <= 0:
            print(
                f"  proceeding with {len(live)} other print session(s) still live",
                flush=True,
            )
            return
        print(
            f"  waiting for other print session(s) ({len(live)} live, {left}s left)…",
            flush=True,
        )
        time.sleep(5)


def draft_valid(path: Path, blind_id: str) -> bool:
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return (
        data.get("blind_id") == blind_id
        and isinstance(data.get("items"), list)
        and len(data["items"]) > 0
    )


def activity_summary(line: str) -> str | None:
    """Turn a stream-json event into a concise terminal activity line."""
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        text = line.strip()
        return text[:180] if text else None

    event_type = str(
        event.get("type")
        or event.get("event")
        or event.get("event_type")
        or event.get("kind")
        or "event"
    )
    tool = (
        event.get("tool_name")
        or event.get("tool")
        or event.get("name")
        or (event.get("function") or {}).get("name")
    )
    if tool and ("tool" in event_type.lower() or "call" in event_type.lower()):
        return f"{event_type}: {tool}"

    text = (
        event.get("text")
        or event.get("delta")
        or event.get("message")
        or event.get("content")
    )
    if isinstance(text, dict):
        text = text.get("text") or text.get("content")
    if isinstance(text, list):
        parts = []
        for part in text:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict) and part.get("text"):
                parts.append(str(part["text"]))
        text = " ".join(parts)
    if isinstance(text, str):
        text = " ".join(text.split())
        if text:
            return f"{event_type}: {text[:180]}"

    useful = ("start", "complete", "finish", "error", "status", "tool", "call")
    if any(word in event_type.lower() for word in useful):
        return event_type
    return None


def summarize_draft(data: dict) -> str:
    items = data.get("items") or []
    confident = sum(
        1
        for item in items
        if item.get("present") is not None and not item.get("needs_review")
    )
    review = sum(1 for item in items if item.get("needs_review"))
    blank = sum(
        1
        for item in items
        if item.get("present") is None and not item.get("needs_review")
    )
    depth = "depth?" if data.get("depth_needs_review") else f"depth={data.get('depth_ok')}"
    guardrails = (
        "guardrails?"
        if data.get("guardrails_needs_review")
        else f"guardrails={data.get('guardrails_ok')}"
    )
    return (
        f"{confident} confident, {review} needs_review, {blank} blank | "
        f"{depth}, {guardrails}"
    )


def run_agent_with_progress(
    cmd: list[str],
    log_path: Path,
    draft_path: Path,
    blind_id: str,
    timeout: int,
    stall_seconds: int,
) -> tuple[int | None, str, float]:
    """Run cursor-agent while streaming useful events and heartbeat progress.

    Returns (exit_code_or_None, status, elapsed_seconds) where status is one of
    ``ok``, ``timeout``, or ``stall``. Stall fires when no stdout arrives for
    ``stall_seconds`` and no draft file exists yet (silent hang).
    """
    started = time.monotonic()
    last_terminal_update = started
    last_output_at = started
    draft_announced = False
    status = "ok"
    try:
        display_log_path = log_path.relative_to(ROOT)
    except ValueError:
        display_log_path = log_path
    try:
        display_draft_path = draft_path.relative_to(ROOT)
    except ValueError:
        display_draft_path = draft_path

    print("  launching Cursor Agent…", flush=True)
    print(f"  full event log: {display_log_path}", flush=True)
    if stall_seconds > 0:
        print(
            f"  stall watchdog: {stall_seconds}s with no output "
            "(before draft exists)",
            flush=True,
        )

    with log_path.open("a", encoding="utf-8") as log:
        proc = subprocess.Popen(
            cmd,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            start_new_session=True,
        )
        assert proc.stdout is not None
        print(f"  agent pid: {proc.pid}", flush=True)

        while True:
            now = time.monotonic()
            elapsed = now - started
            if elapsed >= timeout:
                status = "timeout"
                proc.kill()
                print(f"  [{int(elapsed):>3}s] timeout — stopping agent", flush=True)
                break

            # Silent hang: no stdout for stall_seconds and draft not written yet.
            # Heartbeats alone must not reset this clock.
            if (
                stall_seconds > 0
                and not draft_announced
                and (now - last_output_at) >= stall_seconds
            ):
                status = "stall"
                proc.kill()
                silent = int(now - last_output_at)
                print(
                    f"  [{int(elapsed):>3}s] stall — no agent output for "
                    f"{silent}s; stopping for retry",
                    flush=True,
                )
                break

            ready, _, _ = select.select([proc.stdout], [], [], 1.0)
            if ready:
                line = proc.stdout.readline()
                if line:
                    last_output_at = time.monotonic()
                    log.write(line)
                    log.flush()
                    summary = activity_summary(line)
                    if summary:
                        print(f"  [{int(elapsed):>3}s] {summary}", flush=True)
                        last_terminal_update = time.monotonic()
                elif proc.poll() is not None:
                    break
            elif proc.poll() is not None:
                break

            if not draft_announced and draft_valid(draft_path, blind_id):
                draft_announced = True
                # Draft on disk counts as progress — disable stall kill.
                last_output_at = time.monotonic()
                print(
                    f"  [{int(elapsed):>3}s] draft created: "
                    f"{display_draft_path}",
                    flush=True,
                )
                last_terminal_update = time.monotonic()

            if time.monotonic() - last_terminal_update >= 15:
                if draft_announced:
                    state = "draft created; agent finishing"
                else:
                    silent = int(time.monotonic() - last_output_at)
                    state = f"agent still working (silent {silent}s)"
                print(f"  [{int(elapsed):>3}s] {state}…", flush=True)
                last_terminal_update = time.monotonic()

        if status == "ok":
            for line in proc.stdout:
                last_output_at = time.monotonic()
                log.write(line)
                summary = activity_summary(line)
                if summary:
                    elapsed = time.monotonic() - started
                    print(f"  [{int(elapsed):>3}s] {summary}", flush=True)
            log.flush()

        try:
            exit_code = proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            exit_code = proc.wait()
            if status == "ok":
                status = "timeout"

    elapsed = round(time.monotonic() - started, 1)
    print(f"  agent finished: exit={exit_code}, elapsed={elapsed}s", flush=True)
    return (None if status != "ok" else exit_code), status, elapsed


def run_one(
    protocol: str,
    blind_id: str,
    model: str,
    sandbox: str | None,
    timeout: int,
    retries: int,
    cooldown: int,
    stall_seconds: int,
) -> tuple[bool, str]:
    p = hs_paths(protocol)
    p["drafts"].mkdir(parents=True, exist_ok=True)
    p["logs"].mkdir(parents=True, exist_ok=True)
    write_request(protocol, blind_id, model)
    draft_path = p["drafts"] / f"{blind_id}.json"
    log_path = p["logs"] / f"{blind_id}.log"

    detail = "not attempted"
    for attempt in range(1, retries + 2):
        wait_for_quiet()
        if draft_path.exists():
            draft_path.unlink()
        started = utc_now()
        cmd = agent_cmd(protocol, blind_id, model, sandbox)
        with log_path.open("w", encoding="utf-8") as log:
            log.write(f"# {blind_id}\n# started_at {started}\n# attempt {attempt}\n\n")
            log.flush()
        exit_code, status, elapsed = run_agent_with_progress(
            cmd, log_path, draft_path, blind_id, timeout, stall_seconds
        )
        agent_output = len(log_path.read_text(encoding="utf-8", errors="replace")) > 200
        ok = draft_valid(draft_path, blind_id)
        if ok:
            # stamp model if missing
            data = json.loads(draft_path.read_text(encoding="utf-8"))
            data.setdefault("scorer", "agent-draft")
            data.setdefault("model", model)
            data["drafted_at"] = utc_now()
            data["driver_wall_seconds"] = elapsed
            draft_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            summary = summarize_draft(data)
            print(f"  draft summary: {summary}", flush=True)
            return True, f"draft ok in {elapsed}s — {summary}"

        if status == "stall":
            detail = f"stalled (no output for {stall_seconds}s)"
            if attempt <= retries:
                backoff = cooldown * (2 ** (attempt - 1))
                print(f"  transient ({detail}); retrying in {backoff}s", flush=True)
                time.sleep(backoff)
                continue
        elif status == "timeout":
            detail = f"timed out after {timeout}s"
        elif exit_code is not None and exit_code < 0 and not agent_output:
            detail = f"killed by signal {-exit_code}"
            if attempt <= retries:
                backoff = cooldown * (2 ** (attempt - 1))
                print(f"  transient ({detail}); retrying in {backoff}s", flush=True)
                time.sleep(backoff)
                continue
        else:
            detail = f"agent exited {exit_code}; draft missing/invalid"
        if attempt > retries:
            break
        time.sleep(cooldown)
    return False, detail


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--protocol", default="abp-v1")
    ap.add_argument("--model", default="composer-2.5")
    ap.add_argument("--max-runs", type=int, default=24)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument(
        "--stall-seconds",
        type=int,
        default=90,
        help=(
            "kill and retry if no agent stdout for this many seconds before "
            "a draft exists (0 disables); default 90"
        ),
    )
    ap.add_argument("--cooldown", type=int, default=15)
    ap.add_argument("--retries", type=int, default=1)
    ap.add_argument("--sandbox", choices=("enabled", "disabled"))
    ap.add_argument("--redo", action="store_true", help="re-draft even if draft JSON exists")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--keep-going", action="store_true")
    ap.add_argument(
        "--skip-copy-plans",
        action="store_true",
        help="do not refresh opaque plan copies before starting",
    )
    args = ap.parse_args()

    if not shutil.which("cursor-agent"):
        print("cursor-agent not found on PATH", file=sys.stderr)
        return 2

    if not args.skip_copy_plans:
        n = ensure_opaque_plans(args.protocol)
        print(f"refreshed opaque plan copies for {n} Blind IDs")

    work = pending_blind_ids(args.protocol, args.redo)[: args.max_runs]
    if not work:
        print("No pending S2 drafts.")
        return 0

    print(f"{len(work)} Blind ID(s) queued, model={args.model}")
    for b in work:
        print(f"  {b}")
    if args.list:
        return 0
    if args.dry_run:
        print("dry-run: would launch cursor-agent per Blind ID")
        return 0

    print(
        "\nIMPORTANT: run this from your own terminal (not from a Cursor chat),\n"
        "or the driver may be killed when the tool call ends.\n",
        flush=True,
    )

    passed, failed = [], []
    for i, blind_id in enumerate(work, start=1):
        if i > 1 and args.cooldown:
            time.sleep(args.cooldown)
        print(f"\n[{i}/{len(work)}] {blind_id}", flush=True)
        ok, detail = run_one(
            args.protocol,
            blind_id,
            args.model,
            args.sandbox,
            args.timeout,
            args.retries,
            args.cooldown,
            args.stall_seconds,
        )
        if ok:
            passed.append(blind_id)
            print(f"  ok — {detail}", flush=True)
        else:
            failed.append((blind_id, detail))
            print(f"  FAILED — {detail}", flush=True)
            if not args.keep_going:
                break

    print(f"\nDone: {len(passed)} ok, {len(failed)} failed")
    for b, d in failed:
        print(f"  {b}: {d}")
    left = len(pending_blind_ids(args.protocol, redo=False))
    print(f"{left} Blind ID(s) still without a valid draft")
    print("next: python3 benchmark/s2_xlsx.py merge-drafts")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
