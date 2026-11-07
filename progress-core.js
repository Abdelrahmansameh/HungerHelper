// Store de progression partagé (localStorage), source de vérité unique pour
// quêtes/objectifs terminés. Utilisé par la fiche quête, la liste des quêtes
// et la page « À conserver ». Émet « hunger-progress-changed » à chaque écriture.
window.HungerProgress = (function () {
  'use strict';
  var QK = 'hunger_quest_done', OK = 'hunger_obj_done', TK = 'hunger_quest_tracked';
  function load(k) { try { return JSON.parse(localStorage.getItem(k)) || {}; } catch (e) { return {}; } }
  function save(k, o) { try { localStorage.setItem(k, JSON.stringify(o)); } catch (e) {} }
  var quests = load(QK), objs = load(OK), tracked = load(TK), reg = {};
  function emit() { window.dispatchEvent(new Event('hunger-progress-changed')); }
  // Statistiques anonymes (js/stats.js) : seulement les CHANGEMENTS d'état (jamais la progression complète).
  function track(n, d) { try { if (window.hcTrack) { window.hcTrack(n, d); } } catch (e) {} }

  var API = {
    // Enregistre les objectifs requis d'une quête (pour dériver son achèvement).
    registerQuest: function (slug, reqIds) { if (slug) { reg[slug] = (reqIds || []).map(String); } },
    objDone: function (id) { return !!objs[String(id)]; },
    setObjs: function (ids, on) {
      (ids || []).forEach(function (id) { id = String(id); if (!!objs[id] !== !!on) { track('quest.obj', { id: id, on: on ? 1 : 0 }); } if (on) { objs[id] = 1; } else { delete objs[id]; } });
      save(OK, objs);
    },
    questExplicit: function (slug) { return !!quests[slug]; },
    setQuest: function (slug, on) { if (!!quests[slug] !== !!on) { track('quest.done', { q: slug, on: on ? 1 : 0 }); } if (on) { quests[slug] = 1; } else { delete quests[slug]; } save(QK, quests); },
    // Terminée si marquée explicitement OU tous les objectifs requis (enregistrés) faits.
    questComplete: function (slug) {
      if (quests[slug]) { return true; }
      var req = reg[slug];
      return !!(req && req.length && req.every(function (id) { return objs[id]; }));
    },
    // --- Suivi « En cours » (liste active du joueur ; add/remove, distinct de « terminé ») ---
    isTracked: function (slug) { return !!tracked[slug]; },
    setTracked: function (slug, on) { if (!!tracked[slug] !== !!on) { track('quest.track', { q: slug, on: on ? 1 : 0 }); } if (on) { tracked[slug] = 1; } else { delete tracked[slug]; } save(TK, tracked); },
    trackedSlugs: function () { return Object.keys(tracked); },
    trackedCount: function () { return Object.keys(tracked).length; },
    // Fusionne l'ensemble suivi renvoyé par le serveur (au chargement, connecté).
    mergeTracked: function (slugs) { var ch = false; (slugs || []).forEach(function (s) { if (!tracked[s]) { tracked[s] = 1; ch = true; } }); if (ch) { save(TK, tracked); } return ch; },
    reload: function () { quests = load(QK); objs = load(OK); tracked = load(TK); },
    // Efface TOUTE la progression locale (quêtes + objectifs + suivi) et notifie.
    reset: function () { track('quest.reset', { q: Object.keys(quests).length, t: Object.keys(tracked).length }); quests = {}; objs = {}; tracked = {}; save(QK, quests); save(OK, objs); save(TK, tracked); emit(); },
    changed: function () { emit(); },
    // Instantané partageable (Hub) : quêtes terminées + objectifs faits + suivi.
    snapshot: function () { return { q: Object.assign({}, quests), o: Object.assign({}, objs), t: Object.assign({}, tracked) }; }
  };
  // Après resync BD (connecté), recharger et propager.
  window.addEventListener('hunger-progress-synced', function () { API.reload(); emit(); });
  return API;
})();
