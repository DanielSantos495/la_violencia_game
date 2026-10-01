/**
 * Esquema de entrada del Archivo (doc 04 §7). Validación propia, sin dependencias:
 * se usa igual en el navegador (ArchivoStore) y en Node (tools/validate-archivo).
 */
export const ESTADOS_VERIFICACION = ['verificado', 'pendiente'] as const;
export const ESTADOS_LICENCIA = [
  'solicitada',
  'concedida',
  'no_aplica',
] as const;

export type EstadoVerificacion = (typeof ESTADOS_VERIFICACION)[number];
export type EstadoLicencia = (typeof ESTADOS_LICENCIA)[number];

export interface Fuente {
  titulo: string;
  url: string;
  tipo: string;
}

export interface EntradaArchivo {
  id: string;
  titulo: string;
  /** ISO: AAAA, AAAA-MM o AAAA-MM-DD (las fechas parciales evitan inventar precisión). */
  fecha: string;
  lugar: string;
  nombre_en_juego: string | null;
  nombre_real: string | null;
  texto: string;
  estado_verificacion: EstadoVerificacion;
  fuentes: Fuente[];
  licencia: { titular: string; estado: EstadoLicencia };
  desbloqueo: { episodio: number; mision: string; condicion: string };
}

/** Entradas de prueba del setup: nunca entran a un build público. */
export const PREFIJO_PRUEBA = 'arch-prueba-';

const RE_ID = /^arch-[a-z0-9-]+$/;
const RE_FECHA = /^\d{4}(-(0[1-9]|1[0-2])(-(0[1-9]|[12]\d|3[01]))?)?$/;

type Objeto = Record<string, unknown>;
const esObjeto = (v: unknown): v is Objeto =>
  typeof v === 'object' && v !== null && !Array.isArray(v);
const textoNoVacio = (v: unknown): v is string =>
  typeof v === 'string' && v.trim() !== '';
const textoONulo = (v: unknown): v is string | null =>
  v === null || typeof v === 'string';
const enLista = <T extends string>(lista: readonly T[], v: unknown): v is T =>
  typeof v === 'string' && (lista as readonly string[]).includes(v);

export type ResultadoValidacion =
  | { ok: true; entrada: EntradaArchivo }
  | { ok: false; errores: string[] };

export function validarEntrada(v: unknown): ResultadoValidacion {
  const errores: string[] = [];
  if (!esObjeto(v))
    return { ok: false, errores: ['la entrada no es un objeto'] };

  if (!textoNoVacio(v.id) || !RE_ID.test(v.id))
    errores.push('id: debe cumplir arch-[a-z0-9-]+');
  if (!textoNoVacio(v.titulo)) errores.push('titulo: texto requerido');
  if (typeof v.fecha !== 'string' || !RE_FECHA.test(v.fecha))
    errores.push('fecha: AAAA, AAAA-MM o AAAA-MM-DD');
  if (!textoNoVacio(v.lugar)) errores.push('lugar: texto requerido');
  if (!textoONulo(v.nombre_en_juego))
    errores.push('nombre_en_juego: texto o null');
  if (!textoONulo(v.nombre_real)) errores.push('nombre_real: texto o null');
  if (!textoNoVacio(v.texto)) errores.push('texto: texto requerido');
  if (!enLista(ESTADOS_VERIFICACION, v.estado_verificacion)) {
    errores.push(`estado_verificacion: ${ESTADOS_VERIFICACION.join(' | ')}`);
  }

  if (!Array.isArray(v.fuentes)) {
    errores.push('fuentes: lista requerida');
  } else {
    v.fuentes.forEach((f, i) => {
      if (
        !esObjeto(f) ||
        !textoNoVacio(f.titulo) ||
        typeof f.url !== 'string' ||
        !textoNoVacio(f.tipo)
      ) {
        errores.push(`fuentes[${i}]: requiere titulo, url y tipo`);
      }
    });
    if (v.estado_verificacion === 'verificado' && v.fuentes.length === 0) {
      errores.push(
        'fuentes: una entrada verificada necesita al menos una fuente',
      );
    }
  }

  if (
    !esObjeto(v.licencia) ||
    !textoNoVacio(v.licencia.titular) ||
    !enLista(ESTADOS_LICENCIA, v.licencia.estado)
  ) {
    errores.push(
      `licencia: requiere titular y estado (${ESTADOS_LICENCIA.join(' | ')})`,
    );
  }

  const d = v.desbloqueo;
  if (
    !esObjeto(d) ||
    typeof d.episodio !== 'number' ||
    !Number.isInteger(d.episodio) ||
    d.episodio < 1 ||
    !textoNoVacio(d.mision) ||
    !textoNoVacio(d.condicion)
  ) {
    errores.push(
      'desbloqueo: requiere episodio (entero ≥ 1), mision y condicion',
    );
  }

  return errores.length > 0
    ? { ok: false, errores }
    : { ok: true, entrada: v as unknown as EntradaArchivo };
}

/** Motivo por el que una entrada válida no entra a un build público, o null si entra (doc 04 §7). */
export function motivoExclusionRelease(e: EntradaArchivo): string | null {
  if (e.id.startsWith(PREFIJO_PRUEBA)) return 'entrada de prueba';
  if (e.estado_verificacion === 'pendiente') return 'verificación pendiente';
  if (e.licencia.estado !== 'concedida' && e.licencia.estado !== 'no_aplica') {
    return `licencia ${e.licencia.estado}`;
  }
  return null;
}
