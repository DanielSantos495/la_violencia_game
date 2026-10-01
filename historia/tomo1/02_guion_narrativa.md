# Tomo I — Guion, narrativa y storytelling

> Nomenclatura: ver `01_biblia_nomenclatura.md`. En este guion los nombres de figuras históricas aparecen en su versión de juego; el Archivo usa los reales.
> Marcas: **[V]** verificado con fuente (ver tabla final) · **[P]** pendiente de fuente antes de cerrar guion.

---

## 1. Núcleo narrativo

**Logline:** tres vecinos de un pueblo de Boyacá atraviesan diez años de guerra no declarada entre rojos y azules; ninguno es héroe y ninguno sale intacto. El país firma la paz entre dirigentes, pero en el campo los muertos no se reparten por pactos.

**Tema central:** la violencia partidista como maquinaria que convierte vecinos en enemigos, y la paz pactada desde arriba que no repara abajo.

**Tono:** bélico y sobrio. La guerra se muestra sin omitirla, pero sin épica ni espectáculo. Referencia: novela gráfica testimonial y crónica de guerra.

**Formato:** aventura lateral 2D en estilo novela gráfica (doc 03). Diálogos solo en globos de texto (sin voces); la emoción se marca con tipografía, onomatopeyas y sonido. Se publica en 3 episodios: **Ep. 1** Prólogo + Acto I · **Ep. 2** Acto II · **Ep. 3** Acto III + Epílogo. El combate es breve, poco frecuente y solo contra armados (doc 04 §5).

**Reglas de storytelling**
1. **El jugador nunca ejecuta una atrocidad.** Las masacres se narran en páginas de cómic (siluetas, humo, ausencia, antes/después), nunca como secuencia jugable ni con detalle gráfico.
2. **Cada bando tiene razones y culpas.** Ningún personaje secundario es caricatura: hay azules que protegen liberales y rojos que cometen represalias.
3. **La historia grande entra por medios de época:** radio, periódico, rumor, altavoz. Las figuras reales casi nunca están en escena.
4. **La información es el recurso central.** Se recompensa observar, recordar y registrar, no matar.
5. **Silencio antes que música** en los momentos de mayor peso.

---

## 2. Correcciones al guion base (`tomo1_la_violencia.md`)

| # | Guion base | Corrección | Motivo |
|---|---|---|---|
| 1 | Misión 2: "ataque de pájaros" en Puente Alto (Boyacá) | Ataque de **chulavíes** / policía conservadora | Los pájaros operaban en Valle del Cauca y Viejo Caldas; en Boyacá el actor fueron los chulavitas **[V]** |
| 2 | Personaje "Father/Doña Custodia" | **Doña Custodia Salamanca** | Error de redacción |
| 3 | Misión 3: Aurelio patrulla solo en Puente Alto | Aurelio es enviado **a Bogotá el 10 de abril** con los contingentes conservadores de Boyacá, y luego regresa | Hecho documentado: el gobernador de Boyacá despachó reservistas del norte del departamento a Bogotá el 10-abr-1948 **[V]**. Permite cruzar a Aurelio y Custodia en Bogotá |
| 4 | Misión 8: Aurelio reprime "una protesta" genérica | Anclar a **8–9 de junio de 1954** (estudiantes en Bogotá); Aurelio es testigo, no tirador | Evento documentado **[V]**; quiénes dispararon exactamente y la adscripción de la policía en 1954 **[P]** |
| 5 | Epílogo cita solo "el pacto" | Secuencia: caída de Rojas (10-may-1957) → asesinato de Guadalupe Salgado en Bogotá (6-jun-1957) **[V]** → Acuerdo del Garraf → plebiscito → 7-ago-1958 | Refuerza el tema de la paz incumplida con un hecho verificado |

---

## 3. Personajes y arcos

### Rosalba Insuasty (jugable — perspectiva civil → insurgente)
- **Inicio:** 19 años, hija de pequeños propietarios liberales. Sabe leer gracias a Custodia.
- **Herida:** la muerte de su hermano Efraín y la pérdida de la parcela.
- **Arco:** de víctima a combatiente a sobreviviente. Su pregunta: ¿defenderse justifica volverse igual a quien te atacó?
- **Voz:** habla boyacense ("sumercé", diminutivos, trato de usted). En el Llano aprende códigos llaneros.

