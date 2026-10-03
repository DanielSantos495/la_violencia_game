// Grafo de ramas del guion Ink (P23, doc 10): knots, stitches, diverts y opciones.
//   node tools/ink-graph.ts                 → todos los content/ink/*.ink
//   node tools/ink-graph.ts prologo.ink     → solo ese archivo (con sus INCLUDE)
// Salida en build/ink-grafo/: <nombre>.svg (vector), <nombre>.png (@2x) y <nombre>.dot.
// Además revisa el flujo: diverts a destinos inexistentes, nodos inalcanzables y callejones
// sin salida. Analiza el texto fuente (no el JSON compilado); compila antes con ink:build.
// Colores: tokens de art/paleta.json. Sin rojo ni azul: están reservados a los partidos (doc 03).
import { mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { basename, dirname, join, resolve } from 'node:path';
import { Resvg } from '@resvg/resvg-js';
import { instance } from '@viz-js/viz';

export type TipoArista = 'divert' | 'opcion' | 'hilo' | 'tunel';

export interface Arista {
  desde: string;
  hacia: string;
  tipo: TipoArista;
  /** Texto de la opción (sin corchetes), si la arista sale de una opción. */
  etiqueta?: string;
  /** Opción o divert dentro de una condición. */
  condicional: boolean;
  /** Opción persistente (+). */
  persistente: boolean;
  /** Entrada implícita de un knot a su primer stitch (no está escrita en el fuente). */
  implicita?: boolean;
}

export interface Nodo {
  id: string;
  /** Knot al que pertenece (para stitches); null para knots y nodos especiales. */
  knot: string | null;
  tipo: 'inicio' | 'knot' | 'stitch' | 'fin';
  escribe: Set<string>;
  hablantes: Set<string>;
  opciones: number;
  /** Línea de declaración en el fuente unido (1-based); 0 para nodos especiales. */
  linea: number;
}

export interface Aviso {
  tipo: 'destino-inexistente' | 'inalcanzable' | 'sin-salida';
  nodo: string;
  detalle: string;
}

export interface Grafo {
  nodos: Map<string, Nodo>;
  aristas: Arista[];
  avisos: Aviso[];
}

const INICIO = '·inicio';
const FIN = 'END';
const HECHO = 'DONE';

/** Quita comentarios // y /* *\/ conservando los saltos de línea (para no mover las líneas). */
export function sinComentarios(fuente: string): string {
  return fuente
    .replace(/\/\*[\s\S]*?\*\//g, (m) => m.replace(/[^\n]/g, ''))
    .replace(/(^|[^:])\/\/.*$/gm, '$1');
}

/** Une un archivo con sus INCLUDE (rutas relativas a `base`), sin repetir archivos. */
export function unirIncludes(
  fuente: string,
  leer: (ruta: string) => string,
  vistos = new Set<string>(),
): string {
  return fuente.replace(/^\s*INCLUDE\s+(.+?)\s*$/gm, (_m, ruta: string) => {
    if (vistos.has(ruta)) return '';
    vistos.add(ruta);
    return unirIncludes(leer(ruta), leer, vistos);
  });
}

function nuevoNodo(
  id: string,
  tipo: Nodo['tipo'],
  knot: string | null,
  linea: number,
): Nodo {
  return {
    id,
    knot,
    tipo,
    escribe: new Set(),
    hablantes: new Set(),
    opciones: 0,
    linea,
  };
}

const RE_KNOT =
  /^\s*={2,}\s*(?:function\s+)?([A-Za-z_][\w]*)\s*(?:\([^)]*\))?\s*=*\s*$/;
const RE_STITCH = /^\s*=\s*([A-Za-z_][\w]*)\s*(?:\([^)]*\))?\s*$/;
const RE_OPCION = /^\s*((?:[*+]\s*)+)(.*)$/;
const RE_ESCRITURA =
  /^\s*~\s*(?:temp\s+)?([A-Za-z_][\w]*)\s*(?:=(?!=)|\+\+|--|\+=|-=)/;
