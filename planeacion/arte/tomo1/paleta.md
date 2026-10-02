# Tomo I — Paleta de color

**Estado:** v1.0, **aprobada por Daniel el 2026-10-02**, incluidos el guion de color y su implementación (§5).
Es la parte de color del entregable 1 del doc 03 §6 (hoja de estilo); grosores y tramas siguen pendientes.
**Datos:** `game/art/paleta.json` es la fuente de los valores para el código y los generadores. Si esta hoja
y el JSON difieren en un hex, manda el JSON.
**Método y validación:** skill `paleta-tematica` (`.claude/skills/paleta-tematica/`).

---

## 1. Idea: la página iluminada

El doc 03 aprobó tinta sobre papel envejecido, grises y sepias, con el rojo liberal y el azul conservador
como únicos acentos. Esta paleta conserva esa regla y la amplía con un recurso de la época: la **fotografía
iluminada a mano**. En los estudios colombianos, el retoque y la iluminación con acuarela o sustancias
naturales «suplía el color que no podían captar las placas» (Serrano, *Historia de la fotografía en
Colombia*).

Así se pinta el mundo del juego: **lavados transparentes y apagados** bajo la línea de tinta. Solo el rojo y
el azul de los partidos aparecen **enteros, planos, como tinta de imprenta**. El color sigue contando la
división, porque lo único que grita en la imagen es lo que divide.

Referencias de tono para el registro, no para copiar estilo:

- **Alejandro Obregón, *Masacre 10 de abril* (1948).** Su época «oscura» de 1948, «donde predominan colores
  pardos, azules, grises oscuros y negro» (Enciclopedia Banrepcultural).
- **Débora Arango, *Masacre del 9 de abril* (1948).** Acuarela expresionista y estridente (MAMM). Es el
  camino que **no** se toma: aquí la violencia pierde color, no lo gana.

**Cambio aprobado y aplicado (doc 03, encabezado y §1 fila «Color», 2026-10-02):** el rojo liberal y el azul
conservador pasan de «únicos colores» a «únicos colores enteros» (tinta plana de imprenta). El mundo lleva
lavados apagados con techo de intensidad.

## 2. Registros: cómo existe el color

Los valores están en OKLCH: L es la luz (0–1), C la intensidad o croma y h el tono en grados.

| Registro | Forma | Techo de croma | Qué va ahí |
|---|---|---|---|
| `papel` | Soporte | 0,045 | Fondo y luces del dibujo |
| `tinta` | Línea, mancha, trama | 0,05 | Línea, negros, grises de trama, sepias, humo |
| `iluminacion` | Lavado plano bajo la tinta | 0,08 × guion (§5) | Todo el mundo: casa, campo, ropa, piel |
| `luz` | Lavado claro | 0,13; tono 55–105° | Fuego y lámparas: ocre y amarillo, nunca rojo |
| `partido` | Tinta plana, opaca, borde limpio de tinta | Sin techo | Pañuelos, banderas, afiches, fachadas, la cinta de Rosalba |
| `sangre` | Mancha orgánica con textura | 0,16; tono 10–40° | Solo el instante; pasa a tinta (doc 03 §1 «Violencia») |

Las tramas siguen siendo tinta y van encima del lavado: el color acompaña a la trama, no la reemplaza. Los
lavados son planos, sin degradados (doc 03 §1).

### 2.1 Rojo y azul (definidos el 2026-10-02)

| Color | Hex | OKLCH | Sombra | Desvaído (afiche viejo, epílogo) |
|---|---|---|---|---|
| **Rojo liberal** | **`#ca2d23`** | 0,55 0,195 29° | `#921b1a` | `#dc8271` |
| **Azul conservador** | **`#1d4aac`** | 0,44 0,165 263° | `#153177` | `#678dc6` |

Cómo se eligieron:

- **Son tintas de imprenta, no colores de pantalla.** El rojo está entre el bermellón y el carmín, y el azul es
  un ultramar. Los dos tienen suficiente intensidad para ser lo único que grita sobre el papel hueso, sin el
  brillo de un rojo o un azul de monitor que se saldría de la página.
