import type { GameObjects, Scene } from 'phaser';
import {
  type OpcionesCarrera,
  poseCarrera,
  velocidadCarrera,
} from '../core/animacion/carrera.ts';
import { animarCiclo, type Caminata } from './Caminata.ts';

/**
 * Aplica la carrera procedural (core/animacion/carrera.ts) a un personaje armado con
 * armarRecorte(), en su pose de correr (canillas con pivote en la rodilla).
 */
export type OpcionesCorrer = OpcionesCarrera & {
  /** Duración de un ciclo completo (dos zancadas) en ms. */
  ciclo?: number;
  /** Ángulos que se suman a la pose (postura de la expresión), leídos en cada cuadro. */
  postura?: Readonly<Record<string, number>>;
};

export function correr(
  escena: Scene,
  contenedor: GameObjects.Container,
  piezas: Map<string, GameObjects.Container>,
  { ciclo = 640, postura = {}, ...opciones }: OpcionesCorrer = {},
): Caminata {
  const tween = animarCiclo(
    escena,
    contenedor,
    piezas,
    ciclo,
    (fase) => poseCarrera(fase, opciones),
    postura,
  );
  return { tween, velocidad: velocidadCarrera(ciclo, opciones) };
}
