const pptxgen = require("pptxgenjs");
const path = require("path");

const OUT = path.join(__dirname, "ticket-to-plan-abp-team-update.pptx");

const C = {
  ink: "1A1F2E",
  slate: "2C3345",
  mist: "F4F6F8",
  white: "FFFFFF",
  card: "FFFFFF",
  muted: "5C6578",
  soft: "E8ECF1",
  accent: "0F766E",
  accentSoft: "D1FAF5",
  pass: "047857",
  fail: "B45309",
};

const FONT = "Calibri";

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "ticket-to-plan-test";
pres.title = "Ticket-to-plan × OpenSpec — results";
const S = pres.shapes;

function card(slide, x, y, w, h) {
  slide.addShape(S.ROUNDED_RECTANGLE, {
    x,
    y,
    w,
    h,
    fill: { color: C.card },
    shadow: { type: "outer", color: "1A1F2E", blur: 10, offset: 2, opacity: 0.08 },
    rectRadius: 0.1,
  });
}

// ─── 1. Title ───────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.addShape(S.RECTANGLE, {
    x: 0,
    y: 0,
    w: 10,
    h: 5.625,
    fill: { color: C.ink },
  });
  s.addText("RESULTS UPDATE", {
    x: 0.6,
    y: 1.35,
    w: 8.8,
    h: 0.35,
    fontFace: FONT,
    fontSize: 13,
    bold: true,
    color: C.accentSoft,
    margin: 0,
    charSpacing: 3,
  });
  s.addText("Can ticket-to-plan work well with OpenSpec?", {
    x: 0.6,
    y: 1.85,
    w: 8.8,
    h: 0.9,
    fontFace: FONT,
    fontSize: 30,
    bold: true,
    color: C.white,
    margin: 0,
  });
  s.addText(
    "Short answer: yes for plan quality — OpenSpec matched GSD.\nOn this problem, every method hit the same checklist. Cost is where they differ.",
    {
      x: 0.6,
      y: 2.95,
      w: 8.8,
      h: 0.9,
      fontFace: FONT,
      fontSize: 16,
      color: "A8B0C0",
      margin: 0,
    }
  );
  s.addText("24 planning runs · a human reviewed every plan · optional AI judge skipped", {
    x: 0.6,
    y: 4.9,
    w: 8.8,
    h: 0.3,
    fontFace: FONT,
    fontSize: 12,
    color: "7A8499",
    margin: 0,
  });
}

// ─── 2. How we tested ───────────────────────────────────────
{
  const s = pres.addSlide();
  s.addShape(S.RECTANGLE, {
    x: 0,
    y: 0,
    w: 10,
    h: 5.625,
    fill: { color: C.mist },
  });
  s.addText("How we tested", {
    x: 0.5,
    y: 0.35,
    w: 9,
    h: 0.45,
    fontFace: FONT,
    fontSize: 28,
    bold: true,
    color: C.ink,
    margin: 0,
  });
  s.addText("Same product problem. Four planning methods. Rules locked before any run.", {
    x: 0.5,
    y: 0.85,
    w: 9,
    h: 0.35,
    fontFace: FONT,
    fontSize: 14,
    color: C.muted,
    margin: 0,
  });

  const arms = [
    { title: "GSD", body: "ticket-to-plan + GSD" },
    { title: "OpenSpec", body: "same skill, OpenSpec" },
    { title: "Skill only", body: "no external tools" },
    { title: "Native", body: "plain AI planning" },
  ];
  arms.forEach((a, i) => {
    const x = 0.5 + i * 2.325;
    card(s, x, 1.35, 2.025, 1.25);
    s.addText(a.title, {
      x: x + 0.15,
      y: 1.55,
      w: 1.7,
      h: 0.35,
      fontFace: FONT,
      fontSize: 16,
      bold: true,
      color: C.ink,
      margin: 0,
    });
    s.addText(a.body, {
      x: x + 0.15,
      y: 1.95,
      w: 1.7,
      h: 0.4,
      fontFace: FONT,
      fontSize: 12,
      color: C.muted,
      margin: 0,
    });
  });

  const facts = [
    { t: "Subject", d: "Rust Todo HTTP API (Axum + SQLite)" },
    { t: "Inputs", d: "A fully locked SPEC, plus a vague ticket" },
    { t: "Matrix", d: "4 methods × 2 inputs × 3 repeats = 24 plans" },
    { t: "Scoring", d: "Auto checklist first, then a human scored plans without knowing the method" },
  ];
  facts.forEach((f, i) => {
    const y = 2.9 + i * 0.55;
    s.addText(f.t, {
      x: 0.6,
      y,
      w: 1.5,
      h: 0.4,
      fontFace: FONT,
      fontSize: 14,
      bold: true,
      color: C.accent,
      margin: 0,
    });
    s.addText(f.d, {
      x: 2.2,
      y,
      w: 7,
      h: 0.4,
      fontFace: FONT,
      fontSize: 14,
      color: C.ink,
      margin: 0,
    });
  });
}

