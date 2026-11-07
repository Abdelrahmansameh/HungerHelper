// Page « Mon carnet » — tableau de bord des quêtes suivies (HungerProgress + /api/tracker).
// Deux blocs : CARTES multi-quêtes (couleur par quête, fusion géo, maj dynamique) + QUÊTES SUIVIES.
(function () {
  'use strict';
  var HP = window.HungerProgress;
  var body = document.getElementById('tracker-body');
  if (!HP || !body) { return; }
  var TXT = (window.HUNGER_TRACKER && window.HUNGER_TRACKER.txt) || {};
  var OBJTYPE = (window.HUNGER_TRACKER && window.HUNGER_TRACKER.objtype) || {};
  var empty = document.getElementById('tracker-empty');
  var countEl = document.getElementById('tracker-count');
  var questsEl = document.getElementById('tracker-quests');
  var mapsWrap = document.getElementById('tracker-maps-wrap');
  var mapsEl = document.getElementById('tracker-maps');
  var legendEl = document.getElementById('tracker-legend');
  var PALETTE = ['#e9745e', '#5ec5e9', '#7ed957', '#c77dff', '#ff9f43', '#4ecca3', '#f4c542', '#f06292', '#a1887f', '#26c6da'];
  var DATA = { quests: [], maps: [], points: [] };
  var fetchedKey = null;
  var lastJson = null;     // dernière réponse brute /api/tracker (évite une reconstruction si rien n'a changé)
  var LMAPS = [];        // { leaflet, markers:[{marker, okeys:[], nullOkey:bool, on:bool}] }
  var colorOf = {};      // slug → couleur (partagée carte / légende / cartes de quête)
  // Visibilité carte par quête (masquée = suivie mais pas affichée sur la carte). Persistée.
  var MHK = 'hunger_tracker_maphidden';
  function loadHidden() { try { return JSON.parse(localStorage.getItem(MHK)) || {}; } catch (e) { return {}; } }
  function saveHidden() { try { localStorage.setItem(MHK, JSON.stringify(mapHidden)); } catch (e) {} }
  var mapHidden = loadHidden();
  var activeMapId = null, questMaps = {}, curQs = [];   // filtre carte↔liste : carte active + slug→cartes

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function trackedKey() { return HP.trackedSlugs().slice().sort().join(','); }
  function trackedSet() { var o = {}; HP.trackedSlugs().forEach(function (s) { o[s] = 1; }); return o; }
  function questUrl(q) { return q.npc_slug ? ('/quests/' + q.npc_slug + '/' + q.slug) : ('/quests/' + q.slug); }

  function load() {
    var s = HP.trackedSlugs();
    if (!s.length) { DATA = { quests: [], maps: [], points: [] }; fetchedKey = ''; render(true); return; }
    var key = trackedKey();
    if (key === fetchedKey) { render(false); return; }   // ensemble inchangé → maj légère (pas de rebuild carte)
    fetch('/api/tracker?slugs=' + encodeURIComponent(s.join(',')), { credentials: 'same-origin' })
      .then(function (r) { return r.ok ? r.text() : '{"quests":[]}'; })
      .then(function (txt) {
        // Resynchro périodique (progress-sync, ~20 s) : données identiques → maj légère, sans reconstruire les cartes
        // (sinon un glisser/zoom en cours était interrompu toutes les 20 s).
        var same = txt === lastJson && LMAPS.length > 0;
        var d; try { d = JSON.parse(txt); } catch (e) { d = null; }
        DATA = d || { quests: [] }; lastJson = txt; fetchedKey = key; pruneOrphans(); render(!same);
      })
      .catch(function () { render(true); });
  }

  // Purge les slugs suivis absents de la réponse (quête retirée par un build). Prudent : jamais si réponse
  // vide (build changé / transitoire) ni si l'on frôle le plafond serveur (120) — sinon risque de faux positif.
  function pruneOrphans() {
    var qs = DATA.quests || [];
    if (!qs.length || HP.trackedSlugs().length > 120) { return; }
    var valid = {}; qs.forEach(function (q) { valid[q.slug] = 1; });
    var pruned = false;
    HP.trackedSlugs().forEach(function (s) { if (!valid[s]) { HP.setTracked(s, false); pruned = true; } });
    if (pruned) { HP.changed(); }
  }

  function render(rebuild) {
    var tr = trackedSet();
    var qs = (DATA.quests || []).filter(function (q) { return tr[q.slug]; });
    if (!qs.length) { empty.hidden = false; body.hidden = true; countEl.hidden = true; destroyMaps(); return; }
    empty.hidden = true; body.hidden = false;
    countEl.hidden = false; countEl.textContent = qs.length;
    // Couleur par quête (ordre de suivi) — partagée entre cartes, légende et cartes de quête.
    colorOf = {}; var idx = colorIndexes(qs.map(function (q) { return q.slug; }));
    qs.forEach(function (q) { colorOf[q.slug] = colorAt(idx[q.slug]); });
    curQs = qs;
    // Quête → cartes où elle a des points (pour filtrer la liste par carte sélectionnée).
    questMaps = {};
    (DATA.points || []).forEach(function (p) { if (tr[p.quest]) { (questMaps[p.quest] || (questMaps[p.quest] = {}))[p.map_id] = 1; } });
    if (rebuild) { buildMaps(qs); } else { updateMapMarkers(); }   // buildMaps → setupMapTabs fixe activeMapId
    renderQuests();
  }

  // Quêtes affichées dans la liste = suivies, NON masquées via la légende, ET sur la carte active (si choisie).
  function visibleQuests() {
    return curQs.filter(function (q) {
      if (mapHidden[q.slug]) { return false; }
      if (activeMapId === null) { return true; }
      var qm = questMaps[q.slug];
      return !qm || !!qm[activeMapId];   // sur la carte active, ou quête sans point de carte (toujours visible)
    });
  }

  // ---------- Quêtes suivies ----------
  // Prête à rendre : tous les objectifs requis cochés (ou quête marquée terminée ailleurs).
  function questReady(q) {
    if (HP.questExplicit(q.slug)) { return true; }
    var req = (q.objectives || []).filter(function (o) { return !o.optional && o.okey; });
    return req.length > 0 && req.every(function (o) { return HP.objDone(o.okey); });
  }
  // Terminer depuis le carnet = comme sur la fiche quête (terminée + objectifs cochés + plus suivie),
  // et la suite de la chaîne prend sa place dans le carnet (demande Discord).
  var lastNext = [];
  function completeQuest(slug) {
    var q = null; curQs.forEach(function (x) { if (x.slug === slug) { q = x; } });
    if (!q) { return; }
    HP.setQuest(slug, true);
    HP.setObjs((q.objectives || []).map(function (o) { return o.okey; }).filter(Boolean), true);
    HP.setTracked(slug, false);
    lastNext = (q.next || []).filter(function (n) { return !HP.questExplicit(n.slug); });
    lastNext.forEach(function (n) { HP.setTracked(n.slug, true); });
    HP.changed();
    armNoteTimer();
  }
  // Le bandeau s'efface tout seul après quelques secondes (fondu), sans attendre une autre action.
  var noteTimer = null;
  function armNoteTimer() {
    clearTimeout(noteTimer);
    if (!lastNext.length) { return; }
    noteTimer = setTimeout(function () {
      lastNext = [];
      var el = questsEl.querySelector('.trk-nextnote'); if (!el) { return; }
      el.classList.add('is-leaving');
      setTimeout(function () { if (el.parentNode) { el.parentNode.removeChild(el); } }, 500);
    }, 6000);
  }
  function nextNote() {
    if (!lastNext.length) { return ''; }
    var links = lastNext.map(function (n) { return '<a href="' + esc(questUrl(n)) + '">' + esc(n.title) + '</a>'; }).join(', ');
    return '<p class="trk-nextnote">✓ ' + esc(TXT.next_tracked || 'Next quest tracked:') + ' ' + links + '</p>';
  }
  function currentIdx(objs) {   // 1er objectif non fait & non optionnel = « à faire maintenant »
    for (var k = 0; k < objs.length; k++) { var o = objs[k]; if (!o.optional && !(o.okey && HP.objDone(o.okey))) { return k; } }
    return -1;
  }
  function objRow(o, current) {
    var d = o.okey && HP.objDone(o.okey);
    var badge = o.type_label ? '<span class="obj-type">' + esc(o.type_label) + '</span> ' : '';
    var txt = (o.html && o.html.replace(/<[^>]*>/g, '').trim()) ? o.html : '';
    var extra = '';
    if (o.count > 1) { extra += ' <span class="muted">×' + o.count + '</span>'; }
    if (o.place_name) { extra += ' <span class="muted">→ ' + esc(o.place_name) + '</span>'; }
    if (o.npc_slug) { extra += ' <a class="muted" href="/npcs/' + esc(o.npc_slug) + '">→ ' + esc(o.npc_name) + '</a>'; }
    if (!txt && o.item_slug) { txt = '<a href="/items/' + esc(o.item_slug) + '">' + esc(o.item_name) + '</a>'; }
    var drop = o.drop ? '<span class="trk-drop" title="' + esc(TXT.droptip || 'Best drop spot') + '">' + hcIcon('target') +
      esc(o.drop.container) + ' ' + (window.hcOdds ? window.hcOdds(o.drop.pct / 100) : o.drop.pct + '%') + (o.drop.map_name ? ' · ' + esc(o.drop.map_name) : '') + '</span>' : '';
    var content = badge + txt + extra + drop;
    if (!content.replace(/<[^>]*>/g, '').trim()) { content = '<span class="muted">—</span>'; }
    return '<li class="trk-obj' + (d ? ' is-done' : '') + (o.optional ? ' is-opt' : '') + (current ? ' is-current' : '') + '">' +
      '<button type="button" class="trk-obj__check" data-okey="' + esc(o.okey) + '">' + (d ? '✓' : '') + '</button>' +
      '<span class="trk-obj__txt">' + content + '</span></li>';
  }
  function renderQuests() {
    var qs = visibleQuests();
    if (!qs.length) { questsEl.innerHTML = nextNote() + '<p class="muted trk-nomap">' + esc(TXT.nomap || '—') + '</p>'; return; }
    questsEl.innerHTML = nextNote() + qs.map(function (q) {
      var col = colorOf[q.slug] || '#999';
      var objsArr = q.objectives || [];
      var total = objsArr.length;
      var done = objsArr.filter(function (o) { return o.okey && HP.objDone(o.okey); }).length;
      var cur = currentIdx(objsArr);
      var objs = objsArr.map(function (o, k) { return objRow(o, k === cur); }).join('');
      var rewards = (q.rewards || []).filter(function (r) { return r.name; }).map(function (r) {
        return '<span class="trk-reward">' + (r.icon ? '<img loading="lazy" src="' + esc(r.icon) + '" alt="">' : '') +
          esc(r.name) + (r.amount ? ' ×' + esc(r.amount) : '') + '</span>';
      }).join('');
      var kind = (q.kind && q.kind !== 'standard') ? '<span class="quest-card__kind quest-card__kind--' + esc(q.kind) + '">' + hcIcon('repeat') + '</span> ' : '';
      var repeat = q.kind && q.kind !== 'standard';   // répétable : jamais « terminée » (comme la fiche)
      var ready = !repeat && questReady(q);
      var nextTitles = (q.next || []).map(function (n) { return n.title; }).join(', ');
      var finish = ready ? '<div class="trk-quest__finish"><button type="button" class="btn btn--primary btn--sm" data-complete="' + esc(q.slug) + '">✓ ' +
        esc(q.next && q.next.length ? (TXT.complete_next || 'Complete & track next quest') : (TXT.complete || 'Mark as completed')) + '</button>' +
        (nextTitles ? ' <span class="muted small">→ ' + esc(nextTitles) + '</span>' : '') + '</div>' : '';
      return '<div class="trk-quest' + (ready ? ' is-ready' : '') + '" data-slug="' + esc(q.slug) + '" style="border-left-color:' + col + '">' +
        '<div class="trk-quest__head">' +
        '<span class="trk-quest__dot" style="background:' + col + '"></span>' + kind +
        '<a class="trk-quest__title" href="' + esc(questUrl(q)) + '">' + esc(q.title) + '</a>' +
        (q.npc_name ? '<span class="muted"> · ' + esc(q.npc_name) + '</span>' : '') +
        '<span class="trk-quest__prog muted">' + done + '/' + total + '</span>' +
        (repeat ? '' : '<button type="button" class="trk-quest__done" data-complete="' + esc(q.slug) + '" title="' + esc(TXT.complete || 'Mark as completed') + '">✓</button>') +
        '<button type="button" class="trk-quest__untrack" data-untrack="' + esc(q.slug) + '" title="' + esc(TXT.untrack || 'Untrack') + '">✕</button></div>' +
        '<ul class="trk-objs">' + objs + '</ul>' + finish +
        (rewards ? '<div class="trk-quest__rewards"><span class="muted">' + esc(TXT.rewards || 'Rewards') + ' :</span> ' + rewards + '</div>' : '') +
        '</div>';
    }).join('');
  }

  // ---------- Cartes multi-quêtes (un marqueur par point, couleur par quête) ----------
  // Reconstruction : on détruit les cartes Leaflet MAIS on garde (hors DOM) l'état utilisateur — vue zoomée/déplacée
  // par carte (VIEWS) et carte en plein écran (fsMapId) — que buildMaps réapplique. Le plein écran (.is-fs + body)
  // est toujours nettoyé ici : sinon topbar/sidebar restaient masquées et la page ne défilait plus (retour Ray).
  var VIEWS = {};        // mapId → { c: LatLng, z: zoom } — seulement si l'utilisateur a zoomé/déplacé
  var fsMapId = null;    // mapId de la carte en plein écran (survit aux reconstructions)
  function destroyMaps() {
    LMAPS.forEach(function (m) { m.dead = true; try { m.leaflet.stop(); m.leaflet.remove(); } catch (e) {} });
    LMAPS = []; if (mapsEl) { mapsEl.innerHTML = ''; }
    document.body.classList.remove('trk-fs-on');
  }
  function entryOf(lf) { for (var i = 0; i < LMAPS.length; i++) { if (LMAPS[i].leaflet === lf) { return LMAPS[i]; } } return null; }
  // invalidateSize différé, sans effet si la carte a été détruite entre-temps (sinon erreur Leaflet _leaflet_pos).
  function laterResize(lf) {
    setTimeout(function () { var m = entryOf(lf); if (m && !m.dead) { quiet(m, function () { lf.invalidateSize(); }); } }, 60);
  }
  // Mouvement programmatique (cadrage auto) : ne doit pas être pris pour une action de l'utilisateur.
  function quiet(m, fn) { m.prog = true; try { fn(); } finally { m.prog = false; } }
  // Cadrage : la vue de l'utilisateur si elle existe, sinon l'emprise des points visibles.
  function frame(m) {
    if (m.leaflet.getContainer().clientWidth <= 0) { return; }   // onglet masqué → taille 0, on ne cadre pas
    var v = VIEWS[m.mapId];
    if (v) { quiet(m, function () { m.leaflet.setView(v.c, v.z, { animate: false }); }); return; }
    var lls = m.markers.filter(function (mk) { return mk.on; }).map(function (mk) { return mk.marker.getLatLng(); });
    if (lls.length) { quiet(m, function () { m.leaflet.fitBounds(lls, { padding: [22, 22], maxZoom: 1, animate: false }); }); }
  }
  // Couleur FIXE par quête suivie : index attribué au suivi (premier libre) et gardé tant qu'elle reste suivie.
  // Connecté : le serveur fait foi (progress-sync.js, mêmes couleurs que l'appli overlay) ; sinon attribution locale.
  var CK = 'hunger_quest_tracked_colors';
  function colorIndexes(slugs) {
    var m; try { m = JSON.parse(localStorage.getItem(CK)) || {}; } catch (e) { m = {}; }
    var used = {}, out = {}, i;
    slugs.forEach(function (s) { if (typeof m[s] === 'number' && !used[m[s]]) { used[m[s]] = 1; out[s] = m[s]; } });
    slugs.forEach(function (s) {
      if (out[s] !== undefined) { return; }
      for (i = 0; used[i]; i++) {}
      used[i] = 1; out[s] = i;
    });
    var keep = {};   // on garde les index des quêtes suivies pas encore chargées (réponse /api/tracker partielle)
    HP.trackedSlugs().forEach(function (s) { if (out[s] !== undefined) { keep[s] = out[s]; } else if (typeof m[s] === 'number') { keep[s] = m[s]; } });
    try { localStorage.setItem(CK, JSON.stringify(keep)); } catch (e) {}
    return out;
  }
  function colorAt(i) { return i < PALETTE.length ? PALETTE[i] : 'hsl(' + Math.round((i * 137.508) % 360) + ',62%,60%)'; }
  // Objectif/lieu = disque plein ; drop (loot) = ANNEAU creux (distinct visuellement).
  function markerIcon(color, type) {
    var span = type === 'loot'
      ? '<span style="display:block;width:13px;height:13px;border-radius:50%;background:transparent;border:3px solid ' + color + ';box-shadow:0 0 4px rgba(0,0,0,.8)"></span>'
      : '<span style="display:block;width:15px;height:15px;border-radius:50%;background:' + color + ';border:2px solid #fff;box-shadow:0 0 4px rgba(0,0,0,.7)"></span>';
    return L.divIcon({ className: 'trk-marker' + (type === 'loot' ? ' trk-marker--loot' : ''), html: span, iconSize: [16, 16], iconAnchor: [8, 8], popupAnchor: [0, -8] });
  }
  // Plein écran « in-page » (comme /maps) : overlay CSS via .is-fs, pas l'API navigateur. Échap pour sortir.
  function fsToggle(lf) {
    var wrap = lf.getContainer().closest('.trk-map'); if (!wrap) { return; }
    var on = wrap.classList.toggle('is-fs');
    document.body.classList.toggle('trk-fs-on', on);
    var m = entryOf(lf); fsMapId = on && m ? m.mapId : null;
    laterResize(lf);
  }
  function addFs(lf) {
    var Ctl = L.Control.extend({ options: { position: 'topright' }, onAdd: function () {
      var b = L.DomUtil.create('button', 'trk-fs-btn'); b.type = 'button'; b.innerHTML = '⛶'; b.setAttribute('title', TXT.fullscreen || 'Fullscreen');
      L.DomEvent.disableClickPropagation(b);
      L.DomEvent.on(b, 'click', function (e) { L.DomEvent.stop(e); fsToggle(lf); });
      return b;
    } });
    lf.addControl(new Ctl());
  }
  if (!window.__trkFsEsc) {
    window.__trkFsEsc = true;
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') { return; }
      var el = document.querySelector('.trk-map.is-fs'); if (!el) { return; }
      el.classList.remove('is-fs'); document.body.classList.remove('trk-fs-on'); fsMapId = null;
      LMAPS.forEach(function (m) { laterResize(m.leaflet); });
    });
  }

  function buildMaps(qs) {
    if (!window.L || !mapsWrap) { return; }
    destroyMaps();
    var tr = trackedSet();
    var maps = (DATA.maps || []);
    var titleOf = {}; qs.forEach(function (q) { titleOf[q.slug] = q.title; });
    // Toutes les quêtes suivies ayant des points (pour la légende togglable) ; les masquées ne sont pas tracées.
    var trackedPts = (DATA.points || []).filter(function (p) { return tr[p.quest]; });
    var pts = trackedPts.filter(function (p) { return !mapHidden[p.quest]; });
    if (!trackedPts.length) { mapsWrap.hidden = true; fsMapId = null; return; }
    mapsWrap.hidden = false;

    // Légende = TOGGLE : chaque quête (ayant des points) est un bouton ; cliquer masque/affiche sur la carte.
    var present = {}; trackedPts.forEach(function (p) { present[p.quest] = true; });
    legendEl.innerHTML = qs.filter(function (q) { return present[q.slug]; }).map(function (q) {
      var off = !!mapHidden[q.slug];
      return '<button type="button" class="trk-legend__item' + (off ? ' is-off' : '') + '" data-legend="' + esc(q.slug) + '">' +
        '<span class="trk-legend__dot" style="background:' + colorOf[q.slug] + '"></span>' + esc(q.title) + '</button>';
    }).join('');

    maps.forEach(function (m) {
      var mp = pts.filter(function (p) { return p.map_id === m.id; });
      if (!mp.length) { return; }
      var wrap = document.createElement('div'); wrap.className = 'trk-map' + (m.id === fsMapId ? ' is-fs' : '');
      var h = document.createElement('h3'); h.className = 'trk-map__title'; h.textContent = m.name;
      var cv = document.createElement('div'); cv.className = 'trk-map__canvas'; cv.id = 'trk-map-' + m.id;
      wrap.appendChild(h); wrap.appendChild(cv); mapsEl.appendChild(wrap);

      var bounds = [[0, 0], [m.height, m.width]];
      var lf = L.map(cv.id, { crs: L.CRS.Simple, minZoom: -4, maxZoom: 2, zoomSnap: 0, attributionControl: false, zoomControl: true });
      L.imageOverlay(m.image, bounds).addTo(lf);
      addFs(lf);
      var markers = [], lls = [];
      mp.forEach(function (p) {
        var ll = [m.height - p.y, p.x]; lls.push(ll);
        var mk = L.marker(ll, { icon: markerIcon(colorOf[p.quest] || '#999', p.type) });
        mk.bindTooltip('<b style="color:' + (colorOf[p.quest] || '#fff') + '">' + esc(titleOf[p.quest] || '') + '</b><br>' + esc(p.title || p.type), { direction: 'top', opacity: 0.96 });
        markers.push({ marker: mk, okey: p.okey, quest: p.quest, on: false });
      });
      lf.fitBounds(lls, { padding: [22, 22], maxZoom: 1, animate: false });   // cadrage provisoire (frame() ensuite)
      var ent = { leaflet: lf, markers: markers, wrap: wrap, mapId: m.id };
      // Zoom/déplacement venant de l'utilisateur → on mémorise sa vue et on ne recadre plus automatiquement.
      lf.on('movestart zoomstart', function () { if (!ent.prog) { ent.user = true; } });
      lf.on('moveend', function () { if (ent.user && !ent.dead) { VIEWS[ent.mapId] = { c: lf.getCenter(), z: lf.getZoom() }; } });
      LMAPS.push(ent);
    });
    // Plein écran conservé à travers la reconstruction (si la carte existe encore), sinon abandonné.
    var fsOk = fsMapId !== null && LMAPS.some(function (x) { return x.mapId === fsMapId; });
    if (fsMapId !== null && !fsOk) { fsMapId = null; }
    if (fsOk) { activeMapId = fsMapId; }
    document.body.classList.toggle('trk-fs-on', fsOk);
    setupMapTabs();
    updateMapMarkers();
  }
  // Plusieurs cartes → onglets. La carte sélectionnée FILTRE aussi la liste de quêtes (renderQuests).
  function setupMapTabs() {
    if (LMAPS.length <= 1) { activeMapId = null; return; }   // 1 carte → pas de filtre carte
    var idx = 0;   // préserve la carte active entre reconstructions, sinon la 1re
    LMAPS.forEach(function (m, i) { if (m.mapId === activeMapId) { idx = i; } });
    activeMapId = LMAPS[idx].mapId;
    var bar = document.createElement('div'); bar.className = 'trk-maptabs';
    LMAPS.forEach(function (m, i) {
      var b = document.createElement('button'); b.type = 'button';
      b.className = 'trk-maptab' + (i === idx ? ' is-on' : '');
      var t = m.wrap.querySelector('.trk-map__title'); b.textContent = t ? t.textContent : ('#' + (i + 1));
      b.addEventListener('click', function () {
        activeMapId = m.mapId;
        bar.querySelectorAll('.trk-maptab').forEach(function (x, j) { x.classList.toggle('is-on', j === i); });
        LMAPS.forEach(function (mm, j) { mm.wrap.style.display = j === i ? '' : 'none'; });
        quiet(m, function () { m.leaflet.invalidateSize(); });
        frame(m);
        renderQuests();   // filtre la liste sur la carte choisie
      });
      bar.appendChild(b);
      m.wrap.style.display = i === idx ? '' : 'none';
    });
    mapsEl.insertBefore(bar, mapsEl.firstChild);
  }
  // Maj DYNAMIQUE : un point disparaît quand son objectif est fait, réapparaît sinon. La carte se recadre sur les
  // points restants SAUF si l'utilisateur a zoomé/déplacé (sa vue est conservée).
  function updateMapMarkers() {
    LMAPS.forEach(function (m) {
      m.markers.forEach(function (mk) {
        var hide = mk.okey && HP.objDone(mk.okey);
        if (hide && mk.on) { m.leaflet.removeLayer(mk.marker); mk.on = false; }
        else if (!hide && !mk.on) { mk.marker.addTo(m.leaflet); mk.on = true; }
      });
      frame(m);
    });
  }

  // Survol d'une quête dans la légende → assombrit chaque carte + met en avant SES points (sur les 3 cartes).
  function focusQuest(slug) {
    LMAPS.forEach(function (m) {
      m.wrap.classList.add('is-focusing');
      m.markers.forEach(function (mk) {
        if (!mk.on) { return; }
        var el = mk.marker.getElement(); if (!el) { return; }
        el.classList.toggle('is-hl', mk.quest === slug);
        el.classList.toggle('is-dim', mk.quest !== slug);
      });
    });
  }
  function unfocus() {
    LMAPS.forEach(function (m) {
      m.wrap.classList.remove('is-focusing');
      m.markers.forEach(function (mk) { var el = mk.marker.getElement(); if (el) { el.classList.remove('is-hl', 'is-dim'); } });
    });
  }
  if (legendEl) {
    legendEl.addEventListener('mouseover', function (e) { var it = e.target.closest('[data-legend]'); if (it) { focusQuest(it.getAttribute('data-legend')); } });
    legendEl.addEventListener('mouseleave', unfocus);
  }

  // Interactions : cocher un objectif, ne plus suivre.
  body.addEventListener('click', function (e) {
    var chk = e.target.closest('.trk-obj__check');
    if (chk) { var k = chk.getAttribute('data-okey'); if (k) { lastNext = []; HP.setObjs([k], !HP.objDone(k)); HP.changed(); } return; }
    var cpl = e.target.closest('[data-complete]');
    if (cpl) { e.preventDefault(); completeQuest(cpl.getAttribute('data-complete')); return; }
    var unt = e.target.closest('[data-untrack]');
    if (unt) { e.preventDefault(); lastNext = []; HP.setTracked(unt.getAttribute('data-untrack'), false); HP.changed(); return; }
    var leg = e.target.closest('[data-legend]');
    if (leg) {   // légende cliquable : afficher/masquer les points de cette quête sur la carte (reste suivie)
      e.preventDefault(); var s = leg.getAttribute('data-legend');
      if (mapHidden[s]) { delete mapHidden[s]; } else { mapHidden[s] = 1; } saveHidden(); render(true); return;
    }
  });

  window.addEventListener('hunger-progress-changed', load);
  window.addEventListener('hunger-progress-synced', function () { fetchedKey = null; load(); });
  load();
})();
