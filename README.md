# Prometeo · sitio web

Sitio oficial de **Prometeo**, la marca que agrupa:

| Línea | Página | Qué es |
|---|---|---|
| Prometeo Consulting | `/consulting` | Asesorías de Business Intelligence y Power BI, con modalidades, propuesta comercial y cronograma |
| Prometeo Academy | `/academy` | Cursos y capacitaciones (Student, Enterprise, abiertos) |
| Precio Justo | `/precio-justo` | Monitoreo de precios de la competencia con web scraping |
| Prometeo Talks | `/talks` | Conferencias, eventos y videos (próximamente, con lista de espera) |
| Alianzas | `/#alianzas` | Universidades e instituciones aliadas |

## Stack

- **[Astro 5](https://astro.build)**: genera HTML estático, rápido y bueno para SEO, sin frameworks pesados.
- **CSS propio** con los colores y tipografías originales (Sora + Inter, violeta `#7C4DFF`), en `src/styles/global.css`.
- **Fuentes alojadas en el propio sitio** (`@fontsource`), sin depender de Google Fonts.
- **Imágenes optimizadas** automáticamente a WebP con `astro:assets`.
- Accesible: navegación con teclado, contraste AA, `prefers-reduced-motion` respetado.

## Editar contenido

| Quiero cambiar… | Archivo |
|---|---|
| Correo, WhatsApp, LinkedIn, link de agenda, formularios | `src/data/site.ts` |
| Cifras (+20 dashboards, etc.) | `src/data/site.ts` → `stats` |
| Texto de la portada, alianzas | `src/pages/index.astro` |
| Servicios, portafolio, metodología | `src/pages/consulting.astro` |
| Precios y modalidades | `src/components/Plans.astro` |
| Propuesta comercial y cronograma (Gantt) | `src/components/Proposal.astro` |
| Cursos | `src/pages/academy.astro` |
| Logos de clientes | `src/assets/clients/` + `src/components/Clients.astro` |
| Capturas de dashboards | `src/assets/work/` |
| Logo de Prometeo | `src/components/Logo.astro` y `public/favicon.svg` |

Todo lo que está entre **[corchetes]** en el sitio es un dato pendiente de confirmar.

**Propuesta comercial:** guarda el PDF como `public/Propuesta_Comercial_Prometeo.pdf`. Si usas otro nombre, cambia `proposalFile` en `site.ts`.

## Trabajar en local

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # genera /dist
npm run preview  # sirve /dist
```

## Publicar

### Opción recomendada: Cloudflare Pages o Vercel (gratis, con dominio propio y HTTPS)
1. Sube este repositorio a GitHub.
2. En Cloudflare Pages o Vercel elige **Import from GitHub** y luego este repositorio.
3. Framework: **Astro**. Build: `npm run build`. Carpeta de salida: `dist`.
4. Agrega la variable `SITE_URL` con tu dominio (por ejemplo `https://prometeo.bo`).
5. Conecta tu dominio en la sección *Custom domains*.

Cada `git push` publica la nueva versión automáticamente.

### Opción GitHub Pages (ya configurada)
1. En el repositorio entra a **Settings → Pages → Source: GitHub Actions**.
2. En **Settings → Secrets and variables → Actions → Variables** crea:
   - `SITE_URL` = `https://<usuario>.github.io` (o tu dominio)
   - `BASE_PATH` = `/<nombre-del-repo>/` (o `/` si usas dominio propio)
3. Haz push a `main`. El workflow `.github/workflows/deploy.yml` construye y publica el sitio.

## Formularios

Sin backend, el formulario de Talks abre el correo del visitante. Para recibir inscripciones sin que se abra el correo, crea un formulario gratis en [Formspree](https://formspree.io) y pega su URL en `formEndpoint` dentro de `src/data/site.ts`.
