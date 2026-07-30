#!/usr/bin/env python3
"""Drive the ABP planning matrix with one headless cursor-agent session per slot.

Each slot gets its own `cursor-agent -p` process, which satisfies the protocol's
one-session-per-run isolation requirement without a human starting each chat.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BENCH = Path(__file__).resolve().parent
REPO = BENCH.parent
ORDER_FIXTURES = ("f1", "f2")
ORDER_ARMS = ("gsd", "openspec", "no-tools", "native")
REPLICATES = (1, 2, 3)
DONE_STATUSES = {"plan_ready", "scored"}
PENDING_STATUS = "awaiting_operator"
STALE_STATUS = "running"

PROMPT_TEMPLATE = """Use the skill at .cursor/skills/abp-matrix-runner/SKILL.md to run exactly one ABP planning slot.

The slot is already resolved. Skip step 1 of the skill (do not run next_run.py) and use this run directory:

    {run_dir}

Read {run_dir}/prompt.md and follow its arm instructions.

This session is NON-INTERACTIVE:
- You cannot ask questions and nobody will answer. Never wait for input.
- If the fixture is ambiguous, write the clarifying questions you would have asked and the
  answer you assumed for each into the plan artifacts, then keep going.
- Planning only. Do not implement the Todo API and do not build or test app code.
- Do not read fixtures/todo-api-ambiguous/ANSWER_KEY.md.
- Do not create or edit anything under benchmark/runs/{protocol}/human_sheets/.
- Do not edit docs/benchmark/PROTOCOL.md.

Write the final plan artifacts into {run_dir}/artifacts/ so scoring does not depend on chat history.

Then run these three commands from the repo root, in this exact order, replacing <N> with
the number of tool, MCP, and CLI calls you made during this run. score.py copies token
counts out of meta.json, so tiktoken_count.py has to populate them first:

    python3 benchmark/mark_run.py {run_dir} finish --tool-calls <N> --model "{model}"
    python3 benchmark/tiktoken_count.py {run_dir}
    python3 benchmark/score.py {run_dir}

Finish by printing the run directory and the resulting status.
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_meta(run_dir: Path) -> dict:
    return json.loads((run_dir / "meta.json").read_text(encoding="utf-8"))


