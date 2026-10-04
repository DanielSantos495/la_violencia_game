/**
 * Carrera procedural para personajes cut-out que corren con la falda recogida (función pura,
 * sin Phaser). Devuelve la misma forma de pose que la caminata (caminata.ts).
 *
 * Modelo: cada pierna es la canilla (de la rodilla al pie); la rodilla y el muslo quedan
 * ocultos bajo la falda. La canilla gira en la rodilla y la rodilla se desplaza con el muslo.
 * Cada pie pasa una fracción del ciclo apoyado (`apoyo`) y el resto en el aire; con
 * apoyo < 0,5 hay dos fases de vuelo por ciclo, como en una carrera de verdad.
 * - Apoyo: el pie retrocede respecto al cuerpo a velocidad constante (no patina) y no se
 *   despega del suelo: el cuerpo se hunde a mitad del apoyo y la rodilla sube lo mismo.
 * - Vuelo de la pierna: el talón sube por detrás (patada) y la canilla vuelve adelante a
 *   tiempo para el siguiente apoyo.
 * - El brazo libre bracea con la pierna contraria; el que recoge la falda casi no se mueve.
 *   Trenza, ruana y zarcillo siguen con inercia.
 *
 * Convención de Phaser: ángulo positivo = sentido horario = hacia atrás (mirando a la derecha).
 */
import type { PoseCaminata } from './caminata.ts';

export interface OpcionesCarrera {
  /** Largo de la canilla, de la rodilla (pivote) a la planta, en px del SVG. */
  largo?: number;
  /** Ángulo de la canilla al apoyar (adelante) y al despegar (atrás), en grados. */
  angulo?: number;
  /** Cuánto se desplaza la rodilla adelante y atrás con el muslo, en px. */
  rodilla?: number;
  /** Fracción del ciclo que cada pie pasa apoyado (0..0,5). */
  apoyo?: number;
  /** Cuánto sube el talón por detrás en el vuelo de la pierna, en grados. */
  patada?: number;
  /** Cuánto sube la rodilla en el vuelo de la pierna, en px. */
  alzaRodilla?: number;
  /** Cuánto se hunde el cuerpo a mitad del apoyo, en px. */
  hundimiento?: number;
  /** Cuánto sube el cuerpo a mitad del vuelo, en px. */
  vuelo?: number;
}

export const CARRERA_POR_DEFECTO: Required<OpcionesCarrera> = {
  largo: 128,
  angulo: 26,
  rodilla: 12,
  apoyo: 0.38,
  patada: 90,
  alzaRodilla: 24,
  hundimiento: 6,
  vuelo: 7,
};

const TAU = Math.PI * 2;
const RAD = Math.PI / 180;

function conDefecto(opciones: OpcionesCarrera): Required<OpcionesCarrera> {
  return { ...CARRERA_POR_DEFECTO, ...opciones };
}

/** Cuánto baja el cuerpo (px, abajo positivo): hundido en cada apoyo, arriba en cada vuelo. */
function hundido(u: number, o: Required<OpcionesCarrera>): number {
  const w = (u % 0.5) / 0.5;
  const a = 2 * o.apoyo;
  return w < a
    ? o.hundimiento * Math.sin((Math.PI * w) / a)
    : -o.vuelo * Math.sin((Math.PI * (w - a)) / (1 - a));
}

interface Pierna {
  /** Grados, positivo = adelante. */
  angulo: number;
  avance: number;
  levante: number;
}

/** Una pierna en la fase u (0 = apoya adelante); b = cuánto baja el cuerpo. */
function pierna(u: number, o: Required<OpcionesCarrera>, b: number): Pierna {
  const extendida = o.largo * (1 - Math.cos(o.angulo * RAD));
  if (u < o.apoyo) {
    // El pie relativo al cuerpo (rodilla + L·sen a) va de adelante a atrás en línea recta.
    const k = 1 - 2 * (u / o.apoyo);
    const a = Math.asin(Math.sin(o.angulo * RAD) * k);
    return {
      angulo: a / RAD,
      avance: o.rodilla * k,
      // La rodilla compensa lo que baja el cuerpo y lo que la canilla inclinada se acorta.
      levante: b - o.largo * (1 - Math.cos(a)),
    };
  }
  const q = (u - o.apoyo) / (1 - o.apoyo);
  return {
    angulo:
      -o.angulo * Math.cos(Math.PI * q) -
      o.patada * Math.sin(Math.PI * q) * (1 - q),
    avance: -o.rodilla * Math.cos(Math.PI * q),
    levante: -extendida + o.alzaRodilla * Math.sin(Math.PI * q),
  };
}

export function poseCarrera(
  fase: number,
  opciones: OpcionesCarrera = {},
): PoseCaminata {
  const o = conDefecto(opciones);
  const u = (((fase / TAU) % 1) + 1) % 1;
  const b = hundido(u, o);
  const der = pierna(u, o, b);
  const izq = pierna((u + 0.5) % 1, o, b);
  const paso = Math.sin(2 * TAU * u);
  // El brazo izquierdo va adelante cuando la pierna derecha apoya adelante (u = 0).
  const braceo = Math.cos(TAU * u);
  return {
    angulos: {
      'pierna-der': -der.angulo,
      'pierna-izq': -izq.angulo,
      'brazo-izq': 14 - 24 * braceo,
      'antebrazo-izq': -106 + 8 * braceo,
      'brazo-der': 0.5 * paso,
      'antebrazo-der': -0.5 * paso,
      cabeza: 3 + 1.5 * Math.sin(2 * TAU * u + 0.6),
      trenza: 6 * Math.sin(2 * TAU * u - 1.3) + 3 * Math.sin(TAU * u - 0.8),
      cinta: 10 * Math.sin(2 * TAU * u - 2),
      zarcillo: 14 * Math.sin(2 * TAU * u - 1.6),
      mechones: 3 * Math.sin(2 * TAU * u - 1),
      ruana: 2.5 * Math.sin(2 * TAU * u - 1.1),
      'ruana-doblez': 2.5 * Math.sin(2 * TAU * u - 1.1),
      falda: 0.8 * Math.sin(2 * TAU * u - 0.4),
      enagua: 1.4 * Math.sin(2 * TAU * u - 0.8),
    },
    avance: { 'pierna-der': der.avance, 'pierna-izq': izq.avance },
    levante: { 'pierna-der': der.levante, 'pierna-izq': izq.levante },
    rebote: -b,
  };
}

/**
 * Velocidad de avance (px/s a escala 1) para que el pie de apoyo no patine: en cada apoyo
 * el pie retrocede 2·(L·sen α + rodilla) respecto al cuerpo en `apoyo`·ciclo.
 */
export function velocidadCarrera(
  cicloMs: number,
  opciones: OpcionesCarrera = {},
): number {
  const o = conDefecto(opciones);
  const recorrido = 2 * (o.largo * Math.sin(o.angulo * RAD) + o.rodilla);
  return recorrido / ((o.apoyo * cicloMs) / 1000);
}
