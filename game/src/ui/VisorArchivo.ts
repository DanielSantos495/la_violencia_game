import type { EntradaArchivo } from '../core/archivo/esquema.ts';

/** Visor DOM de una entrada del Archivo. Muestra la correspondencia ficción → historia (doc 01, regla 3). */
export class VisorArchivo {
  private readonly raiz: HTMLElement;

  constructor(contenedor: HTMLElement) {
    this.raiz = document.createElement('article');
    this.raiz.className = 'visor-archivo';
    this.raiz.hidden = true;
    contenedor.appendChild(this.raiz);
  }

  mostrar(e: EntradaArchivo): void {
    const el = (tag: string, texto: string, clase?: string): HTMLElement => {
      const n = document.createElement(tag);
      n.textContent = texto;
      if (clase) n.className = clase;
      return n;
    };
    const hijos: HTMLElement[] = [
      el('h2', e.titulo),
      el('p', `${e.fecha} · ${e.lugar}`, 'visor-archivo__meta'),
    ];
    if (e.nombre_en_juego && e.nombre_real) {
      hijos.push(
        el(
          'p',
          `En el juego: ${e.nombre_en_juego} → En la historia: ${e.nombre_real}`,
        ),
      );
    }
    hijos.push(el('p', e.texto));
    const fuentes = document.createElement('ul');
    for (const f of e.fuentes)
      fuentes.appendChild(el('li', `${f.titulo} (${f.tipo})`));
    hijos.push(
      fuentes,
      el(
        'p',
        `Licencia: ${e.licencia.titular} — ${e.licencia.estado}`,
        'visor-archivo__meta',
      ),
    );
    this.raiz.replaceChildren(...hijos);
    this.raiz.hidden = false;
  }

  destruir(): void {
    this.raiz.remove();
  }
}
