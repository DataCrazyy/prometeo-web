import type { APIRoute } from 'astro';
// Mapa del sitio para Google (se genera con la URL de SITE_URL).
const pages = ['', 'consulting/', 'academy/', 'talks/', 'precio-justo/', 'nosotros/', 'contacto/'];
export const GET: APIRoute = ({ site }) => {
  const base = new URL(import.meta.env.BASE_URL, site);
  const urls = pages.map((p) => `<url><loc>${new URL(p, base).href}</loc></url>`).join('');
  return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls}</urlset>`,
    { headers: { 'Content-Type': 'application/xml' } });
};
