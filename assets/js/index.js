/* Home page: hero live chart, dashboard app (tabs, lazy init, export), gallery lightbox. */
(function () {
  'use strict';
  const PP = window.PP, S = window.SHELL;
  const DASH = { sales: PP.sales, ap: PP.ap, ret: PP.ret };
  const META = {
    sales: { es: 'Ventas retail', en: 'Retail sales', code: 'https://github.com/pablodpavon/pablodpavon.github.io/blob/main/tools/build_data.py' },
    ap: { es: 'Cuentas a pagar', en: 'Accounts payable', code: 'https://github.com/pablodpavon/ap-invoice-control' },
    ret: { es: 'Retención de clientes', en: 'Customer retention', code: 'https://github.com/pablodpavon/pablodpavon.github.io/blob/main/tools/build_data.py' }
  };
  const started = new Set();
  let current = 'sales';

  /* ---------- hero: live product window ---------- */
  let heroData = null;
  async function hero() {
    try { heroData = heroData || await PP.loadJSON('assets/data/sales.json'); } catch (e) { return; }
    const D = heroData, n = D.months.length, from = n - 18;
    const nom = new Array(n).fill(0), real = new Array(n).fill(0), units = new Array(n).fill(0);
    D.rows.forEach(r => { nom[r[0]] += r[4]; real[r[0]] += r[4] / D.cpi[r[0]]; units[r[0]] += r[5]; });
    const sum = (a, i, j) => a.slice(i, j).reduce((x, y) => x + y, 0);
    const realG = sum(real, n - 12, n) / sum(real, n - 24, n - 12) - 1, nomG = sum(nom, n - 12, n) / sum(nom, n - 24, n - 12) - 1;
    const set = (id, v) => { const e = document.getElementById(id); if (e) e.textContent = v; };
    set('hk1', PP.ars(sum(real, n - 12, n))); set('hk2', '+' + PP.pct(realG)); set('hk3', '+' + PP.pct(nomG));
    const tk = PP.tok(), c = PP.chart('hero-chart'), months = D.months.slice(from);
    c.setOption(Object.assign(PP.base(tk), {
      grid: { left: 6, right: 10, top: 14, bottom: 4, containLabel: true },
      tooltip: Object.assign(PP.base(tk).tooltip, { trigger: 'axis', axisPointer: { type: 'line', lineStyle: { color: tk.axis } },
        formatter: ps => `<div style="opacity:.7;margin-bottom:4px">${PP.monthLabel(months[ps[0].dataIndex])}</div>` + ps.map(p => PP.ttRow(p.color, PP.ars(p.value), p.seriesName)).join('') }),
      xAxis: PP.axisCat(tk, { data: months.map(PP.monthLabel), boundaryGap: false, axisLabel: { color: tk.muted, fontSize: 11, interval: 2 } }),
      yAxis: PP.axisVal(tk, { axisLabel: { color: tk.muted, fontSize: 11, formatter: v => PP.ars(v).replace('ARS ', '') } }),
      series: [
        { name: S.lang() === 'es' ? 'Real (pesos de sep-2026)' : 'Real (Sep-2026 pesos)', type: 'line', smooth: 0.3, showSymbol: false, lineStyle: { width: 2.5, color: tk.s[0] }, itemStyle: { color: tk.s[0] },
          areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: tk.s[0] + '33' }, { offset: 1, color: tk.s[0] + '00' }] } }, data: real.slice(from).map(Math.round) },
        { name: S.lang() === 'es' ? 'Nominal' : 'Nominal', type: 'line', smooth: 0.3, showSymbol: false, lineStyle: { width: 2, color: tk.s[1], type: [6, 4] }, itemStyle: { color: tk.s[1] }, data: nom.slice(from).map(Math.round) }
      ]
    }), true);
  }
  const stage = document.querySelector('.stage');
  if (stage) new IntersectionObserver((es, o) => es.forEach(e => { if (e.isIntersecting) { stage.classList.add('in'); o.disconnect(); } }), { threshold: .2 }).observe(stage);

  /* ---------- dashboard app ---------- */
  const tabs = [...document.querySelectorAll('.app [role=tab]')];
  async function openTab(name, focus) {
    current = name;
    tabs.forEach(t => {
      const on = t.dataset.tab === name;
      t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      if (on && focus) t.focus();
    });
    const crumb = document.getElementById('crumb'); if (crumb) crumb.textContent = META[name][S.lang()];
    const code = document.getElementById('codeLink'); if (code) code.href = META[name].code;
    if (!started.has(name)) {
      started.add(name);
      try { await DASH[name].init(); } catch (e) { console.error(e); document.getElementById('panel-' + name).insertAdjacentHTML('beforeend', '<p class="empty">No se pudieron cargar los datos.</p>'); }
    } else requestAnimationFrame(PP.resizeAll);
  }
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => openTab(t.dataset.tab));
    t.addEventListener('keydown', e => {
      if (['ArrowDown', 'ArrowRight', 'ArrowUp', 'ArrowLeft'].includes(e.key)) {
        e.preventDefault(); const d = (e.key === 'ArrowDown' || e.key === 'ArrowRight') ? 1 : tabs.length - 1;
        openTab(tabs[(i + d) % tabs.length].dataset.tab, true);
      }
    });
  });
  document.querySelectorAll('[data-open-tab]').forEach(a => a.addEventListener('click', () => openTab(a.dataset.openTab)));
  const exp = document.getElementById('exportBtn');
  exp && exp.addEventListener('click', () => { if (started.has(current) && DASH[current].csv) { DASH[current].csv(); S.toast(S.lang() === 'es' ? 'CSV descargado con los filtros actuales' : 'CSV downloaded with current filters'); } });

  /* language / theme hooks */
  S.onLang.push(() => { PP.applyText(); started.forEach(k => DASH[k].rerender()); const crumb = document.getElementById('crumb'); if (crumb) crumb.textContent = META[current][S.lang()]; hero(); });
  S.onTheme.push(() => { PP.disposeAll(); started.forEach(k => DASH[k].rerender()); hero(); });

  /* ---------- lightbox ---------- */
  const lb = document.getElementById('lightbox');
  if (lb) {
    const img = lb.querySelector('img'), cap = lb.querySelector('figcaption'); let last = null;
    const open = (src, text) => { last = document.activeElement; img.src = src; cap.textContent = text || ''; lb.hidden = false; lb.querySelector('.close').focus(); document.body.style.overflow = 'hidden'; };
    const close = () => { lb.hidden = true; img.src = ''; document.body.style.overflow = ''; last && last.focus(); };
    document.querySelectorAll('[data-zoom-src]').forEach(b => b.addEventListener('click', () => {
      const h = [...b.closest('.g-item').querySelectorAll('h3')].find(x => x.getAttribute('lang') === S.lang());
      open(b.dataset.zoomSrc, h ? h.textContent : '');
    }));
    lb.addEventListener('click', e => { if (e.target === lb || e.target.classList.contains('close')) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && !lb.hidden) close(); });
  }

  /* ---------- start ---------- */
  PP.applyText();
  hero();
  const lab = document.getElementById('lab');
  const hashTab = (location.hash.match(/^#lab-(sales|ap|ret)$/) || [])[1];
  if (hashTab) { openTab(hashTab); requestAnimationFrame(() => lab && lab.scrollIntoView()); }
  else if (lab) new IntersectionObserver((es, o) => es.forEach(e => { if (e.isIntersecting) { openTab(current); o.disconnect(); } }), { rootMargin: '400px 0px' }).observe(lab);
})();
