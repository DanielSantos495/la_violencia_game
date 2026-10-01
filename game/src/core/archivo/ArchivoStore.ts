import { type EntradaArchivo, validarEntrada } from './esquema.ts';

/**
 * Carga entradas del Archivo ya validadas (doc 04 §4). Vuelve a validar en runtime
 * y descarta lo inválido: el índice generado nunca se da por bueno a ciegas.
 */
export class ArchivoStore {
  private readonly entradas = new Map<string, EntradaArchivo>();
  readonly descartadas: string[] = [];

  constructor(datos: unknown) {
    const lista = Array.isArray(datos) ? datos : [];
    for (const [i, crudo] of lista.entries()) {
      const r = validarEntrada(crudo);
      if (!r.ok) {
        this.descartadas.push(`#${i}: ${r.errores.join('; ')}`);
      } else if (this.entradas.has(r.entrada.id)) {
        this.descartadas.push(`#${i}: id duplicado ${r.entrada.id}`);
      } else {
        this.entradas.set(r.entrada.id, r.entrada);
      }
    }
  }

  todas(): EntradaArchivo[] {
    return [...this.entradas.values()];
  }

  porId(id: string): EntradaArchivo | undefined {
    return this.entradas.get(id);
  }

  porEpisodio(episodio: number): EntradaArchivo[] {
    return this.todas().filter((e) => e.desbloqueo.episodio === episodio);
  }
}
