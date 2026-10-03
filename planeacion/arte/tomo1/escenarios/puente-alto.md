# Escenario — Plaza de Puente Alto (mañana de mercado, 1946)

> Prólogo, beat 1 (doc 02 §5): Custodia fotografía la plaza; tiendas "rojas" y "azules" una
> frente a otra. Puente Alto es ficticio (doc 01): se compone con tipologías del norte de
> Boyacá, sin copiar un pueblo real. Escala y capas: `contrato_escala.md`.
> Dibujo: `game/art/gen/puente_alto.py` → `game/art/src/fondos/puente-alto/*.svg`
> (atlas `fondos/puente-alto`). Se edita el script, no los SVG. Escena: `game/src/core/escenarios/
> puente-alto.ts`. Revisión sin navegador: `pnpm art:escena puente-alto [scrollX…]`.

## 1. Fuentes

| Fuente | Qué aporta | Estado |
|---|---|---|
| Doc 03 §3.1 | Vivienda de un nivel, tapia pisada encalada, teja de barro, alero que forma corredor | [V] |
| Hernán Díaz, *Mercado campesino en Boyacá* (BanRep, Colección Hernán Díaz, hacia 1960, 10 fotos) | Mercado semanal en la plaza mayor "desde tiempos coloniales"; productos sobre costales y tendidos en el suelo; toldos de lona sobre palos con mesa rústica; mulas; canastos; paraguas negros; mujeres con pañolón y sombrero | Costumbre [V]; la foto es ~15 años posterior: detalles de 1946 [P] |
| Hernán Díaz, *Plaza de Villa de Leyva* (BanRep) | Composición: plaza empedrada abierta, casas bajas encaladas, iglesia blanca, cerro grande detrás, encuadre desde un alero | Referencia de composición |
| Iglesia de La Uvita (norte de Boyacá) | Colonial, una nave, fachada con una torre cuadrada, en la parte alta de la plaza | Tipología (Puente Alto no la copia) |
| Arquitectura boyacense (fuentes de divulgación) | Anchos aleros de teja que protegen andenes y muros; empedrado; pila de piedra en la plaza; balcones de madera | Apoyo; confirmar con fotos de los 40 |

Sigue **[P]** (doc 03 §3.1): iglesia, plaza (empedrada o de tierra), portón y tiendas, paisaje,
pila, pañuelos partidistas en 1946, productos concretos del mercado. Los módulos lo marcan con
`data-p`. El rojo y el azul ya están definidos (paleta.md §2.1).

## 2. Composición por capas

El paralaje cuenta la historia: al salir de la tienda roja se ve la azul enfrente, al otro
lado de la plaza.

| Capa | Ancho | Contenido | Estado |
|---|---|---|---|
| cielo (0) | 1920, fijo | `nube-a/b/c` que derivan a 4–9 px/s y vuelven a entrar por la derecha. `cordillera`: sierra lejana en bruma, cerro mayor (cumbre en x≈1170, y≈250) con páramo arriba y franjas de cultivo abajo (trigo, cebada, papa, potrero, barbecho), cercas de piedra, cercos vivos, cañadas con monte, dos caminos de herradura y fincas; dos estribos cercanos. Se ve por encima de los tejados lejanos (y≈250–500) y por las bocas de calle | Hecho |
| lejos (0,15; 30 px/m; suelo 628) | 2784 | `lejos-oeste` (0–1340): casa de corredor, casa de dos pisos con balcón corrido, boca de calle, **tienda azul** (lx 790–1150, tres parroquianos en el corredor) y otra boca de calle. `iglesia` (1340–1760): fachada encalada con portada de piedra, hornacina y óculo; torre a la derecha con campanario y cupulín de teja (≈17,5 m); atrio de piedra con gradas, cruz atrial y dos feligresas. `lejos-este` (1750–2784): casa cural de balcón, boca de calle, casas. `suelo-lejos` en mosaico | Hecho |
| medio (0,45; 90 px/m; suelo 724) | 4512 | Mercado en mx≈960–3770: mula cargada con arriero, toldo de papas, tendido de papas, **pila** (centro mx≈2420, con una mujer que viene por agua y un niño), corrillo de hombres (un pañuelo rojo), tendido de cubios con compradora, toldo de loza, mujeres con paraguas. **Hueco mx≈1300–1600** para que se vea la tienda azul al salir de la roja. En los extremos del nivel asoman una pareja (pañuelo azul) y la mula atada. `suelo-medio` en mosaico | Hecho |
| juego (1; 200 px/m; suelo 900) | 7680 (4 pantallas) | **tienda-roja** en x 200–2100; plaza abierta con costales, ollas y canastos (algunos en espejo); **casa-porton** en 5800–7500; **empedrado** en mosaico (1024 × 180, arriba en y=900) | Hecho |
| frente (1,3; 260 px/m; suelo 996) | 9408 | Siluetas de tinta con luces de papel: canastos y costales con la base bajo el cuadro (nunca suben de y=900), borde de toldo con ristra de cebollas arriba | Hecho |

