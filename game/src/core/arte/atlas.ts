/**
 * Convención de atlas compartida por el pipeline (tools/art-build.ts) y el juego.
 *
 * Un atlas por carpeta de art/src: el grupo de un SVG es la carpeta que lo contiene
 * ("personajes/rosalba.svg" → "personajes"; "fondos/puente-alto/plaza.svg" →
 * "fondos/puente-alto"). Así cada escena carga solo los atlas que usa. Los SVG sueltos en
 * la raíz de art/src van al grupo "general". Cada atlas es un multiatlas de Phaser: si no
 * cabe en una textura se reparte en varias páginas bajo la misma clave.
 *
 * Los nombres de frame no cambian: "<ruta del svg sin extensión>[/<pieza>]".
 */
export const GRUPO_RAIZ = 'general';

/** Lado máximo de una página de atlas, en px (límite seguro de textura WebGL en equipos modestos). */
export const LADO_MAXIMO_ATLAS = 4096;

/**
 * Grupo (clave de atlas en Phaser) de un SVG, a partir de su ruta en art/src sin extensión:
 * "personajes/rosalba" → "personajes"; "plaza" → "general".
 */
export function grupoDe(rutaSvg: string): string {
  const partes = rutaSvg.split('/');
  partes.pop();
  return partes.length === 0 ? GRUPO_RAIZ : partes.join('/');
}

/** Nombre base de los archivos del atlas de un grupo: "fondos/puente-alto" → "fondos-puente-alto". */
export function archivoDeGrupo(grupo: string): string {
  return grupo.replaceAll('/', '-');
}

/** Ruta pública del JSON del atlas de un grupo (las páginas PNG están en la misma carpeta). */
export function rutaAtlas(
  grupo: string,
  escala = 1,
): { json: string; carpeta: string } {
  return {
    json: `generated/art/${archivoDeGrupo(grupo)}@${escala}x.json`,
    carpeta: 'generated/art/',
  };
}
