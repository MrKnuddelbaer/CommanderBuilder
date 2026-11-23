// CommanderBuilder – Frontend (ohne Framework, Hash-Routing)
const $ = (s, el = document) => el.querySelector(s);
const view = $("#view");
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const eur = (v) => (v == null ? "–" : v.toLocaleString("de-DE", { style: "currency", currency: "EUR" }));
const pips = (ci) => (ci || []).map((c) => `<span class="pip ${c}"></span>`).join("") || '<span class="pip" style="background:#888"></span>';
let STATUS = {};

async function api(path, opts = {}) {
  const o = { headers: {}, ...opts };
  if (o.body && !(o.body instanceof FormData)) { o.headers["Content-Type"] = "application/json"; o.body = JSON.stringify(o.body); }
  const r = await fetch(path, o);
  if (r.status === 401) { renderLogin(); throw new Error("login"); }
  const ct = r.headers.get("content-type") || "";
  const data = ct.includes("json") ? await r.json() : await r.text();
  if (!r.ok) throw new Error(data.detail || data || r.statusText);
  return data;
}
function toast(msg, ms = 3500) { const t = $("#toast"); t.textContent = msg; t.hidden = false; clearTimeout(t._h); t._h = setTimeout(() => (t.hidden = true), ms); }
function preview(img) { if (!img) return; const d = document.createElement("div"); d.id = "preview"; d.innerHTML = `<img src="${esc(img)}">`; d.onclick = () => d.remove(); document.body.append(d); }
async function busy(btn, fn) { const t = btn.textContent; btn.disabled = true; btn.textContent = "⏳ " + t; try { return await fn(); } catch (e) { if (e.message !== "login") toast("Fehler: " + e.message, 6000); } finally { btn.disabled = false; btn.textContent = t; } }

// ---------- Login ----------
function renderLogin() {
  view.innerHTML = `<div class="panel" style="max-width:360px;margin:3rem auto"><h1>Anmelden</h1>
    <form id="lf"><label>Passwort</label><input type="password" id="pw" style="width:100%" autofocus>
    <p><button class="primary">Los</button></p></form></div>`;
  $("#lf").onsubmit = async (e) => { e.preventDefault(); try { await api("/api/login", { method: "POST", body: { password: $("#pw").value } }); route(); } catch (err) { toast(err.message); } };
}

// ---------- Decks ----------
async function renderDecks() {
  const [decks, precons] = await Promise.all([api("/api/decks"), api("/api/precons")]);
  view.innerHTML = `<div class="row"><h1>Deine Decks</h1><span class="spacer"></span><a class="btn primary" href="#coach">🎓 Neues Deck mit Coach</a><button id="new">+ Liste einfügen</button></div>
    <div class="grid">${decks.map((d) => `<div class="panel deckcard" data-id="${d.id}"><b>${esc(d.name)}</b>
      <div class="muted small">${esc(d.commander || "kein Commander")}</div>
      <div class="row small" style="margin-top:.4rem"><span class="badge">${d.cards || 0}/100</span><span class="badge">Bracket ${d.bracket}</span><span class="badge">Budget ${eur(d.budget_eur)}</span></div></div>`).join("") || '<p class="muted">Noch keine Decks.</p>'}</div>
    <div class="panel"><h2 style="margin-top:0">Precon laden</h2><div class="row">${precons.map((p) => `<button data-precon="${p}">${esc(p)}</button>`).join("")}</div></div>
    <div class="panel" id="newform" hidden><h2 style="margin-top:0">Neues Deck</h2>
      <label>Name</label><input id="dn" placeholder="z. B. Pantlaza Upgrade">
      <label>Commander (optional, wenn er in der Liste steht)</label><input id="dc" list="ac" placeholder="z. B. Pantlaza, Sun-Favored"><datalist id="ac"></datalist>
      <div class="row"><div><label>Bracket</label><select id="db">${[1, 2, 3, 4, 5].map((b) => `<option ${b == 2 ? "selected" : ""}>${b}</option>`).join("")}</select></div>
      <div><label>Budget (€)</label><input id="dbu" type="number" value="25" style="width:7rem"></div></div>
      <label>Deckliste (optional) – Format „1 Sol Ring“, Abschnitte „Commander“/„Deck“</label><textarea id="dl" placeholder="Commander\n1 Pantlaza, Sun-Favored\nDeck\n1 Sol Ring"></textarea>
      <p><button class="primary" id="create">Anlegen</button></p></div>`;
  view.querySelectorAll(".deckcard").forEach((el) => (el.onclick = () => (location.hash = "deck-" + el.dataset.id)));
  $("#new").onclick = () => { $("#newform").hidden = false; $("#dn").focus(); };
  autocomplete($("#dc"), $("#ac"));
  view.querySelectorAll("[data-precon]").forEach((b) => (b.onclick = () => busy(b, async () => {
    const r = await api("/api/precons/" + b.dataset.precon, { method: "POST" });
    if (r.not_found?.length) toast("Nicht gefunden: " + r.not_found.join(", "), 8000);
    location.hash = "deck-" + r.id;
  })));
  $("#create").onclick = (e) => busy(e.target, async () => {
    const r = await api("/api/decks", { method: "POST", body: { name: $("#dn").value || "Neues Deck", commander: $("#dc").value, bracket: +$("#db").value, budget_eur: +$("#dbu").value, decklist: $("#dl").value } });
    if (r.not_found?.length) toast("Nicht gefunden: " + r.not_found.join(", "), 8000);
    location.hash = "deck-" + r.id;
  });
}

