/**
 * Plaza de Puente Alto, mañana de mercado (1946): prólogo, beat 1 (doc 02 §5).
 * Composición y fuentes: planeacion/arte/tomo1/escenarios/puente-alto.md §2.
 * Módulos: game/art/gen/puente_alto.py → art/src/fondos/puente-alto/*.svg.
 */
import { PARALAJE, Y_SUELO, ySueloCapa } from '../escena/escala.ts';
import type { DefinicionEscenario } from './escenario.ts';

export const PUENTE_ALTO: DefinicionEscenario = {
  atlas: 'fondos/puente-alto',
  // Cuatro pantallas: tienda roja, plaza abierta (se ve el mercado y el otro lado), casa del portón.
  anchoNivel: 7680,
  capas: {
    cielo: {
      colocaciones: [
        { modulo: 'nube-a', x: 120, y: 58, ancla: 'arriba', deriva: -6 },
        { modulo: 'nube-b', x: 980, y: 140, ancla: 'arriba', deriva: -4 },
        { modulo: 'nube-c', x: 1560, y: 36, ancla: 'arriba', deriva: -9 },
        { modulo: 'cordillera', x: 0, ancla: 'arriba' },
      ],
    },
    lejos: {
      mosaicos: [{ modulo: 'suelo-lejos', y: ySueloCapa(PARALAJE.lejos) }],
      colocaciones: [
        // La tienda azul (lx 790–1150) queda detrás de Rosalba cuando sale de la tienda roja.
        { modulo: 'lejos-oeste', x: 0 },
        { modulo: 'iglesia', x: 1340 },
        { modulo: 'lejos-este', x: 1750 },
      ],
    },
    medio: {
      mosaicos: [{ modulo: 'suelo-medio', y: ySueloCapa(PARALAJE.medio) }],
      // Por la plaza abierta se ve el medio entre mx≈945 y ≈3666: ahí va el mercado. El hueco
      // mx≈1300–1600 deja ver la tienda azul al salir de la tienda roja (cámara ≈1460).
      // Al empezar y al terminar el nivel asoman los extremos (mx 0–200 y 4332–4512).
      colocaciones: [
        { modulo: 'gente-pareja', x: 40 },
        { modulo: 'mula-carga', x: 960 },
        { modulo: 'toldo-papas', x: 1600 },
        { modulo: 'tendido-papas', x: 2010 },
        { modulo: 'pila', x: 2250 },
        { modulo: 'gente-corrillo', x: 2610 },
        { modulo: 'tendido-cubios', x: 2830 },
        { modulo: 'toldo-loza', x: 3150 },
        { modulo: 'gente-mujeres', x: 3540 },
        { modulo: 'mula-atada', x: 4262, espejo: true },
      ],
    },
    juego: {
      mosaicos: [{ modulo: 'empedrado', y: Y_SUELO }],
      colocaciones: [
        { modulo: 'tienda-roja', x: 200 },
        { modulo: 'costales', x: 2380 },
        { modulo: 'ollas', x: 2760 },
        { modulo: 'canastos', x: 3420 },
        { modulo: 'costales', x: 4300, espejo: true },
        { modulo: 'canastos', x: 4920, espejo: true },
        { modulo: 'ollas', x: 5330, espejo: true },
        { modulo: 'casa-porton', x: 5800 },
      ],
    },
    frente: {
      // Bases por debajo del cuadro: solo asoma lo de arriba y no tapa el camino del personaje.
      colocaciones: [
        { modulo: 'frente-canastos', x: 1500, y: 1150 },
        { modulo: 'frente-costal', x: 3700, y: 1250 },
        { modulo: 'frente-toldo', x: 4300, y: 0, ancla: 'arriba' },
        { modulo: 'frente-canastos', x: 6700, y: 1170, espejo: true },
        { modulo: 'frente-costal', x: 8700, y: 1240, espejo: true },
      ],
    },
  },
};
