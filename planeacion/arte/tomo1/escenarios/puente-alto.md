# Escenario — Plaza de Puente Alto (mañana de mercado, 1946)

> Prólogo, beat 1 (doc 02 §5): Custodia fotografía la plaza; tiendas "rojas" y "azules" una
> frente a otra. Puente Alto es ficticio (doc 01): se compone con tipologías del norte de
> Boyacá, sin copiar un pueblo real. Escala y capas: `contrato_escala.md`.
> Dibujo: `game/art/gen/puente_alto.py` → `game/art/src/fondos/puente-alto/*.svg`
> (atlas `fondos/puente-alto`). Se edita el script, no los SVG.

## 1. Fuentes

| Fuente | Qué aporta | Estado |
|---|---|---|
| Doc 03 §3.1 | Vivienda de un nivel, tapia pisada encalada, teja de barro, alero que forma corredor | [V] |
| Hernán Díaz, *Mercado campesino en Boyacá* (BanRep, Colección Hernán Díaz, hacia 1960, 10 fotos) | Mercado semanal en la plaza mayor "desde tiempos coloniales"; productos sobre costales y tendidos en el suelo; toldos de lona sobre palos con mesa rústica; mulas; canastos; paraguas negros; mujeres con pañolón y sombrero | Costumbre [V]; la foto es ~15 años posterior: detalles de 1946 [P] |
| Hernán Díaz, *Plaza de Villa de Leyva* (BanRep) | Composición: plaza empedrada abierta, casas bajas encaladas, iglesia blanca, cerro grande detrás, encuadre desde un alero | Referencia de composición |
| Iglesia de La Uvita (norte de Boyacá) | Colonial, una nave, fachada con una torre cuadrada, en la parte alta de la plaza | Tipología (Puente Alto no la copia) |
| Arquitectura boyacense (fuentes de divulgación) | Anchos aleros de teja que protegen andenes y muros; empedrado; pila de piedra en la plaza; balcones de madera | Apoyo; confirmar con fotos de los 40 |

Sigue **[P]** (doc 03 §3.1): iglesia, plaza (empedrada o de tierra), portón y tiendas, paisaje;
tonos de rojo y azul (hoja de estilo). Los módulos lo marcan con `data-p`.

## 2. Composición por capas

El paralaje cuenta la historia: al salir de la tienda roja se ve la azul enfrente, al otro
lado de la plaza.

| Capa | Ancho | Contenido | Estado |
|---|---|---|---|
| cielo (0) | 1920, fijo | Nubes con contorno de tinta y trama abajo (frames sueltos que derivan despacio) + cordillera: cerro grande con cultivos en cuadrícula, cercas de piedra, caminos, fincas diminutas; pie hacia y≈660, detrás del lado lejano | Pendiente |
| lejos (0,15; 30 px/m; suelo 628) | 2784 | Otro lado de la plaza: casas bajas con corredor (alguna de dos pisos con balcón), **tienda azul** en lx≈800–1150, **iglesia** de una torre en lx≈1350–1750 (torre a la derecha, ~19 m = 570 px, atrio elevado con gradas). Mosaico de suelo de 628 a ~738 | Pendiente |
| medio (0,45; 90 px/m; suelo 724) | 4512 | Mercado en mx≈900–3700: tendidos en el suelo con vendedoras sentadas, 2–3 toldos de lona con mesa, 2 mulas cargadas, grupos de gente sin rostro (ruana, sombrero, pañolón, paraguas negro), **pila de piedra** en mx≈2445. Mosaico de suelo 724 → ~924 | Pendiente |
| juego (1; 200 px/m; suelo 900) | 7680 (4 pantallas) | **tienda-roja** en x≈200–2100; plaza abierta 2100–5700 con costales, canastos y ollas; **casa-porton** en ~5800–7500; **empedrado** en mosaico (1024 × 180, arriba en y=900) | Módulos hechos |
| frente (1,3; 260 px/m; suelo 996) | 9408 | Escaso y oscuro (repoussoir): canastos y costales cortados abajo, borde de un toldo arriba | Pendiente |

Ajuste al contrato: la cordillera va en **cielo** (a kilómetros prácticamente no se mueve);
en esta escena "lejos" es el otro lado de la plaza.

## 3. Estilo compartido (cohesión)

- Mismo vocabulario en todas las capas, en `puente_alto.py`: `tejado_frente` (lomos de teja con
  cara en sombra, velo de trama: la teja es más oscura que la cal), `alero` (tablazón negra,
  canecillos tallados, viga), `pilar` (madera con veta y grieta, zapata, basa de piedra),
  `muro_cal` (juntas de los cajones del tapial, humedad al pie, grietas, desconchados oscuros),
  `zocalo` (pintura gastada, borde a mano), `puerta_tablas`, `ventana_reja` (balaustres y
  postigos), `letras_pintadas` (rótulos de brocha sin fuentes), `afiche` (sin consignas ni
  nombres reales), `maceta`, `costal`, `canasto`, `olla`.
- Trazo por capa: frente 3,6 · juego 2,6 · medio 1,7 · lejos 1,1 · cielo 1,0. Lo lejano con menos
  contraste y menos trama (perspectiva aérea en tinta).
- Tramas comunes: `t-fina`, `t-media`, `t-cruz`, `t-densa`, `t-horiz`, `t-vert`, `t-puntos`,
  `t-puntos-ralos`, `t-madera`, `t-madera-v`.
- Color solo en lo partidista: rojo en zócalo, hojas de puerta, postigos, rótulo y afiche de la
  tienda roja; azul en la tienda azul. Provisionales: rojo `#c1121f`, azul `#1f3d8a` [P].
- Cal en `#fff` (más clara que el papel hueso del fondo de cámara): los muros brillan.
- Módulos de 2048 px como máximo a @1x. La base del viewBox es el suelo de la capa, salvo los
  módulos que se colocan por arriba (cielo, mosaicos de suelo).

## 4. Implementación pendiente

- Definición pura de la escena en `game/src/core/escenarios/` (capas → mosaicos y colocaciones:
  frame, x, y, ancla `suelo|arriba`, espejo, deriva en px/s para nubes) + test que valide frames,
  anchos de mosaico y límites de cada capa.
- Builder Phaser en `game/src/game/escenarios/Escenario.ts`: una capa por contenedor con
  `setScrollFactor` del contrato, imágenes con origen (0,1) o (0,0), límites de cámara.
- `tools/art-escena.ts` (`pnpm art:escena`): compone la escena a varias posiciones de cámara
  con los PNG de `art/build/png` y los recortes del atlas, para revisar a 1920×1080.
- `PruebaEscenario` pasa del greybox a la plaza, con Rosalba caminando.

## 5. Pendientes de decisión (Daniel)

- 200 px/m (recomendado) o 160 px/m: con 200 se corta la cumbrera de las casas de un nivel.
- Hex de rojo y azul (hoja de estilo).
- Confirmar con fotos de los años 40: plaza empedrada o de tierra; árboles en la plaza o no.
