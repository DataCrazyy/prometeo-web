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
  email: 'contacto@prometeotech.com',
  phoneDisplay: '+591 7000 0000',
  // Número en formato internacional sin "+" ni espacios
  whatsapp: '59170000000',
  linkedin: 'https://www.linkedin.com/company/prometeotech',
  // Enlace de agenda (Calendly, Google Calendar, Cal.com…). Si queda vacío, se usa WhatsApp.
  bookingUrl: '',
  // Endpoint de formularios (Formspree, Getform, Google Apps Script…). Vacío = abre el correo.
  formEndpoint: '',
  // Archivo de la propuesta comercial dentro de /public
  proposalFile: 'Propuesta_Comercial_Prometeo.pdf',
};

export const waLink = (text = 'Hola Prometeo, quiero conversar sobre un proyecto.') =>
  `https://wa.me/${site.whatsapp}?text=${encodeURIComponent(text)}`;

export const bookingLink = () => site.bookingUrl || waLink('Hola Prometeo, quiero agendar una reunión.');

export const stats = [
  { value: '+20', label: 'Dashboards en producción' },
  { value: '+10', label: 'Procesos automatizados' },
  { value: '[N]', label: 'Personas capacitadas' },
  { value: '[N]', label: 'Empresas e instituciones' },
];

export const nav = [
  { href: 'consulting/', label: 'Consulting' },
  { href: 'academy/', label: 'Academy' },
  { href: 'precio-justo/', label: 'Precio Justo' },
  { href: 'talks/', label: 'Talks' },
];
