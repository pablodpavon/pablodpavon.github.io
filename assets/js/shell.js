/* Shared page shell: language, theme, navigation, reveal-on-scroll, toast, copy email. */
(function () {
  'use strict';
  const root = document.documentElement;
  const S = (window.SHELL = { onLang: [], onTheme: [] });
  const base = document.body.dataset.base || '';

  /* language */
  S.lang = () => (root.lang === 'en' ? 'en' : 'es');
  S.setLang = (l, save) => {
    root.lang = l;
    if (save) { try { localStorage.setItem('lang', l); } catch (e) {} }
    document.querySelectorAll('[data-lang]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.lang === l)));
    document.querySelectorAll('[data-cv]').forEach(a => { a.href = base + (l === 'es' ? 'assets/CV_Pablo_Pavon_ES.pdf' : 'assets/CV_Pablo_Pavon_EN.pdf'); });
    const t = document.querySelector('meta[name="title-' + l + '"]'); if (t) document.title = t.content;
    S.onLang.forEach(f => f(l));
  };
  document.querySelectorAll('[data-lang]').forEach(b => b.addEventListener('click', () => S.setLang(b.dataset.lang, true)));

  /* theme */
  const btn = document.getElementById('themeBtn');
  S.isDark = () => root.getAttribute('data-theme') === 'dark' || (!root.getAttribute('data-theme') && matchMedia('(prefers-color-scheme: dark)').matches);
  const moon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
  const sun = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
  const paint = () => { if (!btn) return; btn.innerHTML = S.isDark() ? sun : moon; btn.setAttribute('aria-label', S.isDark() ? (S.lang() === 'es' ? 'Usar tema claro' : 'Use light theme') : (S.lang() === 'es' ? 'Usar tema oscuro' : 'Use dark theme')); };
  btn && btn.addEventListener('click', () => {
    const next = S.isDark() ? 'light' : 'dark';
    root.setAttribute('data-theme', next); try { localStorage.setItem('theme', next); } catch (e) {}
    paint(); S.onTheme.forEach(f => f());
  });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => { if (!root.getAttribute('data-theme')) { paint(); S.onTheme.forEach(f => f()); } });
  S.onLang.push(paint);

  /* nav */
  const nav = document.querySelector('.nav');
  const onScroll = () => nav && nav.classList.toggle('scrolled', scrollY > 10);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const links = [...document.querySelectorAll('.links a[href^="#"]')];
  if (links.length) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id)); }), { rootMargin: '-45% 0px -50% 0px' });
    links.forEach(l => { const s = document.querySelector(l.getAttribute('href')); s && io.observe(s); });
  }
  const menu = document.getElementById('menuBtn'), linkBox = document.querySelector('.links');
  menu && menu.addEventListener('click', () => { const o = linkBox.classList.toggle('open'); menu.setAttribute('aria-expanded', String(o)); });
  document.querySelectorAll('.links a').forEach(a => a.addEventListener('click', () => { linkBox.classList.remove('open'); menu && menu.setAttribute('aria-expanded', 'false'); }));

  /* reveal on scroll */
  const rv = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); rv.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.reveal').forEach(el => rv.observe(el));

  /* spotlight on tiles */
  document.querySelectorAll('.tile').forEach(t => t.addEventListener('pointermove', e => {
    const r = t.getBoundingClientRect(); t.style.setProperty('--mx', (e.clientX - r.left) + 'px'); t.style.setProperty('--my', (e.clientY - r.top) + 'px');
  }));

  /* toast + copy */
  const toast = document.createElement('div'); toast.className = 'toast'; toast.setAttribute('role', 'status'); document.body.append(toast);
  S.toast = (msg) => { toast.textContent = msg; toast.classList.add('show'); clearTimeout(S._tt); S._tt = setTimeout(() => toast.classList.remove('show'), 2200); };
  document.querySelectorAll('[data-copy]').forEach(b => b.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(b.dataset.copy); S.toast(S.lang() === 'es' ? 'Mail copiado' : 'Email copied'); }
    catch (e) { location.href = 'mailto:' + b.dataset.copy; }
  }));

  /* table of contents (case pages) */
  const toc = [...document.querySelectorAll('.toc a')];
  if (toc.length) {
    const io2 = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) toc.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id)); }), { rootMargin: '-30% 0px -60% 0px' });
    toc.forEach(a => { const s = document.querySelector(a.getAttribute('href')); s && io2.observe(s); });
  }

  /* year */
  document.querySelectorAll('[data-year]').forEach(e => e.textContent = new Date().getFullYear());

  S.setLang(S.lang(), false);
})();
