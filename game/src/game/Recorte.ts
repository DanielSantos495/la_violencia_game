import type { GameObjects, Scene } from 'phaser';

/**
 * Arma un personaje por piezas (cut-out) desde el atlas generado por tools/art-build.ts.
 * Cada frame es "<base>/<pieza>", recortado y con pivote; el contenedor queda con su
 * origen en la esquina superior izquierda del viewBox del SVG fuente.
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
  piezas: Map<string, GameObjects.Image>;
} {
  const contenedor = escena.add.container(x, y);
  const mapa = new Map<string, GameObjects.Image>();
  for (const id of piezas) {
    const frame = escena.textures.getFrame(atlas, `${base}/${id}`);
    if (!frame) throw new Error(`Frame inexistente: ${base}/${id}`);
    // Con pivote propio el origen ya viene del frame; se coloca la pieza en su pivote.
    const img = escena.add.image(
      frame.pivotX * frame.realWidth,
      frame.pivotY * frame.realHeight,
      atlas,
      frame.name,
    );
    contenedor.add(img);
    mapa.set(id, img);
  }
  return { contenedor, piezas: mapa };
}
