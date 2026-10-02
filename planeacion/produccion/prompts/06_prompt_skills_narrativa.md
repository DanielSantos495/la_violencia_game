# Prompt — Skills y herramientas de narrativa: Tomo I "La Violencia"

> Pegar en un chat nuevo de **Claude con la carpeta `la_violencia_game` conectada**: un chat del Proyecto "Prueba de Video Juego" o Claude Code en la raíz del repo.
> Objetivo: equipar a Claude para pulir la narrativa, los personajes y el guion del Tomo I. La historia debe volverse más interesante y creativa **sin perder rigor histórico**.

---

## Contexto

Juego narrativo-documental 2D lateral (novela gráfica) sobre La Violencia en Colombia (1946–1958), Tomo I de 8. Tiene tres personajes jugables: Rosalba (civil → insurgente), Aurelio (estatal/paraestatal) y Doña Custodia (documental). Sin voces: solo globos de texto. Guion en Ink.

**Fuente de diseño: carpeta `planeacion/`** (solo se edita con mi aprobación):

| Referencia | Ruta | Para qué |
|---|---|---|
| doc 00 | `planeacion/produccion/tomo1/00_plan_implementacion.md` | Fases, decisiones confirmadas, pendientes [P] |
| doc 01 | `planeacion/historia/tomo1/01_biblia_nomenclatura.md` | Nombres ficticios ↔ reales, reglas de diálogo |
| doc 02 | `planeacion/historia/tomo1/02_guion_narrativa.md` | Núcleo, arcos, sistema de decisiones, beats, diálogos clave, guía de diálogos |
| doc 03 | `planeacion/arte/tomo1/03_direccion_arte.md` | Tono visual, representación de la violencia, audio |
| doc 04 | `planeacion/tecnico/tomo1/04_documento_tecnico.md` | Combate (§5), episodios (§6), Archivo (§7) |
| Contexto | `planeacion/historia/esquema_tomos_conflicto_armado.md` · `planeacion/historia/tomo1/tomo1_la_violencia.md` | Esquema de los 8 tomos y guion base (corregido por el doc 02) |

**Inventario primero.** Lista todos los `.md` de `planeacion/`. Si hay archivos nuevos, renombrados o faltantes respecto a esta tabla, la carpeta manda: avísame antes de seguir.

---

## Reglas no negociables (la creatividad trabaja dentro de ellas)

1. **Ficción en los personajes, nunca en los hechos.** Fechas, lugares, cifras y hechos se mantienen fieles. Lo no verificado se marca **[P]**. Ninguna idea creativa cambia un hecho [V] ni convierte un [P] en hecho.
2. **Figuras reales:** solo dicen frases documentadas o no hablan, aunque estén renombradas (doc 01). Las víctimas reales no se ficcionalizan.
3. **Sin tomar partido.** Cada bando tiene razones y culpas. Ningún secundario es caricatura.
4. **Violencia por su peso, no como espectáculo.** El jugador nunca ejecuta una atrocidad, no hay contador de bajas y nunca se premia matar.
5. **Voz de época.** Usted y "sumercé" en Boyacá, léxico llanero en el Llano. Sin anacronismos ni ortografía caricaturesca (doc 02 §6).
6. **Propuestas, no imposiciones.** Todo cambio al guion llega como propuesta con alternativas. Nada se escribe en `planeacion/` sin mi aprobación explícita.
7. **No adivines.** Repos, comandos, licencias y SHAs se verifican antes de usarlos. Lo no verificable se marca [P] y me preguntas.
8. **Comunicación.** En español, conciso, sin halagos. Separa lo confirmado de lo no verificado.

---

## Bloque 0 — Reconocimiento y plan de instalación (esperar aprobación)

1. Haz el inventario y lee los docs 01 y 02 completos; del 00, 03 y 04 solo las secciones citadas. Hace falta para construir la skill propia con criterio.
2. **Todavía no diagnostiques el guion.** El diagnóstico se hace después de instalar las skills, para que use sus marcos (Bloque 3).
3. Propón el plan de instalación de los Bloques 1 y 2: qué skills, de qué fuente, con qué tag/SHA y licencia. **Espera mi aprobación.**

## Bloque 1 — Skills de terceros

