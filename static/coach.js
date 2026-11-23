// Deckbau-Coach: Deck-Finder, Fragebogen, geführter Assistent, Glossar, Combos, Rule 0
let KNOW = null, PROFILE = null, QUIZ_RESULT = null, START_PRESET = {};
const CHAT = {}; // deckId -> [{role, content}]

async function know() { if (!KNOW) KNOW = await api("/api/knowledge"); return KNOW; }

// ---------- Glossar: Fachbegriffe antippbar machen ----------
function gloss(text) {
  let html = esc(text);
  if (!KNOW) return html;
  const terms = Object.keys(KNOW.glossary).sort((a, b) => b.length - a.length);
  const used = new Set();
  for (const t of terms) {
    const re = new RegExp(`(^|[\\s(„"/])(${t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})(?=[\\s,.;:!?)“"/-]|$)`, "i");
    if (used.has(t)) continue;
    if (re.test(html)) { html = html.replace(re, `$1<span class="term" data-term="${esc(t)}">$2</span>`); used.add(t); }
  }
  return html;
}
document.addEventListener("click", (e) => {
  const el = e.target.closest(".term");
  document.querySelectorAll(".termpop").forEach((p) => p.remove());
  if (!el || !KNOW) return;
  const p = document.createElement("div");
  p.className = "termpop";
  p.innerHTML = `<b>${esc(el.dataset.term)}</b><br>${esc(KNOW.glossary[el.dataset.term] || "")}`;
  document.body.append(p);
  const r = el.getBoundingClientRect();
  p.style.top = window.scrollY + r.bottom + 6 + "px";
  p.style.left = Math.max(8, Math.min(window.innerWidth - p.offsetWidth - 8, r.left)) + "px";
});

// ---------- Coach-Startseite ----------
async function renderCoachHome() {
  await know();
  PROFILE = await api("/api/profile");
  const nogoOpts = Object.entries(KNOW.nogo_labels);
  view.innerHTML = `<h1>🎓 Deckbau-Coach</h1>
    <p class="muted">Ich erkläre dir jeden Schritt, zeige Optionen mit Begründung – entscheiden tust du.</p>
    <div class="grid">
      <div class="panel deckcard" id="e-quiz"><b>🧭 Welcher Decktyp passt zu mir?</b><p class="small muted">6 Fragen mit Beispielen → deine Top-Archetypen mit Commander-Ideen.</p></div>
      <div class="panel deckcard" id="e-cmd"><b>👑 Ich habe einen Commander im Kopf</b><p class="small muted">Was kann er, welche Themen gibt es, wie viel davon besitzt du schon?</p></div>
      <div class="panel deckcard" id="e-coll"><b>📦 Aus meiner Sammlung</b><p class="small muted">Welche Commander kannst du mit deinen Karten schon fast bauen?</p></div>
    </div>
    <div class="panel"><h2 style="margin-top:0">Dein Profil</h2>
      <label>Was nervt dich am Tisch? (daraus werden Warnungen)</label>
      <div class="row">${nogoOpts.map(([k, l]) => `<label class="chip"><input type="checkbox" data-nogo="${k}" ${PROFILE.nogos.includes(k) ? "checked" : ""}> ${esc(l)}</label>`).join("")}</div>
      <label>Infinite-Combos</label>
      <select id="pcombo"><option value="suggest" ${PROFILE.combos === "suggest" ? "selected" : ""}>aktiv vorschlagen (mit Erklärung & Bracket-Hinweis)</option>
        <option value="show" ${PROFILE.combos === "show" ? "selected" : ""}>nur zeigen, wenn im Deck</option></select>
      <p class="small muted">Lehrer-Modus · Erklärungen für Einsteiger · Spaßtypen: große Momente, clevere Kombis, Chaos</p></div>
    <div class="panel"><h2 style="margin-top:0">📖 Glossar</h2><p class="small muted">Tipp: In den Lektionen kannst du jeden <span class="term" data-term="Ramp">unterstrichenen Begriff</span> antippen.</p>
      ${Object.entries(KNOW.glossary).map(([t, d]) => `<details><summary><b>${esc(t)}</b></summary><p class="small">${esc(d)}</p></details>`).join("")}</div>`;
  $("#e-quiz").onclick = () => (location.hash = "quiz");
  $("#e-cmd").onclick = () => { START_PRESET = {}; location.hash = "start"; };
  $("#e-coll").onclick = () => (location.hash = "commanders");
  const saveProfile = async () => {
    PROFILE.nogos = [...view.querySelectorAll("[data-nogo]:checked")].map((x) => x.dataset.nogo);
    PROFILE.combos = $("#pcombo").value;
    await api("/api/profile", { method: "PUT", body: PROFILE }); toast("Profil gespeichert");
  };
  view.querySelectorAll("[data-nogo]").forEach((x) => (x.onchange = saveProfile));
  $("#pcombo").onchange = saveProfile;
}

