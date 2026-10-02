import type { Scene } from 'phaser';
import { rutaAtlas } from '../core/arte/atlas.ts';

/**
 * Encola en el loader de la escena los multiatlas de los grupos indicados (un atlas por
 * carpeta de art/src; ver src/core/arte/atlas.ts). La clave de textura es el nombre del
 * grupo ("personajes", "fondos/puente-alto") y los frames conservan su ruta completa.
 */
export function cargarAtlas(escena: Scene, ...grupos: string[]): void {
  for (const grupo of grupos) {
    const { json, carpeta } = rutaAtlas(grupo);
    escena.load.multiatlas(grupo, json, carpeta);
  }
}