Lectura por posiciones de cámara (comprobada con `art:escena`): en 0 domina la tienda roja; hacia
1460 Rosalba sale y la tienda azul queda detrás de ella, al otro lado de la plaza; entre 2600 y
3900 la iglesia queda al centro, con la pila delante y la cordillera detrás; en 5760 cierra la casa
del portón.

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
- Figuras de fondo con `persona()` (sin rostro: perfil, sombrero, ruana o pañolón) y `mula()`, a la
  escala de cada capa.

### Color (paleta del Tomo I, `planeacion/arte/tomo1/paleta.md`)

El generador carga `game/art/paleta.json` y dibuja con lavados planos bajo la línea, como una foto
iluminada a mano. Las tramas siguen encima. Al guardar, la línea pasa a la tinta de la capa.

| Material | Token |
|---|---|
| Muros encalados; desconchados y zócalos sin pintar | `cal`; `tapia` |
| Tejados, cupulín, loza, materas | `teja` |
| Puertas y portones; pilares, vigas, canecillos y balaústres al sol | `madera`; `madera` aclarada (cara al sol) |
| Basas, piso del corredor, pila, portada y atrio de la iglesia, piedras del empedrado | `piedra` |
| Suelo de la plaza entre las piedras | `tierra` aclarada (mañana de sol) |
| Costales, canastos, sombreros de paja | `paja` |
| Ruanas | `lana-parda`, `lana-gris`, `lana-cruda`, `pano-oscuro` |
| Faldas y enagua | `negro-anil`, `pano-oscuro`, `lana-parda`; ruedo en `blanco-tela` |
| Pantalón de dril, alpargatas, lona de los toldos | `blanco-tela` |
| Rostros (sin rasgos) y sombra del ala | `piel`, `piel-sombra` |
| Cultivos de la cordillera | `trigo`, `cebada`, `sementera`, `potrero`, `tierra`, `tapia` |
| Páramo, monte, bruma de la sierra lejana | `frailejon`, `monte`, `gris-claro` |
| Agua de la pila | `agua` (gris verdoso: el agua no es azul) |
| Nubes | `nube` con la panza en `niebla` |
| Mulas | `pelaje-castano` (la cargada), `pelaje-bayo` (la atada) |
| Geranios | `cinta-rosa` (rosado: el rojo es del partido) |
| Afiches | `papel-viejo` con la banda del partido |

- **Perspectiva aérea** (paleta.md §6.4): `lav(token, px/m)` mezcla el token con el papel en OKLab
  según la distancia de la capa (100 % en juego y frente, ≈75 % en medio, ≈55 % en lejos; la
  cordillera entre 35 y 60 %). Línea y trama en `tinta` (juego, medio, frente) o `grafito`
  (lejos, cielo); la sierra lejana en `gris-trama`.
- **Partido:** `rojo-liberal` y `azul-conservador` planos y enteros en todas las capas: en el
  zócalo, las puertas, los postigos, el rótulo y el afiche, y en dos pañuelos del mercado. La tienda
  azul, a 30 px/m, grita igual que la roja: lo único que no se diluye con la distancia es la
  división.
- Nada del mundo entra en las zonas reservadas: la loza y la teja quedan separadas del rojo por
  luz, el agua y el cielo no son azules y el tomate se cambió por cubios.
- Módulos de 2048 px como máximo a @1x. La base del viewBox es el suelo de la capa, salvo los
  módulos que se colocan por arriba (cielo, mosaicos de suelo).

## 4. Implementación

- Definición pura: `game/src/core/escenarios/escenario.ts` (tipos y ayudas) y `puente-alto.ts`
  (capas → mosaicos y colocaciones con frame, x, y, ancla `suelo|arriba`, espejo y deriva). Test
  `tests/escenarios.test.ts`: módulos existentes y ≤ 2048 px, todo dentro de su capa, suelos desde
  el suelo de la capa y sin huecos, hilera lejana continua, solo derivan las nubes y el frente no
  tapa al personaje.
- Phaser: `game/src/game/escenarios/Escenario.ts` (un contenedor por capa con el factor del
  contrato; los hijos heredan el factor al dibujarse) y `PruebaEscenario` (la plaza con Rosalba
  en ropa de mercado; fondo de cámara `papel`).
- `pnpm art:escena`: compone las vistas con los PNG recortados y el atlas, sin navegador.
- El atlas recorta cada frame al viewBox (getBBox no descuenta los clipPath de la cordillera).

## 5. Pendientes de decisión (Daniel)

- 200 px/m (recomendado) o 160 px/m: con 200 se corta la cumbrera de las casas de un nivel.
- Confirmar con fotos de los años 40: plaza empedrada o de tierra; árboles en la plaza o no; pila.
- Pañuelos partidistas en el mercado de 1946 (uno rojo y uno azul, marcados [P]).
