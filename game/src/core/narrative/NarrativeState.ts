import type { InkRunner } from './InkRunner.ts';

/**
 * Puente entre las variables de Ink y el guardado (doc 04 §4).
 * Las variables del guion viven en Ink; aquí solo se serializa su estado.
 * El guardado es compatible entre episodios (doc 04 §6).
 */
export const VERSION_GUARDADO = 1;

export interface Guardado {
  version: number;
  episodio: number;
  /** Estado de Ink (`story.state.ToJson()`). */
  ink: string;
  actualizado: string;
}

/** Almacenamiento inyectable: localStorage en web, archivo local en escritorio. */
export interface AlmacenGuardado {
  leer(clave: string): string | null;
  escribir(clave: string, valor: string): void;
}

export const CLAVE_GUARDADO = 'la-violencia:tomo1:guardado';

export class NarrativeState {
  private readonly almacen: AlmacenGuardado;
  private readonly ahora: () => Date;

  constructor(almacen: AlmacenGuardado, ahora: () => Date = () => new Date()) {
    this.almacen = almacen;
    this.ahora = ahora;
  }

  capturar(runner: InkRunner, episodio: number): Guardado {
    return {
      version: VERSION_GUARDADO,
      episodio,
      ink: runner.exportarEstado(),
      actualizado: this.ahora().toISOString(),
    };
  }

  guardar(runner: InkRunner, episodio: number): Guardado {
    const datos = this.capturar(runner, episodio);
    this.almacen.escribir(CLAVE_GUARDADO, NarrativeState.serializar(datos));
    return datos;
  }

  /** Restaura el último guardado en el runner. Devuelve false si no hay guardado. */
  cargar(runner: InkRunner): boolean {
    const crudo = this.almacen.leer(CLAVE_GUARDADO);
    if (crudo === null) return false;
    runner.importarEstado(NarrativeState.parsear(crudo).ink);
    return true;
  }

  /** JSON descargable como respaldo exportable. */
  static serializar(datos: Guardado): string {
    return JSON.stringify(datos);
  }

  static parsear(json: string): Guardado {
    const d: unknown = JSON.parse(json);
    if (
      typeof d !== 'object' ||
      d === null ||
      !('version' in d) ||
      !('episodio' in d) ||
      !('ink' in d) ||
      !('actualizado' in d) ||
      d.version !== VERSION_GUARDADO ||
      typeof d.episodio !== 'number' ||
      typeof d.ink !== 'string' ||
      typeof d.actualizado !== 'string'
    ) {
      throw new Error('Guardado inválido o de una versión no soportada');
    }
    return {
      version: d.version,
      episodio: d.episodio,
      ink: d.ink,
      actualizado: d.actualizado,
    };
  }
}
