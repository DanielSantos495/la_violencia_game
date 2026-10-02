# Hoja de personaje — Rosalba Insuasty

> Entregable del doc 03 §6.2 (en curso: perfil lateral; faltan vista de frente y otros ángulos).
> Personaje ficticio (doc 01). Arco y voz: doc 02 §3. Reglas de estilo: doc 03 §1.
> El dibujo se genera con `game/art/gen/rosalba.py` → `game/art/src/personajes/rosalba*.svg`;
> esta hoja fija las decisiones.

## 1. Concepto

Campesina liberal de 19 años de Puente Alto (norte de Boyacá), hija de pequeños propietarios,
sabe leer gracias a Custodia. El diseño tiene que leerse en silueta a escala de juego y
envejecer con la historia: empieza como muchacha de mercado y termina en el monte.

- **Estatura de diseño: 1,52 m.** Referencia: Meisel Roca y Vega Acevedo, "¿Cuánto crecieron
  los colombianos en el siglo XX?", *El Emisor* n.º 58 (Banco de la República, 2004), con
  cédulas de 4,3 millones de mujeres nacidas entre 1910 y 1984: la estatura femenina subió
  7,87 cm (5,2 %) entre las cohortes 1910-1914 y 1980-1984, es decir de ~151 a ~159 cm.
  Interpolando, una mujer nacida hacia 1927 mide en promedio ~153 cm; Boyacá figura entre los
  departamentos de menor estatura y Rosalba es campesina, de ahí 1,52 m (cálculo propio a partir
  de la fuente, no dato directo). En escena: `escalaPersonaje(1,52 m, 433 px)` según el
  contrato de escala (`../escenarios/contrato_escala.md`); las cifras viven en
  `game/src/game/personajes/rosalba.ts` y un test vuelve a medir el SVG.

- **Silueta:** sombrero claro arriba, masa negra de pañolón o ruana en el centro, falda oscura
  ancha y casi al tobillo, alpargatas blancas abajo. Se reconoce incluso pequeña y en paralaje.
- **Valores y color:** tinta plena en pelo, pañolón y siluetas; lavados apagados de la paleta
  (`../paleta.md` v1.0, aprobada el 02-oct-2026; tokens por pieza en su §9): piel, blanco de tela,
  paja, negro de añil en la falda, lana parda en la ruana. Las sombras van en trama sobre el
  lavado (`piel-sombra` bajo el ala y la mandíbula). Cara y manos claras para que se lean primero.
- **Único color entero:** la **cinta roja** al final de la trenza, en `rojo-liberal` (`#ca2d23`,
  doc 03 §1). Es un rasgo documentado del traje (abajo) y a la vez la marca partidista discreta del
  personaje; en la historia pasa de adorno a señal peligrosa (aprobado por Daniel el 02-oct-2026;
  falta registrarlo en el doc 10 desde narrativa). Cintas del ruedo, abalorios, barbuquejo y
  zarcillos llevan lavados de la paleta, fuera de las zonas del rojo y del azul.
- **Rostro:** perfil firme, ceja gruesa por dentro y algo fruncida, ojo almendrado con iris
  oscuro y brillo, nariz recta de punta redonda, mentón decidido, rubor de tres trazos.
  Expresión por ceja, párpado y postura; nada de retrato realista (doc 03 §2).

## 2. Vestuario por variante

Fuentes: doc 03 §3.1 "Vestido mujer" **[V]** y Javier Ocampo López, *El pueblo boyacense y su
folclor*, cap. 4 "El folclor cotidiano boyacense" (Biblioteca Virtual del Banco de la República),
que describe el traje de la campesina boyacense con detalle. El texto es posterior a 1946 y habla
de un traje tradicional de larga duración: confirmar con fotografías de los años 40 **[P]**.

| Elemento | Diseño | Fuente | Variante |
|---|---|---|---|
| Falda | Negra, de frisa, casi al tobillo, con vuelo y pliegues; cintas de colores en el ruedo → tres bandas en `cinta-amarilla`, `cinta-verde` y `cinta-rosa`, con su labor en tinta | Doc 03 [V]; Ocampo | Todas |
| Enagua | Blanca, de encaje, asoma desigual bajo la falda | Ocampo | Todas (en el monte, con barro en el ruedo) |
| Blusa | Blanca, pechera bordada con abalorios, puños adornados, manga abullonada | Doc 03 [V]; Ocampo | Todas |
| Collar | Abalorios (cuentas) | Ocampo | Mercado |
| Pañolón | Negro, de paño, con bordado y flecos largos | Doc 03 [V]; Ocampo | Mercado |
| Ruana | Oscura y relativamente pequeña; terciada sobre el hombro derecho para dejar libre el brazo (decisión de diseño, no dato) | Doc 03 [V]; Ocampo | Monte |
| Sombrero | De caña o tapia pisada (trencilla), cinta negra, barbuquejo atado bajo el mentón | Doc 03 [V]; Ocampo | Mercado |
| Zarcillos | Flor con gota | Ocampo ("zarcillos muy vistosos") | Todas |
| Peinado | Trenzas con cinta roja al extremo | Ocampo | Todas |
| Alpargatas | Blancas, suela de fique trenzado, capellada labrada, galones negros de lana anudados en rosa | Doc 03 [V]; Ocampo | Todas |

Variantes previstas: **mercado** (prólogo y Acto I antes del ataque) y **monte** (Misión 2 en
adelante: noche del ataque, huida, monte). La del Llano (Acto II) queda pendiente de diseño con
doc 03 §3.3.

## 3. Piezas (cut-out)

