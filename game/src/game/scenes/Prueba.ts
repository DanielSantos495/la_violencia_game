import { Scene } from 'phaser';
import { EXPRESIONES } from '../../core/animacion/expresiones.ts';
import { ArchivoStore } from '../../core/archivo/ArchivoStore.ts';
import { InkRunner } from '../../core/narrative/InkRunner.ts';
import { Globos } from '../../ui/Globos.ts';
import { VisorArchivo } from '../../ui/VisorArchivo.ts';
import { cargarAtlas } from '../arte.ts';
import { Personaje } from '../Personaje.ts';
import {
  APOYO_ROSALBA,
  CAMINATA_ROSALBA,
  ESCALA_ROSALBA,
  ROSALBA_MERCADO,
  ROSALBA_MONTE,
} from '../personajes/rosalba.ts';
import { armarRecorte } from '../Recorte.ts';

/** Escena de prueba del setup: personajes SVG por piezas animados, diálogo Ink en globos DOM y visor del Archivo. No es contenido del juego. */
export class Prueba extends Scene {
  constructor() {
    super('Prueba');
  }

  preload(): void {
    this.load.json('ink-prueba', 'generated/ink/prueba.json');
    this.load.json('archivo', 'generated/archivo/indice.json');
    cargarAtlas(this, 'personajes', 'prueba');
  }

  create(): void {
    const capaUi = document.getElementById('ui');
    if (!capaUi) throw new Error('Falta el contenedor #ui');

    this.cameras.main.setBackgroundColor('#ece4d0');
    const figura = armarRecorte(this, 860, 300, 'prueba', 'prueba/figura', [
      'torso',
      'cabeza',
      'brazo',
    ]);
    this.tweens.add({
      targets: figura.piezas.get('brazo'),
      angle: { from: -25, to: 25 },
      duration: 700,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut',
    });
    this.tweens.add({
      targets: figura.contenedor,
      y: 290,
      duration: 350,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut',
    });

    // Rosalba de mercado al fondo, cruzando en bucle.
    const mercado = new Personaje(
      this,
      -200,
      640,
      'personajes',
      APOYO_ROSALBA,
      ROSALBA_MERCADO,
      'de-pie',
      { caminata: CAMINATA_ROSALBA, expresion: 'neutral' },
    );
    mercado.raiz.setScale(ESCALA_ROSALBA);
    void (async () => {
      for (;;) {
        mercado.raiz.x = -200;
        await mercado.caminarHasta(2150);
      }
    })();
    // Recorre las expresiones mientras camina, para revisarlas en movimiento.
    let indiceExpresion = 0;
    this.time.addEvent({
      delay: 2400,
      loop: true,
      callback: () => {
        indiceExpresion = (indiceExpresion + 1) % EXPRESIONES.length;
        mercado.expresion(EXPRESIONES[indiceExpresion] ?? 'neutral');
      },
    });

    // Rosalba del monte: camina, se agacha a acechar, se levanta y sigue (sigilo, M2).
    const monte = new Personaje(
      this,
      -200,
      850,
      'personajes',
      APOYO_ROSALBA,
      ROSALBA_MONTE,
      'de-pie',
      { caminata: CAMINATA_ROSALBA, expresion: 'alerta' },
    );
    // Escala del contrato (planeacion/arte/tomo1/escenarios/contrato_escala.md).
    monte.raiz.setScale(ESCALA_ROSALBA);
    if (import.meta.env.DEV) {
      // Solo en desarrollo: permite inspeccionar la secuencia desde la consola del navegador.
      Object.assign(globalThis, { __prueba: { monte, mercado } });
    }
    void (async () => {
      for (;;) {
        monte.raiz.x = -200;
        monte.expresion('alerta');
        await monte.caminarHasta(760);
        await monte.cambiarPose('agachada');
        monte.expresion('miedo');
        monte.acechar();
        await this.esperar(3500);
        monte.expresion('alerta');
        await monte.cambiarPose('de-pie');
        await monte.caminarHasta(2150);
      }
    })();

    const archivo = new ArchivoStore(this.cache.json.get('archivo'));
    const visor = new VisorArchivo(capaUi);
    const primera = archivo.todas()[0];

    const runner = new InkRunner(
      this.cache.json.get('ink-prueba') as Record<string, unknown>,
    );
    const globos = new Globos(capaUi, runner, () => {
      if (primera) visor.mostrar(primera);
    });
    globos.avanzar();

    this.events.once('shutdown', () => {
      globos.destruir();
      visor.destruir();
    });
  }

  private esperar(ms: number): Promise<void> {
    return new Promise((resolver) => {
      this.time.delayedCall(ms, resolver);
    });
  }
}
