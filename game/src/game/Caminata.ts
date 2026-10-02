import type { GameObjects, Scene, Tweens } from 'phaser';
import {
  type OpcionesCaminata,
  poseCaminata,
  velocidadCaminata,
} from '../core/animacion/caminata.ts';

/**
 * Aplica la caminata procedural (core/animacion/caminata.ts) a un personaje armado con
 * armarRecorte(). Un solo contador de fase mueve todo; las piezas ausentes se ignoran.
 */
export interface Caminata {
  tween: Tweens.Tween;
  /** Velocidad de avance en px/s (escala 1) que hace coincidir pies y suelo. */
  velocidad: number;
}

export type OpcionesCaminar = OpcionesCaminata & {
  /** Duración de un ciclo completo (dos pasos) en ms. */
  ciclo?: number;
  /** Largo de pierna (cadera → suelo) en px del SVG; solo modo cadera. */
  largoPierna?: number;
  /**
   * Ángulos que se suman a la pose (postura de la expresión). Se lee en cada cuadro, así
   * un cambio de expresión se nota mientras camina.
   */
  postura?: Readonly<Record<string, number>>;
};

export function caminar(
  escena: Scene,
  contenedor: GameObjects.Container,
  piezas: Map<string, GameObjects.Container>,
  {
    ciclo = 1000,
    largoPierna = 222,
    postura = {},
    ...opciones
  }: OpcionesCaminar = {},
): Caminata {
  const yBase = contenedor.y;
  const reposo = new Map(
    [...piezas].map(([id, p]) => [id, { x: p.x, y: p.y }]),
  );

  const tween = escena.tweens.addCounter({
    from: 0,
    to: 1,
    duration: ciclo,
    repeat: -1,
    onUpdate: (tw: Tweens.Tween) => {
      const pose = poseCaminata((tw.getValue() ?? 0) * Math.PI * 2, opciones);
      for (const [id, pieza] of piezas) {
        if (id in pose.angulos || id in postura) {
          pieza.angle = (pose.angulos[id] ?? 0) + (postura[id] ?? 0);
        }
        const r = reposo.get(id);
        if (!r) continue;
        pieza.x = r.x + (pose.avance[id] ?? 0);
        pieza.y = r.y - (pose.levante[id] ?? 0);
      }
      contenedor.y = yBase - pose.rebote;
    },
  });

  return { tween, velocidad: velocidadCaminata(ciclo, opciones, largoPierna) };
}