function autocomplete(input, list) {
  let t;
  input.addEventListener("input", () => { clearTimeout(t); t = setTimeout(async () => {
    const opts = await api("/api/autocomplete?q=" + encodeURIComponent(input.value)).catch(() => []);
    list.innerHTML = opts.map((o) => `<option value="${esc(o)}">`).join("");
  }, 250); });
}

// ---------- Deck-Detail ----------
let DECK = null, DECKTAB = "cards";
async function renderDeck(id) {
  DECK = await api("/api/decks/" + id);
  const d = DECK.deck, a = DECK.analysis;
  const cmd = DECK.cards.find((c) => c.section === "commander");
  view.innerHTML = `<div class="row" style="align-items:flex-start">
      ${cmd?.image_small ? `<img src="${esc(cmd.image_small)}" style="width:110px;border-radius:8px;cursor:pointer" onclick="preview('${esc(cmd.image)}')">` : ""}
      <div style="flex:1;min-width:200px"><h1 style="margin-bottom:.2rem">${esc(d.name)}</h1>
        <div class="muted">${pips(a.color_identity)} ${esc(d.commander || "")}</div>
        <div class="row small" style="margin-top:.5rem">
          <span class="badge ${a.total === 100 ? "good" : "warn"}">${a.total}/100 Karten</span>
          <span class="badge">Ø Manawert ${a.avg_cmc}</span>
          <span class="badge ${a.bracket_estimate > d.bracket ? "bad" : "good"}">Geschätzt Bracket ${a.bracket_estimate}</span>
        </div>
        <div class="row small" style="margin-top:.5rem">
          <label style="margin:0">Ziel-Bracket</label><select id="br">${[1, 2, 3, 4, 5].map((b) => `<option ${b == d.bracket ? "selected" : ""}>${b}</option>`).join("")}</select>
          <label style="margin:0">Budget €</label><input id="bu" type="number" value="${d.budget_eur}" style="width:5.5rem">
        </div></div></div>
    <div class="row" style="margin-top:.6rem"><a class="btn primary" href="#wiz-${id}">🎓 Mit dem Coach durchgehen</a></div>
    <div class="tabs">${[["cards", "Karten"], ["analysis", "Analyse"], ["advisor", "🧠 Berater"], ["shop", "🛒 Einkauf"], ["more", "Mehr"]].map(([k, l]) => `<button data-tab="${k}" class="${k === DECKTAB ? "active" : ""}">${l}</button>`).join("")}</div>
    <div id="tab"></div>`;
  $("#br").onchange = async (e) => { await api(`/api/decks/${id}`, { method: "PATCH", body: { bracket: +e.target.value } }); renderDeck(id); };
  $("#bu").onchange = async (e) => { await api(`/api/decks/${id}`, { method: "PATCH", body: { budget_eur: +e.target.value } }); toast("Budget gespeichert"); DECK.deck.budget_eur = +e.target.value; };
  view.querySelectorAll("[data-tab]").forEach((b) => (b.onclick = () => { DECKTAB = b.dataset.tab; renderDeck(id); }));
  ({ cards: tabCards, analysis: tabAnalysis, advisor: tabAdvisor, shop: tabShop, more: tabMore })[DECKTAB](id);
}

