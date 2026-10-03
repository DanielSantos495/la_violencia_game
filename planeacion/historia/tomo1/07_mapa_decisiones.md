# Tomo I — Mapa de decisiones

> Fuente: doc 02 §4 (variables) y §5 (beats); regla de violencia en doc 02 §1 regla 1 (01-oct-2026).
> Este documento **no cambia el guion**: muestra dónde se escribe y se lee cada variable y qué
> ve el jugador. Las propuestas para cerrar huecos se registran en el doc 10.
> Estado: 01-oct-2026, a partir del diagnóstico narrativo (doc 06, Bloque 3).

Prueba de las cinco condiciones (skill `la-violencia-narrativa`): **1** opciones distintas ·
**2** consecuencia perceptible · **3** coste real · **4** expresa al personaje · **5** no premia
la violencia. En la tabla se listan las condiciones que **fallan**.

## 1. Decisiones del guion actual

| # | Misión · beat | Jugable | Opciones | Variable | Consecuencia visible hoy | Falla |
|---|---|---|---|---|---|---|
| DA | Prólogo · b1 | Custodia | Encuadrar la tienda roja o la azul (P26) | — | Expresiva: la foto elegida | 2 (a propósito) |
| DB | Prólogo · b4 | Rosalba | Esconder la radio / el periódico (P27) | `prologo_escondio` | **Sí**: M2 b1–b3 | — |
| D1 | M1 · b4 | Custodia | Fotografiar el linchamiento de Roa Serna / apartarse | `custodia_archivo` (+) | Ninguna definida; "resta salud emocional/riesgo" no existe como sistema | 2, 3 |
| D2 | M1 · b5 | Custodia | Proteger al niño perdido / documentar | — | Ninguna | 2 |
| DC | M2 · b4 | Rosalba | Llevarse la escopeta del padre / la libreta (P28) | `m2_se_llevo` | **Sí**: M3 b5 (Aurelio) y M4 b1 | — |
| D3 | M3 · b5 | Aurelio | Guardar la libreta de Rosalba / entregarla a Morales | `aurelio_conciencia` +1 | Ninguna | 2 |
| D4 | M4 · b4 | Rosalba | Liberar al prisionero / entregarlo al Gaván / intercambiarlo | `rosalba_represalia` +1 (entregar) | Ninguna antes del epílogo | 2 |
| D5 | M5 · b2 | Aurelio | Avisar a la familia / quedarse en el perímetro / avanzar con la columna | `aurelio_conciencia` +2 / 0 / −1 | Solo el corte a negro en "avanzar"; el amanecer (b3) es igual en las tres | 2 |
| D6 | M6 · b3 | Custodia | Publicar pese a la censura / esconder en el archivo | `custodia_publica` +1 | Ninguna: el "riesgo" no está definido y el allanamiento (b4) ocurre igual | 2, 3 |
| D7 | Cierre Acto II | Rosalba | Acompañar la entrega de armas / quedarse en el monte | `rosalba_desmovilizada` | **Sí**: cambia la M7 | — |
| D8 | M7 (en armas) | Rosalba | Robo a una familia campesina (opciones no definidas) | `rosalba_represalia` | Ninguna antes del epílogo | 1, 2 |
| D9 | M8 | Aurelio | Dónde colocarse y a quién ayudar | No definida | Ninguna | 2 |
| D10 | M8 · final | Aurelio | Desertar / quedarse | `aurelio_deserta` | **Sí**, pero solo en el epílogo | — |
| D11 | M9 | Custodia | Composición del archivo final | `custodia_archivo` (lectura) | **Sí**: epílogo de Custodia | — |

Sin decisión pero con variable: M6 · b2, cruce con la niña → `lazos_puente_alto` +1 automático.

## 2. Variables