- **Tienen el mismo peso en la página y distinta luz.** El azul es más oscuro que el rojo. Así se distinguen
  también en grises y con cualquier tipo de daltonismo: con protanopía el rojo se vuelve un oliva oscuro, pero
  nunca se parece al azul.
- **Se leen sobre el papel:** contraste de 4,3 el rojo y 6,4 el azul (mínimo 3 para objetos).
- **No se confunden con la sangre.** La sangre fresca (`#8e132b`) es más oscura y fría que el rojo liberal, y
  además se distingue por la forma (mancha orgánica frente a tinta plana, doc 03).
- **Las variantes** comparten tono con su color base. `-sombra` es para pliegues. `-desvaído` es el afiche
  gastado por el sol y el pacto del epílogo.

## 3. Zonas reservadas

| Zona | Tono | Croma | Solo pueden entrar |
|---|---|---|---|
| Rojo liberal | 5–45° | ≥ 0,10 | `partido`, `sangre` |
| Azul conservador | 200–295° | ≥ 0,035 | `partido` |

El umbral azul es más bajo porque, sobre papel cálido, el azul se lee como azul con muy poca intensidad.

**Lo que el mundo no puede ser:**

| Elemento | Lo natural | En el juego | Por qué |
|---|---|---|---|
| Fuego, incendios, atardeceres | Rojo anaranjado | Ocre y amarillo (`llama`, `llama-nucleo`, `brasa`) | El fuego no es liberal |
| Cielo, noche | Azul | Papel, `cielo-llano`; la noche en `sepia-oscuro` | El cielo no es conservador |
| Agua | Azul | Gris verdoso (`agua`) | Ídem |
| Teja, ladrillo, barro cocido | Rojo terroso | Apagados y separados del rojo por luz | No deben leerse como afiche, tampoco con daltonismo |
| Mejillas, cintas rosas | Rosa | Por debajo del umbral (`chapas`, `cinta-rosa`) | Rojo sin fuerza: no es el partido |
| Falda teñida con añil **[V]** | Negro azulado | `negro-anil`, por debajo del umbral azul | Hecho de época que cabe sin leerse como azul |
| Enaguas rojas **[V]** (Ocampo: «enaguas blancas y rojas») | Rojo | Se dibujan blancas (**decisión**) | El rojo de la ropa diluiría el del partido |
| Corocoras (garzas rojas del Llano) | Rojo | En tinta o fuera de cuadro | Ídem |
| Uniformes **[P]** | Por verificar | `oliva` o `caqui` provisional | Si resultan azules: gris azulado bajo el umbral o decisión explícita |

## 4. Colores

Fuentes: **[V]** con fuente; **[P]** por verificar (no entra como final); «decisión», de diseño, declarada.
OKLCH = L C h.

### Papel

| Id | Nombre | Hex | OKLCH | Uso | Fuente |
|---|---|---|---|---|---|
| `papel` | Papel hueso | `#eee6d2` | 0.93 0.028 88° | Fondo de pantalla y de toda ilustración; las luces del dibujo son papel | **[V]** doc 03 §1 |
| `papel-viejo` | Papel de archivo | `#e3d4ba` | 0.88 0.038 82° | Archivo, bordes de página, marcos de foto | **[V]** doc 03 §1 (papel envejecido) |
| `papel-sombra` | Pliegue | `#cbbba5` | 0.80 0.036 76° | Sombra plana sobre el papel, pliegues de página | decisión decisión de diseño |

### Tinta