// ---------- Fragebogen ----------
async function renderQuiz() {
  await know();
  const answers = {};
  view.innerHTML = `<h1>🧭 Welcher Decktyp passt zu dir?</h1><p class="muted">Mehrfachauswahl erlaubt. Die Beispiele sollen dir nur beim Vorstellen helfen.</p>
    ${KNOW.questionnaire.map((q, i) => `<div class="panel"><b>${i + 1}. ${esc(q.q)}</b>
      ${q.options.map((o) => `<label class="opt"><input type="checkbox" data-q="${q.id}" value="${o.id}"> <span>${esc(o.t)}<br><span class="small muted">z. B. ${esc(o.ex)}</span></span></label>`).join("")}</div>`).join("")}
    <p><button class="primary" id="qgo">Auswerten</button></p><div id="qres"></div>`;
  $("#qgo").onclick = (e) => busy(e.target, async () => {
    view.querySelectorAll("[data-q]:checked").forEach((x) => (answers[x.dataset.q] ||= []).push(x.value));
    QUIZ_RESULT = await api("/api/finder/questionnaire", { method: "POST", body: { answers } });
    for (const k in answers) delete answers[k];
    renderQuizResult();
  });
}

function archCard(a, i) {
  const stars = (n) => "★".repeat(n) + "☆".repeat(5 - n);
  return `<div class="panel"><div class="row"><b style="font-size:1.05rem">${i + 1}. ${esc(a.name)}</b><span class="spacer"></span><span class="badge">${a.score} Punkte</span></div>
    <p>${gloss(a.plan)}</p>
    ${a.why?.length ? `<p class="small">Passt, weil du gewählt hast: <i>${a.why.map(esc).join(" · ")}</i></p>` : ""}
    <div class="small">Spaß für dich ${stars(a.fun[0])} · für die Gegner ${stars(a.fun[1])} · Komplexität ${stars(a.cx)}</div>
    <div class="small muted">Typische Farben: ${esc(a.colors)}</div>
    <div class="small" style="margin-top:.4rem">Beispiel-Commander: ${a.examples.map((e) => `${esc(e)}${a.owned_examples.includes(e) ? ' <span class="badge good">besitzt du</span>' : ""}`).join(", ")}</div>
    ${a.avoid ? '<p class="hint small">Achtung: Combo-Decks enden oft früh – steht auf deiner No-Go-Liste.</p>' : ""}
    <div class="row" style="margin-top:.6rem">${a.examples.map((e) => `<button class="mini" data-start="${esc(e)}" data-arch="${a.id}">Mit ${esc(e.split(",")[0])} starten</button>`).join("")}
      <button class="mini" data-start="" data-arch="${a.id}">Eigenen Commander wählen</button></div></div>`;
}

function renderQuizResult() {
  const r = QUIZ_RESULT;
  $("#qres").innerHTML = `<h2>Deine Top-Archetypen</h2>${r.top.map(archCard).join("")}
    <p class="small muted">Das ist ein Startpunkt, kein Urteil. Probier ruhig einen Archetyp, der nicht auf Platz 1 steht.</p>`;
  view.querySelectorAll("[data-start]").forEach((b) => (b.onclick = () => { START_PRESET = { commander: b.dataset.start, archetype: b.dataset.arch }; location.hash = "start"; }));
  $("#qres").scrollIntoView({ behavior: "smooth" });
}