function cardBadges(c) {
  const b = [];
  if (c.owned) b.push(`<span class="badge good">✓ besessen</span>`); else b.push(`<span class="badge bad">fehlt ${eur(c.eur)}</span>`);
  if (c.in_decks?.length) b.push(`<span class="badge warn" title="${esc(c.in_decks.join(", "))}">⚠ auch in ${esc(c.in_decks[0])}${c.in_decks.length > 1 ? " +" + (c.in_decks.length - 1) : ""}</span>`);
  if (c.game_changer) b.push(`<span class="badge bad">Game Changer</span>`);
  return b.join(" ");
}

function tabCards(id) {
  const groups = {};
  const order = ["Commander", "Creature", "Planeswalker", "Instant", "Sorcery", "Artifact", "Enchantment", "Battle", "Land", "Vielleicht"];
  for (const c of DECK.cards) {
    let g = c.section === "commander" ? "Commander" : c.section === "maybe" ? "Vielleicht" : order.find((t) => (c.type_line || "").includes(t)) || "Sonstiges";
    (groups[g] ||= []).push(c);
  }
  const names = { Creature: "Kreaturen", Planeswalker: "Planeswalker", Instant: "Spontanzauber", Sorcery: "Hexereien", Artifact: "Artefakte", Enchantment: "Verzauberungen", Battle: "Schlachten", Land: "Länder" };
  $("#tab").innerHTML = `<div class="panel"><div class="row"><input id="addc" list="ac2" placeholder="Karte hinzufügen …" style="flex:1"><datalist id="ac2"></datalist>
      <select id="adds"><option value="main">Deck</option><option value="maybe">Vielleicht</option><option value="commander">Commander</option></select><button id="addb" class="primary">+</button></div></div>
    ${[...order, "Sonstiges"].filter((g) => groups[g]).map((g) => `<div class="panel"><h3 style="margin-top:0">${names[g] || g} (${groups[g].reduce((s, c) => s + c.qty, 0)})</h3>
      ${groups[g].sort((a, b) => (a.cmc - b.cmc) || a.name.localeCompare(b.name)).map((c) => `<div class="cardline">
        <span class="small muted" style="width:1.6rem">${c.qty > 1 ? c.qty + "×" : ""}</span>
        <span class="name" data-img="${esc(c.image)}">${esc(c.name)}</span>
        <span class="small muted">${esc(c.mana_cost || "")}</span>${c.role && KNOW ? `<span class="badge">${esc(KNOW.roles[c.role] || c.role)}</span>` : ""}${cardBadges(c)}
        ${c.section !== "commander" ? `<button class="mini" data-del="${esc(c.name)}" data-sec="${c.section}">✕</button>` : ""}</div>`).join("")}</div>`).join("")}`;
  autocomplete($("#addc"), $("#ac2"));
  $("#addb").onclick = (e) => busy(e.target, async () => { const r = await api(`/api/decks/${id}/cards`, { method: "POST", body: { name: $("#addc").value, section: $("#adds").value } }); toast(r.name + " hinzugefügt"); renderDeck(id); });
  view.querySelectorAll("[data-img]").forEach((el) => (el.onclick = () => preview(el.dataset.img)));
  view.querySelectorAll("[data-del]").forEach((b) => (b.onclick = async () => { await api(`/api/decks/${id}/cards?name=${encodeURIComponent(b.dataset.del)}&section=${b.dataset.sec}`, { method: "DELETE" }); renderDeck(id); }));
}

