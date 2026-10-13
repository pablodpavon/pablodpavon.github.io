/* Retail sales dashboard: nominal vs real (inflation-adjusted) pesos. */
(function () {
  'use strict';
  const PP = window.PP;
  let D, st, ui = {};
  const CH_COLOR = (tk) => ({ 'Tiendas': tk.s[0], 'E-commerce': tk.s[1], 'Marketplace': tk.s[2], 'Mayorista': tk.s[3] });

  function periodIdx(p) {
    const n = D.months.length;
    if (p === 'p12') return [n - 12, n - 1];
    if (p === 'p2025') return [D.months.indexOf('2025-01'), D.months.indexOf('2025-12')];
    if (p === 'p2024') return [0, D.months.indexOf('2024-12')];
    return [0, n - 1];
  }
  const val = (r) => st.mode === 'real' ? r[4] / D.cpi[r[0]] : r[4];
  const passDims = (r, skip) => (skip === 'region' || st.region.has(r[1])) && (skip === 'channel' || st.channel.has(r[2])) && (skip === 'category' || st.category.has(r[3]));

  function sumBy(rows, keyFn, valFn) { const m = new Map(); rows.forEach(r => { const k = keyFn(r); m.set(k, (m.get(k) || 0) + valFn(r)); }); return m; }

  function buildFilters() {
    const f = document.getElementById('f-sales'); f.innerHTML = '';
    ui.period = PP.Segmented({ items: [['p12', 'sales.p12'], ['p2025', 'sales.p2025'], ['p2024', 'sales.p2024'], ['all', 'sales.pAll']], value: st.period, onChange: v => { st.period = v; render(); } });
    ui.mode = PP.Segmented({ items: [['nominal', 'sales.nominal'], ['real', 'sales.real']], value: st.mode, onChange: v => { st.mode = v; render(); } });
    const tk = PP.tok(), cc = CH_COLOR(tk);
    ui.region = PP.MultiSelect({ label: () => PP.t('sales.regions'), values: D.dims.region, selected: st.region, onChange: () => { st.region = ui.region.selected; render(); } });
    ui.channel = PP.MultiSelect({ label: () => PP.t('sales.channels'), values: D.dims.channel, selected: st.channel, color: v => CH_COLOR(PP.tok())[v], onChange: () => { st.channel = ui.channel.selected; render(); } });
    ui.category = PP.MultiSelect({ label: () => PP.t('sales.categories'), values: D.dims.category, selected: st.category, onChange: () => { st.category = ui.category.selected; render(); } });
    const sp = document.createElement('span'); sp.className = 'spacer';
    f.append(ui.period.el, ui.region.el, ui.channel.el, ui.category.el, sp, ui.mode.el, PP.resetBtn(reset));
  }
  function reset() {
    st = defaults(); buildFilters(); render();
  }
  const defaults = () => ({ period: 'p12', mode: 'real', region: new Set(D.dims.region), channel: new Set(D.dims.channel), category: new Set(D.dims.category) });

  function render() {
    const tk = PP.tok(), cc = CH_COLOR(tk);
    const [a, b] = periodIdx(st.period);
    const rowsDim = D.rows.filter(r => passDims(r));
    const inP = rowsDim.filter(r => r[0] >= a && r[0] <= b);
    const inLY = a - 12 >= 0 ? rowsDim.filter(r => r[0] >= a - 12 && r[0] <= b - 12) : null;
    const months = D.months.slice(a, b + 1);

    /* KPIs */
    const k = document.getElementById('k-sales'); k.innerHTML = '';
    const tot = inP.reduce((s, r) => s + val(r), 0);
    const real = inP.reduce((s, r) => s + r[4] / D.cpi[r[0]], 0);
    const units = inP.reduce((s, r) => s + r[5], 0);
    const gm = inP.reduce((s, r) => s + r[6], 0), rev = inP.reduce((s, r) => s + r[4], 0);
    const perMonth = (rows, fn) => { const m = sumBy(rows, r => r[0], fn); return months.map((_, i) => m.get(a + i) || 0); };
    let dRev = null, dReal = null, dUnits = null, dGm = null;
    if (inLY && inLY.length) {
      const totLY = inLY.reduce((s, r) => s + val(r), 0), realLY = inLY.reduce((s, r) => s + r[4] / D.cpi[r[0]], 0);
      const unitsLY = inLY.reduce((s, r) => s + r[5], 0), gmLY = inLY.reduce((s, r) => s + r[6], 0) / inLY.reduce((s, r) => s + r[4], 0);
      dRev = tot / totLY - 1; dReal = real / realLY - 1; dUnits = units / unitsLY - 1; dGm = gm / rev - gmLY;
    }
    const note = PP.t('sales.vsLY');
    const na = { note: PP.lang() === 'es' ? 'sin datos del año anterior' : 'no prior-year data' };
    k.append(
      PP.kpi(PP.t('sales.rev') + (st.mode === 'real' ? ' (' + PP.t('sales.real').toLowerCase() + ')' : ''), PP.ars(tot), dRev == null ? na : { value: dRev, text: PP.pct(Math.abs(dRev)), note }, perMonth(inP, val)),
      PP.kpi(PP.t('sales.realGrowth'), dReal == null ? '—' : (dReal >= 0 ? '+' : '−') + PP.pct(Math.abs(dReal)), { note: PP.lang() === 'es' ? 'facturación en pesos constantes' : 'revenue in constant pesos' }),
      PP.kpi(PP.t('sales.units'), PP.num(units), dUnits == null ? na : { value: dUnits, text: PP.pct(Math.abs(dUnits)), note }, perMonth(inP, r => r[5])),
      PP.kpi(PP.t('sales.margin'), rev ? PP.pct(gm / rev) : '—', dGm == null ? na : { value: dGm, text: PP.num(Math.abs(dGm * 100), 1) + ' pp', note })
    );

    const empty = !inP.length;
    /* Trend by channel */
    const trend = PP.chart('c-sales-trend');
    const chs = D.dims.channel.filter(c => st.channel.has(c));
    PP.legend(document.getElementById('lg-sales-trend'), chs.map(c => [PP.name(c), cc[c]]));
    const series = chs.map(c => {
      const m = sumBy(inP.filter(r => r[2] === c), r => r[0], val);
      return { name: PP.name(c), type: 'line', smooth: false, showSymbol: false, symbolSize: 8, lineStyle: { width: 2, color: cc[c] }, itemStyle: { color: cc[c] },
        emphasis: { focus: 'series' }, data: months.map((_, i) => Math.round(m.get(a + i) || 0)) };
    });
    trend.setOption(Object.assign(PP.base(tk), {
      tooltip: Object.assign(PP.base(tk).tooltip, { trigger: 'axis', axisPointer: { type: 'line', lineStyle: { color: tk.axis } },
        formatter: (ps) => `<div style="margin-bottom:4px;opacity:.7">${PP.monthLabel(months[ps[0].dataIndex])}${st.mode === 'real' ? ' · ' + PP.t('sales.realNote') : ''}</div>` + ps.map(p => PP.ttRow(p.color, PP.ars(p.value), p.seriesName)).join('') }),
      xAxis: PP.axisCat(tk, { data: months.map(PP.monthLabel), boundaryGap: false }),
      yAxis: PP.axisVal(tk, { axisLabel: { color: tk.muted, fontSize: 11.5, formatter: v => PP.ars(v).replace('ARS ', '') } }),
      series
    }), true);

    /* Region bars (cross-filter) */
    const reg = PP.chart('c-sales-region');
    const rowsNoReg = D.rows.filter(r => passDims(r, 'region') && r[0] >= a && r[0] <= b);
    const rm = sumBy(rowsNoReg, r => r[1], val);
    const regs = [...D.dims.region].sort((x, y) => (rm.get(x) || 0) - (rm.get(y) || 0));
    reg.setOption(Object.assign(PP.base(tk), {
      tooltip: Object.assign(PP.base(tk).tooltip, { trigger: 'item', formatter: p => PP.ttRow(p.color, PP.ars(p.value), p.name) }),
      grid: { left: 8, right: 64, top: 8, bottom: 8, containLabel: true },
      xAxis: PP.axisVal(tk, { show: false }),
      yAxis: PP.axisCat(tk, { data: regs, axisLabel: { color: tk.ink2, fontSize: 12 } }),
      series: [{ type: 'bar', barWidth: '58%', cursor: 'pointer',
        data: regs.map(r => ({ value: Math.round(rm.get(r) || 0), itemStyle: { color: st.region.has(r) ? tk.s[0] : tk.grid, borderRadius: [0, 4, 4, 0] } })),
        label: { show: true, position: 'right', color: tk.ink2, fontSize: 11.5, formatter: p => PP.ars(p.value).replace('ARS ', '') } }]
    }), true);
    reg.off('click'); reg.on('click', p => {
      const only = st.region.size === 1 && st.region.has(p.name);
      st.region = only ? new Set(D.dims.region) : new Set([p.name]); ui.region.set(st.region); render();
    });

    /* Category real YoY growth (diverging) */
    const cat = PP.chart('c-sales-cat');
    const e = b, okLY = e - 23 >= 0;
    if (!okLY) {
      cat.clear();
      cat.setOption({ graphic: { type: 'text', left: 'center', top: 'middle', style: { text: PP.lang() === 'es' ? 'Para 2024 no hay 12 meses previos con qué comparar.' : 'For 2024 there are no prior 12 months to compare.', fill: tk.ink2, fontSize: 13 } } });
    } else {
      const cur = sumBy(rowsDim.filter(r => r[0] > e - 12 && r[0] <= e), r => r[3], r => r[4] / D.cpi[r[0]]);
      const prv = sumBy(rowsDim.filter(r => r[0] > e - 24 && r[0] <= e - 12), r => r[3], r => r[4] / D.cpi[r[0]]);
      const cats = D.dims.category.filter(c => st.category.has(c)).map(c => [c, prv.get(c) ? cur.get(c) / prv.get(c) - 1 : 0]).sort((x, y) => x[1] - y[1]);
      cat.setOption(Object.assign(PP.base(tk), {
        tooltip: Object.assign(PP.base(tk).tooltip, { trigger: 'item', formatter: p => PP.ttRow(p.color, (p.value >= 0 ? '+' : '−') + PP.pct(Math.abs(p.value)), p.name) }),
        grid: { left: 8, right: 56, top: 8, bottom: 8, containLabel: true },
        xAxis: PP.axisVal(tk, { splitNumber: 4, axisLabel: { color: tk.muted, fontSize: 11.5, hideOverlap: true, formatter: v => PP.num(v * 100, 0) + '%' } }),
        yAxis: PP.axisCat(tk, { data: cats.map(c => PP.name(c[0])), axisLabel: { color: tk.ink2, fontSize: 12 } }),
        series: [{ type: 'bar', barWidth: '56%', data: cats.map(c => ({ value: c[1], itemStyle: { color: c[1] >= 0 ? tk.pos : tk.neg, borderRadius: c[1] >= 0 ? [0, 4, 4, 0] : [4, 0, 0, 4] } })),
          label: { show: true, position: 'right', color: tk.ink2, fontSize: 11.5, formatter: p => (p.value >= 0 ? '+' : '−') + PP.num(Math.abs(p.value) * 100, 1) + '%' },
          markLine: { silent: true, symbol: 'none', data: [{ xAxis: 0 }], lineStyle: { color: tk.axis, type: 'solid' }, label: { show: false } } }]
      }), true);
    }

    /* Channel mix (100 % stacked bars) */
    const mix = PP.chart('c-sales-mix');
    PP.legend(document.getElementById('lg-sales-mix'), chs.map(c => [PP.name(c), cc[c]]), 'box');
    const totM = sumBy(inP, r => r[0], val);
    mix.setOption(Object.assign(PP.base(tk), {
      tooltip: Object.assign(PP.base(tk).tooltip, { trigger: 'axis', axisPointer: { type: 'shadow', shadowStyle: { color: 'rgba(127,127,127,.08)' } },
        formatter: ps => `<div style="margin-bottom:4px;opacity:.7">${PP.monthLabel(months[ps[0].dataIndex])}</div>` + ps.slice().reverse().map(p => PP.ttRow(p.color, PP.pct(p.value), p.seriesName)).join('') }),
      xAxis: PP.axisCat(tk, { data: months.map(PP.monthLabel) }),
      yAxis: PP.axisVal(tk, { max: 1, axisLabel: { color: tk.muted, fontSize: 11.5, formatter: v => PP.num(v * 100, 0) + '%' } }),
      series: chs.map((c, i) => {
        const m = sumBy(inP.filter(r => r[2] === c), r => r[0], val);
        return { name: PP.name(c), type: 'bar', stack: 'mix', barWidth: '62%',
          itemStyle: { color: cc[c], borderColor: tk.surface, borderWidth: 1, borderRadius: i === chs.length - 1 ? [4, 4, 0, 0] : 0 },
          data: months.map((_, j) => (totM.get(a + j) ? (m.get(a + j) || 0) / totM.get(a + j) : 0)) };
      })
    }), true);

    /* Table */
    const tw = document.getElementById('t-sales');
    if (!tw.hidden) renderTable(inP);
    document.getElementById('panel-sales').classList.toggle('is-empty', empty);
  }

  function renderTable(inP) {
    const tw = document.getElementById('t-sales'); tw.innerHTML = '';
    const g = new Map();
    inP.forEach(r => { const k = r[1] + '|' + r[2]; const o = g.get(k) || { reg: r[1], ch: r[2], v: 0, u: 0, gm: 0, rev: 0 }; o.v += val(r); o.u += r[5]; o.gm += r[6]; o.rev += r[4]; g.set(k, o); });
    const rows = [...g.values()].sort((x, y) => y.v - x.v).map(o => [o.reg, PP.name(o.ch), PP.ars(o.v), PP.num(o.u), PP.pct(o.gm / o.rev)]);
    tw.append(PP.table([{ label: PP.lang() === 'es' ? 'Región' : 'Region' }, { label: PP.lang() === 'es' ? 'Canal' : 'Channel' }, { label: PP.t('sales.rev') + (st.mode === 'real' ? ' (' + PP.t('sales.real').toLowerCase() + ')' : ''), num: true }, { label: PP.t('sales.units'), num: true }, { label: PP.t('sales.margin'), num: true }], rows));
  }

  PP.sales = {
    async init() {
      D = await PP.loadJSON('assets/data/sales.json');
      st = defaults(); buildFilters(); render();
      const tb = document.querySelector('[data-table="sales"]');
      tb.textContent = PP.t('common.showTable');
      tb.onclick = () => { const tw = document.getElementById('t-sales'); tw.hidden = !tw.hidden; tb.setAttribute('aria-expanded', String(!tw.hidden)); tb.textContent = PP.t(tw.hidden ? 'common.showTable' : 'common.hideTable'); render(); };
    },
    rerender() { if (!D) return; buildFilters(); render(); const tb = document.querySelector('[data-table="sales"]'); tb.textContent = PP.t(document.getElementById('t-sales').hidden ? 'common.showTable' : 'common.hideTable'); }
  };
})();