| Variable | Rango (doc 02) | Se escribe en | Máximo alcanzable hoy | Se lee en | Consecuencia visible | Estado |
|---|---|---|---|---|---|---|
| `rosalba_represalia` | 0–3 | D4, D8 | 2 (si D8 suma 1) | Final 2 ("alto") | Solo en el final | ⚠ Rango inalcanzable; "alto" sin umbral |
| `rosalba_desmovilizada` | bool | D7 | — | M7, finales 1 y 2 | Ramas de la M7 | ✔ |
| `aurelio_conciencia` | 0–5 | D3, D5, ¿D9? | 3 + D9 (sin definir) | **Ninguno** | Ninguna | ✖ Decorativa; D5 puede dejarla en −1 |
| `aurelio_deserta` | bool | D10 | — | Epílogo, final 1 | Solo en el epílogo | ✔ |
| `custodia_archivo` | 0–100 | Fotos y testimonios (M1, M6, M9) | Sin escala de puntos | M9, epílogo de Custodia | Epílogo de Custodia | ⚠ Falta la escala |
| `custodia_publica` | 0–3 | D6 | 1 | **Ninguno** | Ninguna | ✖ Decorativa; rango inalcanzable |
| `lazos_puente_alto` | 0–3 | M6 · b2 (automático) | 1 | **Ninguno** | Ninguna | ✖ Decorativa; sin decisión |
| `prologo_escondio` | radio / periódico | DB | — | M2 b1–b3 | Pregunta por "el que lee" o celebración sin noticias | ✔ |
| `m2_se_llevo` | escopeta / libreta | DC | — | M3 b5, M4 b1 | Lo que encuentra Aurelio; Rosalba armada o no | ✔ |

## 3. Finales: condiciones

| Final | Condición en el doc 02 | Hueco |
|---|---|---|
| 1. Reconciliación frágil | `rosalba_desmovilizada` ∧ Rosalba sobrevive ∧ `aurelio_deserta` | "Sobrevive" no tiene condición |
| 2. Ciclo de venganza | Rosalba en armas ∧ `rosalba_represalia` alto | Umbral sin valor; destino de Aurelio sin definir |
| 3. Costo total | Muerte de uno o más personajes | Sin condición de activación |
| Coda de Custodia | Siempre; calidad según `custodia_archivo` | — |

Combinaciones sin final asignado:

| | Aurelio deserta | Aurelio se queda |
|---|---|---|
| **Rosalba desmovilizada** | Final 1 (si sobrevive) | **Sin final** |
| **Rosalba en armas** | Final 2 solo si represalia alta; Aurelio sin destino | Ídem |

## 4. Momentos guionizados de violencia (doc 02 §1 regla 1, 01-oct-2026)

Candidatos donde el jugador puede ejercer violencia contra civiles con control directo. Para
cada uno falta definir: qué controla el jugador, el coste narrativo visible y la variable.

| Momento | Situación | Falta |
|---|---|---|
| M4 · b4 | Prisionero (joven soldado boyacense) tras la emboscada | Si el prisionero se considera civil o combatiente rendido; coste visible |
| M5 · b2 | "Limpieza" del caserío; opción "avanzar con la columna" | Qué hace el jugador con control directo; coste visible al amanecer |
| M7 (en armas) | Robo a una familia campesina | Opciones y coste |

Aparte, M1 · b4: no es violencia del jugador, pero fotografiar el linchamiento de una persona
real (Roa Serna, doc 01) suma Archivo. Revisar el incentivo.

## 5. Huecos (para el registro, doc 10)

- **H1.** ~~El vertical slice (Prólogo + M2) no tiene decisiones.~~ Resuelto el 02-oct-2026 con P26–P28.
- **H2.** Cuatro variables sin consecuencia visible: `aurelio_conciencia`, `custodia_publica`, `lazos_puente_alto` y, hasta el epílogo, `rosalba_represalia`.
- **H3.** Rangos inalcanzables o mal acotados: `rosalba_represalia`, `custodia_publica`, `lazos_puente_alto`, `aurelio_conciencia` (bajo 0).
- **H4.** Finales sin condición y combinaciones sin final (§3).
- **H5.** Decisiones sin variable: D2, D9.
- **H6.** Sistemas mencionados y no definidos: "salud emocional" (D1), "riesgo" de publicar (D6), escala de `custodia_archivo`.
- **H7.** Momentos guionizados de violencia sin diseño (§4).