| Id | Nombre | Hex | OKLCH | Uso | Fuente |
|---|---|---|---|---|---|
| `tinta` | Tinta de imprenta | `#1d1713` | 0.21 0.012 60° | Línea de todo el dibujo y texto | **[V]** doc 03 §1 |
| `tinta-plena` | Mancha negra | `#0f0b09` | 0.15 0.008 60° | Masas negras: pelo, pañolón, siluetas, sangre del después | **[V]** doc 03 §1 |
| `grafito` | Tinta aguada | `#544f49` | 0.43 0.012 70° | Línea de capas lejanas del paralaje | **[V]** doc 03 §1 (línea fina en fondos) |
| `gris-trama` | Trama media | `#96918a` | 0.66 0.012 80° | Equivalente plano de la trama media en capas lejanas | **[V]** doc 03 §1 |
| `gris-claro` | Trama clara | `#c1bdb5` | 0.80 0.012 85° | Capa más lejana, bruma | **[V]** doc 03 §1 |
| `sepia-oscuro` | Sepia oscuro | `#4c382b` | 0.36 0.035 55° | Texto secundario, sombras cálidas, noche | **[V]** doc 03 (grises y sepias) |
| `sepia` | Sepia | `#7c634e` | 0.52 0.045 62° | Tono medio cálido, viraje de fotos | **[V]** doc 03 (grises y sepias) |
| `sepia-claro` | Sepia claro | `#ae9b84` | 0.70 0.040 72° | Elementos desactivados de la UI, lejanías al atardecer | **[V]** doc 03 (grises y sepias) |

### Boyacá: casa y tierra

| Id | Nombre | Hex | OKLCH | Uso | Fuente |
|---|---|---|---|---|---|
| `cal` | Cal | `#f2f0e7` | 0.95 0.012 95° | Tapia encalada; más clara y fría que el papel para que se lea como muro | **[V]** doc 03 §3.1 (tapia pisada encalada en blanco) |
| `tapia` | Tapia | `#bba790` | 0.74 0.040 72° | Tapia pisada o adobe sin encalar, muros desconchados | **[V]** doc 03 §3.1 |
| `tierra` | Tierra | `#967a62` | 0.60 0.050 62° | Caminos, patio, plaza | decisión decisión de diseño |
| `barro` | Barro | `#644d3d` | 0.44 0.040 58° | Barro húmedo, ruedo embarrado en el monte | decisión decisión de diseño |
| `teja` | Teja | `#ab795d` | 0.62 0.075 50° | Teja de barro cocido, cerámica de Ráquira | **[V]** doc 03 §3.1 (teja de barro cocido) |
| `madera` | Madera | `#584330` | 0.40 0.042 64° | Portones, vigas, alero, bancas | **[V]** doc 03 §3.1 (cubierta de madera; portón [P]) |
| `piedra` | Piedra | `#969289` | 0.66 0.013 85° | Cercas de piedra, pila de la plaza | **[P]** doc 03 §3.1 (paisaje [P]) |

### Boyacá: campo

| Id | Nombre | Hex | OKLCH | Uso | Fuente |
|---|---|---|---|---|---|
| `trigo` | Trigo | `#dcc58f` | 0.83 0.075 88° | Sembrados de trigo maduro; el color más cálido del Prólogo | **[V]** Álvarez y Chaves (2017), Rev. Cienc. Agríc. 34(2), citando a Valderrama (1976) y a Adams y Mancini (1964): franja triguera de 2.200 a 3.000 m; Boyacá «cerca de un 30%» de la producción nacional |
| `cebada` | Cebada | `#beb491` | 0.77 0.050 95° | Cebada y rastrojo | **[V]** La industria harinera en Duitama-Boyacá 1920-1940 (SciELO): con Bavaria (1936) «se empezó a sustituir el cultivo del trigo» por la cebada |
| `potrero` | Potrero | `#7e906d` | 0.63 0.055 130° | Pasto, potreros | decisión decisión de diseño |
| `sementera` | Sementera | `#5b7054` | 0.52 0.050 138° | Papa y cultivos de hoja | decisión decisión de diseño |
| `monte` | Monte | `#536a57` | 0.50 0.040 150° | Bosque de vertiente, matorral donde se esconde Rosalba | decisión decisión de diseño |
| `frailejon` | Frailejón | `#abb19c` | 0.75 0.030 120° | Páramo: hoja gris plateada | **[V]** Instituto Humboldt (páramos, Espeletia) |
| `niebla` | Niebla | `#deded9` | 0.90 0.008 110° | Páramo, monte al amanecer | **[V]** doc 03 §2 (monte al amanecer) |
| `agua` | Quebrada | `#9aa8a3` | 0.72 0.018 170° | Agua: reflejo gris verdoso; el agua no es azul porque el azul es del partido | decisión decisión de diseño |

### Gente y vestido