const RE_HABLANTE = /#\s*hablante\s*:\s*([^#]+)/gi;
const RE_DIVERT = /(<-|->)\s*([A-Za-z_][\w.]*)(\s*->(?!>))?/g;
const RE_ETIQUETA = /^\s*(?:[-*+]\s*)+\(([A-Za-z_]\w*)\)/;

/** Analiza el fuente Ink (ya unido con sus INCLUDE) y devuelve el grafo con sus avisos. */
export function analizarInk(fuenteBruta: string): Grafo {
  const lineas = sinComentarios(fuenteBruta).split('\n');
  const nodos = new Map<string, Nodo>();
  const funciones = new Set<string>();
  /** Etiquetas de gathers y opciones: `knot.etiqueta` (y `knot.stitch.etiqueta`) → nodo. */
  const etiquetas = new Map<string, string>();
  const aristas: Arista[] = [];
  nodos.set(INICIO, nuevoNodo(INICIO, 'inicio', null, 0));

  // Primera pasada: declarar knots y stitches para resolver destinos.
  let knotActual: string | null = null;
  let nodoDecl: string = INICIO;
  lineas.forEach((linea, i) => {
    const k = RE_KNOT.exec(linea);
    if (k?.[1]) {
      knotActual = k[1];
      nodoDecl = k[1];
      if (/^\s*={2,}\s*function\b/.test(linea)) funciones.add(k[1]);
      else nodos.set(k[1], nuevoNodo(k[1], 'knot', null, i + 1));
      return;
    }
    const s = RE_STITCH.exec(linea);
    if (s?.[1] && knotActual && !funciones.has(knotActual)) {
      const id = `${knotActual}.${s[1]}`;
      nodoDecl = id;
      nodos.set(id, nuevoNodo(id, 'stitch', knotActual, i + 1));
      return;
    }
    const e = RE_ETIQUETA.exec(linea);
    if (e?.[1]) {
      etiquetas.set(`${nodoDecl}.${e[1]}`, nodoDecl);
      if (knotActual) etiquetas.set(`${knotActual}.${e[1]}`, nodoDecl);
    }
  });

  const avisos: Aviso[] = [];
  const resolver = (destino: string, knot: string | null): string | null => {
    if (destino === FIN || destino === HECHO) return destino;
    if (nodos.has(destino)) return destino;
    if (knot && nodos.has(`${knot}.${destino}`)) return `${knot}.${destino}`;
    const etiqueta =
      etiquetas.get(destino) ??
      (knot ? etiquetas.get(`${knot}.${destino}`) : undefined);
    return etiqueta ?? null;
  };

  // Segunda pasada: aristas, escrituras, hablantes y opciones.
  knotActual = null;
  let nodoActual = INICIO;
  let profundidadCond = 0;
  /** Opción cuyo contenido sigue en las líneas de abajo (su divert puede llegar después). */
  let abierta: {
    etiqueta: string;
    persistente: boolean;
    condicional: boolean;
  } | null = null;
  lineas.forEach((linea, i) => {
    const k = RE_KNOT.exec(linea);
    if (k?.[1]) {
      knotActual = k[1];
      nodoActual = funciones.has(k[1]) ? '' : k[1];
      profundidadCond = 0;
      abierta = null;
      return;
    }
    const s = RE_STITCH.exec(linea);
    if (s?.[1] && knotActual) {
      nodoActual = funciones.has(knotActual) ? '' : `${knotActual}.${s[1]}`;
      abierta = null;
      return;
    }
    if (!nodoActual) return; // contenido de funciones: no forma parte del flujo
    const nodo = nodos.get(nodoActual);
    if (!nodo) return;

    const esc = RE_ESCRITURA.exec(linea);
    if (esc?.[1]) nodo.escribe.add(esc[1]);
    for (const h of linea.matchAll(RE_HABLANTE)) {
      const nombre = h[1]?.trim();
      if (nombre) nodo.hablantes.add(nombre);
    }

    const opcion = RE_OPCION.exec(linea);
    const marcas = opcion?.[1] ?? '';
    const cuerpo = opcion ? (opcion[2] ?? '') : linea;
    if (opcion) nodo.opciones++;
    const etiqueta = opcion ? textoOpcion(cuerpo) : undefined;
    const condicionalLinea =
      profundidadCond > 0 ||
      (opcion !== null && /^\s*(?:\([^)]*\)\s*)?\{/.test(cuerpo));
    if (!opcion && /^\s*-(?!>)/.test(linea)) abierta = null; // un gather cierra la opción
    const efectiva = opcion
      ? {
          etiqueta: etiqueta ?? '',
          persistente: marcas.includes('+'),
          condicional: condicionalLinea,
        }
      : abierta;
    let huboDivert = false;

    for (const d of linea.matchAll(RE_DIVERT)) {
      const flecha = d[1];
      const destino = d[2] ?? '';
      const previo = linea.slice(0, d.index ?? 0);
      const enLlaves =
        (previo.match(/\{/g) ?? []).length > (previo.match(/\}/g) ?? []).length;
      const resuelto = resolver(destino, knotActual);
      if (!resuelto) {
        avisos.push({
          tipo: 'destino-inexistente',
          nodo: nodoActual,
          detalle: `línea ${i + 1}: -> ${destino}`,
        });
        continue;
      }
      if (resuelto === FIN || resuelto === HECHO) {
        if (!nodos.has(resuelto))
          nodos.set(resuelto, nuevoNodo(resuelto, 'fin', null, 0));
      }
      const tipo: TipoArista =
        flecha === '<-'
          ? 'hilo'
          : d[3]
            ? 'tunel'
            : efectiva
              ? 'opcion'
              : 'divert';
      if (tipo === 'opcion' || tipo === 'divert') huboDivert = true;
      aristas.push({
        desde: nodoActual,
        hacia: resuelto,
        tipo,
        etiqueta: tipo === 'opcion' ? efectiva?.etiqueta : undefined,
        condicional:
          condicionalLinea || enLlaves || (efectiva?.condicional ?? false),
        persistente: tipo === 'opcion' && (efectiva?.persistente ?? false),
      });
    }
    if (opcion) abierta = huboDivert ? null : efectiva;
    else if (huboDivert) abierta = null;

    // Profundidad de bloques condicionales { ... } multilínea (aprox.: llaves sin cerrar).
    const abre = (linea.match(/\{/g) ?? []).length;
    const cierra = (linea.match(/\}/g) ?? []).length;
    profundidadCond = Math.max(0, profundidadCond + abre - cierra);
  });

  // Un knot sin diverts propios entra a su primer stitch.
  for (const n of nodos.values()) {
    if (n.tipo !== 'knot' || aristas.some((a) => a.desde === n.id)) continue;
    const primero = [...nodos.values()]
      .filter((x) => x.knot === n.id)
      .sort((a, b) => a.linea - b.linea)[0];
    if (primero) {
      aristas.push({
        desde: n.id,
        hacia: primero.id,
        tipo: 'divert',
        condicional: false,
        persistente: false,
        implicita: true,
      });
    }
  }

  avisos.push(...revisarFlujo(nodos, aristas));
  return { nodos, aristas, avisos };
}