// ---------- Neues Deck im Assistenten ----------
async function renderStart() {
  await know();
  const p = START_PRESET;
  view.innerHTML = `<h1>👑 Neues Deck mit dem Coach</h1>
    <div class="panel"><label>Commander</label><div class="row"><input id="sc" list="sac" value="${esc(p.commander || "")}" placeholder="z. B. Pantlaza, Sun-Favored" style="flex:1"><datalist id="sac"></datalist><button id="slook">Ansehen</button></div>
      <div id="sinfo"></div>
      <label>Archetyp (optional)</label><select id="sa"><option value="">– noch offen –</option>${Object.entries(KNOW.archetypes).map(([k, a]) => `<option value="${k}" ${p.archetype === k ? "selected" : ""}>${esc(a.name)}</option>`).join("")}</select>
      <div class="row"><div><label>Ziel-Bracket</label><select id="sb">${[1, 2, 3, 4].map((b) => `<option value="${b}" ${b === 2 ? "selected" : ""}>${b} – ${esc(KNOW.brackets[b].name)}</option>`).join("")}</select></div>
        <div><label>Budget (€)</label><input id="sbu" type="number" value="25" style="width:6rem"></div></div>
      <p class="small muted" id="bdesc"></p>
      <label>Deckname</label><input id="sn" style="width:100%" placeholder="z. B. Dino-Chaos">
      <p><button class="primary" id="sgo">Assistent starten</button></p></div>`;
  autocomplete($("#sc"), $("#sac"));
  const bd = () => ($("#bdesc").textContent = KNOW.brackets[$("#sb").value].desc);
  $("#sb").onchange = bd; bd();
  const look = async () => {
    if (!$("#sc").value) return;
    $("#sinfo").innerHTML = '<p class="muted small">Schaue nach …</p>';
    try {
      const r = await api("/api/finder/commander?name=" + encodeURIComponent($("#sc").value));
      $("#sc").value = r.card.name;
      $("#sinfo").innerHTML = `<div class="row" style="align-items:flex-start;margin:.6rem 0">${r.card.image_small ? `<img src="${esc(r.card.image_small)}" style="width:110px;border-radius:8px" onclick="preview('${esc(r.card.image)}')">` : ""}
        <div style="flex:1;min-width:180px"><div>${pips(r.card.color_identity)} <b>${esc(r.card.name)}</b> <span class="muted small">${esc(r.card.mana_cost)}</span></div>
        <p class="small">${esc(r.card.oracle_text)}</p>
        ${r.is_game_changer ? '<p class="hint small">Game Changer als Commander → erst ab Bracket 3.</p>' : ""}
        ${r.edhrec_cards ? `<p class="small">Du besitzt <b>${r.percent}%</b> der beliebten Karten für ihn (${r.owned_from_edhrec}/${r.edhrec_cards}).</p>` : ""}
        ${r.themes.length ? `<p class="small">Beliebte Themen auf EDHREC: ${r.themes.map((t) => `<span class="badge">${esc(t.name)}</span>`).join(" ")}</p><p class="small muted">Frag dich: Welches Thema reizt dich am meisten – und warum?</p>` : ""}
        <a class="small" href="${esc(r.edhrec_url)}" target="_blank">Auf EDHREC ansehen ↗</a></div></div>`;
      if (!$("#sn").value) $("#sn").value = r.card.name.split(",")[0] + "-Deck";
    } catch (e) { $("#sinfo").innerHTML = `<p class="problem small">${esc(e.message)}</p>`; }
  };
  $("#slook").onclick = look;
  if (p.commander) look();
  $("#sgo").onclick = (e) => busy(e.target, async () => {
    const r = await api("/api/wizard/start", { method: "POST", body: { name: $("#sn").value || "Neues Deck", commander: $("#sc").value, bracket: +$("#sb").value, budget_eur: +$("#sbu").value, archetype: $("#sa").value || null } });
    location.hash = "wiz-" + r.id;
  });
}

