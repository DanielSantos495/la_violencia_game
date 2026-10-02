import type { GameObjects, Scene } from 'phaser';
import {
  anchoCapa,
  type IdCapa,
  ORDEN_CAPAS,
  PARALAJE,
  VIEWPORT,
} from '../../core/escena/escala.ts';
import {
  copiasMosaico,
  type DefinicionEscenario,
  envolver,
  frameDe,
  yColocacion,
} from '../../core/escenarios/escenario.ts';
import { cargarAtlas } from '../arte.ts';

/** Encola el atlas del escenario; llamar desde preload(). */
export function precargarEscenario(
  escena: Scene,
  def: DefinicionEscenario,
): void {
  cargarAtlas(escena, def.atlas);
}

interface Deriva {
  imagen: GameObjects.Image;
  velocidad: number;
}

/**
 * Arma un escenario por capas (src/core/escenarios/): un contenedor por capa con el factor de
 * paralaje del contrato (escala.ts), los mosaicos de suelo repetidos y los módulos colocados.
 * Los personajes se añaden a `capa('juego')`; el frente queda delante de ellos.
 */
export class Escenario {
  readonly anchoNivel: number;
  private readonly capas = new Map<IdCapa, GameObjects.Container>();
  private readonly derivas: Deriva[] = [];

  constructor(escena: Scene, def: DefinicionEscenario) {
    this.anchoNivel = def.anchoNivel;
    for (const id of ORDEN_CAPAS) {
      const capa = escena.add.container(0, 0).setScrollFactor(PARALAJE[id], 1);
      this.capas.set(id, capa);
      const datos = def.capas[id];
      if (!datos) continue;
      const ancho = anchoCapa(def.anchoNivel, PARALAJE[id]);
      for (const mosaico of datos.mosaicos ?? []) {
        const frame = frameDe(def, mosaico.modulo);
        const anchoModulo = escena.textures.getFrame(
          def.atlas,
          frame,
        ).realWidth;
        for (const x of copiasMosaico(anchoModulo, ancho)) {
          capa.add(
            escena.add.image(x, mosaico.y, def.atlas, frame).setOrigin(0, 0),
          );
        }
      }
      for (const col of datos.colocaciones) {
        // Origen en la base o en el borde de arriba del viewBox (los frames vienen recortados,
        // pero Phaser aplica el origen al tamaño de origen del SVG).
        const imagen = escena.add
          .image(
            col.x,
            yColocacion(col, id),
            def.atlas,
            frameDe(def, col.modulo),
          )
          .setOrigin(0, col.ancla === 'arriba' ? 0 : 1)
          .setFlipX(col.espejo ?? false);
        capa.add(imagen);
        if (col.deriva) this.derivas.push({ imagen, velocidad: col.deriva });
      }
    }
  }

  /** Contenedor de una capa (p. ej. 'juego' para los personajes). */
  capa(id: IdCapa): GameObjects.Container {
    const capa = this.capas.get(id);
    if (!capa) throw new Error(`Capa desconocida: ${id}`);
    return capa;
  }

  /** Mueve lo que deriva (nubes) y lo hace volver por el otro lado; llamar desde update(). */
  actualizar(deltaMs: number): void {
    for (const { imagen, velocidad } of this.derivas) {
      imagen.x = envolver(
        imagen.x + (velocidad * deltaMs) / 1000,
        imagen.width,
        VIEWPORT.ancho,
      );
    }
  }
}
