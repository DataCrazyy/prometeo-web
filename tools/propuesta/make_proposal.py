"""Genera la propuesta comercial estándar de Prometeo Consulting (PDF)."""
import os, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, NextPageTemplate, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
F = os.path.join(HERE, 'fonts')
for name, file in [('Sora', 'sora-400'), ('Sora-Bold', 'sora-700'), ('Sora-Black', 'sora-800'),
                   ('Inter', 'inter-400'), ('Inter-Semi', 'inter-600'), ('Inter-Bold', 'inter-700')]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(F, file + '.ttf')))

PURPLE = colors.HexColor('#7C4DFF'); PDARK = colors.HexColor('#5E35B1'); PDEEP = colors.HexColor('#3D1E9E')
PSOFT = colors.HexColor('#B39DFF'); PLIGHT = colors.HexColor('#EDE7F6'); TINT = colors.HexColor('#F4F1FC')
INK = colors.HexColor('#1A0E3B'); INK2 = colors.HexColor('#2D1566'); CHAR = colors.HexColor('#1E1B2E')
GRAY = colors.HexColor('#5F5F6B'); LINE = colors.HexColor('#E4DDF6')

W, H = A4
M = 20 * mm

st = {
    'h1': ParagraphStyle('h1', fontName='Sora-Black', fontSize=24, leading=29, textColor=CHAR, spaceAfter=4),
    'eyebrow': ParagraphStyle('eb', fontName='Inter-Bold', fontSize=8.5, leading=11, textColor=PDARK, spaceAfter=6),
    'h2': ParagraphStyle('h2', fontName='Sora-Bold', fontSize=13, leading=17, textColor=CHAR, spaceBefore=10, spaceAfter=4),
    'body': ParagraphStyle('body', fontName='Inter', fontSize=10, leading=15, textColor=GRAY, spaceAfter=6),
    'bodyd': ParagraphStyle('bodyd', fontName='Inter', fontSize=10, leading=15, textColor=CHAR),
    'small': ParagraphStyle('small', fontName='Inter', fontSize=8.5, leading=12, textColor=GRAY),
    'cellh': ParagraphStyle('cellh', fontName='Inter-Bold', fontSize=9, leading=12, textColor=colors.white),
    'cell': ParagraphStyle('cell', fontName='Inter', fontSize=9, leading=13, textColor=CHAR),
    'cellb': ParagraphStyle('cellb', fontName='Inter-Semi', fontSize=9.5, leading=13, textColor=CHAR),
    'price': ParagraphStyle('price', fontName='Sora-Black', fontSize=17, leading=21, textColor=PDARK),
    'bullet': ParagraphStyle('bullet', fontName='Inter', fontSize=10, leading=15, textColor=CHAR, leftIndent=12, bulletIndent=0, spaceAfter=3),
}

def P(t, s='body'): return Paragraph(t, st[s])
def bullets(items, s='bullet'): return [Paragraph(i, st[s], bulletText='•') for i in items]


# Símbolo "llama de datos" (mismo dibujo que src/components/Mark.astro, en una grilla de 64)
MARK_BARS = [(17, 54.5, 30), (11, 46, 42), (11, 37.5, 42), (16, 29, 34), (23, 20.5, 24), (30, 12, 13)]
MARK_COLS = ['#3D1E9E', '#5E35B1', '#7C4DFF', '#A35CF5', '#E0609A', '#FF7A3D']
def draw_mark(c, x, y, size, light=False):
    """Dibuja el símbolo con la esquina inferior izquierda en (x, y)."""
    k = size / 64
    for (bx, by, bw), col in zip(MARK_BARS, MARK_COLS):
        hex_ = col
        if light and col in ('#3D1E9E', '#5E35B1'): hex_ = '#9B6EFF' if col == '#5E35B1' else '#7C4DFF'
        c.setFillColor(colors.HexColor(hex_))
        c.roundRect(x + bx * k, y + (64 - by - 6.5) * k, bw * k, 6.5 * k, 3.25 * k, stroke=0, fill=1)
    c.setFillColor(colors.HexColor('#FFA94D'))
    c.circle(x + 38.5 * k, y + (64 - 5.5) * k, 3.4 * k, stroke=0, fill=1)