/** Texto visible de una opción: lo de antes del corchete más lo de dentro, sin diverts ni tags. */
export function textoOpcion(cuerpo: string): string {
  const limpio = cuerpo
    .replace(/^\s*\([^)]*\)\s*/, '')
    .replace(/^\s*\{[^}]*\}\s*/, '')
    .replace(/(<-|->).*$/, '')
    .replace(/#.*$/, '');
  const m = /^(.*?)\[(.*?)\]/.exec(limpio);
  const texto = m ? `${m[1] ?? ''}${m[2] ?? ''}` : limpio;
  return texto.replace(/\s+/g, ' ').trim();
}

function revisarFlujo(nodos: Map<string, Nodo>, aristas: Arista[]): Aviso[] {
  const avisos: Aviso[] = [];
  const salidas = new Map<string, string[]>();
  for (const a of aristas) {
    const lista = salidas.get(a.desde) ?? [];
    lista.push(a.hacia);
    salidas.set(a.desde, lista);
  }
  const alcanzables = new Set<string>([INICIO]);
  const pila = [INICIO];
  while (pila.length > 0) {
    const actual = pila.pop() as string;
    for (const sig of salidas.get(actual) ?? []) {
      if (!alcanzables.has(sig)) {
        alcanzables.add(sig);
        pila.push(sig);
      }
    }
  }
  for (const n of nodos.values()) {
    if (n.tipo === 'fin' || n.tipo === 'inicio') continue;
    if (!alcanzables.has(n.id)) {
      avisos.push({
        tipo: 'inalcanzable',
        nodo: n.id,
        detalle: `línea ${n.linea}`,
      });
    }
    if (!(salidas.get(n.id)?.length ?? 0)) {
      avisos.push({
        tipo: 'sin-salida',
        nodo: n.id,
        detalle: `línea ${n.linea}: no termina en divert, -> END ni -> DONE`,
      });
    }
  }
  return avisos;
}

