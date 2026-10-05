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
  paja, negro de añil en la falda, lana parda en la ruana. Cara y manos claras para que se lean
  primero.
- **Detalle limpio** (doc 03 §1 «Relleno», 04-oct-2026): sin trama de textura. Las sombras son
  aguada plana de tinta en cuatro niveles (0,1 / 0,18 / 0,26 / 0,4) o `piel-sombra` en la cara;
  Rosalba no tiene sombras grandes de primer plano, así que no lleva rayado. Las texturas son
  pocas marcas dibujadas: dos o tres vueltas en el sombrero, dos listas de lana cruda en la ruana,
  zigzag y rombos abiertos en las cintas del ruedo, flecos espaciados. Pliegues, sombras y cintas
  de la falda y listas de la ruana van recortados a su silueta.
- **Variantes por acto** (guion de color, `../paleta.md` §5): el generador hace una variante por
  acto con el croma del mundo de ese acto (×1 / 0,65 / 0,5 / 0,25 / 0,2, en OKLCH, solo los
  lavados del registro `iluminacion`). Tinta, papel y la cinta roja no cambian; la cinta sigue
  roja también en el Epílogo. El Prólogo va en `art/src/personajes/` (mercado, cabezas,
  retrato y cinta suelta); cada acto siguiente, en `art/src/personajes/<acto>/` (un atlas por
  carpeta) solo con lo que usa: el Acto I lleva el mercado (antes del ataque) y el monte; los
  actos II, III y el Epílogo, el monte (llega al Llano con la ruana; puede volver al altiplano)
  y el Llano (§2), gastado en el Acto III y el Epílogo. En el juego: `atlasRosalba(acto)`,
  `rosalbaMercado(acto)`, `rosalbaMonte(acto)`, `rosalbaLlano(acto)` y `retratoRosalba(acto)`
  (`game/src/game/personajes/rosalba.ts`). Si una escena necesita apagar el color en vivo (el
  filtro de §5), la cinta ya es pieza propia y puede quedar fuera del contenedor filtrado.
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
| Peinado | Trenzas con cinta roja al extremo; sin cinta desde la M2 hasta que vuelve a atársela en el Acto II (doc 10 P31–P32) | Ocampo; doc 02 | Con cinta: Prólogo, Acto II tras atarla, epílogo. Sin cinta: M2 en adelante |
| Alpargatas | Blancas, suela de fique trenzado, capellada labrada, galones negros de lana anudados en rosa | Doc 03 [V]; Ocampo | Todas |

Variantes: **mercado** (prólogo y Acto I antes del ataque), **monte** (Misión 2 en adelante:
noche del ataque, huida, monte; también la llegada al Llano en la M4) y **Llano** (abajo).

### Variante Llano (Acto II en adelante)

Doc 02 M4: Rosalba llega al Llano con desplazados boyacenses y entra a la columna del Gaván; choque
de clima y de costumbres. El traje cuenta el paso de la campesina boyacense a combatiente llanera:
deja la frisa, la enagua, las cintas y la ruana (tierra caliente), se pone ropa de trabajo llanera
y conserva lo suyo: la trenza, la cinta roja (que vuelve a atarse en el Acto II) y los zarcillos.

Fuentes:
- Doc 03 §3.3 **[V]**: pantalón y camisa blanca o caqui, cotizas, sombrero de ala ancha (pelo e'
  guama o fieltro; cogollo para faena), faja ancha de cuero con cuchillo o revólver.
- M. A. Hoyos Vega, *El Llano: condición social y plan de estatutos especiales* (tesis, 1943),
  citado por Ó. A. Pabón M., «La vestimenta llanera en el comienzo de la década del cuarenta de mil
  novecientos» (oscarpabon.com, 2024): en el campo, ropa de dril de tonos oscuros; alpargatas de
  cuero con tejidos de hilo de colores; faja ancha de cuero. Fuente secundaria.
- O. Villanueva Martínez, *Guadalupe Salcedo y la insurrección llanera, 1949-1957* (Universidad
  Nacional, 2012): había mujeres en los comandos (pp. 247, 282) y un Comité Femenino
  Revolucionario en Maní (p. 211); dotación de «un sombrero de paja, unas quimbas» (p. 400).
  Leído en notas de lectura publicadas: confirmar en el libro.
- Testimonios de excombatientes («Entrevista con la historia: los guerrilleros de la revolución
  llanera», Pacifista): la guerra echó a los artesanos y escaseaban las cotizas; al entregar las
  armas en 1953 les dieron «un pantalón, una camisa».

**[P]:** no encontramos foto ni descripción de cómo vestían las mujeres combatientes del Llano.
Cada prenda es llanera y verificada; **la combinación es decisión de diseño**, no dato. Los
pañuelos de la guerrilla siguen [P] (`../paleta.md` §12): no se dibujan.

