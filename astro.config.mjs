// @ts-check
import { defineConfig } from 'astro/config';

// SITE: tu dominio final (ej. https://prometeo.bo).
// BASE: déjalo en '/' si usas dominio propio, Vercel, Netlify o Cloudflare Pages.
//       Si publicas en https://<usuario>.github.io/<repo>/ sin dominio, pon '/<repo>/'.
export default defineConfig({
  site: process.env.SITE_URL ?? 'https://techprometeo.com',
  base: process.env.BASE_PATH ?? '/',
  trailingSlash: 'ignore',
  build: { format: 'directory' },
});
