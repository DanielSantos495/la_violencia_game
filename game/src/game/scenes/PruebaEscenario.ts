import { GameObjects, Scene } from 'phaser';
import { color, colorNumero } from '../../core/arte/paleta.ts';
import { VIEWPORT, Y_SUELO } from '../../core/escena/escala.ts';
import { ESCENARIOS } from '../../core/escenarios/catalogo.ts';
import type { DefinicionEscenario } from '../../core/escenarios/escenario.ts';
import { PUENTE_ALTO } from '../../core/escenarios/puente-alto.ts';
import { cargarAtlas } from '../arte.ts';
import { Escenario, precargarEscenario } from '../escenarios/Escenario.ts';
import { Personaje } from '../Personaje.ts';
import {
  APOYO_ROSALBA,
  atlasRosalba,
  CAMINATA_ROSALBA,
  ESCALA_ROSALBA,
  PIEZA_CINTA,
  ROSALBA_MERCADO,
  rosalbaMonte,
} from '../personajes/rosalba.ts';

/**
 * Tinte de prueba para ver a Rosalba en las escenas de noche: multiplica el color de sus piezas
 * (una luz pareja; la luz real por zonas queda para la escena del juego).
 */
const TINTE_NOCHE: Readonly<Record<string, number>> = {
  'casa-interior': 0xcbb9a0,
  'casa-interior-acto1': 0xcbb9a0,
  'casa-exterior': 0x7a6a5c,
  'casa-exterior-acto1': 0x7a6a5c,
};

/** Tiñe todas las piezas menos la cinta: el rojo de partido va entero (paleta.md §6). */
function aplicarTinte(objeto: GameObjects.GameObject, tinte: number): void {
  if (objeto instanceof GameObjects.Container) {
    for (const hijo of objeto.list) aplicarTinte(hijo, tinte);
  } else if (
    objeto instanceof GameObjects.Image &&
    !objeto.frame.name.endsWith(`/${PIEZA_CINTA}`)
  ) {
    objeto.setTint(tinte);
  }
}

/**
 * Escena de prueba de escenarios (src/core/escenarios/catalogo.ts) con Rosalba cruzándolos: la
 * plaza de Puente Alto y la casa de los Insuasty de noche. No es contenido del juego.
 * En desarrollo: ?escena=PruebaEscenario&escenario=casa-exterior (por defecto, puente-alto).
 * Sin navegador: pnpm art:escena <escenario>.
 */
export class PruebaEscenario extends Scene {
  private nombre = 'puente-alto';
  private def: DefinicionEscenario = PUENTE_ALTO;
  private escenario?: Escenario;
  private camaraX?: GameObjects.Text;

  constructor() {
    super('PruebaEscenario');
  }

  init(): void {
    const pedido = new URLSearchParams(window.location.search).get('escenario');
    const def = pedido ? ESCENARIOS[pedido] : undefined;
    if (pedido && !def) console.warn(`Escenario desconocido: ${pedido}`);
    if (pedido && def) {
      this.nombre = pedido;
      this.def = def;
    }
  }

  preload(): void {
    cargarAtlas(this, atlasRosalba(this.def.acto ?? 'prologo'));
    precargarEscenario(this, this.def);
  }

  create(): void {
    const fondo = this.def.fondo ?? 'papel';
    this.cameras.main.setBackgroundColor(colorNumero(fondo));
    const escenario = new Escenario(this, this.def);
    this.escenario = escenario;

    // Rosalba del acto del escenario: en el Prólogo, de mercado y con la cinta; desde la M2, de
    // monte y sin la cinta (P32).
    const acto = this.def.acto ?? 'prologo';
    const rosalba = new Personaje(
      this,
      300,
      Y_SUELO,
      atlasRosalba(acto),
      APOYO_ROSALBA,
      acto === 'prologo' ? ROSALBA_MERCADO : rosalbaMonte(acto),
      'de-pie',
      {
        caminata: CAMINATA_ROSALBA,
        ocultas: acto === 'prologo' ? [] : [PIEZA_CINTA],
      },
    );
    rosalba.raiz.setScale(ESCALA_ROSALBA);
    const tinte = TINTE_NOCHE[this.nombre];
    if (tinte !== undefined) aplicarTinte(rosalba.raiz, tinte);
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
        color: color(fondo === 'papel' ? 'tinta' : 'papel'),
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
      `${this.nombre} · cámara x=${Math.round(this.cameras.main.scrollX)}`,
    );
  }
}
