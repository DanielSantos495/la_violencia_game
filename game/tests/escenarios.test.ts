import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { color } from '../src/core/arte/paleta.ts';
import {
  anchoCapa,
  type IdCapa,
  LADO_MAXIMO_MODULO,
  ORDEN_CAPAS,
  PARALAJE,
  VIEWPORT,
  Y_SUELO,
  ySueloCapa,
} from '../src/core/escena/escala.ts';
import {
  casaInsuastyExterior,
  casaInsuastyInterior,
} from '../src/core/escenarios/casa-insuasty.ts';
import { ESCENARIOS } from '../src/core/escenarios/catalogo.ts';
import {
  copiasMosaico,
  type DefinicionEscenario,
  envolver,
  xEnPantalla,
  yArriba,
  yColocacion,
} from '../src/core/escenarios/escenario.ts';
import {
  HUIDA_CULTIVOS,
  HUIDA_MONTE,
  HUIDA_QUEBRADA,
} from '../src/core/escenarios/huida.ts';
import { PUENTE_ALTO } from '../src/core/escenarios/puente-alto.ts';

const FUENTES = join(import.meta.dirname, '../art/src');

/** Tamaño del viewBox del SVG fuente de un módulo (1 unidad = 1 px a @1x). */
function tamano(
  def: DefinicionEscenario,
  modulo: string,
): { w: number; h: number } {
  const ruta = join(FUENTES, def.atlas, `${modulo}.svg`);
  expect(existsSync(ruta), `falta ${ruta}`).toBe(true);
  const m = /viewBox="0 0 ([\d.]+) ([\d.]+)"/.exec(readFileSync(ruta, 'utf8'));
  if (!m) throw new Error(`${modulo}: sin viewBox`);
  return { w: Number(m[1]), h: Number(m[2]) };
}

function capasDe(def: DefinicionEscenario) {
  return ORDEN_CAPAS.flatMap((id) => {
    const datos = def.capas[id];
    return datos ? [{ id, datos }] : [];
  });
}

/** Tramos [desde, hasta) que cubren los módulos colocados de una capa, ordenados. */
function tramos(def: DefinicionEscenario, capa: IdCapa) {
  return (def.capas[capa]?.colocaciones ?? [])
    .map((c) => [c.x, c.x + tamano(def, c.modulo).w] as const)
    .sort((a, b) => a[0] - b[0]);
}

/** ¿Los tramos cubren [desde, hasta] sin huecos? */
function cubren(
  t: readonly (readonly [number, number])[],
  desde: number,
  hasta: number,
): boolean {
  let cubierto = desde;
  for (const [a, b] of t) {
    if (a > cubierto) break;
    cubierto = Math.max(cubierto, b);
  }
  return cubierto >= hasta;
}

const capas = capasDe(PUENTE_ALTO);

describe('ayudas de escenario', () => {
  it('el ancla suelo apoya en el suelo de la capa; arriba, en y=0', () => {
    expect(yColocacion({ modulo: 'a', x: 0 }, 'medio')).toBe(
      ySueloCapa(PARALAJE.medio),
    );
    expect(yColocacion({ modulo: 'a', x: 0, ancla: 'arriba' }, 'cielo')).toBe(
      0,
    );
    expect(yArriba({ modulo: 'a', x: 0 }, 'juego', 300)).toBe(Y_SUELO - 300);
  });

  it('las copias de un mosaico cubren la capa sin huecos', () => {
    expect(copiasMosaico(1024, 2784)).toEqual([0, 1024, 2048]);
    expect(() => copiasMosaico(0, 100)).toThrow();
  });

  it('lo que deriva vuelve a entrar por el otro lado', () => {
    expect(envolver(-301, 300, 1920)).toBeCloseTo(1919);
    expect(envolver(1920, 300, 1920)).toBeCloseTo(-300);
    expect(envolver(500, 300, 1920)).toBe(500);
  });

  it('el paralaje desplaza cada capa según su factor', () => {
    expect(xEnPantalla(1000, 'cielo', 2000)).toBe(1000);
    expect(xEnPantalla(1000, 'medio', 2000)).toBe(100);
  });
});

