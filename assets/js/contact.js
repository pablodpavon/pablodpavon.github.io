/* Contact layer: fixed contact dock, mobile bar, slide-over drawer and the contact form.
   Messages are delivered by e-mail through FormSubmit (https://formsubmit.co). */
(function () {
  'use strict';
  const S = window.SHELL;
  const EMAIL = 'contact@pablodpavon.com';
  const LINKEDIN = 'https://www.linkedin.com/in/pablo-damian-pavon';
  const ENDPOINT = 'https://formsubmit.co/ajax/' + EMAIL;
  const base = document.body.dataset.base || '/';
  const L = () => S.lang();
  const bi = (es, en) => (L() === 'es' ? es : en);  // one language per page

  const I = {
    msg: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/><path d="M8.5 10.5h7M8.5 13.5h4"/></svg>',
    mail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.5 7 8.5 6 8.5-6"/></svg>',
    li: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.1c.5-1 1.8-2 3.7-2 4 0 4.7 2.6 4.7 6V21h-4v-5.6c0-1.3 0-3-1.9-3s-2.1 1.4-2.1 2.9V21H9z"/></svg>',
    cv: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M12 11v6m0 0-2.5-2.5M12 17l2.5-2.5"/></svg>',
    close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    copy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>',
    send: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2 11 13M22 2l-7 20-4-9-9-4z"/></svg>',
    ok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 5 5 9-10"/></svg>',
    warn: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>'
  };

  const TOPICS = [
    ['dash', 'Dashboards y BI', 'Dashboards & BI'],
    ['fin', 'Automatización financiera', 'Finance automation'],
    ['data', 'Análisis de datos', 'Data analysis'],
    ['mig', 'Migración de datos', 'Data migration'],
    ['ai', 'IA en procesos', 'AI in processes'],
    ['req', 'Requerimientos', 'Requirements'],
    ['other', 'Otro', 'Other']
  ];
  const TIMES = [
    ['', 'Elegí una opción', 'Choose one'],
    ['asap', 'Lo antes posible', 'As soon as possible'],
    ['month', 'En el próximo mes', 'Within the next month'],
    ['quarter', 'En los próximos 3 meses', 'In the next 3 months'],
    ['explore', 'Estoy explorando', 'Just exploring']
  ];

  /* ---------- markup ---------- */
  function formHTML(p) {
    const topics = TOPICS.map(([v, es, en]) =>
      `<label class="tchip"><input type="checkbox" name="topics" value="${v}"><span>${bi(es, en)}</span></label>`).join('');
    const times = TIMES.map(([v, es, en]) => `<option value="${v}">${bi(es, en)}</option>`).join('');
    return `
<form class="cform" novalidate data-form="${p}">
  <div class="cf-grid">
    <div class="fld"><label for="${p}-name">${bi('Nombre', 'Name')} <em>*</em></label><input id="${p}-name" name="name" autocomplete="name" required maxlength="80"><small class="err"></small></div>
    <div class="fld"><label for="${p}-email">${bi('Email de trabajo', 'Work email')} <em>*</em></label><input id="${p}-email" name="email" type="email" autocomplete="email" required maxlength="120"><small class="err"></small></div>
    <div class="fld"><label for="${p}-company">${bi('Empresa', 'Company')}</label><input id="${p}-company" name="company" autocomplete="organization" maxlength="100"></div>
    <div class="fld"><label for="${p}-time">${bi('¿Para cuándo?', 'Timeline')}</label><div class="sel"><select id="${p}-time" name="timeline">${times}</select></div></div>
  </div>
  <fieldset class="fld"><legend>${bi('¿En qué te puedo ayudar?', 'What do you need help with?')}</legend><div class="tchips">${topics}</div></fieldset>
  <div class="fld"><label for="${p}-msg">${bi('Contame el problema', 'Tell me about the problem')} <em>*</em></label>
    <textarea id="${p}-msg" name="message" rows="5" required minlength="20" maxlength="3000"></textarea>
    <div class="hint"><span class="err"></span><span class="count" aria-hidden="true">0 / 3000</span></div></div>
  <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
  <div class="cf-foot">
    <p class="legal">${bi('Uso tus datos solo para responderte. El mensaje se envía por e-mail a través de FormSubmit.', 'I use your details only to reply. The message is sent by e-mail through FormSubmit.')}</p>
    <button class="btn btn-brand cf-submit" type="submit"><span class="spin" aria-hidden="true"></span>${I.send}${bi('Enviar mensaje', 'Send message')}</button>
  </div>
  <div class="cf-alert" role="alert" hidden></div>
</form>
<div class="cf-done" hidden tabindex="-1">
  <div class="ring">${I.ok}</div>
  <h3>${bi('Mensaje enviado', 'Message sent')}</h3>
  <p>${bi('Gracias. Te respondo por mail en 1 o 2 días hábiles.', 'Thank you. I will reply by e-mail within 1–2 business days.')}</p>
  <button type="button" class="btn btn-sm cf-again">${bi('Enviar otro mensaje', 'Send another message')}</button>
</div>`;
  }

  const dock = document.createElement('aside');
  dock.className = 'cdock';
  dock.setAttribute('aria-label', 'Contacto');
  dock.innerHTML = `
  <div class="cdock-av" title="Pablo Pavon"><span class="logo">PP</span><i class="live" aria-hidden="true"></i></div>
  <button type="button" class="cdock-btn primary" data-open-contact aria-label="Escribime">${I.msg}<span class="tip">${bi('Escribime', 'Send a message')}</span></button>
  <a class="cdock-btn" href="mailto:${EMAIL}" aria-label="Email">${I.mail}<span class="tip">${EMAIL}</span></a>
  <a class="cdock-btn" href="${LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn">${I.li}<span class="tip">LinkedIn</span></a>
  <a class="cdock-btn" data-cv href="${base}assets/CV_Pablo_Pavon_ES.pdf" download aria-label="CV">${I.cv}<span class="tip">${bi('Descargar CV', 'Download CV')}</span></a>`;

  const bar = document.createElement('div');
  bar.className = 'cbar';
  bar.innerHTML = `
  <button type="button" class="btn btn-brand" data-open-contact>${I.msg}${bi('Escribime', 'Message me')}</button>
  <a class="icon-btn" href="mailto:${EMAIL}" aria-label="Email">${I.mail}</a>
  <a class="icon-btn" href="${LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn">${I.li}</a>`;

  const drawer = document.createElement('div');
  drawer.className = 'cdrawer';
  drawer.hidden = true;
  drawer.innerHTML = `
  <div class="cd-scrim" data-close-contact></div>
  <section class="cd-panel" role="dialog" aria-modal="true" aria-labelledby="cd-title">
    <header class="cd-head">
      <div class="who"><span class="logo">PP</span><div><b>Pablo Pavon</b><small><i class="live" aria-hidden="true"></i>${bi('Respuesta en 1–2 días hábiles', 'Replies within 1–2 business days')}</small></div></div>
      <button type="button" class="icon-btn" data-close-contact aria-label="Cerrar">${I.close}</button>
    </header>
    <div class="cd-body">
      <h2 id="cd-title">${bi('Contame qué necesitás', 'Tell me what you need')}</h2>
      <p class="cd-lede">${bi('Con una descripción breve alcanza. Te respondo con preguntas concretas o con una propuesta por escrito: alcance, plazos y precio.', 'A short description is enough. I reply with specific questions or a written proposal: scope, timeline and price.')}</p>
      ${formHTML('d')}
      <div class="cd-alt">
        <span>${bi('¿Preferís escribir directo?', 'Prefer to write directly?')}</span>
        <div class="cd-links">
          <button type="button" class="cd-mail" data-copy="${EMAIL}">${I.mail}<span>${EMAIL}</span>${I.copy}</button>
          <a class="cd-li" href="${LINKEDIN}" target="_blank" rel="noopener">${I.li}LinkedIn</a>
        </div>
      </div>
    </div>
  </section>`;

  document.body.append(dock, bar, drawer);
  document.body.classList.add('has-cbar');
  const inline = document.getElementById('contact-form');
  if (inline) inline.innerHTML = formHTML('i');

  /* copy buttons inside the injected markup */
  drawer.querySelectorAll('[data-copy]').forEach(b => b.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(b.dataset.copy); S.toast(L() === 'es' ? 'Mail copiado' : 'Email copied'); }
    catch (e) { location.href = 'mailto:' + b.dataset.copy; }
  }));
  document.querySelectorAll('[data-cv]').forEach(a => { a.href = base + (L() === 'es' ? 'assets/CV_Pablo_Pavon_ES.pdf' : 'assets/CV_Pablo_Pavon_EN.pdf'); });

  /* ---------- drawer ---------- */
  const panel = drawer.querySelector('.cd-panel');
  let lastFocus = null;
  function open(topic) {
    lastFocus = document.activeElement;
    drawer.hidden = false;
    requestAnimationFrame(() => drawer.classList.add('open'));
    document.documentElement.classList.add('cd-lock');
    if (topic) { const c = drawer.querySelector(`input[name=topics][value="${topic}"]`); if (c) c.checked = true; }
    setTimeout(() => { const f = drawer.querySelector('.cf-done:not([hidden])') || drawer.querySelector('#d-name'); f && f.focus(); }, 260);
  }
  function close() {
    drawer.classList.remove('open');
    document.documentElement.classList.remove('cd-lock');
    setTimeout(() => { drawer.hidden = true; }, 280);
    lastFocus && lastFocus.focus && lastFocus.focus();
  }
  S.openContact = open;
  document.addEventListener('click', e => {
    const o = e.target.closest('[data-open-contact]');
    if (o) { e.preventDefault(); open(o.dataset.topic); return; }
    if (e.target.closest('[data-close-contact]')) close();
  });
  document.addEventListener('keydown', e => {
    if (drawer.hidden) return;
    if (e.key === 'Escape') { close(); return; }
    if (e.key === 'Tab') {
      const f = [...panel.querySelectorAll('a[href],button:not([disabled]),input:not(.hp),select,textarea,[tabindex="0"]')].filter(x => x.offsetParent !== null);
      if (!f.length) return;
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  if (location.hash === '#escribime') open();

  /* ---------- form logic ---------- */
  const MSG = {
    es: { req: 'Completá este campo.', email: 'Revisá el formato del mail.', short: 'Contame un poco más (mínimo 20 caracteres).',
      fail: 'No se pudo enviar el mensaje. Probá de nuevo o escribime directo a ', mailto: 'Abrir en mi correo', sending: 'Enviando…' },
    en: { req: 'Please fill in this field.', email: 'Please check the e-mail format.', short: 'Tell me a bit more (at least 20 characters).',
      fail: 'The message could not be sent. Try again or write to me directly at ', mailto: 'Open in my mail app', sending: 'Sending…' }
  };
  const DRAFT = 'contact-draft';
  const readDraft = () => { try { return JSON.parse(localStorage.getItem(DRAFT) || '{}'); } catch (e) { return {}; } };
  const saveDraft = d => { try { localStorage.setItem(DRAFT, JSON.stringify(d)); } catch (e) {} };
  const clearDraft = () => { try { localStorage.removeItem(DRAFT); } catch (e) {} };

  function wire(form) {
    const wrap = form.parentElement, done = wrap.querySelector('.cf-done');
    const msg = form.elements.message, count = form.querySelector('.count');
    const d = readDraft();
    ['name', 'email', 'company', 'timeline', 'message'].forEach(k => { if (d[k]) form.elements[k].value = d[k]; });
    const upd = () => { count.textContent = msg.value.length + ' / 3000'; };
    upd();
    form.addEventListener('input', e => {
      upd();
      const f = e.target.closest('.fld'); if (f) f.classList.remove('bad');
      const o = {}; ['name', 'email', 'company', 'timeline', 'message'].forEach(k => o[k] = form.elements[k].value); saveDraft(o);
    });
    function check() {
      const m = MSG[L()]; let firstBad = null;
      const set = (el, text) => { const f = el.closest('.fld'); f.classList.toggle('bad', !!text); const er = f.querySelector('.err'); if (er) er.textContent = text || ''; if (text && !firstBad) firstBad = el; };
      const n = form.elements.name, em = form.elements.email;
      set(n, n.value.trim() ? '' : m.req);
      set(em, !em.value.trim() ? m.req : (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em.value.trim()) ? '' : m.email));
      set(msg, !msg.value.trim() ? m.req : (msg.value.trim().length < 20 ? m.short : ''));
      if (firstBad) firstBad.focus();
      return !firstBad;
    }
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const alert = form.querySelector('.cf-alert'); alert.hidden = true;
      if (!check()) return;
      if (form.elements._honey.value) return; // bot
      const btn = form.querySelector('.cf-submit');
      btn.disabled = true; form.classList.add('sending');
      const topics = [...form.querySelectorAll('input[name=topics]:checked')].map(c => TOPICS.find(t => t[0] === c.value)[1]);
      const tSel = form.elements.timeline, tOpt = tSel.options[tSel.selectedIndex];
      const name = form.elements.name.value.trim(), company = form.elements.company.value.trim();
      const payload = {
        name, email: form.elements.email.value.trim(), company: company || '—',
        topics: topics.join(', ') || '—', timeline: tSel.value ? tOpt.dataset.es : '—',
        message: msg.value.trim(), page: location.href, language: L(),
        _subject: 'Contacto web: ' + name + (company ? ' · ' + company : ''),
        _template: 'table', _captcha: 'false'
      };
      try {
        const r = await fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(payload) });
        const j = await r.json().catch(() => ({}));
        if (!r.ok || String(j.success) !== 'true') throw new Error(j.message || 'HTTP ' + r.status);
        clearDraft(); form.reset(); upd();
        form.hidden = true; done.hidden = false; done.focus();
      } catch (err) {
        const m = MSG[L()];
        const body = encodeURIComponent(`${payload.message}\n\n— ${payload.name}${company ? ', ' + company : ''}\n${payload.email}`);
        alert.innerHTML = `${I.warn}<div>${m.fail}<a href="mailto:${EMAIL}">${EMAIL}</a>.<br><a class="mt" href="mailto:${EMAIL}?subject=${encodeURIComponent(payload._subject)}&body=${body}">${m.mailto}</a></div>`;
        alert.hidden = false;
      } finally { btn.disabled = false; form.classList.remove('sending'); }
    });
    done.querySelector('.cf-again').addEventListener('click', () => { done.hidden = true; form.hidden = false; form.elements.name.focus(); });
  }
  document.querySelectorAll('.cform').forEach(wire);
})();