# Ícono de Prometeo Consulting (mismo que src/lib/brandIcons.ts): barras que crecen + tendencia + chispa
CONS_H = [12, 19, 15, 26, 33, 41]
CONS_COLS = ['#3D1E9E', '#5E35B1', '#7C4DFF', '#9B6EFF', '#B39DFF', '#D0BFFF']
def draw_consulting(c, x, y, size, light=False):
    k = size / 64
    for i, (h, col) in enumerate(zip(CONS_H, CONS_COLS)):
        if light and i < 2: col = ['#7C4DFF', '#9B6EFF'][i]
        c.setFillColor(colors.HexColor(col))
        c.roundRect(x + (7 + i * 8.6) * k, y + (64 - 59) * k, 6.6 * k, h * k, 3.3 * k, stroke=0, fill=1)
    pts = [(7 + i * 8.6 + 3.3, 59 - h - 6) for i, h in enumerate(CONS_H[:5])] + [(59, 5.5)]
    c.setStrokeColor(colors.HexColor('#FFA94D')); c.setLineWidth(2.4 * k); c.setLineCap(1); c.setLineJoin(1)
    pth = c.beginPath(); pth.moveTo(x + pts[0][0] * k, y + (64 - pts[0][1]) * k)
    for px, py in pts[1:]: pth.lineTo(x + px * k, y + (64 - py) * k)
    c.drawPath(pth, stroke=1, fill=0)
    c.setFillColor(colors.HexColor('#FFA94D')); c.circle(x + 59 * k, y + (64 - 5.5) * k, 3.8 * k, stroke=0, fill=1)

# ── Fondos de página ──
def cover(c, d):
    c.saveState()
    steps = 60
    for i in range(steps):
        t = i / steps
        r = 0x1A + (0x2D - 0x1A) * (1 - abs(t - .5) * 2)
        g = 0x0E + (0x15 - 0x0E) * (1 - abs(t - .5) * 2)
        b = 0x3B + (0x66 - 0x3B) * (1 - abs(t - .5) * 2)
        c.setFillColorRGB(r / 255, g / 255, b / 255)
        c.rect(0, H - (i + 1) * H / steps, W, H / steps + 1, stroke=0, fill=1)
    c.setStrokeColor(colors.Color(124/255, 77/255, 1, alpha=.25)); c.setLineWidth(1)
    c.circle(W - 30 * mm, H - 40 * mm, 110 * mm, stroke=1, fill=0)
    c.circle(W - 10 * mm, H - 70 * mm, 75 * mm, stroke=1, fill=0)
    # Marca
    draw_consulting(c, M - 1 * mm, H - 40 * mm, 17 * mm, light=True)
    c.setFillColor(colors.white); c.setFont('Sora-Bold', 18); c.drawString(M + 18 * mm, H - 32.5 * mm, 'prometeo')
    c.setFillColor(PSOFT); c.setFont('Sora', 15); c.drawString(M + 18 * mm, H - 38.5 * mm, 'consulting')
    # Título
    c.setFillColor(PSOFT); c.setFont('Inter-Bold', 10); c.drawString(M, H - 120 * mm, 'PROPUESTA COMERCIAL')
    c.setFillColor(colors.white); c.setFont('Sora-Black', 38)
    c.drawString(M, H - 137 * mm, 'Business Intelligence')
    c.drawString(M, H - 152 * mm, 'con Power BI')
    c.setFillColor(colors.Color(1, 1, 1, alpha=.75)); c.setFont('Inter', 12)
    c.drawString(M, H - 166 * mm, 'Transformamos datos en decisiones inteligentes.')
    # Ficha
    y = 70 * mm
    c.setFillColor(colors.Color(1, 1, 1, alpha=.08)); c.roundRect(M, y - 6 * mm, W - 2 * M, 38 * mm, 5 * mm, stroke=0, fill=1)
    # Preparada para, Contacto y Fecha quedan vacíos: la web los completa con los datos de cada persona (src/scripts/proposal.ts)
    labels = [('Preparada para', ''), ('Contacto', ''), ('Fecha', ''), ('Validez', '30 días')]
    cw = (W - 2 * M) / 2
    for i, (k, v) in enumerate(labels):
        x = M + 8 * mm + (i % 2) * cw
        yy = y + 22 * mm - (i // 2) * 15 * mm
        c.setFillColor(PSOFT); c.setFont('Inter-Bold', 8); c.drawString(x, yy, k.upper())
        c.setFillColor(colors.white); c.setFont('Inter-Semi', 11); c.drawString(x, yy - 6 * mm, v)
    c.setFillColor(colors.Color(1, 1, 1, alpha=.55)); c.setFont('Inter', 8.5)
    c.drawString(M, 22 * mm, 'techprometeo@gmail.com  ·  +591 782 33445  ·  Santa Cruz de la Sierra, Bolivia')
    c.restoreState()

def inner(c, d):
    c.saveState()
    c.setFillColor(PURPLE); c.rect(0, H - 6, W, 6, stroke=0, fill=1)
    draw_consulting(c, M - .5 * mm, H - 16 * mm, 7.5 * mm)
    c.setFillColor(CHAR); c.setFont('Sora-Bold', 9.5); c.drawString(M + 8 * mm, H - 13 * mm, 'prometeo')
    c.setFillColor(PURPLE); c.setFont('Sora', 9.5); c.drawString(M + 8 * mm + c.stringWidth('prometeo ', 'Sora-Bold', 9.5), H - 13 * mm, 'consulting')
    c.setFillColor(GRAY); c.setFont('Inter', 8); c.drawRightString(W - M, H - 13 * mm, 'Propuesta comercial · Business Intelligence')
    c.setStrokeColor(LINE); c.setLineWidth(.6); c.line(M, 14 * mm, W - M, 14 * mm)
    c.setFont('Inter', 8); c.setFillColor(GRAY)
    c.drawString(M, 9 * mm, 'Documento confidencial · Solo para uso comercial')
    c.drawRightString(W - M, 9 * mm, f'{d.page}')
    c.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=24 * mm, bottomMargin=22 * mm,
                      title='Propuesta comercial · Prometeo Consulting', author='Prometeo', subject='Business Intelligence con Power BI')
