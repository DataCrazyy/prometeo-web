// ─────────────────────────────────────────────────────────────
//  Formularios del sitio (contacto, reunión, inscripción a cursos, lista de Talks).
//  1. Valida los campos marcados con data-req (y el formato del correo).
//  2. Abre WhatsApp con el mensaje ya escrito, para conversar al instante.
//  3. Si site.formEndpoint tiene la URL del Apps Script, guarda los datos del
//     cliente como una fila en Google Sheets y les avisa por correo
//     (ver tools/leads/README.md).
// ─────────────────────────────────────────────────────────────
import { site } from '../data/site';

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const waUrl = (text: string) => `https://wa.me/${site.whatsapp}?text=${encodeURIComponent(text)}`;

export function validate(form: HTMLFormElement): boolean {
  let ok = true;
  form.querySelectorAll<HTMLInputElement | HTMLTextAreaElement>('[data-req]').forEach((el) => {
    if (el.closest('[hidden]')) return; // campos ocultos no se validan
    const v = el.value.trim();
    const bad = !v || (el.type === 'email' && !EMAIL.test(v)) || (el.type === 'number' && el.min !== '' && Number(v) < Number(el.min));
    const err = el.dataset.err ? document.getElementById(el.dataset.err) : null;
    el.setAttribute('aria-invalid', String(bad));
    if (err) { err.hidden = !bad; if (bad) el.setAttribute('aria-describedby', err.id); else el.removeAttribute('aria-describedby'); }
    if (bad) ok = false;
  });
  if (!ok) form.querySelector<HTMLElement>('[aria-invalid="true"]')?.focus();
  return ok;
}

/**
 * Abre WhatsApp (siempre, de forma sincrónica para que el navegador no lo bloquee)
 * y, si hay endpoint, guarda el contacto en Google Sheets.
 * Devuelve true si además quedó guardado.
 */
export async function deliver(form: HTMLFormElement, waText: string, origen: string, extra: Record<string, string> = {}): Promise<boolean> {
  window.open(waUrl(waText), '_blank', 'noopener');
  return saveLead(form, origen, extra);
}

/** Guarda el contacto en Google Sheets (si hay formEndpoint), sin abrir WhatsApp. */
export async function saveLead(form: HTMLFormElement, origen: string, extra: Record<string, string> = {}): Promise<boolean> {
  if (!site.formEndpoint) return false;
  const body = new URLSearchParams();
  new FormData(form).forEach((v, k) => body.append(k, String(v)));
  Object.entries(extra).forEach(([k, v]) => body.append(k, v));
  body.append('origen', origen);
  body.append('pagina', location.pathname + location.search);
  try {
    // Apps Script no devuelve cabeceras CORS: se envía en modo no-cors (no se puede leer la respuesta).
    await fetch(site.formEndpoint, { method: 'POST', mode: 'no-cors', body, keepalive: true });
    return true;
  } catch {
    return false;
  }
}

export function setBusy(btn: HTMLButtonElement | null, busy: boolean, label: string) {
  if (!btn) return;
  btn.disabled = busy;
  const t = btn.querySelector('.lbl');
  if (t) t.textContent = busy ? 'Enviando…' : label;
}

// Limpia el error de un campo apenas la persona lo corrige
document.addEventListener('input', (e) => {
  const el = e.target as HTMLElement;
  if (el?.getAttribute?.('aria-invalid') === 'true') {
    el.setAttribute('aria-invalid', 'false');
    const id = el.dataset.err;
    if (id) { const err = document.getElementById(id); if (err) err.hidden = true; }
  }
});
