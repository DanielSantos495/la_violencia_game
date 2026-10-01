// Compila content/ink/*.ink → public/generated/ink/*.json con el compilador JS de inkjs (MIT).
// Los archivos en subcarpetas se tratan como INCLUDE y no se compilan solos.
import { mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { basename, join, resolve } from 'node:path';
import { PosixFileHandler } from 'inkjs/compiler/FileHandler/PosixFileHandler';
import { Compiler, CompilerOptions } from 'inkjs/full';

const raiz = resolve(import.meta.dirname, '..');
const origen = join(raiz, 'content/ink');
const destino = join(raiz, 'public/generated/ink');

const archivos = readdirSync(origen).filter((f) => f.endsWith('.ink'));
if (archivos.length === 0) {
  console.log('ink:build: no hay archivos .ink');
  process.exit(0);
}

mkdirSync(destino, { recursive: true });
let fallos = 0;

for (const archivo of archivos) {
  const errores: string[] = [];
  const opciones = new CompilerOptions(
    archivo,
    [],
    false,
    (mensaje: string, tipo: number) => {
      // ErrorType: 0 Author, 1 Warning, 2 Error
      if (tipo === 2) errores.push(mensaje);
      else if (tipo === 1) console.warn(`  aviso ${archivo}: ${mensaje}`);
    },
    new PosixFileHandler(`${origen}/`),
  );
  const compilador = new Compiler(
    readFileSync(join(origen, archivo), 'utf8'),
    opciones,
  );
  let json: string | null = null;
  try {
    json = compilador.Compile().ToJson() ?? null;
  } catch (e) {
    errores.push(String(e));
  }
  if (errores.length > 0 || typeof json !== 'string') {
    fallos++;
    console.error(`✗ ${archivo}\n  ${errores.join('\n  ')}`);
    continue;
  }
  writeFileSync(join(destino, `${basename(archivo, '.ink')}.json`), json);
  console.log(`✓ ${archivo}`);
}

process.exit(fallos > 0 ? 1 : 0);