// ---------- Estilo ----------

interface Tinta {
  papel: string;
  papelViejo: string;
  tinta: string;
  tintaPlena: string;
  sepiaOscuro: string;
  sepia: string;
  grafito: string;
}

/** Colores del grafo desde art/paleta.json (tokens, nunca hex sueltos). */
export function tintaDePaleta(paleta: {
  colores: { id: string; hex: string }[];
}): Tinta {
  const c = (id: string): string => {
    const hex = paleta.colores.find((x) => x.id === id)?.hex;
    if (!hex) throw new Error(`La paleta no tiene el color ${id}`);
    return hex;
  };
  return {
    papel: c('papel'),
    papelViejo: c('papel-viejo'),
    tinta: c('tinta'),
    tintaPlena: c('tinta-plena'),
    sepiaOscuro: c('sepia-oscuro'),
    sepia: c('sepia'),
    grafito: c('grafito'),
  };
}

// Graphviz solo conoce las medidas de Times y Courier: el layout se calcula con ellas y el SVG
// se dibuja con fuentes de medidas compatibles (Times New Roman en macOS, Liberation en Linux).
const FUENTE = 'Times-Roman';
const MONO = 'Courier';
const FAMILIA_SERIF = 'Times New Roman, Liberation Serif, Times, serif';
const FAMILIA_MONO = 'Courier New, Liberation Mono, Courier, monospace';

