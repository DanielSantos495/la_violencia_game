# Contrato de escala y capas — escenarios del Tomo I

> Decisiones de diseño (no datos históricos) para que fondos y personajes encajen.
> Pantalla base 1920×1080 (doc 04 §8); plano lateral con 2–3 capas de fondo en paralaje
> (doc 03 §1). Implementación: `game/src/core/escena/escala.ts` (las cifras viven en el código;
> este documento explica el porqué). Revisable antes de producir assets en serie.

## 1. Plano de juego

| Medida | Valor | Por qué |
|---|---|---|
| Escala del plano de juego | **200 px por metro** (a @1x) | Una persona de 1,6 m mide ~320 px, ~30 % de la altura: lo bastante grande para leer rostro, manos y vestuario (novela gráfica), con ~9,6 m de mundo visible a lo ancho. Fácil de dibujar: 1 cm = 2 px |
| Línea de suelo | **y = 900** | Deja 180 px abajo para el suelo en primer plano y para los globos de diálogo (DOM) |
| Horizonte | **y = 580** | Altura de los ojos de alguien de pie en el plano de juego (1,6 m × 200 px/m sobre el suelo) |
| Cámara | Sigue al personaje en horizontal; **no se mueve en vertical** | Vista lateral estable, sin mareo |
| Altura visible sobre el suelo | **4,5 m** (900 / 200) | En el plano de juego se ve la fachada con su alero y corredor; la cumbrera de una casa de un nivel queda cortada arriba (se ve entera en la capa media) |

Alternativa considerada: 160 px/m (persona ~256 px, ~12 m de ancho y 5,6 m de alto visibles):
entran los techos y hay más campo para el sigilo, pero se pierde detalle de vestuario. Queda
como opción si la prueba de sigilo o la composición de la plaza lo piden.

## 2. Personajes

- Cada personaje declara una **estatura de diseño** (metros) y su **altura dibujada** (px del
  SVG, de la coronilla a la suela). Su escala en escena es
  `200 × estatura / altura dibujada`, sin importar a qué tamaño se dibujó el SVG.
- El punto de apoyo del personaje (entre los pies) va sobre la línea de suelo (y = 900).
- Ejemplo: Rosalba con 1,55 m de estatura de diseño y 431 px dibujados → escala ≈ 0,72
  (~310 px en pantalla). La estatura la fija la hoja de personaje
  (`personajes/rosalba.md`); este contrato solo da la regla.

## 3. Capas de paralaje

El factor de paralaje es cuánto se mueve la capa respecto a la cámara (1 = plano de juego).
También fija la escala y el suelo de la capa, como en una perspectiva simplificada:

- **px por metro de la capa** = 200 × factor.
- **Suelo de la capa** = horizonte + (900 − horizonte) × factor (los planos lejanos apoyan más
  cerca del horizonte).
- **Ancho de la capa** = 1920 + (ancho del nivel − 1920) × factor.

| Capa | Factor | px/m | Suelo (y) | Contenido |
|---|---|---|---|---|
| cielo | 0 | — | — | Cielo, nubes que derivan y cordillera: a kilómetros el paisaje no se mueve (se compone a ojo, no a escala) |
| lejos | 0,15 | 30 | 628 | Lo que está a decenas de metros: el otro lado de la plaza, casas e iglesia del fondo |
| medio | 0,45 | 90 | 724 | Lo que está a unos 10 m: el mercado, la gente, la pila |
| juego | 1 | 200 | 900 | Fachadas, suelo, objetos con los que se interactúa, personajes |
| frente | 1,3 | 260 | 996 | Primer plano opcional (postes, ramas, matas) que pasa por delante; nunca tapa al personaje en un punto de decisión |

## 4. Producción de fondos

- Los fondos se arman con **módulos** (fachada, puerta, árbol, tramo de suelo), no con una
  imagen gigante: cada módulo es un SVG o una pieza, y la escena los coloca.
- Un módulo mide como máximo **2048 px a @1x** por lado (4096 px a @2x, el tope de página del
  atlas). Los tramos que se repiten (suelo, cielo) se diseñan para empalmar sin costura.
- Un atlas por escenario: `game/art/src/fondos/<escenario>/` (p. ej. `fondos/puente-alto`).
- Color: paleta del juego (`paleta.md`, datos en `game/art/paleta.json`): lavados bajo la tinta y
  la trama. Perspectiva aérea (paleta.md §6.4): el lavado se diluye hacia el papel según los px/m
  de la capa (100 % en juego y frente, ≈75 % en medio, ≈55 % en lejos, 35–60 % en el cielo) y la
  línea pasa de tinta a grafito en lejos y cielo. El rojo y el azul de partido no se diluyen.
  Las capas lejanas llevan además trazo más fino (doc 03 §1: línea fina en fondos).
- **Fondo de cámara** por escenario (`fondo` en la definición, un color de la paleta): papel de
  día; las escenas de noche usan `sepia-oscuro` (paleta.md §3: la noche no es azul).
- **Interiores en corte** (`casa-insuasty.md` §2): una sola capa, la de juego. Cada cuarto es una
  viñeta con el muro del fondo apoyado en y = 900, el envés del tejado arriba y márgenes de papel
  arriba (y < 44) y abajo (y > 924, para los globos). Los muros cortados son el canal de papel
  entre viñetas, con sus puertas.

## 5. Pendientes

- Confirmar 200 px/m con la primera prueba jugable de sigilo (Misión 2).
- Estaturas de diseño de Aurelio y Custodia (hojas de personaje).