describe.each(Object.entries(ESCENARIOS))('escenario %s', (_nombre, def) => {
  it('cada módulo existe y no pasa del lado máximo', () => {
    for (const { datos } of capasDe(def)) {
      const modulos = [
        ...(datos.mosaicos ?? []).map((m) => m.modulo),
        ...datos.colocaciones.map((c) => c.modulo),
      ];
      for (const modulo of modulos) {
        const { w, h } = tamano(def, modulo);
        expect(w, modulo).toBeLessThanOrEqual(LADO_MAXIMO_MODULO);
        expect(h, modulo).toBeLessThanOrEqual(LADO_MAXIMO_MODULO);
      }
    }
  });

  it('todo queda dentro del ancho de su capa', () => {
    for (const { id, datos } of capasDe(def)) {
      const ancho = anchoCapa(def.anchoNivel, PARALAJE[id]);
      for (const col of datos.colocaciones) {
        const { w } = tamano(def, col.modulo);
        expect(col.x, `${id}/${col.modulo}`).toBeGreaterThanOrEqual(0);
        expect(col.x + w, `${id}/${col.modulo}`).toBeLessThanOrEqual(ancho);
      }
    }
  });

  it('el fondo de cámara es un color de la paleta y solo derivan las nubes', () => {
    expect(() => color(def.fondo ?? 'papel')).not.toThrow();
    for (const { id, datos } of capasDe(def)) {
      for (const col of datos.colocaciones) {
        if (col.deriva) expect(id).toBe<IdCapa>('cielo');
      }
    }
  });

  it('el primer plano no tapa el cuerpo del personaje (queda bajo su suelo o arriba del todo)', () => {
    for (const col of def.capas.frente?.colocaciones ?? []) {
      const { h } = tamano(def, col.modulo);
      const arriba = yArriba(col, 'frente', h);
      if (col.ancla === 'arriba') expect(arriba + h).toBeLessThanOrEqual(300);
      else expect(arriba).toBeGreaterThanOrEqual(Y_SUELO);
    }
  });
});

describe('Puente Alto', () => {
  it('los suelos empiezan en el suelo de su capa y la cubren entera', () => {
    for (const { id, datos } of capas) {
      const ancho = anchoCapa(PUENTE_ALTO.anchoNivel, PARALAJE[id]);
      for (const mosaico of datos.mosaicos ?? []) {
        expect(mosaico.y, mosaico.modulo).toBe(ySueloCapa(PARALAJE[id]));
        const { w } = tamano(PUENTE_ALTO, mosaico.modulo);
        const copias = copiasMosaico(w, ancho);
        expect((copias.at(-1) ?? 0) + w).toBeGreaterThanOrEqual(ancho);
      }
    }
  });

  it('el otro lado de la plaza es una hilera continua de 0 al final de la capa', () => {
    const ancho = anchoCapa(PUENTE_ALTO.anchoNivel, PARALAJE.lejos);
    expect(cubren(tramos(PUENTE_ALTO, 'lejos'), 0, ancho)).toBe(true);
  });

  it('el plano de juego apoya en su suelo', () => {
    for (const col of PUENTE_ALTO.capas.juego?.colocaciones ?? []) {
      expect(yColocacion(col, 'juego')).toBe(Y_SUELO);
    }
  });

  it('P26: la tienda roja y la azul no caben juntas en una foto', () => {
    // Encuadre provisional hasta que exista Camara.ts: foto cuadrada del alto de la pantalla (12
    // exposiciones es el rollo 120 en formato 6×6). Una tienda entra si se ven 120 px de ella.
    const FOTO = VIEWPORT.alto;
    const VISIBLE = 120;
    const tramo = (capa: IdCapa, modulo: string) => {
      const col = PUENTE_ALTO.capas[capa]?.colocaciones.find(
        (c) => c.modulo === modulo,
      );
      if (!col) throw new Error(`falta ${modulo} en ${capa}`);
      return {
        capa,
        desde: col.x,
        hasta: col.x + tamano(PUENTE_ALTO, modulo).w,
      };
    };
    const enPantalla = (
      t: ReturnType<typeof tramo>,
      scroll: number,
    ): [number, number] => [
      Math.max(0, xEnPantalla(t.desde, t.capa, scroll)),
      Math.min(VIEWPORT.ancho, xEnPantalla(t.hasta, t.capa, scroll)),
    ];
    const roja = tramo('juego', 'tienda-roja');
    const azul = tramo('lejos', 'tienda-azul');
    let juntas = 0;
    for (let s = 0; s <= PUENTE_ALTO.anchoNivel - VIEWPORT.ancho; s += 10) {
      const [r0, r1] = enPantalla(roja, s);
      let [a0, a1] = enPantalla(azul, s);
      // la roja, en el plano de juego, tapa lo que la azul tenga detrás
      if (a0 < r1 && a1 > r0) {
        if (a1 > r1) a0 = Math.max(a0, r1);
        else a1 = Math.min(a1, r0);
      }
      if (r1 - r0 < VISIBLE || a1 - a0 < VISIBLE) continue;
      juntas++;
      // la foto más estrecha que muestra VISIBLE px de cada una
      const minima = r0 < a0 ? a0 - r1 + 2 * VISIBLE : r0 - a1 + 2 * VISIBLE;
      expect(minima, `cámara en x=${s}`).toBeGreaterThan(FOTO);
    }
    // y en algún momento se ven las dos a la vez: el jugador elige cuál entra
    expect(juntas).toBeGreaterThan(0);
  });
});

