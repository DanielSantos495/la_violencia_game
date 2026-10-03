---
name: paleta-tematica
description: Método y scripts para crear, ampliar o revisar una paleta de color con contexto (época, lugar, historia, significados que no se pueden tocar), con fuentes, OKLCH, techos de croma, zonas reservadas, guion de color por acto y validación de contraste, daltonismo y grises. Úsala siempre que se elija o cambie un color del juego, se haga una hoja de estilo, la paleta de una región, un acto o la UI, o se pregunte "¿de qué color va esto?", aunque no se diga "paleta".
---

# Paleta temática

Una paleta con contexto es un **sistema de significados**, no un conjunto de colores bonitos. En una obra
histórica algunos colores ya dicen algo antes de que el artista los use: una bandera, un partido, la sangre, el
uniforme de un bando. El trabajo consiste en proteger esos significados y construir el resto del mundo
alrededor, con colores que vengan de fuentes y no del gusto.

En este repo la paleta del juego ya existe. Datos: `game/art/paleta.json`. Reglas y fuentes:
`planeacion/arte/tomo1/paleta.md`. `la-violencia-art` y el doc 03 mandan sobre esta skill. Para dudas de
ciencia del color (espacios, mezcla, nombres) consulta `color-expert`. Para revisar una pantalla ya
renderizada, `critique-color`.

## Flujo

### 1. Inventario de significados (antes de buscar un solo color)

Lista qué colores ya significan algo **en la obra** y **en el mundo que retrata**: partidos, banderas,
uniformes, religión, luto, señales. Pregunta qué está prohibido. Por ejemplo, en este juego la sangre no puede
ser del rojo del partido, el agua y el cielo no pueden ser del azul conservador y el fuego no puede ser rojo.

Cada significado protegido se vuelve una **zona reservada**: un rango de tono más un croma mínimo. Solo los
registros autorizados pueden entrar ahí. Se define por croma y no solo por tono porque un rosa pálido o una
teja comparten tono con el rojo sin leerse como rojo. Lo que convierte un rojo en "el rojo" es la intensidad.

### 2. Investigación con fuentes

Busca el color en el **material**, no en la nostalgia:

- **Ropa y tintes:** qué fibras, qué tintes había, qué dicen los estudios de folclor.
- **Arquitectura y paisaje:** cal, tierra, teja, cultivos de esa época concreta. Ojo: un cultivo pudo
  desaparecer, y las fachadas de colores de muchos pueblos son intervenciones recientes.
- **Oficio de impresión:** cómo se imprimía el color entonces (tintas planas, litografía, fotografía
  iluminada a mano).
- **Arte de la época** que trató el tema: paleta y registro, no estilo para copiar.

Cita la frase exacta y la fuente. Marca cada color **[V]** (fuente), **[P]** (por verificar) o **D**
(decisión de diseño declarada). Un color "de época" sin fuente es una decisión: dilo así.

Las fotos de la época suelen ser en blanco y negro. De ellas se sacan valores y materiales, no tonos. Si
dispones de una imagen en color con licencia, muestrea los píxeles por código (OKLab) en vez de nombrar
colores a ojo. Los modelos de visión fallan con los neutros y los tonos poco prototípicos.

### 3. Registros: cómo existe el color en la obra

Antes de elegir hex, decide los **registros** materiales. Cada uno lleva un techo de croma y, si hace falta,
un rango de tono. Por ejemplo:

- soporte (papel);
- línea y mancha (tinta, grises, sepias);
- lavado (iluminación transparente del mundo);
- tinta plana de imprenta (los colores con significado);
- luz (fuego, lámparas);
- excepciones con regla propia (la sangre que se vuelve tinta).

El registro hace que el significado se lea por la **forma** además del color: plano frente a lavado, borde
limpio frente a mancha. Eso también sirve a quien no distingue tonos.

### 4. Construir en OKLCH

- **L primero.** Organiza la estructura de valores y comprueba que la escena se lee en grises. La
  legibilidad, el daltonismo y la tinta dependen de la luz más que del tono.