frame = Frame(M, 22 * mm, W - 2 * M, H - 46 * mm, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate('cover', frames=[frame], onPage=cover), PageTemplate('inner', frames=[frame], onPage=inner)])

def card_table(rows, widths, head=True, zebra=True):
    t = Table(rows, colWidths=widths, repeatRows=1 if head else 0)
    style = [
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -1), .5, LINE),
    ]
    if head: style += [('BACKGROUND', (0, 0), (-1, 0), INK2)]
    if zebra:
        for r in range(1 if head else 0, len(rows)):
            if r % 2 == 0: style.append(('BACKGROUND', (0, r), (-1, r), TINT))
    t.setStyle(TableStyle(style))
    return t

story = [NextPageTemplate('inner'), PageBreak()]

# ── 1. Sobre nosotros y alcance ──
story += [P('1 · QUIÉNES SOMOS', 'eyebrow'), P('Datos que se convierten en decisiones', 'h1'),
          P('Prometeo Consulting implementa soluciones de Business Intelligence con Power BI para empresas que quieren dejar los reportes manuales y decidir con información confiable y a tiempo. Hemos puesto en producción más de 20 dashboards y automatizado más de 10 procesos de reporte en áreas comerciales, financieras y de distribución.'),
          Spacer(1, 6), P('Qué resolvemos', 'h2')]
story += bullets(['Reportes que se arman a mano en Excel cada semana o cada mes.',
                  'Datos dispersos en ERP, CRM, bases de datos y planillas que no se cruzan.',
                  'Gerencia sin una vista única y actualizada de sus indicadores clave.',
                  'Equipos que tienen Power BI pero no lo aprovechan.'])
story += [Spacer(1, 4), P('2 · ALCANCE DEL SERVICIO', 'eyebrow'), P('Qué incluye un proyecto', 'h2')]
services = [
    ('Dashboards ejecutivos', 'KPIs estratégicos, tendencias y alertas para la gerencia.'),
    ('Automatización de reportes', 'Conexiones automáticas y actualización programada.'),
    ('Modelado de datos', 'Modelo estrella y medidas DAX optimizadas.'),
    ('Integración de sistemas', 'SAP, SQL Server, Oracle, APIs y Excel en un solo modelo.'),
    ('Gobierno de datos', 'Seguridad por rol (RLS), permisos y documentación técnica.'),
    ('Capacitación y soporte', 'Formación a usuarios y acompañamiento posterior.'),
]
rows = [[P('Servicio', 'cellh'), P('Descripción', 'cellh')]] + [[P(a, 'cellb'), P(b, 'cell')] for a, b in services]
story.append(card_table(rows, [55 * mm, W - 2 * M - 55 * mm]))

# ── 2. Metodología ──
story += [PageBreak(), P('3 · METODOLOGÍA', 'eyebrow'), P('Seis etapas, entregas validadas', 'h1'),
          P('Trabajamos de forma colaborativa: cada etapa termina con una validación de tu equipo antes de pasar a la siguiente.')]