| Id | Nombre | Hex | OKLCH | Uso | Fuente |
|---|---|---|---|---|---|
| `piel` | Piel | `#c9ab8c` | 0.76 0.055 68° | Lavado de piel trigueña | decisión decisión de diseño |
| `piel-sombra` | Piel en sombra | `#a78469` | 0.64 0.058 60° | Sombra de piel bajo el ala del sombrero | decisión decisión de diseño |
| `chapas` | Chapas | `#cb9f92` | 0.74 0.055 38° | Mejillas quemadas por el frío; croma bajo para quedar fuera de la zona roja | decisión decisión de diseño |
| `blanco-tela` | Algodón blanco | `#f2eee4` | 0.95 0.014 92° | Blusa, enaguas, alpargatas, globos de diálogo | **[V]** Ocampo López, El pueblo boyacense y su folclor (1977): blusa «generalmente blanca», enaguas blancas, «alpargates blancos» |
| `lana-cruda` | Lana cruda | `#dad0bb` | 0.86 0.030 84° | Ruana de lana sin teñir | **[V]** Ruanas de Nobsa: tonos naturales gris, blanco y negro |
| `lana-gris` | Lana gris | `#78746e` | 0.56 0.010 75° | Ruana gris natural | **[V]** Ruanas de Nobsa: tonos naturales gris, blanco y negro |
| `lana-parda` | Lana parda | `#574336` | 0.40 0.035 55° | Ruana oscura (la de Rosalba en el monte) | **[V]** Ocampo López (1977) citando a Oviedo, s. XVIII: ruanas «en tonos oscuros y relativamente pequeñas» |
| `pano-oscuro` | Paño oscuro | `#2e241f` | 0.27 0.018 48° | Faldas de frisa o paño, pantalón de pañete | **[V]** Ocampo López (1977): faldas «generalmente de tonos oscuros» |
| `negro-anil` | Negro de añil | `#212632` | 0.27 0.024 268° | Falda de frisa teñida con añil: negro frío, por debajo del umbral de la zona azul | **[V]** Ocampo López (1977): faldas tejidas en telares caseros «y las teñían con añil. La falda generalmente es negra» |
| `paja` | Paja | `#cbbd96` | 0.80 0.055 90° | Sombrero de caña, tapia pisada o jipa | **[V]** Ocampo López (1977); doc 03 §3.1 |
| `cinta-amarilla` | Cinta amarilla | `#dbcb8e` | 0.84 0.080 95° | Cintas del ruedo, abalorios, flores de papel del altar | **[V]** Ocampo López (1977): cintas del ruedo «con colores vistosos»; flores amarillo claro en altares |
| `cinta-verde` | Cinta verde | `#7a9e72` | 0.66 0.075 140° | Cintas del ruedo, abalorios | decisión Ocampo López (1977): cintas «con colores vistosos» (tono concreto: decisión) |
| `cinta-rosa` | Cinta rosa | `#e1aeb3` | 0.80 0.060 12° | Cintas, flores del altar; el rosa es rojo sin fuerza: queda fuera de la zona roja | **[V]** Ocampo López (1977): flores «en tonos rosa» en altares |
| `caqui` | Caqui | `#aa9d7f` | 0.70 0.045 88° | Camisa y pantalón llanero | **[V]** doc 03 §3.3 (blanca o caqui) |
| `oliva` | Oliva | `#646648` | 0.50 0.045 112° | Reservado para uniformes cuando se verifiquen | **[P]** doc 03 §3.4 (uniformes [P]) |

### Llano

| Id | Nombre | Hex | OKLCH | Uso | Fuente |
|---|---|---|---|---|---|
| `sabana-seca` | Sabana en verano | `#d4ba8a` | 0.80 0.070 82° | Pajonal seco, diciembre a abril | **[V]** Casanare: verano de diciembre a abril, invierno que inunda la sabana |
| `sabana-verde` | Sabana en invierno | `#738863` | 0.60 0.060 132° | Sabana inundable verde | **[V]** ídem |
| `moriche` | Morichal | `#3b4e37` | 0.40 0.045 140° | Palmas y bosque de galería | **[V]** ídem |
| `tierra-llanera` | Tierra llanera | `#a07e65` | 0.62 0.055 58° | Caminos, caney, corrales | decisión doc 03 §3.3 (caney) |
| `cielo-llano` | Cielo grande | `#f4f0e1` | 0.95 0.020 95° | Cielo del Llano: papel encendido, sin azul | decisión decisión de diseño |

