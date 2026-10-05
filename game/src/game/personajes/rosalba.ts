import { escalaPersonaje } from '../../core/escena/escala.ts';
import type { OpcionesCaminar } from '../Caminata.ts';
import type { OpcionesCorrer } from '../Carrera.ts';
import type { DefinicionPose } from '../Personaje.ts';

/**
 * Poses dibujadas de Rosalba (game/art/src/personajes/). Las piezas van en orden de
 * dibujo; la jerarquía (data-padre) llega desde el atlas. Hoja de personaje:
 * planeacion/arte/tomo1/personajes/rosalba.md.
 */

/**
 * Estatura de diseño (hoja de personaje §1): campesina boyacense nacida hacia 1927. Ver la
 * fuente y el cálculo en planeacion/arte/tomo1/personajes/rosalba.md.
 */
export const ESTATURA_ROSALBA_M = 1.52;

/**
 * Altura dibujada de pie, de la coronilla a la suela (px del SVG, con trazo). La guarda
 * tests/rosalba-arte.test.ts la vuelve a medir en el SVG.
 */
export const ALTURA_DIBUJO_ROSALBA_PX = 433;

/** Escala en el plano de juego según el contrato de escala (core/escena/escala.ts). */
export const ESCALA_ROSALBA = escalaPersonaje(
  ESTATURA_ROSALBA_M,
  ALTURA_DIBUJO_ROSALBA_PX,
);

/**
 * Cómo camina Rosalba: con falda casi al tobillo las piernas no giran desde la cadera; los
 * pies se deslizan bajo el ruedo (pivote en el tobillo) con pasos cortos y rápidos.
 * La guarda tests/rosalba-arte.test.ts comprueba que ninguna pierna salga de la falda.
 */
export const CAMINATA_ROSALBA: OpcionesCaminar = {
  faldaLarga: true,
  ciclo: 740,
};

/**
 * Cómo corre (huida de la M2): falda recogida con la mano derecha, canillas de 128 px con
 * pivote en la rodilla (rosalba-corriendo.svg). Ciclo de 0,62 s: ~2 m/s en escena.
 */
export const CARRERA_ROSALBA: OpcionesCorrer = { largo: 128, ciclo: 620 };

/**
 * Cómo camina en el Llano (Acto II en adelante): con la falda a media canilla se ven las
 * canillas, que giran en la rodilla oculta bajo la falda (modo canilla de caminata.ts), con
 * pasos más largos que en Boyacá: ~0,74 m/s en escena. Guarda en tests/rosalba-arte.test.ts.
 */
export const CAMINATA_LLANO: OpcionesCaminar = { canilla: true, ciclo: 820 };

/** Cómo corre en el Llano: nada que recoger, así que bracean los dos brazos. */
export const CARRERA_LLANO: OpcionesCorrer = {
  largo: 128,
  ciclo: 620,
  bracea: 'ambos',
};

/**
 * Actos del guion de color (planeacion/arte/tomo1/paleta.md §5; ids de `guion` en
 * game/art/paleta.json). Rosalba cruza todos: art/gen/rosalba.py la genera una vez por acto con
 * el croma del mundo de ese acto. La cinta roja (partido) no cambia en ningún acto.
 */
export type ActoRosalba = 'prologo' | 'acto1' | 'acto2' | 'acto3' | 'epilogo';
/** Actos con el traje de mercado: Prólogo y Acto I antes del ataque. */
export type ActoMercado = Extract<ActoRosalba, 'prologo' | 'acto1'>;
/** Actos con la variante monte: desde la M2 (Acto I). */
export type ActoMonte = Exclude<ActoRosalba, 'prologo'>;
/** Actos con la variante Llano: Acto II en adelante (gastada en el Acto III y el Epílogo). */
export type ActoLlano = Extract<ActoRosalba, 'acto2' | 'acto3' | 'epilogo'>;

/**
 * Atlas de Rosalba en un acto (clave de textura y carpeta de art/src): el Prólogo, con la paleta
 * entera, en personajes/; los demás actos en personajes/<acto>/, solo con los dibujos que usan.
 * Cada escena carga el de su acto: `cargarAtlas(this, atlasRosalba('acto2'))`.
 */
export function atlasRosalba(acto: ActoRosalba): string {
  return acto === 'prologo' ? 'personajes' : `personajes/${acto}`;
}

/** Base del retrato en tres cuartos de un acto, para `Retrato`. */
export function retratoRosalba(acto: ActoRosalba = 'prologo'): string {
  return `${atlasRosalba(acto)}/rosalba-retrato`;
}

/** Punto de apoyo entre los pies, común a todas las poses (coordenadas del SVG). */
export const APOYO_ROSALBA = { x: 150, y: 474 };

/**
 * La cinta roja de la trenza es una pieza propia (hija de `trenza`): en la historia se la quitan
 * (Prólogo b4) y va sin ella desde la M2 hasta que vuelve a atársela en el Acto II
 * (planeacion/historia/tomo1/10_registro_propuestas.md P31–P32). Sin cinta, la trenza termina
 * en un amarre oscuro: `new Personaje(..., { ocultas: [PIEZA_CINTA] })` o `mostrarPieza`.
 */
export const PIEZA_CINTA = 'cinta';