**Dónde instalarlas:** en `.claude/skills/` del repo (nivel proyecto, versionadas en git) y nunca en `~/.claude` sin mi aprobación.

**Si este chat es de claude.ai:** las skills del repo no se cargan solas. Verifica en support.claude.com cómo subir skills personalizadas a la cuenta y prepara un .zip por skill para que yo lo suba.

**Para cada skill:**
- Fíjala a un tag o SHA.
- Verifica la licencia (el juego se venderá, así que descarta las no comerciales).
- Audita el `SKILL.md` y sus scripts: red, escritura fuera del repo, credenciales, ejecución remota.
- Adáptala solo si hace falta, y documenta el cambio.

**Candidatas (verificar todo antes de instalar):**

1. **`jwynia/agent-skills`, solo un subconjunto de la carpeta creative/fiction.**
   - La licencia aparece como MIT en un mirror; confírmala en el repo.
   - **Prioridad alta:**
     - `story-sense`: diagnóstico general.
     - `character-arc`
     - `dialogue`: voces planas.
     - `interactive-fiction`: decisiones significativas, *foldback*/cuellos de botella, gestión de estado.
     - `perspectival-constellation`: historias con varios puntos de vista. Es el núcleo de nuestras 3 perspectivas.
     - `moral-parallax`
     - `key-moments`
     - `scene-sequencing`
     - `endings`
     - `cliche-transcendence`
     - `sensitivity-check`
   - **Opcionales:**
     - `oblique-worldbuilding`: contar el mundo por documentos, útil para Custodia y el Archivo.
     - `character-naming`: contrastar con la biblia; nunca reemplaza un nombre ya aprobado sin mi visto bueno.
     - `story-analysis`
     - `revision`
   - **No instalar:** las de mundos especulativos (conlang, metabolic-cultures, multi-order-evolution, etc.), marketing ni sleep-story.
2. **`spaceninja/narrative-ink-skills`** (MIT según su README): `ink-syntax`, `ink-style` (formateador) e `ink-testing` (inkjs + vitest). Sirven para escribir el guion en `.ink` correctamente.
3. **Alternativas de escritura de ficción:** `howells/fiction` (MIT; tiene comandos de personaje, crítica y continuidad) y `danjdewhurst/story-skills`.
   - Evalúalas contra el punto 1 y recomiéndame **solo una si aporta algo que el punto 1 no cubra** (p. ej. un control de continuidad).
   - No instales las dos.
4. **Skills ya disponibles en Claude:**
   - `brainstorming`: exploración divergente antes de escribir.
   - `skill-creator`: para el Bloque 2.

   No dupliques lo que ya cubren.

## Bloque 2 — Skill propia: `la-violencia-narrativa`

Créala con `skill-creator` en `.claude/skills/la-violencia-narrativa/`. **Apunta a `planeacion/`; no copia sus tablas.** Contenido:

- **Cuándo usarla:** al escribir o revisar escenas, diálogos, beats, decisiones o textos del Archivo del Tomo I.
- **Reglas** (las 5 primeras de este prompt), resumidas, con la ruta y sección del doc que las respalda.
- **Proceso creativo con control:**
  1. Leer el beat y su contexto histórico en el doc 02.
  2. Generar **3 alternativas distintas** (no variaciones de una misma idea), al menos una arriesgada.
  3. Pasar cada alternativa por el filtro de rigor: ¿toca algún hecho? ¿depende de un [P]? ¿pone palabras en boca de una figura real?
  4. Recomendar una y explicar por qué.
- **Herramientas de oficio para el tono del proyecto:**
  - Subtexto antes que explicación.
  - Lo que no se ve: fuera de cuadro, ausencia, antes/después.
  - Objetos que cargan historia: la libreta, el rollo de 12, la escopeta del padre.
  - Ecos entre perspectivas: la misma escena vista por dos personajes.
  - Silencio antes que música.
  - La historia grande entrando por radio, prensa y rumor.
- **Pruebas de una decisión jugable:** opciones distintas, consecuencia perceptible, coste real, expresa al personaje, no premia la violencia.
- **Checklist de voz por personaje:** léxico, ritmo, lo que nunca diría.
- **Checklist de revisión** antes de proponer un texto.