### Bogotá 1948

| Id | Nombre | Hex | OKLCH | Uso | Fuente |
|---|---|---|---|---|---|
| `ladrillo` | Ladrillo | `#a47c65` | 0.62 0.060 52° | Muros de ladrillo | **[P]** fotos de Sady González (blanco y negro): color inferido |
| `piedra-bogota` | Piedra y estuco | `#a29e96` | 0.70 0.012 80° | Edificios republicanos de la Séptima | **[P]** doc 03 §3.2 (inmuebles [V]; acabados [P]) |
| `gabardina` | Gabardina | `#9c917e` | 0.66 0.030 80° | Ropa urbana clara | **[P]** doc 03 §3.2 (ropa urbana [P]) |
| `techo-plata` | Techo plateado | `#c5c4c0` | 0.82 0.006 90° | Techo de los tranvías «Lorencitas» (1936) | **[V]** El tranvía de Bogotá, 1882-1951 (Redalyc): techo plateado; color de la carrocería [P] |
| `humo` | Humo | `#3b3734` | 0.34 0.008 60° | Humo de incendio; ciudad envuelta en humo el 9 de abril | **[V]** fotos de Sady González (Archivo de Bogotá) |
| `humo-claro` | Humo claro | `#7d7a75` | 0.58 0.008 70° | Humo lejano, ceniza | **[V]** ídem |

### Luz

| Id | Nombre | Hex | OKLCH | Uso | Fuente |
|---|---|---|---|---|---|
| `llama-nucleo` | Núcleo de llama | `#f9eda7` | 0.94 0.090 100° | Centro de la llama, lo más claro de la escena | decisión decisión de diseño (fuego sin rojo) |
| `llama` | Llama | `#e8b45e` | 0.80 0.120 78° | Lengua de fuego: ocre encendido | decisión decisión de diseño (fuego sin rojo) |
| `brasa` | Brasa | `#c68a49` | 0.68 0.110 66° | Brasas, borde del fuego, tizones | decisión decisión de diseño (fuego sin rojo) |
| `lampara` | Lámpara de petróleo | `#efdda9` | 0.90 0.070 92° | Luz de lámpara y vela en interiores | **[V]** doc 03 §2 (lámpara de petróleo) |

### Partido

| Id | Nombre | Hex | OKLCH | Uso | Fuente |
|---|---|---|---|---|---|
| `rojo-liberal` | Rojo liberal | `#ca2d23` | 0.55 0.195 29° | Pañuelos, banderas, afiches, fachadas liberales | decisión doc 03 §1; tono exacto: decisión (tinta de imprenta roja) |
| `rojo-sombra` | Rojo en sombra | `#921b1a` | 0.43 0.155 27° | Pliegues del pañuelo y la bandera | decisión derivado de rojo-liberal |
| `rojo-desvaido` | Rojo desvaído | `#dc8271` | 0.70 0.115 32° | Afiche viejo al sol; el pacto del epílogo | decisión derivado de rojo-liberal |
| `azul-conservador` | Azul conservador | `#1d4aac` | 0.44 0.165 263° | Pañuelos, banderas, afiches, fachadas conservadoras | decisión doc 03 §1; tono exacto: decisión (tinta de imprenta azul) |
| `azul-sombra` | Azul en sombra | `#153177` | 0.34 0.125 264° | Pliegues | decisión derivado de azul-conservador |
| `azul-desvaido` | Azul desvaído | `#678dc6` | 0.64 0.095 258° | Afiche viejo al sol; el pacto del epílogo | decisión derivado de azul-conservador |

### Sangre

| Id | Nombre | Hex | OKLCH | Uso | Fuente |
|---|---|---|---|---|---|
| `sangre-fresca` | Sangre fresca | `#8e132b` | 0.42 0.155 18° | Solo el instante; mancha orgánica con textura, nunca plana | **[V]** doc 03 §1 Violencia (la sangre se vuelve tinta) |
| `sangre-oxidada` | Sangre oxidada | `#472218` | 0.30 0.060 35° | Paso intermedio hacia tinta-plena en segundos | **[V]** doc 03 §1 Violencia |