### Aurelio Mesa (jugable — perspectiva estatal/paraestatal)
- **Inicio:** 20 años, hijo de Heliodoro Mesa, jefe conservador de vereda. Católico devoto. Amigo de infancia de Efraín.
- **Herida:** obedecer lo lleva a estar presente donde no quería.
- **Arco:** de convicción heredada a duda, a deserción. Su pregunta: ¿cuánto de lo que cree es suyo?
- **Regla de diseño:** el jugador puede desobedecer órdenes injustas; tiene consecuencias (castigo, sospecha), nunca premio por cumplirlas.

### Doña Custodia Salamanca (jugable ligera — perspectiva documental)
- **Inicio:** 45 años, maestra de Puente Alto, corresponsal de *El Correo del Norte*. Liberal moderada, respetada por ambos lados.
- **Herida:** la censura. Lo que ve no puede publicarse.
- **Arco:** de periodista a archivista clandestina. Su archivo personal ES el modo Archivo dentro de la ficción.
- **Mecánica:** cámara con un rollo de 12 exposiciones por misión, libreta de notas y entrevistas. No porta armas.

### Secundarios clave
- **Heliodoro Mesa:** no es un monstruo; teme sinceramente "la revolución roja". Su miedo es el motor de la violencia.
- **Padre Evaristo Rincón / Padre Julián Cárdenas:** las dos caras del clero de la época.
- **Sargento Calixto Morales:** profesional frío; representa la institucionalización de la violencia.
- **Ramiro "el Gaván" Cuéllar:** jefe llanero carismático, justo con los suyos, implacable con sospechosos.
- **Tránsito Guío:** llanera, amiga de Rosalba; encarna la población civil que sostenía a la guerrilla.

---

## 4. Sistema de decisiones

Variables ocultas (se evalúan en el epílogo):

| Variable | Rango | Afectada por |
|---|---|---|
| `rosalba_represalia` | 0–3 | Decisiones de represalia contra civiles conservadores (M4, M7) |
| `rosalba_desmovilizada` | bool | Decisión de entregar armas (fin Acto II) |
| `aurelio_conciencia` | 0–5 | Desobedecer, advertir o proteger a civiles (M3, M5, M8) |
| `aurelio_deserta` | bool | Decisión final de M8 |
| `custodia_archivo` | 0–100 | Fotos y testimonios de valor documental registrados |
| `custodia_publica` | 0–3 | Veces que publica pese a la censura (sube riesgo) |
| `lazos_puente_alto` | 0–3 | Momentos en que los tres personajes se ayudan indirectamente |

---

## 5. Guion por misión

### PRÓLOGO — "La aldea dividida"
**Fecha/lugar:** mayo–junio de 1946, Puente Alto (Boyacá). Contexto: el conservador Mariano Ospino Peralta ha ganado con el liberalismo dividido **[P: fecha exacta de elección, 5-may-1946]**.
**Jugable:** Custodia (tutorial de cámara/notas) → Rosalba (exploración del pueblo).

**Beats**
1. Mañana de mercado. Custodia fotografía la plaza: tiendas "rojas" y "azules" una frente a otra. Tutorial: encuadre, exposición limitada, anotar.
2. Rosalba lleva cuajada al mercado con Efraín. Encuentro con Aurelio: bromas de infancia, tensión cuando Heliodoro aparece.
3. Misa dominical: el padre Evaristo predica sobre "el peligro rojo". Rosalba y Efraín salen antes. (Sin interacción; peso ambiental.)
4. Noche: reunión liberal en la casa de los Insuasty para escuchar la radio. Llega la Seccional y disuelve la reunión. Efraín es golpeado.
5. Cierre: Custodia anota en su libreta. Primera entrada de Archivo.

**Diálogo clave (ficticio)**
> **HELIODORO:** Aurelio, a esa casa no se entra de noche.
> **AURELIO:** Es la casa de Efraín, papá.
> **HELIODORO:** Ya no es la casa de Efraín. Es la casa de un rojo.

**Archivo desbloqueado:** Elecciones de 1946 y división liberal · El bipartidismo en Boyacá · Vestido campesino boyacense.

