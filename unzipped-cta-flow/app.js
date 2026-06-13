/* ═══════════════════════════════════════════
   NOVEM DIGITAL — SHARED SITE JS
   theme toggle · nav scroll · mobile menu · reveal
   ═══════════════════════════════════════════ */
(function(){
  const root=document.documentElement;
  const themeBtn=document.querySelector('[data-theme-toggle]');
  if(themeBtn) themeBtn.addEventListener('click',()=>{
    root.setAttribute('data-theme',root.getAttribute('data-theme')==='dark'?'light':'dark');
  });

  const nav=document.getElementById('mainNav');
  addEventListener('scroll',()=>nav&&nav.classList.toggle('nav--scrolled',scrollY>40),{passive:true});

  const hamburger=document.getElementById('hamburgerBtn');
  const mobileClose=document.getElementById('mobileClose');
  const mobileOverlay=document.getElementById('mobileOverlay');
  const mobileMenu=document.getElementById('mobileMenu');
  function openMobile(){mobileMenu.classList.add('open');mobileOverlay.classList.add('open');document.body.classList.add('no-scroll');hamburger.setAttribute('aria-expanded','true');mobileMenu.setAttribute('aria-hidden','false');}
  function closeMobile(){mobileMenu.classList.remove('open');mobileOverlay.classList.remove('open');document.body.classList.remove('no-scroll');hamburger.setAttribute('aria-expanded','false');mobileMenu.setAttribute('aria-hidden','true');}
  if(hamburger) hamburger.addEventListener('click',openMobile);
  if(mobileClose) mobileClose.addEventListener('click',closeMobile);
  if(mobileOverlay) mobileOverlay.addEventListener('click',closeMobile);
  document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMobile();});
  document.querySelectorAll('.mobile-nav-trigger,.mobile-demo,.mobile-login').forEach(l=>l.addEventListener('click',closeMobile));

  const revEls=document.querySelectorAll('.rev');
  const observer=new IntersectionObserver(entries=>{
    entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');observer.unobserve(e.target);}});
  },{threshold:.12,rootMargin:'0px 0px -40px 0px'});
  revEls.forEach(el=>observer.observe(el));
})();