// ─── 3. Headline finding ────────────────────────────────────
{
  const s = pres.addSlide();
  s.addShape(S.RECTANGLE, {
    x: 0,
    y: 0,
    w: 10,
    h: 5.625,
    fill: { color: C.mist },
  });
  s.addText("Headline finding", {
    x: 0.5,
    y: 0.35,
    w: 9,
    h: 0.45,
    fontFace: FONT,
    fontSize: 28,
    bold: true,
    color: C.ink,
    margin: 0,
  });

  card(s, 0.5, 1.05, 9.0, 1.5);
  s.addText("Plan quality: every method hit 100% of the checklist", {
    x: 0.75,
    y: 1.25,
    w: 8.5,
    h: 0.4,
    fontFace: FONT,
    fontSize: 18,
    bold: true,
    color: C.ink,
    margin: 0,
  });
  s.addText(
    "Plans also had the expected structure and delivery rules. The computer score and the human score agreed every time. OpenSpec matched GSD on quality.",
    {
      x: 0.75,
      y: 1.75,
      w: 8.5,
      h: 0.55,
      fontFace: FONT,
      fontSize: 14,
      color: C.muted,
      margin: 0,
    }
  );

  const boxes = [
    {
      title: "What that means",
      body: "On a locked Todo SPEC (and this vague ticket), the skill and backends did not separate on checklist quality — including plain AI.",
    },
    {
      title: "Where they differ",
      body: "Time, estimated tokens, and tool calls. Plain AI / skill-only are cheaper. GSD is slowest. OpenSpec tends to use more tokens.",
    },
  ];
  boxes.forEach((b, i) => {
    const x = 0.5 + i * 4.6;
    card(s, x, 2.85, 4.3, 2.1);
    s.addText(b.title, {
      x: x + 0.25,
      y: 3.1,
      w: 3.8,
      h: 0.35,
      fontFace: FONT,
      fontSize: 15,
      bold: true,
      color: C.accent,
      margin: 0,
    });
    s.addText(b.body, {
      x: x + 0.25,
      y: 3.55,
      w: 3.8,
      h: 1.15,
      fontFace: FONT,
      fontSize: 13,
      color: C.muted,
      margin: 0,
    });
  });
}

// ─── 4. Cost side-by-side ───────────────────────────────────
{
  const s = pres.addSlide();
  s.addShape(S.RECTANGLE, {
    x: 0,
    y: 0,
    w: 10,
    h: 5.625,
    fill: { color: C.mist },
  });
  s.addText("Cost on the locked SPEC — average of 3 runs", {
    x: 0.5,
    y: 0.3,
    w: 9,
    h: 0.45,
    fontFace: FONT,
    fontSize: 26,
    bold: true,
    color: C.ink,
    margin: 0,
  });

  const headers = ["Method", "Time (sec)", "Est. tokens", "Tool calls", "Checklist %"];
  const widths = [1.8, 1.5, 1.7, 1.7, 1.8];
  let x0 = 0.6;
  headers.forEach((h, i) => {
    s.addText(h, {
      x: x0,
      y: 0.95,
      w: widths[i],
      h: 0.35,
      fontFace: FONT,
      fontSize: 12,
      bold: true,
      color: C.muted,
      margin: 0,
    });
    x0 += widths[i];
  });
  s.addShape(S.RECTANGLE, {
    x: 0.6,
    y: 1.3,
    w: 8.5,
    h: 0.02,
    fill: { color: C.soft },
  });

  const rows = [
    ["GSD", "247", "5,178", "15", "100%"],
    ["OpenSpec*", "159", "7,304", "30", "100%"],
    ["Skill only", "89", "4,505", "27", "100%"],
    ["Native", "36", "4,433", "27", "100%"],
  ];
  rows.forEach((r, ri) => {
    const y = 1.5 + ri * 0.7;
    card(s, 0.5, y, 9.0, 0.58);
    let x = 0.7;
    r.forEach((cell, ci) => {
      s.addText(cell, {
        x,
        y: y + 0.12,
        w: widths[ci],
        h: 0.35,
        fontFace: FONT,
        fontSize: 14,
        bold: ci === 0 || ci === 4,
        color: C.ink,
        margin: 0,
      });
      x += widths[ci];
    });
  });

  s.addText(
    "*OpenSpec time/tokens may be slightly inflated by one old re-run still in the summary. Quality used the three official runs.",
    {
      x: 0.6,
      y: 4.5,
      w: 8.8,
      h: 0.55,
      fontFace: FONT,
      fontSize: 11,
      color: C.muted,
      margin: 0,
    }
  );
}

