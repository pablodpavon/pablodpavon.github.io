/* Customer retention dashboard: cohorts, retention curves by channel and RFM segments. */
(function () {
  'use strict';
  const PP = window.PP;
  let D, st, ui = {};
  const CHS = ['Orgánico', 'Paid social', 'Búsqueda paga', 'Referidos'];
  const chColor = (tk) => ({ 'Orgánico': tk.s[0], 'Paid social': tk.s[1], 'Búsqueda paga': tk.s[2], 'Referidos': tk.s[3] });
  const defaults = () => ({ channel: new Set(CHS), range: 'all' });

  function cohortsIn() {
    return D.cohorts.filter(c => st.channel.has(c.channel) && (st.range === 'all' || c.cohort.startsWith(st.range)));
  }
  function retentionAt(list, k) {
    let a = 0, n = 0; list.forEach(c => { if (c.active.length > k) { a += c.active[k]; n += c.customers; } });
    return n ? a / n : null;
  }

  function buildFilters() {
    const f = document.getElementById('f-ret'); f.innerHTML = '';
    ui.range = PP.Segmented({ items: [['all', 'ret.cAll'], ['2025', 'ret.c2025'], ['2026', 'ret.c2026']], value: st.range, onChange: v => { st.range = v; render(); } });
    ui.ch = PP.MultiSelect({ label: () => PP.t('ret.channels'), values: CHS, selected: st.channel, color: v => chColor(PP.tok())[v], onChange: () => { st.channel = ui.ch.selected; render(); } });
    const sp = document.createElement('span'); sp.className = 'spacer';
    f.append(PP.label('ret.cohorts'), ui.range.el, ui.ch.el, sp, PP.resetBtn(() => { st = defaults(); buildFilters(); render(); }));
  }

  function render() {
    const tk = PP.tok(), cc = chColor(tk);
    const list = cohortsIn();
    const k = document.getElementById('k-ret'); k.innerHTML = '';
    const n = list.reduce((s, c) => s + c.customers, 0);
    const r1 = retentionAt(list, 1), r3 = retentionAt(list, 3), r6 = retentionAt(list, 6);
    const all = D.cohorts;
    const ref = (x, kk) => { const b = retentionAt(all, kk); if (x == null || b == null) return { note: '—' }; if (Math.abs(x - b) < 0.0005) return { note: PP.lang() === 'es' ? 'total de las cohortes' : 'all cohorts' }; return { value: x - b, text: PP.num(Math.abs(x - b) * 100, 1) + ' pp', note: PP.lang() === 'es' ? 'vs el total' : 'vs all cohorts' }; };
    const cohortsSorted = [...new Set(list.map(c => c.cohort))].sort();
    const spark = cohortsSorted.map(co => list.filter(c => c.cohort === co).reduce((s, c) => s + c.customers, 0));
    k.append(
      PP.kpi(PP.t('ret.customers'), PP.num(n), { note: PP.lang() === 'es' ? `${cohortsSorted.length} cohortes mensuales` : `${cohortsSorted.length} monthly cohorts` }, spark),
      PP.kpi(PP.t('ret.m1'), r1 == null ? '—' : PP.pct(r1), ref(r1, 1)),
      PP.kpi(PP.t('ret.m3'), r3 == null ? '—' : PP.pct(r3), ref(r3, 3)),
      PP.kpi(PP.t('ret.m6'), r6 == null ? '—' : PP.pct(r6), ref(r6, 6))
    );

    /* Heatmap */
    const hm = PP.chart('c-ret-heat');
    const maxK = Math.max(1, ...list.map(c => c.active.length - 1));
    const data = []; const dark = document.documentElement.getAttribute('data-theme') === 'dark' || (!document.documentElement.getAttribute('data-theme') && matchMedia('(prefers-color-scheme: dark)').matches);
    cohortsSorted.forEach((co, y) => {
      const cs = list.filter(c => c.cohort === co); const base = cs.reduce((s, c) => s + c.customers, 0);
      for (let kk = 1; kk <= maxK; kk++) {
        if (cs[0] && cs[0].active.length > kk) { const v = cs.reduce((s, c) => s + c.active[kk], 0) / base; const strong = v / 0.5 > 0.55; data.push({ value: [kk - 1, y, v], label: { color: dark ? (strong ? '#0b1a2b' : tk.ink) : (strong ? '#ffffff' : tk.ink) } }); }
      }
    });
    hm.setOption(Object.assign(PP.base(tk), {
      tooltip: Object.assign(PP.base(tk).tooltip, { trigger: 'item', formatter: p => `<div style="opacity:.7;margin-bottom:4px">${PP.t('ret.cohort')} ${PP.monthLabel(cohortsSorted[p.value[1]])} · ${PP.t('ret.monthN')} ${p.value[0] + 1}</div>` + PP.ttRow(p.color, PP.pct(p.value[2]), PP.lang() === 'es' ? 'compró de nuevo' : 'bought again') }),
      grid: { left: 8, right: 16, top: 8, bottom: 48, containLabel: true },
      xAxis: PP.axisCat(tk, { data: Array.from({ length: maxK }, (_, i) => String(i + 1)), name: PP.lang() === 'es' ? 'Meses desde la primera compra' : 'Months since first purchase', nameLocation: 'middle', nameGap: 26, nameTextStyle: { color: tk.muted, fontSize: 11.5 }, splitArea: { show: false } }),
      yAxis: PP.axisCat(tk, { data: cohortsSorted.map(PP.monthLabel), inverse: true, axisLabel: { color: tk.ink2, fontSize: 11.5 } }),
      visualMap: { min: 0, max: 0.5, calculable: false, orient: 'horizontal', right: 8, bottom: 0, itemWidth: 10, itemHeight: 120, text: ['50 %', '0 %'], textStyle: { color: tk.muted, fontSize: 11 }, inRange: { color: tk.seq } },
      series: [{ type: 'heatmap', data, itemStyle: { borderColor: tk.surface, borderWidth: 2, borderRadius: 3 },
        label: { show: window.innerWidth > 900, fontSize: 10, formatter: p => PP.num(p.value[2] * 100, 0) },
        emphasis: { itemStyle: { borderColor: tk.ink, borderWidth: 1 } } }]
    }), true);

    /* Retention curves by channel */
    const cv = PP.chart('c-ret-curve');
    const chs = CHS.filter(c => st.channel.has(c));
    PP.legend(document.getElementById('lg-ret-curve'), chs.map(c => [PP.name(c), cc[c]]));
    const ks = Array.from({ length: Math.min(12, maxK) }, (_, i) => i + 1);
    cv.setOption(Object.assign(PP.base(tk), {
      tooltip: Object.assign(PP.base(tk).tooltip, { trigger: 'axis', axisPointer: { type: 'line', lineStyle: { color: tk.axis } },
        formatter: ps => `<div style="opacity:.7;margin-bottom:4px">${PP.t('ret.monthN')} ${ks[ps[0].dataIndex]}</div>` + ps.filter(p => p.value != null).sort((a, b) => b.value - a.value).map(p => PP.ttRow(p.color, PP.pct(p.value), p.seriesName)).join('') }),
      xAxis: PP.axisCat(tk, { data: ks.map(String), boundaryGap: false, name: PP.lang() === 'es' ? 'Mes' : 'Month', nameLocation: 'middle', nameGap: 26, nameTextStyle: { color: tk.muted, fontSize: 11.5 } }),
      yAxis: PP.axisVal(tk, { min: 0, axisLabel: { color: tk.muted, fontSize: 11.5, formatter: v => PP.num(v * 100, 0) + '%' } }),
      grid: { left: 8, right: 16, top: 12, bottom: 28, containLabel: true },
      series: chs.map(c => ({ name: PP.name(c), type: 'line', showSymbol: false, symbolSize: 8, lineStyle: { width: 2, color: cc[c] }, itemStyle: { color: cc[c] },
        data: ks.map(kk => { const v = retentionAt(list.filter(x => x.channel === c), kk); return v == null ? null : +v.toFixed(4); }) }))
    }), true);

    /* RFM */
    const rf = PP.chart('c-ret-rfm');
    PP.legend(document.getElementById('lg-ret-rfm'), [[PP.t('ret.share_c'), tk.s[0]], [PP.t('ret.share_r'), tk.s[1]]], 'box');
    const segs = D.segments;
    rf.setOption(Object.assign(PP.base(tk), {
      tooltip: Object.assign(PP.base(tk).tooltip, { trigger: 'axis', axisPointer: { type: 'shadow', shadowStyle: { color: 'rgba(127,127,127,.08)' } },
        formatter: ps => `<div style="opacity:.7;margin-bottom:4px">${PP.esc(PP.name(segs[ps[0].dataIndex].seg))}</div>` + ps.map(p => PP.ttRow(p.color, PP.pct(p.value, 0), p.seriesName)).join('') }),
      xAxis: PP.axisCat(tk, { data: segs.map(s => PP.name(s.seg)), axisLabel: { color: tk.ink2, fontSize: 11.5, interval: 0 } }),
      yAxis: PP.axisVal(tk, { axisLabel: { color: tk.muted, fontSize: 11.5, formatter: v => PP.num(v * 100, 0) + '%' } }),
      series: [
        { name: PP.t('ret.share_c'), type: 'bar', barGap: '8%', barWidth: '30%', itemStyle: { color: tk.s[0], borderRadius: [4, 4, 0, 0] }, data: segs.map(s => s.customers),
          label: { show: true, position: 'top', color: tk.ink2, fontSize: 11, formatter: p => PP.num(p.value * 100, 0) + '%' } },
        { name: PP.t('ret.share_r'), type: 'bar', barWidth: '30%', itemStyle: { color: tk.s[1], borderRadius: [4, 4, 0, 0] }, data: segs.map(s => s.revenue),
          label: { show: true, position: 'top', color: tk.ink2, fontSize: 11, formatter: p => PP.num(p.value * 100, 0) + '%' } }
      ]
    }), true);
  }

  PP.ret = {
    async init() { D = await PP.loadJSON('assets/data/retention.json'); st = defaults(); buildFilters(); render(); },
    rerender() { if (!D) return; buildFilters(); render(); }
  };
})();