def save_meta(run_dir: Path, meta: dict) -> None:
    (run_dir / "meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )


def iter_slots(protocol: str):
    base = BENCH / "runs" / protocol
    for fixture in ORDER_FIXTURES:
        for arm in ORDER_ARMS:
            for replicate in REPLICATES:
                run_dir = base / fixture / arm / f"r{replicate}"
                if (run_dir / "meta.json").is_file():
                    yield run_dir


def build_worklist(protocol: str, retry_stalled: bool) -> list[Path]:
    work = []
    for run_dir in iter_slots(protocol):
        status = load_meta(run_dir).get("status")
        if status == PENDING_STATUS or (retry_stalled and status == STALE_STATUS):
            work.append(run_dir)
    return work


def agent_command(run_dir: Path, protocol: str, model: str, sandbox: str | None) -> list[str]:
    prompt = PROMPT_TEMPLATE.format(
        run_dir=run_dir.relative_to(REPO), protocol=protocol, model=model
    )
    cmd = [
        "cursor-agent",
        "--print",
        "--output-format",
        "text",
        "--model",
        model,
        "--force",
        "--trust",
        "--approve-mcps",
        "--workspace",
        str(REPO),
    ]
    if sandbox:
        cmd += ["--sandbox", sandbox]
    cmd.append(prompt)
    return cmd


def live_agents() -> int:
    """Count cursor-agent processes still running, so heavy sessions can drain."""
    try:
        out = subprocess.run(["pgrep", "-f", "cursor-agent"], capture_output=True,
                             text=True, check=False).stdout
    except OSError:
        return 0
    return len([line for line in out.splitlines() if line.strip()])


def wait_for_quiet(max_live: int, timeout: int = 120) -> None:
    deadline = time.monotonic() + timeout
    while live_agents() > max_live and time.monotonic() < deadline:
        time.sleep(5)


def attempt_one(run_dir: Path, protocol: str, model: str, sandbox: str | None,
                timeout: int, log_dir: Path, attempt: int) -> tuple[bool, str, bool]:
    """One headless session attempt. Returns (ok, detail, transient)."""
    label = "-".join(run_dir.relative_to(BENCH / "runs" / protocol).parts)
    log_path = log_dir / f"{label}.log"
    cmd = agent_command(run_dir, protocol, model, sandbox)

    started = utc_now()
    t0 = time.monotonic()
    with log_path.open("w", encoding="utf-8") as log:
        log.write(f"# {label}\n# started_at {started}\n"
                  f"# model {model}\n# attempt {attempt}\n\n")
        log.flush()
        try:
            proc = subprocess.run(
                cmd, cwd=REPO, stdout=log, stderr=subprocess.STDOUT,
                timeout=timeout, check=False, start_new_session=True,
            )
            exit_code: int | None = proc.returncode
            timed_out = False
        except subprocess.TimeoutExpired:
            exit_code, timed_out = None, True
    elapsed = round(time.monotonic() - t0, 1)
    agent_output = len(log_path.read_text(encoding="utf-8", errors="replace")) > 200

    meta = load_meta(run_dir)
    meta.setdefault("started_at", started)
    meta["driver_wall_seconds"] = elapsed
    meta["driver_exit_code"] = exit_code
    meta["driver_log"] = str(log_path.relative_to(REPO))
    meta["model"] = meta.get("model") or model

    status = meta.get("status")
    artifacts = run_dir / "artifacts"
    has_artifacts = artifacts.is_dir() and any(artifacts.iterdir())

    # A negative exit code with no agent output means the session was killed
    # before it could do anything (resource pressure, lifecycle kill) — retryable.
    transient = bool(exit_code is not None and exit_code < 0 and not agent_output)

    if timed_out:
        detail = f"timed out after {timeout}s"
    elif status not in DONE_STATUSES:
        killed = f"killed by signal {-exit_code}" if transient else f"exited {exit_code}"
        detail = f"agent {killed} but status is {status!r}"
    elif not has_artifacts:
        detail = "status advanced but artifacts/ is empty"
    else:
        detail = ""

    if detail:
        meta["status"] = PENDING_STATUS
        meta["driver_last_error"] = detail
        save_meta(run_dir, meta)
        return False, detail, transient

    meta.pop("driver_last_error", None)
    meta.setdefault("ended_at", utc_now())
    save_meta(run_dir, meta)
    return True, f"{status} in {elapsed}s", False


def run_one(run_dir: Path, protocol: str, model: str, sandbox: str | None,
            timeout: int, log_dir: Path, retries: int, cooldown: int) -> tuple[bool, str]:
    """Run one slot, retrying attempts that were killed before doing any work."""
    meta = load_meta(run_dir)
    if meta.get("status") == STALE_STATUS:
        meta["status"] = PENDING_STATUS
        meta["driver_recovered_from_stale"] = utc_now()
        save_meta(run_dir, meta)

    detail = "not attempted"
    for attempt in range(1, retries + 2):
        wait_for_quiet(max_live=1)
        ok, detail, transient = attempt_one(
            run_dir, protocol, model, sandbox, timeout, log_dir, attempt
        )
        if ok:
            return True, detail
        if not transient or attempt > retries:
            return False, detail
        backoff = cooldown * (2 ** (attempt - 1))
        print(f"  transient ({detail}); retrying in {backoff}s", flush=True)
        time.sleep(backoff)
    return False, detail


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--protocol", default="abp-v1")
    ap.add_argument("--model", default="composer-2.5",
                    help="pinned model slug; must match every arm (see cursor-agent --list-models)")
    ap.add_argument("--max-runs", type=int, default=24, help="safety cap on slots per invocation")
    ap.add_argument("--timeout", type=int, default=2400, help="per-run timeout in seconds")
    ap.add_argument("--cooldown", type=int, default=20,
                    help="seconds to idle between slots so agent processes drain")
    ap.add_argument("--retries", type=int, default=2,
                    help="retries per slot for sessions killed before doing any work")
    ap.add_argument("--sandbox", choices=("enabled", "disabled"),
                    help="override the cursor-agent sandbox setting for each session")
    ap.add_argument("--retry-stalled", action="store_true",
                    help="also pick up slots left in status 'running' by a crashed session")
    ap.add_argument("--keep-going", action="store_true",
                    help="continue to the next slot after a failed run instead of stopping")
    ap.add_argument("--list", action="store_true", help="print the worklist and exit")
    ap.add_argument("--dry-run", action="store_true", help="print the command per slot without running it")
    args = ap.parse_args()

    if not shutil.which("cursor-agent"):
        print("cursor-agent not found on PATH", file=sys.stderr)
        return 2

    work = build_worklist(args.protocol, args.retry_stalled)
    if not work:
        print(f"Nothing to do: no {PENDING_STATUS} slots in {args.protocol}.")
        return 0

    work = work[: args.max_runs]
    print(f"{len(work)} slot(s) queued for {args.protocol}, model={args.model}")
    for run_dir in work:
        print(f"  {run_dir.relative_to(REPO)}")
    if args.list:
        return 0

    if args.dry_run:
        for run_dir in work:
            print("\n$ " + " ".join(agent_command(run_dir, args.protocol, args.model, args.sandbox)[:-1]) + " '<prompt>'")
        return 0

    log_dir = BENCH / "runs" / args.protocol / "_driver_logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    passed, failed = [], []
    for index, run_dir in enumerate(work, start=1):
        rel = run_dir.relative_to(REPO)
        if index > 1 and args.cooldown:
            time.sleep(args.cooldown)
        print(f"\n[{index}/{len(work)}] {rel}", flush=True)
        ok, detail = run_one(run_dir, args.protocol, args.model, args.sandbox,
                             args.timeout, log_dir, args.retries, args.cooldown)
        if ok:
            passed.append(rel)
            print(f"  ok — {detail}", flush=True)
        else:
            failed.append((rel, detail))
            print(f"  FAILED — {detail}", flush=True)
            print(f"  log: {log_dir.relative_to(REPO)}", flush=True)
            if not args.keep_going:
                break

    print(f"\nDone: {len(passed)} ok, {len(failed)} failed")
    for rel, detail in failed:
        print(f"  {rel}: {detail}")
    remaining = len(build_worklist(args.protocol, args.retry_stalled))
    print(f"{remaining} slot(s) still {PENDING_STATUS}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