// ---------- Assistent ----------
let WIZ = { id: null, step: "table" };
async function renderWizard(id) {
  await know();
  if (WIZ.id !== id) { const d = await api("/api/decks/" + id); WIZ = { id, step: d.deck.wizard_step || "table" }; }
  view.innerHTML = '<p class="muted">Lade Schritt …</p>';
  const S = await api(`/api/decks/${id}/step/${WIZ.step}`);
  const steps = KNOW.steps;
  const a = S.analysis;
  view.innerHTML = `<div class="row"><h1 style="margin:0">${esc(S.deck.name)}</h1><span class="spacer"></span><a class="btn" href="#deck-${id}">Deckansicht</a></div>
    <div class="stepper">${steps.map((s, i) => `<button class="${s.id === WIZ.step ? "active" : ""} ${i < S.index ? "done" : ""}" data-go="${s.id}" title="${esc(s.title)}">${i + 1}</button>`).join("")}</div>
    <div class="row small muted"><span>${a.total}/100 Karten</span><span>·</span><span>Ø MV ${a.avg_cmc}</span><span>·</span><span>Bracket-Ziel ${S.deck.bracket}</span></div>
    <div class="panel lesson"><h2 style="margin-top:0">Schritt ${S.index + 1}: ${esc(S.step.title)}</h2><p>${gloss(S.step.lesson)}</p>
      ${S.step.questions.length ? `<div class="small"><b>Frag dich:</b><ul>${S.step.questions.map((q) => `<li>${gloss(q)}</li>`).join("")}</ul></div>` : ""}
      ${S.target ? targetBar(S) : ""}</div>
    <div id="stepbody"></div>
    <div class="panel" id="chat"></div>
    <div class="row"><button id="prev" ${S.index === 0 ? "disabled" : ""}>← Zurück</button><span class="spacer"></span><button class="primary" id="next">${S.index === steps.length - 1 ? "Fertig 🎉" : "Weiter →"}</button></div>`;
  view.querySelectorAll("[data-go]").forEach((b) => (b.onclick = () => goStep(id, b.dataset.go)));
  $("#prev").onclick = () => goStep(id, steps[S.index - 1].id);
  $("#next").onclick = () => (S.index === steps.length - 1 ? (location.hash = "deck-" + id) : goStep(id, steps[S.index + 1].id));
  (STEP_UI[WIZ.step] || stepCandidates)(id, S);
  renderChat(id, S);
}

async function goStep(id, step) {
  WIZ.step = step;
  await api(`/api/decks/${id}/meta`, { method: "PATCH", body: { wizard_step: step } });
  renderWizard(id); window.scrollTo(0, 0);
}

function targetBar(S) {
  const t = S.target, v = S.current.length, scale = Math.max(t.to * 1.4, v + 1);
  const cls = v < t.critical ? "low" : v < t.from ? "low" : v > t.max ? "high" : "";
  const msg = v < t.critical ? "deutlich zu wenig" : v < t.from ? `noch ${t.from - v} bis zum Zielbereich` : v > t.max ? "eher zu viel" : "im Zielbereich ✓";
  return `<div class="meter" style="margin-top:.8rem"><span>Stand</span><div class="bar"><b style="left:${(t.from / scale) * 100}%;width:${((t.to - t.from) / scale) * 100}%"></b><i class="${cls}" style="width:${Math.min(100, (v / scale) * 100)}%"></i></div><span>${v} <span class="muted small">/${t.from}–${t.to}</span></span></div><div class="small ${cls ? "hint" : ""}">${msg}</div>`;
}

function currentList(id, S) {
  if (!S.current.length) return '<p class="muted small">Noch keine Karte in dieser Rolle.</p>';
  return S.current.map((c) => `<div class="cardline"><span class="name" data-img="${esc(c.image)}">${esc(c.name)}</span>${c.note ? `<span class="small muted">„${esc(c.note)}“</span>` : ""}<button class="mini" data-rm="${esc(c.name)}">✕</button></div>`).join("");
}

function candidateHTML(c, i) {
  const badges = [c.owned ? '<span class="badge good">✓ besitzt du</span>' : `<span class="badge">${eur(c.eur)}</span>`];
  if (c.in_decks?.length) badges.push(`<span class="badge warn">auch in ${esc(c.in_decks[0])}</span>`);
  if (c.synergy) badges.push(`<span class="badge">EDHREC ${c.inclusion ?? "?"}% · Synergie ${(c.synergy * 100).toFixed(0)}%</span>`);
  c.issues.forEach((x) => badges.push(`<span class="badge bad">${esc(x)}</span>`));
  c.nogos.forEach((x) => badges.push(`<span class="badge warn">${esc(x)}</span>`));
  if (c.salt) badges.push(`<span class="badge warn">Salt ${c.salt}</span>`);
  return `<div class="cand"><div class="row"><span class="name" data-img="${esc(c.image)}">${esc(c.name)}</span><span class="small muted">${esc(c.mana_cost || "")}</span><span class="spacer"></span><button class="mini primary" data-pick="${i}">+ rein</button></div>
    <div class="row small">${badges.join(" ")}</div>
    <details><summary class="small muted">Kartentext</summary><p class="small">${esc(c.type_line)}<br>${esc(c.text)}</p></details></div>`;
}

