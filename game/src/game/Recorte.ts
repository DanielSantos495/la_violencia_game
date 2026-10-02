import type { GameObjects, Scene } from 'phaser';

/**
 * Arma un personaje por piezas (cut-out) desde el atlas generado por tools/art-build.ts.
 * Cada frame es "<base>/<pieza>", recortado y con pivote. Cada pieza vive en su propio
 * contenedor colocado en su pivote, así que girar ese contenedor gira la pieza en su
 * articulación. Si el SVG declara data-padre (antebrazo → brazo, sombrero → cabeza), el
 * atlas lo trae en frame.customData.padre y la pieza cuelga de su padre y hereda su
 * movimiento. El contenedor raíz tiene el origen en la esquina superior izquierda del
 * viewBox del SVG fuente.
 *
 * El orden de `piezas` es el orden de dibujo; un hijo se dibuja justo encima de su padre.
 */
export function armarRecorte(
  escena: Scene,
  x: number,
  y: number,
  atlas: string,
  base: string,
  piezas: readonly string[],
): {
  contenedor: GameObjects.Container;
  piezas: Map<string, GameObjects.Container>;
} {
  const contenedor = escena.add.container(x, y);
  const mapa = new Map<string, GameObjects.Container>();
  const pivotes = new Map<string, { x: number; y: number }>();

  for (const id of piezas) {
    const frame = escena.textures.getFrame(atlas, `${base}/${id}`);
    if (!frame) throw new Error(`Frame inexistente: ${base}/${id}`);
    if (!frame.customPivot)
      throw new Error(`La pieza ${base}/${id} no tiene data-pivote`);
    const pivote = {
      x: frame.pivotX * frame.realWidth,
      y: frame.pivotY * frame.realHeight,
    };

    const datos = frame.customData as { padre?: unknown } | null;
    const idPadre = typeof datos?.padre === 'string' ? datos.padre : null;
    const padre = idPadre ? mapa.get(idPadre) : contenedor;
    const pivotePadre = idPadre ? pivotes.get(idPadre) : { x: 0, y: 0 };
    if (!padre || !pivotePadre) {
      throw new Error(
        `El padre "${idPadre}" de ${id} debe ir antes en la lista de piezas`,
      );
    }

    const articulacion = escena.add.container(
      pivote.x - pivotePadre.x,
      pivote.y - pivotePadre.y,
    );
    // Con pivote propio el origen de la imagen ya es el pivote del frame.
    articulacion.add(escena.add.image(0, 0, atlas, frame.name));
    padre.add(articulacion);
    mapa.set(id, articulacion);
    pivotes.set(id, pivote);
  }
  return { contenedor, piezas: mapa };
}