## 5. Guion de color: el color se va

| Momento | Croma del mundo | Qué pasa |
|---|---|---|
| Prólogo (1946) | × 1,0 | Iluminación plena: mercado, trigo, cintas. El rojo y el azul son un color más entre muchos |
| Acto I — El 9 de abril (1948) | × 0,65 | Humo. Solo brillan la luz del fuego y la sangre fresca, además del partido |
| Acto II — El monte y la ley (1949–1953) | × 0,5 | El Llano trae otra tierra (ocre y verde), blanqueada por el sol |
| Acto III — La amnistía rota (1954–1957) | × 0,25 | Casi sepia: solo el rojo y el azul siguen enteros |
| Epílogo — El pacto (1958) | × 0,2 y partido desvaído | Rojo y azul juntos y desvaídos en el afiche del pacto; en el campo el mundo no recupera el color |

La guerra le quita el color al mundo y no a los partidos. En el Acto III los colores de la división son lo
único que queda. En el epílogo se desvaen por primera vez, en el papel del pacto.

En la prueba con escena se vio un efecto que quedó como decisión: la cinta de Rosalba sigue roja mientras los
afiches del pacto se apagan.

**Implementación (decidida el 2026-10-02: (a) como base y (b) solo en momentos puntuales).** Solo baja el
croma del registro `iluminacion`. Luz, tono y los demás
registros se mantienen. Hay dos caminos:

- **(a) Generar cada escena con el croma de su acto.** El generador SVG recibe el factor del acto y escribe
  los colores ya apagados, calculados en OKLCH. Así sale exacto a lo validado, sin costo en tiempo de juego, y
  el rojo y el azul no se tocan porque no son `iluminacion`.
  - **Fondos:** casi todos pertenecen a un solo acto (la plaza del mercado es del Prólogo), así que no hay que
    duplicarlos.
  - **Personajes que cruzan actos** (Rosalba aparece en todos): necesitan una variante por acto. Si van en
    carpetas por acto (`personajes/acto1/…`), el pipeline hace un atlas por carpeta y cada escena carga solo
    el suyo. Crece el peso de la descarga, no la memoria de cada escena.
  - **Límite:** el color no puede cambiar *dentro* de una escena.
- **(b) Filtro en tiempo real.** Phaser 4 tiene un filtro de matriz de color con `saturate()` que se aplica a
  la cámara o a un objeto o contenedor (`enableFilters()`, solo WebGL; skill `filters-and-postfx`).
  - **Ventaja:** permite que el color se escurra en vivo, en el momento dramático.
  - **Costo:** apaga *todo* lo que pasa por él, incluidos el rojo y el azul que estén dentro. La cinta de
    Rosalba vive dentro de la pieza `trenza`, dentro de su contenedor, y se apagaría con ella. Además satura en
    RGB, no en OKLCH, así que los colores se alejan un poco de los validados, y cada objeto filtrado suma
    dibujado.

**Decisión:** (a) como base y (b) solo para momentos dramáticos puntuales, como la noche de la Misión 2. En esas
escenas, los objetos partidistas que deban seguir rojos o azules se dibujan como objetos aparte, fuera del
contenedor filtrado.

Qué implica para cada área:

- Los generadores de SVG aceptan el acto, toman `croma_mundo` de `guion` en `paleta.json` y escalan el croma de
  los colores `iluminacion` en OKLCH (como hace `muestrario.py`).
- Los personajes que cruzan actos se exportan por acto a `art/src/personajes/<acto>/`.
- Los factores aprobados son los de la tabla de arriba, sin cambios. El efecto del epílogo se queda: los
  afiches del pacto se desvaen y la cinta de Rosalba sigue roja, porque es la gente la que carga el color.

## 6. Reglas de uso

1. **Rojo y azul:** planos, opacos, con borde limpio de tinta, solo en objetos que cuentan la división. En la
   UI solo para datos de partido (Archivo).