---

### ACTO I — "El 9 de abril" (1948)

#### Misión 1 — "Carrera Séptima" (Custodia)
**Fecha/lugar:** 9-abr-1948, centro de Bogotá. **[V]** Asesinato frente al edificio Agustín Nieto (Carrera 7.ª con Av. Jiménez) · IX Conferencia Panamericana sesionando · incendio de tranvías, Palacio de San Carlos, Gobernación (San Francisco), hoteles Regina y Atlántico · linchamiento de Roa Serna.
**Hora exacta del disparo y cifra de muertos del Bogotazo [P]** — las estimaciones varían mucho; no dar cifra sin fuente.
**Por qué está Custodia en Bogotá:** viaja a entregar en la redacción de *Jornada Popular* una crónica sobre la persecución en Boyacá.

**Mecánica:** observación y registro. Sin combate. Riesgo: turba, disparos, incendios. Fallar = Custodia herida, pierde el rollo.

**Beats**
1. Mediodía. Ambiente de ciudad moderna: tranvía, cafés, delegados extranjeros. Custodia camina por la Séptima buscando la redacción.
2. Disparos fuera de cámara. El jugador no ve el asesinato; escucha, llega tarde, ve el tumulto frente al edificio. **No se recrea el cuerpo de Gaitano.**
3. La radio tomada anuncia la noticia (texto ficticio, sin atribuir a personas reales).
4. La multitud arrastra a Roa Serna **fuera de cuadro**; Custodia decide si fotografiar o apartarse (ambas válidas; fotografiar suma Archivo y resta salud emocional/riesgo).
5. Tarde: incendio del tranvía y de edificios; saqueo. Custodia protege a un niño perdido (opcional) o documenta.
6. Anochecer, lluvia **[P: confirmar lluvia esa noche con fuente]**. Custodia se refugia en una pensión. Escucha disparos de francotiradores y rumores contradictorios.
7. Madrugada del 10: ve llegar camiones con campesinos armados de Boyacá. Entre ellos reconoce a Aurelio. **Primer cruce.**

**Diálogo clave (ficticio)**
> **HOMBRE EN LA CALLE:** ¡Mataron al Tribuno! ¡Mataron al pueblo!
> **CUSTODIA** *(voz interna, a la libreta)*: Nueve de abril. Una y tantos. No lo vi caer. Vi caer la ciudad.

**Archivo:** Jorge Eliécer Gaitán · El 9 de abril (fotografías de Sady González, Archivo de Bogotá/Banrep, con licencia) · IX Conferencia Panamericana y creación de la OEA · Edificios destruidos.

#### Misión 2 — "La noche de los chulavíes" (Rosalba)
**Fecha/lugar:** días posteriores al 9-abr-1948, Puente Alto. **[P]** Cronología exacta de la violencia en el norte de Boyacá tras el 9 de abril (fuente: estudio Uniandes sobre Chulavita; Guzmán, Fals Borda y Umaña).
**Mecánica:** sigilo y huida. Rosalba no tiene arma al inicio.

**Beats**
1. En el pueblo, liberales celebran un breve "levantamiento" que dura horas; conservadores se arman.
2. Noche: llega una partida de chulavíes (policías uniformados mezclados con civiles armados **[P: vestimenta mixta según fotos de época]**).
3. Rosalba y Efraín esconden a la madre. Efraín sale a distraerlos. Ella escucha, no ve.
4. Huida por los cultivos y la quebrada. Quema de la casa vista a distancia.
5. Amanecer en el monte. Encuentra a otros desplazados. Toma la escopeta de su padre.

**Diálogo clave (ficticio)**
> **EFRAÍN:** Sumercé se lleva a mi mamá por la quebrada. Yo los entretengo.
> **ROSALBA:** No, Efraín.
> **EFRAÍN:** Si nos cogen a los tres, no queda nadie que cuente.

**Archivo:** Los chulavitas de Boavita · Desplazamiento en La Violencia · Vivienda campesina (tapia pisada, teja de barro).

#### Misión 3 — "Reservistas" (Aurelio)
**Fecha/lugar:** 10-abr-1948: concentración en Soatá/Duitama/Tunja y traslado a Bogotá **[V]**; mayo–junio 1948: regreso a Boyacá como policía.
**Mecánica:** aventura lateral con órdenes y sistema de conciencia. Incluye el único combate del episodio 1 (azoteas en Bogotá, contra francotiradores armados).

