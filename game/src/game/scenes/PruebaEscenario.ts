import { type GameObjects, Math as PhaserMath, Scene } from 'phaser';
import {
  anchoCapa,
  escalaPersonaje,
  type IdCapa,
  ORDEN_CAPAS,
  PARALAJE,
  PX_POR_METRO,
  pxPorMetroCapa,
  VIEWPORT,
  Y_HORIZONTE,
  Y_SUELO,
  ySueloCapa,
} from '../../core/escena/escala.ts';
import { cargarAtlas } from '../arte.ts';
import { Personaje } from '../Personaje.ts';
import {
  APOYO_ROSALBA,
  CAMINATA_ROSALBA,
  ROSALBA_MONTE,
} from '../personajes/rosalba.ts';

/** Ancho del nivel de prueba en el plano de juego: tres pantallas. */
const ANCHO_NIVEL = VIEWPORT.ancho * 3;

/** Rosalba: estatura de diseño y altura dibujada (coronilla → suela) medidas en su SVG. */
const ESTATURA_ROSALBA_M = 1.55;
const ALTURA_DIBUJO_ROSALBA = 431;

// Greybox: tonos provisionales de papel y tinta, no la paleta final (doc 03 §6.1 [P]).
const PAPEL = 0xece4d0;
const TINTA = 0x1b1b1b;
// Perspectiva aérea del greybox: lo lejano más claro, lo cercano más oscuro (opaco, sin mezclas).
const TONO: Readonly<
  Record<'lejos' | 'medio' | 'juego' | 'suelo' | 'frente', number>
> = {
  lejos: 0xdcd3bf,
  medio: 0xc2b9a5,
  juego: 0x9a917f,
  suelo: 0xd0c7b3,
  frente: 0x2b2b2b,
};
const TEXTO = {
  fontFamily: 'Georgia, serif',
  fontSize: '18px',
  color: '#1b1b1b',
};

/**
 * Escena de prueba del contrato de escala y capas (planeacion/arte/tomo1/escenarios/
 * contrato_escala.md). Greybox: valida proporciones y paralaje antes de producir fondos.
 * No es contenido del juego.
 */
export class PruebaEscenario extends Scene {
  constructor() {
    super('PruebaEscenario');
  }

  preload(): void {
    cargarAtlas(this, 'personajes');
  }

  create(): void {
    this.cameras.main.setBackgroundColor(PAPEL);
    const capas = new Map<IdCapa, GameObjects.Container>();
    for (const id of ORDEN_CAPAS) {
      const capa = this.add.container(0, 0).setScrollFactor(PARALAJE[id], 1);
      capas.set(id, capa);
    }
    const capa = (id: IdCapa) => capas.get(id) as GameObjects.Container;

    this.cielo(capa('cielo'));
    this.lejos(capa('lejos'));
    this.medio(capa('medio'));
    this.juego(capa('juego'));

    const rosalba = new Personaje(
      this,
      300,
      Y_SUELO,
      'personajes',
      APOYO_ROSALBA,
      ROSALBA_MONTE,
      'de-pie',
      { caminata: CAMINATA_ROSALBA },
    );
    rosalba.raiz.setScale(
      escalaPersonaje(ESTATURA_ROSALBA_M, ALTURA_DIBUJO_ROSALBA),
    );
    capa('juego').add(rosalba.raiz);
    // El primer plano va después del personaje para pasar por delante.
    this.frente(capa('frente'));

    const camara = this.cameras.main;
    camara.setBounds(0, 0, ANCHO_NIVEL, VIEWPORT.alto);
    camara.startFollow(rosalba.raiz, true, 0.08, 0);
    // El personaje queda a un tercio: se ve más mundo por delante que por detrás.
    camara.setFollowOffset(-VIEWPORT.ancho / 6, 0);
    camara.setDeadzone(160, VIEWPORT.alto);

    this.add
      .text(
        24,
        20,
        `Contrato de escala · ${PX_POR_METRO} px/m · suelo y=${Y_SUELO} · horizonte y=${Y_HORIZONTE} · capas ${ORDEN_CAPAS.map((c) => `${c} ${PARALAJE[c]}`).join(' · ')}`,
        TEXTO,
      )
      .setScrollFactor(0);

    void (async () => {
      for (;;) {
        rosalba.raiz.x = 300;
        await rosalba.caminarHasta(ANCHO_NIVEL - 300);
      }
    })();
  }

  private cielo(capa: GameObjects.Container): void {
    const g = this.add.graphics();
    g.lineStyle(1, TINTA, 0.5);
    for (let x = 0; x < VIEWPORT.ancho; x += 24) {
      g.lineBetween(x, Y_HORIZONTE, x + 12, Y_HORIZONTE);
    }
    capa.add([
      g,
      this.add.text(24, Y_HORIZONTE - 28, 'horizonte (ojos a 1,6 m)', TEXTO),
    ]);
  }

