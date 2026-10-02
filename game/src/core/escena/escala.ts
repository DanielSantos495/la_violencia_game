/**
 * Contrato de escala y capas de los escenarios (sin Phaser). Las razones y la tabla están en
 * planeacion/arte/tomo1/escenarios/contrato_escala.md; aquí viven las cifras.
 */

/** Resolución base (doc 04 §8). */
export const VIEWPORT = { ancho: 1920, alto: 1080 } as const;

/** Escala del plano de juego: píxeles (a @1x) por metro. */
export const PX_POR_METRO = 200;

/** Línea de suelo del plano de juego. */
export const Y_SUELO = 900;

/** Altura del mundo visible sobre el suelo del plano de juego, en metros (4,5 m). */
export const ALTURA_VISIBLE_M = Y_SUELO / PX_POR_METRO;

/** Altura de los ojos de quien mira, en metros: fija el horizonte. */
export const ALTURA_OJOS_M = 1.6;

/** Horizonte: altura de los ojos de alguien de pie en el plano de juego. */
export const Y_HORIZONTE = Y_SUELO - ALTURA_OJOS_M * PX_POR_METRO;

export type IdCapa = 'cielo' | 'lejos' | 'medio' | 'juego' | 'frente';

/** Factor de paralaje de cada capa (1 = se mueve con la cámara, como el personaje). */
export const PARALAJE: Readonly<Record<IdCapa, number>> = {
  cielo: 0,
  lejos: 0.15,
  medio: 0.45,
  juego: 1,
  frente: 1.3,
};

/** Orden de dibujo de las capas, del fondo al frente. */
export const ORDEN_CAPAS: readonly IdCapa[] = [
  'cielo',
  'lejos',
  'medio',
  'juego',
  'frente',
];

/** Escala de los objetos de una capa: los planos lejanos se dibujan más pequeños. */
export function pxPorMetroCapa(paralaje: number): number {
  return PX_POR_METRO * paralaje;
}

/** Línea de suelo de una capa: los planos lejanos apoyan más cerca del horizonte. */
export function ySueloCapa(paralaje: number): number {
  return Y_HORIZONTE + (Y_SUELO - Y_HORIZONTE) * paralaje;
}

/** Ancho que debe cubrir una capa para un nivel de `anchoNivel` px en el plano de juego. */
export function anchoCapa(anchoNivel: number, paralaje: number): number {
  return VIEWPORT.ancho + (anchoNivel - VIEWPORT.ancho) * paralaje;
}

/**
 * Escala a aplicar a un personaje para que mida su estatura de diseño en el plano de juego.
 * `alturaDibujoPx`: de la coronilla a la suela, en px del SVG.
 */
export function escalaPersonaje(
  estaturaM: number,
  alturaDibujoPx: number,
): number {
  if (estaturaM <= 0 || alturaDibujoPx <= 0) {
    throw new Error('Estatura y altura dibujada deben ser positivas');
  }
  return (PX_POR_METRO * estaturaM) / alturaDibujoPx;
}

/** Lado máximo de un módulo de fondo a @1x (a @2x llena una página de atlas de 4096 px). */
export const LADO_MAXIMO_MODULO = 2048;
