// ─────────────────────────────────────────────────────────────
//  Capa de interacción (estilo Apple): scroll suave, apariciones,
//  titulares palabra por palabra, contadores, parallax y secciones "sticky".
//  Librería: GSAP + ScrollTrigger (gsap.com). El scroll es el nativo del navegador (sin retraso).
//  Todo el contenido es visible sin JavaScript; esto solo añade movimiento.
// ─────────────────────────────────────────────────────────────
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = window.matchMedia('(pointer: fine)').matches;

/* Historia "sticky": se activa también con movimiento reducido (solo cambia de estado) */
function initStories() {
  document.querySelectorAll<HTMLElement>('[data-story]').forEach((story) => {
    const steps = [...story.querySelectorAll<HTMLElement>('[data-step]')];
    const visuals = [...story.querySelectorAll<HTMLElement>('[data-visual]')];
    const setActive = (i: number) => {
      story.dataset.active = String(i);
      steps.forEach((s, j) => s.classList.toggle('is-active', i === j));
      visuals.forEach((v, j) => v.classList.toggle('is-active', i === j));
    };
    setActive(0);
    steps.forEach((step, i) => {
      ScrollTrigger.create({
        trigger: step,
        start: 'top 55%',
        end: 'bottom 55%',
        onToggle: (self) => self.isActive && setActive(i),
      });
    });
  });
}

/* Contadores: "+20" cuenta de 0 a 20 */
function initCounters() {
  document.querySelectorAll<HTMLElement>('[data-count]').forEach((el) => {
    const target = Number(el.dataset.count);
    if (!Number.isFinite(target)) return;
    const prefix = el.dataset.prefix ?? '';
    const suffix = el.dataset.suffix ?? '';
    const obj = { v: 0 };
    el.textContent = `${prefix}0${suffix}`;
    gsap.to(obj, {
      v: target, duration: 1.6, ease: 'power2.out',
      scrollTrigger: { trigger: el, start: 'top 88%', once: true },
      onUpdate: () => { el.textContent = `${prefix}${Math.round(obj.v)}${suffix}`; },
    });
  });
}

function initMotion() {
  document.documentElement.classList.add('motion');

  ScrollTrigger.config({ ignoreMobileResize: true });

  // Titulares palabra por palabra
  document.querySelectorAll<HTMLElement>('[data-split]').forEach((el) => {
    if (el.dataset.splitDone) return;
    el.dataset.splitDone = '1';
    el.setAttribute('aria-label', el.textContent?.replace(/\s+/g, ' ').trim() ?? '');
    const walk = (node: Node) => {
      [...node.childNodes].forEach((child) => {
        if (child.nodeType === Node.TEXT_NODE) {
          const frag = document.createDocumentFragment();
          (child.textContent ?? '').split(/(\s+)/).forEach((part) => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.append(part); return; }
            const outer = document.createElement('span');
            outer.className = 'w';
            outer.setAttribute('aria-hidden', 'true');
            const inner = document.createElement('span');
            inner.className = 'wi';
            inner.textContent = part;
            outer.append(inner);
            frag.append(outer);
          });
          child.replaceWith(frag);
        } else if (child.nodeType === Node.ELEMENT_NODE) {
          walk(child);
        }
      });
    };
    walk(el);
    gsap.from(el.querySelectorAll('.wi'), {
      yPercent: 110, opacity: 0, duration: 0.9, ease: 'power3.out', stagger: 0.045,
      scrollTrigger: el.dataset.split === 'scroll' ? { trigger: el, start: 'top 85%', once: true } : undefined,
      delay: el.dataset.split === 'scroll' ? 0 : 0.15,
    });
  });

  // Apariciones suaves
  gsap.set('.reveal', { opacity: 0, y: 28 });
  ScrollTrigger.batch('.reveal', {
    start: 'top 90%',
    once: true,
    onEnter: (els) => gsap.to(els, { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out', stagger: 0.08, overwrite: true }),
  });

  // Visual del hero: se inclina y escala al hacer scroll (tipo producto Apple)
  document.querySelectorAll<HTMLElement>('[data-hero-visual]').forEach((el) => {
    gsap.fromTo(el, { y: 40, opacity: 0, rotateX: 14, scale: 0.94 }, { y: 0, opacity: 1, rotateX: 0, scale: 1, duration: 1.2, ease: 'power3.out', delay: 0.3 });
    gsap.to(el, {
      yPercent: -8, rotateX: -6, scale: 0.96, ease: 'none',
      scrollTrigger: { trigger: el, start: 'top 20%', end: 'bottom top', scrub: 0.3 },
    });
  });

  // Parallax ligero
  document.querySelectorAll<HTMLElement>('[data-parallax]').forEach((el) => {
    const amount = Number(el.dataset.parallax) || 12;
    gsap.fromTo(el, { yPercent: amount }, {
      yPercent: -amount, ease: 'none',
      scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: 0.3 },
    });
  });

  // Barras de gráficos que crecen
  document.querySelectorAll<HTMLElement>('[data-grow]').forEach((el) => {
    gsap.from(el.querySelectorAll('[data-bar]'), {
      scaleY: 0, transformOrigin: 'bottom', duration: 1, ease: 'power3.out', stagger: 0.05,
      scrollTrigger: { trigger: el, start: 'top 85%', once: true },
    });
  });

  // Tarjetas con inclinación 3D al pasar el mouse
  if (finePointer) {
    document.querySelectorAll<HTMLElement>('[data-tilt]').forEach((el) => {
      const qx = gsap.quickTo(el, 'rotateY', { duration: 0.5, ease: 'power3.out' });
      const qy = gsap.quickTo(el, 'rotateX', { duration: 0.5, ease: 'power3.out' });
      gsap.set(el, { transformPerspective: 1000 });
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        qx(((e.clientX - r.left) / r.width - 0.5) * 8);
        qy(-((e.clientY - r.top) / r.height - 0.5) * 8);
      });
      el.addEventListener('pointerleave', () => { qx(0); qy(0); });
    });
  }

  initCounters();
}

initStories();
if (!reduce) initMotion();
window.addEventListener('load', () => ScrollTrigger.refresh());
