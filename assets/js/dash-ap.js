/* Accounts payable dashboard: output of github.com/pablodpavon/ap-invoice-control */
(function () {
  'use strict';
  const PP = window.PP;
  let D, st, ui = {}, page = 0, sort = { key: 'amount', dir: -1 };
  const PER = 12;
  const STATUSES = ['ready_to_pay', 'review', 'blocked'];
  const ICON = { ready_to_pay: ['good', '✓'], review: ['warn', '!'], blocked: ['crit', '✕'] };
  const RULE_ES = { R01: 'CUIT inválido', R02: 'Proveedor desconocido', R03: 'Duplicado exacto', R04: 'Posible duplicado', R05: 'Error de IVA',
    R06: 'Total no cierra', R07: 'Sin OC sobre umbral', R08: 'Precio sobre la OC', R09: 'Cantidad sobre lo recibido', R10: 'Tipo vs condición fiscal',
    R11: 'CAE faltante o vencido', R12: 'Fechas inconsistentes' };
  const ruleName = (r) => PP.lang() === 'es' ? RULE_ES[r.rule] : r.short;
  const statusLabel = (s) => PP.t(s === 'ready_to_pay' ? 'ap.ready_to_pay' : s === 'review' ? 'ap.review_s' : 'ap.blocked_s');
  const statusColor = (tk, s) => s === 'ready_to_pay' ? tk.good : s === 'review' ? tk.warn : tk.crit;
  const fmtCuit = (c) => c && c.length === 11 ? `${c.slice(0, 2)}-${c.slice(2, 10)}-${c.slice(10)}` : c;
  const ico = (s) => { const i = document.createElement('span'); i.className = 'ico ' + ICON[s][0]; i.textContent = ICON[s][1]; i.setAttribute('aria-hidden', 'true'); return i; };

  const defaults = () => ({ status: new Set(STATUSES), rules: new Set(D.rules.map(r => r.rule)), q: '' });
  const allRules = () => st.rules.size === D.rules.length;

  function filtered(skipRules) {
    const q = st.q.trim().toLowerCase();
    return D.rows.filter(r => st.status.has(r[5])
      && (!q || r[1].toLowerCase().includes(q) || r[2].includes(q.replace(/\D/g, '') || '§'))
      && (skipRules || allRules() || r[6].split(',').some(x => st.rules.has(x))));
  }

  function buildFilters() {
    const f = document.getElementById('f-ap'); f.innerHTML = '';
    f.append(PP.label('ap.status'));
    STATUSES.forEach(s => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'statuschip'; b.setAttribute('aria-pressed', String(st.status.has(s)));
      b.append(ico(s), document.createTextNode(statusLabel(s)));
      b.onclick = () => { st.status.has(s) ? st.status.delete(s) : st.status.add(s); b.setAttribute('aria-pressed', String(st.status.has(s))); page = 0; render(); };
      f.append(b);
    });
    ui.rules = PP.MultiSelect({ label: () => PP.t('ap.rule'), values: D.rules.map(r => r.rule), selected: st.rules,
      display: v => v + '  ' + ruleName(D.rules.find(r => r.rule === v)), onChange: () => { st.rules = ui.rules.selected; page = 0; render(); } });
    const s = document.createElement('label'); s.className = 'search';
    s.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>';
    const inp = document.createElement('input'); inp.type = 'search'; inp.placeholder = PP.t('ap.search'); inp.value = st.q; inp.setAttribute('aria-label', PP.t('ap.search'));
    inp.addEventListener('input', () => { st.q = inp.value; page = 0; clearTimeout(ui.qt); ui.qt = setTimeout(render, 150); });
    s.append(inp);
    const sp = document.createElement('span'); sp.className = 'spacer';
    f.append(ui.rules.el, s, sp, PP.resetBtn(() => { st = defaults(); page = 0; buildFilters(); render(); }));
  }

  function render() {
    const tk = PP.tok();
    const rows = filtered(false);
    const amt = rows.reduce((s, r) => s + r[7], 0);
    const by = (s) => rows.filter(r => r[5] === s);
    const blocked = by('blocked').reduce((s, r) => s + r[7], 0), review = by('review').reduce((s, r) => s + r[7], 0);

    const k = document.getElementById('k-ap'); k.innerHTML = '';
    k.append(
      PP.kpi(PP.t('ap.invoices'), PP.num(rows.length), { note: PP.lang() === 'es' ? `de ${PP.num(D.rows.length)} recibidas` : `of ${PP.num(D.rows.length)} received` }),
      PP.kpi(PP.t('ap.amount'), PP.ars(amt), { note: PP.arsFull(amt) }),
      PP.kpi(PP.t('ap.blocked'), PP.ars(blocked), { note: (amt ? PP.pct(blocked / amt) : '—') + ' ' + PP.t('ap.ofAmount') + ' · ' + PP.num(by('blocked').length) + ' ' + PP.t('ap.invoices').toLowerCase() }),
      PP.kpi(PP.t('ap.review'), PP.ars(review), { note: (amt ? PP.pct(review / amt) : '—') + ' ' + PP.t('ap.ofAmount') + ' · ' + PP.num(by('review').length) + ' ' + PP.t('ap.invoices').toLowerCase() })
    );

    /* Monthly stacked bars by status */
    const months = [...new Set(D.rows.map(r => r[3]))].sort();
    const mc = PP.chart('c-ap-month');
    const sts = STATUSES.filter(s => st.status.has(s));
    PP.legend(document.getElementById('lg-ap-month'), sts.map(s => [statusLabel(s), statusColor(tk, s)]), 'box');
    mc.setOption(Object.assign(PP.base(tk), {
      tooltip: Object.assign(PP.base(tk).tooltip, { trigger: 'axis', axisPointer: { type: 'shadow', shadowStyle: { color: 'rgba(127,127,127,.08)' } },
        formatter: ps => `<div style="margin-bottom:4px;opacity:.7">${PP.monthLabel(months[ps[0].dataIndex])}</div>` + ps.slice().reverse().map(p => PP.ttRow(p.color, PP.ars(p.value), p.seriesName)).join('') }),
      xAxis: PP.axisCat(tk, { data: months.map(PP.monthLabel) }),
      yAxis: PP.axisVal(tk, { axisLabel: { color: tk.muted, fontSize: 11.5, formatter: v => PP.ars(v).replace('ARS ', '') } }),
      series: sts.map((s, i) => ({ name: statusLabel(s), type: 'bar', stack: 'st', barWidth: '54%',
        itemStyle: { color: statusColor(tk, s), borderColor: tk.surface, borderWidth: 1, borderRadius: i === sts.length - 1 ? [4, 4, 0, 0] : 0 },
        data: months.map(m => Math.round(rows.filter(r => r[3] === m && r[5] === s).reduce((t, r) => t + r[7], 0))) }))
    }), true);

    /* Exceptions by rule */
    const rc = PP.chart('c-ap-rules');
    const base = filtered(true);
    const counts = D.rules.map(r => [r, base.filter(x => x[6].split(',').includes(r.rule)).length]).sort((x, y) => x[1] - y[1]);
    rc.setOption(Object.assign(PP.base(tk), {
      tooltip: Object.assign(PP.base(tk).tooltip, { trigger: 'item', formatter: p => { const r = counts[p.dataIndex][0]; return PP.ttRow(p.color, PP.num(p.value), r.rule + ' · ' + ruleName(r)) + `<div style="opacity:.7;margin-top:2px">${r.severity === 'block' ? (PP.lang() === 'es' ? 'bloquea el pago' : 'blocks payment') : (PP.lang() === 'es' ? 'requiere revisión' : 'needs review')}</div>`; } }),
      grid: { left: 4, right: 36, top: 4, bottom: 4, containLabel: true },
      xAxis: PP.axisVal(tk, { show: false }),
      yAxis: PP.axisCat(tk, { data: counts.map(c => c[0].rule + ' · ' + ruleName(c[0])), axisLabel: { color: tk.ink2, fontSize: 11, width: 190, overflow: 'truncate' } }),
      series: [{ type: 'bar', barWidth: '60%', cursor: 'pointer',
        data: counts.map(([r, n]) => ({ value: n, itemStyle: { color: (allRules() || st.rules.has(r.rule)) ? (r.severity === 'block' ? tk.crit : tk.warn) : tk.grid, borderRadius: [0, 4, 4, 0] } })),
        label: { show: true, position: 'right', color: tk.ink2, fontSize: 11.5 } }]
    }), true);
    PP.rowClick(rc, i => {
      if (!counts[i]) return; const code = counts[i][0].rule;
      st.rules = (st.rules.size === 1 && st.rules.has(code)) ? new Set(D.rules.map(r => r.rule)) : new Set([code]);
      ui.rules.set(st.rules); page = 0; render();
    });

    renderTable(rows);
  }

  function renderTable(rows) {
    const tw = document.getElementById('t-ap'); tw.innerHTML = '';
    const key = { amount: 7, date: 4, supplier: 1 }[sort.key];
    const sorted = rows.slice().sort((a, b) => (a[key] > b[key] ? 1 : a[key] < b[key] ? -1 : 0) * sort.dir);
    const pages = Math.max(1, Math.ceil(sorted.length / PER)); page = Math.min(page, pages - 1);
    const slice = sorted.slice(page * PER, page * PER + PER);
    const t = document.createElement('table'); t.className = 'dtable';
    const cols = [['id', 'ID'], ['date', PP.t('ap.date')], ['supplier', PP.t('ap.supplier')], ['cuit', 'CUIT'], ['status', PP.t('ap.status')], ['rules', PP.t('ap.rulesCol')], ['amount', PP.lang() === 'es' ? 'Monto' : 'Amount']];
    const hr = document.createElement('tr');
    cols.forEach(([k, label]) => {
      const th = document.createElement('th'); if (k === 'amount') th.className = 'num';
      if (['amount', 'date', 'supplier'].includes(k)) {
        const b = document.createElement('button'); b.type = 'button'; b.textContent = label + (sort.key === k ? (sort.dir === 1 ? ' ↑' : ' ↓') : '');
        th.setAttribute('aria-sort', sort.key === k ? (sort.dir === 1 ? 'ascending' : 'descending') : 'none');
        b.onclick = () => { sort = { key: k, dir: sort.key === k ? -sort.dir : (k === 'amount' ? -1 : 1) }; renderTable(rows); };
        th.append(b);
      } else th.textContent = label;
      hr.append(th);
    });
    const thead = document.createElement('thead'); thead.append(hr); t.append(thead);
    const tb = document.createElement('tbody');
    if (!slice.length) { const tr = document.createElement('tr'); const td = document.createElement('td'); td.colSpan = 7; td.className = 'empty'; td.textContent = PP.t('common.noData'); tr.append(td); tb.append(tr); }
    slice.forEach(r => {
      const tr = document.createElement('tr');
      const cell = (txt, cls) => { const td = document.createElement('td'); if (cls) td.className = cls; if (txt instanceof Node) td.append(txt); else td.textContent = txt; tr.append(td); return td; };
      cell(r[0]); cell(new Date(r[4] + 'T00:00').toLocaleDateString(PP.lang() === 'es' ? 'es-AR' : 'en-US', { day: '2-digit', month: 'short', year: 'numeric' }));
      cell(PP.name(r[1])); cell(fmtCuit(r[2]));
      const b = document.createElement('span'); b.className = 'badge'; b.append(ico(r[5]), document.createTextNode(statusLabel(r[5]))); cell(b);
      const rr = document.createElement('span'); (r[6] ? r[6].split(',') : []).forEach(x => { const p = document.createElement('span'); p.className = 'rulepill'; p.textContent = x; p.title = ruleName(D.rules.find(z => z.rule === x)); rr.append(p); }); cell(rr);
      cell(PP.arsFull(r[7]), 'num');
      tb.append(tr);
    });
    t.append(tb); tw.append(t);

    const pg = document.getElementById('p-ap'); pg.innerHTML = '';
    const info = document.createElement('span');
    info.textContent = `${PP.t('ap.showing')} ${sorted.length ? page * PER + 1 : 0}–${Math.min(sorted.length, page * PER + PER)} ${PP.t('ap.of')} ${PP.num(sorted.length)}`;
    const prev = document.createElement('button'); prev.type = 'button'; prev.textContent = PP.t('ap.prev'); prev.disabled = page === 0; prev.onclick = () => { page--; renderTable(rows); };
    const next = document.createElement('button'); next.type = 'button'; next.textContent = PP.t('ap.next'); next.disabled = page >= pages - 1; next.onclick = () => { page++; renderTable(rows); };
    pg.append(info, prev, next);
  }

  PP.ap = {
    async init() { D = await PP.loadJSON('assets/data/ap.json'); st = defaults(); buildFilters(); render(); },
    rerender() { if (!D) return; buildFilters(); render(); },
    focusRule(code) { if (!D) return; st.rules = new Set([code]); ui.rules.set(st.rules); render(); }
  };
})();
