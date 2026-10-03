/**
 * Pose de caminata procedural para personajes cut-out (función pura, sin Phaser).
 *
 * Una sola fase (0..2π = un ciclo de dos pasos) produce todos los ángulos con senos
 * desfasados, así el movimiento es continuo y nunca se descuadra:
 * - Piernas en contrafase; el pie que avanza se levanta (fase de vuelo).
 * - Brazos opuestos a la pierna del mismo lado; el codo se dobla con retraso.
 * - El cuerpo sube cuando las piernas pasan por la vertical (dos veces por ciclo).
 * - Prendas y pelo siguen con retraso, como tela (inercia secundaria).
 *
 * Dos modos de pierna:
 * - **Cadera** (por defecto): la pierna gira desde la cadera (pantalón, piernas visibles).
 * - **Falda larga**: bajo una falda hasta el tobillo la pierna no se ve; los pies se deslizan
 *   dentro de un rango acotado (avance) y se inclinan en el tobillo (talón al apoyar, punta
 *   al despegar). Así ningún pie sale por detrás de la falda ni asoma la canilla cortada.
 *   Exige que las piernas tengan el pivote en el tobillo.
 *
 * Convención de Phaser: ángulo positivo = sentido horario; con el personaje mirando a la
 * derecha, un ángulo positivo lleva la pierna o el brazo hacia atrás.
 */
export interface PiesBajoFalda {
  /** Cuánto avanza el pie por delante de su posición de reposo, en px del SVG. */
  adelante?: number;
  /** Cuánto retrocede el pie por detrás de su posición de reposo, en px del SVG. */
  atras?: number;
  /** Inclinación máxima del pie en el tobillo, en grados. */
  inclinacion?: number;
}

export interface OpcionesCaminata {
  /** Amplitud de la cadera en grados (modo cadera) y del braceo. */
  zancada?: number;
  /** Altura máxima que se despega el pie que avanza, en px del SVG. */
  levantePie?: number;
  /** Rebote vertical del cuerpo, en px del SVG. */
  rebote?: number;
  /** Activa el modo de pies bajo falda larga (true usa los valores por defecto). */
  faldaLarga?: boolean | PiesBajoFalda;
}

export interface PoseCaminata {
  /** Ángulo en grados por id de pieza (las ausentes del personaje se ignoran). */
  angulos: Record<string, number>;
  /** Desplazamiento horizontal, en px, de las piezas que se deslizan (pies bajo falda). */
  avance: Record<string, number>;
  /** Desplazamiento hacia arriba, en px, de las piernas que se despegan. */
  levante: Record<string, number>;
  /** Cuánto sube el cuerpo entero, en px. */
  rebote: number;
}

export const ZANCADA_POR_DEFECTO = 12;
export const PIES_BAJO_FALDA_POR_DEFECTO: Required<PiesBajoFalda> = {
  adelante: 35,
  atras: 23,
  inclinacion: 8,
};

function piesBajoFalda(
  opcion: OpcionesCaminata['faldaLarga'],
): Required<PiesBajoFalda> | null {
  if (!opcion) return null;
  return { ...PIES_BAJO_FALDA_POR_DEFECTO, ...(opcion === true ? {} : opcion) };
}

export function poseCaminata(
  fase: number,
  {
    zancada = ZANCADA_POR_DEFECTO,
    levantePie = 9,
    rebote = 3.5,
    faldaLarga,
  }: OpcionesCaminata = {},
): PoseCaminata {
  const s = Math.sin(fase);
  const c = Math.cos(fase);
  const pies = piesBajoFalda(faldaLarga);

  const angulos: Record<string, number> = {
    'brazo-der': -zancada * 1.3 * s,
    'brazo-izq': zancada * 1.3 * s,
    'antebrazo-der': -6 - 7 * (0.5 - 0.5 * Math.sin(fase - 0.7)),
    'antebrazo-izq': -6 - 7 * (0.5 + 0.5 * Math.sin(fase - 0.7)),
    cabeza: 0.8 * Math.sin(2 * fase + 0.5),
    panolon: 0.9 * Math.sin(2 * fase - 1.1) + 0.6 * Math.sin(fase - 1),
    ruana: 0.9 * Math.sin(2 * fase - 1.1),
    'ruana-doblez': 0.9 * Math.sin(2 * fase - 1.1),
    trenza: 3.5 * Math.sin(fase - 1.7) + 1.5 * Math.sin(2 * fase - 1.2),
    zarcillo: 9 * Math.sin(2 * fase - 1.5),
  };
  const avance: Record<string, number> = {};

  if (pies) {
    // Recorrido simétrico alrededor de un centro desplazado: sin cambios bruscos de velocidad.
    const amplitud = (pies.adelante + pies.atras) / 2;
    const centro = (pies.adelante - pies.atras) / 2;
    avance['pierna-der'] = centro - amplitud * s;
    avance['pierna-izq'] = centro + amplitud * s;
    // Atrás (s > 0 para la derecha): talón arriba; adelante: punta arriba al apoyar.
    angulos['pierna-der'] = pies.inclinacion * s;
    angulos['pierna-izq'] = -pies.inclinacion * s;
    // La falda se mece poco y hacia atrás cuando el pie izquierdo (el más atrasado) retrocede.
    angulos.falda = -1 * Math.sin(fase - 0.3);
    angulos.enagua = -1.2 * Math.sin(fase - 0.5);
  } else {
    angulos['pierna-der'] = zancada * s;
    angulos['pierna-izq'] = -zancada * s;
    angulos.falda = 2.4 * Math.sin(fase - 0.9);
    angulos.enagua = 3.2 * Math.sin(fase - 1.3);
  }

  return {
    angulos,
    avance,
    levante: {
      // El pie que avanza está en el aire.
      'pierna-der': levantePie * Math.max(0, -c) ** 1.5,
      'pierna-izq': levantePie * Math.max(0, c) ** 1.5,
    },
    rebote: rebote * (0.5 + 0.5 * Math.cos(2 * fase)),
  };
}

/**
 * Velocidad de avance (px/s a escala 1) para que los pies no patinen. Cada paso recorre lo
 * que el pie de apoyo retrocede respecto al cuerpo: en modo cadera la cuerda del arco de la
 * pierna, 2·L·sen(zancada); en falda larga, adelante + atrás. Hay dos pasos por ciclo.
 */
export function velocidadCaminata(
  cicloMs: number,
  { zancada = ZANCADA_POR_DEFECTO, faldaLarga }: OpcionesCaminata = {},
  largoPierna = 222,
): number {
  const pies = piesBajoFalda(faldaLarga);
  const paso = pies
    ? pies.adelante + pies.atras
    : 2 * largoPierna * Math.sin((zancada * Math.PI) / 180);
  return (2 * paso) / (cicloMs / 1000);
}