function esc(texto: string): string {
  return texto
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function recortar(texto: string, max = 42): string {
  return texto.length > max ? `${texto.slice(0, max - 1)}…` : texto;
}

function idDot(id: string): string {
  return `"${id.replace(/"/g, '\\"')}"`;
}

function etiquetaNodo(n: Nodo, t: Tinta): string {
  const nombre = n.tipo === 'stitch' ? (n.id.split('.')[1] ?? n.id) : n.id;
  const filas = [`<TR><TD ALIGN="LEFT"><B>${esc(nombre)}</B></TD></TR>`];
  if (n.hablantes.size > 0) {
    filas.push(
      `<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="10" COLOR="${t.sepiaOscuro}">hablan: ${esc(recortar([...n.hablantes].join(', '), 48))}</FONT></TD></TR>`,
    );
  }
  if (n.escribe.size > 0) {
    filas.push(
      `<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="10" FACE="${MONO}" COLOR="${t.sepia}">~ ${esc(recortar([...n.escribe].join(', '), 48))}</FONT></TD></TR>`,
    );
  }
  if (n.opciones > 0) {
    filas.push(
      `<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="10" COLOR="${t.grafito}">${n.opciones} ${n.opciones === 1 ? 'opción' : 'opciones'}</FONT></TD></TR>`,
    );
  }
  return `<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="1" CELLPADDING="2">${filas.join('')}</TABLE>>`;
}

/** DOT del grafo con el estilo del juego: tinta y sepia sobre papel. */
export function aDot(g: Grafo, titulo: string, t: Tinta): string {
  const problemas = new Set(g.avisos.map((a) => a.nodo));
  const out: string[] = [
    `digraph ${idDot(titulo)} {`,
    `  graph [rankdir=TB, bgcolor="${t.papel}", pad=0.5, nodesep=0.6, ranksep=0.75, splines=spline, fontname="${FUENTE}", fontcolor="${t.tinta}", labelloc=t, fontsize=22, label=<<B>${esc(titulo)}</B><BR/><FONT POINT-SIZE="11" COLOR="${t.sepiaOscuro}">grafo de ramas · ${g.nodos.size} nodos · ${g.aristas.length} aristas · ${g.avisos.length} avisos</FONT>>];`,
    `  node [shape=box, style="rounded,filled", fillcolor="${t.papel}", color="${t.tinta}", penwidth=1.3, fontname="${FUENTE}", fontcolor="${t.tinta}", fontsize=13, margin="0.18,0.08"];`,
    `  edge [color="${t.tinta}", penwidth=1.1, arrowsize=0.7, fontname="${FUENTE}", fontsize=10, fontcolor="${t.sepiaOscuro}"];`,
  ];
  const porKnot = new Map<string, Nodo[]>();
  for (const n of g.nodos.values()) {
    if (n.tipo === 'stitch' && n.knot) {
      const lista = porKnot.get(n.knot) ?? [];
      lista.push(n);
      porKnot.set(n.knot, lista);
    }
  }
  for (const n of g.nodos.values()) {
    if (n.tipo === 'stitch') continue;
    if (n.tipo === 'inicio') {
      out.push(
        `  ${idDot(n.id)} [label="inicio", shape=circle, style=filled, fillcolor="${t.tinta}", fontcolor="${t.papel}", fontsize=10, width=0.6, fixedsize=true];`,
      );
      continue;
    }
    if (n.tipo === 'fin') {
      out.push(
        `  ${idDot(n.id)} [label="${n.id}", shape=doublecircle, style=filled, fillcolor="${t.tintaPlena}", fontcolor="${t.papel}", fontsize=10, width=0.6, fixedsize=true];`,
      );
      continue;
    }
    const stitches = porKnot.get(n.id);
    const borde = problemas.has(n.id)
      ? `, color="${t.sepia}", style="rounded,filled,dashed"`
      : '';
    if (stitches) {
      out.push(`  subgraph ${idDot(`cluster_${n.id}`)} {`);
      out.push(
        `    style="rounded,filled"; fillcolor="${t.papelViejo}"; color="${t.sepia}"; penwidth=1; label=""; margin=14;`,
      );
      out.push(
        `    ${idDot(n.id)} [label=${etiquetaNodo(n, t)}, penwidth=2${borde}];`,
      );
      for (const s of stitches) {
        const b = problemas.has(s.id)
          ? `, color="${t.sepia}", style="rounded,filled,dashed"`
          : '';
        out.push(`    ${idDot(s.id)} [label=${etiquetaNodo(s, t)}${b}];`);
      }
      out.push('  }');
    } else {
      out.push(
        `  ${idDot(n.id)} [label=${etiquetaNodo(n, t)}, penwidth=2${borde}];`,
      );
    }
  }
  for (const a of g.aristas) {
    const attrs: string[] = [];
    if (a.implicita)
      attrs.push(`color="${t.sepia}"`, 'arrowhead=onormal', 'penwidth=0.9');
    if (a.tipo === 'opcion') {
      attrs.push(`color="${t.sepiaOscuro}"`);
      if (a.etiqueta)
        attrs.push(`label=<<I>${esc(recortar(a.etiqueta, 34))}</I>>`);
      if (a.persistente) attrs.push('arrowhead=normalnormal');
    }
    if (a.tipo === 'hilo') attrs.push('style=dotted', 'arrowhead=odiamond');
    if (a.tipo === 'tunel') attrs.push('arrowhead=dot', 'penwidth=1.6');
    if (a.condicional && a.tipo !== 'hilo')
      attrs.push('style=dashed', `color="${t.grafito}"`);
    out.push(
      `  ${idDot(a.desde)} -> ${idDot(a.hacia)}${attrs.length ? ` [${attrs.join(', ')}]` : ''};`,
    );
  }
  out.push(...leyenda(t));
  out.push('  { rank=sink; leyenda; }');
  out.push('}');
  return out.join('\n');
}

function leyenda(t: Tinta): string[] {
  const fila = (estilo: string, texto: string) =>
    `<TR><TD WIDTH="90" ALIGN="LEFT"><FONT COLOR="${t.tinta}">${estilo}</FONT></TD><TD ALIGN="LEFT"><FONT POINT-SIZE="10">${texto}</FONT></TD></TR>`;
  return [
    `  leyenda [shape=plaintext, style="", label=<<TABLE BORDER="1" COLOR="${t.sepia}" CELLBORDER="0" CELLPADDING="3" BGCOLOR="${t.papelViejo}">`,
    `<TR><TD COLSPAN="2" ALIGN="LEFT"><B>Leyenda</B></TD></TR>`,
    fila('——▶', 'divert'),
    fila('——▷', 'entrada implícita al primer stitch'),
    fila('<I>texto</I>', 'opción (con su texto); ▶▶ persistente (+)'),
    fila('- - ▶', 'condicional'),
    fila('···◇', 'hilo (&lt;-)'),
    fila('——●', 'túnel (-&gt; x -&gt;)'),
    fila('▭ - -', 'nodo con aviso (ver consola)'),
    `</TABLE>>];`,
  ];
}

/** Renderiza DOT a SVG con Graphviz (viz.js, WASM). */
export async function renderizarSvg(dot: string): Promise<string> {
  const viz = await instance();
  return viz
    .renderString(dot, { format: 'svg', engine: 'dot' })
    .replace(/font-family="Times[^"]*"/g, `font-family="${FAMILIA_SERIF}"`)
    .replace(/font-family="Courier[^"]*"/g, `font-family="${FAMILIA_MONO}"`);
}

/** SVG a PNG a escala (por defecto @2x) con resvg y las fuentes del sistema. */
export function svgAPng(svg: string, escala = 2): Buffer {
  return new Resvg(svg, {
    fitTo: { mode: 'zoom', value: escala },
    font: { loadSystemFonts: true, defaultFontFamily: 'Times New Roman' },
  })
    .render()
    .asPng();
}

if (import.meta.main) {
  const raiz = resolve(import.meta.dirname, '..');
  const origen = join(raiz, 'content/ink');
  const destino = join(raiz, 'build/ink-grafo');
  const pedidos = process.argv.slice(2).filter((a) => a.endsWith('.ink'));
  const archivos =
    pedidos.length > 0
      ? pedidos.map((a) => basename(a))
      : readdirSync(origen).filter((f) => f.endsWith('.ink'));
  if (archivos.length === 0) {
    console.log('ink:graph: no hay archivos .ink');
    process.exit(0);
  }
  const paleta = JSON.parse(
    readFileSync(join(raiz, 'art/paleta.json'), 'utf8'),
  );
  const tinta = tintaDePaleta(paleta);
  mkdirSync(destino, { recursive: true });
  for (const archivo of archivos) {
    const ruta = join(origen, archivo);
    const fuente = unirIncludes(readFileSync(ruta, 'utf8'), (r) =>
      readFileSync(join(dirname(ruta), r), 'utf8'),
    );
    const grafo = analizarInk(fuente);
    const nombre = basename(archivo, '.ink');
    const dot = aDot(grafo, nombre, tinta);
    const svg = await renderizarSvg(dot);
    writeFileSync(join(destino, `${nombre}.dot`), dot);
    writeFileSync(join(destino, `${nombre}.svg`), svg);
    writeFileSync(join(destino, `${nombre}.png`), svgAPng(svg));
    console.log(
      `✓ ${archivo}: ${grafo.nodos.size} nodos, ${grafo.aristas.length} aristas → build/ink-grafo/${nombre}.{svg,png,dot}`,
    );
    for (const a of grafo.avisos)
      console.warn(`  ⚠ ${a.tipo} · ${a.nodo} · ${a.detalle}`);
  }
}
