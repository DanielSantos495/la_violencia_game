/**
 * Paleta del juego: game/art/paleta.json (reglas y fuentes en planeacion/arte/tomo1/paleta.md).
 * El código pide los colores por id de token, nunca con un hex suelto.
 */
import datos from '../../../art/paleta.json';

const HEX = new Map(datos.colores.map((c) => [c.id, c.hex]));

/** Hex (#rrggbb) de un token de la paleta. */
export function color(id: string): string {
  const hex = HEX.get(id);
  if (!hex) throw new Error(`La paleta no tiene el color ${id}`);
  return hex;
}

/** Un token como número 0xrrggbb, para Phaser (cámara, Graphics, tinte). */
export function colorNumero(id: string): number {
  return Number.parseInt(color(id).slice(1), 16);
}
