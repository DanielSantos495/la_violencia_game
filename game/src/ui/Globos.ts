import type { InkRunner } from '../core/narrative/InkRunner.ts';

/**
 * Globos de diálogo en DOM sobre el canvas (doc 04 §3: UI en DOM).
 * Estilo provisional: la hoja de estilo final sale del doc 03 §6.
 */
export class Globos {
  private readonly raiz: HTMLElement;
  private readonly runner: InkRunner;
  private readonly alTerminar: () => void;

  constructor(
    contenedor: HTMLElement,
    runner: InkRunner,
    alTerminar: () => void = () => {},
  ) {
    this.runner = runner;
    this.alTerminar = alTerminar;
    this.raiz = document.createElement('div');
    this.raiz.className = 'globos';
    contenedor.appendChild(this.raiz);
  }

  /** Muestra la siguiente línea; si hay decisión, muestra las opciones. */
  avanzar(): void {
    this.raiz.replaceChildren();
    const linea = this.runner.continuar();
    if (linea) {
      const globo = document.createElement('button');
      globo.type = 'button';
      globo.className = 'globo';
      if (linea.hablante) {
        const quien = document.createElement('strong');
        quien.textContent = linea.hablante;
        globo.append(quien, document.createElement('br'));
      }
      globo.append(linea.texto);
      globo.addEventListener('click', () => this.avanzar());
      this.raiz.appendChild(globo);
      return;
    }
    const opciones = this.runner.opciones();
    if (opciones.length > 0) {
      for (const opcion of opciones) {
        const boton = document.createElement('button');
        boton.type = 'button';
        boton.className = 'globo globo--opcion';
        boton.textContent = opcion.texto;
        boton.addEventListener('click', () => {
          this.runner.elegir(opcion.indice);
          this.avanzar();
        });
        this.raiz.appendChild(boton);
      }
      return;
    }
    this.alTerminar();
  }

  destruir(): void {
    this.raiz.remove();
  }
}