function stepCandidates(id, S) {
  const role = S.step.role;
  let filter = "all";
  const draw = () => {
    const list = S.candidates.filter((c) => filter === "all" || (filter === "owned" ? c.owned : !c.owned));
    $("#cands").innerHTML = list.map((c) => candidateHTML(c, S.candidates.indexOf(c))).join("") || '<p class="muted small">Keine Kandidaten gefunden. Du kannst oben jede Karte per Name hinzufügen.</p>';
    bindCards(id, S, role);
  };
  $("#stepbody").innerHTML = `<div class="panel"><h3 style="margin-top:0">Schon im Deck (${S.current.length})</h3>${currentList(id, S)}</div>
    <div class="panel"><h3 style="margin-top:0">Kandidaten</h3>
      <p class="small muted">Sortiert: deine Karten zuerst, dann nach EDHREC-Synergie. Überleg bei jeder Karte: Bringt sie meinen Spielplan voran? ${S.deck.plan ? `<br>Dein Plan: <i>„${esc(S.deck.plan)}“</i>` : ""}</p>
      <div class="row"><input id="own" list="oac" placeholder="Eigene Idee: Kartenname …" style="flex:1"><datalist id="oac"></datalist><button id="ownb">+ rein</button></div>
      <div class="row small" style="margin:.6rem 0"><button class="mini" data-f="all">alle</button><button class="mini" data-f="owned">nur meine</button><button class="mini" data-f="buy">zum Kaufen</button></div>
      <div id="cands"></div></div>`;
  autocomplete($("#own"), $("#oac"));
  $("#ownb").onclick = () => pickCard(id, $("#own").value, role);
  view.querySelectorAll("[data-f]").forEach((b) => (b.onclick = () => { filter = b.dataset.f; draw(); }));
  draw();
}

function bindCards(id, S, role) {
  view.querySelectorAll("[data-img]").forEach((el) => (el.onclick = () => preview(el.dataset.img)));
  view.querySelectorAll("[data-pick]").forEach((b) => (b.onclick = () => pickCard(id, S.candidates[+b.dataset.pick].name, role, b)));
  view.querySelectorAll("[data-rm]").forEach((b) => (b.onclick = async () => { await api(`/api/decks/${id}/cards?name=${encodeURIComponent(b.dataset.rm)}&section=main`, { method: "DELETE" }); renderWizard(id); }));
}

function pickCard(id, name, role, btn) {
  if (!name) return;
  const box = document.createElement("div");
  box.className = "panel pickbox";
  box.innerHTML = `<b>${esc(name)}</b> als ${esc(KNOW.roles[role] || role || "Karte")}<label>Warum nimmst du sie? (optional – hilft beim Lernen und später beim Kürzen)</label>
    <input id="why" style="width:100%" placeholder="z. B. „billig und trifft auch Verzauberungen“"><div class="row" style="margin-top:.5rem"><button class="primary" id="pk">Rein damit</button><button id="pc">Abbrechen</button></div><div id="fb"></div>`;
  (btn?.closest(".cand") || $("#stepbody")).after(box);
  box.scrollIntoView({ behavior: "smooth", block: "center" });
  $("#why").focus();
  $("#pc").onclick = () => box.remove();
  $("#pk").onclick = (e) => busy(e.target, async () => {
    const r = await api(`/api/decks/${id}/pick`, { method: "POST", body: { name, role, note: $("#why").value || null } });
    $("#fb").innerHTML = feedbackHTML(r.feedback) + '<p><button class="mini" id="fbok">Weiter</button></p>';
    $("#pk").remove(); $("#pc").remove();
    $("#fbok").onclick = () => renderWizard(id);
  });
}

function feedbackHTML(fb) {
  const icon = { good: "✅", info: "💡", warn: "⚠️" };
  return fb.map((f) => `<div class="small fb ${f.level}">${icon[f.level] || "•"} ${gloss(f.text)}</div>`).join("");
}

