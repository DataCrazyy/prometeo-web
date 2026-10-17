"""Genera el sistema de logos de Prometeo (SVG con texto convertido a trazos + PNG).

Uso:  python tools/brand/make_brand.py
Salida: public/brand/<marca>/*.svg|png  y  public/brand/instagram/*.png

Idea de la familia: el logo de Prometeo son 6 barras (una llama de datos) y una chispa naranja.
Cada línea usa esas mismas barras para formar su propio ícono y conserva SIEMPRE la chispa naranja,
que es la firma de Prometeo.
"""
import os, math, glob
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'public', 'brand')
FONTS = os.path.join(ROOT, 'node_modules', '@fontsource', 'sora', 'files')
SPARK = '#FFA94D'
INK = '#1A1033'      # texto sobre fondo claro
NIGHT = '#0B0716'    # fondo oscuro de marca

# ── texto a trazos ────────────────────────────────────
_fonts = {}
def font(w):
    if w not in _fonts:
        _fonts[w] = TTFont(os.path.join(FONTS, f'sora-latin-{w}-normal.woff2'))
    return _fonts[w]

def text_path(txt, weight, size, x0=0, base=0, track=0):
    f = font(weight); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm
    s = size / upm; pen = SVGPathPen(gs); x = 0
    for ch in txt:
        g = cmap[ord(ch)]
        tp = TransformPen(pen, (s, 0, 0, -s, x0 + x, base)); gs[g].draw(tp)
        x += gs[g].width * s + track
    return pen.getCommands(), x - track

def text_w(txt, weight, size, track=0): return text_path(txt, weight, size, track=track)[1]
def xheight(weight, size): f = font(weight); return f['OS/2'].sxHeight / f['head'].unitsPerEm * size
def capheight(weight, size): f = font(weight); return f['OS/2'].sCapHeight / f['head'].unitsPerEm * size

# ── íconos (en una caja de 64×64) ─────────────────────
def rr(x, y, w, h, fill, op=1):
    r = min(w, h) / 2
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"' + (f' fill-opacity="{op}"' if op < 1 else '') + '/>'

