import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
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
  copiasMosaico,
  envolver,
  xEnPantalla,
  yArriba,
  yColocacion,
} from '../src/core/escenarios/escenario.ts';
import { PUENTE_ALTO } from '../src/core/escenarios/puente-alto.ts';

const FUENTES = join(import.meta.dirname, '../art/src');

/** Tamaño del viewBox del SVG fuente de un módulo (1 unidad = 1 px a @1x). */
function tamano(modulo: string): { w: number; h: number } {
  const ruta = join(FUENTES, PUENTE_ALTO.atlas, `${modulo}.svg`);
  expect(existsSync(ruta), `falta ${ruta}`).toBe(true);
  const m = /viewBox="0 0 ([\d.]+) ([\d.]+)"/.exec(readFileSync(ruta, 'utf8'));
  if (!m) throw new Error(`${modulo}: sin viewBox`);
  return { w: Number(m[1]), h: Number(m[2]) };
}

const capas = ORDEN_CAPAS.flatMap((id) => {
  const datos = PUENTE_ALTO.capas[id];
  return datos ? [{ id, datos }] : [];
});

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

describe('Puente Alto', () => {
  it('cada módulo existe y no pasa del lado máximo', () => {
    for (const { datos } of capas) {
      const modulos = [
        ...(datos.mosaicos ?? []).map((m) => m.modulo),
        ...datos.colocaciones.map((c) => c.modulo),
      ];
      for (const modulo of modulos) {
        const { w, h } = tamano(modulo);
        expect(w, modulo).toBeLessThanOrEqual(LADO_MAXIMO_MODULO);
        expect(h, modulo).toBeLessThanOrEqual(LADO_MAXIMO_MODULO);
      }
    }
  });

  it('todo queda dentro del ancho de su capa', () => {
    for (const { id, datos } of capas) {
      const ancho = anchoCapa(PUENTE_ALTO.anchoNivel, PARALAJE[id]);
      for (const col of datos.colocaciones) {
        const { w } = tamano(col.modulo);
        expect(col.x, `${id}/${col.modulo}`).toBeGreaterThanOrEqual(0);
        expect(col.x + w, `${id}/${col.modulo}`).toBeLessThanOrEqual(ancho);
      }
    }
  });

  it('los suelos empiezan en el suelo de su capa y la cubren entera', () => {
    for (const { id, datos } of capas) {
      const ancho = anchoCapa(PUENTE_ALTO.anchoNivel, PARALAJE[id]);
      for (const mosaico of datos.mosaicos ?? []) {
        expect(mosaico.y, mosaico.modulo).toBe(ySueloCapa(PARALAJE[id]));
        const { w } = tamano(mosaico.modulo);
        const copias = copiasMosaico(w, ancho);
        expect((copias.at(-1) ?? 0) + w).toBeGreaterThanOrEqual(ancho);
      }
    }
  });

  it('el otro lado de la plaza es una hilera continua de 0 al final de la capa', () => {
    const ancho = anchoCapa(PUENTE_ALTO.anchoNivel, PARALAJE.lejos);
    const tramos = (PUENTE_ALTO.capas.lejos?.colocaciones ?? [])
      .map((c) => [c.x, c.x + tamano(c.modulo).w] as const)
      .sort((a, b) => a[0] - b[0]);
    let cubierto = 0;
    for (const [desde, hasta] of tramos) {
      expect(desde).toBeLessThanOrEqual(cubierto);
      cubierto = Math.max(cubierto, hasta);
    }
    expect(cubierto).toBeGreaterThanOrEqual(ancho);
  });

  it('solo derivan las nubes del cielo, y el plano de juego apoya en su suelo', () => {
    for (const { id, datos } of capas) {
      for (const col of datos.colocaciones) {
        if (col.deriva) expect(id).toBe<IdCapa>('cielo');
        if (id === 'juego') expect(yColocacion(col, id)).toBe(Y_SUELO);
      }
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
      return { capa, desde: col.x, hasta: col.x + tamano(modulo).w };
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

  it('el primer plano no tapa el cuerpo del personaje (queda bajo su suelo o arriba del todo)', () => {
    for (const col of PUENTE_ALTO.capas.frente?.colocaciones ?? []) {
      const { h } = tamano(col.modulo);
      const arriba = yArriba(col, 'frente', h);
      if (col.ancla === 'arriba') expect(arriba + h).toBeLessThanOrEqual(300);
      else expect(arriba).toBeGreaterThanOrEqual(Y_SUELO);
    }
  });
});