  private lejos(capa: GameObjects.Container): void {
    const f = PARALAJE.lejos;
    const ancho = anchoCapa(ANCHO_NIVEL, f);
    const suelo = ySueloCapa(f);
    const puntos = [new PhaserMath.Vector2(0, suelo)];
    for (let x = 0; x <= ancho; x += 120) {
      puntos.push(
        new PhaserMath.Vector2(
          x,
          suelo - 60 - 50 * Math.sin(x / 260) - 30 * Math.sin(x / 97),
        ),
      );
    }
    puntos.push(new PhaserMath.Vector2(ancho, suelo));
    const g = this.add.graphics();
    g.fillStyle(TONO.lejos, 1);
    g.fillPoints(puntos, true);
    g.fillStyle(TONO.lejos, 1);
    g.fillRect(0, suelo, ancho, Y_SUELO - suelo);
    capa.add([
      g,
      this.add.text(
        40,
        suelo - 150,
        `lejos · paralaje ${f} · cerros (a ojo)`,
        TEXTO,
      ),
    ]);
  }

  private medio(capa: GameObjects.Container): void {
    const f = PARALAJE.medio;
    const ppm = pxPorMetroCapa(f);
    const ancho = anchoCapa(ANCHO_NIVEL, f);
    const suelo = ySueloCapa(f);
    const g = this.add.graphics();
    g.fillStyle(TONO.medio, 1);
    // Casas de 7 m × 3,5 m con techo, y una torre de 14 m (greybox de iglesia a lo lejos).
    for (let x = 120; x < ancho - 300; x += 9 * ppm) {
      g.fillRect(x, suelo - 3.5 * ppm, 7 * ppm, 3.5 * ppm);
      g.fillTriangle(
        x - 0.4 * ppm,
        suelo - 3.5 * ppm,
        x + 3.5 * ppm,
        suelo - 5.5 * ppm,
        x + 7.4 * ppm,
        suelo - 3.5 * ppm,
      );
    }
    g.fillRect(ancho / 2, suelo - 14 * ppm, 4 * ppm, 14 * ppm);
    capa.add([
      g,
      this.add.text(
        40,
        suelo - 6.5 * ppm - 30,
        `medio · paralaje ${f} · ${ppm} px/m · casas de 7 m`,
        TEXTO,
      ),
    ]);
  }

  private juego(capa: GameObjects.Container): void {
    const ppm = PX_POR_METRO;
    const g = this.add.graphics();
    // Suelo
    g.fillStyle(TONO.suelo, 1);
    g.fillRect(0, Y_SUELO, ANCHO_NIVEL, VIEWPORT.alto - Y_SUELO);
    g.lineStyle(3, TINTA, 1);
    g.lineBetween(0, Y_SUELO, ANCHO_NIVEL, Y_SUELO);
    // Muros de 3 m con puertas de 2 m × 1 m (referencias greybox, no datos de época).
    for (let x = 900; x < ANCHO_NIVEL - 600; x += 1700) {
      g.fillStyle(TONO.juego, 1);
      g.fillRect(x, Y_SUELO - 3 * ppm, 6 * ppm, 3 * ppm);
      g.fillStyle(PAPEL, 1);
      g.fillRect(x + 2.5 * ppm, Y_SUELO - 2 * ppm, 1 * ppm, 2 * ppm);
      g.lineStyle(2, TINTA, 1);
      g.strokeRect(x + 2.5 * ppm, Y_SUELO - 2 * ppm, 1 * ppm, 2 * ppm);
    }
    // Regla vertical de 0 a 2 m, marcas cada 0,5 m.
    const textos: GameObjects.Text[] = [];
    g.lineStyle(2, TINTA, 1);
    g.lineBetween(120, Y_SUELO, 120, Y_SUELO - 2 * ppm);
    for (let m = 0; m <= 2; m += 0.5) {
      const y = Y_SUELO - m * ppm;
      g.lineBetween(110, y, 140, y);
      textos.push(
        this.add.text(148, y - 10, `${m.toLocaleString('es')} m`, TEXTO),
      );
    }
    textos.push(
      this.add.text(
        900,
        Y_SUELO - 3 * ppm - 30,
        'juego · 200 px/m · muro de 3 m, puerta de 2 m',
        TEXTO,
      ),
    );
    capa.add([g, ...textos]);
  }

  private frente(capa: GameObjects.Container): void {
    const f = PARALAJE.frente;
    const ppm = pxPorMetroCapa(f);
    const ancho = anchoCapa(ANCHO_NIVEL, f);
    const suelo = ySueloCapa(f);
    const g = this.add.graphics();
    g.fillStyle(TONO.frente, 1);
    // Postes de cerca de 1,4 m cada 6 m.
    for (let x = 500; x < ancho; x += 6 * ppm) {
      g.fillRect(
        x,
        suelo - 1.4 * ppm,
        0.14 * ppm,
        1.4 * ppm + (VIEWPORT.alto - suelo),
      );
    }
    capa.add(g);
  }
}
