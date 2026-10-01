// Valida content/archivo/*.json (una entrada por archivo) contra el esquema del doc 04 §7
// y genera public/generated/archivo/indice.json para el juego.
//   node tools/validate-archivo.ts            modo normal: valida estructura, incluye todo lo válido
//   node tools/validate-archivo.ts --release  excluye pendientes, licencias no concedidas y pruebas
import { mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import {
  type EntradaArchivo,
  motivoExclusionRelease,
  validarEntrada,
} from '../src/core/archivo/esquema.ts';

export interface Informe {
  incluidas: EntradaArchivo[];
  excluidas: { archivo: string; motivo: string }[];
  errores: { archivo: string; errores: string[] }[];
}

export function procesar(
  archivos: { nombre: string; contenido: string }[],
  release: boolean,
): Informe {
  const informe: Informe = { incluidas: [], excluidas: [], errores: [] };
  const ids = new Set<string>();
  for (const { nombre, contenido } of archivos) {
    let datos: unknown;
    try {
      datos = JSON.parse(contenido);
    } catch (e) {
      informe.errores.push({
        archivo: nombre,
        errores: [`JSON inválido: ${String(e)}`],
      });
      continue;
    }
    const r = validarEntrada(datos);
    if (!r.ok) {
      informe.errores.push({ archivo: nombre, errores: r.errores });
      continue;
    }
    if (ids.has(r.entrada.id)) {
      informe.errores.push({
        archivo: nombre,
        errores: [`id duplicado: ${r.entrada.id}`],
      });
      continue;
    }
    ids.add(r.entrada.id);
    const motivo = release ? motivoExclusionRelease(r.entrada) : null;
    if (motivo) informe.excluidas.push({ archivo: nombre, motivo });
    else informe.incluidas.push(r.entrada);
  }
  return informe;
}

if (import.meta.main) {
  const raiz = resolve(import.meta.dirname, '..');
  const origen = join(raiz, 'content/archivo');
  const destino = join(raiz, 'public/generated/archivo');
  const release = process.argv.includes('--release');

  const archivos = readdirSync(origen)
    .filter((f) => f.endsWith('.json'))
    .sort()
    .map((nombre) => ({
      nombre,
      contenido: readFileSync(join(origen, nombre), 'utf8'),
    }));
  const informe = procesar(archivos, release);

  for (const e of informe.errores)
    console.error(`✗ ${e.archivo}\n  ${e.errores.join('\n  ')}`);
  for (const e of informe.excluidas)
    console.log(`– ${e.archivo}: excluida (${e.motivo})`);
  console.log(
    `validate:archivo [${release ? 'release' : 'normal'}]: ${informe.incluidas.length} incluidas, ` +
      `${informe.excluidas.length} excluidas, ${informe.errores.length} con errores`,
  );
  if (informe.errores.length > 0) process.exit(1);

  mkdirSync(destino, { recursive: true });
  writeFileSync(
    join(destino, 'indice.json'),
    JSON.stringify(informe.incluidas),
  );
}
