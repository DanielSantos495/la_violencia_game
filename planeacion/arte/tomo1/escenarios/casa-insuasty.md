# Escenario — Casa de los Insuasty (noche)

> Prólogo b4: junio de 1946, reunión liberal para oír la radio; la Seccional disuelve la reunión y
> Rosalba esconde la radio o el periódico (P27). Misión 2 b2–b4: abril de 1948, llega la partida,
> esconden a la madre, Efraín sale a hablar y Rosalba huye por el solar (P24–P28) (doc 02 §5).
> Casa ficticia de pequeños propietarios liberales en una vereda de Puente Alto (doc 02 §3). Escala
> y capas: `contrato_escala.md`.
> Dibujo: `game/art/gen/casa_insuasty.py` (usa el vocabulario de `puente_alto.py`) →
> `game/art/src/fondos/casa-insuasty/<lugar>-<acto>/*.svg`. Escena:
> `game/src/core/escenarios/casa-insuasty.ts`. Revisión sin navegador:
> `pnpm art:escena casa-interior|casa-exterior[-acto1] [scrollX…]`. En el navegador:
> `?escena=PruebaEscenario&escenario=casa-exterior`.

## 1. Fuentes y [V]/[P]

| Elemento | Fuente | Estado |
|---|---|---|
| Casa de un nivel, tapia encalada, teja de barro, alero con corredor; habitaciones oscuras encadenadas | Doc 03 §3.1 | [V] |
| Lámpara de petróleo | Doc 03 §2 (objetos del slice); paleta `lampara` | [V], forma genérica |
| Radio de válvulas | Doc 03 §2 | [P] modelo (`data-p`) |
| Escopeta del padre | Doc 03 §2; hoja de Rosalba | [P] modelo: silueta de marcador (`data-p`) |
| Libreta escolar de Rosalba | Doc 02 §3 (sabe leer gracias a Custodia); P28 | Ficción |
| Ropa en la cuerda: pañolón, falda de añil, blusa | Ocampo López (1977), en `paleta.md` | [V] |
| Mesa, bancas, taburete, cama, baúl, repisas | — | [P] (`data-p`) |
| Piso y patio de tierra pisada, encalado por dentro, zócalo de tierra | — | [P] (`data-p` en el piso y el patio) |
| Fogón de leña sobre poyo de barro, zarzo encima, cocina sin chimenea (el humo sale entre las tejas) | — | [P] (`data-p`) |
| Cerca de piedra seca | `paleta.md` («piedra» [P]) | [P] (`data-p`) |
| Árboles de cerca (capulí, aliso) y matas de fique | — | [P] (`data-p`) |
| Puente Alto a lo lejos, con su iglesia | `puente-alto.md` | [P] (`data-p`) |
| Noche sin luna y pueblo sin luz eléctrica | Decisión; [P] luz eléctrica en 1946 | Decisión |

## 2. Interior en corte

Se mira desde el solar, sin el muro de atrás: el muro que se ve es la fachada por dentro, con la
puerta de la casa, la ventana de la sala y la puerta de la cocina. Cada cuarto es una **viñeta**
de la página. Los muros cortados (0,5 m) quedan en papel, como el canal entre viñetas, y por sus
puertas se pasa de un cuarto a otro. Arriba (y < 44) y abajo (y > 924) hay margen de papel; el de
abajo es para los globos. El suelo es la línea y = 900. Encima de la tapia (2,7 m) se ve el envés
del tejado: varas, cañizo y la solera.

| Cuarto | x del nivel | Qué hay (x del nivel) |
|---|---|---|
| Alcoba | 110–910 | Cama 150–590, con el hueco de debajo oscuro (escondite). Ropa en la cuerda, ventanuco cerrado y baúl 640–840 (escondite) |
| Puerta de la alcoba | 900–1020 | Cortina de lienzo recogida |
| Sala | 1010–2210 | Sombreros de los vecinos y una ruana en estacas (1050–1120): hay visita. Puerta de la casa con la tranca puesta (1180–1370). Escopeta del padre sobre la ventana (1480–1710). Ventana con los postigos cerrados (1510–1720) y banca debajo. Mesa (1810–2100) con el radio (1830–1934), la lámpara (2010) y la libreta (2044–2084). Repisa con botellas y taburete |
| Puerta de la cocina | 2200–2320 | Hueco abierto |
| Cocina | 2310–3110 | Leña (2324–2414) y fogón con brasas (2420–2730). Zarzo con mazorcas encima (y ≈ 460) y escalera. Repisa con loza, mazorcas colgadas y un costal. **Puerta al solar** (2920–3100): por ahí se huye en la M2 |