method = [
    ('1', 'Descubrimiento', 'Reuniones y entrevistas para entender el negocio, los procesos y las necesidades de información.'),
    ('2', 'Diseño funcional', 'Definición de KPIs, bocetos (wireframes) de los dashboards y catálogo de requerimientos validado.'),
    ('3', 'Desarrollo', 'Modelo de datos, medidas DAX, conexión de fuentes y construcción del dashboard en Power BI.'),
    ('4', 'Validación', 'Revisión conjunta para asegurar la precisión de los datos y la funcionalidad.'),
    ('5', 'Implementación', 'Publicación en el servicio Power BI, capacitación de usuarios y entrega de manuales.'),
    ('6', 'Soporte', 'Acompañamiento, ajustes, monitoreo y evolución continua de la solución.'),
]
rows = [[P('#', 'cellh'), P('Etapa', 'cellh'), P('Qué hacemos', 'cellh')]] + [[P(f'<font name="Sora-Black" color="#7C4DFF">{n}</font>', 'cell'), P(t, 'cellb'), P(d, 'cell')] for n, t, d in method]
story.append(card_table(rows, [12 * mm, 38 * mm, W - 2 * M - 50 * mm]))
story += [Spacer(1, 12), P('4 · CRONOGRAMA ESTIMADO', 'eyebrow'), P('Un proyecto completo toma en promedio 6 semanas', 'h2')]
gantt = [('Descubrimiento', [1, 2]), ('Documentación', [2, 3]), ('Diseño funcional', [2, 3]), ('Desarrollo', [3, 4, 5]),
         ('Validación', [4, 5]), ('Implementación', [5, 6]), ('Capacitación', [6])]
rows = [[P('Actividad', 'cellh')] + [P(f'S{w}', 'cellh') for w in range(1, 7)]]
for name, ws in gantt: rows.append([P(name, 'cellb')] + ['' for _ in range(6)])
gw = (W - 2 * M - 48 * mm) / 6
t = Table(rows, colWidths=[48 * mm] + [gw] * 6)
gs = [('BACKGROUND', (0, 0), (-1, 0), INK2), ('LINEBELOW', (0, 0), (-1, -1), .5, LINE), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
      ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6), ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
      ('LINEBEFORE', (1, 1), (-1, -1), .5, LINE)]
shades = ['#7C4DFF', '#5E35B1', '#3D1E9E', '#9B6EFF', '#7C4DFF', '#B39DFF', '#D6C8FF']
for r, (name, ws) in enumerate(gantt, start=1):
    for w in ws:
        gs.append(('BACKGROUND', (w, r), (w, r), colors.HexColor(shades[r - 1])))
t.setStyle(TableStyle(gs)); story.append(t)
story.append(Spacer(1, 4)); story.append(P('El cronograma final se ajusta según el alcance definido en la sesión de exploración.', 'small'))

# ── 3. Entregables e inversión ──
story += [PageBreak(), P('5 · ENTREGABLES', 'eyebrow'), P('Lo que recibes al finalizar', 'h1')]
deliv = [('Documento funcional', 'KPIs, reglas de negocio y fuentes acordadas.'), ('Modelo de datos', 'Modelo estrella documentado y medidas DAX.'),
         ('Dashboard en Power BI', 'Reportes interactivos publicados en el servicio.'), ('Manual de usuario', 'Guía de uso y navegación.'),
         ('Capacitación', 'Sesiones prácticas con los usuarios clave.'), ('Soporte post-entrega', 'Acompañamiento durante la adopción.')]
rows = [[P(a, 'cellb'), P(b, 'cell')] for a, b in deliv]
story.append(card_table(rows, [55 * mm, W - 2 * M - 55 * mm], head=False))
story += [Spacer(1, 12), P('6 · MODALIDADES E INVERSIÓN', 'eyebrow'), P('Elige cómo trabajar con nosotros', 'h2')]
def plan(label, name, price, period, items, featured=False):
    bg = INK2 if featured else TINT
    fg = 'white' if featured else '#1E1B2E'
    sub = '#B39DFF' if featured else '#5E35B1'
    inner_rows = [[Paragraph(f'<font color="{sub}">{label.upper()}</font>', ParagraphStyle('x', fontName='Inter-Bold', fontSize=7.5, leading=10))],
                  [Paragraph(f'<font color="{fg}">{name}</font>', ParagraphStyle('x', fontName='Sora-Bold', fontSize=11.5, leading=14))],
                  [Paragraph(f'<font color="{"#FFFFFF" if featured else "#5E35B1"}">{price}</font>', st['price'])],
                  [Paragraph(f'<font color="{"#D6C8FF" if featured else "#5F5F6B"}">{period}</font>', st['small'])]]
    for it in items:
        inner_rows.append([Paragraph(f'<font color="{fg}">•  {it}</font>', ParagraphStyle('x', fontName='Inter', fontSize=8.5, leading=12))])
    t = Table(inner_rows, colWidths=[(W - 2 * M - 8 * mm) / 3 - 2 * mm])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), bg), ('LEFTPADDING', (0, 0), (-1, -1), 9), ('RIGHTPADDING', (0, 0), (-1, -1), 9),
                           ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                           ('TOPPADDING', (0, 0), (-1, 0), 10), ('BOTTOMPADDING', (0, -1), (-1, -1), 10), ('ROUNDEDCORNERS', [8, 8, 8, 8])]))
    return t
