# Tomo I "La Violencia" — Plan de implementación

## Documentos del plan
| # | Documento | Contenido |
|---|---|---|
| 00 | Plan de implementación (este) | Decisiones, fases, backlog de arranque, riesgos, fuentes |
| 01 | Biblia de nomenclatura | Nombres ficticios de personas, partidos, grupos, medios y pactos |
| 02 | Guion y narrativa | Arcos, sistema de decisiones, beats y diálogos clave del prólogo, 9 misiones y epílogo, finales |
| 03 | Dirección de arte | Estilo visual recomendado, referencias verificadas por región, fuentes a licenciar |
| 04 | Documento técnico | Plataforma web + escritorio, Phaser 4, stack, arquitectura, combate, episodios, esquema del Archivo |
| 05 | Prompt de setup desde cero | Bloques de configuración del proyecto en `game/` con Claude Code y decisiones del Bloque 0 |
| 06 | Prompt de skills de narrativa | Skills de narrativa (terceros y `la-violencia-narrativa`), diagnóstico del guion, herramientas narrativas y primera pasada de pulido |

---

## 1. Decisiones tomadas en este plan (revisables)
1. **Nombres alterados en la ficción; nombres reales en el Archivo.** Se mantiene la regla de no inventar diálogos a figuras reales aunque estén renombradas.
2. **Estilo visual: novela gráfica 2D lateral**, tinta sobre papel con rojo y azul partidistas como únicos acentos. Assets SVG producidos por Claude (doc 03).
3. **Plataforma: web principal + escritorio** (Tauri) con **Phaser 4 + TypeScript + Ink/inkjs**; el Archivo vive en el mismo sitio (doc 04).
4. **Correcciones al guion base** (pájaros → chulavíes en Boyacá, traslado de Aurelio a Bogotá el 10-abr-1948, anclaje de la Misión 8 a junio de 1954, etc.). Detalle en doc 02 §2.

## 2. Decisiones confirmadas por Daniel (28-sept-2026)
| Tema | Decisión |
|---|---|
| Nombres | Alterados en la ficción; reales en el Archivo con correspondencia |
| "9 de abril" / "Bogotazo" | Se mantiene sin alterar |
| Jugabilidad | Aventura lateral; bélica, sin omitir la violencia ni la guerra |
| Combate | Simple y poco frecuente |
| Plataforma | Web + escritorio |
| Público | General adulto |
| Equipo | Daniel como único desarrollador; Claude produce arte, música y efectos de sonido |
| Voces | Sin voces: solo texto en globos |
| Duración | Por episodios (3 episodios, uno por acto) |
| Color | Tinta + acentos rojo/azul |

**Pendiente todavía:** historiador(a) asesor(a) y presupuesto para licencias de archivo (fotos, película, audio histórico).

---

## 3. Fases

| Fase | Salida |
|---|---|
| **0. Preproducción** | Hoja de estilo, guion en Ink del prólogo y M2, proyecto base, fuentes [P] críticas del slice |
| **1. Vertical slice** | Prólogo + Misión 2 jugables en web (ver §4) |
| **2. Episodio 1** | M1 y M3 → lanzamiento web del Episodio 1 |
| **3. Episodios 2 y 3** | Actos II y III + epílogo; versión escritorio |

Sin plazos: se avanza por fases y sprints; cada fase empieza cuando la anterior cumple su salida.

## 4. Vertical slice recomendado
**Prólogo + Misión 2 ("La noche de los chulavíes").**
Por qué: cubre las mecánicas núcleo (movimiento lateral, cámara de Custodia, sigilo y huida de Rosalba, página de cómic, decisiones, Archivo) en un solo escenario (Puente Alto). Queda fuera el combate, que se prueba en la M3.

---

## 5. Backlog de arranque (Sprint 0 y 1)

### Sprint 0 — Fundaciones
**Producción / investigación**
- [ ] Definir presupuesto para licencias de archivo.
- [ ] Contratar/asesorarse con historiador(a) del periodo 1946–1958.
- [ ] Solicitar licencias: Banrep (fondo Sady González), Archivo de Bogotá, Museo de Bogotá, Patrimonio Fílmico (película de Lizarazo), Señal Memoria.
- [ ] Resolver fuentes [P] críticas del slice: uniforme policial 1948, vestimenta de chulavitas, cronología de la violencia en el norte de Boyacá tras el 9 de abril.
- [ ] Verificar que ningún nombre ficticio de la biblia coincida con personas vivas conocidas.

**Técnica**
> El código anterior se borró para reconstruir desde cero con el doc 05 (rama `setup/tomo1-base`, 1-oct-2026). Las tareas técnicas vuelven a estar pendientes.

- [x] Verificar versiones vigentes (1-oct-2026): Phaser 4.2.1, Vite 8, TypeScript 7, inkjs 2.4.0, Node 24 LTS, pnpm 11. Detalle en doc 04 §3.
- [ ] Crear proyecto en `game/` con estructura por capas (`src/core`, `src/game`, `src/ui`, `content/`, `art/src`, `tools/`, `tests/`; ver doc 04 §4).
- [ ] Integrar inkjs: prólogo de prueba con decisión, globos en DOM.
- [ ] Validador del Archivo (modo release excluye pendientes) + GitHub Actions.
- [ ] Pipeline de arte: SVGO → SVG → PNG → atlas (empaquetador por elegir).