**Beats**
1. Heliodoro inscribe a Aurelio como reservista. Bendición de armas en la iglesia **[P: bendición de armas documentada en testimonios; confirmar para Boyacá]**.
2. Camión a Bogotá. Llegada a la ciudad humeante. Cruce visual con Custodia.
3. Guardia de edificios en Bogotá: enfrentamiento breve con francotiradores en azoteas (combate contra armados).
4. Regreso a Boyacá con uniforme. Primer patrullaje en Puente Alto, a casas de antiguos vecinos.
5. **Decisión:** en la casa quemada de los Insuasty, Aurelio encuentra la libreta escolar de Rosalba. Guardarla (conciencia +1) o entregarla al sargento.

**Diálogo clave (ficticio)**
> **SARGENTO MORALES:** Aquí no hay vecinos, Mesa. Hay azules y hay rojos.
> **AURELIO:** ¿Y los que no son nada?
> **SARGENTO MORALES:** Esos son rojos que todavía no se han dado cuenta.

**Archivo:** Contingentes boyacenses del 10 de abril · La policía partidista · Armamento de 1948 **[P]**.

---

### ACTO II — "El monte y la ley" (1949–1953)

#### Misión 4 — "Sabana adentro" (Rosalba)
**Fecha/lugar:** 1951–1952, Casanare **[P: estatus administrativo de Casanare en la época — confirmar si era parte de Boyacá]**.
**Contexto [V]:** guerrillas liberales del Llano financiadas por aportes campesinos y ganaderos; ataque a Orocué (junio 1952); gran emboscada al Ejército en 1952; Primera Ley del Llano (11-sept-1952).
**Mecánica:** combate de emboscada con recursos escasos, navegación a caballo, protección de civiles.

**Beats**
1. Rosalba llega al Llano con desplazados boyacenses. Tránsito la recibe. Choque cultural (clima, dieta, formas de hablar).
2. Entrenamiento con la columna del Gaván.
3. Emboscada a una patrulla (combatientes armados, no civiles). Inspirada en acciones de 1952, **no recrea una batalla específica con nombre**.
4. Tras la emboscada, un prisionero: joven soldado boyacense. **Decisión:** liberarlo, entregarlo al Gaván (será ejecutado fuera de cuadro; `rosalba_represalia` +1) o intercambiarlo.
5. Asamblea en un caney: se lee en voz alta el Primer Estatuto del Llano (texto parafraseado de la Ley del Llano **[V]**, cita breve si los derechos lo permiten).

**Diálogo clave (ficticio)**
> **TRÁNSITO:** Aquí nadie le pregunta a uno si es rojo. Le preguntan si sabe nadar.
> **EL GAVÁN:** Los azules nos enseñaron la guerra. No se nos olvide que no queríamos aprenderla.

**Archivo:** Guadalupe Salcedo · Leyes del Llano · Vestido llanero · Organización civil de la guerrilla.

#### Misión 5 — "Orden de limpieza" (Aurelio)
**Fecha/lugar:** 1950–1952, vereda liberal cercana a Puente Alto.
**Mecánica:** aventura lateral con dilema, sin combate. La columna policial recibe orden de "limpiar" un caserío.

**Beats**
1. Patrulla nocturna con Morales. Aurelio reconoce el caserío: familias que conoce.
2. **Decisión:** avisar en secreto a una familia (sigilo, alto riesgo, conciencia +2), quedarse en el perímetro (conciencia +0) o avanzar con la columna (la escena corta a negro; el jugador ve la consecuencia al amanecer; conciencia −1).
3. Amanecer: humo, silencio. Aurelio encuentra a una niña sobreviviente. La lleva al padre Julián.
4. Confesión con el padre Julián (ficticio). Primera verbalización de la duda.

> **PADRE JULIÁN:** ¿Viene a confesarse o a que le diga que no fue su culpa?
> **AURELIO:** No sé, padre.
> **PADRE JULIÁN:** Entonces empiece por ahí.

