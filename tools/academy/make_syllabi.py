"""Temarios en PDF de Prometeo Academy (uno por curso), con el diseño de la marca.

Uso:
  npx esbuild src/data/courses.ts --format=cjs --outfile=/tmp/courses.cjs
  node -e "const c=require('/tmp/courses.cjs');require('fs').writeFileSync('/tmp/courses.json',JSON.stringify({courses:c.courses,format:c.format}))"
  python tools/academy/make_syllabi.py /tmp/courses.json public/academy
Genera public/academy/Temario_<Nivel>_Prometeo_Academy.pdf
"""
import json, os, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, KeepTogether, NextPageTemplate, PageBreak
from reportlab.lib.styles import ParagraphStyle

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.join(ROOT, 'tools', 'propuesta', 'fonts')
for name, file in [('Sora', 'sora-400'), ('Sora-Bold', 'sora-700'), ('Sora-Black', 'sora-800'), ('Inter', 'inter-400'), ('Inter-Semi', 'inter-600'), ('Inter-Bold', 'inter-700')]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(F, file + '.ttf')))

data = json.load(open(sys.argv[1], encoding='utf-8')); OUTDIR = sys.argv[2]; os.makedirs(OUTDIR, exist_ok=True)
FMT = data['format']
W, H = A4; M = 20 * mm
INK = colors.HexColor('#0A1236'); INK2 = colors.HexColor('#18286E'); BLUE = colors.HexColor('#3B5BDB'); BLUE_D = colors.HexColor('#2F4AC0')
SOFT = colors.HexColor('#91A7FF'); PALE = colors.HexColor('#E7ECFF'); TINT = colors.HexColor('#F1F4FF'); CHAR = colors.HexColor('#1A1033'); MUTED = colors.HexColor('#5F5F6B')
SPARK = colors.HexColor('#FFA94D')

st = {
    'h2': ParagraphStyle('h2', fontName='Sora-Bold', fontSize=17, leading=21, textColor=CHAR, spaceBefore=4, spaceAfter=6),
    'k': ParagraphStyle('k', fontName='Inter-Bold', fontSize=8, leading=10, textColor=BLUE, spaceAfter=3),
    'body': ParagraphStyle('body', fontName='Inter', fontSize=9.5, leading=14.5, textColor=MUTED),
    'mod': ParagraphStyle('mod', fontName='Sora-Bold', fontSize=11.5, leading=15, textColor=colors.white),
    'sn': ParagraphStyle('sn', fontName='Sora-Bold', fontSize=10, leading=12, textColor=BLUE_D, alignment=1),
    'st': ParagraphStyle('st', fontName='Inter-Bold', fontSize=9.5, leading=13, textColor=CHAR),
    'goal': ParagraphStyle('goal', fontName='Inter', fontSize=8.8, leading=12.4, textColor=MUTED, leftIndent=8, bulletIndent=0),
    'small': ParagraphStyle('small', fontName='Inter', fontSize=8.5, leading=12, textColor=MUTED),
}

def bs(n): return 'Bs ' + f'{n:,}'.replace(',', '.')

def academy_icon(c, x, y, size, mono_white=False):
    """Ícono de Academy (libros + birrete + chispa), esquina inferior izquierda en (x, y)."""
    k = size / 64; Y = lambda v: y + (64 - v) * k
    cols = ['#1E3A8A', '#2F4AC0', '#3B5BDB', '#5C7CFA']
    if mono_white: cols = ['#FFFFFF'] * 4
    books = [(9, 52, 46, 7), (13, 43.5, 39, 7), (8, 35, 43, 7), (14, 26.5, 36, 7)]
    for (bx, by, bw, bh), col in zip(books, cols):
        c.setFillColor(colors.HexColor(col)); c.roundRect(x + bx * k, Y(by + bh), bw * k, bh * k, bh * k / 2, stroke=0, fill=1)
    c.setFillColor(colors.HexColor('#5C7CFA')); c.roundRect(x + 21 * k, Y(24), 22 * k, 6.5 * k, 3.25 * k, stroke=0, fill=1)
    p = c.beginPath(); p.moveTo(x + 32 * k, Y(3)); p.lineTo(x + 59 * k, Y(12)); p.lineTo(x + 32 * k, Y(21)); p.lineTo(x + 5 * k, Y(12)); p.close()
    c.setFillColor(colors.HexColor('#91A7FF')); c.drawPath(p, stroke=0, fill=1)
    c.setStrokeColor(colors.HexColor('#BAC8FF')); c.setLineWidth(1.8 * k); c.setLineCap(1); c.setLineJoin(1)
    p = c.beginPath(); p.moveTo(x + 32 * k, Y(12)); p.lineTo(x + 54 * k, Y(13)); p.lineTo(x + 54 * k, Y(23)); c.drawPath(p, stroke=1, fill=0)
    c.setFillColor(SPARK); c.circle(x + 54 * k, Y(25.5), 3 * k, stroke=0, fill=1)