Convención del pipeline y de ids: skill `la-violencia-art` y `game/tools/art-build.ts`.
Mira a la derecha: el lado visible es su lado derecho (`-der` delante, `-izq` detrás).

- **De pie** (`rosalba.svg`, `rosalba-monte.svg`): brazos y antebrazos (el antebrazo cuelga del
  brazo), piernas con alpargata, enagua, falda, torso, cabeza (con zarcillo y sombrero como hijos),
  pañolón o ruana, trenza.
- **Agachada** (`rosalba-agachada.svg`, variante monte): pose dibujada aparte para el sigilo,
  con cuerpo, ruana, trenza, brazo y antebrazo apoyados en el suelo, y cabeza con zarcillo.
- **Cabezas por expresión** (`rosalba-cabezas.svg` de pie, `rosalba-agachada-cabezas.svg`
  inclinada): una cabeza completa por expresión y su capa de parpadeo, con el mismo pivote del
  cuello; el juego cambia la cabeza sin mover sombrero, zarcillo ni mechones (los mechones del
  monte son pieza aparte, hija de la cabeza).
- **Retrato en tres cuartos** (`rosalba-retrato.svg`) para viñetas de cómic y diálogos: busto
  girado hacia la derecha, con los dos ojos visibles y la trenza (con su cinta roja) cayendo por
  delante del hombro. Capas con el mismo pivote (pie del busto): base por variante (mercado con
  sombrero, pañolón y collar; monte con ruana y mechones; rostro sin rasgos), rasgos por
  expresión (ojos, cejas, boca, mejilla) y parpadeo. En el juego: `Retrato`
  (`game/src/game/personajes/Retrato.ts`).
  Construcción (v2): cabeza a 3/4 con guías fijas (cejas, ojos, base de la nariz, boca y mentón
  a alturas constantes en todas las capas); ojo lejano más estrecho y con el lagrimal hacia la
  nariz; puente de la nariz que tapa el lagrimal lejano; luz de arriba a la izquierda (sombra en
  el lado lejano, bajo la nariz, bajo el ala y bajo la mandíbula). Trazo de grosor variable en
  párpados, cejas, labios y contorno. Sombrero proyectado en 3D: copa redonda, ala caída y
  trencilla cosida en espiral, con cinta negra y moño al costado de atrás; barbuquejo pegado al
  borde de la cara y anudado bajo el mentón. Pelo recogido hacia la nuca, de donde sale la
  trenza de tres cabos. Pechera bordada con columna central simétrica, guarda de flores en el
  escote y abalorios en dos vueltas; pañolón con guarda bordada en los bordes delanteros. En el
  monte, la ruana va terciada sobre el hombro derecho y deja ver la manga abullonada.

## 4. Animación

- Caminata procedural: `game/src/core/animacion/caminata.ts` (revisión con `pnpm art:walk`).
- Agacharse y acechar: cambio de pose con un aplastamiento breve y mirada alrededor.
- Expresiones (`game/src/core/animacion/expresiones.ts`): el dibujo cambia de golpe, como en una
  viñeta; la postura de la cabeza se interpola y se suma a la caminata y al acecho.

| Expresión | Ojos y cejas | Boca y rostro | Postura y parpadeo |
|---|---|---|---|
| Neutral | Mirada tranquila | Rubor de campo | Cabeza recta, brazos sueltos; parpadeo pausado |
| Alerta | Ceja alzada, arruga de preocupación | Igual | Cabeza algo alzada, brazo adelantado, listo; parpadea más |
| Miedo | Ojo muy abierto pero almendrado, blanco sobre el iris, ceja arqueada con la cabeza alzada, un pliegue entre las cejas | Boca entreabierta en óvalo (filo de los dientes de arriba), gota de sudor en la sien, sin rubor | Cabeza atrás, codo pegado al cuerpo y mano al pecho (se aferra al pañolón o a la ruana); parpadeo rápido, a veces doble |
| Rabia | Ceja baja hacia la nariz, entrecejo, párpado recto y pesado | Labios apretados, comisura abajo, aleta de la nariz abierta, rubor intenso | Mentón abajo, brazos tensos hacia adelante; casi no parpadea (mirada fija) |
| Duelo | Párpado pesado, mirada baja, ceja de tristeza, ojeras | Lágrima en tinta (sin color), comisura abajo, mentón tenso | Cabeza caída, brazos colgando sin fuerza; parpadeo lento |

A la escala de juego la cabeza mide pocos píxeles: de lejos la emoción se lee sobre todo por la
postura (cabeza y brazos); el detalle del rostro rinde en planos cercanos y viñetas de cómic.
Agachada, la postura solo mueve la cabeza: la mano de apoyo sigue en el suelo.
- La violencia no se anima: lo que viva Rosalba en la noche de los chulavíes se narra en viñetas
  (doc 02 §1, doc 03 §1).

## 5. Pendientes [P]

- Color por acto (`../paleta.md` §11): sigue abierta la forma de apagarlo. Si se genera cada
  escena con el croma de su acto, Rosalba necesitará variantes por acto; si se usa un filtro en
  vivo, la cinta roja tendrá que salir de la pieza `trenza` a una pieza propia para no apagarse.
- Fotografías de campesinas boyacenses de los años 40 que confirmen el traje.
- Vista de frente de cuerpo entero (hoja completa del doc 03 §6.2).
- Hombros y torso por expresión (hoy la postura mueve cabeza, brazos y trenza; el torso no es
  padre de la cabeza, así que inclinarlo exige rehacer la jerarquía de piezas).
- Escopeta del padre (doc 03 §2): modelo **[P]**; no se dibuja final hasta resolverlo.