function tabAnalysis(id) {
  const a = DECK.analysis;
  const max = Math.max(1, ...Object.values(a.curve));
  const labels = { lands: "Länder", ramp: "Ramp", draw: "Kartenvorteil", removal: "Removal", wipe: "Brettwischer", protection: "Schutz", wincon: "Wincons" };
  const meter = (k) => { const v = a.counts[k] ?? 0, [lo, hi] = a.targets[k], scale = hi * 1.4;
    const cls = v < lo ? "low" : v > hi ? "high" : "";
    return `<div class="meter"><span>${labels[k]}</span><div class="bar"><b style="left:${(lo / scale) * 100}%;width:${((hi - lo) / scale) * 100}%"></b><i class="${cls}" style="width:${Math.min(100, (v / scale) * 100)}%"></i></div><span>${v} <span class="muted small">/${lo}–${hi}</span></span></div>`; };
  $("#tab").innerHTML = `
    ${a.problems.length ? `<div class="panel">${a.problems.map((p) => `<div class="problem">✗ ${esc(p)}</div>`).join("")}</div>` : ""}
    <div class="panel"><h3 style="margin-top:0">Manakurve (ohne Länder)</h3>
      <div class="curve">${Object.entries(a.curve).map(([k, v]) => `<div style="height:${(v / max) * 100}%"><span>${v}</span></div>`).join("")}</div>
      <div class="curve-labels">${Object.keys(a.curve).map((k) => `<span>${k === "7" ? "7+" : k}</span>`).join("")}</div></div>
    <div class="panel"><h3 style="margin-top:0">Rollen im Deck</h3>${Object.keys(labels).map(meter).join("")}
      <p class="muted small">Grauer Bereich = Richtwert. Zählung per Kartentext – Grenzfälle möglich.</p>
      ${a.advice.map((x) => `<div class="hint">• ${esc(x.text)}</div>`).join("")}
      <details><summary class="small muted">Welche Karten zählen wofür?</summary>${Object.entries(a.category_cards).map(([k, v]) => `<p class="small"><b>${labels[k] || k}:</b> ${v.map(esc).join(", ") || "–"}</p>`).join("")}</details></div>
    <div class="panel"><h3 style="margin-top:0">Bracket</h3><p>Geschätzt: <b>Bracket ${a.bracket_estimate}</b> – ${esc(a.bracket_reason)}</p>
      <p class="small">Game Changer: ${a.game_changers.map(esc).join(", ") || "keine"}</p>${a.notes.map((n) => `<div class="hint small">• ${esc(n)}</div>`).join("")}
      <p><button id="cb">Combos prüfen (Commander Spellbook)</button></p><div id="combos"></div></div>
    <div class="panel"><h3 style="margin-top:0">Farbquellen (Länder)</h3>${Object.entries(a.color_sources).filter(([c]) => a.color_identity.includes(c)).map(([c, n]) => `<span style="margin-right:1rem">${pips([c])} ${n}</span>`).join("")}</div>`;
  $("#cb").onclick = (e) => busy(e.target, async () => {
    const r = await api(`/api/decks/${id}/combos`);
    const fmt = (x) => `<div class="small" style="margin:.3rem 0">• ${x.cards.map(esc).join(" + ")} → ${x.result.map(esc).join(", ")} ${x.url ? `<a href="${x.url}" target="_blank">↗</a>` : ""}</div>`;
    $("#combos").innerHTML = r.error ? `<p class="hint">Combo-Check nicht erreichbar: ${esc(r.error)}</p>` :
      `<h3>Im Deck (${r.included.length})</h3>${r.included.map(fmt).join("") || '<p class="muted small">Keine kompletten Combos.</p>'}
       <h3>Fehlt nur 1 Karte (${r.almost.length})</h3>${r.almost.map(fmt).join("") || '<p class="muted small">–</p>'}`;
  });
}

