/**
 * Escenarios por nombre, para la escena de prueba (?escenario=) y para `pnpm art:escena`.
 */
import { casaInsuastyExterior, casaInsuastyInterior } from './casa-insuasty.ts';
import type { DefinicionEscenario } from './escenario.ts';
import { PUENTE_ALTO } from './puente-alto.ts';

export const ESCENARIOS: Readonly<Record<string, DefinicionEscenario>> = {
  'puente-alto': PUENTE_ALTO,
  'casa-interior': casaInsuastyInterior('prologo'),
  'casa-exterior': casaInsuastyExterior('prologo'),
  'casa-interior-acto1': casaInsuastyInterior('acto1'),
  'casa-exterior-acto1': casaInsuastyExterior('acto1'),
};
