// ─────────────────────────────────────────────────────────────
//  Cursos de Prometeo Academy. Edita precios, temarios y fechas aquí.
//  Formato común: 2 meses · 16 sesiones · 2 por semana · 1,5 h
//  (1 clase en vivo presencial + 1 clase virtual por semana)
// ─────────────────────────────────────────────────────────────

export type Session = { n: number; title: string; goals: string[] };
export type Module = { title: string; sessions: Session[] };
export type Course = {
  id: string; level: string; title: string; summary: string; icon: 'chart' | 'database' | 'bot';
  priceSolo: number; priceGroup: number; forWho: string; outcome: string; modules: Module[];
};

export const format = {
  duration: '2 meses',
  sessions: 16,
  perWeek: 2,
  hours: '1,5 h por sesión',
  mode: '1 clase en vivo + 1 clase virtual por semana',
  groupMin: 3,
};

const s = (n: number, title: string, goals: string[]): Session => ({ n, title, goals });

export const courses: Course[] = [
  {
    id: 'inicial', level: 'Inicial', icon: 'chart',
    title: 'Analítica de datos con Power BI',
    summary: 'De los datos en bruto a un dashboard publicado: Power Query, modelado, DAX, diseño y Power BI Service.',
    priceSolo: 1400, priceGroup: 800,
    forWho: 'Profesionales y estudiantes que empiezan con Power BI o lo usan sin bases sólidas.',
    outcome: 'Un proyecto final publicado en Power BI Service, con seguridad y listo para compartir.',
    modules: [
      { title: 'Módulo 1 · Fundamentos de BI y transformación de datos con Power Query', sessions: [
        s(1, 'Business Intelligence y el rol del analista', ['Qué es BI y su rol en la toma de decisiones', 'Datos, información e inteligencia de negocio', 'El rol del analista de datos en la organización', 'Panorama de herramientas BI y posición de Power BI']),
        s(2, 'Conexión a fuentes y Power Query Editor', ['Conectar Excel, CSV, bases de datos y web', 'Interfaz y flujo de trabajo de Power Query', 'Tipos de datos y configuración regional', 'Transformaciones básicas: filtros, orden y tipos']),
        s(3, 'Limpieza y transformaciones avanzadas', ['Eliminar duplicados, nulos y errores', 'Columnas condicionales, combinar y dividir', 'Consolidar archivos y carpetas', 'Parámetros para rutas dinámicas y buenas prácticas']),
        s(4, 'Taller: ingestión y limpieza de un caso real', ['Flujo completo de ingestión y limpieza', 'Revisión de buenas prácticas', 'Retroalimentación grupal']),
      ] },
      { title: 'Módulo 2 · Modelado de datos y análisis con DAX', sessions: [
        s(5, 'El modelo de datos y primeras medidas', ['Tablas calculadas, columnas calculadas y medidas', 'Sintaxis DAX y contexto de fila', 'Convenciones de nombres', 'SUM, AVERAGE, COUNT, DISTINCTCOUNT']),
        s(6, 'Relaciones y modelo estrella', ['Modelo estrella vs. modelo plano', 'Cardinalidad y dirección de filtros', 'Dimensiones y hechos', 'Relaciones inactivas con USERELATIONSHIP', 'Optimización del modelo']),
        s(7, 'DAX para KPIs y comparativos', ['Variables VAR / RETURN', 'IF, SWITCH y manejo de BLANK', 'Variaciones vs. período anterior', 'SAMEPERIODLASTYEAR y DATESYTD']),
        s(8, 'Taller: modelo completo sobre un caso real', ['Modelo estrella desde datos en bruto', 'Medidas de ventas, márgenes y comparativos', 'Errores frecuentes de modelado']),
      ] },
      { title: 'Módulo 3 · Visualización estratégica y diseño de dashboards', sessions: [
        s(9, 'Criterio visual y diseño', ['Jerarquía, contraste, alineación y proximidad', 'Color, semáforos y accesibilidad', 'Maquetar en Figma antes de construir', 'Referentes de reportes de alto impacto']),
        s(10, 'Dashboards interactivos', ['Tablas, matrices, barras, líneas y tarjetas KPI', 'Segmentadores, filtros y drill down', 'Reportes por perfil: ejecutivo, operativo, analítico', 'Narrativa visual hacia el insight clave']),
        s(11, 'Móvil, IA y visuales personalizados', ['Vista móvil con buenas prácticas', 'Cards inteligentes, IA y Q&A', 'Visuales HTML con Deneb', 'Accesibilidad y experiencia de usuario']),
        s(12, 'Taller: dashboard con enfoque narrativo', ['Diseño aplicado a un caso real', 'Iteración con retroalimentación', 'Evaluación por claridad, utilidad y estética']),
      ] },
      { title: 'Módulo 4 · Publicación, Power BI Service y proyecto final', sessions: [
        s(13, 'Publicación y ciclo de vida', ['Desktop vs. Service', 'Actualizaciones programadas', 'Workspaces y gateways on-premise']),
        s(14, 'Colaboración y distribución', ['Apps de Power BI', 'Permisos, suscripciones y alertas', 'Integración con Teams y SharePoint']),
        s(15, 'Seguridad y gobierno del dato', ['RLS estático y dinámico con USERNAME()', 'Versionado y gestión de cambios', 'Documentación y lineamientos de gobierno']),
        s(16, 'Proyecto final', ['Caso de negocio, modelo, DAX y dashboard ejecutivo', 'Publicación con seguridad', 'Presentación y retroalimentación final']),
      ] },
    ],
  },
  {
    id: 'intermedio', level: 'Intermedio', icon: 'database',
    title: 'DAX avanzado y modelado para negocio',
    summary: 'Domina CALCULATE, el contexto de filtro, el lenguaje M y el rendimiento de modelos grandes.',
    priceSolo: 1800, priceGroup: 1100,
    forWho: 'Analistas que ya construyen reportes y quieren modelos más rápidos y medidas más potentes.',
    outcome: 'Un modelo optimizado con medidas avanzadas, grupos de cálculo y análisis de negocio.',
    modules: [
      { title: 'Módulo 1 · Power Query avanzado y lenguaje M', sessions: [
        s(1, 'Lenguaje M desde el código', ['Estructura de consultas y pasos', 'Funciones personalizadas', 'Manejo de errores en M']),
        s(2, 'APIs, web y fuentes dinámicas', ['Conexión a APIs REST y paginación', 'Parámetros y fuentes dinámicas', 'Actualización incremental']),
        s(3, 'Dataflows y reutilización', ['Dataflows en Power BI Service', 'Plegado de consultas (query folding)', 'Buenas prácticas de rendimiento en M']),
        s(4, 'Taller: ETL de varias fuentes', ['Integración de ERP, Excel y API', 'Documentación del flujo']),
      ] },
      { title: 'Módulo 2 · DAX avanzado', sessions: [
        s(5, 'CALCULATE y contexto de filtro', ['Contexto de filtro vs. de fila', 'Transición de contexto', 'ALL, ALLEXCEPT, REMOVEFILTERS, KEEPFILTERS']),
        s(6, 'Iteradores y tablas virtuales', ['SUMX, AVERAGEX, RANKX', 'SUMMARIZE, ADDCOLUMNS, TOPN', 'Medidas de ranking y Pareto']),
        s(7, 'Inteligencia de tiempo personalizada', ['Calendarios fiscales y semanas', 'Acumulados, promedios móviles y YoY', 'Comparativos entre períodos personalizados']),
        s(8, 'Taller: tablero de KPIs comerciales', ['Medidas avanzadas sobre un caso real', 'Revisión de código DAX']),
      ] },
      { title: 'Módulo 3 · Modelado y rendimiento', sessions: [
        s(9, 'Modelos complejos', ['Varias tablas de hechos', 'Dimensiones de rol múltiple', 'Dimensiones lentamente cambiantes']),
        s(10, 'Grupos de cálculo y parámetros', ['Calculation groups con Tabular Editor', 'Parámetros de campo', 'Formato dinámico de medidas']),
        s(11, 'Optimización', ['Performance Analyzer y DAX Studio', 'Motor VertiPaq y cardinalidad', 'Agregaciones y modos de almacenamiento']),
        s(12, 'Taller: optimizar un modelo lento', ['Diagnóstico y plan de mejora', 'Medición antes y después']),
      ] },
      { title: 'Módulo 4 · Análisis para el negocio', sessions: [
        s(13, 'Análisis avanzado', ['Escenarios what-if', 'Segmentación ABC y RFM', 'Pronósticos']),
        s(14, 'Reportes paginados y exportación', ['Power BI Report Builder', 'Reportes operativos imprimibles']),
        s(15, 'Storytelling avanzado', ['Marcadores, navegación y tooltips de página', 'Diseño de experiencia por usuario']),
        s(16, 'Proyecto final', ['Modelo optimizado con medidas avanzadas', 'Presentación ejecutiva']),
      ] },
    ],
  },
  {
    id: 'avanzado', level: 'Avanzado', icon: 'bot',
    title: 'BI corporativo, automatización e IA',
    summary: 'Arquitectura con Microsoft Fabric, automatización, Python e IA aplicada, y gobierno de BI a escala.',
    priceSolo: 2300, priceGroup: 1400,
    forWho: 'Líderes de BI y analistas senior que llevan Power BI a toda la organización.',
    outcome: 'Una solución de BI corporativa automatizada, con IA aplicada y modelo de gobierno.',
    modules: [
      { title: 'Módulo 1 · Arquitectura de datos y Microsoft Fabric', sessions: [
        s(1, 'Arquitectura BI moderna', ['Data warehouse, lakehouse y capa semántica', 'Cuándo usar cada enfoque']),
        s(2, 'Microsoft Fabric en la práctica', ['Lakehouse, pipelines y notebooks', 'Direct Lake']),
        s(3, 'SQL para analistas', ['Consultas, joins y vistas', 'Modelado dimensional en SQL']),
        s(4, 'Taller: arquitectura de un caso real', ['Diseño de punta a punta', 'Retroalimentación grupal']),
      ] },
      { title: 'Módulo 2 · Automatización', sessions: [
        s(5, 'Power Automate con Power BI', ['Alertas y flujos automáticos', 'Envío programado de reportes']),
        s(6, 'Python en Power BI', ['Limpieza y análisis con pandas', 'Scripts y visuales con Python']),
        s(7, 'Despliegue y versionado', ['Deployment pipelines', 'Proyectos PBIP con Git']),
        s(8, 'Taller: reporte que se actualiza y se envía solo', ['Automatización completa de un reporte']),
      ] },
      { title: 'Módulo 3 · IA aplicada a BI', sessions: [
        s(9, 'Copilot en Power BI', ['Generar reportes y medidas con IA', 'Buenas prácticas y límites']),
        s(10, 'Visuales de IA', ['Influenciadores clave y árbol de descomposición', 'Detección de anomalías']),
        s(11, 'Modelos predictivos', ['Pronóstico y clasificación con Python', 'Integrar predicciones al modelo']),
        s(12, 'Taller: analítica predictiva', ['Caso de negocio con predicción']),
      ] },
      { title: 'Módulo 4 · Gobierno y BI corporativo', sessions: [
        s(13, 'Seguridad avanzada', ['RLS y OLS a escala', 'Estrategia de workspaces y licencias']),
        s(14, 'Distribución y embebido', ['Power BI Embedded', 'Apps y audiencias']),
        s(15, 'Adopción y centro de excelencia', ['Métricas de uso', 'Lineamientos y formación interna']),
        s(16, 'Proyecto final', ['Solución corporativa de punta a punta', 'Presentación ante el grupo']),
      ] },
    ],
  },
];

