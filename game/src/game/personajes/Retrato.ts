import type { GameObjects, Scene } from 'phaser';
import {
  DATOS_EXPRESION,
  EXPRESIONES,
  type Expresion,
  intervaloParpadeo,
} from '../../core/animacion/expresiones.ts';

/**
 * Retrato en tres cuartos para viñetas y diálogos: base por variante (ropa, pelo, rostro sin
 * rasgos) + rasgos de la expresión + capa de parpadeo, apiladas en el mismo pivote (el pie
 * del busto). Los frames vienen de "<base>/base-<variante>", "<base>/cinta",
 * "<base>/rasgos-<expresión>" y "<base>/parpado-<expresión>". La cinta roja de la trenza es
 * una capa aparte porque en la historia se la quitan y se la vuelve a poner (doc 10 P31–P32).
 */
export class Retrato {
  readonly contenedor: GameObjects.Container;
  private readonly escena: Scene;
  private readonly base: string;
  private readonly rasgos: GameObjects.Image;
  private readonly parpado: GameObjects.Image;
  private readonly capaCinta: GameObjects.Image;
  private expresionActual: Expresion;

  constructor(
    escena: Scene,
    x: number,
    y: number,
    atlas: string,
    base: string,
    variante: string,
    expresion: Expresion = 'neutral',
    conCinta = true,
  ) {
    this.escena = escena;
    this.base = base;
    this.expresionActual = expresion;
    const textura = escena.textures.get(atlas);
    const necesarios = [
      `${base}/base-${variante}`,
      `${base}/cinta`,
      ...EXPRESIONES.flatMap((e) => [
        `${base}/rasgos-${e}`,
        `${base}/parpado-${e}`,
      ]),
    ];
    for (const frame of necesarios) {
      if (!textura.has(frame)) throw new Error(`Frame inexistente: ${frame}`);
    }
    this.contenedor = escena.add.container(x, y);
    this.capaCinta = escena.add
      .image(0, 0, atlas, `${base}/cinta`)
      .setVisible(conCinta);
    this.rasgos = escena.add.image(0, 0, atlas, `${base}/rasgos-${expresion}`);
    this.parpado = escena.add
      .image(0, 0, atlas, `${base}/parpado-${expresion}`)
      .setVisible(false);
    this.contenedor.add([
      escena.add.image(0, 0, atlas, `${base}/base-${variante}`),
      this.capaCinta,
      this.rasgos,
      this.parpado,
    ]);
    this.programarParpadeo();
  }

  get gesto(): Expresion {
    return this.expresionActual;
  }

  /** Pone o quita la cinta roja de la trenza. */
  cinta(visible: boolean): void {
    this.capaCinta.setVisible(visible);
  }

  /** Cambia la expresión de golpe, como entre viñetas. */
  expresion(nombre: Expresion): void {
    this.expresionActual = nombre;
    this.rasgos.setFrame(`${this.base}/rasgos-${nombre}`);
    this.parpado.setFrame(`${this.base}/parpado-${nombre}`);
  }

  private programarParpadeo(): void {
    const { parpadeo } = DATOS_EXPRESION[this.expresionActual];
    this.escena.time.delayedCall(
      intervaloParpadeo(this.expresionActual, Math.random),
      () => {
        if (!this.contenedor.active) return;
        this.parpado.setVisible(true);
        this.escena.time.delayedCall(parpadeo.dura, () =>
          this.parpado.setVisible(false),
        );
        this.programarParpadeo();
      },
    );
  }
}