| Elemento | Diseño | Fuente |
|---|---|---|
| Camisa | Caqui, de hombre (le queda ancha y se abolsa sobre la pretina), cuello abierto en V, tapeta con botones, bolsillo de pecho con tapa, mangas remangadas sobre el codo | Doc 03 §3.3 [V] (camisa caqui); de hombre y remangada: decisión |
| Falda | De dril oscuro (`pano-oscuro`), a media canilla, sin cintas ni enagua; dobladillo cosido a mano | Hoyos Vega (dril oscuro en el campo); largo y corte: decisión |
| Faja | Ancha, de cuero, con pespunte, hebilla de hierro y la punta colgando; cuchillo de cacha de madera en vaina de cuero crudo sobre la cadera derecha | Doc 03 §3.3 [V]; Hoyos Vega |
| Cotizas | Suela de cuero crudo de dos capas, capellada tejida en hilo con una lista de color, talonera de cuero; pie descalzo dentro | Doc 03 §3.3 [V]; Hoyos Vega |
| Sombrero | De cogollo, ala ancha casi plana, copa baja con hendidura, cinta de cuero delgada; barbuquejo de cordón de cuero | Doc 03 §3.3 [V] (cogollo para faena); barbuquejo: decisión |
| Trenza, cinta, zarcillos | Los de siempre: lo que conserva de Puente Alto | §1; doc 10 P31–P32 |

Colores: `caqui`, `pano-oscuro`, `madera` (cuero de faja, cinta y talonera), `tierra-llanera`
(cuero crudo de suelas y vaina) y `paja`, con el croma de cada acto. La paleta no tiene token de
cuero: si hace falta uno propio, se pide a la sesión de color.

**Acto III y Epílogo, gastado** (doc 02 M7: «para nosotros apenas cambió de ropa»): el mismo traje
con un remiendo de caqui en la falda, otro de lana cruda en la manga derecha, el ruedo
deshilachado y el ala del sombrero rota atrás, con un pedazo colgando. Si se desmoviliza (M7, final
1) va sin la faja: `ocultas: [PIEZA_FAJA]`.

## 3. Piezas (cut-out)

Convención del pipeline y de ids: skill `la-violencia-art` y `game/tools/art-build.ts`.
Mira a la derecha: el lado visible es su lado derecho (`-der` delante, `-izq` detrás).

- **De pie** (`rosalba.svg`, `rosalba-monte.svg`): brazos y antebrazos (el antebrazo cuelga del
  brazo), piernas con alpargata, enagua, falda, torso, cabeza (con zarcillo y sombrero como hijos),
  pañolón o ruana, trenza y cinta.
- **Agachada** (`rosalba-agachada.svg`, variante monte): pose dibujada aparte para el sigilo,
  con cuerpo, ruana, trenza y cinta, brazo y antebrazo apoyados en el suelo, y cabeza con zarcillo.
- **Corriendo** (`rosalba-corriendo.svg`, variante monte; huida de la M2, doc 02 beat 4): con la
  falda de frisa casi al tobillo no se corre, así que la mano derecha la recoge por delante, a la
  altura del muslo, y el ruedo sube hasta la rodilla: se ven la enagua y las canillas. Torso
  inclinado 14° y cuerpo agachado; cabeza derecha (sirven las cabezas por expresión de pie y la
  postura solo la mueve a ella); trenza echada atrás. Las piernas son la canilla entera con su
  alpargata y pivote en la rodilla, oculta siempre bajo la falda o la enagua (guarda:
  `pnpm art:walk <svg> --carrera`). El brazo izquierdo bracea con el puño cerrado.
- **Llano** (`rosalba-llano.svg`, `rosalba-llano-agachada.svg`, `rosalba-llano-corriendo.svg`, en
  `acto2/`, `acto3/` y `epilogo/`): con la falda a media canilla se ven las canillas, así que de
  pie y corriendo cada pierna es la canilla con su cotiza y el pivote en la rodilla, oculta bajo
  la falda (guardas: `pnpm art:walk <svg> --canilla` y `--carrera --bracea-ambos`). Piezas
  nuevas: `manga-izq` y `manga-der` (el rollo de la manga remangada, hijo del brazo, dibujado
  encima del antebrazo para tapar el codo), `faja` (faja y cuchillo; se quita) y `cuello` (la
  garganta en V y la punta del cuello caen por delante del hombro, así que van después del
  brazo derecho). La agachada pone la cabeza en el mismo sitio que la del monte (sirven
  `rosalba-agachada-cabezas`); camisa sobre la espalda curvada, falda en domo sobre las rodillas
  con el ruedo alto adelante para que se vean las cotizas, faja más baja adelante. Corriendo, la
  tela liviana vuela atrás con el ruedo a la altura de la rodilla y los dos brazos bracean.
- **Cinta roja** (doc 10 P31–P32): pieza propia `cinta`, hija de `trenza`, en las cuatro poses, y
  capa `cinta` en el retrato. Sin ella, la trenza termina en un amarre de hilo oscuro. En el
  juego: `Personaje.mostrarPieza('cinta', …)` o la opción `ocultas: [PIEZA_CINTA]`, y
  `Retrato.cinta(…)`. Va sin cinta desde la M2 hasta que vuelve a atársela en el Acto II.
  La cinta suelta del Prólogo b2 (en la mano de Aurelio y luego de Heliodoro) está en
  `cinta-roja.svg`: `cinta-suelta` a la escala del personaje y `cinta-suelta-vineta` a la del
  retrato, con el pivote donde se coge; `rojo-liberal` plano, revés en `rojo-sombra`, borde de tinta.
