import type { GameObjects, Scene, Tweens } from 'phaser';
import {
  type OpcionesCaminata,
  type PoseCaminata,
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
  const tween = animarCiclo(
    escena,
    contenedor,
    piezas,
    ciclo,
    (fase) => poseCaminata(fase, opciones),
    postura,
  );
  return { tween, velocidad: velocidadCaminata(ciclo, opciones, largoPierna) };
}

/**
 * Repite en bucle una pose cíclica (caminata, carrera…): un solo contador de fase 0..2π mueve
 * ángulos, desplazamientos de pieza y rebote del contenedor. Las piezas ausentes se ignoran.
 */
export function animarCiclo(
  escena: Scene,
  contenedor: GameObjects.Container,
  piezas: Map<string, GameObjects.Container>,
  ciclo: number,
  pose: (fase: number) => PoseCaminata,
  postura: Readonly<Record<string, number>> = {},
): Tweens.Tween {
  const yBase = contenedor.y;
  const reposo = new Map(
    [...piezas].map(([id, p]) => [id, { x: p.x, y: p.y }]),
  );
  return escena.tweens.addCounter({
    from: 0,
    to: 1,
    duration: ciclo,
    repeat: -1,
    onUpdate: (tw: Tweens.Tween) => {
      const p = pose((tw.getValue() ?? 0) * Math.PI * 2);
      for (const [id, pieza] of piezas) {
        if (id in p.angulos || id in postura) {
          pieza.angle = (p.angulos[id] ?? 0) + (postura[id] ?? 0);
        }
        const r = reposo.get(id);
        if (!r) continue;
        pieza.x = r.x + (p.avance[id] ?? 0);
        pieza.y = r.y - (p.levante[id] ?? 0);
      }
      contenedor.y = yBase - p.rebote;
    },
  });
}
