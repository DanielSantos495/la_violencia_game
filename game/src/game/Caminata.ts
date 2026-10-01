import type { GameObjects, Scene } from 'phaser';

/**
 * Ciclo de caminata por tweens para un personaje cut-out armado con armarRecorte().
 * Piernas y brazos en contrafase, rebote del cuerpo dos veces por ciclo y prendas
 * (falda, ruana, trenza) que siguen el movimiento con retraso, como tela.
 * Las piezas ausentes se ignoran: sirve para cualquier personaje con la convención de ids.
 */
export interface OpcionesCaminata {
  /** Duración de un paso en ms (medio ciclo). */
  paso?: number;
  /** Amplitud de las piernas en grados. */
  zancada?: number;
}

export function caminar(
  escena: Scene,
  contenedor: GameObjects.Container,
  piezas: Map<string, GameObjects.Image>,
  { paso = 420, zancada = 9 }: OpcionesCaminata = {},
): void {
  const balancear = (
    id: string,
    desde: number,
    hasta: number,
    retraso = 0,
    duracion = paso,
  ): void => {
    const pieza = piezas.get(id);
    if (!pieza) return;
    pieza.setAngle(desde);
    escena.tweens.add({
      targets: pieza,
      angle: hasta,
      duration: duracion,
      delay: retraso,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut',
    });
  };

  balancear('pierna-der', -zancada, zancada);
  balancear('pierna-izq', zancada, -zancada);
  balancear('brazo-der', zancada * 1.2, -zancada * 1.2);
  balancear('brazo-izq', -zancada * 1.2, zancada * 1.2);
  balancear('falda', -1.5, 1.5, paso * 0.25);
  balancear('ruana', -1, 1, paso * 0.35);
  balancear('ruana-doblez', -1, 1, paso * 0.35);
  balancear('trenza', 5, -5, paso * 0.5);
  balancear('cabeza', -1, 1, 0, paso * 2);
  balancear('sombrero', -1, 1, 0, paso * 2);
  balancear('panuelo', -2, 2, paso * 0.3);

  // Rebote: el cuerpo sube en el paso de apoyo, dos veces por ciclo.
  escena.tweens.add({
    targets: contenedor,
    y: contenedor.y - 4,
    duration: paso / 2,
    yoyo: true,
    repeat: -1,
    ease: 'Sine.easeInOut',
  });
}