// ─── 5. Acceptance rules ────────────────────────────────────
{
  const s = pres.addSlide();
  s.addShape(S.RECTANGLE, {
    x: 0,
    y: 0,
    w: 10,
    h: 5.625,
    fill: { color: C.mist },
  });
  s.addText("Did we meet our own pass rules?", {
    x: 0.5,
    y: 0.3,
    w: 9,
    h: 0.45,
    fontFace: FONT,
    fontSize: 26,
    bold: true,
    color: C.ink,
    margin: 0,
  });
  s.addText("We wrote these pass/fail rules before seeing results. Overall: not a full pass — still useful.", {
    x: 0.5,
    y: 0.8,
    w: 9,
    h: 0.35,
    fontFace: FONT,
    fontSize: 13,
    color: C.muted,
    margin: 0,
  });

  const rules = [
    {
      result: "PASS",
      title: "OpenSpec matches GSD on the locked SPEC",
      detail: "Same checklist coverage and plan structure — within our 5-point rule.",
      ok: true,
    },
    {
      result: "FAIL",
      title: "Skill methods beat plain AI on delivery rules",
      detail: "Everyone scored 100% — a tie, not a win for the skill.",
      ok: false,
    },
    {
      result: "FAIL",
      title: "Skill methods beat plain AI on the vague ticket",
      detail: "Again everyone hit 100%. The ticket was not hard enough to separate them.",
      ok: false,
    },
    {
      result: "NOT DONE",
      title: "Build from each plan and run contract tests",
      detail: "We have not implemented the four plans yet — so we cannot claim “plans work.”",
      ok: false,
    },
  ];
  rules.forEach((r, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.5 + col * 4.7;
    const y = 1.3 + row * 1.85;
    card(s, x, y, 4.4, 1.65);
    s.addText(r.result, {
      x: x + 0.25,
      y: y + 0.2,
      w: 3.9,
      h: 0.3,
      fontFace: FONT,
      fontSize: 13,
      bold: true,
      color: r.ok ? C.pass : C.fail,
      margin: 0,
    });
    s.addText(r.title, {
      x: x + 0.25,
      y: y + 0.55,
      w: 3.9,
      h: 0.45,
      fontFace: FONT,
      fontSize: 14,
      bold: true,
      color: C.ink,
      margin: 0,
    });
    s.addText(r.detail, {
      x: x + 0.25,
      y: y + 1.05,
      w: 3.9,
      h: 0.45,
      fontFace: FONT,
      fontSize: 12,
      color: C.muted,
      margin: 0,
    });
  });
}

// ─── 6. Ask / next ──────────────────────────────────────────
{
  const s = pres.addSlide();
  s.addShape(S.RECTANGLE, {
    x: 0,
    y: 0,
    w: 10,
    h: 5.625,
    fill: { color: C.ink },
  });
  s.addText("What we recommend", {
    x: 0.6,
    y: 0.4,
    w: 8.8,
    h: 0.45,
    fontFace: FONT,
    fontSize: 28,
    bold: true,
    color: C.white,
    margin: 0,
  });

  const recs = [
    {
      title: "Treat OpenSpec as a viable swap for GSD",
      body: "On this subject, plan quality matched. Prefer it when you want OpenSpec files and CLI.",
    },
    {
      title: "Pick a method by cost, not checklist score",
      body: "Plain AI and skill-only were much faster here. Heavier stacks bought process, not higher scores.",
    },
    {
      title: "Optional: prove the plans actually build",
      body: "Implement one mid-quality plan per method and run the API contract tests if you need that proof.",
    },
    {
      title: "Use a harder problem if we need a quality winner",
      body: "Everything scored 100%. Separating methods needs a tougher ticket — and a new frozen test, not quiet rule edits.",
    },
  ];
  recs.forEach((r, i) => {
    const y = 1.1 + i * 1.0;
    s.addShape(S.ROUNDED_RECTANGLE, {
      x: 0.6,
      y,
      w: 8.8,
      h: 0.85,
      fill: { color: C.slate },
      rectRadius: 0.1,
    });
    s.addText(r.title, {
      x: 0.85,
      y: y + 0.12,
      w: 8.3,
      h: 0.28,
      fontFace: FONT,
      fontSize: 15,
      bold: true,
      color: C.accentSoft,
      margin: 0,
    });
    s.addText(r.body, {
      x: 0.85,
      y: y + 0.42,
      w: 8.3,
      h: 0.3,
      fontFace: FONT,
      fontSize: 13,
      color: "C5CBD6",
      margin: 0,
    });
  });
}

pres.writeFile({ fileName: OUT }).then(() => {
  console.log("Wrote", OUT);
});