2. **Lavados:** planos, bajo la línea; tramas encima. Sin degradados.
3. **Sombras:** bajar luz *y* croma (variantes `-sombra` o trama). Nunca oscurecer manteniendo el croma.
4. **Paralaje:** cuanto más lejos, más papel y menos croma (`gris-claro`, `gris-trama`; línea en `grafito`).
5. **Sangre:** `sangre-fresca` → `sangre-oxidada` → `tinta-plena`, en segundos (doc 03 §1).
6. **Modo registro (Custodia):** foto en blanco y negro virada a sepia, sin lavados y sin rojo ni azul. La
   cámara registra el hecho, no el partido (aprobado el 2026-10-02; doc 03 §1).
7. **Lo [P]** usa su token provisional y no se da por final.

## 7. UI

| Rol | Token | Hex |
|---|---|---|
| Fondo | `papel` | `#eee6d2` |
| Texto | `tinta` | `#1d1713` |
| Texto secundario, fechas, fuentes | `sepia-oscuro` | `#4c382b` |
| Globo de diálogo | `blanco-tela` | `#f2eee4` |
| Selección (fondo) | `cinta-amarilla` | `#dbcb8e` |
| Foco | `tinta-plena` (marco grueso) | `#0f0b09` |
| Desactivado | `sepia-claro` | `#ae9b84` |
| Archivo | `papel-viejo` y `sepia-oscuro` | `#e3d4ba` / `#4c382b` |

Contraste WCAG 2.x:

| Texto | Fondo | Razón | Mínimo |
|---|---|---|---|
| Tinta | Papel | 14,3 | 7 |
| Tinta | Globo | 15,3 | 7 |
| Tinta | Papel de archivo | 12,2 | 7 |
| Texto secundario | Papel | 8,9 | 4,5 |
| Tinta | Selección | 10,9 | 4,5 |
| Papel | Tinta plena (texto invertido) | 15,8 | 7 |
| Rojo liberal / azul conservador | Papel (objeto, no texto) | 4,3 / 6,4 | 3 |

El estado nunca se marca solo con color: forma, icono o texto lo acompañan (skill `critique-color`).

## 8. Accesibilidad

```bash
python3 .claude/skills/paleta-tematica/scripts/validar_paleta.py game/art/paleta.json
```

Resultado: **0 fallos**. El rojo y el azul se distinguen en las cinco vistas: normal, protanopía,
deuteranopía, tritanopía y grises. La menor distancia es 0,106 en grises.

Los pares del mundo que se tocan con el rojo están separados por luz además de por tono:

- teja: separada por luz;
- ladrillo: separado por luz;
- madera: separada por luz;
- brasa: separada por luz.

Con protanopía el rojo se oscurece hacia un oliva y por eso esa separación importa. Hay seis avisos
aceptados: sombras, desvaídos y sangre quedan cerca de sepias o pardos con protanopía o deuteranopía. Los
resuelve la forma (plano frente a mancha, doc 03) y el contexto del objeto.

## 9. Primera aplicación: Rosalba

Rosalba ya usa la paleta. El generador `game/art/gen/rosalba.py` carga `paleta.json`, y al guardar la tinta
y el papel pasan a los tokens.

| Pieza | Token |
|---|---|
| Piel | `piel` |
| Chapas (solo en neutral, alerta y rabia: en miedo y duelo, palidez) | `chapas` |
| Blusa, enagua, capellada | `blanco-tela` |
| Sombrero y suela de fique | `paja` |
| Falda | `negro-anil` |
| Cintas del ruedo y abalorios | `cinta-amarilla`, `cinta-verde`, `cinta-rosa` |
| Barbuquejo (las muchachas lo llevaban «de cinta de color», Ocampo) | `cinta-verde` |
| Zarcillos | `cinta-amarilla` |
| Ruana | `lana-parda` |
| Barro | `barro` |
| Cinta de la trenza | `rojo-liberal` |

Detalle en la hoja de personaje (`personajes/rosalba.md`).

## 10. Fuentes