**Prueba de activación al terminar los Bloques 1 y 2:** "pule el diálogo de Efraín en la M2" debe activar `la-violencia-narrativa` + `dialogue`. Si no se activan, corrige las descripciones antes del diagnóstico.

## Bloque 3 — Diagnóstico narrativo con las skills (esperar aprobación)

1. Analiza el guion (doc 02) **aplicando las skills instaladas**: `story-sense` para el diagnóstico general, `character-arc` para los arcos, `perspectival-constellation` para las 3 perspectivas, `interactive-fiction` para el sistema de decisiones, `dialogue` para las voces, `cliche-transcendence` para los clichés y `la-violencia-narrativa` como filtro de rigor. En cada hallazgo indica qué skill lo detectó.
2. Entrégame un **diagnóstico breve** del guion actual con estos puntos:
   - Qué funciona y por qué. Máximo 5 puntos.
   - Debilidades concretas, citando misión y beat: arcos planos, decisiones sin consecuencia visible, secundarios funcionales sin deseo propio, escenas que repiten función, clichés del género bélico o del "drama histórico", diálogos explicativos.
   - Riesgos de rigor: escenas que dependen de un [P] para funcionar.
3. Si el diagnóstico muestra un hueco que ninguna skill cubre, propón cómo cubrirlo (ajuste a la skill propia o una skill adicional verificada).
4. Ajusta al diagnóstico el plan de los Bloques 4 y 5. **Espera mi aprobación.**

## Bloque 4 — Herramientas de trabajo narrativo

Prioriza según el diagnóstico. Primero propón; crea solo con mi aprobación. Los documentos van en `planeacion/historia/tomo1/` y usan el siguiente número libre.

1. **Fichas de personaje** (jugables y secundarios clave) con:
   - deseo, necesidad, miedo, contradicción y secreto;
   - qué cree de los otros bandos;
   - una frase que nunca diría;
   - su relación con los otros dos jugables;
   - cómo cambia en cada acto.
2. **Cronología cruzada:** tabla por fecha con dónde está cada personaje, qué pasa en la historia real ([V]/[P]) y qué sabe cada uno. Sirve para detectar incoherencias y oportunidades de cruce.
3. **Mapa de decisiones:** cada variable del doc 02 §4, dónde se modifica, dónde se lee y qué consecuencia visible produce. Marca las variables que no tienen consecuencia (esa es una debilidad).
4. **Registro de propuestas:** cambios propuestos, su estado (propuesto / aprobado / descartado) y el motivo. Así no se pierden ideas ni se repiten debates.
5. **Herramientas de Ink (verificar antes):**
   - Inky (editor oficial de inkle) para leer y jugar borradores.
   - Compilación con inklecate o el compilador de inkjs.
   - Si existe una herramienta verificada para visualizar el grafo de ramas, recomiéndala; si no, propón un script simple. **No instales sin aprobación.**

## Bloque 5 — Primera pasada de pulido (prueba de las skills)

1. Toma **el Prólogo y la Misión 2** (el vertical slice, doc 00 §4).
2. Usa las skills para proponer:
   - 3 mejoras de arco o de escena;
   - 2 decisiones jugables más significativas;
   - una pasada de diálogo con la voz de cada personaje;
   - 1 idea arriesgada para hacer la historia más memorable, siempre dentro de las reglas.
3. Entrega en formato de propuesta: original → propuesta → motivo → riesgo de rigor. **No edites el doc 02.**

## Bloque 6 — Registro y validación

1. `.claude/SKILLS.md`: añade las skills de narrativa a la tabla existente (o créala) con nombre, fuente, tag/SHA, licencia, fecha, motivo y auditoría.
2. `CLAUDE.md` (Edit, si existe): una sección corta sobre cuándo usar `la-violencia-narrativa` y las de terceros. Las reglas de historia prevalecen sobre cualquier sugerencia creativa de una skill de terceros.
3. Commits por bloque con mensajes claros. **No hagas push**; al terminar, sugiéreme hacerlo.

## Reporte final (breve)

- Skills instaladas, con tag/SHA y licencia.
- Lo descartado y por qué.
- Herramientas pendientes de mi decisión.
- Resumen del diagnóstico (Bloque 3) y de las propuestas del Bloque 5.
- Los [P] que bloquean escenas.
- Riesgos de la auditoría.
