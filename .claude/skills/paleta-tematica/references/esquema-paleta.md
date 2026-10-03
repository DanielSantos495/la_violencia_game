# Esquema del JSON de paleta

Un archivo por paleta. Ejemplo real: `game/art/paleta.json`.

| Clave | Tipo | Para qué |
|---|---|---|
| `nombre`, `version`, `estado`, `documento` | texto | Identificación y ruta de la hoja que explica las decisiones |
| `distancia_min` | número (ΔOK) | Mínimo por defecto para los pares de `distinguir` (0,05 ≈ distinguible con claridad) |
| `distancia_reserva_min` | número (ΔOK) | Umbral del aviso "vecino más cercano" de los colores reservados (por defecto 0,04) |
| `registros` | objeto | `id → {croma_max?, tono?: [ini, fin], descripcion}`. Cada color pertenece a uno |
| `zonas_reservadas` | lista | `{id, tono: [ini, fin], croma_min, registros_permitidos: [...]}`. Un rango de tono puede cruzar 0° (`[350, 20]`) |
| `colores` | lista | Ver abajo |
| `roles_ui` | objeto | `rol → id de color` (texto, fondo, selección…). La UI consume roles, no hex |
| `contrastes` | lista | `{texto, fondo, min, uso}` con ids; `min` es la razón WCAG (4,5 texto normal, 3 texto grande y no texto, 7 AAA) |
| `distinguir` | lista | `{a, b, min?, motivo}`: pares que se tocan en escena y deben separarse en las cinco vistas |
| `registro_guion` | texto | Registro cuyo croma escala el guion (por defecto `iluminacion`) |
| `guion` | lista | `{id, acto, anios, croma_mundo, partido?, nota}`. `partido: "desvaido"` cambia cada color reservado por su variante `<prefijo>-desvaido` |

## Color

```json
{"id": "trigo", "familia": "Boyacá: campo", "registro": "iluminacion",
 "oklch": [0.83, 0.075, 88], "hex": "#dcc58f",
 "nombre": "Trigo", "uso": "Sembrados de trigo maduro",
 "fuente": "Álvarez y Chaves, Rev. Colomb. Cienc. Agríc. 34(2)", "estado": "V"}
```

- `oklch`: `[L 0–1, C ≥ 0, h en grados]`. Es la fuente; `hex` lo escribe el validador con `--escribir`.
- `id`: kebab-case estable. El código y los generadores lo usan: no se renombra sin avisar.
- `estado`: `V` (con fuente), `P` (por verificar; no entra como final), `D` (decisión de diseño).

## Ejemplo mínimo

```json
{
  "nombre": "Ejemplo",
  "registros": {
    "papel": {"croma_max": 0.04},
    "mundo": {"croma_max": 0.08},
    "bando": {}
  },
  "zonas_reservadas": [
    {"id": "rojo-bando", "tono": [5, 45], "croma_min": 0.1, "registros_permitidos": ["bando"]}
  ],
  "colores": [
    {"id": "papel", "familia": "Papel", "registro": "papel", "oklch": [0.93, 0.03, 88]},
    {"id": "tinta", "familia": "Tinta", "registro": "papel", "oklch": [0.21, 0.012, 60]},
    {"id": "teja", "familia": "Mundo", "registro": "mundo", "oklch": [0.62, 0.075, 50]},
    {"id": "rojo", "familia": "Bando", "registro": "bando", "oklch": [0.55, 0.195, 29]}
  ],
  "roles_ui": {"fondo": "papel", "texto": "tinta"},
  "contrastes": [{"texto": "tinta", "fondo": "papel", "min": 7}],
  "distinguir": [{"a": "rojo", "b": "teja"}],
  "guion": [{"id": "inicio", "acto": "Inicio", "croma_mundo": 1.0},
            {"id": "final", "acto": "Final", "croma_mundo": 0.3}],
  "registro_guion": "mundo"
}
```
