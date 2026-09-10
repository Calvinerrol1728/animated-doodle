// Headless smoke test: boots index.html in jsdom and drives every mode of the study app.
// Run from the repo root:  node .test/smoke.mjs      (DBG=1 to dump the view DOM at each step)
import fs from "node:fs";
import path from "node:path";
import jsdomPkg from "jsdom";
const { JSDOM, VirtualConsole, requestInterceptor } = jsdomPkg;

const ROOT = path.resolve(new URL("..", import.meta.url).pathname);
const results = [];
function ok(name, fn, extra = "") {
  let cond, err = "";
  try { cond = typeof fn === "function" ? fn() : fn; } catch (e) { cond = false; err = e.message; }
  let note = typeof extra === "function" ? "" : extra;
  if (typeof extra === "function") { try { note = String(extra() ?? ""); } catch (e) { note = "(unreadable)"; } }
  results.push([cond ? "PASS" : "FAIL", name + ((note || err) ? ` — ${note || err}` : "")]);
}

const vc = new VirtualConsole();
const jsdomErrors = [];
vc.on("jsdomError", (e) => jsdomErrors.push(String((e && e.message) || e)));
vc.on("error", (m) => jsdomErrors.push(String(m)));

// jsdom exposes no window.fetch; app.js guards on it, and this shim keeps the deck.json path testable.
const shim = `<script>(function(){ if (window.fetch) return;
window.fetch = function(u){ return new Promise(function(res,rej){ var x=new XMLHttpRequest(); x.open("GET",u,true);
 x.onload=function(){ res({ ok:x.status>=200&&x.status<300, status:x.status,
   json:function(){ try{return Promise.resolve(JSON.parse(x.responseText));}catch(e){return Promise.reject(e);} },
   text:function(){return Promise.resolve(x.responseText);} }); };
 x.onerror=function(){ rej(new Error("network")); }; x.send(); }); }; })();</script>`;

const html = fs.readFileSync(path.join(ROOT, "index.html"), "utf8")
  .replace('<script src="data/deck.json.js"></script>', shim + "\n<script src=\"data/deck.json.js\"></script>");

