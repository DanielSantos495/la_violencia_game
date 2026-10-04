import type { GameObjects, Scene, Tweens } from 'phaser';
import { poseAcecho } from '../core/animacion/acecho.ts';
import {
  DATOS_EXPRESION,
  type Expresion,
  intervaloParpadeo,
  PIEZAS_POSTURA_CABEZA,
} from '../core/animacion/expresiones.ts';
import { caminar, type OpcionesCaminar } from './Caminata.ts';
import { correr, type OpcionesCorrer } from './Carrera.ts';
import { armarRecorte } from './Recorte.ts';

/** Una pose dibujada del personaje: frames "<base>/<pieza>" del atlas, en orden de dibujo. */
export interface DefinicionPose {
  base: string;
  piezas: readonly string[];
  /**
   * Base de las cabezas por expresión para esta pose ("<cabezas>/<expresión>" y
   * "<cabezas>/parpado-<expresión>"), con el mismo pivote que la pieza `cabeza`.
   */
  cabezas?: string;
  /**
   * Qué mueve la postura de la expresión en esta pose: todo el cuerpo (por defecto) o solo
   * la cabeza (p. ej. agachada, con la mano apoyada en el suelo).
   */
  postura?: 'cuerpo' | 'cabeza';
}

export interface OpcionesPersonaje {
  /** Cómo camina (p. ej. pies bajo falda larga, duración del ciclo). */
  caminata?: OpcionesCaminar;
  /** Cómo corre en su pose de correr (largo de canilla, duración del ciclo…). */
  carrera?: OpcionesCorrer;
  /** Expresión inicial. */
  expresion?: Expresion;
  /** Piezas que empiezan ocultas en todas las poses (p. ej. la cinta de Rosalba). */
  ocultas?: readonly string[];
}

interface Rig {
  contenedor: GameObjects.Container;
  piezas: Map<string, GameObjects.Container>;
  /** Posición de reposo de cada pieza y del contenedor (la caminata las altera). */
  reposo: Map<string, { x: number; y: number }>;
  yBase: number;
  /** Postura de la expresión que admite esta pose (copia filtrada de la del personaje). */
  postura: Record<string, number>;
  soloCabeza: boolean;
  /** Imagen de la cabeza (cambia de frame con la expresión) y su capa de parpadeo. */
  cabezas?: string;
  cabeza?: GameObjects.Image;
  parpado?: GameObjects.Image;
}

/**
 * Personaje cut-out con varias poses dibujadas (p. ej. de pie y agachada) que comparten
 * un punto de apoyo, y con expresiones (core/animacion/expresiones.ts). La raíz está en los
 * pies: escalar la raíz aplasta o estira el personaje sin que los pies se muevan, y moverla
 * lo desplaza por el suelo.
 */
export class Personaje {
  readonly raiz: GameObjects.Container;
  private readonly escena: Scene;
  private readonly atlas: string;
  private readonly rigs = new Map<string, Rig>();
  private poseActual: string;
  private animacion: Tweens.Tween | null = null;
  private readonly opcionesCaminata: OpcionesCaminar;
  private readonly opcionesCarrera: OpcionesCorrer;
  private expresionActual: Expresion = 'neutral';
  /** Ángulos de la expresión que se suman a la pose; se interpola al cambiar de expresión. */
  private readonly postura: Record<string, number> = {};
  private transicionPostura: Tweens.Tween | null = null;