function tabAdvisor(id) {
  $("#tab").innerHTML = `<div class="panel"><p>Der Berater sucht Tausche: zuerst Karten aus deiner Sammlung, dann Käufe bis zum Budget (${eur(DECK.deck.budget_eur)}), passend zu Ziel-Bracket ${DECK.deck.bracket}.</p>
    <label>Fokus (optional)</label><input id="focus" style="width:100%" placeholder="z. B. mehr Schutz gegen Brettwischer · schneller werden · weniger 7-Drops">
    <div class="row" style="margin-top:.7rem"><label style="margin:0">Anzahl Tausche</label><input id="cnt" type="number" value="8" style="width:4.5rem">
      <button class="primary" id="sg">Vorschläge (${esc(STATUS.models?.default || "")})</button>
      <button id="sgd">Tiefenanalyse (${esc(STATUS.models?.deep || "")})</button></div>
    ${STATUS.ai ? "" : '<p class="hint small">Kein ANTHROPIC_API_KEY gesetzt – es gibt nur regelbasierte Vorschläge.</p>'}</div><div id="res"></div>`;
  const run = (deep) => async () => {
    const r = await api(`/api/decks/${id}/suggest`, { method: "POST", body: { deep, focus: $("#focus").value, count: +$("#cnt").value } });
    $("#res").innerHTML = `<div class="panel"><p>${esc(r.summary)}</p>
      <div class="row small"><span class="badge">Kosten ${eur(r.cost_eur)}</span><span class="badge">${r.candidates} Kandidaten geprüft</span>${r.edhrec ? '<span class="badge good">EDHREC-Daten</span>' : '<span class="badge warn">ohne EDHREC</span>'}${r.model ? `<span class="badge">${esc(r.model)}</span>` : ""}</div>
      ${r.swaps.map((s, i) => `<div class="swap"><div><div class="arrow"><span class="out">${esc(s.out)}</span> → <span class="in" data-img="${esc(s.image)}" style="cursor:pointer">${esc(s.in)}</span></div>
        <div class="small muted">${esc(s.reason)}</div><div class="row small" style="margin-top:.2rem">${s.owned ? '<span class="badge good">✓ besessen</span>' : `<span class="badge bad">kaufen ${eur(s.eur)}</span>`}${s.in_deck?.length ? `<span class="badge warn">⚠ steckt in ${esc(s.in_deck.join(", "))}</span>` : ""}</div></div>
        <button data-swap="${i}">Übernehmen</button></div>`).join("") || '<p class="muted">Keine Vorschläge.</p>'}</div>`;
    view.querySelectorAll("[data-img]").forEach((el) => (el.onclick = () => preview(el.dataset.img)));
    view.querySelectorAll("[data-swap]").forEach((b) => (b.onclick = () => busy(b, async () => {
      const s = r.swaps[+b.dataset.swap];
      await api(`/api/decks/${id}/swap`, { method: "POST", body: { out: s.out, into: s.in } });
      b.textContent = "✓ übernommen"; b.disabled = true; b.onclick = null; toast(`${s.out} → ${s.in}`);
    })));
  };
  $("#sg").onclick = (e) => busy(e.target, run(false));
  $("#sgd").onclick = (e) => busy(e.target, run(true));
}

async function tabShop(id) {
  $("#tab").innerHTML = '<p class="muted">Lade …</p>';
  const s = await api(`/api/decks/${id}/shopping`);
  const over = s.total_eur > s.budget_eur;
  $("#tab").innerHTML = `<div class="panel"><div class="row"><b>Fehlende Karten: ${s.missing.length}</b><span class="spacer"></span>
      <span class="badge ${over ? "bad" : "good"}">${eur(s.total_eur)} von ${eur(s.budget_eur)}</span></div>
    <table>${s.missing.map((m) => `<tr><td>${m.qty > 1 ? m.qty + "× " : ""}${esc(m.name)}</td><td>${eur(m.eur)}</td><td>${m.cardmarket ? `<a href="${esc(m.cardmarket)}" target="_blank">Cardmarket ↗</a>` : ""}</td></tr>`).join("") || '<tr><td class="muted">Alles da 🎉</td></tr>'}</table>
    <p class="muted small">Preise: Cardmarket-Trend laut Scryfall (täglich aktualisiert).</p></div>
    ${s.borrowed.length ? `<div class="panel"><h3 style="margin-top:0">⚠ Aus anderen Decks ausgeliehen</h3>${s.borrowed.map((b) => `<div class="small">${esc(b.name)} – steckt in ${esc(b.in_decks.join(", "))}</div>`).join("")}</div>` : ""}`;
}

