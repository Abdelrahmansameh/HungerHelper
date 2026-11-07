// Resync deux-sens de la progression locale (localStorage) ↔ BD, si connecté.
// - quêtes terminées : fusion à TROIS voies (base QBK), comme le suivi ci-dessous : rouvrir une quête (bouton
//   « Réinitialiser », appli overlay via /api/overlay/v1/me/quests) se propage au lieu d'être ressuscité.
// - objectifs faits : fusion à TROIS voies aussi (base OBK) : le client envoie ses changements (cocher ET décocher),
//   un décochage fait ailleurs (l'appli rouvre une quête) n'est plus ré-imposé par ce navigateur.
// - quêtes SUIVIES : fusion à TROIS voies avec BASE = dernier ensemble reçu du serveur. Le client n'envoie
//   que ses changements (ajouts = local − base, retraits = base − local) ; ce qui a changé ailleurs (autre
//   appareil, appli overlay via /api/overlay/v1/me/track) est conservé, retraits compris.
// Émet « hunger-progress-synced » si le local change.
(function () {
  'use strict';
  if (!window.HUNGER_AUTH) return;
  var QK = 'hunger_quest_done', OK = 'hunger_obj_done', TK = 'hunger_quest_tracked', BK = 'hunger_quest_tracked_base';
  var CK = 'hunger_quest_tracked_colors';
  var QBK = 'hunger_quest_done_base';      // dernier ensemble « terminées » reçu du serveur
  var OBK = 'hunger_obj_done_base';        // dernier ensemble d'objectifs cochés reçu du serveur   // slug → index de palette FIXE attribué par le serveur (tracker.js)
  function load(k) { try { return JSON.parse(localStorage.getItem(k)) || {}; } catch (e) { return {}; } }
  function save(k, o) { try { localStorage.setItem(k, JSON.stringify(o)); } catch (e) {} }

  function buildBody(pushTracked) {
    var quests = load(QK), objs = load(OK), tracked = load(TK);
    var body = '_csrf=' + encodeURIComponent(window.HUNGER_CSRF || '');
    Object.keys(quests).forEach(function (s) { body += '&quests%5B%5D=' + encodeURIComponent(s); });
    Object.keys(objs).forEach(function (i) { body += '&objectives%5B%5D=' + encodeURIComponent(i); });
    if (pushTracked) {   // ensemble suivi local + base : le serveur applique la différence
      body += '&tracked_push=1&tracked_delta=1&quests_delta=1&objectives_delta=1';
      Object.keys(load(OBK)).forEach(function (i) { body += '&objectives_base%5B%5D=' + encodeURIComponent(i); });
      Object.keys(load(QBK)).forEach(function (s) { body += '&quests_base%5B%5D=' + encodeURIComponent(s); });
      Object.keys(tracked).forEach(function (s) { body += '&tracked%5B%5D=' + encodeURIComponent(s); });
      Object.keys(load(BK)).forEach(function (s) { body += '&tracked_base%5B%5D=' + encodeURIComponent(s); });
    }
    return body;
  }

  // local' = serveur + (local − base) − (base − local). Sans base (1re synchro sur ce navigateur) : union.
  function merge3(server, local, base) {
    var out = {};
    server.forEach(function (s) { out[s] = 1; });
    Object.keys(local).forEach(function (s) { if (!base[s]) { out[s] = 1; } });
    Object.keys(base).forEach(function (s) { if (!local[s]) { delete out[s]; } });
    return out;
  }
  function sameSet(a, b) {
    var ka = Object.keys(a), kb = Object.keys(b);
    return ka.length === kb.length && ka.every(function (k) { return b[k]; });
  }

  function syncNow(pushTracked) {
    var quests = load(QK), objs = load(OK);
    var body = buildBody(pushTracked);
    return fetch('/progress/sync', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest' },
      body: body, credentials: 'same-origin'
    }).then(function (r) { return r.ok ? r.json() : null; })
      .then(function (st) {
        if (!st) { return; }
        var changed = false;
        // Terminées : fusion à trois voies contre l'état ACTUEL du navigateur (base = ce qu'on a envoyé au push).
        var qBase = load(QBK);
        if (pushTracked) {
          qBase = {};
          body.split('&').forEach(function (kv) { if (kv.indexOf('quests%5B%5D=') === 0) { qBase[decodeURIComponent(kv.slice(13))] = 1; } });
        }
        quests = load(QK);
        var qMerged = merge3(st.quests || [], quests, qBase);
        var nqb = {};
        (st.quests || []).forEach(function (s) { nqb[s] = 1; });
        save(QBK, nqb);
        if (!sameSet(qMerged, quests)) { quests = qMerged; changed = true; }
        var oBase = load(OBK);
        if (pushTracked) {
          oBase = {};
          body.split('&').forEach(function (kv) { if (kv.indexOf('objectives%5B%5D=') === 0) { oBase[decodeURIComponent(kv.slice(17))] = 1; } });
        }
        objs = load(OK);
        var sObjs = (st.objectives || []).map(String);
        var oMerged = merge3(sObjs, objs, oBase);
        var nob = {};
        sObjs.forEach(function (i) { nob[i] = 1; });
        save(OBK, nob);
        if (!sameSet(oMerged, objs)) { objs = oMerged; changed = true; }
        // Suivi : fusion à trois voies contre l'état ACTUEL du navigateur (un clic pendant la requête est gardé
        // comme changement local, et repartira au prochain push), puis base = ensemble serveur reçu.
        var tracked = load(TK), base = load(BK);
        if (pushTracked) {   // au push, le serveur a déjà appliqué nos changements : base = ce qu'on a envoyé
          base = {};
          body.split('&').forEach(function (kv) { if (kv.indexOf('tracked%5B%5D=') === 0) { base[decodeURIComponent(kv.slice(14))] = 1; } });
        }
        var merged = merge3(st.tracked || [], tracked, base);
        var nb = {};
        (st.tracked || []).forEach(function (s) { nb[s] = 1; });
        save(BK, nb);
        if (!sameSet(merged, tracked)) { tracked = merged; changed = true; }
        if (st.colors) {   // couleurs du compte (les mêmes que dans l'appli overlay)
          var oldC = JSON.stringify(load(CK)), newC = JSON.stringify(st.colors);
          if (oldC !== newC) { save(CK, st.colors); changed = true; }
        }
        if (changed) { save(QK, quests); save(OK, objs); save(TK, tracked); window.dispatchEvent(new Event('hunger-progress-synced')); }
      }).catch(function () {});
  }

  // Chargement : PULL (fusion serveur→local) puis PUSH (persiste l'union + les suivis hors-ligne).
  syncNow(false).then(function () { syncNow(true); });

  // À chaque écriture locale (coche, suivi…) → push-remplacement différé.
  var t = null;
  window.addEventListener('hunger-progress-changed', function () {
    clearTimeout(t);
    t = setTimeout(function () { t = null; syncNow(true); }, 700);
  });

  // Page quittée AVANT la fin du délai (clic « Suivre » puis navigation) : sans ça le push était perdu jusqu'au
  // prochain chargement de page connecté → l'overlay / un autre appareil ne voyait pas le suivi. sendBeacon
  // survit au déchargement de la page (cookies de session inclus, même origine).
  function flush() {
    if (t === null || !navigator.sendBeacon) { return; }
    clearTimeout(t); t = null;
    navigator.sendBeacon('/progress/sync', new Blob([buildBody(true)], { type: 'application/x-www-form-urlencoded' }));
  }
  window.addEventListener('pagehide', flush);
  // Onglet revenu au premier plan : PULL (le suivi a pu changer depuis l'appli overlay ou un autre appareil).
  var lastPull = Date.now();
  function pullIfStale() {
    if (document.visibilityState !== 'visible' || t !== null || Date.now() - lastPull < 5000) { return; }
    lastPull = Date.now();
    syncNow(false);
  }
  document.addEventListener('visibilitychange', pullIfStale);
  window.addEventListener('focus', pullIfStale);
  // Carnet ouvert sur un 2e écran pendant la partie (pas de changement de focus) : sondage léger toutes les 20 s.
  if (document.getElementById('tracker-body')) {
    setInterval(function () { lastPull = 0; pullIfStale(); }, 20000);
  }
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') { flush(); } });
})();
