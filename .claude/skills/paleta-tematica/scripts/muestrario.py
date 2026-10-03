#!/usr/bin/env python3
"""Genera la hoja de muestras (SVG) de una paleta temática.

Secciones: colores por familia (nombre, id, hex, OKLCH y estado de la fuente), guion de
color por acto (croma del mundo escalada) y prueba de reserva (pares declarados en
`distinguir` vistos con protanopía, deuteranopía, tritanopía y en grises).

Uso: python3 muestrario.py <paleta.json> <salida.svg> [--muestra id1,id2,...]
`--muestra` elige los colores de la franja del guion (por defecto, los 12 primeros de
registros que cambian más los reservados).
Para PNG, renderiza el SVG con cualquier motor (resvg, navegador).
"""

import json
import os
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from color import oklch_a_hex, simular  # noqa: E402

ANCHO = 1800
M = 48
SW, SH, GAP = 150, 84, 14
FUENTE = "Helvetica Neue, Helvetica, Arial, sans-serif"
VISTAS = (('normal', 'Normal'), ('protan', 'Protanopía'), ('deutan', 'Deuteranopía'),
          ('tritan', 'Tritanopía'), ('grises', 'Grises'))


def color_en_acto(paleta, c, acto):
    """Color de `c` en un acto del guion: el registro que cambia escala su croma."""
    L, C, h = c['oklch']
    cambia = paleta.get('registro_guion', 'iluminacion')
    if c['registro'] == cambia:
        return oklch_a_hex(L, C * acto['croma_mundo'], h)[0]
    if acto.get('partido') and c['registro'] == 'partido':
        variante = next((o for o in paleta['colores']
                         if o['id'].startswith(c['id'].split('-')[0]) and o['id'].endswith(acto['partido'])), None)
        if variante:
            return variante['hex']
    return c['hex']


def texto(x, y, s, tam=13, peso=400, color=None, ancla='start'):
    return (f'<text x="{x}" y="{y}" font-family="{FUENTE}" font-size="{tam}" font-weight="{peso}" '
            f'fill="{color}" text-anchor="{ancla}">{escape(str(s))}</text>')


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    paleta = json.load(open(sys.argv[1], encoding='utf-8'))
    colores = paleta['colores']
    for c in colores:
        c.setdefault('hex', oklch_a_hex(*c['oklch'])[0])
    por_id = {c['id']: c for c in colores}
    ui = paleta.get('roles_ui', {})
    fondo = por_id[ui.get('fondo', colores[0]['id'])]['hex']
    tinta = por_id[ui.get('texto', colores[-1]['id'])]['hex']
    suave = por_id[ui.get('texto-secundario', ui.get('texto', colores[-1]['id']))]['hex']

    out, y = [], M
    out.append(texto(M, y + 26, paleta.get('nombre', 'Paleta'), 30, 700, tinta))
    out.append(texto(M, y + 50, f"v{paleta.get('version', '')} · {paleta.get('estado', '')}", 14, 400, suave))
    y += 84

    familias = []
    for c in colores:
        if c['familia'] not in familias:
            familias.append(c['familia'])
    por_fila = (ANCHO - 2 * M + GAP) // (SW + GAP)
    for fam in familias:
        grupo = [c for c in colores if c['familia'] == fam]
        out.append(texto(M, y + 18, fam, 18, 700, tinta))
        y += 30
        for i, c in enumerate(grupo):
            fx = M + (i % por_fila) * (SW + GAP)
            fy = y + (i // por_fila) * (SH + 78)
            out.append(f'<rect x="{fx}" y="{fy}" width="{SW}" height="{SH}" fill="{c["hex"]}" stroke="{tinta}" stroke-width="1.5"/>')
            out.append(texto(fx, fy + SH + 17, c.get('nombre', c['id']), 13, 700, tinta))
            out.append(texto(fx, fy + SH + 33, c['id'], 11, 400, suave))
            L, C, h = c['oklch']
            out.append(texto(fx, fy + SH + 48, f"{c['hex']} · {L:.2f} {C:.3f} {h:.0f}°", 11, 400, suave))
            out.append(texto(fx, fy + SH + 63, f"[{c.get('estado', '?')}] {c['registro']}", 11, 400, suave))
        y += ((len(grupo) - 1) // por_fila + 1) * (SH + 78) + 16

    guion = paleta.get('guion', [])
    if guion:
        ids = None
        if '--muestra' in sys.argv:
            ids = sys.argv[sys.argv.index('--muestra') + 1].split(',')
        muestra = [por_id[i] for i in ids] if ids else colores[:12]
        out.append(texto(M, y + 22, 'Guion de color', 22, 700, tinta))
        y += 40
        cw = (ANCHO - 2 * M - 360) // len(muestra)
        for acto in guion:
            out.append(texto(M, y + 22, acto['acto'], 14, 700, tinta))
            out.append(texto(M, y + 40, f"{acto.get('anios', '')} · croma del mundo ×{acto['croma_mundo']}", 12, 400, suave))
            for i, c in enumerate(muestra):
                out.append(f'<rect x="{M + 360 + i * cw}" y="{y}" width="{cw}" height="56" fill="{color_en_acto(paleta, c, acto)}"/>')
            y += 66
        out.append(''.join(texto(M + 360 + i * cw + 4, y + 12, c['id'], 10, 400, suave) for i, c in enumerate(muestra)))
        y += 34

    pares = paleta.get('distinguir', [])
    if pares:
        out.append(texto(M, y + 22, 'Reserva y daltonismo (pares que deben distinguirse)', 22, 700, tinta))
        y += 40
        col = (ANCHO - 2 * M - 300) // len(VISTAS)
        for j, (_, nombre) in enumerate(VISTAS):
            out.append(texto(M + 300 + j * col, y + 12, nombre, 13, 700, tinta))
        y += 22
        for par in pares:
            a, b = por_id[par['a']]['hex'], por_id[par['b']]['hex']
            out.append(texto(M, y + 26, f"{par['a']} / {par['b']}", 13, 400, tinta))
            for j, (v, _) in enumerate(VISTAS):
                va, vb = (a, b) if v == 'normal' else (simular(a, v), simular(b, v))
                x0 = M + 300 + j * col
                out.append(f'<rect x="{x0}" y="{y}" width="{col // 2 - 10}" height="40" fill="{va}"/>')
                out.append(f'<rect x="{x0 + col // 2 - 10}" y="{y}" width="{col // 2 - 10}" height="40" fill="{vb}"/>')
            y += 50
        y += 10

    alto = y + M
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{ANCHO}" height="{alto}" viewBox="0 0 {ANCHO} {alto}">'
           f'<rect width="{ANCHO}" height="{alto}" fill="{fondo}"/>' + ''.join(out) + '</svg>')
    open(sys.argv[2], 'w', encoding='utf-8').write(svg)
    print(f'{sys.argv[2]}: {len(colores)} colores, {ANCHO}×{alto}')


if __name__ == '__main__':
    main()
