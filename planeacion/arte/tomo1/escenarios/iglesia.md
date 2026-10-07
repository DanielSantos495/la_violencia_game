# Página de cómic — La misa (Prólogo b3)

> Prólogo b3 (doc 02 §5): misa dominical. El padre Evaristo predica sobre «el peligro rojo» y
> Rosalba y Efraín salen antes. Sin interacción, con peso ambiental. El sermón cierra con «no les
> abran la puerta de noche», que Heliodoro repite esa noche (P29).
> Daniel decidió el 05-oct-2026 hacerla como página de cómic y no como escena: con la escala del
> juego solo se ven 4,5 m de alto y se perdería la altura de la nave. Aprobó el formato de cuatro
> viñetas y, el 06-oct-2026, la página: encuadres, composición y lugar de los globos.
> Dibujo: `game/art/gen/iglesia.py` → `game/art/src/fondos/iglesia/misa-*.svg` (atlas
> `fondos/iglesia`). Página de revisión: `game/art/build/revision/pagina-misa.svg` (no va al atlas).

## 1. Fuentes y [V]/[P]

| Elemento | Fuente | Estado |
|---|---|---|
| Beat, diálogo del padre (P29) | Doc 02 §5, Prólogo b3 | Diseño |
| Padre Evaristo Rincón, párroco de Puente Alto; Efraín Insuasty | Doc 01 | Ficticios, sin hoja de personaje |
| La iglesia por fuera: colonial, de una nave, portada de piedra con arco de medio punto, torre a la derecha, atrio con gradas | `puente-alto.md` §1 (tipología de La Uvita) y `puente_alto.py` (`iglesia`) | [P] (doc 03 §3.1) |
| Por dentro: armadura de par y nudillo con tirantes, muros encalados, piso de barro cocido, ventanas altas, arco toral, retablo, altar, púlpito con tornavoz y escalera, coro alto de madera sobre la puerta, bancas | Tipología colonial, sin una iglesia real de modelo | [P]: confirmar con fotos de iglesias del norte de Boyacá en los años 40 |
| Ruana, pañolón, pantalón de dril | Doc 03 §3.1 (Ocampo López) | [V] |
| Mujeres con la cabeza cubierta y hombres descubiertos en misa | Costumbre de la época | [P] |
| Velas encendidas y flores de papel en el altar | `paleta.json` (`cinta-amarilla` y `cinta-rosa`: flores de papel del altar) | [P] |

Todo lo [P] va con `data-p` en el SVG. Nada se copia de una iglesia real.

## 2. Página

Mide 1920 × 1080, como la pantalla. Lleva un margen de papel de 44 px y canales de 28 px. Las
viñetas aparecen en orden:

| Viñeta | Frame | x, y | Tamaño | Qué cuenta |
|---|---|---|---|---|
| 1 | `misa-1-nave` | 44, 44 | 560 × 992 | La altura de la nave. El púlpito alto en el muro izquierdo, sobre los fieles. Rosalba y Efraín en la última fila, de espaldas |
| 2 | `misa-2-pulpito` | 632, 44 | 1244 × 470 | El padre en el púlpito, de medio cuerpo y con el brazo alzado. A la derecha, el muro con la luz de la ventana de enfrente: es el sitio del globo |
| 3 | `misa-3-salida` | 632, 542 | 608 × 494 | Desde el medio de la nave hacia la puerta mayor, que entra encendida bajo el coro. Rosalba y Efraín salen por el pasillo a contraluz; los fieles siguen de frente, y alguno vuelve la cabeza |
| 4 | `misa-4-atrio` | 1268, 542 | 608 × 494 | Afuera, en el atrio y a pleno sol: la misma portada de la plaza, con la puerta abierta y oscura y las velas del altar al fondo. Los dos se alejan; el último globo sale de la puerta |

Globos propuestos (de muestra en la página de revisión):

- En la viñeta 2, arriba a la derecha: «Recen por los que se fueron detrás de los que no creen. Yo
  también rezo por ellos.»
- En la viñeta 4, con la cola metida en la puerta: «Pero no les abran la puerta de noche.»

Los globos y el marco de las viñetas no son parte de los fondos: los pone la página (`PaginaComic`,
doc 04 §4; los globos van en el DOM).

## 3. Dibujo

- **Viñetas 1 y 3:** perspectiva de un punto con el ojo a 1,55 m. La nave mide 7,6 m de ancho y
  7 m hasta la solera; la armadura llega a 9 m. En la 1 se ven unos 22 m de nave hasta el
  retablo; en la 3, el coro alto a 4,8 m sobre la puerta mayor, que es de medio punto y de 2,4 m,
  como la de la plaza.
- **Viñeta 2:** alzado a 190 px/m. La copa queda cortada abajo y el tornavoz, arriba.
- **Viñeta 4:** alzado a 80 px/m de la portada de `puente_alto.py`.
- **Luz de día:** la nave en penumbra con aguadas planas. Las ventanas altas del muro derecho dejan
  manchas planas de luz en el piso. La puerta es el punto más claro de la viñeta 3.
- **Fieles:** sin rostro (doc 03 §1). De espaldas en la viñeta 1 y de frente en la 3, siempre de los
  hombros arriba sobre el respaldo de la banca.
- **Figuras provisionales:** el padre Evaristo, Rosalba y Efraín van en gris y con borde de tinta
  discontinuo (`data-p="figura provisional"`). Rosalba la pone su área (hoja
  `personajes/rosalba.md`); el padre y Efraín necesitan hoja propia.
- **Color:** paleta del juego con el croma del Prólogo (×1). El rojo y el azul no aparecen.

## 4. Implementación

- `iglesia.py` importa el vocabulario de `puente_alto.py`: `lav`, las aguadas, `recortar`,
  `muro_cal` y la portada.
- `Vista` proyecta los planos de la nave y los recorta al cuadro. Sin ese recorte, lo que queda
  cerca del ojo se proyecta a miles de píxeles y resvg cae (`geom.rs:27`) en cuanto hay un
  `clipPath` detrás.
- `art:build` arma el atlas `fondos/iglesia`: cuatro frames en una página de 2048 px a @1x y de
  4096 px a @2x.
- La página de revisión se compone en el mismo generador y se renderiza aparte, con las fuentes
  del sistema para los globos de muestra.

## 5. Pendientes

- `PaginaComic` (doc 00, Sprint 1): la arma una sesión especialista aparte (`paginas-comic`, creada
  el 06-oct-2026 y a la espera de la orden de Daniel). Fondos le da las viñetas y esta hoja; el
  formato de los datos (frames, posiciones, orden y globos desde Ink) lo propone esa sesión.
- Hojas del padre Evaristo y de Efraín. Cuando existan, se redibujan las viñetas con ellos y con
  Rosalba.
- Verificar con fotos de los años 40 lo [P] de §1, sobre todo el púlpito, el coro, las bancas y el
  retablo.
