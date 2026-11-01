/* Systems status: renders /assets/data/status.json (written by tools/status/build_status.py) into #st-grid.
   If the file is missing or broken, the static fallback text in the page stays. Added 1-nov-2026. */
(function () {
  'use strict';
  const grid = document.getElementById('st-grid');
  if (!grid) return;
  const es = document.documentElement.lang === 'es';
  const T = es
    ? { ok: 'Funcionando', bad: 'Revisar', none: 'Sin datos', last: 'Última corrida', items: 'Procesado', cost: 'Costo',
        dur: 'Duración', resp: 'Respuesta', sched: 'Frecuencia', open: 'Abrir', gen: 'Datos generados', ago: 'hace',
        min: 'min', h: 'h', d: 'd', now: 'recién', free: 'US$ 0', empty: 'Todavía no hay datos de estado publicados.' }
    : { ok: 'Running', bad: 'Check', none: 'No data', last: 'Last run', items: 'Processed', cost: 'Cost',
        dur: 'Duration', resp: 'Response', sched: 'Schedule', open: 'Open', gen: 'Data generated', ago: 'ago',
        min: 'min', h: 'h', d: 'd', now: 'just now', free: 'US$ 0', empty: 'No status data has been published yet.' };
  const loc = es ? 'es-AR' : 'en-GB';
  const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
  const pick = (s, k) => (es ? s[k + '_es'] : s[k + '_en']) || s[k + '_en'] || s[k] || '';
  const num = (n, dec) => Number(n).toLocaleString(loc, { minimumFractionDigits: dec || 0, maximumFractionDigits: dec || 0 });

  function when(iso) {
    if (!iso) return '—';
    const dateOnly = /^\d{4}-\d{2}-\d{2}$/.test(iso);
    const t = new Date(dateOnly ? iso + 'T12:00:00Z' : iso);
    if (isNaN(t)) return '—';
    const abs = dateOnly
      ? t.toLocaleDateString(loc, { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' })
      : t.toLocaleString(loc, { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Europe/Berlin', timeZoneName: 'short' });
    if (dateOnly) return abs;
    const m = Math.round((Date.now() - t) / 60000);
    const rel = m < 2 ? T.now : m < 90 ? `${m} ${T.min}` : m < 48 * 60 ? `${Math.round(m / 60)} ${T.h}` : `${Math.round(m / 1440)} ${T.d}`;
    return `${abs} · ${m < 2 ? rel : es ? `${T.ago} ${rel}` : `${rel} ${T.ago}`}`;
  }
  function dur(s) {
    if (s == null) return null;
    const m = Math.floor(s / 60), r = s % 60;
    return m ? `${m} min ${String(r).padStart(2, '0')} s` : `${r} s`;
  }
  function cost(v) {
    if (v == null) return null;
    if (v === 0) return T.free;
    return 'US$ ' + num(v, v < 0.01 ? 4 : v < 1 ? 4 : 2);
  }

  function card(s) {
    const c = el('article', 'st-card');
    const head = el('div', 'st-head');
    const name = el('div');
    name.append(el('h2', null, pick(s, 'title')));
    const kind = pick(s, 'kind');
    if (kind) name.append(el('small', null, kind));
    const state = s.last_run_utc == null ? 'none' : s.ok ? 'ok' : 'bad';
    const pill = el('span', 'st-state ' + state);
    pill.append(el('i'), document.createTextNode(T[state]));
    head.append(name, pill);
    c.append(head);

    const dl = el('dl', 'st-rows');
    const row = (k, v) => { if (v == null || v === '') return; dl.append(el('dt', null, k), el('dd', null, v)); };
    row(T.last, when(s.last_run_utc));
    if (s.items != null) row(T.items, `${num(s.items)} ${pick(s, 'items_label')}`.trim());
    row(T.cost, cost(s.cost_usd));
    row(T.dur, dur(s.duration_s));
    if (s.latency_ms != null) row(T.resp, `${num(s.latency_ms)} ms`);
    row(T.sched, pick(s, 'schedule'));
    c.append(dl);

    const note = es ? (s.note_es || s.note) : s.note;
    if (note) c.append(el('p', 'st-note', note));
    if (s.link && /^https:\/\//.test(s.link)) {
      const a = el('a', null, `${T.open}: ${s.link.replace(/^https:\/\//, '').replace(/\/$/, '')}`);
      a.href = s.link; a.rel = 'noopener';
      const p = el('p', 'st-note'); p.append(a); c.append(p);
    }
    return c;
  }

  fetch('/assets/data/status.json', { cache: 'no-cache' })
    .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(d => {
      const list = Array.isArray(d.systems) ? d.systems : [];
      if (!list.length) { grid.replaceChildren(el('p', 'st-empty', T.empty)); return; }
      grid.replaceChildren(...list.map(card));
      const meta = document.getElementById('st-meta');
      if (meta && d.generated_utc) { meta.textContent = `${T.gen}: ${when(d.generated_utc)}`; meta.hidden = false; }
    })
    .catch(() => { /* keep the static fallback that is already in the page */ });
})();
