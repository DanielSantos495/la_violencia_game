# Hoja de personaje — Rosalba Insuasty

> Entregable del doc 03 §6.2 (en curso: perfil lateral; faltan vista de frente y otros ángulos).
> Personaje ficticio (doc 01). Arco y voz: doc 02 §3. Reglas de estilo: doc 03 §1.
> Los SVG en `game/art/src/personajes/` son la fuente del dibujo; esta hoja fija las decisiones.

## 1. Concepto

Campesina liberal de 19 años de Puente Alto (norte de Boyacá), hija de pequeños propietarios,
sabe leer gracias a Custodia. El diseño tiene que leerse en silueta a escala de juego y
envejecer con la historia: empieza como muchacha de mercado y termina en el monte.

- **Silueta:** sombrero claro arriba, masa negra de pañolón o ruana en el centro, falda oscura
  ancha y casi al tobillo, alpargatas blancas abajo. Se reconoce incluso pequeña y en paralaje.
- **Valores:** negro pleno en pelo y abrigo; grises solo por trama (falda); blanco de papel en
  blusa, piel y alpargatas, para que cara y manos se lean primero.
- **Único acento de color:** la **cinta roja** al final de la trenza (rojo liberal, doc 03 §1).
  Es un rasgo documentado del traje (abajo) y a la vez la marca partidista discreta del personaje.
  Hex del rojo pendiente de la hoja de estilo **[P]**.
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
| Falda | Negra, de frisa, casi al tobillo, con vuelo y pliegues; cintas de colores en el ruedo → tres bandas de trama distinta (no hay color fuera del rojo/azul) | Doc 03 [V]; Ocampo | Todas |
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

## 4. Animación

- Caminata procedural: `game/src/core/animacion/caminata.ts` (revisión con `pnpm art:walk`).
- Agacharse y acechar: cambio de pose con un aplastamiento breve y mirada alrededor.
- La violencia no se anima: lo que viva Rosalba en la noche de los chulavíes se narra en viñetas
  (doc 02 §1, doc 03 §1).

## 5. Pendientes [P]

- Hex del rojo y de la paleta completa (hoja de estilo, doc 03 §6.1).
- Fotografías de campesinas boyacenses de los años 40 que confirmen el traje.
- Vista de frente y tres cuartos; expresiones (miedo, rabia, duelo).
- Escopeta del padre (doc 03 §2): modelo **[P]**; no se dibuja final hasta resolverlo.
