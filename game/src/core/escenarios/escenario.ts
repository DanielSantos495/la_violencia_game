/**
 * Definición pura de un escenario por capas (sin Phaser): qué módulo va en cada capa y dónde.
 * Escala, suelos y paralaje: src/core/escena/escala.ts (contrato_escala.md). Los módulos son
 * SVG de una carpeta de art/src y salen en un mismo atlas (src/core/arte/atlas.ts).
 */
import { type IdCapa, PARALAJE, ySueloCapa } from '../escena/escala.ts';

/** Cómo se apoya un módulo: por la base de su viewBox (suelo) o por su borde de arriba. */
export type Ancla = 'suelo' | 'arriba';

export interface Colocacion {
  /** Nombre del SVG en la carpeta del atlas, sin extensión (p. ej. 'iglesia'). */
  modulo: string;
  /** Borde izquierdo en coordenadas de la capa. */
  x: number;
  /** Por defecto, el suelo de la capa (ancla 'suelo') o 0 (ancla 'arriba'). */
  y?: number;
  ancla?: Ancla;
  /** Volteo horizontal en el sitio: ocupa el mismo rectángulo. */
  espejo?: boolean;
  /** Desplazamiento propio en px/s (nubes); al salir de cuadro vuelve por el otro lado. */
  deriva?: number;
}

/** Módulo que se repite en x para cubrir todo el ancho de la capa (suelos). */
export interface Mosaico {
  modulo: string;
  /** Borde de arriba del mosaico. */
  y: number;
}

export interface CapaEscenario {
  mosaicos?: readonly Mosaico[];
  /** En orden de dibujo: lo primero queda detrás. */
  colocaciones: readonly Colocacion[];
}

export interface DefinicionEscenario {
  /** Grupo del atlas: la carpeta de los SVG en art/src (p. ej. 'fondos/puente-alto'). */
  atlas: string;
  /** Ancho del nivel en el plano de juego, en px. */
  anchoNivel: number;
  capas: Partial<Record<IdCapa, CapaEscenario>>;
}

/** Nombre del frame de un módulo en el atlas del escenario. */
export function frameDe(def: DefinicionEscenario, modulo: string): string {
  return `${def.atlas}/${modulo}`;
}

/** y del punto de anclaje de una colocación en su capa. */
export function yColocacion(col: Colocacion, capa: IdCapa): number {
  if (col.y !== undefined) return col.y;
  return col.ancla === 'arriba' ? 0 : ySueloCapa(PARALAJE[capa]);
}

/** Borde de arriba de un módulo colocado, conocida su altura. */
export function yArriba(col: Colocacion, capa: IdCapa, alto: number): number {
  const y = yColocacion(col, capa);
  return col.ancla === 'arriba' ? y : y - alto;
}

/** x de cada copia de un mosaico para cubrir [0, anchoCapa]. */
export function copiasMosaico(
  anchoModulo: number,
  anchoCapa: number,
): number[] {
  if (anchoModulo <= 0) throw new Error('El módulo del mosaico no tiene ancho');
  const copias: number[] = [];
  for (let x = 0; x < anchoCapa; x += anchoModulo) copias.push(x);
  return copias;
}

/** x en pantalla de un punto de una capa con la cámara en `scrollX` (paralaje). */
export function xEnPantalla(x: number, capa: IdCapa, scrollX: number): number {
  return x - scrollX * PARALAJE[capa];
}

/** Lleva x a [-ancho, anchoVista): lo que deriva y sale por un lado entra por el otro. */
export function envolver(x: number, ancho: number, anchoVista: number): number {
  const periodo = anchoVista + ancho;
  return ((((x + ancho) % periodo) + periodo) % periodo) - ancho;
}