**Arte (Claude)**
- [ ] Hoja de estilo con paleta en hex, grosores y tramas.
- [ ] Hoja de personaje de Rosalba (piezas de recorte).
- [ ] Fondo de prueba: plaza de Puente Alto en 3 capas de paralaje (provisional; se perdió con el código borrado).
- [ ] Prueba de audio: tema de Puente Alto (torbellino) + 5 efectos + 2 expresiones no verbales, para validar calidad antes de producir en masa.

### Sprint 1 — Primer jugable del slice
- [ ] Escena lateral con movimiento, paralaje y cámara que sigue al personaje.
- [ ] `Camara.ts`: rollo de 12 exposiciones, viñeta de foto, guardado en archivo del jugador.
- [ ] `PaginaComic`: viñetas en secuencia con globos desde Ink.
- [ ] `ArchivoStore` leyendo 3 entradas de prueba.
- [ ] Guion completo del prólogo en Ink.
- [ ] Assets del prólogo (lista en doc 03 §2).

### Definición de "hecho" para cada misión
1. Jugable de principio a fin sin bloqueos.
2. Todas las marcas [P] de esa misión resueltas o el elemento retirado.
3. Revisión del historiador firmada.
4. Entradas de Archivo con fuente y licencia válidas.
5. Ningún sistema premia matar; la violencia contra civiles solo es jugable en momentos guionizados y siempre con coste narrativo (doc 02 §1 regla 1).
6. Build de rendimiento dentro del objetivo.

---

## 6. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Imprecisión histórica | Alto (proyecto documental) | Marcas [P], historiador obligatorio, validación en CI del Archivo |
| Licencias de fotos/audio no concedidas | Medio | Solicitar en preproducción; plan B con fuentes de dominio público |
| Carga de trabajo de un solo desarrollador | Alto | Lanzamiento por episodios; slice pequeño; reutilizar sistemas entre misiones |
| Calidad de assets SVG generados por código | Medio | Estilo de línea clara diseñado para ese medio; prueba de escena antes de producir en masa |
| Calidad de música y expresiones sintetizadas | Medio | Prueba de audio en Sprint 0; expresiones siempre lejanas/filtradas y apoyadas con onomatopeya |
| Percepción de "tomar partido" | Alto | Perspectivas balanceadas, pruebas con públicos diversos y organizaciones de víctimas |
| Nombres alterados leídos como burla o evasión | Medio | Correspondencia explícita en el Archivo; tono sobrio |
| Integración de Steam en escritorio (Tauri) | Bajo–medio | Spike antes del Episodio 2; alternativa Electron |

---

## 7. Fuentes consultadas para este plan

**Históricas**
- Wikipedia (es): "Los Chulavitas" — origen en la vereda Chulavita (Boavita) y envío de reservistas a Bogotá el 10-abr-1948.
- Semanario Voz, "Yo vi llegar a los chulavitas" (2025).
- Repositorio Uniandes, "Relatos de 'todo lo malo': el caso de Chulavita".
- CNMH, "El legado de Guadalupe Salcedo y Dumar Aljure" (2024).
- Señal Memoria, "La paz con las guerrillas liberales, 70 años después" (2023) y "Censura de El Tiempo en el gobierno de Rojas Pinilla".
- El Tiempo, archivo 1991 "Clave 1953 guerrilla Llanos"; archivo 2005 y 2015 sobre el cierre de El Tiempo; nota 2019 sobre junio de 1954.
- El Espectador, "Guadalupe Salcedo y la historia de los incumplimientos…" (2021); "60 años de un proceso de paz"; "60 años de una tragedia estudiantil".
- Fototeca Digital del Archivo de Bogotá (registros de Sady González, 9-abr-1948); Semana, "Sady González, el fotógrafo del Bogotazo".
- IDPC, "Patrimonio en llamas: el Bogotazo y sus cicatrices".
- Biblioteca Virtual Banrep / Cervantes Virtual ("Campesina caminando"); estudios de vivienda rural de Ráquira; textos de folclor boyacense y llanero.

**Técnicas**
- Phaser 4 (phaser.io): descargas y notas de versión 4.x.
- inkjs (inkle, GitHub).
- Tauri 2 y Steam: guía de portado e issue de overlay.
- 80.lv: Godot 4.6 (ene-2026).

## 8. Pendientes de fuente [P] — resumen
Fecha exacta de entrega de armas de 1953 (12 vs 15 de sept.) · uniformes policiales y militares 1948–1954 · armamento por año · cifra de muertos del 9 de abril · cronología de la violencia en el norte de Boyacá · estatus administrativo de Casanare · unidad que disparó el 9-jun-1954 · cifra total de La Violencia según CNMH · lluvia la noche del 9 de abril · géneros musicales vigentes en Boyacá en los 40.
