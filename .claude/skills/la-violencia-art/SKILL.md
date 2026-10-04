---
name: la-violencia-art
description: >
  Dirección de arte y pipeline de assets del juego "La Violencia" (Tomo I): estilo novela
  gráfica de tinta, personajes SVG por piezas (cut-out), exactitud de época 1946–1958 y
  representación de la violencia sin espectáculo. Úsala SIEMPRE que se cree, edite, revise o
  anime cualquier asset visual del juego — SVG, personajes, fondos, paralaje, objetos, armas,
  uniformes, UI dibujada, viñetas de cómic, tweens de piezas o el atlas — aunque la petición
  no diga "arte" (p. ej. "crea un tween de caminata para Rosalba", "dibuja la plaza de Puente
  Alto", "añade el fusil de Aurelio"). Tiene prioridad sobre skills genéricas de arte o
  assets (create-game-assets, canvas-design, algorithmic-art) en este repo.
---

# La Violencia — arte

El juego es un documental jugable: el arte puede ser simple, pero no puede mentir sobre la
época ni convertir la violencia en espectáculo. Esta skill resume las reglas; **la fuente es
`planeacion/arte/tomo1/03_direccion_arte.md` (doc 03)**. Léelo antes de actuar: aquí no se
copian sus tablas para que no queden desactualizadas. `planeacion/` es solo lectura salvo
que Daniel pida editarla.

## Antes de dibujar

1. Lee el doc 03 §1 (lenguaje visual y violencia) y la sección de §3 que corresponda al
   lugar o actor (Boyacá rural, Bogotá 9-abr-1948, Llanos, fuerzas armadas y policía).
2. Busca cada elemento que vas a dibujar en la tabla [V]/[P] del doc 03 §3. Si está **[P]**
   o no aparece, no lo dibujes como versión final: haz un placeholder marcado
   (`data-p="motivo"` en el grupo y "[P]" en el nombre del archivo o en un comentario) y
   avísalo. Un [P] dibujado con aplomo se lee como hecho histórico.
3. Si el asset es de un personaje, revisa su nombre y rol en
   `planeacion/historia/tomo1/01_biblia_nomenclatura.md` (doc 01): las figuras reales
   aparecen con nombre alterado y nunca se retratan con rasgos inventados como si fueran
   documentales.

## Estilo (resumen del doc 03 §1)

- Tinta negra de grosor variable (gruesa en siluetas y primer plano, fina en fondo) sobre
  papel hueso con textura leve.
- **Detalle limpio** (doc 03 §1 «Relleno»): el color de la paleta da el valor y la trama solo
  dice sombra. Nada de trama como textura (semitono, rayas, cuadrícula, veta de relleno).
  Sombras chicas en aguada plana de tinta (`fill-opacity`); rayado abierto (paso ≥ 9 px ya en
  pantalla, medido después de escalar el personaje) solo en sombras grandes cercanas; capas
  lejanas sin trama. Textura con pocas marcas dibujadas e irregulares. Las marcas interiores
  se recortan a la silueta (`clipPath`): nada se sale del borde. Sin degradados.
- Únicos acentos de color: **rojo liberal** y **azul conservador**, y solo en lo que cuenta
  la división (pañuelos, banderas, afiches, fachadas). Ningún otro color de acento. El resto
  del mundo, si lleva color, va en lavados apagados de la paleta (ver "Paleta").
- Plano lateral con 2–3 capas de paralaje por escena.
- Rostros simplificados: expresión por ojos, cejas y postura; nada de retrato realista.

## Violencia (doc 03 §1 "Violencia")

- Explícita cuando la escena lo pide (heridas, sangre y muertos visibles), por su peso y no
  como espectáculo. **La sangre se vuelve tinta:** roja solo en el
  instante, como mancha orgánica con textura y borde irregular; en segundos se oxida a tinta
  negra (tween de tinte) y en viñetas fijas ya es negra. El rojo partidista es siempre plano,
  de imprenta, borde limpio y solo en objetos (doc 03 §1).
- Rostros de víctimas nunca identificables.
- La violencia contra civiles puede ser jugable en momentos guionizados (doc 02 §1 regla 1):
  los assets de esas escenas deben poder animarse; el después se cierra en viñetas fijas.
- Armas: silueta correcta para el año. Un fusil de cerrojo no se dibuja como uno automático;
  los modelos por año están [P] en el doc 03 §3.4 hasta que se resuelvan.

## Paleta

Fuentes de color:

- **Reglas y fuentes:** `planeacion/arte/tomo1/paleta.md`, aprobada por Daniel el 2026-10-02. Rojo
  `#ca2d23` y azul `#1d4aac`. Guion de color por acto: cada escena se genera con el
  `croma_mundo` de su acto (`guion` en el JSON); detalle en su §5.
- **Valores:** `game/art/paleta.json`. Cada color tiene id, OKLCH, hex, uso y fuente. Los generadores
  cargan el JSON y usan tokens por id; no escribas hex sueltos.
- **Para elegir o añadir un color:** sigue la skill `paleta-tematica` y valida con
  `python3 .claude/skills/paleta-tematica/scripts/validar_paleta.py game/art/paleta.json`.

Lo esencial: el mundo va en lavados apagados (registro `iluminacion`, con techo de croma). El rojo
y el azul son tinta plana de imprenta y nada más puede entrar en sus zonas de tono. Por eso el
fuego es ocre, y el cielo, el agua y la noche no son azules. Un `id` no se renombra sin avisar.

Las tramas están en el doc 03 §1 «Relleno»; los grosores de línea siguen pendientes (doc 03 §6.1) **[P]**.

## Personajes por piezas (cut-out)

Piezas mínimas (doc 03 §2): cabeza, torso, brazos, piernas, ruana, sombrero.

Convención del pipeline (`game/tools/art-build.ts`):

- Un archivo por personaje: `game/art/src/personajes/<personaje>.svg`, con
  `viewBox="0 0 W H"` (1 unidad = 1 px a @1x).
- Cada pieza es un `<g id="…" data-pieza data-pivote="x y">` directo bajo la raíz.
  El pivote está en la articulación (hombro, cadera, cuello) en coordenadas del viewBox.
- IDs estables en kebab-case, con lado del **propio personaje**:
  `cabeza`, `torso`, `brazo-izq`, `brazo-der`, `antebrazo-izq`, `antebrazo-der`,
  `pierna-izq`, `pierna-der`, `ruana`, `sombrero`. Detalles internos pueden llevar ids
  propios dentro de la pieza (`ojo-izq`, `ceja-der`), pero no cambies un id publicado:
  el código y los tweens los referencian como frame `personajes/<personaje>/<id>`.
- Si una pieza cuelga de otra (antebrazo → brazo, zarcillo o sombrero → cabeza), añade
  `data-padre="<id>"`; el padre se declara antes y el hijo hereda su movimiento en Phaser.
- El orden en el documento es el orden de dibujo (lo primero queda detrás).
- `<defs>` compartidas (tramas) arriba; SVGO conserva ids, grupos y `data-*`.

En Phaser se arma con `armarRecorte()` (`game/src/game/Recorte.ts`): todas las piezas en el
mismo punto, cada una en un contenedor articulado en su pivote (y anidada según
`data-padre`). Las animaciones son **tweens de Phaser** sobre esas articulaciones, no cuadro
a cuadro. La caminata es procedural: `poseCaminata()` (`game/src/core/animacion/caminata.ts`)
calcula la pose y `caminar()` (`game/src/game/Caminata.ts`) la aplica; reutiliza esos ids
(`pierna-*`, `brazo-*`, `antebrazo-*`, prendas) para que un personaje nuevo camine sin código
extra. Con **falda larga** (Rosalba) las piernas no giran desde la cadera: usa la opción
`faldaLarga` (pies que se deslizan bajo el ruedo, pivote de la pierna en el **tobillo**) y
verifica con `pnpm art:walk <svg> --falda-larga`, que falla si en alguna fase asoma la canilla
o un pie sale por detrás de la falda. Para la API de tweens consulta la skill oficial `tweens`.

Poses que no salen de girar piezas (agacharse, caer, trepar) se **dibujan aparte** en otro
SVG del mismo personaje, en el mismo marco y con el mismo punto de apoyo entre los pies.
`Personaje` (`game/src/game/Personaje.ts`) cambia de pose con un aplastamiento breve hacia el
suelo; las listas de piezas por pose van en `game/src/game/personajes/<personaje>.ts`.
Si los SVG de un personaje se generan con un script (`game/art/gen/<personaje>.py`), edita
el script y regenera: no edites el SVG generado.

## Pipeline (no edites PNG a mano)

```
art/src/**/*.svg → SVGO → PNG @1x/@2x → un multiatlas por carpeta (art/build/atlas, public/generated/art)
```

- `pnpm run art:build` (en `game/`) genera todo; los PNG jamás se editan a mano.
- **Un atlas por carpeta:** la clave del atlas es la carpeta del SVG (`personajes`,
  `fondos/puente-alto`); organiza los SVG por escena para que cada una cargue solo lo suyo.
  En la escena: `cargarAtlas(this, 'personajes', 'fondos/puente-alto')`
  (`game/src/game/arte.ts`). Si un atlas no cabe en 4096 px se reparte en páginas; un frame
  que por sí solo no cabe es un error: divídelo en módulos o tramos.
- `pnpm run art:review <ruta.svg | art/build/atlas/<grupo>@1x.json>` crea un PNG de revisión en
  `art/build/revision/` con cajas y pivotes. Ábrelo (Read) para inspeccionarlo antes de
  dar un asset por bueno.
- `pnpm run art:walk <personaje.svg> [fases]` crea la hoja del ciclo de caminata
  (`art/build/revision/<nombre>-caminata.png`) con la misma pose que usa el juego: revisa
  apoyo de pies, contrafase de brazos y que las prendas no se despeguen.
- Las referencias de época se usan solo para dibujar; las fotos reales con licencia viven
  en el Archivo, no en el arte del juego (doc 03 §4).

## Checklist por asset

1. ¿Cada elemento de época está [V] en el doc 03 §3? Lo [P] queda como placeholder marcado.
2. ¿Solo tinta, trama, lavados de `paleta.json` y los dos acentos partidistas? ¿Sin
   degradados, sin hex sueltos y sin nada fuera del partido en las zonas roja o azul?
3. ¿Detalle limpio? Trama solo en sombras (paso ≥ 9 px en pantalla), ninguna textura de relleno
   y ninguna marca que se salga de la silueta del objeto.
4. ¿Violencia con peso y no como espectáculo? ¿Sangre orgánica que se oxida a negro (nunca roja plana)? ¿Sin rostros de víctimas identificables?
5. ¿Silueta de arma/uniforme/vehículo correcta para el año?
6. Personajes: ¿piezas con ids de la convención, pivotes en articulaciones, orden de capas?
7. `pnpm run art:build` sin errores y PNG de revisión inspeccionado.
8. ¿Se ve bien a escala de juego (1920×1080) sobre su fondo y con el paralaje, también reducido
   al 50–75 % (pantalla de portátil) y con la cámara en movimiento, sin hormigueo?
9. Si es la figura de una persona real: ¿sin rasgos inventados presentados como documentales?