// Historial de cursos dictados y alianzas (edita y agrega)
export const history = [
  { status: 'Próximamente', title: 'Nueva cohorte · Analista de datos con Power BI + Inteligencia Artificial', place: 'Santa Cruz · en vivo + virtual', when: 'Este 2026', upcoming: true, cert: true },
  { status: 'En curso', title: 'Experto en análisis de datos con Power BI (posgrado)', place: 'Universidad Autónoma Gabriel René Moreno (UAGRM)', when: '2026', ally: true },
  { status: 'En curso', title: 'Análisis de datos con Python (posgrado)', place: 'Universidad Católica Boliviana (UCB)', when: '2026', ally: true },
  { status: 'In-company', title: 'Capacitación en Power BI', place: 'Industrias Venado', when: '2025' },
  { status: 'In-company', title: 'Capacitación en Power BI', place: 'Nexocorp', when: '2024' },
];

export const bs = (n: number) => `Bs ${String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.')}`;

// Preguntas frecuentes de Academy (lo que está entre [corchetes] falta confirmar)
export const faqs = [
  { q: '¿Necesito saber Power BI para el curso Inicial?', a: 'No. Empezamos desde cero; basta con manejar Excel a nivel básico.' },
  { q: '¿Qué computadora necesito?', a: 'Una laptop con Windows, porque Power BI Desktop solo funciona en Windows. Si usas Mac, te ayudamos a instalarlo con una máquina virtual.' },
  { q: '¿Cómo son las clases en vivo y virtuales?', a: 'Cada semana hay una clase en vivo presencial en [lugar en Santa Cruz] y una clase virtual por [Zoom / Google Meet], de 1,5 horas cada una.' },
  { q: '¿Qué pasa si falto a una clase?', a: 'No te pierdes nada: todas las clases quedan grabadas en una carpeta de Google Drive junto con el material de cada sesión, y puedes consultar tus dudas en el grupo del curso.' },
  { q: '¿Entregan certificado?', a: 'Sí. Al aprobar el proyecto final recibes un certificado de Prometeo Academy [digital y verificable].' },
  { q: '¿Cómo funciona el precio de grupo?', a: 'Desde 3 personas de la misma empresa o institución, cada una paga el precio de grupo. Por ejemplo, en el curso Inicial son Bs 800 por persona en lugar de Bs 1.400.' },
  { q: '¿Cómo pago?', a: 'Por QR o transferencia bancaria. Al inscribirte te enviamos los datos de pago por WhatsApp.' },
  { q: '¿Pueden dictar el curso en mi empresa o universidad?', a: 'Sí. Con Prometeo Enterprise y Prometeo Student adaptamos el programa, el horario y los casos a tu institución.' },
];
