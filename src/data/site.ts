import { url } from '../lib/url';

// ─────────────────────────────────────────────────────────────
//  Datos editables del sitio. Cambia aquí y se actualiza en todas las páginas.
//  Todo lo que está entre [corchetes] es un dato pendiente de confirmar.
// ─────────────────────────────────────────────────────────────

export const site = {
  name: 'Prometeo',
  tagline: 'Datos, formación y tecnología para decidir mejor',
  description:
    'Prometeo reúne consultoría en Business Intelligence, cursos de Power BI, inteligencia de precios y eventos sobre datos e IA desde Santa Cruz de la Sierra, Bolivia.',
  city: 'Santa Cruz de la Sierra, Bolivia',
  email: 'techprometeo@gmail.com',
  phoneDisplay: '+591 782 33445',
  // Número en formato internacional sin "+" ni espacios
  whatsapp: '59178233445',
  // Página de empresa en LinkedIn (vacío = no se muestra)
  linkedin: '',
  // Cuenta de Instagram, p. ej. 'https://www.instagram.com/prometeo.bo/' (vacío = no se muestra)
  instagram: '',
  // Enlace de agenda (Calendly, Google Calendar, Cal.com…). Si queda vacío, se usa WhatsApp.
  bookingUrl: '',
  // URL del Apps Script que guarda cada contacto en Google Sheets (ver tools/leads/README.md).
  // Vacío = los formularios solo abren WhatsApp con el mensaje listo.
  formEndpoint: '',
  // Plataforma pública de Precios Claros
  preciosClarosUrl: 'https://datacrazyy.github.io/price-intelligence-backend/',
  // Archivo de la propuesta comercial dentro de /public
  // Tiempo de respuesta que prometemos en el formulario de contacto
  responseTime: 'durante el día',
  proposalFile: 'Propuesta_Comercial_Prometeo_Consulting.pdf',
};

export const waLink = (text = 'Hola Prometeo, quiero conversar sobre un proyecto.') =>
  `https://wa.me/${site.whatsapp}?text=${encodeURIComponent(text)}`;

// "Agendar reunión" lleva al formulario de contacto con la reunión marcada, para tener los datos del cliente.
// Si algún día usan Calendly/Cal.com, pongan el enlace en bookingUrl.
export const bookingLink = (tema?: string) =>
  site.bookingUrl || url(`contacto/?reunion=1${tema ? `&tema=${tema}` : ''}`);

// count = número para la animación; deja count vacío si el dato aún no está confirmado
export const stats = [
  { count: 20, prefix: '+', label: 'Dashboards en producción' },
  { count: 10, prefix: '+', label: 'Procesos automatizados' },
  { count: 40, prefix: '', label: 'Personas capacitadas', academy: true },
  { count: 3, prefix: '', label: 'Empresas capacitadas', academy: true },
  { count: 2, prefix: '', label: 'Universidades aliadas', academy: true },
];

// Líneas de Prometeo (Precios Claros va aparte en el menú, como proyecto)
export const nav = [
  { key: 'consulting', href: 'consulting/', label: 'Consulting' },
  { key: 'academy', href: 'academy/', label: 'Academy' },
  { key: 'talks', href: 'talks/', label: 'Talks' },
  { key: 'nosotros', href: 'nosotros/', label: 'Nosotros' },
];
