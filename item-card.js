// Carte de survol des objets, partout sur le site : dès qu'une icône d'objet pointe vers sa fiche (/items/{slug}),
// le survol (ou le focus clavier) affiche l'essentiel. Données : /api/item-card/{slug}, chargées à la demande et
// gardées en mémoire. Un lien peut aussi fournir ses données en ligne (data-j) ; « Tous les objets » ne le fait plus (HTML trop lourd).
(function () {
  'use strict';
  var C = window.HC_CARD; if (!C) return;
  var card = document.createElement('div');
  card.className = 'hc-card'; card.hidden = true; card.setAttribute('role', 'tooltip');
  document.body.appendChild(card);
  var cache = {}, cur = null, timer = null;
  function esc(s) { var d = document.createElement('div'); d.textContent = s == null ? '' : String(s); return d.innerHTML; }
  function coins(v) {
    var g = Math.floor(v / 10000), s = Math.floor(v % 10000 / 100), c = v % 100, out = '';
    [['gold', g], ['silver', s], ['copper', c]].forEach(function (x) {
      if (x[1] > 0) out += '<span class="currency-amount">' + x[1] + '</span><img class="currency-icon currency-icon--' + x[0] + '" src="' + C.coin[x[0]] + '" alt="">';
    });
    return '<span class="currency-value">' + (out || '0') + '</span>';
  }
  function render(j) {
    var rows = '';
    ['d', 'f', 'm', 'a', 'h', 'e'].forEach(function (k) { if (j[k] != null) rows += '<dt>' + esc(C.lbl[k]) + '</dt><dd>' + esc(j[k]) + '</dd>'; });
    if (j.v != null) rows += '<dt>' + esc(C.lbl.v) + '</dt><dd>' + coins(j.v) + '</dd>';
    card.className = 'hc-card r-' + (j.r || 'common');
    card.innerHTML = '<span class="k">' + esc(C.rar[j.r] || j.r || '') + (j.c ? ' · ' + esc(C.cat[j.c] || j.c) : '') + (j.w || j.s ? ' · ' + esc(j.w || j.s) : '') + '</span>'
      + '<b>' + esc(j.t) + '</b>' + (rows ? '<dl>' + rows + '</dl>' : '') + '<span class="more">' + esc(C.lbl.more) + '</span>';
  }
  function place(x, y) {
    card.hidden = false;
    var w = card.offsetWidth, h = card.offsetHeight;
    card.style.left = Math.max(8, Math.min(x + 16, innerWidth - w - 8)) + 'px';
    card.style.top = Math.max(8, Math.min(y + 16, innerHeight - h - 8)) + 'px';
  }
  function hide() { card.hidden = true; cur = null; clearTimeout(timer); }
  function slugOf(a) {
    var m = (a.getAttribute('href') || '').match(/\/items\/([a-z0-9][a-z0-9-]*)\/?(?:[?#].*)?$/i);
    return m && C.cats.indexOf(m[1]) === -1 ? m[1] : null;   // /items/weapon = une catégorie, pas une fiche
  }
  function target(el) {
    var a = el.closest && el.closest('a[href*="/items/"]');
    if (!a || a.closest('.hc-card') || a.hasAttribute('data-nocard')) return null;
    if (!a.querySelector('img') && !a.closest('.v, .vr, .chip, .ia-t')) return null;   // une icône d'objet, pas un lien texte
    return a;
  }
  function load(a, cb) {
    if (a.hasAttribute('data-j')) { try { return cb(JSON.parse(a.getAttribute('data-j'))); } catch (e) { return; } }
    var slug = slugOf(a); if (!slug) return;
    if (cache[slug]) return cb(cache[slug]);
    fetch(C.api + encodeURIComponent(slug), { credentials: 'same-origin' }).then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) { if (j && !j.error) { cache[slug] = j; cb(j); } }).catch(function () {});
  }
  var seenCards = {};
  function show(a, x, y) {
    var key = (a.getAttribute('href') || '').replace(/^.*\/items\//, '').slice(0, 80);
    if (key && !seenCards[key]) { seenCards[key] = 1; try { if (window.hcTrack) { window.hcTrack('item.card', { i: key }); } } catch (e) {} }
    if (a.title) { a.setAttribute('data-title', a.title); a.removeAttribute('title'); }   // pas de double infobulle
    load(a, function (j) { if (cur !== a) return; render(j); place(x, y); });
  }
  window.HCCard = { render: render, place: place, hide: hide };
  var mx = 0, my = 0;
  if (window.matchMedia('(hover: hover)').matches) {
    document.addEventListener('mousemove', function (e) {
      mx = e.clientX; my = e.clientY;
      var a = target(e.target);
      if (!a) { if (cur) hide(); return; }
      if (a !== cur) { hide(); cur = a; timer = setTimeout(function () { show(a, mx, my); }, 120); }
      else if (!card.hidden) { place(mx, my); }
    }, { passive: true });
  }
  document.addEventListener('focusin', function (e) {
    var a = target(e.target); if (!a) return;
    cur = a; var b = a.getBoundingClientRect(); show(a, b.right, b.top);
  });
  document.addEventListener('focusout', hide);
  window.addEventListener('scroll', hide, { passive: true });
})();