- **Cabezas por expresión** (`rosalba-cabezas.svg` de pie, `rosalba-agachada-cabezas.svg`
  inclinada): una cabeza completa por expresión y su capa de parpadeo, con el mismo pivote del
  cuello; el juego cambia la cabeza sin mover sombrero, zarcillo ni mechones (los mechones del
  monte son pieza aparte, hija de la cabeza).
- **Retrato en tres cuartos** (`rosalba-retrato.svg`) para viñetas de cómic y diálogos: busto
  girado hacia la derecha, con los dos ojos visibles y la trenza (con su cinta roja) cayendo por
  delante del hombro. Capas con el mismo pivote (pie del busto): base por variante (mercado con
  sombrero, pañolón y collar; monte con ruana y mechones; Llano, en los actos que lo usan, con
  camisa caqui de cuello abierto, dos bolsillos con tapa y sombrero de cogollo; rostro sin
  rasgos), rasgos por
  expresión (ojos, cejas, boca, mejilla) y parpadeo. En el juego: `Retrato`
  (`game/src/game/personajes/Retrato.ts`).
  Construcción (v2): cabeza a 3/4 con guías fijas (cejas, ojos, base de la nariz, boca y mentón
  a alturas constantes en todas las capas); ojo lejano más estrecho y con el lagrimal hacia la
  nariz; puente de la nariz que tapa el lagrimal lejano; luz de arriba a la izquierda (sombra en
  el lado lejano, bajo la nariz, bajo el ala y bajo la mandíbula). Trazo de grosor variable en
  párpados, cejas, labios y contorno. Sombrero proyectado en 3D: copa redonda, ala caída y
  unas vueltas de trencilla (dos en el ala, tres en la copa), con cinta negra y moño al costado
  de atrás; barbuquejo pegado al
  borde de la cara y anudado bajo el mentón. El de cogollo del Llano usa la misma proyección con
  ala más ancha y casi plana, copa más baja y plana con una hendidura de adelante atrás, cinta de
  cuero con nudo y barbuquejo de cuero. Pelo recogido hacia la nuca, de donde sale la
  trenza de tres cabos. Pechera bordada con columna central simétrica, guarda de flores en el
  escote y abalorios en dos vueltas; pañolón con guarda bordada en los bordes delanteros. En el
  monte, la ruana va terciada sobre el hombro derecho y deja ver la manga abullonada.

## 4. Animación

- Caminata procedural: `game/src/core/animacion/caminata.ts` (revisión con `pnpm art:walk`).
  Con la falda casi al tobillo (mercado, monte) los pies se deslizan bajo el ruedo; en el Llano,
  con la falda a media canilla, modo canilla: la rodilla avanza y retrocede con el muslo, el pie
  de apoyo no patina ni se despega (60 % del ciclo apoyado, con doble apoyo), el talón sube atrás
  en el vuelo y el cuerpo sube a mitad de cada apoyo. Ciclo de 0,82 s: unos 0,74 m/s en escena,
  pasos más largos que en Boyacá (`CAMINATA_LLANO`).
- Agacharse y acechar: cambio de pose con un aplastamiento breve y mirada alrededor.
- Carrera procedural (`game/src/core/animacion/carrera.ts`; `Personaje.correrHasta`): cada pie
  apoya el 38 % del ciclo y hay dos fases de vuelo; el pie de apoyo no patina ni se despega del
  suelo (el cuerpo se hunde a mitad del apoyo y la rodilla sube lo mismo); el talón sube atrás
  y la rodilla se alza para que el pie libre el suelo. Ciclo de 0,62 s: unos 2 m/s en escena.
  Revisión con `pnpm art:walk art/src/personajes/acto1/rosalba-corriendo.svg --carrera`.
  En el Llano no hay falda que recoger: `bracea: 'ambos'` (`CARRERA_LLANO`), los dos brazos en
  contrafase; el que va atrás abre el codo y el que va adelante lo cierra.
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

- Ropa de las mujeres combatientes del Llano: buscar fotos o testimonios (fotos de Monterrey de
  1953, Archivo Germán Guzmán Campos; Guzmán, Fals Borda y Umaña, cap. VIII). Hasta entonces la
  variante Llano es combinación de prendas verificadas (§2).
- Beat en que vuelve a atarse la cinta en el Acto II (narrativa) y dónde vive Rosalba en el
  Acto III y el final 1 (Llano o altiplano), para decidir si esos actos necesitan el monte.
- Fotografías de campesinas boyacenses de los años 40 que confirmen el traje.
- Vista de frente de cuerpo entero (hoja completa del doc 03 §6.2).
- Hombros y torso por expresión (hoy la postura mueve cabeza, brazos y trenza; el torso no es
  padre de la cabeza, así que inclinarlo exige rehacer la jerarquía de piezas).
- Escopeta del padre (doc 03 §2): modelo **[P]**; no se dibuja final hasta resolverlo.
