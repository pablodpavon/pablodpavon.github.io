/* Shared helpers: i18n, number formats, theme-aware chart setup and small UI components. */
(function () {
  'use strict';
  const PP = (window.PP = {});

  /* ---------------- i18n ---------------- */
  const T = {
    es: {
      'common.showTable': 'Ver los datos en tabla', 'common.hideTable': 'Ocultar tabla', 'common.howBuilt': 'Cómo se generan estos datos',
      'common.code': 'Ver el código en GitHub', 'common.reset': 'Limpiar filtros', 'common.all': 'Todas', 'common.none': 'Ninguna',
      'common.synthetic': 'Datos sintéticos de una tienda ficticia.', 'common.noData': 'No hay datos para esta combinación de filtros.',
      'common.vsPrev': 'vs mismo período del año anterior', 'common.period': 'Período', 'common.page': 'Página',
      'sales.trend': 'Facturación mensual por canal', 'sales.trendSub': 'Pesos del período o pesos constantes del último mes',
      'sales.region': 'Facturación por región', 'sales.clickToFilter': 'Clic en una barra para filtrar',
      'sales.cat': 'Crecimiento interanual real por categoría', 'sales.catSub': 'Últimos 12 meses del período contra los 12 anteriores, en pesos constantes',
      'sales.mix': 'Participación de cada canal', 'sales.mixSub': '% de la facturación de cada mes',
      'sales.rev': 'Facturación', 'sales.realGrowth': 'Crecimiento real interanual', 'sales.units': 'Unidades', 'sales.margin': 'Margen bruto',
      'sales.nominal': 'Nominal', 'sales.real': 'Real', 'sales.regions': 'Regiones', 'sales.channels': 'Canales', 'sales.categories': 'Categorías',
      'sales.p12': 'Últimos 12 meses', 'sales.p2025': '2025', 'sales.p2024': '2024', 'sales.pAll': 'Todo',
      'sales.month': 'Mes', 'sales.realNote': 'en pesos de sep-2026', 'sales.vsLY': 'vs año anterior',
      'ap.month': 'Facturas por mes y estado', 'ap.monthSub': 'Monto en ARS según fecha de factura',
      'ap.rules': 'Excepciones por regla', 'ap.rulesSub': 'Clic en una barra para filtrar la tabla',
      'ap.invoices': 'Facturas', 'ap.amount': 'Monto total', 'ap.blocked': 'Bloqueado', 'ap.review': 'A revisar',
      'ap.ready_to_pay': 'Lista para pagar', 'ap.review_s': 'A revisar', 'ap.blocked_s': 'Bloqueada', 'ap.rule': 'Regla',
      'ap.search': 'Buscar proveedor o CUIT', 'ap.status': 'Estado', 'ap.supplier': 'Proveedor', 'ap.date': 'Fecha', 'ap.rulesCol': 'Reglas',
      'ap.ofAmount': 'del monto', 'ap.showing': 'Mostrando', 'ap.of': 'de', 'ap.prev': 'Anterior', 'ap.next': 'Siguiente', 'ap.allRules': 'Todas las reglas',
      'ret.heat': 'Retención por cohorte', 'ret.heatSub': '% de clientes de cada cohorte que compró en cada mes posterior a su primera compra',
      'ret.curve': 'Curva de retención por canal', 'ret.curveSub': 'Promedio ponderado de las cohortes filtradas',
      'ret.rfm': 'Segmentos RFM: clientes y facturación', 'ret.rfmSub': '% del total en cada segmento',
      'ret.customers': 'Clientes nuevos', 'ret.m1': 'Retención al mes 1', 'ret.m3': 'Retención al mes 3', 'ret.m6': 'Retención al mes 6',
      'ret.channels': 'Canales', 'ret.cohorts': 'Cohortes', 'ret.monthN': 'Mes', 'ret.cohort': 'Cohorte',
      'ret.share_c': '% de clientes', 'ret.share_r': '% de la facturación', 'ret.c2025': '2025', 'ret.c2026': '2026', 'ret.cAll': 'Todas',
      'ret.weighted': 'promedio ponderado'
    },
    en: {
      'common.showTable': 'Show data as a table', 'common.hideTable': 'Hide table', 'common.howBuilt': 'How this data is generated',
      'common.code': 'See the code on GitHub', 'common.reset': 'Clear filters', 'common.all': 'All', 'common.none': 'None',
      'common.synthetic': 'Synthetic data from a fictional store.', 'common.noData': 'No data for this filter combination.',
      'common.vsPrev': 'vs same period last year', 'common.period': 'Period', 'common.page': 'Page',
      'sales.trend': 'Monthly revenue by channel', 'sales.trendSub': 'Pesos of each month, or constant pesos of the last month',
      'sales.region': 'Revenue by region', 'sales.clickToFilter': 'Click a bar to filter',
      'sales.cat': 'Real year-on-year growth by category', 'sales.catSub': 'Last 12 months of the period vs the previous 12, in constant pesos',
      'sales.mix': 'Channel share', 'sales.mixSub': '% of each month’s revenue',
      'sales.rev': 'Revenue', 'sales.realGrowth': 'Real growth, year on year', 'sales.units': 'Units', 'sales.margin': 'Gross margin',
      'sales.nominal': 'Nominal', 'sales.real': 'Real', 'sales.regions': 'Regions', 'sales.channels': 'Channels', 'sales.categories': 'Categories',
      'sales.p12': 'Last 12 months', 'sales.p2025': '2025', 'sales.p2024': '2024', 'sales.pAll': 'All',
      'sales.month': 'Month', 'sales.realNote': 'in Sep-2026 pesos', 'sales.vsLY': 'vs last year',
      'ap.month': 'Invoices by month and status', 'ap.monthSub': 'Amount in ARS by invoice date',
      'ap.rules': 'Exceptions by rule', 'ap.rulesSub': 'Click a bar to filter the table',
      'ap.invoices': 'Invoices', 'ap.amount': 'Total amount', 'ap.blocked': 'Blocked', 'ap.review': 'Needs review',
      'ap.ready_to_pay': 'Ready to pay', 'ap.review_s': 'Needs review', 'ap.blocked_s': 'Blocked', 'ap.rule': 'Rule',
      'ap.search': 'Search supplier or CUIT', 'ap.status': 'Status', 'ap.supplier': 'Supplier', 'ap.date': 'Date', 'ap.rulesCol': 'Rules',
      'ap.ofAmount': 'of the amount', 'ap.showing': 'Showing', 'ap.of': 'of', 'ap.prev': 'Previous', 'ap.next': 'Next', 'ap.allRules': 'All rules',
      'ret.heat': 'Retention by cohort', 'ret.heatSub': '% of each cohort that bought in each month after their first purchase',
      'ret.curve': 'Retention curve by channel', 'ret.curveSub': 'Weighted average of the filtered cohorts',
      'ret.rfm': 'RFM segments: customers and revenue', 'ret.rfmSub': '% of the total in each segment',
      'ret.customers': 'New customers', 'ret.m1': 'Month-1 retention', 'ret.m3': 'Month-3 retention', 'ret.m6': 'Month-6 retention',
      'ret.channels': 'Channels', 'ret.cohorts': 'Cohorts', 'ret.monthN': 'Month', 'ret.cohort': 'Cohort',
      'ret.share_c': '% of customers', 'ret.share_r': '% of revenue', 'ret.c2025': '2025', 'ret.c2026': '2026', 'ret.cAll': 'All',
      'ret.weighted': 'weighted average'
    }
  };
  const NAMES = { // dimension values shown in English
    en: { 'Tiendas': 'Stores', 'Mayorista': 'Wholesale', 'Hogar': 'Home', 'Indumentaria': 'Apparel', 'Alimentos': 'Food', 'Juguetería': 'Toys', 'Orgánico': 'Organic', 'Búsqueda paga': 'Paid search', 'Referidos': 'Referral',
          'Campeones': 'Champions', 'Leales': 'Loyal', 'Prometedores': 'Promising', 'En riesgo': 'At risk', 'Dormidos': 'Dormant', '(no está en el maestro)': '(not in supplier master)' }
  };
  PP.lang = () => document.documentElement.lang === 'en' ? 'en' : 'es';
  PP.t = (k) => (T[PP.lang()][k] ?? T.es[k] ?? k);
  PP.name = (v) => (PP.lang() === 'en' && NAMES.en[v]) || v;
  PP.applyText = (root = document) => root.querySelectorAll('[data-t]').forEach(el => { el.textContent = PP.t(el.dataset.t); });

  /* ---------------- numbers ---------------- */
  const loc = () => PP.lang() === 'es' ? 'es-AR' : 'en-US';
  PP.num = (v, d = 0) => (v ?? 0).toLocaleString(loc(), { minimumFractionDigits: d, maximumFractionDigits: d });
  PP.pct = (v, d = 1) => PP.num(v * 100, d) + ' %';
  PP.ars = (v) => {
    const a = Math.abs(v);
    if (a >= 1e9) return PP.lang() === 'es' ? 'ARS ' + PP.num(v / 1e6, 0) + ' M' : 'ARS ' + PP.num(v / 1e9, 2) + 'B';
    if (a >= 1e6) return 'ARS ' + PP.num(v / 1e6, 1) + ' M';
    if (a >= 1e3) return 'ARS ' + PP.num(v / 1e3, 1) + (PP.lang() === 'es' ? ' mil' : 'k');
    return 'ARS ' + PP.num(v, 0);
  };
  PP.arsFull = (v) => 'ARS ' + PP.num(v, 2);
  PP.monthLabel = (ym) => {
    const [y, m] = ym.split('-').map(Number);
    return new Date(y, m - 1, 1).toLocaleDateString(loc(), { month: 'short', year: '2-digit' }).replace('.', '');
  };

  /* ---------------- theme tokens ---------------- */
  const css = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  PP.tok = () => ({
    ink: css('--ink'), ink2: css('--ink-2'), muted: css('--muted'), grid: css('--grid'), axis: css('--axis'), surface: css('--surface'), line: css('--line'),
    s: [css('--s1'), css('--s2'), css('--s3'), css('--s4'), css('--s5'), css('--s6')],
    seq: [css('--seq-1'), css('--seq-2'), css('--seq-3'), css('--seq-4'), css('--seq-5')],
    neg: css('--div-neg'), pos: css('--div-pos'), mid: css('--mid'),
    good: css('--good'), warn: css('--warn'), crit: css('--crit')
  });

  /* Base options every chart shares: recessive axes, thin grid, styled tooltip */
  PP.base = (tk) => ({
    animationDuration: 350, animationDurationUpdate: 300,
    textStyle: { fontFamily: 'Archivo, system-ui, sans-serif', color: tk.ink2 },
    grid: { left: 8, right: 24, top: 16, bottom: 8, containLabel: true },
    tooltip: {
      backgroundColor: tk.surface, borderColor: tk.line, borderWidth: 1, padding: [8, 12],
      textStyle: { color: tk.ink, fontSize: 12.5 }, extraCssText: 'box-shadow:0 8px 24px -10px rgba(0,0,0,.35);border-radius:10px;'
    }
  });
  PP.axisCat = (tk, extra = {}) => Object.assign({ type: 'category', axisLine: { lineStyle: { color: tk.axis } }, axisTick: { show: false }, axisLabel: { color: tk.muted, fontSize: 11.5 } }, extra);
  PP.axisVal = (tk, extra = {}) => Object.assign({ type: 'value', splitLine: { lineStyle: { color: tk.grid } }, axisLabel: { color: tk.muted, fontSize: 11.5 } }, extra);

  /* tooltip rows: value first (strong), name second, keyed with a short stroke */
  PP.ttRow = (color, value, name) => `<div style="display:flex;align-items:center;gap:8px;margin:2px 0"><span style="width:12px;height:3px;border-radius:2px;background:${color}"></span><b style="min-width:84px;display:inline-block">${value}</b><span style="opacity:.75">${PP.esc(name)}</span></div>`;
  PP.esc = (s) => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  /* chart registry: init lazily, resize, dispose on theme change */
  const charts = new Map();
  PP.chart = (id) => {
    let c = charts.get(id);
    if (!c || c.isDisposed()) { c = echarts.init(document.getElementById(id), null, { renderer: 'svg' }); charts.set(id, c); }
    return c;
  };
  /* whole-row hit target for horizontal bar charts: click anywhere on the row, not only on the painted bar */
  PP.rowClick = (chart, cb) => {
    chart.__rowCb = cb;
    if (chart.__rowBound) return;
    chart.__rowBound = true;
    const zr = chart.getZr();
    const idx = (e) => {
      const v = chart.convertFromPixel({ gridIndex: 0 }, [e.offsetX, e.offsetY]);
      const n = ((chart.getOption().yAxis || [{}])[0].data || []).length;
      const i = v ? Math.round(v[1]) : NaN;
      return Number.isFinite(i) && i >= 0 && i < n && chart.containPixel({ gridIndex: 0 }, [chart.getWidth() / 2, e.offsetY]) ? i : null;
    };
    zr.on('click', e => { const i = idx(e); if (i != null) chart.__rowCb(i); });
    zr.on('mousemove', e => { zr.setCursorStyle(idx(e) != null ? 'pointer' : 'default'); });
  };
  PP.resizeAll = () => charts.forEach(c => !c.isDisposed() && c.resize());
  PP.disposeAll = () => { charts.forEach(c => c.dispose()); charts.clear(); };
  window.addEventListener('resize', () => { clearTimeout(PP._rt); PP._rt = setTimeout(PP.resizeAll, 120); });

  /* legend (HTML, mirrors marks) */
  PP.legend = (el, items, kind = 'line') => {
    el.innerHTML = '';
    items.forEach(([name, color]) => {
      const s = document.createElement('span'); const i = document.createElement('i');
      if (kind === 'box') i.className = 'box'; i.style.background = color;
      s.append(i, document.createTextNode(name)); el.append(s);
    });
  };

  /* ---------------- UI components ---------------- */
  const chevron = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg>';

  /* Multi-select dropdown. opts: {label(), values, selected:Set, color(v), onChange} */
  PP.MultiSelect = function (opts) {
    const wrap = document.createElement('div'); wrap.className = 'ms';
    const btn = document.createElement('button'); btn.type = 'button'; btn.setAttribute('aria-haspopup', 'true'); btn.setAttribute('aria-expanded', 'false');
    const pop = document.createElement('div'); pop.className = 'pop'; pop.hidden = true; pop.setAttribute('role', 'group');
    wrap.append(btn, pop);
    const self = { el: wrap, selected: new Set(opts.selected || opts.values) };
    const renderBtn = () => {
      const n = self.selected.size, all = n === opts.values.length;
      btn.innerHTML = '';
      btn.append(document.createTextNode(opts.label()));
      const c = document.createElement('span'); c.className = 'count'; c.textContent = all ? PP.t('common.all') : String(n);
      btn.append(c); btn.insertAdjacentHTML('beforeend', chevron);
    };
    const renderPop = () => {
      pop.innerHTML = '';
      opts.values.forEach(v => {
        const l = document.createElement('label'); const i = document.createElement('input'); i.type = 'checkbox'; i.checked = self.selected.has(v);
        i.addEventListener('change', () => { i.checked ? self.selected.add(v) : self.selected.delete(v); renderBtn(); opts.onChange(); });
        l.append(i);
        if (opts.color) { const sw = document.createElement('span'); sw.className = 'swatch'; sw.style.background = opts.color(v); l.append(sw); }
        l.append(document.createTextNode(opts.display ? opts.display(v) : PP.name(v))); pop.append(l);
      });
      const acts = document.createElement('div'); acts.className = 'acts';
      const a = document.createElement('button'); a.type = 'button'; a.textContent = PP.t('common.all');
      const n = document.createElement('button'); n.type = 'button'; n.textContent = PP.t('common.none');
      a.onclick = () => { opts.values.forEach(v => self.selected.add(v)); renderPop(); renderBtn(); opts.onChange(); };
      n.onclick = () => { self.selected.clear(); renderPop(); renderBtn(); opts.onChange(); };
      acts.append(a, n); pop.append(acts);
    };
    btn.addEventListener('click', (e) => { e.stopPropagation(); const open = pop.hidden; document.querySelectorAll('.ms .pop').forEach(p => { p.hidden = true; p.previousSibling.setAttribute('aria-expanded', 'false'); }); pop.hidden = !open; btn.setAttribute('aria-expanded', String(open)); });
    pop.addEventListener('click', e => e.stopPropagation());
    self.set = (vals) => { self.selected = new Set(vals); renderPop(); renderBtn(); };
    self.refresh = () => { renderPop(); renderBtn(); };
    self.refresh();
    return self;
  };
  document.addEventListener('click', () => document.querySelectorAll('.ms .pop').forEach(p => { p.hidden = true; p.previousSibling && p.previousSibling.setAttribute('aria-expanded', 'false'); }));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') document.querySelectorAll('.ms .pop').forEach(p => p.hidden = true); });

  /* Segmented control. opts: {items:[[value,labelKey]], value, onChange} */
  PP.Segmented = function (opts) {
    const el = document.createElement('div'); el.className = 'seg'; el.setAttribute('role', 'group');
    const self = { el, value: opts.value };
    const render = () => {
      el.innerHTML = '';
      opts.items.forEach(([v, k]) => {
        const b = document.createElement('button'); b.type = 'button'; b.textContent = PP.t(k); b.setAttribute('aria-pressed', String(v === self.value));
        b.onclick = () => { self.value = v; render(); opts.onChange(v); };
        el.append(b);
      });
    };
    self.refresh = render; self.set = (v) => { self.value = v; render(); };
    render(); return self;
  };

  PP.label = (key) => { const s = document.createElement('span'); s.className = 'label'; s.dataset.t = key; s.textContent = PP.t(key); return s; };
  PP.resetBtn = (fn) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'reset'; b.dataset.t = 'common.reset'; b.textContent = PP.t('common.reset'); b.onclick = fn; return b; };

  /* KPI tile with optional delta and sparkline */
  PP.kpi = (label, value, delta, spark, goodWhenUp = true) => {
    const d = document.createElement('div'); d.className = 'kpi';
    const l = document.createElement('div'); l.className = 'k-label'; l.textContent = label;
    const v = document.createElement('div'); v.className = 'k-value'; v.textContent = value;
    d.append(l, v);
    if (delta) {
      const k = document.createElement('div'); k.className = 'k-delta';
      if (delta.value != null && isFinite(delta.value)) {
        const up = delta.value >= 0; const good = up === goodWhenUp;
        const b = document.createElement('b'); b.className = good ? 'up' : 'down';
        b.textContent = (up ? '▲ ' : '▼ ') + delta.text;
        k.append(b, document.createTextNode(' ' + delta.note));
      } else k.textContent = delta.note;
      d.append(k);
    }
    if (spark && spark.length > 1) {
      const max = Math.max(...spark), min = Math.min(...spark), w = 200, h = 28, c = PP.tok().s[0];
      const pts = spark.map((y, i) => `${((i / (spark.length - 1)) * w).toFixed(1)},${(2 + (h - 4) - ((y - min) / ((max - min) || 1)) * (h - 4)).toFixed(1)}`).join(' ');
      d.insertAdjacentHTML('beforeend', `<svg class="spark" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" aria-hidden="true"><polygon points="0,${h} ${pts} ${w},${h}" fill="${c}" fill-opacity=".1"/><polyline points="${pts}" fill="none" stroke="${c}" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/></svg>`);
    }
    return d;
  };

  /* simple table */
  PP.table = (cols, rows) => {
    const t = document.createElement('table'); t.className = 'dtable';
    const thead = document.createElement('thead'); const hr = document.createElement('tr');
    cols.forEach(c => { const th = document.createElement('th'); th.textContent = c.label; if (c.num) th.className = 'num'; hr.append(th); });
    thead.append(hr); t.append(thead);
    const tb = document.createElement('tbody');
    rows.forEach(r => { const tr = document.createElement('tr'); cols.forEach((c, i) => { const td = document.createElement('td'); td.textContent = r[i]; if (c.num) td.className = 'num'; tr.append(td); }); tb.append(tr); });
    t.append(tb); return t;
  };

  PP.downloadCSV = (name, header, rows) => {
    const esc = v => { const t = String(v ?? ''); return /[",;\n]/.test(t) ? '"' + t.replace(/"/g, '""') + '"' : t; };
    const csv = '\ufeff' + [header, ...rows].map(r => r.map(esc).join(',')).join('\n');
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' })); a.download = name; a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  };
  PP.loadJSON = (url) => fetch(url).then(r => { if (!r.ok) throw new Error(url + ' ' + r.status); return r.json(); });
})();