- **C con techo por registro.** El mundo, apagado; lo reservado, entero. Las sombras bajan L *y* C: bajar
  solo L produce sombras chillonas.
- **h fuera de las zonas reservadas** para todo lo que no sea su dueño.
- Cada color es un token: `id` estable, nombre, uso, fuente, estado. Los usos (texto, fondo, selección)
  se mapean a tokens con roles, nunca con hex sueltos.

### 5. Guion de color

Decide cómo cambia el color con la historia: por acto, por región o por estado del personaje. Un color
significa lo que la obra le asocia por repetición, y su transición cuenta la historia (ver `color-expert`,
"Colour meaning in a story"). Implementa el guion como un **multiplicador de croma por registro** (y como
variantes con nombre para lo reservado). No crees colores nuevos por acto: así el sistema sigue siendo uno.

### 6. Validar

```bash
python3 .claude/skills/paleta-tematica/scripts/validar_paleta.py game/art/paleta.json --escribir
```

El script comprueba:

- gamut sRGB (reduce croma, nunca luz ni tono);
- techos y tonos por registro;
- zonas reservadas;
- contrastes WCAG declarados;
- pares que deben distinguirse en vista normal, protanopía, deuteranopía, tritanopía y grises (ΔOK);
- el vecino más cercano de cada color reservado.

Con `--escribir` guarda el hex calculado en el JSON. Sale con código 1 si algo falla.

Cuando falla, mueve **L** antes que el tono. Con protanopía el rojo se oscurece hacia un oliva y choca con
los marrones medios; separarlos en luz lo resuelve sin traicionar la fuente. Un aviso que se acepta (por
ejemplo, sangre frente a sepia en protanopía) se documenta con el motivo: la forma lo resuelve.

### 7. Muestrario y prueba en contexto

```bash
python3 .claude/skills/paleta-tematica/scripts/muestrario.py game/art/paleta.json salida.svg --muestra id1,id2,...
```

El muestrario genera el SVG con familias, guion por acto y la prueba de reserva y daltonismo. Renderízalo
(resvg o el navegador) y **míralo**.

Después aplica la paleta a un asset real (un personaje y un trozo de fondo) a escala de juego. Revisa que:

- lo reservado sea lo único que salta;
- la piel no se vea gris;
- los oscuros conserven la línea de tinta;
- los acentos pequeños no se pierdan.

Corrige y vuelve a validar.

### 8. Documentar

Hoja de paleta en el lugar de diseño del proyecto: concepto, registros, zonas, tabla de colores con fuente,
guion, reglas de uso (lo que nunca se pinta de un color reservado), accesibilidad y decisiones abiertas. El
JSON es la fuente para el código; el documento, la fuente de las decisiones. Cambiar un `id` rompe a quien lo
consume: avisa antes.

## Trampas frecuentes

- **Tablas universales de simbolismo** ("el rojo es pasión"). El significado lo fija la obra y su contexto.
- **Luz, cielo, agua o noche** que invaden un color reservado por costumbre (fuego rojo, cielo azul). Busca la
  alternativa material: fuego ocre, cielo de papel, noche sepia.
- **Un hecho de época que choca con una reserva.** Por ejemplo, enaguas rojas o faldas teñidas con añil
  documentadas. No lo borres: llévalo por debajo del umbral de la zona, o úsalo a propósito como significado,
  y documenta la decisión.
- **Medir con el ojo.** Nombra y compara colores con números (OKLCH, ΔOK, contraste), no con la impresión.
- **El color como único indicador** de estado o bando. Acompáñalo de forma, texto o icono.

## Archivos

- `scripts/color.py`: conversiones OKLab/OKLCH, gamut, contraste WCAG, simulación de daltonismo
  (Machado 2009) y ΔOK. Solo biblioteca estándar.
- `scripts/validar_paleta.py`: validador e informe Markdown (`--informe ruta.md`).
- `scripts/muestrario.py`: hoja de muestras SVG.
- `references/esquema-paleta.md`: esquema del JSON con un ejemplo mínimo. Léelo antes de crear una paleta
  nueva.