async function tabMore(id) {
  const txt = await api(`/api/decks/${id}/export`);
  $("#tab").innerHTML = `<div class="panel"><h3 style="margin-top:0">Export (Moxfield/Archidekt-Format)</h3><textarea readonly id="ex">${esc(txt)}</textarea>
      <p><button id="cp">Kopieren</button></p></div>
    <div class="panel"><h3 style="margin-top:0">Verlauf</h3>${DECK.history.map((h) => `<div class="small">${new Date(h.created_at * 1000).toLocaleString("de-DE")} – ${esc(h.action)}</div>`).join("") || '<p class="muted small">Noch keine Änderungen.</p>'}</div>
    <div class="panel"><button id="del" style="color:var(--bad)">Deck löschen</button></div>`;
  $("#cp").onclick = async () => { try { await navigator.clipboard.writeText(txt); toast("Kopiert"); } catch { $("#ex").select(); toast("Markiert – jetzt kopieren"); } };
  $("#del").onclick = async (e) => { if (e.target.dataset.sure) { await api(`/api/decks/${id}`, { method: "DELETE" }); location.hash = "decks"; } else { e.target.dataset.sure = 1; e.target.textContent = "Wirklich löschen? Nochmal tippen"; } };
}

// ---------- Sammlung ----------
async function renderCollection() {
  view.innerHTML = `<div class="row"><h1>Sammlung</h1><span class="spacer"></span></div>
    <div class="panel"><b>Collectr-Export importieren</b> <span class="muted small">(ersetzt die bisherige Sammlung)</span>
      <div class="row" style="margin-top:.5rem"><input type="file" id="f" accept=".csv"><button class="primary" id="imp">Importieren</button></div><div id="impres" class="small"></div></div>
    <div class="panel"><div class="row"><input id="q" placeholder="Suche Name oder Typ (z. B. Dinosaur)" style="flex:1">
      <select id="col"><option value="">alle Farben</option><option value="RGW">Naya (RGW)</option><option value="WUBRG">alles</option><option value="G">nur Grün</option><option value="R">nur Rot</option><option value="W">nur Weiß</option><option value="U">nur Blau</option><option value="B">nur Schwarz</option></select>
      <label class="small" style="margin:0"><input type="checkbox" id="free"> nur freie</label></div><div id="list" style="margin-top:.6rem"></div></div>`;
  const load = async () => {
    const r = await api(`/api/collection?q=${encodeURIComponent($("#q").value)}&color=${$("#col").value}&only_free=${$("#free").checked}`);
    $("#list").innerHTML = `<p class="muted small">${r.cards.length} Karten · Wert ca. ${eur(r.total_eur)}${r.unresolved.length ? ` · ${r.unresolved.length} nicht erkannt` : ""}</p>
      ${r.cards.slice(0, 400).map((c) => `<div class="cardline"><span class="small muted" style="width:1.6rem">${c.qty}×</span><span class="name" data-img="${esc(c.image)}">${esc(c.name)}</span>
        ${pips(c.color_identity)}<span class="small muted">${eur(c.eur)}</span>${c.in_decks.length ? `<span class="badge warn">${esc(c.in_decks.join(", "))}</span>` : ""}</div>`).join("")}
      ${r.unresolved.length ? `<details><summary class="small muted">Nicht erkannt</summary><p class="small">${r.unresolved.map(esc).join("; ")}</p></details>` : ""}`;
    view.querySelectorAll("[data-img]").forEach((el) => (el.onclick = () => preview(el.dataset.img)));
  };
  let t; ["q", "col", "free"].forEach((i) => $("#" + i).addEventListener("input", () => { clearTimeout(t); t = setTimeout(load, 250); }));
  $("#imp").onclick = (e) => busy(e.target, async () => {
    const f = $("#f").files[0]; if (!f) return toast("Bitte CSV wählen");
    const fd = new FormData(); fd.append("file", f);
    $("#impres").textContent = "Importiere und gleiche mit Scryfall ab – kann 1–2 Minuten dauern …";
    const r = await api("/api/collection/import", { method: "POST", body: fd });
    $("#impres").innerHTML = `✓ ${r.imported} Einträge (${r.cards} Karten) importiert${r.unresolved.length ? `, ${r.unresolved.length} nicht erkannt` : ""}.`;
    load();
  });
  load();
}

