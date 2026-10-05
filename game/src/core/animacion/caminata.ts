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
 * Tres modos de pierna:
 * - **Cadera** (por defecto): la pierna gira desde la cadera (pantalón, piernas visibles).
 * - **Falda larga**: bajo una falda hasta el tobillo la pierna no se ve; los pies se deslizan
 *   dentro de un rango acotado (avance) y se inclinan en el tobillo (talón al apoyar, punta
 *   al despegar). Así ningún pie sale por detrás de la falda ni asoma la canilla cortada.
 *   Exige que las piernas tengan el pivote en el tobillo.
 * - **Canilla** (falda a media pierna): se ve la canilla y la rodilla queda bajo la falda.
 *   Cada pierna es la canilla con pivote en la rodilla, que se desplaza con el muslo: el pie
 *   de apoyo retrocede en línea recta sin patinar ni despegarse (con doble apoyo, como al
 *   caminar), y en el vuelo el talón sube atrás y la canilla vuelve adelante. El cuerpo sube a
 *   mitad de cada apoyo (péndulo invertido). Misma geometría que la carrera (carrera.ts).
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

export interface CanillaBajoFalda {
  /** Largo de la canilla, de la rodilla (pivote) a la planta, en px del SVG. */
  largo?: number;
  /** Ángulo de la canilla al apoyar el talón (adelante) y al despegar (atrás), en grados. */
  angulo?: number;
  /** Cuánto se desplaza la rodilla adelante y atrás con el muslo, en px. */
  rodilla?: number;
  /** Fracción del ciclo que cada pie pasa apoyado (> 0,5: hay doble apoyo). */
  apoyo?: number;
  /** Cuánto se dobla la rodilla (talón atrás) en el vuelo de la pierna, en grados. */
  flexion?: number;
  /** Cuánto sube la rodilla en el vuelo de la pierna, en px. */
  alzaRodilla?: number;
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
  /** Activa el modo canilla bajo falda a media pierna (true usa los valores por defecto). */
  canilla?: boolean | CanillaBajoFalda;
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

export const CANILLA_POR_DEFECTO: Required<CanillaBajoFalda> = {
  largo: 128,
  angulo: 18,
  rodilla: 12,
  apoyo: 0.6,
  flexion: 28,
  alzaRodilla: 10,
};

const TAU = Math.PI * 2;
const RAD = Math.PI / 180;

function canillaBajoFalda(
  opcion: OpcionesCaminata['canilla'],
): Required<CanillaBajoFalda> | null {
  if (!opcion) return null;
  return { ...CANILLA_POR_DEFECTO, ...(opcion === true ? {} : opcion) };
}

/**
 * Una canilla en la fase u de su pierna (0 = apoya el talón adelante); `sube` = cuánto sube
 * el cuerpo en ese instante. Ángulo en grados, positivo = adelante.
 */
function canilla(
  u: number,
  o: Required<CanillaBajoFalda>,
  sube: number,
): { angulo: number; avance: number; levante: number } {
  const extendida = o.largo * (1 - Math.cos(o.angulo * RAD));
  if (u < o.apoyo) {
    // El pie relativo al cuerpo (rodilla + L·sen a) va de adelante a atrás en línea recta.
    const k = 1 - 2 * (u / o.apoyo);
    const a = Math.asin(Math.sin(o.angulo * RAD) * k);
    return {
      angulo: a / RAD,
      avance: o.rodilla * k,
      // La rodilla baja lo que sube el cuerpo y lo que la canilla inclinada se acorta.
      levante: -sube - o.largo * (1 - Math.cos(a)),
    };
  }
  const q = (u - o.apoyo) / (1 - o.apoyo);
  return {
    angulo:
      -o.angulo * Math.cos(Math.PI * q) -
      o.flexion * Math.sin(Math.PI * q) * (1 - q),
    avance: -o.rodilla * Math.cos(Math.PI * q),
    levante: -sube - extendida + o.alzaRodilla * Math.sin(Math.PI * q),
  };
}

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
    canilla: opcionCanilla,
  }: OpcionesCaminata = {},
): PoseCaminata {
  const s = Math.sin(fase);
  const c = Math.cos(fase);
  const pies = piesBajoFalda(faldaLarga);
  const canillas = canillaBajoFalda(opcionCanilla);

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

  if (canillas) {
    // El talón derecho apoya adelante en la fase 3π/2, cuando el brazo derecho va más atrás.
    const u = (((fase / TAU - 0.75) % 1) + 1) % 1;
    // El cuerpo sube a mitad de cada apoyo y baja en el doble apoyo.
    const sube =
      rebote * (0.5 + 0.5 * Math.cos(2 * TAU * (u - canillas.apoyo / 2)));
    const der = canilla(u, canillas, sube);
    const izq = canilla((u + 0.5) % 1, canillas, sube);
    angulos['pierna-der'] = -der.angulo;
    angulos['pierna-izq'] = -izq.angulo;
    avance['pierna-der'] = der.avance;
    avance['pierna-izq'] = izq.avance;
    // Falda de tela liviana: se mece con el paso y se retrasa un poco.
    angulos.falda = 1.6 * Math.sin(fase - 0.9) + 0.5 * Math.sin(2 * fase - 1.4);
    angulos.faja = 0.6 * Math.sin(2 * fase - 1);
    return {
      angulos,
      avance,
      levante: { 'pierna-der': der.levante, 'pierna-izq': izq.levante },
      rebote: sube,
    };
  }

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
 * pierna, 2·L·sen(zancada); en falda larga, adelante + atrás. Hay dos pasos por ciclo. En
 * modo canilla, lo que retrocede el pie en un apoyo dividido por lo que dura el apoyo.
 */
export function velocidadCaminata(
  cicloMs: number,
  {
    zancada = ZANCADA_POR_DEFECTO,
    faldaLarga,
    canilla: opcionCanilla,
  }: OpcionesCaminata = {},
  largoPierna = 222,
): number {
  const pies = piesBajoFalda(faldaLarga);
  const canillas = canillaBajoFalda(opcionCanilla);
  if (canillas) {
    // En cada apoyo el pie retrocede 2·(L·sen α + rodilla) respecto al cuerpo en apoyo·ciclo.
    const recorrido =
      2 * (canillas.largo * Math.sin(canillas.angulo * RAD) + canillas.rodilla);
    return recorrido / ((canillas.apoyo * cicloMs) / 1000);
  }
  const paso = pies
    ? pies.adelante + pies.atras
    : 2 * largoPierna * Math.sin((zancada * Math.PI) / 180);
  return (2 * paso) / (cicloMs / 1000);
}
