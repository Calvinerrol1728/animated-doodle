// Study Deck — self-contained course-prep app.
// Modes: Notes (explanations) / Flashcards (self-rated) / Practice (tutor) / Mock exam (timed, scored) / Weak spots.
// Your material never leaves the page: it lives in localStorage under `studydeck.deck.v1`.

(function () {
  "use strict";

  var LS = {
    deck: "studydeck.deck.v1",
    example: "studydeck.deck.example.v1",
    ratings: "studydeck.ratings.v1",     // cardId -> 0..3 (again/hard/good/easy)
    missed: "studydeck.missed.v1",       // questionKey -> {m: misses, c: corrects}
    stats: "studydeck.stats.v1",         // {days:[iso], runs:[{at,mode,pct,n}]}
    ui: "studydeck.ui.v1"
  };

  // A run is stored per kind, so practice / mock / drill can each be left half-done and
  // resumed from its own tab without clobbering the others.
  function cur() { return state.sessions[state.mode] || null; }
  function setCur(sess) { if (state.mode === "notes" || state.mode === "cards" || state.mode === "results") return; state.sessions[state.mode] = sess; }

  // ---------------------------------------------------------------- utilities
  function readJSON(key, fallback) {
    try { var v = localStorage.getItem(key); return v ? JSON.parse(v) : fallback; }
    catch (e) { return fallback; }
  }
  function writeJSON(key, val) { try { localStorage.setItem(key, JSON.stringify(val)); } catch (e) {} }
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function clamp(n, lo, hi) { return Math.max(lo, Math.min(hi, n)); }
  function today() { return new Date().toISOString().slice(0, 10); }
  function fmtMMSS(sec) {
    sec = Math.max(0, Math.round(sec));
    var m = Math.floor(sec / 60), s = sec % 60;
    return m + ":" + (s < 10 ? "0" : "") + s;
  }
  // Lightweight inline markdown: **bold**, `code`, - lists, blank-line paragraphs.
  function rich(text) {
    if (text == null) return "";
    var lines = String(text).replace(/\r/g, "").split("\n");
    var out = [], inList = false;
    lines.forEach(function (raw) {
      var line = raw.trim();
      var isBullet = /^[-*•]\s+/.test(line);
      if (inList && !isBullet) { out.push("</ul>"); inList = false; }
      if (isBullet) {
        if (!inList) { out.push("<ul>"); inList = true; }
        out.push("<li>" + inline(line.replace(/^[-*•]\s+/, "")) + "</li>");
        return;
      }
      if (!line) return;
      out.push("<p>" + inline(line) + "</p>");
    });
    if (inList) out.push("</ul>");
    return out.join("");
  }
  function inline(s) {
    return esc(s)
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
      .replace(/__([^_]+)__/g, "<b>$1</b>");
  }
  function normAnswer(s) {
    return String(s).toLowerCase()
      .replace(/[’‘`"]/g, "")
      .replace(/[^a-z0-9%.\- ]+/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }
  function answersMatch(given, acceptedList) {
    var g = normAnswer(given);
    if (!g) return false;
    return acceptedList.some(function (acc) {
      var a = normAnswer(acc);
      if (!a) return false;
      if (a === g) return true;
      // accept when every required token is present (handles "30 days" vs "thirty (30) days")
      var tokens = a.split(/[,;]/).map(function (t) { return t.trim(); }).filter(Boolean);
      if (tokens.length > 1 && tokens.every(function (t) { return g.indexOf(normAnswer(t)) >= 0; })) return true;
      return a.length > 4 && g.length > 4 && (g.indexOf(a) >= 0 || a.indexOf(g) >= 0);
    });
  }

  // ---------------------------------------------------------------- deck store
  var state = {
    mode: "notes",
    deck: null,
    sessions: {},
    isExample: false,
    filter: { section: "all", onlyUnseen: false },
    cards: { idx: 0, flipped: false },
    results: null,          // last finished scorecard
    ratings: readJSON(LS.ratings, {}),
    missed: readJSON(LS.missed, {}),
    stats: readJSON(LS.stats, { days: [], runs: [] })
  };

  function normalizeDeck(d) {
    if (!d || typeof d !== "object") throw new Error("Deck must be a JSON object.");
    if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = parseMarkdown(d); } }
    if (!Array.isArray(d.sections)) d.sections = [];
    if (!Array.isArray(d.flashcards)) d.flashcards = [];
    if (!Array.isArray(d.questions)) d.questions = [];
    if (!d.title) d.title = "Untitled course";
    var sectNames = d.sections.map(function (s) { return s.title; })
      .concat(d.flashcards.map(function (c) { return c.section || ""; }))
      .concat(d.questions.map(function (q) { return q.section || ""; }));
    d._sections = Array.from(new Set(sectNames.filter(Boolean)));
    d.flashcards.forEach(function (c, i) {
      c.id = c.id || ("c" + i);
      if (!c.front || !c.back) throw new Error("flashcards[" + i + "] needs `front` and `back`.");
    });
    d.questions.forEach(function (q, i) {
      q._i = i;
      q.type = (q.type || "single").toLowerCase();
      if (q.type === "multiple" || q.type === "multi") q.type = "multiple";
      if (q.type === "boolean" || q.type === "yesno") q.type = "truefalse";
      q.key = q.id || ("q" + i + ":" + String(q.stem || "").slice(0, 24));
      if (!q.stem) throw new Error("questions[" + i + "] needs a `stem`.");
      if (q.type === "single" || q.type === "multiple") {
        if (!Array.isArray(q.options) || q.options.length < 2) throw new Error("questions[" + i + "] needs ≥2 `options`.");
        var raw = [].concat(q.answer != null ? q.answer : [], q.answers || []);
        var idxs = raw.map(function (x) {
          if (typeof x === "string" && /^[a-fA-F]$/.test(x.trim())) return x.trim().toUpperCase().charCodeAt(0) - 65;  // "B" -> 1
          return Number(x);
        }).filter(function (n) { return n >= 0 && n < q.options.length; });
        if (!idxs.length) { q.type = "single"; q.options = []; return; }
        if (!idxs.length) throw new Error("questions[" + i + "] `answer` index is out of range.");
        q._answerIdx = Array.from(new Set(idxs)).sort();
        if (q.type === "single" && q._answerIdx.length > 1) q.type = "multiple";
        if (q._answerIdx.length > 1) q.type = "multiple";
      } else if (q.type === "truefalse") {
        q._answerBool = (q.answer === true || q.answer === "true" || q.answer === "yes" || q.answer === 1);
      } else if (q.type === "fillin") {
        q._accept = Array.isArray(q.answer) ? q.answer : [q.answer != null ? q.answer : q.answers];
        var acc = []; q._accept.forEach(function (x) { acc = acc.concat(x); });
        q._accept = acc.filter(function (x) { return x != null && x !== ""; }).map(String);
        if (!q._accept.length) throw new Error("questions[" + i + "] fill-in needs an `answer` string.");
      } else {
        throw new Error("questions[" + i + "]: unknown type `" + q.type + "`.");
      }
    });
    return d;
  }

  // Tolerant markdown-ish import: ## Section / ### Card -> **Front:** … **Back:** … / ### Q: … A) … Correct: X
  function parseMarkdown(text) {
    var deck = { title: "Imported deck", sections: [], flashcards: [], questions: [] };
    var section = null, mode = null, cur = null, buf = [];
    function flushCard() {
      if (!cur || mode !== "card") return;
      if (cur._side) cur[cur._side] = buf.join("\n").trim();
      if (cur.front && cur.back) deck.flashcards.push({ front: cur.front, back: cur.back, section: section });
      cur = null; buf = [];
    }
    function flushQ() {
      if (!cur || mode !== "q") return;
      var q = { stem: cur.stem || "", section: section };
      if (cur.type === "fillin") { q.type = "fillin"; q.answer = cur.answerText || ""; }
      else if (cur.type === "truefalse") { q.type = "truefalse"; q.answer = cur.answerBool; }
      else {
        q.type = cur.correct.length > 1 ? "multiple" : "single";
        q.options = cur.options; q.answer = cur.correct;
      }
      if (cur.rationale) q.rationale = cur.rationale;
      if (cur.why) q.why_wrong = cur.why;
      if (q.stem) deck.questions.push(q);
      cur = null; buf = [];
    }
    text.replace(/\r/g, "").split("\n").forEach(function (raw) {
      var line = raw.trim();
      var h = /^(#{1,4})\s+(.*)$/.exec(line);
      if (h) {
        var depth = h[1].length, txt = h[2].trim();
        if (depth === 1) { deck.title = txt.replace(/^title:?\s*/i, ""); return; }
        var isQ = /^q\b\s*[:\-]?\s*/i.test(txt) || /\?\s*$/.test(txt);   // `\b` alone also fires on "Quality of care?" — keep the marker narrow
        isQ = /^(?:q\b\s*[:\-]?\s*)/i.test(txt) || /\?\s*$/.test(txt);
        var isCardH = !isQ && /^(card|term)\b\s*[:\-]?\s*/i.test(txt);
        if (depth === 2 && !isQ && !isCardH) { flushCard(); flushQ(); mode = null; section = txt; deck.sections.push({ title: txt, body: "" }); return; }
        flushCard(); flushQ();
        if (isQ) { mode = "q"; cur = { type: "single", options: [], correct: [], stem: txt.replace(/^q\b\s*[:\-]?\s*/i, "") }; }
        else { mode = "card"; cur = {}; var lbl = txt.replace(/^(card|term)\b\s*[:\-]?\s*/i, ""); if (lbl) cur.front = lbl; }
        if (mode === "card" && /^\*\*front:?\*\*/i.test(txt)) cur._side = "front";
        if (mode === "card" && /^\*\*back:?\*\*/i.test(txt)) cur._side = "back";
        return;
      }
      if (!line) return;
      if (mode === "card" && cur) {
        var f = /^\*\*front:?\*\*\s*(.*)$/i.exec(line), b = /^\*\*back:?\*\*\s*(.*)$/i.exec(line);
        if (f) { if (cur._side) cur[cur._side] = buf.join("\n").trim(); buf = []; cur._side = "front"; if (f[1]) buf.push(f[1]); return; }
        if (b) { if (cur._side) cur[cur._side] = buf.join("\n").trim(); buf = []; cur._side = "back"; if (b[1]) buf.push(b[1]); return; }
        buf.push(line); return;
      }
      if (mode === "q" && cur) {
        var opt = /^([A-Fa-f1-9])[\.\)]\s+(.*)$/.exec(line);
        if (opt) { cur.options.push(opt[2]); return; }
        var cor = /^correct:?\s*(.*)$/i.exec(line);
        if (cor) {
          var v = cor[1].trim();
          if (/^(true|false|yes|no)$/i.test(v)) { cur.type = "truefalse"; cur.answerBool = /^(true|yes)$/i.test(v); }
          else if (/^fill/i.test(v)) { cur.type = "fillin"; }
          else {
            cur.correct = v.split(/[\s,]+/).map(function (t) {
              t = t.trim().replace(/[A-F]\)/g, "");
              var letter = /^[a-fA-F]$/.test(t) ? t.toUpperCase().charCodeAt(0) - 65 : parseInt(t, 10) - 1;
              return letter;
            }).filter(function (n) { return n >= 0 && n < (cur.options.length || 26); });
            if (!cur.correct.length) cur.correct = [0];
          }
          return;
        }
        var rat = /^rationale:?\s*(.*)$/i.exec(line);
        if (rat) { cur.rationale = rat[1]; return; }
        var why = /^why:?wrong:?\s*(.*)$/i.exec(line) || /^why:?-?wrong:?\s*(.*)$/i.exec(line);
        if (why) { cur.why = why[1]; return; }
        var ans = /^answer:?\s*(.*)$/i.exec(line);
        if (ans) { cur.type = "fillin"; cur.answerText = ans[1]; return; }
        if (cur.type === "fillin") { cur.answerText = (cur.answerText ? cur.answerText + ", " : "") + line; return; }
        if (!cur.stem) cur.stem = line; else cur.rationale = (cur.rationale ? cur.rationale + " " : "") + line;
      }
    });
    if (mode === "card") flushCard(); else flushQ();
    if (!deck.sections.length && !deck.flashcards.length && !deck.questions.length) {
      throw new Error("Nothing recognised. Use `## Section`, `### Card` with **Front:**/**Back:**, and `### Q:` with `A)` … `Correct: B`. Or just paste JSON.");
    }
    return deck;
  }

  function applyDeck(raw, opts) {
    var text = typeof raw === "string" ? raw : JSON.stringify(raw);
    var parsed;
    try {
      parsed = typeof raw === "string" ? (JSON.parse(raw)) : raw;
    } catch (e) {
      parsed = parseMarkdown(text);
    }
    state.deck = normalizeDeck(parsed);
    state.isExample = !!(opts && opts.example);
    writeJSON(LS.deck, state.deck);
    writeJSON(LS.example, state.isExample);
    state.cards.idx = 0; state.cards.flipped = false;
    state.sessions = {}; state.results = null; state.drillView = false;
    if (state.mode === "mock" || state.mode === "practice" || state.mode === "weak") state.mode = "notes";
    render();
  }

  // ---------------------------------------------------------------- stats
  function touchDay() {
    var t = today();
    if (state.stats.days.indexOf(t) < 0) { state.stats.days.push(t); writeJSON(LS.stats, state.stats); }
  }
  function streakDays() {
    var set = new Set(state.stats.days), n = 0, d = new Date();
    if (!set.has(d.toISOString().slice(0, 10))) d.setDate(d.getDate() - 1);
    while (set.has(d.toISOString().slice(0, 10))) { n++; d.setDate(d.getDate() - 1); }
    return n;
  }
  function logRun(mode, pct, n) {
    state.stats.runs.push({ at: Date.now(), mode: mode, pct: pct, n: n });
    if (state.stats.runs.length > 60) state.stats.runs = state.stats.runs.slice(-60);
    writeJSON(LS.stats, state.stats);
    touchDay();
  }

  function missedOf(q) { var r = state.missed[q.key] || { m: 0, c: 0 }; return r.m > r.c; }
  function scoreMissed(q, correct) {
    var r = state.missed[q.key] || { m: 0, c: 0 };
    if (correct) { r.c++; if (r.m > r.c) r.m = r.c + 1; } else { r.m++; }
    state.missed[q.key] = r; writeJSON(LS.missed, state.missed);
  }
  function weakQueue() {
    if (!state.deck) return [];
    return state.deck.questions.filter(missedOf);
  }

  // ---------------------------------------------------------------- render: shell
  var view = document.getElementById("view");
  var statusline = document.getElementById("statusline");
  var tabs = document.getElementById("tabs");

  function render() {
    var d = state.deck;
    var titleEl = document.getElementById("course-title");
    titleEl.innerHTML = d ? esc(d.title) + (state.isExample ? '<span class="badge-example">example data</span>' : "") : "Untitled course";
    var meta = "no material loaded";
    if (d) {
      meta = d.sections.length + " sections · " + d.flashcards.length + " cards · " + d.questions.length + " questions";
      if (d.subtitle) meta = esc(d.subtitle) + " — " + meta;
      else meta = " — " + meta;
    }
    document.getElementById("course-meta").innerHTML = meta;
    var st = streakDays();
    document.getElementById("streak").textContent = st ? st + "d" : "·";
    Array.prototype.forEach.call(tabs.querySelectorAll(".tab"), function (t) {
      t.classList.toggle("is-active", t.dataset.mode === state.mode);
    });
    var wq = weakQueue().length;
    var wEl = document.getElementById("weak-count");
    wEl.textContent = wq; wEl.classList.toggle("hot", wq > 0);

    if (!d) { renderEmpty(); return; }
    var needs = !d.sections.length && !d.flashcards.length && !d.questions.length;
    if (needs) { renderEmpty("This deck is empty."); return; }

    stopTimer();
    if (state.mode !== "practice" && state.mode !== "mock" && !(state.mode === "weak" && state.drillView)) hideStatus();
    if (state.mode === "results") { renderResults(); return; }
    if (state.mode === "notes") renderNotes();
    else if (state.mode === "cards") renderCards();
    else if (state.mode === "practice") cur() ? renderSession() : renderQuizSetup("practice");
    else if (state.mode === "mock") cur() ? renderSession() : renderQuizSetup("mock");
    else if (state.mode === "weak") {
      if (cur()) { if (state.drillView) { renderSession(); return; } state.drillView = true; renderSession(); return; }
      state.drillView = false;
      renderWeakIntro(wq);
    }
  }

  function hideStatus() {
    statusline.hidden = true;
    statusline.innerHTML = "";
  }
  function renderEmpty(msg) {
    view.innerHTML =
      '<div class="empty"><div class="big">🗂</div><h3>' + (msg || "No course material loaded") + '</h3>' +
      '<p>Put your own notes in <code>data/deck.json</code>, or paste them via <b>Paste / import material</b>.<br>' +
      'Everything stays in this browser — nothing is uploaded.</p>' +
      '<p class="row" style="justify-content:center"><button class="primary" id="go-import" type="button">Paste material</button>' +
      '<button class="ghost" id="go-example" type="button">Load example deck</button></p></div>';
    document.getElementById("go-import").onclick = openImport;
    document.getElementById("go-example").onclick = function () { loadExample(true); };
  }

  // ---------------------------------------------------------------- render: notes
  function renderNotes() {
    var d = state.deck, wrap = el("div");
    var intro = el("div", "card-shell");
    intro.innerHTML =
      '<div class="row" style="justify-content:space-between"><div class="muted small">' +
      '<b style="color:var(--ink)">Study notes</b> — written so the logic sticks, not for rote memorising. ' +
      'Each section ends with “exam trap” notes on why near-miss answers are wrong.</div>' +
      '<div class="row"><select id="note-filter"></select><button class="ghost" id="btn-toggle-all" type="button">Expand all</button></div></div>';
    wrap.appendChild(intro);

    var sel = intro.querySelector("#note-filter");
    sel.appendChild(new Option("All sections", "all"));
    d._sections.forEach(function (s) { sel.appendChild(new Option(s, s)); });
    sel.value = state.filter.section;
    sel.onchange = function () { state.filter.section = sel.value; render(); };

    var any = false;
    d.sections.forEach(function (s) {
      if (state.filter.section !== "all" && state.filter.section !== s.title) return;
      any = true;
      var n = el("div", "note");
      var body = s.body || (s.points || []).map(function (p) { return typeof p === "string" ? "- " + p : "- **" + p.point + "** — " + (p.why || ""); }).join("\n");
      n.innerHTML = "<h3>" + inline(s.title) + "</h3>" + rich(body);
      var cards = d.flashcards.filter(function (c) { return !s.title || c.section === s.title; });
      if (cards.length) {
        n.appendChild(el("div", "why", "<b>Recall prompts for this section</b>"));
        cards.slice(0, 8).forEach(function (c) {
          var row = el("div", "row", '<span class="mono">→</span> <span>' + inline(c.front) + "</span>");
          row.style.gap = "8px";
          var b = el("button", "ghost", "reveal");
          b.style.cssText = "padding:2px 8px;font-size:11.5px;margin-left:auto";
          b.onclick = function () {
            row.insertAdjacentHTML("afterend", '<p class="small" style="color:var(--ink-dim);margin:2px 0 8px 26px">' + rich(c.back) + "</p>");
            row.nextElementSibling.appendChild(b); b.remove(); row.remove();
          };
          row.appendChild(b);
          n.appendChild(row);
        });
      }
      wrap.appendChild(n);
    });
    if (!any) wrap.appendChild(el("p", "muted", "No notes in this deck yet — questions and cards only."));
    view.innerHTML = ""; view.appendChild(wrap);
  }

  // ---------------------------------------------------------------- render: flashcards
  function renderCards() {
    var d = state.deck;
    var all = d.flashcards.filter(function (c) {
      if (state.filter.section !== "all" && (c.section || "") !== state.filter.section) return false;
      if (state.filter.onlyUnseen && (state.ratings[c.id] || 0) > 0) return false;
      return true;
    });
    if (all.length) {                                    // resolve the position before painting the counter
      if (state.cards.idx < 0) state.cards.idx = all.length - 1;
      else if (state.cards.idx > all.length - 1) state.cards.idx = 0;
      state.cards.idx = clamp(state.cards.idx, 0, all.length - 1);
    }
    var bar = el("div", "card-shell");
    bar.style.padding = "12px 16px";
    var seen = all.filter(function (c) { return (state.ratings[c.id] || 0) >= 2; }).length;
    bar.innerHTML =
      '<div class="row" style="justify-content:space-between"><span class="mono">' +
      (all.length ? (state.cards.idx + 1) : 0) + " / " + all.length + "</span>" +
      '<span class="muted small">' + seen + " rated solid · <span class='kbd'>Space</span> flip · <span class='kbd'>1-4</span> rate · <span class='kbd'>←/→</span> move</span>" +
      '<div class="row"><select id="card-filter"></select>' +
      '<label class="small muted" style="display:flex;gap:6px;align-items:center;cursor:pointer"><input type="checkbox" id="only-unseen" ' +
      (state.filter.onlyUnseen ? "checked" : "") + "> hide rated</label></div></div>";
    view.innerHTML = "";
    view.appendChild(bar);

    var sel = bar.querySelector("#card-filter");
    sel.appendChild(new Option("All sections", "all"));
    d._sections.forEach(function (s) { sel.appendChild(new Option(s, s)); });
    sel.value = state.filter.section;
    sel.onchange = function () { state.filter.section = sel.value; state.cards.idx = 0; render(); };
    bar.querySelector("#only-unseen").onchange = function (e) { state.filter.onlyUnseen = e.target.checked; state.cards.idx = 0; render(); };

    if (!all.length) {
      view.appendChild(el("div", "empty", "<h3>No cards here</h3><p>Add <code>flashcards</code> to your deck, or clear the filters.</p>"));
      return;
    }
    if (state.cards.idx < 0) state.cards.idx = all.length - 1;      // wrap backwards
    else if (state.cards.idx > all.length - 1) state.cards.idx = 0;  // wrap forwards
    state.cards.idx = clamp(state.cards.idx, 0, Math.max(0, all.length - 1));
    var c = all[state.cards.idx];
    var flip = el("div", "flip" + (state.cards.flipped ? " is-flipped" : ""));
    flip.innerHTML =
      '<div class="flip-inner">' +
      '<div class="face front"><div class="tag">' + esc(c.section || "card") + "</div><div class='q'>" + inline(c.front) + "</div></div>" +
      '<div class="face back"><div class="tag">answer</div><div class="a">' + rich(c.back) + "</div></div>" +
      '<span class="flip-hint">' + (state.cards.flipped ? "" : "click to flip") + "</span></div>";
    function toggleFlip() { state.cards.flipped = !state.cards.flipped; render(); }
    flip.onclick = function (e) { if (!e.target.closest("button")) toggleFlip(); };
    flip.tabIndex = 0;
    view.appendChild(flip);

    var act = el("div", "row");
    act.style.justifyContent = "space-between";
    if (!state.cards.flipped) {
      act.innerHTML = '<button class="ghost" id="prev" type="button">←</button>' +
        '<button class="primary" id="flipbtn" type="button">Flip answer</button>' +
        '<button class="ghost" id="next" type="button">→</button>';
    } else {
      act.innerHTML = '<button class="ghost" id="prev" type="button">←</button>' +
        '<div class="row">' +
        '<button class="danger" data-rate="0" type="button">1 · Again</button>' +
        '<button class="ghost" data-rate="1" type="button">2 · Hard</button>' +
        '<button class="ghost" data-rate="2" type="button">3 · Good</button>' +
        '<button class="primary" data-rate="3" type="button">4 · Easy</button></div>' +
        '<button class="ghost" id="next" type="button">→</button>';
    }
    view.appendChild(act);
    var pv = act.querySelector("#prev"), nx = act.querySelector("#next"), fb = act.querySelector("#flipbtn");
    if (pv) pv.onclick = function () { bumpCard(-1); };
    if (nx) nx.onclick = function () { bumpCard(1); };
    if (fb) fb.onclick = function () { state.cards.flipped = true; render(); };
    Array.prototype.forEach.call(act.querySelectorAll("[data-rate]"), function (b) {
      b.onclick = function () {
        var v = Number(b.dataset.rate);
        state.ratings[c.id] = v;
        if (v >= 2 && c.linkedQuestion != null) { var q = d.questions[c.linkedQuestion]; if (q) scoreMissed(q, true); }
        writeJSON(LS.ratings, state.ratings);
        touchDay();
        bumpCard(1);
      };
    });
  }
  function bumpCard(delta) {
    state.cards.flipped = false;
    state.cards.idx = state.cards.idx + delta;   // renderCards clamps into the filtered list
    render();
  }

  // ---------------------------------------------------------------- render: quiz setup
  function renderQuizSetup(kind) {
    var d = state.deck;
    var pool = kind === "weak" ? weakQueue() : d.questions;
    var isMock = kind === "mock";
    var max = pool.length;
    var shell = el("div", "card-shell");
    shell.innerHTML =
      "<h2 class='sec' style='margin-top:0'>" + (isMock ? "Mock exam setup" : "Practice setup") + " <span>" +
      (isMock ? "· answers are held until you submit, like the real thing" : "· instant feedback with rationales") + "</span></h2>" +
      '<div class="two">' +
      '<label class="f"><span>Number of questions (' + max + " available)</span><input type='number' id='qn' min='1' max='" + max + "' value='" + (isMock ? Math.min(20, max) : Math.min(12, max)) + "'></label>" +
      '<label class="f"><span>Time limit (minutes, 0 = none)</span><input type="number" id="qt" min="0" max="240" value="' + (isMock ? (d.suggested_time_minutes || 20) : 0) + '"></label>' +
      '<label class="f"><span>Section</span><select id="qs"></select></label>' +
      '<label class="f"><span>Order</span><select id="qo"><option value="shuffle">Randomise (like a real bank)</option><option value="source">Course order</option></select></label>' +
      "</div>" +
      (isMock ? '<p class="hint">Pass mark used for the banner is the one in your deck (<code>pass_mark</code>, default 70%). ' +
        "Your real course's pass mark is whatever your LMS says — check it, don't guess.</p>" : "") +
      '<div class="row-end"><button class="primary" id="start" type="button">Start ' + (isMock ? "mock" : "practice") + "</button></div>";
    view.innerHTML = ""; view.appendChild(shell);
    var sel = shell.querySelector("#qs");
    sel.appendChild(new Option("All sections", "all"));
    d._sections.forEach(function (s) { sel.appendChild(new Option(s, s)); });
    sel.onchange = function () { state.filter.section = sel.value; };
    sel.value = state.filter.section;
    shell.querySelector("#start").onclick = function () {
      var filtered = pool.filter(function (q) { return sel.value === "all" || (q.section || "") === sel.value; });
      if (!filtered.length) return;
      var n = clamp(Number(shell.querySelector("#qn").value) || filtered.length, 1, filtered.length);
      var mins = clamp(Number(shell.querySelector("#qt").value) || 0, 0, 240);
      var ordered = shell.querySelector("#qo").value === "shuffle" ? shuffle(filtered) : filtered.slice();
      state.results = null;
      startSession({ kind: kind, items: ordered.slice(0, n), minutes: mins });
    };
  }

  function renderWeakIntro(n) {
    n = (n == null) ? weakQueue().length : n;
    state.results = null;
    var shell = el("div", "card-shell");
    shell.innerHTML = "<h2 class='sec' style='margin-top:0'>Weak spots <span>· " + n +
      " question(s) you have missed more often than you have nailed</span></h2>" +
      "<p class='muted'>This queue is built from your own misses, not from an answer key. Clear it by answering each one correctly — or reset it below.</p>" +
      '<div class="row-end"><button class="ghost" id="reset-weak" type="button">Reset missed log</button>' +
      '<button class="primary" id="drill" type="button">Drill them now</button></div>';
    view.innerHTML = ""; view.appendChild(shell);
    shell.querySelector("#drill").onclick = function () {
      state.results = null;
      state.drillView = true;
      startSession({ kind: "weak", items: shuffle(weakQueue()), minutes: 0 });
    };
    shell.querySelector("#reset-weak").onclick = function () { state.missed = {}; writeJSON(LS.missed, state.missed); render(); };
  }
  function renderWeakEmpty() {
    view.innerHTML = "";
    var s = el("div", "card-shell");
    s.innerHTML = "<h2 class='sec' style='margin-top:0'>Weak spots</h2><p>Nothing in the queue — you have not missed anything twice. " +
      "Run a practice set and the misses will collect here for targeted drilling.</p>";
    view.appendChild(s);
  }

  // ---------------------------------------------------------------- session engine
  function startSession(cfg) {
    cfg = cfg || {};
    if (cfg.resume && cur() && cur().kind === cfg.kind) { state.results = null; render(); return; }
    var sess = {
      kind: cfg.kind, items: cfg.items, i: 0, minutes: cfg.minutes || 0,
      startedAt: Date.now(), left: (cfg.minutes || 0) * 60,
      picks: cfg.items.map(function () { return []; }),
      total: 0, scoreCorrect: 0, revealed: false, lastRevealed: -1
    };
    state.results = null;
    state.sessions[cfg.kind] = sess;
    if (cfg.minutes) startTimer();
    render();
  }
  function startTimer() {
    var run = cur(); if (!run) return;
    stopTimer();
    run.timer = setInterval(function () {
      var r = cur();
      if (!r) { stopTimer(); return; }
      r.left--;
      paintTimer();
      if (r.left <= 0) { finishSession(true); }
    }, 1000);
  }
  function stopTimer() {
    Object.keys(state.sessions).forEach(function (k) {
      var r = state.sessions[k];
      if (r && r.timer) { clearInterval(r.timer); r.timer = null; }
    });
  }
  function paintTimer() {
    var t = document.getElementById("timer");
    if (!t || !cur()) return;
    var s = cur().left;
    t.textContent = "⏱ " + fmtMMSS(s);
    t.className = "timer" + (s <= 60 ? " bad" : s <= 300 ? " warn" : "");
    t.title = s <= 0 ? "time up" : "remaining";
  }

  function renderStatus() {
    var s = cur();
    if (!document.getElementById("status-q")) {
      statusline.innerHTML = '<strong id="status-q"></strong><div class="bar"><i id="status-bar"></i></div><span id="status-score" class="mono"></span>';
    }
    statusline.hidden = false;
    document.getElementById("status-q").textContent =
      (s.kind === "mock" ? "MOCK " : s.kind === "weak" ? "DRILL " : "PRACTICE ") + (s.i + 1) + "/" + s.items.length;
    document.getElementById("status-bar").style.width = ((s.i) / s.items.length * 100) + "%";
    var answered = s.picks.filter(function (p) { return p.length; }).length;
    document.getElementById("status-score").innerHTML =
      (s.kind === "mock" ? "<span id='timer'>⏱ " + fmtMMSS(s.left) + "</span> · " : "") +
      "answered " + answered + "/" + s.items.length +
      (s.kind !== "mock" && s.total ? " · ✓ " + s.scoreCorrect + "/" + s.total : "");
    if (s.kind === "mock") paintTimer();
  }

  function renderSession() {
    var s = cur(), q = s.items[s.i];
    renderStatus();
    view.innerHTML = "";
    var shell = el("div", "card-shell");

    var typeTag = q.type === "multiple" ? "select all that apply" : q.type === "truefalse" ? "true / false" : q.type === "fillin" ? "short answer" : "single answer";
    shell.appendChild(el("div", "qstem", '<span class="qtype">' + typeTag + "</span>" + inline(q.stem)));
    if (q.section) shell.appendChild(el("div", "mono", q.section));

    var answered = s.picks[s.i] || [];
    var revealed = s.kind !== "mock" && s.revealed && s.i === s.lastRevealed;

    if (q.type === "fillin") {
      var inp = el("input", "fillin");
      inp.type = "text"; inp.placeholder = "type your answer…"; inp.id = "fillin";
      inp.value = answered[0] || "";
      if (revealed) { inp.disabled = true; inp.classList.add(answersMatch(answered[0], q._accept) ? "is-correct" : "is-wrong"); }
      shell.appendChild(inp);
      inp.addEventListener("input", function () { s.picks[s.i] = inp.value ? [inp.value] : []; });
      inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); revealOrNext(); } });
    } else if (q.type === "truefalse") {
      var row = el("div", "tf row");
      [true, false].forEach(function (v) {
        var b = el("button", "opt", "<span>" + (v ? "True" : "False") + "</span>");
        b.type = "button";
        var picked = answered.indexOf(String(v)) >= 0;
        if (picked) b.classList.add("is-picked");
        if (revealed) {
          b.disabled = true;
          var right = v === q._answerBool, chosen = picked;
          if (right) b.classList.add("is-correct");
          else if (chosen) b.classList.add("is-wrong");
        }
        b.onclick = function () { s.picks[s.i] = [String(v)]; render(); };
        row.appendChild(b);
      });
      shell.appendChild(row);
    } else {
      var multi = q.type === "multiple";
      q.options.forEach(function (opt, i) {
        var b = el("button", "opt" + (multi ? " is-multi" : ""), "");
        b.type = "button";
        b.innerHTML = (multi ? '<span class="box"></span>' : "") +
          '<span class="key">' + String.fromCharCode(65 + i) + "</span><span>" + inline(opt) + "</span>";
        var picked = answered.indexOf(i) >= 0;
        if (picked) b.classList.add("is-picked");
        if (revealed) {
          b.disabled = true;
          var right = q._answerIdx.indexOf(i) >= 0;
          if (right) b.classList.add("is-correct");
          else if (picked) b.classList.add("is-wrong");
        }
        b.onclick = function () {
          if (revealed) return;
          if (multi) {
            var a = s.picks[s.i].slice();
            var at = a.indexOf(i);
            if (at >= 0) a.splice(at, 1); else a.push(i);
            s.picks[s.i] = a.sort();
          } else s.picks[s.i] = [i];
          render();
        };
        shell.appendChild(b);
      });
    }

    if (revealed) {
      var ok = checkAnswer(q, s.picks[s.i]);
      var why = q.why_wrong || q.whyWrong || q.distractors;
      var html = '<div class="rationale' + (ok ? "" : " neg") + '"><b>' + (ok ? "Correct." : "Not correct.") + "</b> ";
      html += "<b>Answer:</b> " + inline(answerText(q)) + ". " + (q.rationale ? inline(q.rationale) : "");
      if (!ok && why) html += " <div style='margin-top:8px'><b>Why the near-miss option fails:</b> " + inline(why) + "</div>";
      html += "</div>";
      if (!ok && !why && q.type === "single") {
        var wrong = q.options.map(function (o, i) { return { o: o, i: i }; })
          .filter(function (x) { return q._answerIdx.indexOf(x.i) < 0 && s.picks[s.i].indexOf(x.i) >= 0; });
        if (wrong.length) html += '<p class="small muted">You chose “' + inline(wrong[0].o) + "”. If the deck has no rationale for this one, add one under <code>why_wrong</code> in <code>data/deck.json</code> — writing your own is the best 30 seconds of studying there is.</p>";
      }
      shell.appendChild(el("div", "", html));
    }

    var nav = el("div", "row");
    nav.style.justifyContent = "space-between";
    nav.style.marginTop = "6px";
    nav.innerHTML =
      '<div class="row"><button class="ghost" id="qprev" type="button">← Prev</button>' +
      '<button class="ghost" id="qskip" type="button">' + (s.kind === "mock" ? "Next →" : "Skip") + "</button>" +
      '<button class="ghost" id="giveup" type="button">Show answer</button></div>' +
      '<div class="row"><button class="ghost" id="abort" type="button">End run</button>' +
      '<button class="primary" id="submitq" type="button">' +
      (s.kind === "mock" ? (s.i === s.items.length - 1 ? "Submit exam" : "Next →") : (revealed ? (s.i === s.items.length - 1 ? "See results" : "Next →") : "Check answer")) +
      "</button></div>";
    shell.appendChild(nav);
    view.appendChild(shell);

    shell.querySelector("#qprev").onclick = function () { s.revealed = false; s.i = clamp(s.i - 1, 0, s.items.length - 1); render(); };
    shell.querySelector("#qskip").onclick = function () { advance(); };
    shell.querySelector("#giveup").onclick = function () { s.revealed = true; s.lastRevealed = s.i; s.scoreCorrect = s.scoreCorrect || 0; scoreMissed(q, false); render(); };
    shell.querySelector("#abort").onclick = function () { finishSession(false); };
    shell.querySelector("#submitq").onclick = function () { s.kind === "mock" ? (s.i === s.items.length - 1 ? finishSession(false) : advance()) : (revealed ? advance() : revealOrNext()); };

    var f = shell.querySelector("#fillin");
    if (f && !revealed) setTimeout(function () { f.focus(); }, 30);
  }

  function revealOrNext() {
    var s = cur(), q = s.items[s.i];
    if (s.kind === "mock") { advance(); return; }
    if (s.revealed && s.i === s.lastRevealed) { advance(); return; }
    var picks = s.picks[s.i] || [];
    var has = q.type === "fillin" ? !!(picks[0] || "").trim() : picks.length > 0;
    if (!has) { flashPick(); return; }
    var ok = checkAnswer(q, picks);
    s.revealed = true; s.lastRevealed = s.i;
    s.total = (s.total || 0) + 1;
    s.scoreCorrect = (s.scoreCorrect || 0) + (ok ? 1 : 0);
    scoreMissed(q, ok);
    touchDay();
    render();
  }
  function flashPick() {
    var n = view.querySelector(".qstem");
    if (!n) return;
    n.animate([{ opacity: 1 }, { opacity: .35 }, { opacity: 1 }], { duration: 320 });
  }
  function advance() {
    var s = cur();
    s.revealed = false;
    if (s.i >= s.items.length - 1) { finishSession(false); return; }
    s.i++;
    render();
  }
  function checkAnswer(q, picks) {
    picks = picks || [];
    if (q.type === "fillin") return answersMatch(picks[0] || "", q._accept);
    if (q.type === "truefalse") return picks[0] === String(q._answerBool);
    var sel = picks.map(Number).sort(function (a, b) { return a - b; });
    var exp = q._answerIdx.slice().sort(function (a, b) { return a - b; });
    return sel.length === exp.length && sel.every(function (v, i) { return v === exp[i]; });
  }
  function answerText(q) {
    if (q.type === "fillin") return q._accept.join(" / ");
    if (q.type === "truefalse") return q._answerBool ? "True" : "False";
    return q._answerIdx.map(function (i) { return String.fromCharCode(65 + i) + ") " + q.options[i]; }).join(" · ");
  }

  // ---------------------------------------------------------------- results
  function finishSession(timedOut) {
    var s = cur();
    if (!s) return;
    stopTimer();
    var rows = s.items.map(function (q, i) {
      var picks = s.picks[i] || [];
      var attempted = q.type === "fillin" ? !!(picks[0] || "").trim() : picks.length > 0;
      return { q: q, picks: picks, attempted: attempted, ok: attempted && checkAnswer(q, picks) };
    });
    var correct = rows.filter(function (r) { return r.ok; }).length;
    if (!rows.length) { setCur(null); state.drillView = false; state.mode = "notes"; render(); return; }
    var pct = Math.round(correct / rows.length * 100);
    var pass = state.deck.pass_mark || 70;
    logRun(s.kind, pct, rows.length);
    state.results = { rows: rows, correct: correct, pct: pct, timedOut: timedOut, seconds: Math.round((Date.now() - s.startedAt) / 1000), pass: pass, kind: s.kind };
    setCur(null);
    state.drillView = false;
    state.mode = "results";
    renderResults();
  }

  function renderResults() {
    var r = state.results, d = state.deck;
    hideStatus();
    view.innerHTML = "";
    var head = el("div", "result-head");
    var passMsg = d.pass_mark
      ? (r.pct >= r.pass ? "Above your deck pass mark of " + r.pass + "%." : "Below " + r.pass + "%. Re-run the weak queue before you sit it.")
      : (r.pct >= 80 ? "Strong. Set <code>pass_mark</code> in your deck to mirror the real cut score." : "Solid first pass, but shore up the misses below.");
    head.innerHTML =
      '<div class="mono">' + (r.kind === "mock" ? "MOCK EXAM" : r.kind === "weak" ? "WEAK-SPOT DRILL" : "PRACTICE RUN") + (r.timedOut ? " · time expired" : "") + "</div>" +
      '<div class="score ' + (r.pct >= r.pass ? "pass" : "fail") + '">' + r.pct + "%</div>" +
      '<div class="verdict">' + r.correct + " / " + r.rows.length + " correct · " + fmtMMSS(r.seconds) +
      " elapsed<br>" + esc(passMsg) + "</div>" +
      '<div class="row" style="justify-content:center;margin-top:14px">' +
      '<button class="primary" id="drill-misses" type="button">Drill the ' + r.rows.filter(function (x) { return !x.ok; }).length + " miss(es)</button>" +
      '<button class="ghost" id="again" type="button">New ' + (r.kind === "mock" ? "mock" : "run") + "</button>" +
      '<button class="ghost" id="tonotes" type="button">Back to notes</button></div>';
    view.appendChild(head);

    var bySection = {};
    r.rows.forEach(function (row) {
      var k = row.q.section || "general";
      bySection[k] = bySection[k] || { t: 0, c: 0 };
      bySection[k].t++; if (row.ok) bySection[k].c++;
    });
    var g = el("div", "grid");
    Object.keys(bySection).sort().forEach(function (k) {
      var v = bySection[k], p = Math.round(v.c / v.t * 100);
      g.appendChild(el("div", "tile", "<div class='n' style='color:" + (p >= 80 ? "var(--accent-2)" : p >= 50 ? "var(--warn)" : "var(--bad)") + "'>" + p +
        "%</div><div class='lab'>" + esc(k) + " · " + v.c + "/" + v.t + "</div><div class='bar-mini'><i style='width:" + p + "%'></i></div>"));
    });
    view.appendChild(g);

    var recent = state.stats.runs.slice(-8);
    if (recent.length > 1) {
      var spark = el("div", "card-shell");
      spark.innerHTML = "<h2 class='sec' style='margin-top:0'>Your runs <span>· last " + recent.length + "</span></h2>" +
        '<div class="row">' + recent.map(function (x) {
          return '<div class="mono" title="' + esc(new Date(x.at).toLocaleString()) + '">' + x.pct + "%<br>" + x.mode + "</div>";
        }).join('<span class="muted">→</span>') + "</div>" +
        '<p class="muted small" style="margin-bottom:0">Target: a rising line, not a high single number. Two runs at 85%+ on randomised order is the honest signal you are ready.</p>';
      view.appendChild(spark);
    }

    view.appendChild(el("h2", "sec", "Review <span>· what you picked vs. what is right, with rationale</span>"));
    r.rows.forEach(function (row, i) {
      var box = el("div", "review-item");
      box.style.borderLeft = "3px solid " + (row.ok ? "var(--accent-2)" : "var(--bad)");
      var pickedTxt = row.q.type === "fillin" ? (row.picks[0] || "—") :
        row.q.type === "truefalse" ? (row.picks[0] || "—") :
          row.picks.length ? row.picks.map(function (p) { return String.fromCharCode(65 + p) + ") " + row.q.options[p]; }).join(" · ") : "not answered";
      box.innerHTML =
        '<div class="rstem"><span class="dot ' + (row.ok ? "ok" : "no") + '"></span>' + (i + 1) + ". " + inline(row.q.stem) + "</div>" +
        '<div class="line muted"><b>You:</b> ' + inline(pickedTxt) + "</div>" +
        (row.ok ? "" : '<div class="line"><b>Correct:</b> ' + inline(answerText(row.q)) + "</div>") +
        (row.q.rationale ? '<div class="line muted" style="margin-top:6px">' + inline(row.q.rationale) + "</div>" : "") +
        (!row.ok && (row.q.why_wrong || row.q.whyWrong) ? '<div class="line" style="margin-top:4px"><b>Trap:</b> ' + inline(row.q.why_wrong || row.q.whyWrong) + "</div>" : "") +
        (row.q.section ? '<div class="mono" style="margin-top:6px">' + esc(row.q.section) + "</div>" : "");
      view.appendChild(box);
    });

    var misses = r.rows.filter(function (x) { return !x.ok; });
    head.querySelector("#drill-misses").onclick = function () {
      if (!misses.length) { state.mode = "notes"; render(); return; }
      startSession({ kind: "weak", items: shuffle(misses.map(function (m) { return m.q; })), minutes: 0 });
      render();
    };
    head.querySelector("#again").onclick = function () { state.mode = r.kind === "mock" ? "mock" : "practice"; render(); };
    head.querySelector("#tonotes").onclick = function () { state.mode = "notes"; render(); };
  }

  // ---------------------------------------------------------------- import dialog
  var modal = document.getElementById("import-modal");
  var ta = document.getElementById("import-text");
  var errEl = document.getElementById("import-err");
  function dlgOpen(d) { if (d.showModal) d.showModal(); else { d.setAttribute("open", ""); } }
  function dlgClose(d) { if (d.close) d.close(); else d.removeAttribute("open"); }
  function openImport() {
    errEl.hidden = true;
    ta.value = state.deck && !state.isExample ? JSON.stringify({
      title: state.deck.title, subtitle: state.deck.subtitle, pass_mark: state.deck.pass_mark,
      suggested_time_minutes: state.deck.suggested_time_minutes, sections: state.deck.sections,
      flashcards: state.deck.flashcards, questions: state.deck.questions
    }, null, 2) : "";
    ta.placeholder = DECK_HELP;
    dlgOpen(modal);
    setTimeout(function () { ta.focus(); }, 40);
  }
  var DECK_HELP = "Paste JSON here. Minimal shape:\n" +
    '{ "title": "Course name", "pass_mark": 75,\n' +
    '  "sections": [{"title": "Scope", "points": [{"point": "…", "why": "…"}]}],\n' +
    '  "flashcards": [{"front": "…", "back": "…", "section": "Scope"}],\n' +
    '  "questions": [{"type":"single","stem":"…","options":["…","…"],"answer":1,"rationale":"…","why_wrong":"…","section":"Scope"}] }\n' +
    "\nTypes: single | multiple (answer:[0,2]) | truefalse (answer:true) | fillin (answer:\"30 days\").\n" +
    "Prefer markdown? Paste it: ## Section / ### Card with **Front:** **Back:** / ### Q: with A) B) then `Correct: B`, `Rationale:`, `Why-wrong:`.";

  document.getElementById("btn-import").onclick = openImport;
  document.getElementById("import-go").onclick = function () {
    var v = ta.value.trim();
    if (!v) { showErr("Nothing to import."); return; }
    try { applyDeck(v); dlgClose(modal); }
    catch (e) { showErr(e.message); }
  };
  function showErr(msg) { errEl.textContent = "⚠ " + msg; errEl.hidden = false; }

  var drop = document.getElementById("drop");
  ["dragenter", "dragover"].forEach(function (ev) {
    drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add("over"); });
  });
  ["dragleave", "drop"].forEach(function (ev) {
    drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.remove("over"); });
  });
  drop.addEventListener("drop", function (e) {
    var f = e.dataTransfer.files && e.dataTransfer.files[0];
    if (!f) return;
    var rd = new FileReader();
    rd.onload = function () {
      try { applyDeck(String(rd.result)); dlgClose(modal); } catch (err) { showErr(err.message); }
    };
    rd.onerror = function () { showErr("Could not read that file."); };
    rd.readAsText(f);
  });
  var ex = document.getElementById("export-deck");
  if (ex) ex.onclick = function () {
    if (!state.deck) { showErr("Nothing loaded yet."); return; }
    ta.value = JSON.stringify({
      title: state.deck.title, subtitle: state.deck.subtitle, pass_mark: state.deck.pass_mark,
      suggested_time_minutes: state.deck.suggested_time_minutes, sections: state.deck.sections,
      flashcards: state.deck.flashcards, questions: state.deck.questions
    }, null, 2);
    ta.select();
    showErr("Deck serialised above — save it as data/deck.json (or Ctrl/Cmd+C) so it survives a cache clear.");
  };
  document.querySelector("[data-close]").onclick = function () { dlgClose(modal); };

  // ---------------------------------------------------------------- keyboard
  document.addEventListener("keydown", function (e) {
    if (modal.open) return;
    var tgt = e.target;
    if (tgt && tgt.matches && tgt.matches("input, textarea")) return;
    if (state.mode === "cards" && (e.key === " " || e.code === "Space")) e.preventDefault();
    if (state.mode === "cards") {
      if (e.code === "Space") { e.preventDefault(); state.cards.flipped = !state.cards.flipped; render(); return; }
      if (e.key === "ArrowLeft") { state.cards.idx--; state.cards.flipped = false; render(); return; }
      if (e.key === "ArrowRight") { state.cards.idx++; state.cards.flipped = false; render(); return; }
      if (state.cards.flipped && "1234".indexOf(e.key) >= 0) {
        var btn = view.querySelector('[data-rate="' + (Number(e.key) - 1) + '"]');
        if (btn) btn.click();
      }
      return;
    }
    if (cur()) {
      if (e.key === "Enter") { e.preventDefault(); view.querySelector("#submitq").click(); return; }
      if (/^[1-9]$/.test(e.key)) {
        var opts = view.querySelectorAll(".opt");
        var at = Number(e.key) - 1;
        if (opts[at]) { e.preventDefault(); opts[at].click(); }
      }
    }
  });

  Array.prototype.forEach.call(tabs.querySelectorAll(".tab"), function (t) {
    t.onclick = function () {
      // Tab switches never destroy an in-flight run: an unfinished practice/mock is
      // resumable from its own tab, and a finished scorecard survives navigation.
      state.mode = t.dataset.mode;
      render();
    };
  });

  // ---------------------------------------------------------------- boot
  function loadExample(store) {
    var raw = window.__DECK_EXAMPLE;
    try { applyDeck(JSON.parse(JSON.stringify(raw)), { example: true }); }
    catch (e) { view.innerHTML = '<div class="card-shell"><p class="err">Example deck failed to parse: ' + esc(e.message) + "</p></div>"; }
    if (store) { /* example is flagged, not persisted as user content */ writeJSON(LS.example, true); }
  }
  window.loadExampleDeck = loadExample;
  // debug/test handle — harmless in production, handy when a deck refuses to load
  window.__studydeck = {
    state: state,
    parseMarkdown: parseMarkdown,
    applyDeck: applyDeck,
    normalizeDeck: normalizeDeck,
    answersMatch: answersMatch
  };

  function useDeck(saved, isExample) {
    state.deck = normalizeDeck(saved);
    state.isExample = !!isExample;
    render();
  }

  (function boot() {
    var saved = readJSON(LS.deck, null);
    if (saved) {
      try { return useDeck(saved, readJSON(LS.example, false)); } catch (e) { /* fall through */ }
    }
    // no deck saved yet: pick up data/deck.json if the user dropped one in the repo
    if (typeof fetch !== "function") return loadExample(false);
    fetch("data/deck.json", { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error("no deck.json");
      return r.json();
    }).then(function (j) { useDeck(j, false); })
      .catch(function () { loadExample(false); });
  })();
})();
