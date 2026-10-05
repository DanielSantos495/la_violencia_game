import {
  type Cameras,
  type Filters,
  type Scene,
  type Tweens,
  WEBGL,
} from 'phaser';
import { color } from '../../core/arte/paleta.ts';
import { hexARgb, matrizNocheDeTinta } from '../../core/escenarios/noche.ts';

/**
 * Noche de tinta (estilo B) en vivo sobre una cámara, para el momento en que llama la Seccional o
 * llega la partida (src/core/escenarios/noche.ts; casa-insuasty.md §7). Tiñe todo lo que dibuja la
 * cámara, personajes incluidos. El rojo y el azul guardan el tono; lo que deba quedar exacto se
 * dibuja con otra cámara (paleta.md §5). Solo WebGL: con Canvas no hace nada.
 */
export class NocheDeTinta {
  private readonly escena: Scene;
  private readonly matriz?: Filters.ColorMatrix;
  private tween?: Tweens.Tween;
  private terminar?: () => void;
  private t = 0;

  constructor(escena: Scene, camara: Cameras.Scene2D.Camera) {
    this.escena = escena;
    if (escena.renderer.type !== WEBGL) return;
    this.matriz = camara.filters.internal.addColorMatrix();
    this.matriz.colorMatrix.set(
      matrizNocheDeTinta({
        papel: hexARgb(color('papel')),
        tinta: hexARgb(color('tinta')),
      }),
    );
    this.aplicar(0);
  }

  /** Intensidad actual: 0 es la noche sepia de los fondos y 1 la noche de tinta entera. */
  get intensidad(): number {
    return this.t;
  }

  /** Va hacia la intensidad `destino` en `ms` milisegundos; resuelve al llegar o si otro la corta. */
  fundir(destino: number, ms = 700): Promise<void> {
    this.tween?.stop();
    this.terminar?.();
    return new Promise((resolver) => {
      this.terminar = resolver;
      this.tween = this.escena.tweens.addCounter({
        from: this.t,
        to: destino,
        duration: ms,
        ease: 'Sine.easeInOut',
        onUpdate: (tween) => this.aplicar(tween.getValue() ?? destino),
        onComplete: () => {
          this.aplicar(destino);
          this.terminar = undefined;
          resolver();
        },
      });
    });
  }

  private aplicar(t: number): void {
    this.t = t;
    if (!this.matriz) return;
    // El alpha de la matriz mezcla el color de antes con el filtrado.
    this.matriz.colorMatrix.alpha = t;
    // Sin noche de tinta, el filtro no se dibuja.
    this.matriz.setActive(t > 0);
  }
}