// ---------- Commander finden ----------
async function renderCommanders() {
  view.innerHTML = '<h1>Commander aus deiner Sammlung</h1><p class="muted">Legendäre Kreaturen, die du besitzt – sortiert nach passenden Karten in ihren Farben.</p><div id="cl"><p class="muted">Lade …</p></div>';
  const list = await api("/api/commanders/owned");
  $("#cl").innerHTML = `<div class="grid">${list.map((c, i) => `<div class="panel"><div class="row"><b style="flex:1">${esc(c.name)}</b>${pips(c.color_identity)}</div>
    <div class="small muted">${c.owned_fitting} eigene Karten passen farblich</div>
    <div class="row" style="margin-top:.5rem"><button class="mini" data-fit="${i}">EDHREC-Abgleich</button><button class="mini" data-img="${esc(c.image_small)}">Bild</button><button class="mini" data-build="${i}">Deck anlegen</button></div><div class="small" id="fit${i}"></div></div>`).join("") || '<p class="muted">Erst die Sammlung importieren.</p>'}</div>`;
  view.querySelectorAll("[data-img]").forEach((el) => (el.onclick = () => preview(el.dataset.img)));
  view.querySelectorAll("[data-fit]").forEach((b) => (b.onclick = () => busy(b, async () => {
    const c = list[+b.dataset.fit], r = await api(`/api/commanders/${encodeURIComponent(c.name)}/fit`);
    $("#fit" + b.dataset.fit).innerHTML = r.edhrec_cards ? `<p><b>${r.percent}%</b> der EDHREC-Liste besitzt du (${r.owned}/${r.edhrec_cards}).</p><p class="muted">${r.cards.slice(0, 12).map((x) => esc(x.name)).join(", ")}</p>` : '<p class="hint">Keine EDHREC-Daten gefunden.</p>';
  })));
  view.querySelectorAll("[data-build]").forEach((b) => (b.onclick = () => busy(b, async () => {
    const c = list[+b.dataset.build];
    const r = await api("/api/decks", { method: "POST", body: { name: c.name.split(",")[0] + " (neu)", commander: c.name, bracket: 2, budget_eur: 25 } });
    location.hash = "deck-" + r.id;
  })));
}

// ---------- Router ----------
async function route() {
  try {
    STATUS = await api("/api/status");
    if (!STATUS.logged_in) return renderLogin();
    const h = location.hash.slice(1) || "decks";
    const navKey = { quiz: "coach", start: "coach", wiz: "coach" }[h.split("-")[0]] || h.split("-")[0];
    document.querySelectorAll("nav a").forEach((a) => a.classList.toggle("active", a.getAttribute("href") === "#" + navKey));
    if (!KNOW) know().catch(() => {});
    if (h.startsWith("deck-")) return await renderDeck(+h.slice(5));
    if (h.startsWith("wiz-")) return await renderWizard(+h.slice(4));
    if (h === "coach") return await renderCoachHome();
    if (h === "quiz") return await renderQuiz();
    if (h === "start") return await renderStart();
    if (h === "collection") return await renderCollection();
    if (h === "commanders") return await renderCommanders();
    return await renderDecks();
  } catch (e) { if (e.message !== "login") view.innerHTML = `<p class="problem">Fehler: ${esc(e.message)}</p>`; }
}
window.addEventListener("hashchange", () => { DECKTAB = location.hash.startsWith("#deck-") ? DECKTAB : "cards"; route(); });
window.addEventListener("DOMContentLoaded", route);
