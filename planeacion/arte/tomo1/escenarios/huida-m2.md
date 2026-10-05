# Escenarios — Huida de la Misión 2 (cultivos, quebrada, monte al amanecer)

> M2 b4–b5, abril de 1948, Acto I (doc 02 §5). Rosalba sale por el boquete del solar
> (`casa-insuasty.md` §3) y cruza los cultivos de noche mientras la casa arde a lo lejos. Lleva la
> escopeta del padre o su libreta (P28). Baja a la quebrada y amanece en el monte, donde la
> esperan otros desplazados.
> Dibujo: `game/art/gen/huida.py` (usa el vocabulario de `puente_alto.py` y la noche de
> `casa_insuasty.py`) → `game/art/src/fondos/huida/<tramo>/*.svg`. Escena:
> `game/src/core/escenarios/huida.ts`. Revisión: `pnpm art:escena huida-cultivos|huida-quebrada|huida-monte`.
> Todo va con el croma del Acto I (×0,65, paleta.md §5).

## 1. Fuentes y [V]/[P]

| Elemento | Fuente | Estado |
|---|---|---|
| Altiplano y vertiente andina, cultivos y cercas de piedra | Doc 03 §3.1 | [P] referencias fotográficas regionales |
| Trigo y cebada (franja triguera) | `paleta.md` §4 | [V] |
| Maíz y papa en la vereda en abril de 1948 | — | [P] (`data-p`) |
| Monte de vertiente y helechos de quebrada; especies de árboles | — | [P] (`data-p`) |
| Agua gris verdosa, fuego en ocre y amarillo, niebla del amanecer | `paleta.md` §3 y §4 | Decisión de paleta |
| La casa quemada vista a distancia, sin personas | Doc 02 M2 b4; doc 03 §1 «Violencia» | Guion |

## 2. Tramos

| Tramo | Ancho | Qué hay | Luz |
|---|---|---|---|
| **Cultivos** | 5760 | Del boquete del solar (izquierda) al borde del barranco (derecha), pasando por papa en surcos, un **maizal alto** con un claro (x 1220–2620, donde agacharse en el sigilo), cebada a media altura con una cerca y su portillo, y un papal con un árbol solo. Al fondo, **la casa ardiendo** (capa lejana, lx 290–710): tejado hundido, ventanas encendidas y columna de humo. Se ve al empezar y se va quedando atrás | Noche |
| **Quebrada** | 3840 | Bajada entre helechos, el agua con las piedras para pasar, un tronco caído y la subida al monte. Las paredes de la quebrada (capa media, un solo perfil de copas) encierran la vista; por encima solo asoman el humo y el resplandor de la casa | Noche |
| **Monte al amanecer** | 3840 | Sendero en la bruma entre raíces, piedras y helechos, hasta el **claro de los desplazados** (x 1920–2880): una fogata con atados y una olla. Los personajes los pone la escena. Abajo, el valle en la bruma con un hilo de humo: la casa que ya no está | Alba |

## 3. Luz

- **Noche:** es el estilo de noche de la casa (`usar_noche`, `casa-insuasty.md` §7); cambia a la vez
  cuando Daniel elija. El fuego va encima de la noche, en `llama`, `llama-nucleo` y `brasa`, con un
  charco plano de luz en el suelo.
- **Alba:** cada capa se mezcla con `niebla` según su distancia: 62 % el valle, 42 % el monte medio
  y 10–14 % el plano de juego. Sobre el horizonte hay una franja de `llama` y `llama-nucleo` (el
  amanecer va en ocre, nunca en rojo ni en azul) y encima bancos de niebla planos. El fondo de
  cámara es `niebla`.
- La noche y la niebla se calculan color por color en el generador, sin filtros SVG: resvg se
  caía al recortar un frame con filtro, y el resultado es el mismo porque la mezcla es afín.

## 4. Empalmes

Lo que cruza de un módulo a otro se decide una sola vez para todo el tramo. Así, los dos módulos
del empalme dibujan lo mismo:
- las matas del maizal;
- las copas del borde de la quebrada, que salen de un perfil continuo.

Lo demás termina antes del borde: matorrales, cercas y árboles de la capa media.

## 5. Pendientes

- Confirmar con fotos: cultivos de abril en la vereda (maíz, papa, cebada), cercas, monte y
  especies.
- Cobertura en el sigilo: hoy el maizal está detrás del personaje. Para esconder a Rosalba hay
  que pintarlo delante (o una franja de matas delante) en la escena del juego.
- Fondos para lo que la escena muestre en primer plano de la quema (si la hay) y para el
  encuentro con los desplazados (personajes).
- Estilo de noche definitivo (`casa-insuasty.md` §7).