describe('Casa Insuasty', () => {
  const interior = casaInsuastyInterior('prologo');
  const exterior = casaInsuastyExterior('prologo');

  it('el interior es una fila de viñetas y muros cortados, sin huecos', () => {
    expect(cubren(tramos(interior, 'juego'), 0, interior.anchoNivel)).toBe(
      true,
    );
    // cada cuarto queda entre dos muros que montan sobre sus bordes
    const muros = tramos(interior, 'juego').filter(([a, b]) => b - a <= 120);
    for (const cuarto of ['alcoba', 'sala', 'cocina']) {
      const col = interior.capas.juego?.colocaciones.find(
        (c) => c.modulo === cuarto,
      );
      if (!col) throw new Error(`falta ${cuarto}`);
      const fin = col.x + tamano(interior, cuarto).w;
      expect(
        muros.some(([a, b]) => a < col.x && b > col.x),
        cuarto,
      ).toBe(true);
      expect(
        muros.some(([a, b]) => a < fin && b > fin),
        cuarto,
      ).toBe(true);
    }
  });

  it('por fuera, el plano de juego cubre el nivel y lo lejano cubre lo que se ve por los extremos', () => {
    expect(cubren(tramos(exterior, 'juego'), 0, exterior.anchoNivel)).toBe(
      true,
    );
    // Solo el solar y el patio dejan ver el cielo; la casa tapa hasta arriba.
    const conCielo = (exterior.capas.juego?.colocaciones ?? []).filter((c) =>
      ['solar', 'patio'].includes(c.modulo),
    );
    const maximo = exterior.anchoNivel - VIEWPORT.ancho;
    for (let s = 0; s <= maximo; s += 20) {
      for (const col of conCielo) {
        const w = tamano(exterior, col.modulo).w;
        const desde = Math.max(0, col.x - s);
        const hasta = Math.min(VIEWPORT.ancho, col.x + w - s);
        if (hasta <= desde) continue;
        for (const capa of ['lejos', 'medio'] as const) {
          const f = PARALAJE[capa];
          expect(
            cubren(tramos(exterior, capa), desde + s * f, hasta + s * f),
            `${capa} con la cámara en ${s}`,
          ).toBe(true);
        }
      }
    }
  });

  it('cada acto tiene los mismos módulos', () => {
    for (const lugar of ['interior', 'exterior']) {
      const prologo = readdirSync(
        join(FUENTES, `fondos/casa-insuasty/${lugar}-prologo`),
      ).sort();
      const acto1 = readdirSync(
        join(FUENTES, `fondos/casa-insuasty/${lugar}-acto1`),
      ).sort();
      expect(acto1, lugar).toEqual(prologo);
    }
  });
});

describe('Huida de la M2', () => {
  it('cada tramo es del Acto I y su plano de juego cubre el nivel', () => {
    for (const def of [HUIDA_CULTIVOS, HUIDA_QUEBRADA, HUIDA_MONTE]) {
      expect(def.acto).toBe('acto1');
      expect(cubren(tramos(def, 'juego'), 0, def.anchoNivel), def.atlas).toBe(
        true,
      );
    }
  });

  it('el cielo asoma por encima de los cultivos y del monte: lo lejano y lo medio no tienen huecos', () => {
    for (const def of [HUIDA_CULTIVOS, HUIDA_MONTE]) {
      for (const capa of ['lejos', 'medio'] as const) {
        const ancho = anchoCapa(def.anchoNivel, PARALAJE[capa]);
        expect(
          cubren(tramos(def, capa), 0, ancho),
          `${def.atlas} ${capa}`,
        ).toBe(true);
      }
    }
    // en la quebrada, las paredes (capa media) encierran la vista de punta a punta
    const ancho = anchoCapa(HUIDA_QUEBRADA.anchoNivel, PARALAJE.medio);
    expect(cubren(tramos(HUIDA_QUEBRADA, 'medio'), 0, ancho)).toBe(true);
  });
});
