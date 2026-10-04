/**
 * Casa de los Insuasty, de noche: Prólogo b4 (la reunión para oír la radio, P27) y Misión 2 b2–b4
 * (la partida y la huida, P24–P28) (doc 02 §5). Composición y fuentes:
 * planeacion/arte/tomo1/escenarios/casa-insuasty.md.
 * Módulos: game/art/gen/casa_insuasty.py → art/src/fondos/casa-insuasty/<lugar>-<acto>/*.svg. Cada
 * acto tiene su atlas, con el croma de su guion de color (paleta.md §5).
 */
import type { DefinicionEscenario } from './escenario.ts';

/** Actos en los que sale la casa: el Prólogo (1946) y el Acto I (Misión 2, 1948). */
export type ActoCasa = 'prologo' | 'acto1';

const arriba = (modulo: string, x: number, y = 0) =>
  ({ modulo, x, y, ancla: 'arriba' }) as const;

/**
 * Interior en corte, visto desde el solar: alcoba, sala y cocina son viñetas de la página y los
 * muros cortados son el papel entre ellas; por sus puertas se pasa de un cuarto a otro.
 */
export function casaInsuastyInterior(acto: ActoCasa): DefinicionEscenario {
  return {
    atlas: `fondos/casa-insuasty/interior-${acto}`,
    anchoNivel: 3220,
    capas: {
      juego: {
        colocaciones: [
          arriba('alcoba', 110),
          arriba('sala', 1010),
          arriba('cocina', 2310),
          arriba('muro-oeste', 0),
          arriba('puerta-alcoba', 900),
          arriba('puerta-cocina', 2200),
          arriba('muro-este', 3100),
        ],
      },
    },
  };
}

/**
 * La casa por fuera, desde el patio y de noche: el solar con la senda de la huida (izquierda), la
 * fachada (cocina, sala, alcoba) y el portillo al camino de Puente Alto (derecha).
 */
export function casaInsuastyExterior(acto: ActoCasa): DefinicionEscenario {
  return {
    atlas: `fondos/casa-insuasty/exterior-${acto}`,
    anchoNivel: 4600,
    fondo: 'sepia-oscuro',
    capas: {
      cielo: { colocaciones: [arriba('cielo-noche', 0)] },
      // Solo se ven por los extremos del nivel (la casa tapa el centro): lx 0–900 y 1520–2322.
      lejos: {
        colocaciones: [
          arriba('lomas-oeste', 0, 380),
          arriba('lomas-este', 1300, 380),
        ],
      },
      // mx 0–900 a la izquierda y 2326–3126 a la derecha; la casa de los vecinos queda del lado
      // del camino.
      medio: {
        colocaciones: [
          arriba('campo-oeste', 0, 120),
          arriba('campo-este', 2200, 120),
        ],
      },
      juego: {
        colocaciones: [
          arriba('solar', 0),
          arriba('casa-cocina', 900),
          arriba('casa-sala', 1900),
          arriba('casa-alcoba', 3100),
          arriba('patio', 3800),
        ],
      },
      // Matas de fique con la base bajo el cuadro: solo asoman las puntas, por debajo de los pies.
      frente: {
        colocaciones: [
          { modulo: 'maguey', x: 700, y: 1240 },
          { modulo: 'maguey', x: 2900, y: 1250, espejo: true },
          { modulo: 'maguey', x: 4800, y: 1240 },
        ],
      },
    },
  };
}
