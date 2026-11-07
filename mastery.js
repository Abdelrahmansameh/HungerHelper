// Planificateur Mastery — calqué sur l'écran Mastery du jeu : un arbre à la fois, 8 paliers (I–VIII),
// cases alignées à gauche par colonne (node_order), liens horizontaux entre voisins d'un palier et
// verticaux entre cases d'une même colonne. Compteur x/5 seulement pour les nœuds à rangs.
// Règles : un palier s'ouvre après N points dans le précédent ; prérequis nœud → nœud ; un seul
// talent de palier VIII. Piloté par window.HUNGER_MASTERY.
(function () {
  'use strict';
  var DATA = window.HUNGER_MASTERY || [];
  var I18N = window.HUNGER_MASTERY_I18N || {};
  var PREFS = window.HUNGER_MASTERY_PREFS || {};
  var LS_KEY = 'hunger_mastery', saveTimer = null;
  // Ordre d'encodage du build (#b=…) figé : les liens partagés et les builds sauvegardés restent valides
  // même si l'ordre d'affichage des arbres change. Un nouvel arbre s'ajoute toujours EN FIN (Arms au patch 48811) :
  // un ancien code à moins de groupes reste lisible (groupe absent = zéro point). Tout arbre livré qui ne serait
  // pas encore listé ici est encodé après, par ordre alphabétique, pour ne jamais perdre de points.
  var CODE_ORDER = ['cunning', 'martial', 'physiology', 'survival', 'arms'];
  var ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'];

  var board = document.getElementById('mastery-planner');
  var tabsEl = document.getElementById('mtree-tabs');
  if (!board || !tabsEl || !DATA.length) return;

  var coarse = window.matchMedia && window.matchMedia('(pointer: coarse)').matches;
  var active = 0, selected = null, byId = {};

  function esc(s) { var d = document.createElement('div'); d.textContent = s == null ? '' : s; return d.innerHTML; }
  function fmt(s, v) { return (s || '').replace(/%[ds]/, v); }

  DATA.forEach(function (tree) {
    tree.tiers.forEach(function (tier, ti) {
      tier.index = ti;
      tier.exclusive = ti === tree.tiers.length - 1;   // dernier palier (VIII) : « Only one Tier VIII Mastery can be unlocked. »
      tier.nodes.forEach(function (n) { n.rank = 0; n.tree = tree; n.tierRef = tier; byId[n.id] = n; });
    });
    tree.max = 0;
    tree.tiers.forEach(function (t) { t.nodes.forEach(function (n) { tree.max += n.max; }); });
  });

  function pointsInTier(t) { var s = 0; t.nodes.forEach(function (n) { s += n.rank; }); return s; }
  function treeSpent(tree) { var s = 0; tree.tiers.forEach(function (t) { s += pointsInTier(t); }); return s; }
  function totalSpent() { var s = 0; DATA.forEach(function (t) { s += treeSpent(t); }); return s; }
  function reqNode(n) { return n.reqId ? byId[n.reqId] : null; }
  function reqNeed(n) { var r = reqNode(n); return r ? Math.max(1, Math.min(r.max, n.reqPts || 1)) : 0; }
  function reqMet(n) { var r = reqNode(n); return !r || r.rank >= reqNeed(n); }
  function t8Taken(n) {
    if (!n.tierRef.exclusive) return false;
    return n.tierRef.nodes.some(function (o) { return o !== n && o.rank > 0; });
  }

  // Retire en cascade les rangs devenus illégaux (palier refermé, prérequis perdu).
  function recomputeLocks() {
    var changed = true, g = 0;
    while (changed && g++ < 40) {
      changed = false;
      DATA.forEach(function (tree) {
        tree.tiers.forEach(function (tier, i) {
          tier.unlocked = (i === 0) || (pointsInTier(tree.tiers[i - 1]) >= tier.required);
          tier.nodes.forEach(function (n) {
            if (n.rank && (!tier.unlocked || !reqMet(n))) { n.rank = 0; changed = true; }
          });
        });
      });
    }
  }

  function canAdd(n) { return n.tierRef.unlocked && n.rank < n.max && reqMet(n) && !t8Taken(n); }

  function buildTabs() {
    tabsEl.innerHTML = '';
    DATA.forEach(function (tree, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'ms-tree' + (i === active ? ' on' : '');
      b.style.setProperty('--tc', tree.color || '#9e9e9e');
      b.setAttribute('aria-pressed', i === active ? 'true' : 'false');
      b.innerHTML = '<i></i><span>' + esc(tree.name) + '</span><b data-tab="' + i + '">0</b><small>/' + tree.max + '</small>';
      b.addEventListener('click', function () { if (active !== i) { active = i; selected = null; renderTree(); } });
      tabsEl.appendChild(b);
    });
  }

  function renderTree() {
    var tree = DATA[active];
    board.style.setProperty('--tc', tree.color || '#9e9e9e');
    var html = '<div class="ms-grid">';
    tree.tiers.forEach(function (tier, ti) {
      var cols = {};
      tier.nodes.forEach(function (n) { cols[n.order] = n; });
      var prevCols = {};
      if (ti > 0) tree.tiers[ti - 1].nodes.forEach(function (n) { prevCols[n.order] = n; });
      var row = ti * 2 + 1;
      html += '<div class="ms-tl" style="grid-row:' + row + '"><b>' + (ROMAN[ti] || ti + 1) + '</b><span class="ms-req" data-tier="' + ti + '"></span></div>';
      tier.nodes.forEach(function (n) {
        n._left = cols[n.order - 1] || null;
        n._up = prevCols[n.order] || null;
        html += '<button type="button" class="ms-n' + (n.wip ? ' wip' : '') + (n._left ? ' hl' : '') + (n._up ? ' vl' : '')
          + '" data-id="' + esc(n.id) + '" style="grid-row:' + row + ';grid-column:' + (n.order + 2) + '" aria-label="' + esc(n.name) + '">'
          + '<span class="ms-ico">' + (n.icon ? '<img src="' + esc(n.icon) + '" alt="" loading="lazy">' : '') + '</span>'
          + (n.wip ? '<span class="ms-wip">WIP</span>' : '')
          + (n.max > 1 ? '<span class="ms-rk"><b>0</b>/' + n.max + '</span>' : '')
          + '</button>';
      });
      if (tier.exclusive) html += '<div class="ms-t8" style="grid-row:' + (row + 1) + '">' + esc(I18N.t8 || '') + '</div>';
    });
    html += '</div>';
    board.innerHTML = html;

    tree.tiers.forEach(function (tier) {
      tier.nodes.forEach(function (n) {
        var el = board.querySelector('.ms-n[data-id="' + CSS.escape(n.id) + '"]');
        n._el = el;
        if (!coarse) el.addEventListener('mouseenter', function () { if (!selected) showDetail(n); });
        el.addEventListener('click', function (e) {
          e.preventDefault();
          var was = selected === n;
          select(n);
          // Souris : clic = +1 rang, Maj+clic = −1. Tactile : 1er appui = sélection, appuis suivants = +1.
          if (!coarse || was) changeRank(n, e.shiftKey ? -1 : 1);
        });
        el.addEventListener('contextmenu', function (e) { e.preventDefault(); select(n); changeRank(n, -1); });
      });
    });
    buildTabs();
    render();
    showDetail(selected);
  }

  function select(n) { selected = n; render(); showDetail(n); }

  function changeRank(n, delta) {
    if (delta > 0) { if (!canAdd(n)) { flash(n); return; } n.rank++; }
    else { if (n.rank <= 0) return; n.rank--; }
    try { if (window.hcTrack) { window.hcTrack('mastery.rank', { id: String(n.id).slice(0, 60), d: delta > 0 ? 1 : -1 }); } } catch (e) {}
    recomputeLocks(); render(); showDetail(n); pushState();
  }

  function flash(n) {
    if (!n._el) return;
    n._el.classList.remove('deny'); void n._el.offsetWidth; n._el.classList.add('deny');
  }

  // Description : la série « 20% / 40% / … » est découpée, le rang courant est mis en valeur.
  function descHtml(n) {
    var d = esc(n.desc || '');
    var m = d.match(/-?\d[\d.,]*\s?%?(?:\s*\/\s*-?\d[\d.,]*\s?%?)+/);
    if (m) {
      var out = m[0].split(/\s*\/\s*/).map(function (p, i) {
        return '<span class="sv' + (n.rank === i + 1 ? ' on' : '') + '">' + p + '</span>';
      }).join('<i>/</i>');
      d = d.replace(m[0], '<span class="ser' + (n.rank ? ' has' : '') + '">' + out + '</span>');
    } else {
      d = d.replace(/-?\d[\d.,]*\s?%?/g, '<span class="sv on">$&</span>');
    }
    return d.replace(/\n/g, '<br>');
  }

  function showDetail(n) {
    var nm = document.getElementById('mtree-node-name'), ds = document.getElementById('mtree-node-desc'),
        mt = document.getElementById('mtree-node-meta'), tr = document.getElementById('mtree-node-tree'),
        act = document.getElementById('mtree-node-act'), box = document.getElementById('mtree-node');
    board.classList.toggle('pad', !!n);
    if (!n) {
      nm.textContent = I18N.pick || ''; ds.innerHTML = ''; mt.innerHTML = ''; tr.innerHTML = ''; act.hidden = true;
      box.classList.remove('has'); return;
    }
    box.classList.add('has');
    box.style.setProperty('--tc', n.tree.color || '#9e9e9e');
    tr.innerHTML = '<i></i>' + esc(n.tree.name) + ' · ' + esc(fmt(I18N.tier, ROMAN[n.tierRef.index]));
    nm.textContent = n.name;
    mt.textContent = n.max > 1 ? fmt(I18N.ranks, n.max) : (I18N.single || '');
    var html = '<p>' + descHtml(n) + '</p>';
    var r = reqNode(n);
    if (r) html += '<p class="ms-cond' + (reqMet(n) ? ' ok' : '') + '">' + hcIcon(reqMet(n) ? 'check' : 'lock') + esc(I18N.requires || 'Requires') + ' <b>' + esc(r.name) + '</b>' + (reqNeed(n) > 1 ? ' (' + reqNeed(n) + '/' + r.max + ')' : '') + '</p>';
    if (!n.tierRef.unlocked) {
      var have = pointsInTier(n.tree.tiers[n.tierRef.index - 1]);
      html += '<p class="ms-cond">' + hcIcon('lock') + esc(fmt(I18N.unlock, Math.max(0, n.tierRef.required - have))) + '</p>';
    }
    if (t8Taken(n)) html += '<p class="ms-cond">' + hcIcon('lock') + esc(I18N.t8taken || '') + '</p>';
    if (n.wip) html += '<p class="ms-cond wip">' + esc(I18N.wip || '') + '</p>';
    ds.innerHTML = html;
    act.hidden = false;
    document.getElementById('mnode-rank').textContent = n.rank + ' / ' + n.max;
    document.getElementById('mnode-plus').disabled = !canAdd(n);
    document.getElementById('mnode-minus').disabled = n.rank <= 0;
  }

  function render() {
    var tree = DATA[active];
    tree.tiers.forEach(function (tier, ti) {
      tier.nodes.forEach(function (n) {
        if (!n._el) return;
        var b = n._el.querySelector('.ms-rk b'); if (b) b.textContent = n.rank;
        n._el.classList.toggle('on', n.rank > 0);
        n._el.classList.toggle('max', n.rank >= n.max);
        n._el.classList.toggle('lock', !tier.unlocked || !reqMet(n) || t8Taken(n));
        n._el.classList.toggle('sel', selected === n);
        n._el.classList.toggle('hl-on', !!(n._left && n._left.rank > 0 && n.rank > 0));
        n._el.classList.toggle('vl-on', !!(n._up && n._up.rank > 0 && n.rank > 0));
      });
      var reqEl = board.querySelector('.ms-req[data-tier="' + ti + '"]');
      if (reqEl) {
        reqEl.innerHTML = (ti === 0 || tier.unlocked) ? ''
          : hcIcon('lock') + Math.max(0, tier.required - pointsInTier(tree.tiers[ti - 1]));
      }
    });
    DATA.forEach(function (tr, i) { var el = tabsEl.querySelector('[data-tab="' + i + '"]'); if (el) el.textContent = treeSpent(tr); });
    var spent = totalSpent();
    document.getElementById('mastery-spent').textContent = spent;
    var budget = parseInt(document.getElementById('mastery-budget').value, 10) || 0;
    var rem = document.getElementById('mastery-remaining');
    rem.textContent = budget - spent;
    rem.classList.toggle('over', spent > budget);
  }

  // ---- build : encodage stable, persistance compte / localStorage, lien partageable
  function ordered() {
    var known = CODE_ORDER.map(function (s) { return DATA.filter(function (t) { return t.slug === s; })[0]; }).filter(Boolean);
    var extra = DATA.filter(function (t) { return CODE_ORDER.indexOf(t.slug) < 0; }).sort(function (a, b) { return a.slug < b.slug ? -1 : a.slug > b.slug ? 1 : 0; });
    return known.concat(extra);
  }
  function buildCode() { return ordered().map(function (tree) { var s = ''; tree.tiers.forEach(function (t) { t.nodes.forEach(function (n) { if (n.max > 0) s += n.rank; }); }); return s; }).join('.'); }
  function loadCode(code) {
    var parts = (code || '').split('.');
    ordered().forEach(function (tree, ti) {
      var s = parts[ti] || '', k = 0;
      tree.tiers.forEach(function (t) { t.nodes.forEach(function (n) { if (n.max > 0) { var v = parseInt(s.charAt(k++) || '0', 10); n.rank = isNaN(v) ? 0 : Math.min(n.max, Math.max(0, v)); } }); });
    });
    // Un seul palier VIII par arbre : un ancien build qui en avait plusieurs garde le premier.
    DATA.forEach(function (tree) { tree.tiers.forEach(function (t) { if (!t.exclusive) return; var seen = false; t.nodes.forEach(function (n) { if (n.rank) { if (seen) n.rank = 0; seen = true; } }); }); });
    recomputeLocks();
  }
  function loadSavedState() {
    var raw = PREFS.saved || (!PREFS.csrf ? (function () { try { return localStorage.getItem(LS_KEY); } catch (e) { return null; } })() : null);
    if (!raw) return null;
    try { return JSON.parse(raw); } catch (e) { return null; }
  }
  function persist() {
    var be = document.getElementById('mastery-budget');
    var payload = JSON.stringify({ code: buildCode(), budget: parseInt(be && be.value, 10) || 0 });
    if (PREFS.csrf) {
      clearTimeout(saveTimer);
      saveTimer = setTimeout(function () {
        try {
          fetch('/preferences/mastery', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: 'value=' + encodeURIComponent(payload) + '&_csrf=' + encodeURIComponent(PREFS.csrf) });
        } catch (e) {}
      }, 700);
    } else {
      try { localStorage.setItem(LS_KEY, payload); } catch (e) {}
    }
  }
  function pushState() { try { history.replaceState(null, '', '#b=' + buildCode()); } catch (e) {} persist(); }

  // Vue large (défaut, remplit la largeur) ↔ compacte (tout en hauteur) — préférence du navigateur.
  var viewBtn = document.getElementById('mastery-view');
  function setView(compact) {
    board.classList.toggle('compact', compact);
    if (viewBtn) { viewBtn.setAttribute('aria-pressed', compact ? 'true' : 'false'); viewBtn.querySelector('span').textContent = viewBtn.getAttribute(compact ? 'data-on' : 'data-off'); }
  }
  try { setView(localStorage.getItem('hunger_mastery_view') === 'compact'); } catch (e) { setView(false); }
  if (viewBtn) viewBtn.addEventListener('click', function () {
    var c = !board.classList.contains('compact'); setView(c);
    try { localStorage.setItem('hunger_mastery_view', c ? 'compact' : 'large'); } catch (e) {}
  });
  document.getElementById('mnode-close').addEventListener('click', function () { selected = null; render(); showDetail(null); });
  document.getElementById('mnode-plus').addEventListener('click', function () { if (selected) changeRank(selected, 1); });
  document.getElementById('mnode-minus').addEventListener('click', function () { if (selected) changeRank(selected, -1); });
  document.getElementById('mastery-budget').addEventListener('input', function () { render(); persist(); });
  document.getElementById('mastery-reset').addEventListener('click', function () {
    try { if (window.hcTrack) { window.hcTrack('mastery.reset'); } } catch (e) {}
    DATA.forEach(function (tree) { tree.tiers.forEach(function (t) { t.nodes.forEach(function (n) { n.rank = 0; }); }); });
    recomputeLocks(); render(); showDetail(selected); pushState();
  });
  document.getElementById('mastery-share').addEventListener('click', function () {
    try { if (window.hcTrack) { window.hcTrack('mastery.share'); } } catch (e) {}
    var url = location.href.split('#')[0] + '#b=' + buildCode(), lab = this.querySelector('span');
    var done = function () { var t = lab.textContent; lab.textContent = I18N.copied || 'OK'; setTimeout(function () { lab.textContent = t; }, 1500); };
    if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(url).then(done, done); }
    else { window.prompt('URL', url); }
  });

  var m = (location.hash || '').match(/b=([0-9.]*)/);
  if (m) {
    loadCode(m[1]);
  } else {
    var sv = loadSavedState();
    if (sv) {
      if (sv.code) loadCode(sv.code); else recomputeLocks();
      if (sv.budget != null) document.getElementById('mastery-budget').value = sv.budget;
    } else {
      recomputeLocks();
    }
  }
  renderTree();
})();