**Archivo:** Estado de sitio de 1949 y cierre del Congreso **[P: 9-nov-1949]** · La Iglesia durante La Violencia (posturas diversas).

#### Misión 6 — "Tinta y tijera" (Custodia)
**Fecha/lugar:** 1950–1952, Tunja y caminos de Boyacá.
**Contexto [V]:** bajo el estado de sitio la prensa circulaba con estricto control de contenidos.
**Mecánica:** investigación: entrevistar desplazados, fotografiar, montar la edición; el censor tacha. **Decisión:** publicar igual (`custodia_publica` +1, riesgo) o esconder en archivo personal.

**Beats**
1. Recorrido por caminos con desplazados; testimonios (escritos a partir de patrones documentados, no calcados de testimonios reales específicos).
2. Encuentra a la niña rescatada por Aurelio en la casa del padre Julián. **Cruce indirecto** Aurelio–Custodia (`lazos_puente_alto` +1).
3. Redacción de *El Correo del Norte*: minijuego de edición; llega el censor.
4. Allanamiento. Custodia salva el archivo o parte de él.

> **LEÓNIDAS PARDO:** Si no lo publicamos, no pasó.
> **CUSTODIA:** Pasó igual, Leónidas. Lo que no publicamos es lo que no se va a creer.

**Archivo:** Censura de prensa 1949–1957 · Caricaturistas de la época (referencia) · Cifras de desplazamiento **[P]**.

#### Evento histórico integrado — "El 13 de junio" (1953)
Secuencia no jugable (montaje de radio y prensa ficticia): golpe del Gral. Rojas Pineda **[V: 13-jun-1953]**, cese al fuego, decreto de indulto **[V: decreto 1546 de 1953, El Espectador]**.
**Cierre del Acto II — decisión de Rosalba:** acompañar a la columna a la entrega de armas o quedarse en el monte.
Entrega histórica **[V]:** Monterrey (Casanare), septiembre de 1953; Guadalupe Salgado entrega su arma al Gral. Duarte Blume. **Fecha exacta [P]:** una fuente da 12-sept (Las Delicias), otras 15-sept; resolver con fuente primaria.
Detalle visual verificado: Salgado portaba un casco alemán con estrella amarilla **[V: El Tiempo, archivo 1991 — reconfirmar con foto]**.

---

### ACTO III — "La amnistía rota" (1954–1957)

#### Misión 7 — "Los que entregaron" (Rosalba)
**Fecha/lugar:** 1954–1956, Llano o Boyacá según decisión.
**Contexto [V]:** muchos desmovilizados de la época fueron perseguidos o asesinados pese a la amnistía; la paz tuvo incumplimientos.
- **Si se desmovilizó:** intenta trabajar la tierra; compañeros aparecen asesinados; ella debe huir o esconderse. Sigilo.
- **Si siguió en armas:** la columna se fragmenta; algunos derivan en bandolerismo. **Decisión** sobre un robo a una familia campesina (`rosalba_represalia`).
**Cierre:** Rosalba escucha rumores de que antiguos comandantes están siendo buscados. (La muerte de Guadalupe Salgado, 6-jun-1957 **[V]**, se reserva para el inicio del epílogo, respetando la cronología.)

> **ROSALBA:** Nos dijeron que entregando el fusil se acababa la guerra.
> **TRÁNSITO:** Se acabó para ellos. Para nosotros apenas cambió de ropa.

#### Misión 8 — "Carrera Séptima con Calle 13" (Aurelio)
**Fecha/lugar:** 8–9 de junio de 1954, Bogotá **[V]**: el 8 muere el estudiante Uriel Gutiérrez en la Universidad Nacional; el 9, otros estudiantes mueren en la Carrera 7.ª con Calle 13.
**Rol de Aurelio:** su unidad es enviada como apoyo de control; está en la calle, **no es parte de quienes disparan**. **[P]:** unidad exacta que disparó y adscripción de la policía en 1954.
**Mecánica:** secuencia de tensión controlada, sin combate. El jugador decide dónde colocarse y a quién ayudar.
**Decisión final:** desertar esa noche (`aurelio_deserta`) o quedarse (y en el epílogo ser trasladado a otra región).
**Víctimas reales:** solo en el Archivo, con nombre real. En la ficción no se ven rostros identificables de víctimas.