def icon(brand, mode='color'):
    """mode: color | white (sobre fondos oscuros o de color) | ink (un solo color oscuro)"""
    mono = None if mode == 'color' else ('#FFFFFF' if mode == 'white' else INK)
    OP = [1, .9, .8, .7, .6, .5]
    col = lambda c, i=0: c if not mono else mono
    op = lambda i: 1 if not mono else OP[i]
    spark = SPARK if mode == 'color' else mono
    out = []
    if brand == 'prometeo':
        bars = [(17, 54.5, 30), (11, 46, 42), (11, 37.5, 42), (16, 29, 34), (23, 20.5, 24), (30, 12, 13)]
        cols = ['#3D1E9E', '#5E35B1', '#7C4DFF', '#A35CF5', '#E0609A', '#FF7A3D']
        out += [rr(x, y, w, 6.5, col(cols[i]), op(i)) for i, (x, y, w) in enumerate(bars)]
        out.append(f'<circle cx="38.5" cy="5.5" r="3.4" fill="{spark}"/>')
    elif brand == 'consulting':
        hs = [12, 19, 15, 26, 33, 41]; cols = ['#3D1E9E', '#5E35B1', '#7C4DFF', '#9B6EFF', '#B39DFF', '#D0BFFF']
        out += [rr(7 + i * 8.6, 59 - h, 6.6, h, col(cols[i]), op(5 - i) if mono else 1) for i, h in enumerate(hs)]
        tops = [(7 + i * 8.6 + 3.3, 59 - h - 6) for i, h in enumerate(hs)]
        line = ' '.join(f'{x:.1f},{y:.1f}' for x, y in tops[:-1]) + ' 59,5.5'
        out.append(f'<polyline points="{line}" fill="none" stroke="{spark}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
        out.append(f'<circle cx="59" cy="5.5" r="3.8" fill="{spark}"/>')
    elif brand == 'academy':
        cols = ['#1E3A8A', '#2F4AC0', '#3B5BDB', '#5C7CFA']
        books = [(9, 52, 46, 7), (13, 43.5, 39, 7), (8, 35, 43, 7), (14, 26.5, 36, 7)]
        out += [rr(x, y, w, h, col(cols[i]), op(i)) for i, (x, y, w, h) in enumerate(books)]
        out.append(rr(21, 17.5, 22, 6.5, col('#5C7CFA'), op(3)))
        out.append(f'<path d="M32 3 L59 12 L32 21 L5 12 Z" fill="{col("#91A7FF")}" fill-opacity="{op(1)}" stroke-linejoin="round"/>')
        out.append(f'<path d="M32 12 L54 13 L54 23" fill="none" stroke="{col("#BAC8FF")}" stroke-opacity="{op(2)}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
        out.append(f'<circle cx="54" cy="25.5" r="3" fill="{spark}"/>')
    elif brand == 'talks':
        cols = ['#C2410C', '#E8590C', '#FF6A1A', '#FF8A3D', '#FFA94D', '#FFC078']
        bub = 'M10 6 H54 a6 6 0 0 1 6 6 V43 a6 6 0 0 1 -6 6 H26 L15 58 V49 H10 a6 6 0 0 1 -6 -6 V12 a6 6 0 0 1 6 -6 Z'
        out.append(f'<path d="{bub}" fill="none" stroke="{col("#FF8A3D")}" stroke-opacity="{op(1)}" stroke-width="3.4" stroke-linejoin="round"/>')
        hs = [10, 20, 28, 17, 24, 11]
        out += [rr(13.5 + i * 6.6, 27.5 - h / 2, 4.4, h, col(cols[i]), op(i % 3)) for i, h in enumerate(hs)]
        out.append(f'<circle cx="52" cy="14" r="3" fill="{spark}"/>')
    elif brand == 'precios-claros':
        tag = 'M4 32 L19 13 H55 a5 5 0 0 1 5 5 V46 a5 5 0 0 1 -5 5 H19 Z M14.5 32 m-4 0 a4 4 0 1 0 8 0 a4 4 0 1 0 -8 0 Z'
        bars = [(25, 23, 3, 18), (30, 23, 1.6, 18), (33.6, 23, 4, 18), (39.6, 23, 2, 18), (43.6, 23, 3.4, 18), (49, 23, 1.8, 18)]
        g = [f'<path d="{tag}" fill="{col("#12B886")}" fill-rule="evenodd"/>']
        bar_fill = '#FFFFFF' if mode == 'color' else (NIGHT if mode == 'white' else '#FFFFFF')
        g += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(w, h) / 2}" fill="{bar_fill}" fill-opacity="{.92 if mode == "color" else 1}"/>' for x, y, w, h in bars]
        g.append(f'<circle cx="14.5" cy="32" r="5.6" fill="none" stroke="{spark}" stroke-width="2.2"/>')
        out.append(f'<g transform="translate(32 32) rotate(-18) scale(.9) translate(-32 -32)">' + ''.join(g) + '</g>')
    return ''.join(out)

BRANDS = {
    'prometeo':     dict(word=None,         acc_l=None,      acc_d=None),
    'consulting':   dict(word='consulting', acc_l='#7C4DFF', acc_d='#B39DFF'),
    'academy':      dict(word='academy',    acc_l='#3B5BDB', acc_d='#91A7FF'),
    'talks':        dict(word='talks',      acc_l='#E8590C', acc_d='#FFA94D'),
    'precios-claros': dict(word=None,         acc_l='#0B8A65', acc_d='#63E6BE'),
}
BG = {'prometeo': '#7C4DFF', 'consulting': '#5E35B1', 'academy': '#2F4AC0', 'talks': '#E8590C', 'precios-claros': '#0B8A65'}

def wordmark(brand, dark, size):
    """Devuelve (lista de paths, ancho, alto de referencia) con la línea base en y=0."""
    b = BRANDS[brand]; ink = '#FFFFFF' if dark else INK
    if brand == 'precios-claros':
        acc = b['acc_d'] if dark else b['acc_l']
        d1, w1 = text_path('Precios Claros', 800, size, track=-size * .02)
        s2 = size * .44; d2, w2 = text_path('by prometeo', 600, s2, base=s2 * 1.45)
        return [(d1, ink), (d2, acc)], max(w1, w2), 'pj'
    d1, w1 = text_path('prometeo', 700, size, track=-size * .02)
    parts = [(d1, ink)]; w = w1
    if b['word']:
        acc = b['acc_d'] if dark else b['acc_l']
        gap = size * .26
        d2, w2 = text_path(b['word'], 400, size, x0=w1 + gap, track=-size * .01)
        parts.append((d2, acc)); w = w1 + gap + w2
    return parts, w, 'one'

def svg(w, h, body, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}">{rect}{body}</svg>'

def paths(parts, tx, ty): return f'<g transform="translate({tx:.2f} {ty:.2f})">' + ''.join(f'<path d="{d}" fill="{c}"/>' for d, c in parts) + '</g>'
def place_icon(brand, mode, x, y, size): return f'<g transform="translate({x:.2f} {y:.2f}) scale({size / 64:.4f})">{icon(brand, mode)}</g>'

def horizontal(brand, dark):
    H = 200; size = 104 if brand != 'precios-claros' else 92
    parts, tw, kind = wordmark(brand, dark, size)
    gap = H * .2; pad = 8
    if kind == 'one': base = H / 2 + xheight(700, size) / 2
    else: base = H / 2 - (size * .44 * 1.45) / 2 + capheight(800, size) / 2
    W = pad + H + gap + tw + pad
    return svg(W, H + 2 * pad, place_icon(brand, 'white' if False else 'color', pad, pad, H) + paths(parts, pad + H + gap, pad + base))

def vertical(brand, dark):
    I = 300; size = (96 if brand == 'prometeo' else 70) if brand != 'precios-claros' else 80
    parts, tw, kind = wordmark(brand, dark, size)
    W = max(I, tw) + 40; top = 20
    base = top + I + 46 + (capheight(800, size) if kind == 'pj' else xheight(700, size))
    Hh = base + (size * .44 * 1.45 + 20 if kind == 'pj' else size * .32) + 20
    if kind == 'pj':  # centrar cada línea
        d1, w1 = text_path('Precios Claros', 800, size, track=-size * .02); s2 = size * .44
        d2, w2 = text_path('by prometeo', 600, s2, x0=(w1 - text_w('by prometeo', 600, s2)) / 2, base=s2 * 1.45)
        parts = [(d1, parts[0][1]), (d2, parts[1][1])]; tw = w1
    return svg(W, Hh, place_icon(brand, 'color', (W - I) / 2, top, I) + paths(parts, (W - tw) / 2, base))

def isotipo(brand, mode): return svg(64, 64, icon(brand, mode)).replace('width="64" height="64"', 'width="1024" height="1024"')

def avatar(brand):
    """Foto de perfil 1080×1080: el ícono dentro del círculo seguro de Instagram."""
    S = 1080
    if brand == 'prometeo':
        bg = f'<rect width="{S}" height="{S}" fill="{NIGHT}"/><circle cx="540" cy="560" r="520" fill="url(#gl)"/>'
        defs = '<defs><radialGradient id="gl"><stop offset="0" stop-color="#7C4DFF" stop-opacity=".55"/><stop offset="1" stop-color="#7C4DFF" stop-opacity="0"/></radialGradient></defs>'
        return svg(S, S, defs + bg + place_icon(brand, 'color', 540 - 290, 540 - 290, 580))
    bg = f'<rect width="{S}" height="{S}" fill="{BG[brand]}"/>'
    return svg(S, S, bg + place_icon(brand, 'white', 540 - 290, 540 - 290, 580))

def highlight(brand, label):
    """Portada de historia destacada 1080×1920 (Instagram la recorta en círculo al centro)."""
    W, H = 1080, 1920
    ring = f'<circle cx="540" cy="960" r="400" fill="{BG[brand] if brand != "prometeo" else "#1A1033"}"/>'
    lp, lw = text_path(label, 700, 64)
    return svg(W, H, f'<rect width="{W}" height="{H}" fill="{NIGHT}"/>' + ring + place_icon(brand, 'white' if brand != 'prometeo' else 'color', 540 - 230, 960 - 230, 460)
               + paths([(lp, '#FFFFFF')], 540 - lw / 2, 1500) )

# ── escritura + PNG ───────────────────────────────────
def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f: f.write(content)

jobs = []  # (svg_path, png_path, scale)
for b in BRANDS:
    d = os.path.join(OUT, b)
    for name, content, sc in [
        ('isotipo', isotipo(b, 'color'), 1), ('isotipo-blanco', isotipo(b, 'white'), 1), ('isotipo-mono', isotipo(b, 'ink'), 1),
        ('horizontal-fondo-claro', horizontal(b, False), 3), ('horizontal-fondo-oscuro', horizontal(b, True), 3),
        ('vertical-fondo-claro', vertical(b, False), 3), ('vertical-fondo-oscuro', vertical(b, True), 3)]:
        p = os.path.join(d, name + '.svg'); write(p, content); jobs.append((p, p[:-4] + '.png', sc))
    p = os.path.join(OUT, 'instagram', f'perfil-{b}.svg'); write(p, avatar(b)); jobs.append((p, p[:-4] + '.png', 1))
for b, label in [('prometeo', 'Nosotros'), ('consulting', 'Consulting'), ('academy', 'Academy'), ('talks', 'Talks'), ('precios-claros', 'Precios Claros')]:
    p = os.path.join(OUT, 'instagram', f'destacada-{b}.svg'); write(p, highlight(b, label)); jobs.append((p, p[:-4] + '.png', 1))

from playwright.sync_api import sync_playwright
import re
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page()
    for s, png, sc in jobs:
        src = open(s, encoding='utf-8').read()
        w, h = map(float, re.search(r'width="(\d+)" height="(\d+)"', src).groups())
        pg.set_viewport_size({'width': int(w * sc), 'height': int(h * sc)})
        pg.set_content(f'<html><body style="margin:0;background:transparent">{src.replace(f"width=\"{w:.0f}\" height=\"{h:.0f}\"", f"width=\"{w * sc:.0f}\" height=\"{h * sc:.0f}\"", 1)}</body></html>')
        pg.screenshot(path=png, omit_background=True, clip={'x': 0, 'y': 0, 'width': w * sc, 'height': h * sc})
    br.close()
print(len(jobs), 'archivos SVG + PNG en', OUT)
