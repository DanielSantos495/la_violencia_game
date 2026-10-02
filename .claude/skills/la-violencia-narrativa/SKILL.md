---
name: la-violencia-narrativa
description: "Escribir o pulir narrativa del Tomo I de La Violencia (Rosalba, Aurelio, Custodia, Puente Alto): escenas, diálogos, beats, decisiones o Archivo. Úsala antes que cualquier skill de ficción."
---

# La Violencia — narrativa con rigor

Juego narrativo-documental 2D (novela gráfica, sin voces, globos de texto, guion en Ink)
sobre La Violencia en Colombia, 1946–1958. Tomo I. Jugables: **Rosalba** (civil → insurgente),
**Aurelio** (estatal/paraestatal) y **Doña Custodia** (documental).

El objetivo es que la historia sea más interesante y memorable **sin mover un solo hecho**.
La creatividad trabaja dentro de las reglas; cuando choquen, ganan las reglas.

## Fuentes (leer antes de proponer; citar por ruta y sección, no copiar tablas)

La carpeta `planeacion/` es la única fuente de verdad (en claude.ai está en los docs del
Proyecto `la_violencia_game/planeacion/…` o en la carpeta enlazada). Si algo aquí contradice
un doc, manda el doc.

| Para | Doc |
|---|---|
| Nombres ficticios ↔ reales, quién puede hablar | doc 01 `historia/tomo1/01_biblia_nomenclatura.md` |
| Núcleo, reglas de storytelling, arcos, variables, beats, guía de diálogos | doc 02 `historia/tomo1/02_guion_narrativa.md` §1–§6 |
| Representación de la violencia, silencio, audio | doc 03 `arte/tomo1/03_direccion_arte.md` §1 "Violencia", §5 |
| Combate, episodios, Archivo | doc 04 `tecnico/tomo1/04_documento_tecnico.md` §5–§7 |
| Pendientes [P], vertical slice | doc 00 `produccion/tomo1/00_plan_implementacion.md` §4, §8 |

**Relación con otras skills.** En Claude Code, `la-violencia-historia` manda en rigor,
nombres y Archivo; esta skill manda en el oficio creativo y el filtro final.

## Paso 0 — Cargar la skill de oficio que corresponde

Esta skill no reemplaza a las de ficción: las orquesta. Antes de proponer, **carga además**
la(s) skill(s) de la tabla que correspondan a la tarea (con la herramienta de skills si está
disponible) y usa su marco de análisis. Sus sugerencias pasan después por el filtro de rigor
de abajo. Si una no está instalada, sigue sin ella y dilo.

| Si la tarea es… | Carga |
|---|---|
| Pulir o escribir diálogos, voces que suenan iguales, diálogo explicativo | `dialogue` |
| Arcos, cambio de un personaje, motivación, secundario sin deseo propio | `character-arc` |
| Decisiones jugables, variables, ramas, consecuencias, cuellos de botella | `interactive-fiction` |
| Cruces entre Rosalba, Aurelio y Custodia; misma escena desde dos jugables | `perspectival-constellation` |
| Complicidad, culpas repartidas, "nadie es inocente" | `moral-parallax` |
| Beats emocionales clave de una misión | `key-moments` |
| Orden de escenas, ritmo, escenas que repiten función | `scene-sequencing` |
| Epílogo y finales | `endings` |
| Algo suena a cliché bélico o de drama histórico | `cliche-transcendence` |
| Representación de grupos, regiones o víctimas | `sensitivity-check` |
| Textos de época dentro de la ficción: notas de Custodia, prensa, radio, Archivo | `oblique-worldbuilding` |
| Diagnóstico general de una misión o del guion | `story-sense` |
| Escribir o revisar archivos `.ink` (solo Claude Code) | `ink-syntax`, `ink-style`, `ink-testing` |

En la entrega, indica qué skill(s) usaste en cada propuesta.

## Reglas (resumen; el detalle está en los docs)

1. **Ficción en los personajes, nunca en los hechos.** Fechas, lugares, cifras y hechos
   fieles. Lo no verificado es **[P]**. Ninguna idea convierte un [P] en hecho ni altera un
   [V]. (doc 02 encabezado y §2; doc 00 §8)
2. **Figuras reales**, aunque estén renombradas: solo frases documentadas o silencio. Las
   víctimas reales no se ficcionalizan: solo en el Archivo, con nombre real. (doc 01 reglas 4–5)
3. **Sin tomar partido.** Cada bando tiene razones y culpas; ningún secundario es caricatura.
   (doc 02 §1 regla 2)
4. **Violencia por su peso, no como espectáculo.** Es jugable pero nunca el objetivo: contra
   civiles solo en momentos guionizados de la misión, con control directo y coste narrativo;
   nunca contra víctimas reales; sin contador de bajas y nunca se premia matar.
   (doc 02 §1 regla 1; doc 03 §1; doc 04 §5)
5. **Voz de época.** Usted y "sumercé" en Boyacá, léxico llanero en el Llano, sin
   anacronismos ni ortografía caricaturesca, frases cortas. (doc 02 §6)

Por qué importa: el jugador va a leer el juego como documento. Un error de hecho dentro de
una escena bien escrita es más dañino que una escena plana, porque convence.