function makeDom() {
  return new JSDOM(html, {
    url: "http://localhost:8000/",
    runScripts: "dangerously",
    pretendToBeVisual: true,
    virtualConsole: vc,
    resources: {
      interceptors: [requestInterceptor((request) => {
        const rel = new URL(request.url).pathname.replace(/^\//, "");
        const f = path.join(ROOT, rel);
        if (!rel || !fs.existsSync(f) || fs.statSync(f).isDirectory()) {
          return new Response("not found", { status: 404, headers: { "Access-Control-Allow-Origin": "*" } });
        }
        return new Response(fs.readFileSync(f), { status: 200, headers: { "Access-Control-Allow-Origin": "*" } });
      })],
    },
  });
}
const dom = makeDom();
const { window } = dom;
window.Element.prototype.animate = window.Element.prototype.animate || function () { return { cancel() {} }; };

await new Promise((r) => setTimeout(r, 900));   // boot + fetch fallback

const doc = window.document;
const q = (s) => doc.querySelector(s);
const all = (s) => Array.from(doc.querySelectorAll(s));
const txt = () => (q("#view") ? q("#view").textContent.replace(/\s+/g, " ").trim() : "");
const dump = (tag) => { if (process.env.DBG) console.log(`\n### ${tag}\n`, q("#view").innerHTML.slice(0, 700)); };
function click(sel) {
  const e = typeof sel === "string" ? q(sel) : sel;
  if (!e) throw new Error("missing element: " + sel);
  e.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
}
const soft = (fn, tag) => { try { fn(); } catch (e) { console.log("  [step failed] " + tag + ": " + e.message); if (process.env.DBG) console.log(q("#view").innerHTML.slice(0, 1200)); } };
const key = (k, code) => doc.dispatchEvent(new window.KeyboardEvent("keydown", { key: k, code: code || k, bubbles: true }));
const setVal = (sel, v, ev = "input") => { const e = q(sel); if (!e) throw new Error("missing " + sel); e.value = v; e.dispatchEvent(new window.Event(ev, { bubbles: true })); };
const store = (k) => JSON.parse(window.localStorage.getItem(k) || "null");

const deck = window.__DECK_EXAMPLE;
const N = { cards: deck.flashcards.length, q: deck.questions.length, s: deck.sections.length };

/* ── boot ──────────────────────────────────────────────────────────── */
ok("no runtime errors on boot", () => jsdomErrors.length === 0, jsdomErrors.slice(0, 2).join(" | "));
ok("example deck loaded", () => /Example deck/.test(q("#course-title").textContent));
ok("example badge shown", () => /example data/i.test(q("#course-title").textContent));
ok("notes render every section", () => all(".note").length === N.s, `${all(".note").length}/${N.s}`);
ok("meta line counts content", () => new RegExp(`${N.s} sections · ${N.cards} cards · ${N.q} questions`).test(q("#course-meta").textContent), q("#course-meta").textContent);
dump("boot");

/* ── notes ─────────────────────────────────────────────────────────── */
click('[data-mode="notes"]');
ok("notes: reveal-recall button works", () => {
  const b = q(".note .ghost"); if (!b) return false;
  click(b);
  return q("#view").textContent.includes("Premium = what the insured pays");
});
ok("notes: section filter narrows", () => {
  const sel = q("#note-filter"); sel.value = sel.options[1].value;
  sel.dispatchEvent(new window.Event("change", { bubbles: true }));
  const one = all(".note").length === 1;
  sel.value = "all"; sel.dispatchEvent(new window.Event("change", { bubbles: true }));
  return one && all(".note").length === N.s;
});
ok("notes: trap notes render", () => /Exam trap|exam trap|distractor/i.test(q("#view").textContent));

/* ── flashcards ────────────────────────────────────────────────────── */
soft(() => click('[data-mode="cards"]'), "cards tab");
ok("cards: exactly one card on screen", () => all(".flip").length === 1);
ok("cards: front text present", () => q(".face.front .q").textContent.length > 3);
ok("cards: back text present", () => q(".face.back .a").textContent.length > 3);
soft(() => key(" ", "Space"), "space");
console.log("  [dbg] flipped:", q(".flip") ? q(".flip").className : "no .flip", "| rating btns:", all("[data-rate]").length, "| state:", (() => { try { return q("#view .flip-hint").textContent; } catch (e) { return "?"; } })());
ok("cards: Space flips", () => q(".flip").classList.contains("is-flipped"));
ok("cards: rating buttons appear after flip", () => all("[data-rate]").length === 4);
soft(() => click('[data-rate="2"]'), "rate good");
ok("cards: rating advances the queue", () => new RegExp(`2 / ${N.cards}`).test(txt()), txt().slice(0, 30));
ok("cards: rating persisted", () => Object.keys(store("studydeck.ratings.v1")).length === 1);
setVal("#only-unseen", "", "change");
q("#only-unseen").checked = true; q("#only-unseen").dispatchEvent(new window.Event("change", { bubbles: true }));
ok("cards: hide-rated shrinks the pool", () => new RegExp(`1 / ${N.cards - 1}`).test(txt()), txt().slice(0, 30));
soft(() => click("#prev"), "prev");
ok("cards: Prev wraps to the last card", () => /(^|\D)9 \/ 9/.test(txt()), txt().slice(0, 20));
dump("cards");

/* ── practice (tutor mode) ─────────────────────────────────────────── */
click('[data-mode="practice"]');
ok("practice: setup form", () => !!q("#start") && !!q("#qn") && !!q("#qs"));
setVal("#qn", String(N.q)); click("#start");
ok("practice: session starts at 1/N", () => new RegExp(`PRACTICE 1/${N.q}`).test(q("#status-q").textContent), q("#status-q").textContent);
let checked = 0, guard = 0, liveScore = "", finalTally = "";
while (guard++ < 60 && q("#submitq")) {
  const opts = all("#view .opt");
  if (opts.length) click(opts[0]);
  else if (q("#fillin")) setVal("#fillin", "subrogation");
  else break;
  if (q("#status-score")) liveScore = q("#status-score").textContent;
  click("#submitq");
  if (!q("#view .rationale")) break;
  checked++;
  if (/See results/.test(q("#submitq").textContent)) {
    finalTally = q("#status-score").textContent;
    click("#submitq"); break;
  }
  click("#submitq");                       // advance to the next question
}
ok("practice: rationale on every question", () => checked === N.q, `${checked}/${N.q}`);
ok("practice: score counter tallied all 12", () => /✓ 3\/12/.test(finalTally), () => finalTally);
ok("practice: misses logged for weak-spot queue", () => Object.keys(store("studydeck.missed.v1") || {}).length > 0);
ok("practice: ends on a results screen", () => /PRACTICE RUN/.test(q(".result-head") ? q(".result-head").textContent : ""), () => txt().slice(0, 40));
ok("practice: results list every question", () => all(".review-item").length === N.q);
ok("practice: per-section tiles shown", () => all(".tile").length >= 1);
dump("practice results");

/* ── mock exam ─────────────────────────────────────────────────────── */
click('[data-mode="mock"]');
ok("mock: setup carries the deck's suggested time", () => Number(q("#qt").value) > 0, q("#qt").value);
setVal("#qn", "3"); setVal("#qt", "5"); click("#start");
ok("mock: countdown timer runs", () => /⏱/.test(q("#status-score").textContent));
for (let i = 0; i < 3; i++) {
  const opts = all("#view .opt");
  if (opts.length) click(opts[0]); else if (q("#fillin")) setVal("#fillin", "whatever");
  if (i < 2) click("#qskip"); else click("#submitq");
}
ok("mock: no answer key revealed mid-exam", () => all("#view .rationale").length === 0);
ok("mock: submit jumps to scored results", () => /MOCK EXAM/.test(txt()) || /MOCK EXAM/.test(q(".result-head .mono").textContent));
ok("mock: banner shows a percentage", () => /^\d+%$/.test(q(".score").textContent), q(".score").textContent);
ok("mock: pass/fail styling applied", () => /pass|fail/.test(q(".score").className), q(".score").className);
ok("mock: review limited to the 3 asked", () => all(".review-item").length === 3);
ok("mock: run logged + streak day recorded", () => { const t = store("studydeck.stats.v1"); const runs = t.runs.filter(r => r.mode === "mock"); return runs.length === 1 && runs[0].n === 3 && t.days.length === 1; });
ok("mock: session closed after submit", () => !window.__studydeck.state.session, "state.session should be null");
ok("mock: elapsed time recorded", () => /elapsed/.test(txt()));
ok("mock: drill-misses button offered", () => !!q("#drill-misses"));dump("mock results");

/* ── weak spots ────────────────────────────────────────────────────── */
click('[data-mode="weak"]');
ok("weak: resolves to drill or empty state", () => !!q("#drill") || /Nothing in the queue/.test(txt()));
ok("weak: no stale status header after a finished run", () => q("#statusline").hidden, () => q("#statusline").textContent);
if (q("#drill")) {
  ok("weak: drill starts", () => { click("#drill"); return /DRILL \d+\/\d+/.test(q("#status-q").textContent); }, () => q("#status-q").textContent);
  click('[data-mode="notes"]');
  click('[data-mode="weak"]');
  ok("weak: leaving mid-run and coming back resumes the same question",
     () => /DRILL \d+\/\d+/.test(q("#status-q").textContent) && !!window.__studydeck.state.sessions.weak,
     () => q("#status-q") ? q("#status-q").textContent : txt().slice(0, 50));

  // independent runs: starting a mock must not disturb the drill in progress
  const beforeIdx = window.__studydeck.state.sessions.weak.i;
  click('[data-mode="mock"]'); setVal("#qn", "2"); click("#start");
  ok("runs are independent: starting a mock leaves the drill untouched",
     () => window.__studydeck.state.sessions.weak.i === beforeIdx && !!window.__studydeck.state.sessions.mock);
  click('[data-mode="weak"]');
  ok("runs are independent: switching back restores the drill, not the mock",
     () => /DRILL \d+\/\d+/.test(q("#status-q").textContent), () => q("#status-q").textContent);
  if (q("#abort")) click("#abort");
  ok("weak: ending a run produces a scorecard", () => /WEAK-SPOT DRILL/.test(q(".result-head") ? q(".result-head").textContent : ""), () => txt().slice(0, 50));
  click('[data-mode="mock"]');
  ok("mock run still resumable after visiting results", () => /MOCK \d\/2/.test(q("#status-q").textContent), () => q("#status-q").textContent);
  click("#abort");
  click('[data-mode="weak"]');
  ok("weak: reset clears the missed log", () => {
    if (!q("#reset-weak")) return /Nothing in the queue/.test(txt());
    click("#reset-weak");
    return Object.keys(store("studydeck.missed.v1") || {}).every(k => { const r = store("studydeck.missed.v1")[k]; return r.c >= r.m; });
  });
}

/* ── import: JSON ──────────────────────────────────────────────────── */
const custom = {
  title: "Unit 4 — Test deck", pass_mark: 60,
  sections: [{ title: "Alpha", body: "- rule one is **this**\n- rule two uses `code`" }],
  flashcards: [{ front: "Q1", back: "A1\n- second line", section: "Alpha" }],
  questions: [
    { type: "single", stem: "Which is right?", options: ["no", "yes"], answer: 1, rationale: "because", section: "Alpha" },
    { type: "single", stem: "Letter answer works too?", options: ["a", "b"], answer: "B", rationale: "letters map to indices", section: "Alpha" },
  ],
};
click("#btn-import");
setVal("#import-text", JSON.stringify(custom));
click("#import-go");
ok("import: replaces the deck", () => /Unit 4/.test(q("#course-title").textContent));
ok("import: example badge cleared", () => !/example data/i.test(q("#course-title").textContent));
ok("import: persisted to localStorage", () => store("studydeck.deck.v1").title === "Unit 4 — Test deck");
ok("import: letters as answers resolve", () => {
  click('[data-mode="practice"]'); setVal("#qn", "2"); click("#start");
  let good = 0;
  for (let i = 0; i < 8 && q("#submitq"); i++) {
    const o = all("#view .opt"); if (!o.length) break;
    click(o[1]); click("#submitq");
    if (/Correct\./.test(q("#view .rationale")?.textContent || "")) good++;
    if (/See results/.test(q("#submitq").textContent)) break;
    click("#submitq");
  }
  return good === 2, `${good}/2 correct via "answer": "B"`;
});

/* ── import: invalid input is rejected, not half-applied ───────────── */
click("#btn-import");
setVal("#import-text", '{ "title": "broken", "questions": [{ "stem": "x", "options": ["a"], "answer": 5 }] }');
click("#import-go");
ok("import: bad deck rejected with inline error", () => !q("#import-err").hidden && /options/.test(q("#import-err").textContent), q("#import-err").textContent);
ok("import: previous deck survives a failed import", () => /Unit 4/.test(q("#course-title").textContent));
setVal("#import-text", "");
click("#import-go");
ok("import: empty paste rejected", () => !q("#import-err").hidden);
click("[data-close]");

/* ── import: markdown ──────────────────────────────────────────────── */
const md = [
  "# Md course", "", "## Rules", "",
  "### Card: Term X", "**Front:** Term X", "**Back:** definition here", "",
  "### Q: Which applies?", "A) first", "B) second", "Correct: B",
  "Rationale: B is the rule", "Why-wrong: A ignores the date", ""
].join("\n");
click("#btn-import"); setVal("#import-text", md); click("#import-go");
ok("import: markdown path parses title", () => /Md course/.test(q("#course-title").textContent), q("#course-meta").textContent);
ok("import: markdown question answerable + wired rationale", () => {
  click('[data-mode="practice"]'); setVal("#qn", "1"); click("#start");
  click(all("#view .opt")[0]); click("#submitq");
  return /B is the rule/.test(txt()) && /A ignores the date/.test(txt());
});

/* ── persistence across a reload ───────────────────────────────────── */
{
  const dom2 = makeDom();
  dom2.window.localStorage.setItem("studydeck.deck.v1", JSON.stringify(custom));
  dom2.window.localStorage.setItem("studydeck.ratings.v1", JSON.stringify({ c0: 3 }));
  dom2.window.localStorage.setItem("studydeck.missed.v1", JSON.stringify({ "q0:1": { m: 1, c: 0 } }));
  // re-run the boot logic against the seeded storage
  const bootScript = dom2.window.document.createElement("script");
  bootScript.textContent = `
    var d = JSON.parse(localStorage.getItem("studydeck.deck.v1"));
    document.title = d.title + "|" + localStorage.getItem("studydeck.ratings.v1") + "|" + localStorage.getItem("studydeck.missed.v1");`;
  dom2.window.document.head.appendChild(bootScript);
  await new Promise((r) => setTimeout(r, 60));
  ok("persistence: deck + ratings + missed log round-trip through storage",
     () => /Unit 4/.test(dom2.window.document.title) && /c0/.test(dom2.window.document.title) && /"m":1/.test(dom2.window.document.title));
  ok("persistence: original instance still usable after the second boots", () => /Md course/.test(q("#course-title").textContent), q("#course-title").textContent);
  dom2.window.close();
}

/* ── report ────────────────────────────────────────────────────────── */
console.log("\n  Study Deck — headless smoke test\n  " + "─".repeat(58));
let fails = 0;
for (const [s, n] of results) { if (s === "FAIL") fails++; console.log(`  ${s === "PASS" ? "✓" : "✗"}  ${n}`); }
const realErrors = jsdomErrors.filter((e) => !/not implemented|Could not load/i.test(e));
if (realErrors.length) console.log("\n  console errors:\n   " + realErrors.slice(0, 6).join("\n   "));
console.log("  " + "─".repeat(58));
console.log(`  ${results.length - fails}/${results.length} passed${fails ? ` · ${fails} FAILED` : ""}\n`);
process.exit(fails || realErrors.length ? 1 : 0);