plans = Table([[
    plan('Bajo demanda', 'Desarrollo por horas', 'Bs 200', 'por hora de trabajo', ['Nuevos dashboards e indicadores', 'Cambios y automatizaciones', 'Optimización DAX']),
    plan('Recomendado', 'Implementación de proyecto', 'Desde Bs 4.000', 'por proyecto · según alcance', ['Solución completa en ~6 semanas', 'Incluye 2 meses de soporte', 'Documentación y capacitación'], True),
    plan('Opcional', 'Soporte mensual', 'Bs 500', 'por mes · desde el 3.er mes', ['Soporte remoto y ajustes', 'Revisión mensual', 'Atención prioritaria']),
]], colWidths=[(W - 2 * M) / 3] * 3)
plans.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 2), ('RIGHTPADDING', (0, 0), (-1, -1), 2)]))
story.append(plans)
story += [Spacer(1, 8), P('Condiciones generales', 'h2')]
story += bullets(['Precios en bolivianos (Bs). La implementación incluye 2 meses obligatorios de soporte a Bs 500/mes.',
                  'No incluye licencias de Microsoft Power BI (Pro / Premium), que contrata el cliente.',
                  'Forma de pago: QR o transferencia bancaria, [50 % al inicio y 50 % a la entrega].',
                  'El alcance definitivo y la inversión final se confirman tras la sesión de exploración.'])

# ── 4. Próximos pasos ──
story += [PageBreak(), P('7 · PRÓXIMOS PASOS', 'eyebrow'), P('Empecemos con una sesión de exploración', 'h1'),
          P('Esta es nuestra propuesta estándar. Para adaptarla a tu empresa, agendamos una sesión de exploración: conversamos sobre tus objetivos, tus fuentes de datos y las decisiones que necesitas tomar.')]
nxt = [('1', 'Sesión de exploración', '[60] minutos, presencial o virtual. Revisamos objetivos, áreas y fuentes de datos.'),
       ('2', 'Propuesta ajustada', 'Te enviamos alcance, cronograma e inversión definitivos en [3] días hábiles.'),
       ('3', 'Inicio del proyecto', 'Firmamos, agendamos la reunión de arranque y comenzamos con el descubrimiento.')]
rows = [[P(f'<font name="Sora-Black" size="18" color="#7C4DFF">{n}</font>', 'cell'), [P(t, 'cellb'), P(d, 'cell')]] for n, t, d in nxt]
story.append(card_table(rows, [16 * mm, W - 2 * M - 16 * mm], head=False, zebra=False))
story += [Spacer(1, 14)]
contact = Table([[Paragraph('<font color="#FFFFFF" name="Sora-Bold" size="14">Agenda tu sesión de exploración</font><br/><br/>'
                            '<font color="#D6C8FF">Correo: techprometeo@gmail.com<br/>WhatsApp: +591 782 33445<br/>Respondemos durante el día<br/>Web: [prometeo.dominio]<br/>Santa Cruz de la Sierra, Bolivia</font>',
                            ParagraphStyle('c', fontName='Inter', fontSize=10, leading=15))]], colWidths=[W - 2 * M])
contact.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), INK2), ('LEFTPADDING', (0, 0), (-1, -1), 16), ('TOPPADDING', (0, 0), (-1, -1), 16),
                             ('BOTTOMPADDING', (0, 0), (-1, -1), 16), ('ROUNDEDCORNERS', [10, 10, 10, 10])]))
story.append(contact)
story += [Spacer(1, 26), P('Aceptación de la propuesta', 'h2')]
sig = Table([[P('_______________________________', 'cell'), P('_______________________________', 'cell')],
             [P('Por el cliente<br/>Nombre, cargo y fecha', 'small'), P('Por Prometeo Consulting<br/>Nombre, cargo y fecha', 'small')]],
            colWidths=[(W - 2 * M) / 2] * 2)
sig.setStyle(TableStyle([('TOPPADDING', (0, 0), (-1, 0), 24)]))
story.append(sig)

doc.build(story)
print('ok', OUT)