def wordmark(c, x, y, size, light):
    c.setFillColor(colors.white if light else CHAR); c.setFont('Sora-Bold', size); c.drawString(x, y, 'prometeo')
    c.setFillColor(SOFT if light else BLUE); c.setFont('Sora', size); c.drawString(x + c.stringWidth('prometeo ', 'Sora-Bold', size), y, 'academy')

def make(course):
    out = os.path.join(OUTDIR, f"Temario_{course['level']}_Prometeo_Academy.pdf")
    nses = sum(len(m['sessions']) for m in course['modules'])

    def cover(c, d):
        c.saveState()
        for i in range(70):  # degradado azul noche
            t = i / 70; f = 1 - abs(t - .45) * 1.6
            c.setFillColorRGB((10 + 14 * f) / 255, (18 + 22 * f) / 255, (54 + 56 * f) / 255)
            c.rect(0, H - (i + 1) * H / 70, W, H / 70 + 1, stroke=0, fill=1)
        c.setStrokeColor(colors.Color(.36, .49, .98, alpha=.25)); c.setLineWidth(1)
        c.circle(W - 25 * mm, H - 45 * mm, 105 * mm, stroke=1, fill=0); c.circle(W - 5 * mm, H - 75 * mm, 70 * mm, stroke=1, fill=0)
        academy_icon(c, M - 1 * mm, H - 41 * mm, 18 * mm)
        wordmark(c, M + 19 * mm, H - 33.5 * mm, 17, True)
        c.setFillColor(colors.Color(1, 1, 1, alpha=.6)); c.setFont('Inter', 9); c.drawString(M + 19 * mm, H - 39 * mm, 'Cursos y capacitación en datos')
        # nivel + título
        c.setFillColor(BLUE); c.roundRect(M, H - 118 * mm, c.stringWidth(f"CURSO {course['level'].upper()}", 'Inter-Bold', 9) + 10 * mm, 8 * mm, 4 * mm, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont('Inter-Bold', 9); c.drawString(M + 5 * mm, H - 115.3 * mm, f"CURSO {course['level'].upper()}")
        title = course['title']; size = 34
        words = title.split(); lines = []; cur = ''
        for w_ in words:
            test = (cur + ' ' + w_).strip()
            if c.stringWidth(test, 'Sora-Black', size) > W - 2 * M: lines.append(cur); cur = w_
            else: cur = test
        lines.append(cur)
        c.setFillColor(colors.white); c.setFont('Sora-Black', size)
        for i, l in enumerate(lines): c.drawString(M, H - 135 * mm - i * 13.5 * mm, l)
        ty = H - 135 * mm - len(lines) * 13.5 * mm - 2 * mm
        c.setFillColor(colors.Color(1, 1, 1, alpha=.78)); c.setFont('Inter', 11.5)
        sm = course['summary']; words = sm.split(); cur = ''; yy = ty
        for w_ in words:
            test = (cur + ' ' + w_).strip()
            if c.stringWidth(test, 'Inter', 11.5) > W - 2 * M - 10 * mm: c.drawString(M, yy, cur); yy -= 6 * mm; cur = w_
            else: cur = test
        c.drawString(M, yy, cur)
        # ficha
        y0 = 58 * mm; bw = (W - 2 * M - 3 * 4 * mm) / 4
        facts = [('Duración', FMT['duration'], f"{nses} sesiones"), ('Ritmo', f"{FMT['perWeek']} clases por semana", FMT['hours']),
                 ('Modalidad', 'En vivo + virtual', 'Clases grabadas en Drive'), ('Inversión', bs(course['priceSolo']), f"{bs(course['priceGroup'])} c/u en grupo de {FMT['groupMin']}+")]
        for i, (k_, v, sub) in enumerate(facts):
            x = M + i * (bw + 4 * mm)
            c.setFillColor(colors.Color(1, 1, 1, alpha=.08)); c.roundRect(x, y0, bw, 30 * mm, 4 * mm, stroke=0, fill=1)
            c.setFillColor(SOFT); c.setFont('Inter-Bold', 7); c.drawString(x + 4 * mm, y0 + 23 * mm, k_.upper())
            c.setFillColor(colors.white); c.setFont('Sora-Bold', 10.5 if len(v) < 18 else 9); c.drawString(x + 4 * mm, y0 + 15.5 * mm, v)
            c.setFillColor(colors.Color(1, 1, 1, alpha=.65)); c.setFont('Inter', 7.2)
            # sub en hasta 2 líneas
            ws = sub.split(); cur = ''; yy = y0 + 9 * mm
            for w_ in ws:
                test = (cur + ' ' + w_).strip()
                if c.stringWidth(test, 'Inter', 7.2) > bw - 8 * mm: c.drawString(x + 4 * mm, yy, cur); yy -= 3.6 * mm; cur = w_
                else: cur = test
            c.drawString(x + 4 * mm, yy, cur)
        c.setFillColor(colors.Color(1, 1, 1, alpha=.55)); c.setFont('Inter', 8.5)
        c.drawString(M, 22 * mm, 'techprometeo@gmail.com  ·  WhatsApp +591 782 33445  ·  Santa Cruz de la Sierra, Bolivia')
        c.restoreState()

    def inner(c, d):
        c.saveState()
        c.setFillColor(BLUE); c.rect(0, H - 3 * mm, W, 3 * mm, stroke=0, fill=1)
        academy_icon(c, M - .5 * mm, H - 16 * mm, 7.5 * mm)
        wordmark(c, M + 8.5 * mm, H - 13 * mm, 9.5, False)
        c.setFillColor(MUTED); c.setFont('Inter', 8); c.drawRightString(W - M, H - 13 * mm, f"Temario · {course['title']}")
        c.setStrokeColor(colors.HexColor('#E3E7F5')); c.line(M, 14 * mm, W - M, 14 * mm)
        c.setFillColor(MUTED); c.setFont('Inter', 7.5); c.drawString(M, 9 * mm, 'Prometeo Academy · Los contenidos pueden ajustarse a cada grupo')
        c.drawRightString(W - M, 9 * mm, str(d.page))
        c.restoreState()

    doc = BaseDocTemplate(out, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=24 * mm, bottomMargin=20 * mm,
                          title=f"Temario · {course['title']} · Prometeo Academy", author='Prometeo Academy')
    fr = Frame(M, 20 * mm, W - 2 * M, H - 44 * mm, id='f')
    doc.addPageTemplates([PageTemplate('cover', [Frame(0, 0, W, H, id='c')], onPage=cover), PageTemplate('inner', [fr], onPage=inner)])
    S = [NextPageTemplate('inner'), PageBreak()]
    # para quién / te llevas
    t = Table([[Paragraph('PARA QUIÉN', st['k']), Paragraph('TE LLEVAS', st['k'])],
               [Paragraph(course['forWho'], st['body']), Paragraph(course['outcome'], st['body'])]], colWidths=[(W - 2 * M) / 2 - 3 * mm] * 2, hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), TINT), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 10), ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                           ('TOPPADDING', (0, 0), (-1, 0), 9), ('BOTTOMPADDING', (0, -1), (-1, -1), 10), ('LINEAFTER', (0, 0), (0, -1), 6, colors.white)]))
    S += [Paragraph('Temario', st['h2']), Paragraph(f"{len(course['modules'])} módulos y {nses} sesiones de 1,5 horas: una clase en vivo y una virtual por semana. Todas quedan grabadas en Google Drive con el material de cada sesión.", st['body']), Spacer(1, 4 * mm), t, Spacer(1, 6 * mm)]
    for m in course['modules']:
        rows = [[Paragraph(m['title'], st['mod']), '']]
        for s_ in m['sessions']:
            goals = [Paragraph(g, st['goal'], bulletText='•') for g in s_['goals']]
            rows.append([Paragraph(f"S{s_['n']}", st['sn']), [Paragraph(s_['title'], st['st']), Spacer(1, 1.5 * mm)] + goals])
        body = Table(rows, colWidths=[16 * mm, W - 2 * M - 16 * mm], repeatRows=1)
        body.setStyle(TableStyle([('SPAN', (0, 0), (1, 0)), ('BACKGROUND', (0, 0), (-1, 0), INK2), ('LEFTPADDING', (0, 0), (-1, 0), 10),
               ('TOPPADDING', (0, 0), (-1, 0), 8), ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
               ('VALIGN', (0, 1), (-1, -1), 'TOP'), ('TOPPADDING', (0, 1), (-1, -1), 7), ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
               ('LINEBELOW', (0, 1), (-1, -2), .6, colors.HexColor('#E3E7F5')), ('BOX', (0, 0), (-1, -1), .6, colors.HexColor('#E3E7F5')),
               ('BACKGROUND', (0, 1), (0, -1), PALE)]))
        S += [body, Spacer(1, 6 * mm)]
    # cierre
    fin = Table([[Paragraph('<font name="Sora-Bold" size="13" color="#FFFFFF">¿Te inscribes?</font>', st['body'])],
                 [Paragraph(f'<font color="#C5D0FF">Inversión individual <b>{bs(course["priceSolo"])}</b> · Grupo de {FMT["groupMin"]}+ personas <b>{bs(course["priceGroup"])}</b> c/u · Pago por QR o transferencia.<br/>'
                            f'Inscríbete en la web de Prometeo (Academy, botón “Quiero este curso”) o escríbenos por WhatsApp al +591 782 33445.</font>', st['body'])]], colWidths=[W - 2 * M])
    fin.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), INK), ('LEFTPADDING', (0, 0), (-1, -1), 12), ('RIGHTPADDING', (0, 0), (-1, -1), 12), ('TOPPADDING', (0, 0), (-1, 0), 12), ('BOTTOMPADDING', (0, -1), (-1, -1), 12), ('ROUNDEDCORNERS', [8, 8, 8, 8])]))
    S += [KeepTogether([fin])]
    doc.build(S)
    return out

for c_ in data['courses']: print(make(c_))