// ---------- Spezielle Schritte ----------
const STEP_UI = {
  table(id, S) {
    $("#stepbody").innerHTML = `<div class="panel"><label>Ziel-Bracket</label><select id="wb">${[1, 2, 3, 4, 5].map((b) => `<option value="${b}" ${b == S.deck.bracket ? "selected" : ""}>${b} – ${esc(KNOW.brackets[b].name)}</option>`).join("")}</select>
      <div id="bexp" class="small" style="margin-top:.5rem"></div>
      <label>Budget (€)</label><input id="wbu" type="number" value="${S.deck.budget_eur}" style="width:6rem">
      <label>Notizen zu deiner Runde</label><textarea id="wt" style="min-height:90px" placeholder="z. B. „Gemischte Runde: Tim spielt optimierte Decks, die anderen Precons. Keine Combos vor Zug 8.“">${esc(S.deck.table_notes || "")}</textarea>
      <p><button id="ws">Speichern</button></p></div>`;
    const exp = () => { const b = KNOW.brackets[$("#wb").value];
      $("#bexp").innerHTML = `${esc(b.desc)}<br>Spiel sollte mindestens <b>${b.turns}</b> Züge dauern · Game Changer: <b>${b.gc >= 99 ? "frei" : b.gc}</b> · Combos: <b>${b.combos === true ? "frei" : b.combos === false ? "nein" : esc(b.combos)}</b> · Extrazüge: ${esc(b.extra_turns)}`; };
    $("#wb").onchange = exp; exp();
    $("#ws").onclick = (e) => busy(e.target, async () => {
      await api(`/api/decks/${id}`, { method: "PATCH", body: { bracket: +$("#wb").value, budget_eur: +$("#wbu").value } });
      await api(`/api/decks/${id}/meta`, { method: "PATCH", body: { table_notes: $("#wt").value } });
      toast("Gespeichert");
    });
  },
  commander(id, S) {
    const c = S.commander;
    if (!c) { $("#stepbody").innerHTML = '<p class="hint">Kein Commander gesetzt.</p>'; return; }
    $("#stepbody").innerHTML = `<div class="panel"><div class="row" style="align-items:flex-start">${c.card.image_small ? `<img src="${esc(c.card.image_small)}" style="width:120px;border-radius:8px" onclick="preview('${esc(c.card.image)}')">` : ""}
      <div style="flex:1;min-width:180px"><b>${esc(c.card.name)}</b> ${pips(c.card.color_identity)}<p class="small">${esc(c.card.oracle_text)}</p>
      <p class="small">Manawert <b>${c.card.cmc}</b> → ${c.card.cmc >= 5 ? "teurer Commander: du brauchst genug Ramp, um ihn ab Zug 4 zu spielen." : "günstiger Commander: er kommt früh und treibt dein Spiel jede Runde an."}</p>
      ${c.is_game_changer ? '<p class="hint small">Game Changer als Commander → erst ab Bracket 3.</p>' : ""}</div></div>
      ${c.themes.length ? `<h3>Wofür andere ihn spielen (EDHREC-Themen)</h3><p>${c.themes.map((t) => `<span class="badge">${esc(t.name)}${t.count ? " · " + t.count : ""}</span>`).join(" ")}</p>` : ""}
      <label>Archetyp für dieses Deck</label><select id="warch"><option value="">– offen –</option>${Object.entries(KNOW.archetypes).map(([k, a]) => `<option value="${k}" ${S.deck.archetype === k ? "selected" : ""}>${esc(a.name)}</option>`).join("")}</select>
      <div id="aexp" class="small" style="margin-top:.4rem"></div></div>`;
    const exp = () => { const a = KNOW.archetypes[$("#warch").value]; $("#aexp").innerHTML = a ? `${gloss(a.plan)} · Komplexität ${a.cx}/5` : ""; };
    $("#warch").onchange = async () => { exp(); await api(`/api/decks/${id}/meta`, { method: "PATCH", body: { archetype: $("#warch").value } }); toast("Archetyp gespeichert – Zielwerte angepasst"); };
    exp();
  },
  plan(id, S) {
    $("#stepbody").innerHTML = `<div class="panel"><label>Dein Spielplan in einem Satz</label>
      <textarea id="wp" style="min-height:90px" placeholder="z. B. „Ich rampe früh, spiele große Dinos, die über Discover Gratis-Zauber bringen, und gewinne mit einem großen Angriff.“">${esc(S.deck.plan || "")}</textarea>
      <p class="small muted">Weitere Beispiele: „Ich mache jede Runde Token und gewinne mit einem Overrun.“ · „Ich lasse die Gegner sich gegenseitig angreifen und gewinne am Ende mit Drain.“</p>
      <p><button class="primary" id="wps">Speichern</button></p></div>`;
    $("#wps").onclick = (e) => busy(e.target, async () => { await api(`/api/decks/${id}/meta`, { method: "PATCH", body: { plan: $("#wp").value } }); toast("Plan gespeichert"); });
  },
  wincon(id, S) {
    stepCandidates(id, S);
    $("#stepbody").insertAdjacentHTML("afterbegin", combosHTML(S.combos, true));
    bindCombos(id);
  },
  lands(id, S) {
    stepCandidates(id, S);
    const a = S.analysis;
    $("#stepbody").insertAdjacentHTML("afterbegin", `<div class="panel"><h3 style="margin-top:0">Deine Länder-Rechnung</h3><p>${esc(S.formula.text)}</p>
      <p class="small">Farbquellen: ${a.color_identity.map((c) => `${pips([c])} ${a.color_sources[c] ?? 0}`).join(" &nbsp; ")} <span class="muted">(Faustregel: ~19 Quellen für eine Farbe, die du früh brauchst)</span></p>
      ${a.tapped_lands.length ? `<p class="small">Immer getappt: ${a.tapped_lands.map(esc).join(", ")} (${a.tapped_lands.length}, Ziel ≤ 4)</p>` : ""}</div>`);
  },
  curve(id, S) {
    const a = S.analysis, max = Math.max(1, ...Object.values(a.curve));
    $("#stepbody").innerHTML = `<div class="panel"><h3 style="margin-top:0">Manakurve</h3>
      <div class="curve">${Object.entries(a.curve).map(([k, v]) => `<div style="height:${(v / max) * 100}%"><span>${v}</span></div>`).join("")}</div>
      <div class="curve-labels">${Object.keys(a.curve).map((k) => `<span>${k === "7" ? "7+" : k}</span>`).join("")}</div>
      <p>Ø-Manawert: <b>${a.avg_cmc}</b> (Ziel ~3) · Karten: <b>${a.total}</b>/100</p>
      ${a.advice.map((x) => `<div class="small ${x.level === "critical" ? "problem" : "hint"}">• ${esc(x.text)}</div>`).join("")}
      <p class="small muted">Zum Kürzen findest du in der Deckansicht jede Karte mit ✕. Tipp: Bei jeder Karte fragen „Welche Rolle erfüllt sie – und gibt es eine bessere?“</p>
      <a class="btn" href="#deck-${id}">Zur Deckansicht</a></div>`;
  },
  async check(id, S) {
    $("#stepbody").innerHTML = '<p class="muted">Prüfe …</p>';
    const c = await api(`/api/decks/${id}/check`);
    const icon = { critical: "⛔", warn: "⚠️", info: "💡" };
    $("#stepbody").innerHTML = `<div class="panel"><h3 style="margin-top:0">Bracket</h3>
      <p>Ziel: <b>${c.bracket_target}</b> · Einschätzung: <b class="${c.bracket_estimate > c.bracket_target ? "problem" : ""}">${c.bracket_estimate}</b> <span class="small muted">(${esc(c.bracket_reason)})</span></p>
      ${c.findings.map((f) => `<div class="small" style="margin:.25rem 0">${icon[f.level] || "•"} ${gloss(f.text)}</div>`).join("") || '<p class="small">Alles im grünen Bereich ✓</p>'}</div>
      ${combosHTML(c.combos, true)}`;
    bindCombos(id);
  },
  rule0(id, S) {
    $("#stepbody").innerHTML = `<div class="panel"><textarea readonly id="r0" style="min-height:170px">${esc(S.rule0.text)}</textarea><p><button id="r0c">Kopieren</button></p></div>`;
    $("#r0c").onclick = async () => { try { await navigator.clipboard.writeText(S.rule0.text); toast("Kopiert"); } catch { $("#r0").select(); } };
  },
};

