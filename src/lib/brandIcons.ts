// Íconos de la familia de marca (caja 64×64). Misma geometría que tools/brand/make_brand.py
// y que los archivos de public/brand/. Todas las marcas conservan la chispa naranja de Prometeo.
export type Brand = 'prometeo' | 'consulting' | 'academy' | 'talks' | 'precio';
export type IconMode = 'color' | 'white' | 'mono';

const SPARK = '#FFA94D';
const INK = '#1A1033';
const OP = [1, 0.9, 0.8, 0.7, 0.6, 0.5];

const rr = (x: number, y: number, w: number, h: number, fill: string, op = 1) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${Math.min(w, h) / 2}" fill="${fill}"${op < 1 ? ` fill-opacity="${op}"` : ''}/>`;

export function brandIcon(brand: Brand, mode: IconMode = 'color', monoColor = INK): string {
  const mono = mode === 'color' ? null : mode === 'white' ? '#FFFFFF' : monoColor;
  const col = (c: string) => mono ?? c;
  const op = (i: number) => (mono ? OP[i] : 1);
  const spark = mono ?? SPARK;
  const out: string[] = [];

  if (brand === 'prometeo') {
    const bars: [number, number, number][] = [[17, 54.5, 30], [11, 46, 42], [11, 37.5, 42], [16, 29, 34], [23, 20.5, 24], [30, 12, 13]];
    const cols = ['#3D1E9E', '#5E35B1', '#7C4DFF', '#A35CF5', '#E0609A', '#FF7A3D'];
    bars.forEach(([x, y, w], i) => out.push(rr(x, y, w, 6.5, col(cols[i]), op(i))));
    out.push(`<circle cx="38.5" cy="5.5" r="3.4" fill="${spark}"/>`);
  } else if (brand === 'consulting') {
    const hs = [12, 19, 15, 26, 33, 41];
    const cols = ['#3D1E9E', '#5E35B1', '#7C4DFF', '#9B6EFF', '#B39DFF', '#D0BFFF'];
    hs.forEach((h, i) => out.push(rr(7 + i * 8.6, 59 - h, 6.6, h, col(cols[i]), mono ? op(5 - i) : 1)));
    const pts = hs.slice(0, 5).map((h, i) => `${(7 + i * 8.6 + 3.3).toFixed(1)},${(59 - h - 6).toFixed(1)}`).join(' ') + ' 59,5.5';
    out.push(`<polyline points="${pts}" fill="none" stroke="${spark}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>`);
    out.push(`<circle cx="59" cy="5.5" r="3.8" fill="${spark}"/>`);
  } else if (brand === 'academy') {
    const cols = ['#1E3A8A', '#2F4AC0', '#3B5BDB', '#5C7CFA'];
    const books: [number, number, number, number][] = [[9, 52, 46, 7], [13, 43.5, 39, 7], [8, 35, 43, 7], [14, 26.5, 36, 7]];
    books.forEach(([x, y, w, h], i) => out.push(rr(x, y, w, h, col(cols[i]), op(i))));
    out.push(rr(21, 17.5, 22, 6.5, col('#5C7CFA'), op(3)));
    out.push(`<path d="M32 3 L59 12 L32 21 L5 12 Z" fill="${col('#91A7FF')}" fill-opacity="${op(1)}"/>`);
    out.push(`<path d="M32 12 L54 13 L54 23" fill="none" stroke="${col('#BAC8FF')}" stroke-opacity="${op(2)}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>`);
    out.push(`<circle cx="54" cy="25.5" r="3" fill="${spark}"/>`);
  } else if (brand === 'talks') {
    const cols = ['#C2410C', '#E8590C', '#FF6A1A', '#FF8A3D', '#FFA94D', '#FFC078'];
    out.push(`<path d="M10 6 H54 a6 6 0 0 1 6 6 V43 a6 6 0 0 1 -6 6 H26 L15 58 V49 H10 a6 6 0 0 1 -6 -6 V12 a6 6 0 0 1 6 -6 Z" fill="none" stroke="${col('#FF8A3D')}" stroke-opacity="${op(1)}" stroke-width="3.4" stroke-linejoin="round"/>`);
    [10, 20, 28, 17, 24, 11].forEach((h, i) => out.push(rr(13.5 + i * 6.6, 27.5 - h / 2, 4.4, h, col(cols[i]), op(i % 3))));
    out.push(`<circle cx="52" cy="14" r="3" fill="${spark}"/>`);
  } else {
    const tag = 'M4 32 L19 13 H55 a5 5 0 0 1 5 5 V46 a5 5 0 0 1 -5 5 H19 Z M14.5 32 m-4 0 a4 4 0 1 0 8 0 a4 4 0 1 0 -8 0 Z';
    const bars: [number, number, number, number][] = [[25, 23, 3, 18], [30, 23, 1.6, 18], [33.6, 23, 4, 18], [39.6, 23, 2, 18], [43.6, 23, 3.4, 18], [49, 23, 1.8, 18]];
    const barFill = mode === 'white' ? '#0B0716' : '#FFFFFF';
    const g = [`<path d="${tag}" fill="${col('#12B886')}" fill-rule="evenodd"/>`];
    bars.forEach(([x, y, w, h]) => g.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${Math.min(w, h) / 2}" fill="${barFill}"${mode === 'color' ? ' fill-opacity="0.92"' : ''}/>`));
    g.push(`<circle cx="14.5" cy="32" r="5.6" fill="none" stroke="${spark}" stroke-width="2.2"/>`);
    out.push(`<g transform="translate(32 32) rotate(-18) scale(.9) translate(-32 -32)">${g.join('')}</g>`);
  }
  return out.join('');
}

export const brandNames: Record<Brand, { word?: string; label: string }> = {
  prometeo: { label: 'Prometeo' },
  consulting: { word: 'consulting', label: 'Prometeo Consulting' },
  academy: { word: 'academy', label: 'Prometeo Academy' },
  talks: { word: 'talks', label: 'Prometeo Talks' },
  precio: { label: 'Precio Justo by prometeo' },
};
