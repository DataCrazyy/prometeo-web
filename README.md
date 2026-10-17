# Prometeo · sitio web

Sitio oficial de **Prometeo**, la marca que agrupa:

| Línea | Página | Qué es |
|---|---|---|
| Prometeo Consulting | `/consulting` | Asesorías de Business Intelligence y Power BI, con modalidades, propuesta comercial y cronograma |
| Prometeo Academy | `/academy` | Cursos y capacitaciones (Student, Enterprise, abiertos) |
| Prometeo Talks | `/talks` | Conferencias, eventos y videos (próximamente, con lista de espera) |
| **Precios Claros by Prometeo** | `/precios-claros` | Proyecto aparte: comparador y monitoreo de precios con web scraping |

Cada página tiene su color: Prometeo y Consulting en violeta, Academy en azul, Talks en naranja y Precios Claros en verde (`data-theme` en `src/styles/global.css`).

## Stack

- **[Astro 5](https://astro.build)**: genera HTML estático, rápido y bueno para SEO, sin frameworks pesados.
- **CSS propio** con los colores y tipografías originales (Sora + Inter, violeta `#7C4DFF`), en `src/styles/global.css`.
- **Fuentes alojadas en el propio sitio** (`@fontsource`), sin depender de Google Fonts.
- **Imágenes optimizadas** automáticamente a WebP con `astro:assets`.
- **Interacción tipo Apple:** [GSAP + ScrollTrigger](https://gsap.com) con el scroll nativo del navegador (sin retraso): titulares que aparecen palabra por palabra, secciones fijas al hacer scroll, contadores y tarjetas con efecto 3D (`src/scripts/motion.ts`). Si el visitante pide menos movimiento en su sistema, todo se muestra quieto.
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
| Cursos, precios, temarios e historial | `src/data/courses.ts` |
| Logos de clientes | `src/assets/clients/` + `src/components/Clients.astro` |
| Capturas de dashboards | `src/assets/work/` |
| Logos de Prometeo y sus líneas | `src/lib/brandIcons.ts` (íconos), `src/components/Logo.astro` y `Mark.astro`; archivos en `public/brand/` |
| Cuenta de Instagram / LinkedIn | `src/data/site.ts` → `instagram`, `linkedin` |

Todo lo que está entre **[corchetes]** en el sitio es un dato pendiente de confirmar.

**Propuesta comercial:** el PDF está en `public/Propuesta_Comercial_Prometeo_Consulting.pdf`. En la web, antes de descargarla, la persona deja su nombre, empresa y WhatsApp: el navegador completa "Preparada para", "Contacto" y la fecha de hoy en la portada (`src/scripts/proposal.ts`) y, si `formEndpoint` está configurado, guarda el contacto en Google Sheets. Para regenerarlo después de editar textos o precios:

```bash
pip install reportlab
python tools/propuesta/make_proposal.py public/Propuesta_Comercial_Prometeo_Consulting.pdf
```

## Marca

Los logos de las cinco marcas (Prometeo, Consulting, Academy, Talks y Precios Claros) están en `public/brand/<marca>/` en SVG y PNG, con versiones para fondo claro y oscuro, y las piezas de Instagram en `public/brand/instagram/`. Cada página usa el logo, el favicon y la imagen para compartir de su línea. Para regenerarlos:

```bash
pip install fonttools brotli playwright
python tools/brand/make_brand.py   # logos e Instagram
python tools/brand/make_og.py      # favicons e imágenes para compartir
```

**Temarios de Academy en PDF:** `public/academy/Temario_<Nivel>_Prometeo_Academy.pdf`. Si cambias un temario en `src/data/courses.ts`, regenera los PDF:

```bash
npx esbuild src/data/courses.ts --format=cjs --outfile=/tmp/courses.cjs
node -e "const c=require('/tmp/courses.cjs');require('fs').writeFileSync('/tmp/courses.json',JSON.stringify({courses:c.courses,format:c.format}))"
python tools/academy/make_syllabi.py /tmp/courses.json public/academy
```

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

## Formularios y contactos

Todos los botones "Agendar reunión", "Cotizar" e "Inscribirme" llevan a un formulario, así siempre quedan los datos del cliente:

- **Contacto / reunión** (`/contacto/`): tema, nombre, cargo, empresa, correo, WhatsApp, cómo nos conoció y, si quiere reunión, día, horario y modalidad.
- **Inscripción a cursos** (Academy): curso, individual o grupo, cantidad de personas, forma de pago y total.
- **Lista de espera de Talks.**

Al enviar se abre WhatsApp con el mensaje ya escrito. Para **guardar además cada contacto en Google Sheets**
(y recibir un aviso por correo), sigan `tools/leads/README.md` y peguen la URL en `formEndpoint` de `src/data/site.ts`.
