import { describe, expect, it } from 'vitest';
import { color } from '../src/core/arte/paleta.ts';
import {
  hexARgb,
  luminancia,
  NOCHE_SEPIA_AFUERA,
  nocheDeTinta,
  nocheSepia,
  type Rgb,
} from '../src/core/escenarios/noche.ts';

const rgb = (id: string): Rgb => hexARgb(color(id));
const COLORES = { papel: rgb('papel'), tinta: rgb('tinta') };
const tinta = (t: number, c: Rgb): Rgb => nocheDeTinta(t, c, COLORES);
const sepia = (c: Rgb, a: number): Rgb => nocheSepia(c, a, COLORES);

/** Escalones de la aguada adentro (oscuro, penumbra, media luz): `ESTILOS_NOCHE` en casa_insuasty.py. */
const ADENTRO_SEPIA = [0.8, 0.58, 0.32] as const;
const ADENTRO_TINTA = [0.93, 0.74, 0.46] as const;

/** Tono en grados (HSV), para ver que un color sigue siendo el mismo. */
function tono([r, g, b]: Rgb): number {
  const max = Math.max(r, g, b);
  const d = max - Math.min(r, g, b);
  const h =
    max === r ? (g - b) / d : max === g ? 2 + (b - r) / d : 4 + (r - g) / d;
  return (h * 60 + 360) % 360;
}

function cerca(a: Rgb, b: Rgb, margen: number): void {
  for (const i of [0, 1, 2] as const) {
    expect(Math.abs(a[i] - b[i])).toBeLessThanOrEqual(margen);
  }
}

/** Aguada de tinta con opacidad o sobre un color, como la de los cuartos. */
function aguada(c: Rgb, o: number): Rgb {
  const t = COLORES.tinta;
  return [
    (1 - o) * c[0] + o * t[0],
    (1 - o) * c[1] + o * t[1],
    (1 - o) * c[2] + o * t[2],
  ];
}

describe('noche de tinta (casa-insuasty.md §7)', () => {
  it('lee los colores de la paleta', () => {
    expect(hexARgb('#ff8000')).toEqual([1, 128 / 255, 0]);
  });

  it('con intensidad 0 no cambia nada', () => {
    for (const id of ['papel', 'tinta', 'sepia', 'llama', 'rojo-liberal']) {
      cerca(tinta(0, rgb(id)), rgb(id), 1e-9);
    }
  });

  it('el papel sigue siendo papel y el encalado de afuera cae en tinta', () => {
    cerca(tinta(1, rgb('papel')), rgb('papel'), 1 / 255);
    const encalado = sepia(rgb('papel'), NOCHE_SEPIA_AFUERA);
    cerca(tinta(1, encalado), rgb('tinta'), 1 / 255);
  });

  it('lo más oscuro y el cielo quedan casi negros', () => {
    const sombra = sepia(rgb('sepia'), NOCHE_SEPIA_AFUERA);
    for (const c of [sombra, rgb('sepia-oscuro'), rgb('humo')]) {
      expect(luminancia(tinta(1, c))).toBeLessThan(luminancia(rgb('tinta')));
    }
  });

  it('adentro, la penumbra y la media luz caen donde las pinta la noche de tinta', () => {
    const papel = rgb('papel');
    for (const i of [1, 2] as const) {
      cerca(
        tinta(1, sepia(papel, ADENTRO_SEPIA[i])),
        aguada(papel, ADENTRO_TINTA[i]),
        0.03,
      );
    }
  });

  it('la luz, el rojo y el azul guardan el tono y casi toda su fuerza', () => {
    for (const id of [
      'lampara',
      'llama-nucleo',
      'llama',
      'brasa',
      'rojo-liberal',
      'azul-conservador',
    ]) {
      const antes = rgb(id);
      const despues = tinta(1, antes);
      expect(Math.abs(tono(despues) - tono(antes)), id).toBeLessThanOrEqual(5);
      expect(
        Math.abs(Math.max(...despues) - Math.max(...antes)),
        id,
      ).toBeLessThanOrEqual(0.05);
    }
  });

  it('a mitad de camino queda entre la noche sepia y la de tinta', () => {
    const media = sepia(rgb('papel'), ADENTRO_SEPIA[1]);
    const [l0, l5, l1] = [0, 0.5, 1].map((t) => luminancia(tinta(t, media)));
    expect(l5).toBeLessThan(l0 ?? 0);
    expect(l5).toBeGreaterThan(l1 ?? 0);
  });
});
