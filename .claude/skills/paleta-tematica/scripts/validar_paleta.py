#!/usr/bin/env python3
"""Valida una paleta temática (JSON, esquema en references/esquema-paleta.md).

Comprueba: gamut sRGB, techo de croma y rango de tono por registro, zonas de tono
reservadas, contrastes WCAG declarados y que los pares declarados (y cada color
reservado frente al resto) sigan distinguiéndose con protanopía, deuteranopía,
tritanopía y en grises. Con --escribir guarda el hex calculado en el JSON.

Uso: python3 validar_paleta.py <paleta.json> [--escribir] [--informe salida.md]
Sale con código 1 si alguna regla falla.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from color import contraste, delta_ok, oklch_a_hex, simular, tono_en  # noqa: E402

VISTAS = ('normal', 'protan', 'deutan', 'tritan', 'grises')


def distancia(h1, h2, vista):
    if vista == 'normal':
        return delta_ok(h1, h2)
    return delta_ok(simular(h1, vista), simular(h2, vista))


def validar(paleta):
    fallos, avisos, filas = [], [], []
    registros = paleta.get('registros', {})
    zonas = paleta.get('zonas_reservadas', [])
    colores = {}
    for c in paleta['colores']:
        L, C, h = c['oklch']
        hx, c_usada = oklch_a_hex(L, C, h)
        c['hex'] = hx
        colores[c['id']] = c
        if C - c_usada > 0.005:
            avisos.append(f"`{c['id']}`: croma {C} fuera de sRGB; se usa {c_usada:.3f}")
        reg = registros.get(c['registro'])
        if reg is None:
            fallos.append(f"`{c['id']}`: registro desconocido `{c['registro']}`")
            continue
        if 'croma_max' in reg and C > reg['croma_max'] + 1e-9:
            fallos.append(f"`{c['id']}`: croma {C} supera el techo {reg['croma_max']} del registro `{c['registro']}`")
        if 'tono' in reg and C > 0.02 and not tono_en(h, reg['tono']):
            fallos.append(f"`{c['id']}`: tono {h}° fuera del rango {reg['tono']} del registro `{c['registro']}`")
        for z in zonas:
            if c['registro'] in z['registros_permitidos']:
                continue
            if tono_en(h, z['tono']) and C >= z['croma_min']:
                fallos.append(f"`{c['id']}` invade la zona reservada `{z['id']}` (tono {h}°, croma {C})")
        filas.append(f"| `{c['id']}` | {c['registro']} | {hx} | {L:.3f} {C:.3f} {h:.0f} |")

    for par in paleta.get('contrastes', []):
        a, b = colores[par['texto']]['hex'], colores[par['fondo']]['hex']
        r = contraste(a, b)
        linea = f"`{par['texto']}` sobre `{par['fondo']}`: {r:.2f} (mín. {par['min']})"
        (fallos if r < par['min'] else avisos if r < par['min'] * 1.1 else [])\
            .append(linea + (' — justo' if r >= par['min'] else ''))
        par['_r'] = r

    minimo = paleta.get('distancia_min', 0.05)
    distinguir = []
    for par in paleta.get('distinguir', []):
        a, b = colores[par['a']]['hex'], colores[par['b']]['hex']
        ds = {v: distancia(a, b, v) for v in VISTAS}
        peor = min(ds, key=ds.get)
        lim = par.get('min', minimo)
        distinguir.append((par, ds, peor))
        if ds[peor] < lim:
            fallos.append(f"`{par['a']}` y `{par['b']}` se confunden en {peor}: ΔOK {ds[peor]:.3f} < {lim}")

    # Cada color de un registro reservado frente a todos los demás. Sin la vista en grises:
    # en grises siempre habrá algún color del mundo con la misma luz; eso se controla con
    # los pares declarados en `distinguir`, que son los que de verdad se tocan en escena.
    reservados = {r for z in zonas for r in z['registros_permitidos']}
    umbral = paleta.get('distancia_reserva_min', 0.04)
    otros = [o for o in paleta['colores'] if o['registro'] not in reservados]
    vecinos = []
    for c in paleta['colores']:
        if c['registro'] not in reservados:
            continue
        for v in VISTAS[:-1]:
            mas_cerca = min(otros, key=lambda o: distancia(c['hex'], o['hex'], v))
            d = distancia(c['hex'], mas_cerca['hex'], v)
            vecinos.append((c['id'], v, mas_cerca['id'], d))
            if d < umbral:
                avisos.append(f"`{c['id']}` queda a ΔOK {d:.3f} de `{mas_cerca['id']}` en {v}")
    return fallos, avisos, filas, distinguir, vecinos


def informe(paleta, fallos, avisos, filas, distinguir, vecinos):
    out = [f"# Validación — {paleta.get('nombre', 'paleta')}", '']
    out.append(f"**Resultado:** {'FALLA' if fallos else 'OK'} · {len(paleta['colores'])} colores · "
               f"{len(fallos)} fallos · {len(avisos)} avisos")
    out += ['', '## Fallos', ''] + ([f'- {x}' for x in fallos] or ['- Ninguno'])
    out += ['', '## Avisos', ''] + ([f'- {x}' for x in avisos] or ['- Ninguno'])
    out += ['', '## Contrastes (WCAG 2.x)', '', '| Texto | Fondo | Razón | Mínimo |', '|---|---|---|---|']
    out += [f"| `{p['texto']}` | `{p['fondo']}` | {p['_r']:.2f} | {p['min']} |" for p in paleta.get('contrastes', [])]
    out += ['', '## Pares que deben distinguirse (ΔOK por vista)', '',
            '| A | B | ' + ' | '.join(VISTAS) + ' |', '|---|---|' + '---|' * len(VISTAS)]
    for par, ds, peor in distinguir:
        celdas = [f"**{ds[v]:.3f}**" if v == peor else f"{ds[v]:.3f}" for v in VISTAS]
        out.append(f"| `{par['a']}` | `{par['b']}` | " + ' | '.join(celdas) + ' |')
    out += ['', '## Vecino más cercano de cada color reservado', '', '| Color | Vista | Vecino | ΔOK |', '|---|---|---|---|']
    out += [f'| `{a}` | {v} | `{b}` | {d:.3f} |' for a, v, b, d in vecinos]
    out += ['', '## Colores', '', '| Id | Registro | Hex | OKLCH |', '|---|---|---|---|'] + filas
    return '\n'.join(out) + '\n'


def actualizar_hex(texto, paleta):
    """Cambia solo el valor de "hex" de cada color, sin tocar el formato del archivo.

    Devuelve None si algún color no tiene todavía la clave "hex" en el texto.
    """
    import re
    for c in paleta['colores']:
        patron = re.compile(r'("id":\s*"' + re.escape(c['id']) + r'"[^{}]*?"hex":\s*")#[0-9a-fA-F]{6}(")', re.S)
        texto, n = patron.subn(lambda m: m.group(1) + c['hex'] + m.group(2), texto, count=1)
        if n == 0:
            return None
    return texto


def json_compacto(paleta):
    """JSON legible: claves de primer nivel en líneas propias y un elemento de lista por línea."""
    def uno(v):
        return json.dumps(v, ensure_ascii=False)
    partes = []
    for k, v in paleta.items():
        if isinstance(v, list):
            cuerpo = ',\n'.join(f'    {uno(x)}' for x in v)
            partes.append(f'  {uno(k)}: [\n{cuerpo}\n  ]')
        elif isinstance(v, dict):
            cuerpo = ',\n'.join(f'    {uno(kk)}: {uno(vv)}' for kk, vv in v.items())
            partes.append(f'  {uno(k)}: {{\n{cuerpo}\n  }}')
        else:
            partes.append(f'  {uno(k)}: {uno(v)}')
    return '{\n' + ',\n'.join(partes) + '\n}'


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    ruta = sys.argv[1]
    paleta = json.load(open(ruta, encoding='utf-8'))
    fallos, avisos, filas, distinguir, vecinos = validar(paleta)
    texto = informe(paleta, fallos, avisos, filas, distinguir, vecinos)
    if '--informe' in sys.argv:
        open(sys.argv[sys.argv.index('--informe') + 1], 'w', encoding='utf-8').write(texto)
    else:
        print(texto)
    if '--escribir' in sys.argv:
        for par in paleta.get('contrastes', []):
            par.pop('_r', None)
        original = open(ruta, encoding='utf-8').read()
        nuevo = actualizar_hex(original, paleta)
        if nuevo is None:  # algún color aún sin "hex": se reescribe el archivo entero
            nuevo = json_compacto(paleta) + '\n'
            print('Archivo reescrito: si el proyecto formatea JSON (Biome, Prettier), formatéalo ahora.', file=sys.stderr)
        if nuevo != original:
            with open(ruta, 'w', encoding='utf-8') as fh:
                fh.write(nuevo)
    print(f"{'FALLA' if fallos else 'OK'}: {len(fallos)} fallos, {len(avisos)} avisos", file=sys.stderr)
    sys.exit(1 if fallos else 0)


if __name__ == '__main__':
    main()
