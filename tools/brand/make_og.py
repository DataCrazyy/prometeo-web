"""Imágenes para compartir (og:image, 1200×630) y favicons de cada página, con los logos de public/brand/.
Uso: python tools/brand/make_og.py   (después de make_brand.py)"""
import os, shutil
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PUB = os.path.join(ROOT, 'public'); BR = os.path.join(PUB, 'brand')
PAGES = [  # tema de la página, carpeta del logo, color del brillo, frase
  ('prometeo', 'prometeo', '#7C4DFF', 'Transformamos datos en decisiones inteligentes.'),
  ('consulting', 'consulting', '#7C4DFF', 'Business Intelligence y Power BI para tu empresa.'),
  ('academy', 'academy', '#3B5BDB', 'Cursos de Power BI en vivo y virtuales.'),
  ('talks', 'talks', '#E8590C', 'Conferencias y videos sobre datos e IA · Próximamente'),
  ('precio', 'precios-claros', '#12B886', 'Compara precios de supermercados y farmacias antes de comprar.'),
]
FONT = os.path.join(ROOT, 'node_modules/@fontsource/inter/files/inter-latin-500-normal.woff2')
for theme, folder, _, _ in PAGES:  # favicons
    shutil.copy(os.path.join(BR, folder, 'isotipo.svg'), os.path.join(PUB, 'favicon.svg' if theme == 'prometeo' else f'favicon-{theme}.svg'))
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1200, 'height': 630})
    for theme, folder, glow, line in PAGES:
        logo = open(os.path.join(BR, folder, 'horizontal-fondo-oscuro.svg'), encoding='utf-8').read()
        html = f'''<html><head><style>
          @font-face {{ font-family: Inter; src: url(file://{FONT}); font-weight: 500; }}
          body {{ margin: 0; width: 1200px; height: 630px; background: #0B0716; overflow: hidden; font-family: Inter, sans-serif; }}
          .g {{ position: absolute; width: 1100px; height: 1100px; left: 50px; top: -330px; border-radius: 50%;
                background: radial-gradient(circle, {glow}55 0%, {glow}00 62%); }}
          .logo {{ position: absolute; left: 0; right: 0; top: 190px; display: flex; justify-content: center; }}
          .logo svg {{ max-height: 190px; max-width: 1000px; width: auto; height: auto; }}
          .t {{ position: absolute; left: 0; right: 0; top: 440px; text-align: center; color: rgba(255,255,255,.78); font-size: 34px; font-weight: 500; }}
        </style></head><body><div class="g"></div><div class="logo">{logo}</div><div class="t">{line}</div></body></html>'''
        pg.set_content(html); pg.wait_for_timeout(150)
        pg.screenshot(path=os.path.join(PUB, 'og.jpg' if theme == 'prometeo' else f'og-{theme}.jpg'), type='jpeg', quality=90)
    b.close()
print('ok')
