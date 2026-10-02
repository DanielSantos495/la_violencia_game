# Tomo I — Dirección de arte y estilo visual

**Estilo aprobado:** novela gráfica 2D en vista lateral. Tinta negra sobre papel envejecido, grises y sepias; **rojo y azul partidistas como únicos colores de acento**.
**Principio:** sencillo en imagen, exacto en época. Vestuario, arquitectura, armas y objetos siguen siendo correctos para 1946–1958; lo que no tenga fuente queda marcado **[P]** y no se dibuja en versión final hasta resolverse.

---

## 1. Lenguaje visual

| Elemento | Regla |
|---|---|
| Línea | Tinta negra de grosor variable: gruesa en siluetas y primeros planos, fina en fondos |
| Relleno | Manchas planas de negro; grises por trama (rayado o puntos de semitono), sin degradados complejos |
| Papel | Fondo color hueso con textura leve de papel de prensa |
| Color | Solo **rojo liberal** y **azul conservador**: pañuelos, banderas, afiches, fachadas de tiendas partidistas. El color cuenta la división |
| Encuadre de juego | Plano lateral con 2–3 capas de fondo en paralaje |
| Viñetas | Las escenas de guion se presentan como páginas de cómic: viñetas que aparecen en secuencia, globos de texto, onomatopeyas mínimas |
| Modo registro (Custodia) | Al fotografiar, la escena se congela en una viñeta con marco de foto de época y trama de semitono más densa |
| Transición al Archivo | La última viñeta de cada misión se convierte en la página del Archivo (donde luego se muestran fotos reales licenciadas) |

### Violencia (tono bélico sin espectáculo)
- La guerra se muestra: combates, incendios, muertos, desplazamiento. No se omite.
- Se dibuja con **silueta y mancha negra**: sin sangre roja (el rojo está reservado al partido liberal, y así no compite), sin gore ni mutilaciones detalladas.
- Las atrocidades se narran en viñetas fijas (antes/después, siluetas, humo, objetos abandonados); nunca son acciones controladas por el jugador.
- Muertos: cuerpos en silueta o cubiertos; rostros de víctimas nunca identificables.

---

## 2. Producción de assets (hechos por Claude)

**Formato:** ilustración vectorial **SVG** generada por código, exportada a PNG en atlas para el juego.

**Qué se puede producir con buena calidad así:**
- Fondos por capas (arquitectura, paisaje, interiores).
- Personajes en estilo de silueta y línea clara, articulados por piezas (cabeza, torso, brazos, piernas, ruana, sombrero) para animación por recortes (*cut-out*).
- Objetos, armas, vehículos, UI, marcos de viñeta, tipografía de prensa de época.

**Limitaciones honestas:**
- Es un estilo de **línea clara y manchas**, no dibujo a mano suelto con pincel. La textura de tinta se simula con filtros SVG y tramas.
- Rostros simplificados (pocos rasgos, expresión por ojos, cejas y postura). No retratos realistas.
- Animación por recortes y tweens, no animación cuadro a cuadro.
- Todo asset se revisa contra referencias de época antes de darse por final.

**Pipeline**
```
referencias [V] → boceto SVG → revisión histórica → SVG final por capas
  → script de exportación (SVG → PNG @1x/@2x) → atlas de texturas → juego
```
Los SVG fuente se versionan en el repo (`art/src`) y los PNG se generan en el build, nunca a mano.

### Lista de assets del vertical slice (Prólogo + Misión 2)
| Tipo | Assets |
|---|---|
| Personajes | Rosalba, Efraín, madre Insuasty, Aurelio, Heliodoro, Custodia, padre Evaristo, 3 chulavíes, 4 vecinos genéricos |
| Fondos | Plaza de Puente Alto (mercado), iglesia exterior/interior, casa Insuasty (exterior, interior con radio), cultivos, quebrada, monte al amanecer |
| Objetos | Radio de válvulas de época [P: modelo], cámara de prensa, libreta, escopeta del padre, lámpara de petróleo, afiches rojo/azul |
| UI | Globos de texto, marco de viñeta, visor de Archivo, libreta, contador de exposiciones (12) |

---

## 3. Referencias verificadas por bloque

### 3.1 Boyacá rural (Puente Alto)
| Elemento | Referencia | Estado |
|---|---|---|
| Vivienda | Un nivel, muros gruesos de adobe o tapia pisada, cubierta de madera con teja de barro cocido, alero sobre la fachada que forma corredor; habitaciones oscuras encadenadas | **[V]** estudio de vivienda rural en Ráquira |
| Muros | Tapia pisada encalada en blanco | **[V]** foto Biblioteca Virtual Banrep |
| Vestido hombre | Pantalón de dril (angosto, sobre el tobillo en la primera mitad del s. XX), camisa de algodón, ruana de lana, sombrero de tapia pisada (palmiche/fique) o de fieltro, alpargatas | **[V]** estudios de folclor boyacense |
| Vestido mujer | Falda de paño/algodón, blusa, pañolón, ruana, sombrero de paño negro o de caña, alpargatas blancas | **[V]** · detalle en J. Ocampo López, *El pueblo boyacense y su folclor*, cap. 4 (BanRep) |
| Iglesia, plaza, tiendas | Plaza con pila, iglesia colonial, tiendas con portón de madera | **[P]** fotos de pueblos del norte de Boyacá (Soatá, Boavita, La Uvita) años 40–50 |
| Paisaje | Altiplano y vertiente andina, cultivos, cercas de piedra | **[P]** referencias fotográficas regionales |