- Javier Ocampo López, *El pueblo boyacense y su folclor* (1977), Biblioteca Virtual del Banco de la
  República: faldas «generalmente de tonos oscuros», teñidas con añil; cintas del ruedo «con colores
  vistosos»; blusa blanca; enaguas blancas y rojas; pañolón negro; ruanas «en tonos oscuros»; trenzas con
  «cintas rojas generalmente, o de otros colores»; barbuquejo de color en las muchachas; altares con flores
  blancas, rosa y amarillo claro.
  https://babel.banrepcultural.org/digital/api/collection/p17054coll10/id/2782/download
- Eduardo Serrano, *Historia de la fotografía en Colombia* (Villegas Editores), sobre la iluminación y el
  retoque de retratos. https://100libroslibres.com/historia-de-la-fotografia-en-colombia-arte-y-fotografia-la-tradicion-del-retrato
- D. Álvarez y D. Chaves (2017), «El cultivo de trigo en Colombia: su agonía y posible desaparición»,
  *Rev. Cienc. Agríc.* 34(2). Cita a Valderrama (1976): franja triguera de 2.200–3.000 m. Cita a Adams y
  Mancini (1964): Boyacá «cerca de un 30%» de la producción nacional.
  http://www.scielo.org.co/scielo.php?script=sci_arttext&pid=S0120-01352017000200010
- «La industria harinera en Duitama-Boyacá 1920-1940», SciELO: cebada con la llegada de Bavaria (1936).
  http://www.scielo.org.co/scielo.php?script=sci_arttext&pid=S1657-63572012000100009
- José Eduardo Rueda Enciso, «Guaches vs. cachacos: la sociabilidad democrática en Bogotá 1845-1876»: los
  artesanos gritaban «viva la ruana, abajo las casacas azules». Es el antecedente popular de la ruana; el azul
  de las casacas era el de la élite, aún no el de un partido. https://dialnet.unirioja.es/descarga/articulo/5839872.pdf
- «El tranvía de Bogotá, 1882-1951», Redalyc: los tranvías de 1936, llamados «Lorencitas», tenían el techo
  plateado. https://www.redalyc.org/journal/419/41952579008/html/
- Enciclopedia Banrepcultural, «Alejandro Obregón»: la época «oscura» de 1948.
  https://enciclopedia.banrepcultural.org/index.php?title=Alejandro_Obreg%C3%B3n
- MAMM, *Masacre del 9 de abril* de Débora Arango. https://www.elmamm.org/coleccion-mamm/obra/masacre-del-9-de-abril/
- Ruanas de Nobsa, tonos naturales gris, blanco y negro: https://ruanasdenobsa.com/2021/11/08/la-ruana-boyacense/
- Páramos y frailejón: Instituto Humboldt. https://www.humboldt.org.co/noticias/entre-ruanas-y-frailejones-el-desafio-de-ubicar-el-ecosistema-de-paramo
- Casanare: verano de diciembre a abril e invierno que inunda la sabana.
  https://www.eltiempo.com/vida/viajar/conozca-el-encanto-llanero-de-casanare-359464
- Sady González, la ciudad en humo el 9 de abril: Archivo de Bogotá.
  https://archivobogota.secretariageneral.gov.co/noticias/legado-sady-gonzalez

## 11. Decisiones abiertas (Daniel)

Decididas el 2026-10-02:

1. ✅ Paleta aprobada y doc 03 actualizado (encabezado y §1, filas «Color» y «Modo registro»).
2. ✅ Rojo `#ca2d23` y azul `#1d4aac` (§2.1).
3. ✅ **Cinta de Rosalba en rojo liberal.** Está documentado (Ocampo) y marca a su familia liberal desde el
   primer cuadro. Con ella se aprobó la propuesta para narrativa: que la cinta pase de adorno a señal
   peligrosa. Falta llevarla al registro de propuestas (doc 10) desde el chat de narrativa.
4. ✅ Factores del guion de color aprobados como están, con el epílogo desvaído (§5).
5. ✅ Modo registro sin rojo ni azul (§6.6).
6. ✅ Implementación: (a) cada escena generada con el croma de su acto, y (b) filtro en vivo solo en momentos
   puntuales (§5).

Abiertas:

7. Pendientes **[P]**: uniformes, tranvía (carrocería), ladrillo y acabados de Bogotá, pañuelos de la
   guerrilla del Llano, piedra de las cercas.