/**
 * Faja de cuero con el cuchillo (variante Llano), pieza propia: si se desmoviliza (doc 02,
 * M7) va sin ella: `ocultas: [PIEZA_FAJA]` o `mostrarPieza(PIEZA_FAJA, false)`.
 */
export const PIEZA_FAJA = 'faja';

/**
 * Traje de mercado, de pie. Las cabezas por expresión (core/animacion/expresiones.ts) tienen
 * el mismo pivote que la pieza `cabeza`.
 */
export function rosalbaMercado(
  acto: ActoMercado = 'prologo',
): Record<string, DefinicionPose> {
  const atlas = atlasRosalba(acto);
  return {
    'de-pie': {
      base: `${atlas}/rosalba`,
      cabezas: `${atlas}/rosalba-cabezas`,
      piezas: [
        'brazo-izq',
        'antebrazo-izq',
        'pierna-izq',
        'pierna-der',
        'enagua',
        'falda',
        'torso',
        'cabeza',
        'zarcillo',
        'sombrero',
        'brazo-der',
        'antebrazo-der',
        'panolon',
        'trenza',
        'cinta',
      ],
    },
  };
}

/** Variante monte: de pie, corriendo (huida) y agachada (sigilo). */
export function rosalbaMonte(
  acto: ActoMonte = 'acto1',
): Record<string, DefinicionPose> {
  const atlas = atlasRosalba(acto);
  return {
    'de-pie': {
      base: `${atlas}/rosalba-monte`,
      cabezas: `${atlas}/rosalba-cabezas`,
      piezas: [
        'brazo-izq',
        'antebrazo-izq',
        'pierna-izq',
        'pierna-der',
        'enagua',
        'falda',
        'torso',
        'cabeza',
        'zarcillo',
        'mechones',
        'ruana',
        'trenza',
        'cinta',
        'brazo-der',
        'antebrazo-der',
        'ruana-doblez',
      ],
    },
    // Huida (M2): la mano derecha recoge la falda; la expresión solo mueve la cabeza.
    corriendo: {
      base: `${atlas}/rosalba-corriendo`,
      cabezas: `${atlas}/rosalba-cabezas`,
      postura: 'cabeza',
      piezas: [
        'brazo-izq',
        'antebrazo-izq',
        'pierna-izq',
        'pierna-der',
        'enagua',
        'falda',
        'torso',
        'cabeza',
        'zarcillo',
        'mechones',
        'ruana',
        'trenza',
        'cinta',
        'brazo-der',
        'antebrazo-der',
        'ruana-doblez',
      ],
    },
    agachada: {
      base: `${atlas}/rosalba-agachada`,
      cabezas: `${atlas}/rosalba-agachada-cabezas`,
      // La mano de apoyo sigue en el suelo: la expresión solo mueve la cabeza.
      postura: 'cabeza',
      piezas: [
        'cuerpo',
        'cabeza',
        'zarcillo',
        'mechones',
        'ruana',
        'trenza',
        'cinta',
        'brazo-der',
        'antebrazo-der',
        'ruana-doblez',
      ],
    },
  };
}

/**
 * Variante Llano (doc 03 §3.3; hoja de personaje §2): camisa caqui remangada, falda de dril a
 * media canilla, cotizas, faja con cuchillo y sombrero de cogollo. De pie y corriendo las
 * piernas son canillas con pivote en la rodilla: camina con CAMINATA_LLANO y corre con
 * CARRERA_LLANO. El rollo de cada manga (`manga-*`) cuelga del brazo y tapa el codo; el
 * cuello abierto de la camisa va por delante del hombro.
 */
export function rosalbaLlano(
  acto: ActoLlano = 'acto2',
): Record<string, DefinicionPose> {
  const atlas = atlasRosalba(acto);
  const piezas = [
    'brazo-izq',
    'antebrazo-izq',
    'manga-izq',
    'pierna-izq',
    'pierna-der',
    'falda',
    'torso',
    'faja',
    'cabeza',
    'zarcillo',
    'sombrero',
    'trenza',
    'cinta',
    'brazo-der',
    'antebrazo-der',
    'manga-der',
    'cuello',
  ];
  return {
    'de-pie': {
      base: `${atlas}/rosalba-llano`,
      cabezas: `${atlas}/rosalba-cabezas`,
      piezas,
    },
    corriendo: {
      base: `${atlas}/rosalba-llano-corriendo`,
      cabezas: `${atlas}/rosalba-cabezas`,
      postura: 'cabeza',
      piezas,
    },
    agachada: {
      base: `${atlas}/rosalba-llano-agachada`,
      cabezas: `${atlas}/rosalba-agachada-cabezas`,
      // La mano de apoyo sigue en el suelo: la expresión solo mueve la cabeza.
      postura: 'cabeza',
      piezas: [
        'cuerpo',
        'faja',
        'cabeza',
        'zarcillo',
        'sombrero',
        'trenza',
        'cinta',
        'brazo-der',
        'antebrazo-der',
        'manga-der',
      ],
    },
  };
}

/** Atajos: el mercado del Prólogo y el monte del Acto I (M2). */
export const ROSALBA_MERCADO = rosalbaMercado('prologo');
export const ROSALBA_MONTE = rosalbaMonte('acto1');
