import type { GameObjects, Scene, Tweens } from 'phaser';
import { poseAcecho } from '../core/animacion/acecho.ts';
import { caminar, type OpcionesCaminar } from './Caminata.ts';
import { armarRecorte } from './Recorte.ts';

/** Una pose dibujada del personaje: frames "<base>/<pieza>" del atlas, en orden de dibujo. */
export interface DefinicionPose {
  base: string;
  piezas: readonly string[];
}

interface Rig {
  contenedor: GameObjects.Container;
  piezas: Map<string, GameObjects.Container>;
  /** Posición de reposo de cada pieza y del contenedor (la caminata las altera). */
  reposo: Map<string, { x: number; y: number }>;
  yBase: number;
}

/**
 * Personaje cut-out con varias poses dibujadas (p. ej. de pie y agachada) que comparten
 * un punto de apoyo. La raíz está en los pies: escalar la raíz aplasta o estira el
 * personaje sin que los pies se muevan, y moverla lo desplaza por el suelo.
 */
export class Personaje {
  readonly raiz: GameObjects.Container;
  private readonly escena: Scene;
  private readonly rigs = new Map<string, Rig>();
  private poseActual: string;
  private animacion: Tweens.Tween | null = null;
  private readonly opcionesCaminata: OpcionesCaminar;

  constructor(
    escena: Scene,
    x: number,
    ySuelo: number,
    atlas: string,
    /** Punto de apoyo (entre los pies) en coordenadas del SVG, igual en todas las poses. */
    apoyo: { x: number; y: number },
    poses: Record<string, DefinicionPose>,
    inicial: string,
    /** Cómo camina este personaje (p. ej. pies bajo falda larga, duración del ciclo). */
    opcionesCaminata: OpcionesCaminar = {},
  ) {
    this.escena = escena;
    this.opcionesCaminata = opcionesCaminata;
    this.raiz = escena.add.container(x, ySuelo);
    for (const [nombre, def] of Object.entries(poses)) {
      const rig = armarRecorte(
        escena,
        -apoyo.x,
        -apoyo.y,
        atlas,
        def.base,
        def.piezas,
      );
      rig.contenedor.setVisible(nombre === inicial);
      this.raiz.add(rig.contenedor);
      this.rigs.set(nombre, {
        ...rig,
        reposo: new Map(
          [...rig.piezas].map(([id, p]) => [id, { x: p.x, y: p.y }]),
        ),
        yBase: rig.contenedor.y,
      });
    }
    if (!this.rigs.has(inicial))
      throw new Error(`Pose inicial inexistente: ${inicial}`);
    this.poseActual = inicial;
  }

  get pose(): string {
    return this.poseActual;
  }

  /** Empieza a caminar en la pose actual; devuelve la velocidad (px/s a escala 1). */
  caminar(): number {
    this.quieto();
    const rig = this.rig();
    const caminata = caminar(
      this.escena,
      rig.contenedor,
      rig.piezas,
      this.opcionesCaminata,
    );
    this.animacion = caminata.tween;
    return caminata.velocidad * this.raiz.scaleX;
  }

  /** Camina hasta la x indicada a la velocidad que no hace patinar los pies, y se detiene. */
  async caminarHasta(x: number): Promise<void> {
    const velocidad = this.caminar();
    const duracion = (Math.abs(x - this.raiz.x) / velocidad) * 1000;
    await this.interpolar({ x }, duracion, 'Linear');
    this.quieto();
  }

  /** Acecho: respiración y mirada alrededor, sin desplazarse. */
  acechar(): void {
    this.quieto();
    const rig = this.rig();
    const inicio = this.escena.time.now;
    this.animacion = this.escena.tweens.addCounter({
      from: 0,
      to: 1,
      duration: 1000,
      repeat: -1,
      onUpdate: () => {
        const { angulos } = poseAcecho((this.escena.time.now - inicio) / 1000);
        for (const [id, angulo] of Object.entries(angulos)) {
          const pieza = rig.piezas.get(id);
          if (pieza) pieza.angle = angulo;
        }
      },
    });
  }

  /** Detiene la animación y devuelve todas las piezas a su posición de reposo. */
  quieto(): void {
    this.animacion?.remove();
    this.animacion = null;
    const rig = this.rig();
    rig.contenedor.y = rig.yBase;
    for (const [id, pieza] of rig.piezas) {
      pieza.angle = 0;
      const r = rig.reposo.get(id);
      if (r) pieza.setPosition(r.x, r.y);
    }
  }

  /**
   * Cambia de pose con un aplastamiento breve, como en animación limitada: la pose actual
   * se comprime hacia el suelo, se sustituye y la nueva rebota hasta su altura.
   */
  async cambiarPose(nombre: string, duracion = 260): Promise<void> {
    if (nombre === this.poseActual) return;
    const destino = this.rigs.get(nombre);
    if (!destino) throw new Error(`Pose inexistente: ${nombre}`);
    const escalaX = this.raiz.scaleX;
    const escalaY = this.raiz.scaleY;
    this.quieto();
    await this.interpolar(
      { scaleY: escalaY * 0.88, scaleX: escalaX * 1.04 },
      duracion * 0.4,
      'Quad.easeIn',
    );
    this.rig().contenedor.setVisible(false);
    destino.contenedor.setVisible(true);
    this.poseActual = nombre;
    this.quieto();
    await this.interpolar(
      { scaleY: escalaY, scaleX: escalaX },
      duracion * 0.6,
      'Back.easeOut',
    );
  }

  private interpolar(
    valores: Record<string, number>,
    duracion: number,
    ease: string,
  ): Promise<void> {
    return new Promise((resolver) => {
      this.escena.tweens.add({
        targets: this.raiz,
        ...valores,
        duration: duracion,
        ease,
        onComplete: () => resolver(),
      });
    });
  }

  private rig(): Rig {
    const rig = this.rigs.get(this.poseActual);
    if (!rig) throw new Error(`Pose inexistente: ${this.poseActual}`);
    return rig;
  }
}