  constructor(
    escena: Scene,
    x: number,
    ySuelo: number,
    atlas: string,
    /** Punto de apoyo (entre los pies) en coordenadas del SVG, igual en todas las poses. */
    apoyo: { x: number; y: number },
    poses: Record<string, DefinicionPose>,
    inicial: string,
    opciones: OpcionesPersonaje = {},
  ) {
    this.escena = escena;
    this.atlas = atlas;
    this.opcionesCaminata = opciones.caminata ?? {};
    this.opcionesCarrera = opciones.carrera ?? {};
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
      const datos: Rig = {
        ...rig,
        reposo: new Map(
          [...rig.piezas].map(([id, p]) => [id, { x: p.x, y: p.y }]),
        ),
        yBase: rig.contenedor.y,
        postura: {},
        soloCabeza: def.postura === 'cabeza',
      };
      if (def.cabezas) this.prepararCabezas(datos, def.cabezas);
      this.rigs.set(nombre, datos);
    }
    if (!this.rigs.has(inicial))
      throw new Error(`Pose inicial inexistente: ${inicial}`);
    this.poseActual = inicial;
    for (const id of opciones.ocultas ?? []) this.mostrarPieza(id, false);
    this.expresion(opciones.expresion ?? 'neutral', 0);
    this.programarParpadeo();
  }

  get pose(): string {
    return this.poseActual;
  }

  get gesto(): Expresion {
    return this.expresionActual;
  }

  /** Muestra u oculta una pieza (y lo que cuelga de ella) en todas las poses. */
  mostrarPieza(id: string, visible: boolean): void {
    let hallada = false;
    for (const rig of this.rigs.values()) {
      const pieza = rig.piezas.get(id);
      if (!pieza) continue;
      pieza.setVisible(visible);
      hallada = true;
    }
    if (!hallada) throw new Error(`Pieza inexistente: ${id}`);
  }

  /**
   * Cambia la expresión en todas las poses: el dibujo cambia de golpe (como en una viñeta) y
   * la postura se interpola en `duracion` ms.
   */
  expresion(nombre: Expresion, duracion = 220): void {
    this.expresionActual = nombre;
    for (const rig of this.rigs.values()) {
      if (!rig.cabezas) continue;
      rig.cabeza?.setFrame(`${rig.cabezas}/${nombre}`);
      rig.parpado?.setFrame(`${rig.cabezas}/parpado-${nombre}`);
    }
    const destino: Record<string, number> = {
      ...DATOS_EXPRESION[nombre].postura,
    };
    for (const id of Object.keys(this.postura)) destino[id] ??= 0;

    this.transicionPostura?.remove();
    this.transicionPostura = null;
    if (duracion <= 0) {
      Object.assign(this.postura, destino);
      this.sincronizarPostura();
      return;
    }
    for (const id of Object.keys(destino)) this.postura[id] ??= 0;
    this.transicionPostura = this.escena.tweens.add({
      targets: this.postura,
      ...destino,
      duration: duracion,
      ease: 'Sine.easeOut',
      onUpdate: () => this.sincronizarPostura(),
    });
  }

  /** Empieza a caminar en la pose actual; devuelve la velocidad (px/s a escala 1). */
  caminar(): number {
    this.quieto();
    const rig = this.rig();
    const caminata = caminar(this.escena, rig.contenedor, rig.piezas, {
      ...this.opcionesCaminata,
      postura: rig.postura,
    });
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

  /** Corre en la pose actual (debe ser la de correr); devuelve la velocidad en px/s. */
  correr(): number {
    this.quieto();
    const rig = this.rig();
    const carrera = correr(this.escena, rig.contenedor, rig.piezas, {
      ...this.opcionesCarrera,
      postura: rig.postura,
    });
    this.animacion = carrera.tween;
    return carrera.velocidad * this.raiz.scaleX;
  }

  /**
   * Pasa a la pose de correr y corre hasta la x indicada a la velocidad que no hace patinar
   * los pies; se queda en esa pose (quien llama decide si vuelve a estar de pie).
   */
  async correrHasta(x: number, pose = 'corriendo'): Promise<void> {
    if (this.poseActual !== pose) await this.cambiarPose(pose, 180);
    const velocidad = this.correr();
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
        for (const [id, pieza] of rig.piezas) {
          if (id in angulos || id in rig.postura) {
            pieza.angle = (angulos[id] ?? 0) + (rig.postura[id] ?? 0);
          }
        }
      },
    });
  }

  /** Detiene la animación y devuelve todas las piezas a su reposo (con la postura de la expresión). */
  quieto(): void {
    this.animacion?.remove();
    this.animacion = null;
    const rig = this.rig();
    rig.contenedor.y = rig.yBase;
    for (const [id, pieza] of rig.piezas) {
      pieza.angle = rig.postura[id] ?? 0;
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

  /** La cabeza de la pose pasa a mostrar las cabezas por expresión, con capa de parpadeo. */
  private prepararCabezas(rig: Rig, cabezas: string): void {
    const contenedor = rig.piezas.get('cabeza');
    const imagen = contenedor?.list[0];
    if (!contenedor || !imagen || !('setFrame' in imagen)) {
      throw new Error(`La pose con cabezas "${cabezas}" no tiene pieza cabeza`);
    }
    const textura = this.escena.textures.get(this.atlas);
    for (const e of Object.keys(DATOS_EXPRESION)) {
      for (const frame of [`${cabezas}/${e}`, `${cabezas}/parpado-${e}`]) {
        if (!textura.has(frame)) throw new Error(`Frame inexistente: ${frame}`);
      }
    }
    rig.cabezas = cabezas;
    rig.cabeza = imagen as GameObjects.Image;
    // El parpadeo va encima de todo lo que cuelga de la cabeza (sombrero, zarcillo, mechones).
    rig.parpado = this.escena.add.image(
      0,
      0,
      this.atlas,
      `${cabezas}/parpado-neutral`,
    );
    rig.parpado.setVisible(false);
    contenedor.add(rig.parpado);
  }

  /** Parpadea a intervalos irregulares según la expresión (a veces dos veces seguidas). */
  private programarParpadeo(): void {
    const { parpadeo } = DATOS_EXPRESION[this.expresionActual];
    this.escena.time.delayedCall(
      intervaloParpadeo(this.expresionActual, Math.random),
      () => {
        const veces = Math.random() < parpadeo.doble ? 2 : 1;
        for (let i = 0; i < veces; i++) {
          const inicio = i * (parpadeo.dura + 90);
          this.escena.time.delayedCall(inicio, () => this.ojosCerrados(true));
          this.escena.time.delayedCall(inicio + parpadeo.dura, () =>
            this.ojosCerrados(false),
          );
        }
        this.programarParpadeo();
      },
    );
  }

  private ojosCerrados(cerrados: boolean): void {
    for (const rig of this.rigs.values()) rig.parpado?.setVisible(cerrados);
  }

  /**
   * Copia la postura del personaje a cada pose según lo que admite, y la aplica si la pose
   * está quieta (caminata y acecho la leen en cada cuadro).
   */
  private sincronizarPostura(): void {
    for (const rig of this.rigs.values()) {
      for (const [id, angulo] of Object.entries(this.postura)) {
        if (rig.soloCabeza && !PIEZAS_POSTURA_CABEZA.includes(id)) continue;
        rig.postura[id] = angulo;
      }
    }
    if (this.animacion) return;
    const rig = this.rig();
    for (const [id, pieza] of rig.piezas) {
      if (id in rig.postura) pieza.angle = rig.postura[id] ?? 0;
    }
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