**Luz.** La noche es una aguada de tinta plana por escalones (80, 58 y 32 %) con charcos de luz
alrededor de la lámpara y del fogón. El centro lleva un lavado de `lampara` (la sala) o de `llama`
(la cocina). La media luz de la sala entra por la puerta de la alcoba y el envés del tejado queda
un escalón más oscuro. La llama, el vidrio y las brasas van encima de la noche. No hay degradados
(doc 03 §1).

## 3. Exterior

Visto desde el patio. Como el interior se mira desde atrás, por fuera los cuartos van en orden
contrario.

| Tramo | x del nivel | Qué hay |
|---|---|---|
| Solar | 0–900 | Huerta en surcos, árbol y cerca de piedra con un **boquete** (250–420): la senda hacia los cultivos y la quebrada (M2 b4) |
| Cocina | 900–1900 | Leña bajo el corredor y puerta con el resplandor del fogón por debajo. El humo sale entre las tejas |
| Sala | 1900–3100 | Ventana con reja y los postigos cerrados: la luz de la reunión se cuela por las juntas. Puerta con luz por debajo, por el canto y por la cerradura, con un charco de luz en el corredor. Banca |
| Alcoba | 3100–3800 | Ventanuco a oscuras y esquina de la casa |
| Patio | 3800–4600 | Portillo de varas entreabierto (4270–4490) al camino de Puente Alto: por ahí llegan los vecinos, la Seccional y la partida |

**Capas.**

- **Cielo:** el color lo pone el fondo de cámara, `sepia-oscuro` (paleta.md §3: la noche no es
  azul). Encima van una franja más clara sobre el horizonte, la sierra y Puente Alto en silueta y
  26 estrellas sueltas.
- **Lejos:** lomas de la vereda con dos o tres lámparas de vecinos.
- **Medio:** campos de papa, cercas y árboles. Del lado del camino está **la casa de los vecinos**
  con su lámpara: la que Heliodoro no deja quemar (M2 b3).
- **Frente:** matas de fique con la base bajo el cuadro, que solo asoman por debajo de los pies.

La casa tapa el plano medio y el lejano salvo por los extremos del nivel.

**Noche.** Un filtro de matriz de color mezcla lo dibujado con la tinta (84 % en juego, 86 % en
medio y lejos) y deja transparente lo que no está dibujado. Es una aguada plana, sin degradados. La
luz se dibuja encima: rendijas, charcos y lámparas.

## 4. Actos

`interior-prologo` y `exterior-prologo` van con el croma del Prólogo (×1); `interior-acto1` y
`exterior-acto1`, con el del Acto I (×0,65). Las dos versiones tienen la misma composición. Para la
noche de la M2, `paleta.md` §5 prevé además el filtro en tiempo real (b) en los momentos
dramáticos, que va en la escena del juego.

## 5. Implementación

- `casa_insuasty.py` importa `puente_alto.py`, que ya no genera nada al importarse. Antes de dibujar
  cambia `ESCENA`, `GENERADOR`, `OUTDIR` y el acto (`usar_acto`). `fachada_con_corredor` acepta
  `esquinas`, para que una fachada partida en módulos no lleve esquina en los empalmes.
- `casa-insuasty.ts` define `casaInsuastyInterior(acto)` y `casaInsuastyExterior(acto)`.
  `catalogo.ts` reúne los escenarios por nombre. `DefinicionEscenario.fondo` da el fondo de cámara
  y `DefinicionEscenario.acto` el acto del guion de color, para que entren personajes de ese acto.
- `tests/escenarios.test.ts` revisa:
  - En todo el catálogo: módulos de 2048 px como máximo y dentro de su capa, fondo de la paleta y
    un frente que no tapa al personaje.
  - En la casa: viñetas y muros sin huecos, un plano de juego que cubre el nivel, lo lejano y lo
    medio cubriendo lo que se ve por los extremos, y los mismos módulos en los dos actos.
- `PruebaEscenario` acepta `?escenario=` y usa la Rosalba del acto: en el Prólogo, de mercado y
  con la cinta; en el Acto I, de monte y sin la cinta (P32). De noche la tiñe con un tinte de
  prueba parejo que no toca la cinta, porque es roja de partido.

## 6. Pendientes

- Confirmar con fotos de los años 40: mobiliario, fogón y zarzo, piso de tierra, encalado interior,
  cercas de piedra y árboles. Modelo del radio y de la escopeta (doc 03 §2).
- Luz de los personajes de noche en la escena del juego: por zonas (bajo la lámpara, en penumbra,
  afuera). Hoy solo hay un tinte de prueba.
- Variantes de la M2: la lámpara apagada cuando llega la partida y la puerta abierta.
- La quema de la casa vista a distancia (M2 b4) y los fondos de la huida: cultivos, quebrada y
  monte al amanecer.
- Decidir si las viñetas con canal de papel sirven para todos los interiores (p. ej. la iglesia
  por dentro).