function comboItem(x, almost) {
  return `<div class="combo"><div><b>${x.cards.map((n) => (x.missing?.includes(n) ? `<span class="in">${esc(n)}</span>` : esc(n))).join(" + ")}</b></div>
    <div class="small">→ ${x.result.map(esc).join(", ") || "?"} <span class="badge ${x.bracket_tag === "R" ? "bad" : x.bracket_tag === "S" || x.bracket_tag === "P" ? "warn" : ""}">${esc(x.bracket_label || "")}</span></div>
    ${x.steps ? `<details><summary class="small muted">So funktioniert's</summary><p class="small" style="white-space:pre-line">${esc(x.prerequisites ? "Voraussetzung: " + x.prerequisites + "\n" : "")}${esc(x.steps)}</p></details>` : ""}
    <div class="row small">${almost && x.missing?.length ? `<span>Fehlt: <b>${esc(x.missing[0])}</b></span><button class="mini" data-addcombo="${esc(x.missing[0])}">+ ins Deck</button>` : ""}${x.url ? `<a href="${esc(x.url)}" target="_blank">Spellbook ↗</a>` : ""}</div></div>`;
}

function combosHTML(c, withAlmost) {
  if (!c) return "";
  if (c.error) return `<div class="panel small hint">Combo-Check gerade nicht erreichbar (${esc(c.error)}).</div>`;
  return `<div class="panel"><h3 style="margin-top:0">♾️ Combos</h3>
    <p class="small muted">Eine <span class="term" data-term="Infinite Combo">Infinite Combo</span> gewinnt oft sofort. Bracket 1–2: keine; Bracket 3: frühestens Zug 6; ab 4: frei. Du entscheidest – ich baue nie automatisch ein.</p>
    <h3>Schon im Deck (${c.included.length})</h3>${c.included.map((x) => comboItem(x, false)).join("") || '<p class="small muted">keine</p>'}
    ${withAlmost ? `<h3>Fehlt nur 1 Karte (${c.almost.length})</h3>${c.almost.slice(0, 10).map((x) => comboItem(x, true)).join("") || '<p class="small muted">keine</p>'}` : ""}</div>`;
}

function bindCombos(id) {
  view.querySelectorAll("[data-addcombo]").forEach((b) => (b.onclick = () => pickCard(id, b.dataset.addcombo, "wincon", b)));
}

// ---------- Coach-Chat ----------
function renderChat(id, S) {
  const hist = (CHAT[id] ||= []);
  const box = $("#chat");
  if (!STATUS.ai) { box.innerHTML = '<p class="small muted">💬 Der Coach-Chat braucht einen ANTHROPIC_API_KEY in Railway. Lektionen, Kandidaten und Feedback funktionieren auch ohne.</p>'; return; }
  const draw = () => {
    box.innerHTML = `<h3 style="margin-top:0">💬 Frag den Coach</h3>
      <div class="chatlog">${hist.map((m) => `<div class="msg ${m.role}">${m.role === "assistant" ? gloss(m.content).replace(/\n/g, "<br>") : esc(m.content)}</div>`).join("")}</div>
      <div class="row small" style="margin:.4rem 0">${["Erklär mir diesen Schritt nochmal einfacher", "Welche 3 Kandidaten würdest du mir zeigen und warum?", "Gibt es eine lustige Combo für mein Deck?"].map((q) => `<button class="mini" data-q="${esc(q)}">${esc(q)}</button>`).join("")}</div>
      <div class="row"><input id="cm" style="flex:1" placeholder="Deine Frage …"><button class="primary" id="cs">Senden</button></div>`;
    const send = (msg) => busy($("#cs"), async () => {
      if (!msg) return;
      hist.push({ role: "user", content: msg }); draw();
      const r = await api(`/api/decks/${id}/coach`, { method: "POST", body: { message: msg, step: WIZ.step, history: hist.slice(0, -1) } });
      hist.push({ role: "assistant", content: r.reply }); draw();
    });
    $("#cs").onclick = () => send($("#cm").value);
    $("#cm").onkeydown = (e) => e.key === "Enter" && send($("#cm").value);
    box.querySelectorAll("[data-q]").forEach((b) => (b.onclick = () => send(b.dataset.q)));
  };
  draw();
}
