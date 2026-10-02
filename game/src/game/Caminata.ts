import type { GameObjects, Scene, Tweens } from 'phaser';
import {
  type OpcionesCaminata,
  poseCaminata,
  velocidadCaminata,
  ZANCADA_POR_DEFECTO,
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

export function caminar(
  escena: Scene,
  contenedor: GameObjects.Container,
  piezas: Map<string, GameObjects.Container>,
  {
    ciclo = 1000,
    largoPierna = 222,
    ...opciones
  }: OpcionesCaminata & { ciclo?: number; largoPierna?: number } = {},
): Caminata {
  const yBase = contenedor.y;
  const yInicial = new Map([...piezas].map(([id, p]) => [id, p.y]));

  const tween = escena.tweens.addCounter({
    from: 0,
    to: 1,
    duration: ciclo,
    repeat: -1,
    onUpdate: (tw: Tweens.Tween) => {
      const pose = poseCaminata((tw.getValue() ?? 0) * Math.PI * 2, opciones);
      for (const [id, angulo] of Object.entries(pose.angulos)) {
        const pieza = piezas.get(id);
        if (pieza) pieza.angle = angulo;
      }
      for (const [id, px] of Object.entries(pose.levante)) {
        const pieza = piezas.get(id);
        if (pieza) pieza.y = (yInicial.get(id) ?? 0) - px;
      }
      contenedor.y = yBase - pose.rebote;
    },
  });

  return {
    tween,
    velocidad: velocidadCaminata(
      largoPierna,
      ciclo,
      opciones.zancada ?? ZANCADA_POR_DEFECTO,
    ),
  };
}