### 3.2 Bogotá, 9 de abril de 1948
| Elemento | Referencia | Estado |
|---|---|---|
| Punto del asesinato | Edificio Agustín Nieto, Carrera 7.ª con Av. Jiménez | **[V]** Fototeca Archivo de Bogotá |
| Tranvía | Tranvías incendiados en la Séptima | **[V]** fotos de Sady González |
| Edificios incendiados | Palacio de San Carlos, Palacio de San Francisco (Gobernación), hoteles Regina y Atlántico, palacio arzobispal, nunciatura, Palacio de Justicia (Calle 11 con Carrera 6.ª) | **[V]** IDPC y prensa |
| Capitolio | Sede de la IX Conferencia Panamericana | **[V]** |
| Escala del daño | Cerca de 150 inmuebles afectados; no exagerar la destrucción | **[V]** |
| Multitud | Machetes, palos, cuchillos | **[V]** Fototeca Archivo de Bogotá |
| Ropa urbana | Vestido de paño, sombrero de fieltro, gabardina; ruanas de migrantes rurales | **[P]** |
| Vehículos | Tranvía, taxis, buses y camiones de fines de los 40 | **[P]** modelos concretos |

En 2D la multitud se resuelve con capas de siluetas en paralaje: el riesgo técnico del 9 de abril desaparece.

### 3.3 Llanos Orientales (Casanare)
| Elemento | Referencia | Estado |
|---|---|---|
| Vestido | Pantalón y camisa blanca o caqui, cotizas, sombrero de ala ancha (pelo e' guama/fieltro o cogollo para faena) | **[V]** |
| Faja | Cinturón ancho de cuero con cuchillo o revólver | **[V]** |
| Arquitectura | Caney; chinchorro | **[V]** |
| Casco de Guadalupe Salgado | Casco alemán con estrella amarilla en la entrega de 1953 | **[V]** El Tiempo — reconfirmar con foto |
| Entrega de armas 1953 | Película silente de Marco Tulio Lizarazo, restaurada por Patrimonio Fílmico | **[V]** |

### 3.4 Fuerzas armadas y policía
| Elemento | Estado |
|---|---|
| Uniforme de la Policía 1948–1953 | **[P]** Museo Histórico de la Policía Nacional / Academia de Historia de la Policía |
| Chulavíes | Actuaban "en uniforme o en civil" **[V]**; mezcla de prendas **[P]** |
| Ejército 1948–1953 | **[P]** uniformes y equipo |
| Fusiles | Mauser en servicio **[P: modelos por año]** |
| Guerrilla | Escopetas, revólveres, machetes, armas capturadas **[P]** |

**Regla:** en estilo simplificado igual importa la silueta correcta (un fusil de cerrojo no se dibuja como uno automático).

---

## 4. Fuentes visuales primarias (a licenciar para el Archivo)
| Fondo | Custodio |
|---|---|
| Archivo fotográfico Sady González | Biblioteca Luis Ángel Arango / Banco de la República; copias en Fototeca del Archivo de Bogotá |
| Colección Museo de Bogotá | Museo de Bogotá |
| Película de Lizarazo (1953) | Patrimonio Fílmico Colombiano |
| Audio y radio de época | Señal Memoria (RTVC) |
| Contexto y cifras | CNMH |

Sin licencia, estas fuentes solo se usan como referencia interna para dibujar.

---

## 5. Audio (producido por Claude)

**Voces:** no hay. Todo el diálogo va en globos de texto. La emoción se transmite con la tipografía (tamaño, trazo tembloroso, globos quebrados para gritos), onomatopeyas dibujadas y sonido.

**Música**
- Compuesta por código: partitura (MIDI) generada a partir de estructuras de géneros de época y renderizada con instrumentos muestreados de licencia libre **[P: elegir bancos de sonido y verificar licencia de uso comercial]**.
- Boyacá: torbellino, guabina, bambuco con tiple, requinto y guitarra **[P: vigencia regional en los 40]**. Llano: joropo con arpa, cuatro y maracas. Bogotá 1948: radio de época (pasillo, bolero). La carranga es posterior, no se usa.
- Temas: uno por región + tema de cada personaje + tema de silencio/duelo (casi sin notas).
- Regla del guion: silencio antes que música en los momentos de mayor peso.
- **Limitación honesta:** los instrumentos muestreados libres no igualan a músicos grabados; el resultado es correcto y ambiental, no virtuoso.

**Efectos de sonido (síntesis por código)**
- Ambiente: viento de páramo, lluvia, fuego, grillos, río, mercado, campanas, radio con estática.
- Acción: pasos por superficie (tierra, piedra, madera), puertas, disparos de cerrojo y escopeta, obturador de cámara, pasar páginas.
- **Expresiones no verbales** (respiración agitada, jadeo, sollozo contenido, gritos lejanos de multitud): se producen por síntesis y procesado. **Limitación:** la voz humana sintetizada suena artificial de cerca; se usan filtradas, lejanas o mezcladas con ambiente, y siempre acompañadas de onomatopeya en viñeta. Se valida en la prueba de audio del Sprint 0 antes de producirlas en masa.

**Formato:** OGG como principal y M4A como respaldo (compatibilidad Safari); música en bucle con puntos de corte limpios.
- Grabaciones históricas reales (discursos, radio) solo en el Archivo y con licencia.

## 6. Entregables de arte de preproducción
1. Hoja de estilo: grosores de línea, tramas, paleta exacta (hueso, grises, negro, rojo, azul en hex).
2. Hoja de personaje de Rosalba, Aurelio y Custodia (frente, perfil, piezas de recorte). Rosalba en curso: `personajes/rosalba.md`.
3. Kit modular de arquitectura boyacense en SVG.
4. Prueba de escena: plaza de Puente Alto con paralaje y una página de cómic.
