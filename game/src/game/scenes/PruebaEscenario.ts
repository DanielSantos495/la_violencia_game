import { type GameObjects, Scene } from 'phaser';
import { color, colorNumero } from '../../core/arte/paleta.ts';
import { VIEWPORT, Y_SUELO } from '../../core/escena/escala.ts';
import { PUENTE_ALTO } from '../../core/escenarios/puente-alto.ts';
import { cargarAtlas } from '../arte.ts';
import { Escenario, precargarEscenario } from '../escenarios/Escenario.ts';
import { Personaje } from '../Personaje.ts';
import {
  APOYO_ROSALBA,
  CAMINATA_ROSALBA,
  ESCALA_ROSALBA,
  ROSALBA_MERCADO,
} from '../personajes/rosalba.ts';

/**
 * Escena de prueba de escenarios: la plaza de Puente Alto en sus cinco capas (planeacion/arte/
 * tomo1/escenarios/puente-alto.md) con Rosalba cruzándola. No es contenido del juego.
 * En desarrollo: ?escena=PruebaEscenario. Sin navegador: pnpm art:escena puente-alto.
 */
export class PruebaEscenario extends Scene {
  private escenario?: Escenario;
  private camaraX?: GameObjects.Text;

  constructor() {
    super('PruebaEscenario');
  }

  preload(): void {
    cargarAtlas(this, 'personajes');
    precargarEscenario(this, PUENTE_ALTO);
  }

  create(): void {
    this.cameras.main.setBackgroundColor(colorNumero('papel'));
    const escenario = new Escenario(this, PUENTE_ALTO);
    this.escenario = escenario;

    const rosalba = new Personaje(
      this,
      300,
      Y_SUELO,
      'personajes',
      APOYO_ROSALBA,
      ROSALBA_MERCADO,
      'de-pie',
      { caminata: CAMINATA_ROSALBA },
    );
    rosalba.raiz.setScale(ESCALA_ROSALBA);
    escenario.capa('juego').add(rosalba.raiz);

    const camara = this.cameras.main;
    camara.setBounds(0, 0, escenario.anchoNivel, VIEWPORT.alto);
    camara.startFollow(rosalba.raiz, true, 0.08, 0);
    // El personaje queda a un tercio: se ve más mundo por delante que por detrás.
    camara.setFollowOffset(-VIEWPORT.ancho / 6, 0);
    camara.setDeadzone(160, VIEWPORT.alto);

    // Posición de la cámara, para compararla con las vistas de art:escena.
    this.camaraX = this.add
      .text(24, 20, '', {
        fontFamily: 'Georgia, serif',
        fontSize: '18px',
        color: color('tinta'),
      })
      .setScrollFactor(0);

    void (async () => {
      for (;;) {
        rosalba.raiz.x = 300;
        await rosalba.caminarHasta(escenario.anchoNivel - 300);
      }
    })();
  }

  update(_tiempo: number, delta: number): void {
    this.escenario?.actualizar(delta);
    this.camaraX?.setText(
      `Puente Alto · cámara x=${Math.round(this.cameras.main.scrollX)}`,
    );
  }
}
