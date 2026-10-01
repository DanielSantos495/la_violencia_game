---
name: la-violencia-historia
description: >
  Rigor histórico, nomenclatura y reglas éticas del juego "La Violencia" (Tomo I, Colombia
  1946–1958): nombres ficticios vs. reales, prohibición de inventar diálogos a figuras
  reales, marcas [V]/[P], esquema y validación del modo Archivo, y reglas de diseño sobre
  violencia y combate. Úsala SIEMPRE que se toque contenido histórico o narrativo del juego:
  añadir o editar entradas del Archivo (content/archivo), escribir o revisar Ink/diálogos,
  nombrar personajes, partidos o grupos, diseñar misiones, combate, decisiones o
  recompensas, o citar fechas, cifras y fuentes — aunque la petición no lo diga
  (p. ej. "añade una entrada al Archivo", "escribe la escena del mercado", "agrega un
  contador de enemigos"). Tiene prioridad sobre skills genéricas de diálogo o diseño.
---

# La Violencia — historia y Archivo

El juego es documental: lo que diga se va a leer como hecho. Esta skill resume las reglas;
las fuentes viven en `planeacion/` (solo lectura salvo que Daniel pida editar) y se leen
**antes** de actuar:

| Tema | Doc y sección |
|---|---|
| Nombres ficticios ↔ reales, reglas de uso | `planeacion/historia/tomo1/01_biblia_nomenclatura.md` (doc 01) |
| Núcleo, reglas de storytelling, variables, beats, guía de diálogos | `planeacion/historia/tomo1/02_guion_narrativa.md` (doc 02 §1, §4, §5, §6) |
| Combate y esquema del Archivo | `planeacion/tecnico/tomo1/04_documento_tecnico.md` (doc 04 §5, §7) |
| Pendientes [P] y fuentes | `planeacion/produccion/tomo1/00_plan_implementacion.md` (doc 00 §7–8) |

No copies las tablas de esos docs al código o a otros archivos: cítalas por ruta y sección.

## Nombres (doc 01)

- En la ficción, personas históricas, partidos, grupos armados, medios y pactos llevan el
  **nombre alterado** de la biblia. Fechas, lugares, edificios e instituciones genéricas no
  cambian; "el 9 de abril" / "el Bogotazo" se mantienen.
- En el **Archivo** van los nombres reales, con la correspondencia
  `nombre_en_juego` → `nombre_real`.
- Un nombre que no está en la biblia no se inventa en silencio: propónlo y márcalo [P]
  (debe verificarse que no coincida con personas vivas conocidas, doc 01 regla 6).

## Diálogos

- **Prohibido inventar diálogos a figuras reales**, aunque estén renombradas: solo frases
  documentadas (parafraseadas si hay derechos) o sin diálogo (doc 01 regla 4; la tabla
  dice qué se permite a cada una).
- **Las víctimas reales no se ficcionalizan ni se renombran**: solo aparecen en el Archivo
  con su nombre real (doc 01 regla 5).
- Los personajes ficticios hablan según doc 02 §6: usted y "sumercé" en Boyacá, léxico
  llanero en el Llano, sin anacronismos ni ortografía caricaturesca, frases cortas.
- En Ink, el hablante va como tag `# hablante: Nombre` en la línea (lo lee `InkRunner`).
  Los `.ink` están en `game/content/ink/`; `pnpm run ink:build` los compila.

## Marcas [V]/[P]

- [V] = verificado con fuente; [P] = pendiente de fuente.
- **Nada [P] entra a un build público.** En el Archivo eso es
  `estado_verificacion: "pendiente"`, que el modo release excluye.
- Nunca conviertas un [P] en afirmación, ni completes una cifra o fecha "probable". Si una
  fuente no se puede verificar ahora, déjalo [P] y dilo.

## Entradas del Archivo (doc 04 §7)

Esquema y validación en `game/src/core/archivo/esquema.ts`; una entrada por archivo en
`game/content/archivo/<id>.json`.

1. `id`: `arch-<fecha-o-tema>-<slug>` (`arch-prueba-*` solo para pruebas: nunca se publica).
2. `fecha`: `AAAA`, `AAAA-MM` o `AAAA-MM-DD`; usa la precisión que la fuente respalda.
3. `nombre_en_juego` / `nombre_real`: de la biblia, o `null` si no aplica.
4. `fuentes`: título, url y tipo **reales**. No inventes títulos, registros ni URLs. Si no
   tienes la fuente, la entrada va `pendiente` y lo reportas. Prioriza CNMH, Comisión de la
   Verdad, informe ¡Basta Ya!, archivos de prensa y fototecas citadas en el doc 03 §4.
5. `estado_verificacion`: `verificado` solo con al menos una fuente que respalde el texto.
6. `licencia.estado`: `solicitada | concedida | no_aplica`. Material de terceros (fotos,
   audio, película) sin licencia concedida no entra a builds públicos.
7. `desbloqueo`: episodio, misión y condición del guion (doc 02 §5, doc 04 §6).
8. Valida con `pnpm run validate:archivo` y comprueba con `--release` qué quedaría fuera.

Cifras sensibles (muertos del 9 de abril, total de La Violencia) se citan tal como las
reporta la fuente, con rango si lo hay; mientras no haya fuente, [P] (doc 02 §5, doc 00 §8).

## Diseño (doc 02 §1, doc 04 §5)

- Nunca se premia matar. **Sin contador de bajas** en ningún sistema ni UI; las misiones
  se evalúan por supervivencia, civiles protegidos e información registrada.
- Las atrocidades no son jugables: se narran en páginas de cómic.
- Combate solo contra combatientes armados, **máximo 1 por misión** y solo en misiones de
  Rosalba y Aurelio; retirarse siempre es válido; munición escasa y armas de la época.
- Cada bando tiene razones y culpas; ningún secundario es caricatura.
- Desobedecer órdenes injustas tiene consecuencias, nunca premio por cumplirlas (Aurelio).

Si una petición choca con estas reglas (p. ej. "agrega un contador de enemigos"), no la
implementes tal cual: explica el conflicto, cita el doc y propone una alternativa.

## Fuentes de referencia

Centro Nacional de Memoria Histórica (CNMH), informe final de la Comisión de la Verdad,
informe ¡Basta Ya! (CNMH) y la bibliografía del doc 00 §7. Contrasta antes de cerrar
cualquier texto histórico; la revisión del historiador es obligatoria antes de bloquear
una misión (doc 00 §5, "Definición de hecho").
