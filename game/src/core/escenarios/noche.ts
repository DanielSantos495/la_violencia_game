/**
 * Noche de tinta (estilo B) en vivo: el momento en que llama la Seccional o llega la partida
 * (planeacion/arte/tomo1/escenarios/casa-insuasty.md §7; paleta.md §5, camino (b)). Los fondos van
 * con la noche sepia (C) ya dibujada; este filtro hunde en tinta lo que está en sombra y deja lo
 * que toca la luz.
 *
 * Es una sola matriz de color que aleja cada color del papel: c' = papel + k·(c − papel). Así:
 * - el papel queda igual (los canales entre viñetas siguen siendo papel);
 * - el encalado bajo la noche sepia de afuera cae justo en tinta, y lo más oscuro, a casi negro;
 * - la luz, que está cerca del papel, apenas cambia; el rojo y el azul guardan su tono (más hondos);
 * - los escalones de luz de adentro caen casi donde los pinta la noche de tinta dibujada
 *   (`ESTILOS_NOCHE['tinta']` en art/gen/casa_insuasty.py).
 *
 * Recibe el papel y la tinta en vez de leer la paleta para que sirva también en las herramientas
 * de Node (tools/art-escena.ts), que no importan JSON.
 */

export type Rgb = readonly [number, number, number];
type Canal = 0 | 1 | 2;

/** Papel y tinta de la paleta, en RGB de 0 a 1. */
export interface PapelYTinta {
  readonly papel: Rgb;
  readonly tinta: Rgb;
}

function porCanal(f: (c: Canal) => number): Rgb {
  return [f(0), f(1), f(2)];
}

/** #rrggbb en RGB de 0 a 1. */
export function hexARgb(hex: string): Rgb {
  const n = Number.parseInt(hex.slice(1), 16);
  return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
}

/** Luminancia con los pesos de los generadores (art/gen/casa_insuasty.py, `de_noche`). */
export function luminancia(c: Rgb): number {
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
}

/** Cuánta tinta lleva afuera la noche sepia: `ESTILOS_NOCHE['sepia']['afuera']` en casa_insuasty.py. */
export const NOCHE_SEPIA_AFUERA = 0.8;

/** Un color bajo la noche sepia (C), como lo pinta `de_noche`: su luz sobre papel y `a` de tinta. */
export function nocheSepia(
  c: Rgb,
  a: number,
  { papel, tinta }: PapelYTinta,
): Rgb {
  return porCanal((i) => (1 - a) * luminancia(c) * papel[i] + a * tinta[i]);
}

/** Cuánto se aleja cada color del papel: lo justo para que el encalado de afuera caiga en tinta. */
export function factorNocheDeTinta(colores: PapelYTinta): number {
  const { papel, tinta } = colores;
  const encalado = nocheSepia(papel, NOCHE_SEPIA_AFUERA, colores);
  return (
    (luminancia(papel) - luminancia(tinta)) /
    (luminancia(papel) - luminancia(encalado))
  );
}

/** Matriz de color de la noche de tinta (formato de Phaser: 4×5, desplazamientos de 0 a 255). */
export function matrizNocheDeTinta(colores: PapelYTinta): number[] {
  const { papel } = colores;
  const k = factorNocheDeTinta(colores);
  return [
    ...[k, 0, 0, 0, (1 - k) * papel[0] * 255],
    ...[0, k, 0, 0, (1 - k) * papel[1] * 255],
    ...[0, 0, k, 0, (1 - k) * papel[2] * 255],
    ...[0, 0, 0, 1, 0],
  ];
}

/**
 * Lo que hace el filtro con un color opaco con la intensidad t (el `alpha` de la matriz: 0 no
 * cambia nada, 1 es la noche de tinta entera). Para tests y revisión.
 */
export function nocheDeTinta(t: number, c: Rgb, colores: PapelYTinta): Rgb {
  const { papel } = colores;
  const k = factorNocheDeTinta(colores);
  return porCanal((i) => {
    const filtrado = papel[i] + k * (c[i] - papel[i]);
    return Math.min(1, Math.max(0, c[i] + t * (filtrado - c[i])));
  });
}