## Proceso creativo con control

Para cada beat, escena, diálogo o decisión:

1. **Contexto.** Lee el beat en doc 02 §5, su fecha/lugar, sus marcas [V]/[P] y las variables
   de §4 que toca. Anota qué hecho histórico lo sostiene.
2. **Tres alternativas distintas**, no variaciones de una idea: cambian el ángulo (qué se
   muestra, desde quién, qué se calla), no solo las palabras. **Al menos una arriesgada**
   (estructura, punto de vista, elipsis, objeto, eco entre perspectivas).
3. **Filtro de rigor** a cada alternativa, respondiendo explícitamente:
   - ¿Toca o desplaza algún hecho [V]?
   - ¿Depende de un [P] para funcionar? (si sí: queda bloqueada hasta tener fuente)
   - ¿Pone palabras en boca de una figura real o ficcionaliza a una víctima real?
   - ¿Premia la violencia, la vuelve espectáculo o la permite fuera de un momento guionizado?
   - ¿Convierte a algún bando o secundario en caricatura?
4. **Recomienda una** y explica por qué (qué gana la historia, qué cuesta).

**Formato de entrega** (cada propuesta):

```
### <Misión · beat>
**Original:** <cita breve del doc 02>
**Alternativas:** A (segura) · B · C (arriesgada) — una línea cada una
**Propuesta recomendada:** <texto o descripción>
**Motivo:** <qué mejora: arco, subtexto, decisión, eco…>
**Riesgo de rigor:** ninguno | depende de [P: …] | otro
**Skill(s) usadas:** <p. ej. dialogue, interactive-fiction>
```

Son **propuestas**: nada se escribe en `planeacion/` sin aprobación explícita de Daniel.

## Herramientas de oficio para este tono

- **Subtexto antes que explicación.** Nadie dice su tema. Si un personaje explica la
  política, sobra la línea.
- **Lo que no se ve.** Fuera de cuadro, ausencia, antes/después, sonido sin imagen
  (Efraín se escucha, no se ve; doc 02 M2 beat 3).
- **Objetos que cargan historia.** La libreta escolar de Rosalba, el rollo de 12 de
  Custodia, la escopeta del padre. Un objeto que cambia de manos vale más que un discurso.
- **Ecos entre perspectivas.** La misma escena o el mismo objeto visto por dos jugables
  (Custodia y Aurelio en Bogotá el 10-abr; la niña de M5 en M6).
- **Silencio antes que música** en los momentos de mayor peso (doc 02 §1 regla 5).
- **La historia grande entra por radio, prensa y rumor**; las figuras reales casi nunca en
  escena (doc 02 §1 regla 3).

## Prueba de una decisión jugable

Una decisión vale si cumple las cinco:

1. **Opciones distintas** — no "sí / sí con otras palabras".
2. **Consecuencia perceptible** — el jugador la ve o la siente después (no solo una variable
   oculta). Indica dónde se lee la variable (doc 02 §4).
3. **Coste real** — toda opción pierde algo.
4. **Expresa al personaje** — dice quién es o en quién se está convirtiendo.
5. **No premia la violencia** — desobedecer o proteger puede costar; matar nunca suma.

## Voz por personaje (base: doc 02 §3 y §6; se amplía con las fichas de personaje)

| Personaje | Léxico | Ritmo | Nunca diría |
|---|---|---|---|
| Rosalba | Boyacense: usted, "sumercé", diminutivos, religiosidad cotidiana; en el Llano incorpora léxico llanero poco a poco | Frases cortas, concretas, de oficio y tierra | Abstracciones ideológicas de manual; jerga moderna |
| Aurelio | Boyacense conservador, católico; vocabulario de obediencia ("orden", "sargento") que se agrieta | Breve, más respuestas que preguntas al inicio; las preguntas crecen con la duda | Que "todos son iguales" antes de que su arco lo gane |
| Custodia | Culta, de maestra y corresponsal; precisa con fechas y nombres | Voz interna de libreta: datos y una frase seca | Una cifra o hecho sin fuente |
| Secundarios | Heliodoro: miedo sincero, no maldad; Morales: frialdad profesional; El Gaván: carisma y dureza; Tránsito: humor llanero | — | Ninguno habla como villano de caricatura |

"Nunca diría" es provisional hasta que existan las fichas de personaje; si una ficha lo
contradice, manda la ficha aprobada.

## Checklist antes de proponer un texto

- [ ] Leí el beat y su contexto en doc 02 y las marcas [V]/[P] que lo afectan.
- [ ] Nombres según doc 01; ninguna figura real con diálogo inventado.
- [ ] Ningún hecho [V] alterado; ningún [P] tratado como hecho.
- [ ] Violencia solo en el contexto de la escena, con coste narrativo; nada que premie matar.
- [ ] Voz de época del personaje (tabla de arriba y doc 02 §6); sin anacronismos.
- [ ] Hay subtexto: la línea hace al menos dos cosas (personaje + tensión, o tensión + mundo).
- [ ] Si hay decisión, pasa las cinco pruebas.
- [ ] Entregado como propuesta (original → propuesta → motivo → riesgo de rigor).
