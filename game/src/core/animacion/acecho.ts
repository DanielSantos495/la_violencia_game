/**
 * Pose de acecho (agachada, quieta) para personajes cut-out. Función pura del tiempo.
 *
 * - Respiración contenida: la ruana sube y baja apenas.
 * - Mirada: la cabeza explora adelante y atrás con dos senos de periodo distinto, así el
 *   movimiento no se repite de forma mecánica.
 * - El brazo de apoyo se mueve con el cuerpo y el antebrazo compensa para que la mano
 *   siga en el suelo.
 * - Trenza y zarcillo siguen con inercia.
 */
export interface PoseAcecho {
  angulos: Record<string, number>;
}

export function poseAcecho(segundos: number): PoseAcecho {
  const respiracion = Math.sin(segundos * 2.4);
  const mirada =
    -5 * Math.sin(segundos * 0.7) + 2.5 * Math.sin(segundos * 1.9 + 1);
  const balanceo = 1.2 * Math.sin(segundos * 0.9);
  return {
    angulos: {
      cabeza: mirada,
      ruana: 0.7 * respiracion,
      'ruana-doblez': 0.7 * respiracion,
      'brazo-der': balanceo,
      'antebrazo-der': -balanceo,
      trenza: 2 * Math.sin(segundos * 0.7 - 0.8) + 0.6 * respiracion,
      zarcillo: 6 * Math.sin(segundos * 1.9),
    },
  };
}