> **AURELIO** *(a Morales, tras el silencio)*: Eran estudiantes, sargento.
> **SARGENTO MORALES:** Eran órdenes, Mesa.

**Archivo:** Estudiantes 8–9 de junio de 1954 · Gobierno militar 1953–1957.

#### Misión 9 — "El archivo" (Custodia)
**Fecha/lugar:** agosto 1955 – mayo 1957, Tunja y Bogotá.
**Contexto [V]:** cierre de *La Hora* (El Tiempo) en agosto de 1955, reemplazado por *Interludio*; cierre de *El Observador* (El Espectador); caída del gobierno militar el 10-may-1957 **[P: confirmar fecha y mecánica de la transición a Junta Militar]**.
**Mecánica:** la síntesis. El jugador organiza todo lo registrado en las misiones anteriores en el "archivo final" (tablero de pruebas: fotos, notas, testimonios). La calidad del archivo define el epílogo de Custodia.

**Beats**
1. Custodia recibe en Tunja la noticia del cierre de *La Hora*.
2. Oculta su archivo en la sacristía del padre Julián.
3. Mayo 1957: en Bogotá, cobertura de las jornadas contra el gobierno militar.
4. Composición del archivo final (puzle narrativo).

> **CUSTODIA:** No escribo para hoy. Hoy nadie lee. Escribo para el que venga a preguntar.

---

### EPÍLOGO — "El pacto" (1958)
**Hechos [V]:** Acuerdo de la Costa Blanca (24-jul-1956), Acuerdo del Garraf (20-jul-1957), plebiscito (1-dic-1957), Frente de Concordia Nacional desde el 7-ago-1958 con Alberto Llanos Camargo.
**Apertura:** junio de 1957, noticia radial del asesinato de Guadalupe Salgado en Bogotá por agentes de policía **[V]**, escuchada por Rosalba. Es el golpe que resignifica la amnistía.
**Escena coral:** los tres escuchan (o no) la radio del 7 de agosto de 1958 en lugares distintos. Montaje final con fotos del archivo de Custodia.

**Finales (según variables)**
1. **Reconciliación frágil:** `rosalba_desmovilizada` y sobrevive + `aurelio_deserta`. Rosalba vuelve a una parcela ajena como jornalera; Aurelio vive en Bogotá con otro nombre. Cruce final en un bus: se reconocen y no se hablan. Nota de Archivo: muchos excombatientes asesinados pese a la amnistía.
2. **Ciclo de venganza:** Rosalba sigue en armas con `rosalba_represalia` alto. Su grupo se desplaza al sur del Tolima. Enlaza con el Tomo II.
3. **Costo total:** muerte de uno o más personajes. El Archivo muestra que ese destino corresponde al de miles de personas reales del periodo.
- **Custodia en todos los finales:** su archivo sobrevive (en mayor o menor medida). Escena post-créditos: una estudiante en los años 60 encuentra la caja en la sacristía — puente al Tomo II.

**Cifra de cierre (Archivo):** estimaciones de muertos de La Violencia del orden de 200.000; el rango y la fuente se deben citar tal como los reporte el CNMH **[P]**.

---

## 6. Guía de escritura de diálogos

- **Boyacá:** trato de usted y "sumercé", diminutivos, religiosidad en expresiones cotidianas. Validar con hablantes de la región.
- **Llano:** léxico ganadero y fluvial; validar con asesor llanero (no copiar coplas con derechos).
- **Prohibido:** anacronismos ("ok", jerga actual), insultos modernos, citas inventadas de figuras reales.
- **Longitud:** frases cortas; la guerra se cuenta con pocas palabras.
- **Sin voces:** el acento regional se transmite en la escritura (léxico y giros), sin deformar la ortografía hasta volverla caricatura.

## 7. Estado del guion

| Entregable | Estado |
|---|---|
| Estructura y beats de las 9 misiones + prólogo + epílogo | Listo (este documento) |
| Diálogos completos | **Pendiente** — se escriben por misión en producción, a partir de estos beats y la guía |
| Revisión por historiador(a) | **Pendiente** — obligatoria antes de bloquear cada misión |
| Resolución de marcas **[P]** | **Pendiente** — ver tabla de fuentes del plan maestro |
