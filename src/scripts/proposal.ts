// ─────────────────────────────────────────────────────────────
//  Propuesta comercial personalizada.
//  La persona deja su nombre, empresa y WhatsApp; el navegador completa la portada
//  del PDF ("Preparada para", "Contacto" y "Fecha" de hoy), lo descarga y, si hay
//  formEndpoint, guarda el contacto en Google Sheets para un próximo seguimiento.
//  La plantilla es public/Propuesta_Comercial_Prometeo_Consulting.pdf
//  (tools/propuesta/make_proposal.py deja esos tres campos vacíos).
// ─────────────────────────────────────────────────────────────
import { validate, saveLead } from './forms';
import { site } from '../data/site';

const MM = 72 / 25.4;
// Posiciones de los valores en la portada (A4, en puntos desde abajo a la izquierda)
const COL1 = 28 * MM, COL2 = 28 * MM + (595.28 - 40 * MM) / 2, MAXW = 72 * MM;
const FIELDS = { preparada: [COL1, 86 * MM], contacto: [COL2, 86 * MM], fecha: [COL1, 71 * MM] } as const;

const base = import.meta.env.BASE_URL;
const asset = (p: string) => `${base.endsWith('/') ? base : base + '/'}${p}`;

function today() {
  const d = new Date();
  return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}/${d.getFullYear()}`;
}
const slug = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^A-Za-z0-9]+/g, '_').replace(/^_|_$/g, '').slice(0, 40);

const loaded = new Map<string, Promise<void>>();
function loadScript(src: string) {
  if (!loaded.has(src)) loaded.set(src, new Promise((ok, fail) => {
    const el = Object.assign(document.createElement('script'), { src, async: true });
    el.onload = () => ok(); el.onerror = () => fail(new Error('No se pudo cargar ' + src));
    document.head.append(el);
  }));
  return loaded.get(src)!;
}

async function buildPdf(preparada: string, contacto: string, fecha: string) {
  // pdf-lib y fontkit viven en public/vendor/ (no necesitan npm) y se cargan solo al pedir la propuesta
  await Promise.all([loadScript(asset('vendor/pdf-lib.min.js')), loadScript(asset('vendor/fontkit.umd.min.js'))]);
  const { PDFDocument, rgb } = (window as any).PDFLib;
  const fontkit = (window as any).fontkit;
  const [tpl, fontBytes] = await Promise.all([
    fetch(asset(site.proposalFile)).then((r) => r.arrayBuffer()),
    fetch(asset('fonts/inter-600.ttf')).then((r) => r.arrayBuffer()),
  ]);
  const pdf = await PDFDocument.load(tpl);
  pdf.registerFontkit(fontkit);
  const font = await pdf.embedFont(fontBytes, { subset: true });
  const page = pdf.getPage(0);
  const put = (text: string, [x, y]: readonly [number, number]) => {
    let size = 11;
    while (size > 7 && font.widthOfTextAtSize(text, size) > MAXW) size -= 0.5;
    let t = text;
    while (font.widthOfTextAtSize(t, size) > MAXW && t.length > 4) t = t.slice(0, -2) + '…';
    page.drawText(t, { x, y, size, font, color: rgb(1, 1, 1) });
  };
  put(preparada, FIELDS.preparada);
  put(contacto, FIELDS.contacto);
  put(fecha, FIELDS.fecha);
  pdf.setTitle(`Propuesta comercial Prometeo Consulting · ${preparada}`);
  pdf.setAuthor('Prometeo Consulting');
  return pdf.save();
}

function download(bytes: Uint8Array, name: string) {
  const blob = new Blob([bytes], { type: 'application/pdf' });
  const href = URL.createObjectURL(blob);
  const a = Object.assign(document.createElement('a'), { href, download: name });
  document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(href), 60_000);
}

const dlg = document.querySelector<HTMLDialogElement>('#dlg-propuesta');
const form = dlg?.querySelector<HTMLFormElement>('form');
let last: { bytes: Uint8Array; name: string } | null = null;

document.querySelectorAll<HTMLElement>('[data-open-proposal]').forEach((b) =>
  b.addEventListener('click', (e) => { e.preventDefault(); dlg?.showModal(); dlg?.querySelector<HTMLInputElement>('input')?.focus(); }));
dlg?.querySelectorAll('[data-close]').forEach((b) => b.addEventListener('click', () => dlg.close()));
dlg?.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });
dlg?.querySelector('[data-again]')?.addEventListener('click', () => last && download(last.bytes, last.name));

form?.addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!validate(form)) return;
  const btn = form.querySelector<HTMLButtonElement>('button[type="submit"]');
  const lbl = btn?.querySelector('.lbl');
  const fd = new FormData(form);
  const nombre = String(fd.get('nombre') ?? '').trim();
  const empresa = String(fd.get('empresa') ?? '').trim();
  const tel = String(fd.get('whatsapp') ?? '').trim();
  const fecha = today();
  const preparada = empresa || nombre;
  const contacto = [empresa ? nombre : '', tel].filter(Boolean).join(' · ');
  if (btn) btn.disabled = true;
  if (lbl) lbl.textContent = 'Preparando tu propuesta…';
  try {
    const bytes = await buildPdf(preparada, contacto, fecha);
    last = { bytes, name: `Propuesta_Prometeo_Consulting_${slug(preparada) || 'cliente'}.pdf` };
    download(last.bytes, last.name);
    saveLead(form, 'Propuesta comercial', { fecha });
    form.hidden = true;
    const ok = dlg?.querySelector<HTMLElement>('[data-done]');
    if (ok) { ok.hidden = false; ok.querySelector('[data-who]')!.textContent = nombre.split(/\s+/)[0]; }
  } catch (err) {
    console.error(err);
    const fail = dlg?.querySelector<HTMLElement>('[data-fail]');
    if (fail) fail.hidden = false;
  } finally {
    if (btn) btn.disabled = false;
    if (lbl) lbl.textContent = 'Descargar mi propuesta';
  }
});
