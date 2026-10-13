/* Page shell: language, theme, tabs, navigation, lightbox. */
(function () {
  'use strict';
  const PP = window.PP;
  const root = document.documentElement;
  const DASH = { sales: PP.sales, ap: PP.ap, ret: PP.ret };
  const started = new Set();

  /* ---------- language ---------- */
  function setLang(l, save) {
    root.lang = l;
    if (save) { try { localStorage.setItem('lang', l); } catch (e) {} }
    document.querySelectorAll('[data-lang]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.lang === l)));
    document.querySelectorAll('[data-cv]').forEach(a => { a.href = l === 'es' ? 'assets/CV_Pablo_Pavon_ES.pdf' : 'assets/CV_Pablo_Pavon_EN.pdf'; });
    document.title = l === 'es' ? 'Pablo Pavon · Senior Business & Data Analyst' : 'Pablo Pavon · Senior Business & Data Analyst';
    PP.applyText();
    started.forEach(k => DASH[k].rerender());
  }
  document.querySelectorAll('[data-lang]').forEach(b => b.addEventListener('click', () => setLang(b.dataset.lang, true)));

  /* ---------- theme ---------- */
  const themeBtn = document.getElementById('themeBtn');
  const isDark = () => root.getAttribute('data-theme') === 'dark' || (!root.getAttribute('data-theme') && matchMedia('(prefers-color-scheme: dark)').matches);
  const sun = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
  const moon = themeBtn.innerHTML;
  const paintThemeBtn = () => { themeBtn.innerHTML = isDark() ? sun : moon; themeBtn.setAttribute('aria-label', isDark() ? (PP.lang() === 'es' ? 'Usar tema claro' : 'Use light theme') : (PP.lang() === 'es' ? 'Usar tema oscuro' : 'Use dark theme')); };
  themeBtn.addEventListener('click', () => {
    const next = isDark() ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
    paintThemeBtn(); PP.disposeAll(); started.forEach(k => DASH[k].rerender());
  });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => { if (!root.getAttribute('data-theme')) { paintThemeBtn(); PP.disposeAll(); started.forEach(k => DASH[k].rerender()); } });

  /* ---------- tabs ---------- */
  const tabs = [...document.querySelectorAll('[role=tab]')];
  async function openTab(name, focus) {
    tabs.forEach(t => {
      const on = t.dataset.tab === name;
      t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      if (on && focus) t.focus();
    });
    if (!started.has(name)) {
      started.add(name);
      try { await DASH[name].init(); } catch (e) { console.error(e); document.getElementById('panel-' + name).insertAdjacentHTML('beforeend', '<p class="empty">No se pudieron cargar los datos.</p>'); }
    } else { requestAnimationFrame(PP.resizeAll); }
  }
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => openTab(t.dataset.tab));
    t.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        e.preventDefault(); const n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length]; openTab(n.dataset.tab, true);
      }
    });
  });
  document.querySelectorAll('[data-open-tab]').forEach(a => a.addEventListener('click', () => openTab(a.dataset.openTab)));

  /* ---------- nav ---------- */
  const bar = document.querySelector('.topbar');
  const onScroll = () => bar.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const links = [...document.querySelectorAll('.nav a')];
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id));
  }), { rootMargin: '-40% 0px -55% 0px' });
  links.forEach(l => { const s = document.querySelector(l.getAttribute('href')); if (s) io.observe(s); });
  const menuBtn = document.getElementById('menuBtn'), nav = document.getElementById('nav');
  menuBtn.addEventListener('click', () => { const o = nav.classList.toggle('open'); menuBtn.setAttribute('aria-expanded', String(o)); });
  links.forEach(l => l.addEventListener('click', () => { nav.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); }));

  /* ---------- lightbox ---------- */
  const lb = document.getElementById('lightbox'), lbImg = lb.querySelector('img'), lbCap = lb.querySelector('figcaption');
  let lastFocus = null;
  function openLB(src, cap) { lastFocus = document.activeElement; lbImg.src = src; lbCap.textContent = cap || ''; lb.hidden = false; lb.querySelector('.close').focus(); document.body.style.overflow = 'hidden'; }
  function closeLB() { lb.hidden = true; lbImg.src = ''; document.body.style.overflow = ''; lastFocus && lastFocus.focus(); }
  document.querySelectorAll('[data-zoom-src]').forEach(b => b.addEventListener('click', () => {
    const h = b.parentElement.querySelector('h3:not([hidden])'); const cap = [...b.parentElement.querySelectorAll('h3')].find(x => x.getAttribute('lang') === PP.lang());
    openLB(b.dataset.zoomSrc, cap ? cap.textContent : '');
  }));
  document.querySelectorAll('img[data-zoom]').forEach(i => i.addEventListener('click', () => openLB(i.currentSrc || i.src, i.alt)));
  lb.addEventListener('click', e => { if (e.target === lb || e.target.classList.contains('close')) closeLB(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !lb.hidden) closeLB(); });

  /* ---------- start ---------- */
  setLang(root.lang === 'en' ? 'en' : 'es', false);
  paintThemeBtn();
  const hashTab = (location.hash.match(/^#lab-(sales|ap|ret)$/) || [])[1];
  openTab(hashTab || 'sales');
})();
