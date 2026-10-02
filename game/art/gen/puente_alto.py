"""Generador de los fondos de la plaza de Puente Alto (game/art/src/fondos/puente-alto/*.svg).

Mañana de mercado, mayo–junio de 1946 (doc 02 §5, prólogo). Puente Alto es ficticio (doc 01):
se compone a partir de tipologías del norte de Boyacá, sin copiar un pueblo real.
Escala y capas: planeacion/arte/tomo1/escenarios/contrato_escala.md (200 px/m en el plano de
juego; cada capa a 200 × paralaje). Fuentes y [V]/[P]: planeacion/arte/tomo1/escenarios/puente-alto.md.
Color: paleta del juego (game/art/paleta.json; planeacion/arte/tomo1/paleta.md).

  python3 art/gen/puente_alto.py        (desde game/; sin dependencias)

Edita este script, no los SVG generados.
"""
import json
import math
import os
import random
import re
import sys

OUTDIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'fondos', 'puente-alto')

# Paleta del juego (game/art/paleta.json; reglas y fuentes en planeacion/arte/tomo1/paleta.md). El mundo
# es una foto iluminada a mano: lavados apagados bajo la tinta y la trama. Solo el rojo y el azul de los
# partidos van enteros, planos como tinta de imprenta, y no se diluyen con la distancia (paleta.md §6).
PALETA = {c['id']: c['hex'] for c in json.load(open(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'paleta.json'), encoding='utf-8'))['colores']}
ROJO, AZUL = PALETA['rojo-liberal'], PALETA['azul-conservador']
PAPEL, TINTA, GRAFITO, GRIS_TRAMA = PALETA['papel'], PALETA['tinta'], PALETA['grafito'], PALETA['gris-trama']


def _a_oklab(hexa):
    r, g, b = (int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5))
    r, g, b = (c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b))
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def _de_oklab(L, a, b):
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
           -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
           -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_)
    srgb = (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055 for c in (max(0.0, min(1.0, v)) for v in rgb))
    return '#' + ''.join(f'{round(c * 255):02x}' for c in srgb)


def diluir(hexa, k):
    """Lavado más aguado: mezcla en OKLab con el papel (k=1 el color tal cual, k=0 papel)."""
    a, b = _a_oklab(PAPEL), _a_oklab(hexa)
    return _de_oklab(*(x + (y - x) * k for x, y in zip(a, b)))


def lav(token, m, luz=1.0):
    """Lavado de un color del mundo (registro iluminacion) con perspectiva aérea (paleta.md §6.4):
    cuanto menos px/m, más lejos y más papel. luz < 1 aclara la cara al sol. Lo partidista no pasa
    por aquí: va entero en cualquier capa."""
    return diluir(PALETA[token], (0.35 + 0.65 * min(1.0, m / 200) ** 0.6) * luz)

PARALAJE = {'cielo': 0, 'lejos': 0.15, 'medio': 0.45, 'juego': 1.0, 'frente': 1.3}
# Trazo base por capa: grueso cerca, fino lejos (doc 03 §1). Lo lejano se entinta en grafito (paleta.md §6.4).
TRAZO = {'cielo': 1.0, 'lejos': 1.1, 'medio': 1.7, 'juego': 2.6, 'frente': 3.6}
LINEA = {'cielo': GRAFITO, 'lejos': GRAFITO, 'medio': TINTA, 'juego': TINTA, 'frente': TINTA}


def ppm(capa):
    return 200 * PARALAJE[capa]


def f(x):
    return f"{x:.1f}".rstrip('0').rstrip('.')


def pts(lista):
    return ' '.join(f"{f(x)},{f(y)}" for x, y in lista)


def tramas(esc=1.0):
    """Tramas compartidas por todos los módulos: la cohesión empieza aquí."""
    s = esc
    return f'''
  <defs>
    <pattern id="t-fina" width="{f(6*s)}" height="{f(6*s)}" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="{f(6*s)}" stroke="#000" stroke-width="{f(0.7*s)}"/></pattern>
    <pattern id="t-media" width="{f(3.6*s)}" height="{f(3.6*s)}" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="{f(3.6*s)}" stroke="#000" stroke-width="{f(0.9*s)}"/></pattern>
    <pattern id="t-cruz" width="{f(4*s)}" height="{f(4*s)}" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="{f(4*s)}" stroke="#000" stroke-width="{f(0.9*s)}"/><line x1="0" y1="0" x2="{f(4*s)}" y2="0" stroke="#000" stroke-width="{f(0.9*s)}"/></pattern>
    <pattern id="t-densa" width="{f(2.8*s)}" height="{f(2.8*s)}" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><line x1="0" y1="0" x2="0" y2="{f(2.8*s)}" stroke="#000" stroke-width="{f(1.2*s)}"/><line x1="0" y1="0" x2="{f(2.8*s)}" y2="0" stroke="#000" stroke-width="{f(1*s)}"/></pattern>
    <pattern id="t-horiz" width="{f(8*s)}" height="{f(4*s)}" patternUnits="userSpaceOnUse"><line x1="0" y1="{f(2*s)}" x2="{f(8*s)}" y2="{f(2*s)}" stroke="#000" stroke-width="{f(0.8*s)}"/></pattern>
    <pattern id="t-vert" width="{f(4*s)}" height="{f(8*s)}" patternUnits="userSpaceOnUse"><line x1="{f(2*s)}" y1="0" x2="{f(2*s)}" y2="{f(8*s)}" stroke="#000" stroke-width="{f(0.8*s)}"/></pattern>
    <pattern id="t-puntos" width="{f(4*s)}" height="{f(4*s)}" patternUnits="userSpaceOnUse"><circle cx="{f(2*s)}" cy="{f(2*s)}" r="{f(0.75*s)}" fill="#000"/></pattern>
    <pattern id="t-puntos-ralos" width="{f(7*s)}" height="{f(7*s)}" patternUnits="userSpaceOnUse"><circle cx="{f(2*s)}" cy="{f(2*s)}" r="{f(0.7*s)}" fill="#000"/><circle cx="{f(5.5*s)}" cy="{f(5.5*s)}" r="{f(0.6*s)}" fill="#000"/></pattern>
    <pattern id="t-madera" width="{f(40*s)}" height="{f(6*s)}" patternUnits="userSpaceOnUse"><path d="M0,{f(3*s)} C{f(10*s)},{f(2*s)} {f(20*s)},{f(4*s)} {f(40*s)},{f(3*s)}" stroke="#000" stroke-width="{f(0.6*s)}" fill="none"/></pattern>
    <pattern id="t-tejido" width="{f(6.5*s)}" height="{f(6.5*s)}" patternUnits="userSpaceOnUse"><path d="M0,{f(3.2*s)} H{f(6.5*s)} M{f(3.2*s)},0 V{f(6.5*s)}" stroke="#000" stroke-width="{f(0.4*s)}"/></pattern>
    <pattern id="t-madera-v" width="{f(6*s)}" height="{f(40*s)}" patternUnits="userSpaceOnUse"><path d="M{f(3*s)},0 C{f(2*s)},{f(10*s)} {f(4*s)},{f(20*s)} {f(3*s)},{f(40*s)}" stroke="#000" stroke-width="{f(0.6*s)}" fill="none"/></pattern>
  </defs>'''


def archivo(nombre, w, h, capa, titulo, cuerpo, notas='', esc_trama=1.0):
    contenido = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{f(w)}" height="{f(h)}" viewBox="0 0 {f(w)} {f(h)}">
  <!--
    Puente Alto · {titulo}
    Capa: {capa} (paralaje {PARALAJE[capa]}, {f(ppm(capa))} px/m). La base del viewBox es el suelo de la capa
    salvo que el módulo se coloque por arriba (cielo, mosaicos de suelo).
    {notas}
    Colores: paleta del juego (game/art/paleta.json, planeacion/arte/tomo1/paleta.md): lavados bajo la
    línea ({'tinta' if LINEA[capa] == TINTA else 'grafito'}), rojo y azul enteros.
    GENERADO por game/art/gen/puente_alto.py: edita el script, no este archivo.
  -->{tramas(esc_trama)}
{cuerpo}
</svg>
'''
    # Se dibuja en negro y blanco; al guardar, la línea (y la trama) pasan a la tinta de la capa y
    # las luces que quedan en blanco, al papel.
    contenido = re.sub(r'"#000"', f'"{LINEA[capa]}"', contenido)
    contenido = re.sub(r'"#fff"', f'"{PAPEL}"', contenido)
    ruta = os.path.join(OUTDIR, nombre + '.svg')
    os.makedirs(OUTDIR, exist_ok=True)
    with open(ruta, 'w') as fh:
        fh.write(contenido)
    print('ok', nombre, f'{f(w)}x{f(h)}')


# ============================== vocabulario de arquitectura ==============================

def tejado_frente(x0, x1, y_borde, y_arriba, m, sw, rnd, oscuro=True):
    """Tejado de barro visto desde la plaza: plano con canales de teja y borde festoneado."""
    paso = 0.24 * m  # ancho de una teja (canal + cobija)
    alto = y_borde - y_arriba
    teja, teja_sol = lav('teja', m), lav('teja', m, 0.85)
    out = [f'<rect x="{f(x0)}" y="{f(y_arriba)}" width="{f(x1-x0)}" height="{f(alto)}" fill="{teja}"/>']
    # canales en sombra entre las cobijas; arriba, el tejado se aleja y se oscurece
    out.append(f'<rect x="{f(x0)}" y="{f(y_arriba)}" width="{f(x1-x0)}" height="{f(alto)}" fill="url(#t-media)"/>')
    if oscuro:
        out.append(f'<rect x="{f(x0)}" y="{f(y_arriba)}" width="{f(x1-x0)}" height="{f(alto*0.45)}" fill="url(#t-fina)"/>')
    # cobijas: lomos convexos con su sombra a la derecha; canales: surcos entre ellas
    x = x0
    while x < x1:
        dx = rnd.uniform(-0.03, 0.03) * m
        xc = x + paso * 0.5
        lomo = (f'M{f(xc-paso*0.3+dx)},{f(y_arriba)} L{f(xc-paso*0.3)},{f(y_borde-0.08*m)} '
                f'Q{f(xc)},{f(y_borde-0.16*m)} {f(xc+paso*0.3)},{f(y_borde-0.08*m)} L{f(xc+paso*0.3+dx)},{f(y_arriba)} Z')
        out.append(f'<path d="{lomo}" fill="{teja_sol}" stroke="#000" stroke-width="{f(sw*0.45)}"/>')
        out.append(f'<path d="M{f(xc+paso*0.08+dx)},{f(y_arriba)} L{f(xc+paso*0.08)},{f(y_borde-0.12*m)} L{f(xc+paso*0.3)},{f(y_borde-0.08*m)} L{f(xc+paso*0.3+dx)},{f(y_arriba)} Z" fill="url(#t-media)"/>')
        # juntas entre piezas de teja a lo largo del lomo
        for k in range(1, 6):
            yy = y_arriba + alto * k / 6 + rnd.uniform(-0.03, 0.03) * m
            if yy < y_borde - 0.2 * m:
                out.append(f'<path d="M{f(xc-paso*0.3)},{f(yy)} Q{f(xc)},{f(yy-0.05*m)} {f(xc+paso*0.3)},{f(yy)}" stroke="#000" stroke-width="{f(sw*0.35)}" fill="none"/>')
        x += paso
    # bocas de las cobijas en el borde: medias lunas oscuras
    x = x0
    bocas = []
    while x < x1:
        xc = x + paso * 0.5
        r = paso * 0.3
        bocas.append(f'M{f(xc-r)},{f(y_borde-0.08*m)} Q{f(xc)},{f(y_borde-0.08*m-r*1.1)} {f(xc+r)},{f(y_borde-0.08*m)} Q{f(xc)},{f(y_borde-0.08*m-r*0.35)} {f(xc-r)},{f(y_borde-0.08*m)} Z')
        x += paso
    out.append(f'<path d="{" ".join(bocas)}" fill="#000"/>')
    out.append(f'<rect x="{f(x0)}" y="{f(y_borde-0.08*m)}" width="{f(x1-x0)}" height="{f(0.08*m)}" fill="{teja}" stroke="#000" stroke-width="{f(sw*0.7)}"/>')
    out.append(f'<rect x="{f(x0)}" y="{f(y_borde-0.08*m)}" width="{f(x1-x0)}" height="{f(0.08*m)}" fill="url(#t-vert)"/>')
    out.append(f'<line x1="{f(x0)}" y1="{f(y_borde)}" x2="{f(x1)}" y2="{f(y_borde)}" stroke="#000" stroke-width="{f(sw*1.2)}"/>')
    return ''.join(out)


def alero(x0, x1, y_viga, m, sw, rnd):
    """Alero con canecillos de madera bajo el borde de la teja, y viga del corredor."""
    out = []
    y_tablazon = y_viga - 0.32 * m
    # tablazón bajo el alero (sombra)
    out.append(f'<rect x="{f(x0)}" y="{f(y_tablazon)}" width="{f(x1-x0)}" height="{f(0.2*m)}" fill="#000"/>')
    out.append(f'<line x1="{f(x0)}" y1="{f(y_tablazon+0.03*m)}" x2="{f(x1)}" y2="{f(y_tablazon+0.03*m)}" stroke="#fff" stroke-width="{f(sw*0.35)}"/>')
    # canecillos: cabezas de vigueta talladas, con cara en sombra
    paso = 0.5 * m
    x = x0 + 0.12 * m
    canes = []
    while x < x1 - 0.12 * m:
        w = 0.13 * m
        y0 = y_tablazon + 0.04 * m
        cab = (f'M{f(x)},{f(y0)} L{f(x+w)},{f(y0)} L{f(x+w)},{f(y0+0.16*m)} '
               f'Q{f(x+w)},{f(y0+0.26*m)} {f(x+w*0.55)},{f(y0+0.26*m)} Q{f(x+w*0.2)},{f(y0+0.26*m)} {f(x+w*0.2)},{f(y0+0.19*m)} '
               f'Q{f(x)},{f(y0+0.19*m)} {f(x)},{f(y0+0.12*m)} Z')
        canes.append(f'<path d="{cab}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
        canes.append(f'<path d="M{f(x+w*0.62)},{f(y0)} L{f(x+w)},{f(y0)} L{f(x+w)},{f(y0+0.16*m)} Q{f(x+w)},{f(y0+0.26*m)} {f(x+w*0.62)},{f(y0+0.255*m)} Z" fill="url(#t-media)"/>')
        x += paso
    out.extend(canes)
    # viga
    out.append(f'<rect x="{f(x0)}" y="{f(y_viga-0.12*m)}" width="{f(x1-x0)}" height="{f(0.14*m)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw*0.8)}"/>')
    out.append(f'<rect x="{f(x0)}" y="{f(y_viga-0.12*m)}" width="{f(x1-x0)}" height="{f(0.14*m)}" fill="url(#t-madera)"/>')
    return ''.join(out)


def pilar(x, y_piso, y_viga, m, sw, color=None):
    """Pie derecho de madera sobre basa de piedra, con zapata bajo la viga."""
    w = 0.2 * m
    basa_h, basa_w = 0.3 * m, 0.34 * m
    zap_w, zap_h = 0.7 * m, 0.15 * m
    relleno = color or lav('madera', m, 0.55)
    piedra = lav('piedra', m)
    alto_fuste = y_piso - basa_h - y_viga
    out = [
        # fuste de madera: veta, cara en sombra y una grieta
        f'<rect x="{f(x-w/2)}" y="{f(y_viga+0.02*m)}" width="{f(w)}" height="{f(alto_fuste)}" fill="{relleno}" stroke="#000" stroke-width="{f(sw*0.9)}"/>',
        f'<rect x="{f(x-w/2)}" y="{f(y_viga+0.02*m)}" width="{f(w)}" height="{f(alto_fuste)}" fill="url(#t-madera-v)"/>',
        f'<rect x="{f(x+w*0.12)}" y="{f(y_viga+0.02*m)}" width="{f(w*0.38)}" height="{f(alto_fuste)}" fill="url(#t-cruz)"/>',
        f'<path d="M{f(x-w*0.22)},{f(y_viga+0.35*m)} L{f(x-w*0.18)},{f(y_viga+0.8*m)} L{f(x-w*0.24)},{f(y_viga+1.1*m)}" stroke="#000" stroke-width="{f(sw*0.45)}" fill="none"/>',
        # zapata
        f'<path d="M{f(x-zap_w/2)},{f(y_viga+0.02*m)} L{f(x+zap_w/2)},{f(y_viga+0.02*m)} L{f(x+zap_w/2)},{f(y_viga+0.06*m)} Q{f(x+zap_w/2-0.08*m)},{f(y_viga+zap_h)} {f(x+w/2)},{f(y_viga+zap_h)} L{f(x-w/2)},{f(y_viga+zap_h)} Q{f(x-zap_w/2+0.08*m)},{f(y_viga+zap_h)} {f(x-zap_w/2)},{f(y_viga+0.06*m)} Z" fill="{relleno}" stroke="#000" stroke-width="{f(sw*0.7)}"/>',
        f'<path d="M{f(x-zap_w/2)},{f(y_viga+0.02*m)} L{f(x+zap_w/2)},{f(y_viga+0.02*m)} L{f(x+zap_w/2)},{f(y_viga+0.06*m)} Q{f(x+zap_w/2-0.08*m)},{f(y_viga+zap_h)} {f(x+w/2)},{f(y_viga+zap_h)} L{f(x-w/2)},{f(y_viga+zap_h)} Q{f(x-zap_w/2+0.08*m)},{f(y_viga+zap_h)} {f(x-zap_w/2)},{f(y_viga+0.06*m)} Z" fill="url(#t-madera)"/>',
        # basa de piedra
        f'<path d="M{f(x-basa_w/2)},{f(y_piso)} L{f(x-basa_w/2+0.03*m)},{f(y_piso-basa_h)} L{f(x+basa_w/2-0.03*m)},{f(y_piso-basa_h)} L{f(x+basa_w/2)},{f(y_piso)} Z" fill="{piedra}" stroke="#000" stroke-width="{f(sw*0.8)}"/>',
        f'<path d="M{f(x)},{f(y_piso-basa_h)} L{f(x+basa_w/2)},{f(y_piso)} L{f(x+basa_w/2-0.08*m)},{f(y_piso)} Z" fill="url(#t-media)"/>',
    ]
    return ''.join(out)


def muro_cal(x0, x1, y_arriba, y_abajo, m, sw, rnd, grietas=4, desconchados=3):
    """Tapia encalada: blanco con grietas finas y desconchados donde asoma la tierra (doc 03 §3.1 [V])."""
    out = [f'<rect x="{f(x0)}" y="{f(y_arriba)}" width="{f(x1-x0)}" height="{f(y_abajo-y_arriba)}" fill="{lav("cal", m)}" stroke="#000" stroke-width="{f(sw)}"/>']
    # juntas de los cajones del tapial, apenas visibles bajo la cal
    y = y_abajo - 0.85 * m
    while y > y_arriba + 0.3 * m:
        out.append(f'<line x1="{f(x0)}" y1="{f(y)}" x2="{f(x1)}" y2="{f(y+rnd.uniform(-0.02,0.02)*m)}" stroke="#000" stroke-width="{f(sw*0.25)}" stroke-dasharray="{f(0.5*m)} {f(0.12*m)} {f(0.2*m)} {f(0.25*m)}" opacity="0.7"/>')
        y -= 0.85 * m
    # humedad que sube del suelo y polvo bajo el alero
    out.append(f'<rect x="{f(x0)}" y="{f(y_abajo-0.45*m)}" width="{f(x1-x0)}" height="{f(0.45*m)}" fill="url(#t-puntos-ralos)" opacity="0.8"/>')
    for _ in range(grietas):
        x = rnd.uniform(x0 + 0.3 * m, x1 - 0.3 * m)
        y = rnd.uniform(y_arriba + 0.2 * m, y_abajo - 0.8 * m)
        d = f'M{f(x)},{f(y)}'
        for _ in range(4):
            x += rnd.uniform(-0.08, 0.08) * m
            y += rnd.uniform(0.06, 0.16) * m
            d += f' L{f(x)},{f(y)}'
        out.append(f'<path d="{d}" stroke="#000" stroke-width="{f(sw*0.3)}" fill="none"/>')
    for _ in range(desconchados):
        # la cal saltada deja ver la tierra de la tapia: mancha pequeña, oscura y de borde roto
        cx = rnd.uniform(x0 + 0.5 * m, x1 - 0.5 * m)
        cy = rnd.uniform(y_arriba + 0.3 * m, y_abajo - 0.5 * m)
        r = rnd.uniform(0.06, 0.16) * m
        pts_ = []
        for k in range(12):
            a = k * 2 * math.pi / 12
            rr = r * rnd.uniform(0.45, 1.2)
            pts_.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.55))
        out.append(f'<polygon points="{pts(pts_)}" fill="{lav("tapia", m)}" stroke="#000" stroke-width="{f(sw*0.3)}"/>'
                   f'<polygon points="{pts(pts_)}" fill="url(#t-fina)"/>')
    return ''.join(out)


def zocalo(x0, x1, y_abajo, alto, m, sw, rnd, color=None):
    """Zócalo de la fachada: franja baja pintada, gastada (color de tienda partidista o trama)."""
    y = y_abajo - alto
    # sin partido, la tapia queda a la vista; con partido, pintura plana (paleta.md §6.1)
    out = [f'<rect x="{f(x0)}" y="{f(y)}" width="{f(x1-x0)}" height="{f(alto)}" fill="{color or lav("tapia", m)}" stroke="#000" stroke-width="{f(sw*0.8)}"/>']
    if not color:
        out.append(f'<rect x="{f(x0)}" y="{f(y)}" width="{f(x1-x0)}" height="{f(alto)}" fill="url(#t-fina)"/>')
    # borde superior pintado a mano, irregular
    borde = f'M{f(x0)},{f(y)}'
    x = x0
    while x < x1:
        x += rnd.uniform(0.25, 0.6) * m
        borde += f' L{f(min(x, x1))},{f(y + rnd.uniform(-0.015, 0.015) * m)}'
    out.append(f'<path d="{borde}" stroke="#000" stroke-width="{f(sw*0.7)}" fill="none"/>')
    # desconchados: la pintura saltada deja ver la cal (formas irregulares, sobre todo arriba y abajo)
    for _ in range(int((x1 - x0) / (1.1 * m))):
        cx = rnd.uniform(x0 + 0.1 * m, x1 - 0.1 * m)
        cy = rnd.choice([y + rnd.uniform(0.02, 0.12) * m, y_abajo - rnd.uniform(0.1, 0.25) * m])
        r = rnd.uniform(0.03, 0.08) * m
        p = [(cx + math.cos(k * 2 * math.pi / 7) * r * rnd.uniform(0.5, 1.3),
              cy + math.sin(k * 2 * math.pi / 7) * r * rnd.uniform(0.3, 0.7)) for k in range(7)]
        out.append(f'<polygon points="{pts(p)}" fill="{lav("cal", m)}" stroke="#000" stroke-width="{f(sw*0.25)}"/>')
    # barro salpicado al pie
    out.append(f'<rect x="{f(x0)}" y="{f(y_abajo-0.1*m)}" width="{f(x1-x0)}" height="{f(0.1*m)}" fill="url(#t-puntos)"/>')
    return ''.join(out)


def puerta_tablas(x0, y0, w, h, m, sw, rnd, color=None, hojas=1):
    """Puerta de tablas con clavos (portón de madera: doc 03 §3.1 [P])."""
    out = [f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="{color or lav("madera", m)}" stroke="#000" stroke-width="{f(sw*0.9)}"/>']
    if not color:
        out.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="url(#t-madera-v)"/>')
    n = max(3, int(w / (0.16 * m)))
    for i in range(1, n):
        x = x0 + w * i / n
        out.append(f'<line x1="{f(x)}" y1="{f(y0)}" x2="{f(x)}" y2="{f(y0+h)}" stroke="#000" stroke-width="{f(sw*0.4)}"/>')
    if hojas == 2:
        out.append(f'<line x1="{f(x0+w/2)}" y1="{f(y0)}" x2="{f(x0+w/2)}" y2="{f(y0+h)}" stroke="#000" stroke-width="{f(sw*0.9)}"/>')
    # travesaños y clavos
    for ty in (0.18, 0.5, 0.82):
        yy = y0 + h * ty
        out.append(f'<line x1="{f(x0)}" y1="{f(yy)}" x2="{f(x0+w)}" y2="{f(yy)}" stroke="#000" stroke-width="{f(sw*0.35)}" stroke-dasharray="{f(0.02*m)} {f(0.13*m)}"/>')
    # aldaba / cerrojo
    out.append(f'<circle cx="{f(x0+w*(0.46 if hojas==2 else 0.85))}" cy="{f(y0+h*0.52)}" r="{f(0.035*m)}" fill="none" stroke="#000" stroke-width="{f(sw*0.5)}"/>')
    return ''.join(out)


def ventana_reja(x0, y0, w, h, m, sw, color=None):
    """Ventana con reja de balaustres de madera torneada y postigos abiertos."""
    out = [f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="#000"/>']
    # interior apenas sugerido
    out.append(f'<rect x="{f(x0+w*0.1)}" y="{f(y0+h*0.55)}" width="{f(w*0.8)}" height="{f(h*0.02)}" fill="#fff" opacity="0.5"/>')
    n = max(5, int(w / (0.11 * m)))
    for i in range(1, n):
        x = x0 + w * i / n
        r = 0.022 * m
        out.append(f'<path d="M{f(x-r)},{f(y0+0.06*m)} L{f(x-r)},{f(y0+h*0.3)} Q{f(x-r*2)},{f(y0+h*0.4)} {f(x-r)},{f(y0+h*0.5)} L{f(x-r)},{f(y0+h-0.06*m)} L{f(x+r)},{f(y0+h-0.06*m)} L{f(x+r)},{f(y0+h*0.5)} Q{f(x+r*2)},{f(y0+h*0.4)} {f(x+r)},{f(y0+h*0.3)} L{f(x+r)},{f(y0+0.06*m)} Z" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw*0.35)}"/>')
    out.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(0.07*m)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
    out.append(f'<rect x="{f(x0)}" y="{f(y0+h-0.07*m)}" width="{f(w)}" height="{f(0.07*m)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
    out.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="none" stroke="#000" stroke-width="{f(sw)}"/>')
    # postigos abiertos a los lados
    pw = w * 0.42
    for lado, xx in ((-1, x0 - pw), (1, x0 + w)):
        out.append(puerta_tablas(xx, y0, pw, h, m, sw * 0.8, random.Random(1), color=color))
    # alféizar y sombra
    out.append(f'<rect x="{f(x0-0.06*m)}" y="{f(y0+h)}" width="{f(w+0.12*m)}" height="{f(0.06*m)}" fill="{lav("cal", m)}" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
    out.append(f'<rect x="{f(x0-0.06*m)}" y="{f(y0+h+0.06*m)}" width="{f(w+0.12*m)}" height="{f(0.09*m)}" fill="url(#t-fina)"/>')
    return ''.join(out)


def letras_pintadas(texto, x0, y_base, alto, sw, color):
    """Letras de brocha (sin fuentes del sistema): trazos a mano alzada para rótulos genéricos."""
    formas = {
        'T': [[(0, 0), (1, 0)], [(0.5, 0), (0.5, 1)]],
        'I': [[(0.5, 0), (0.5, 1)], [(0.25, 0), (0.75, 0)], [(0.25, 1), (0.75, 1)]],
        'E': [[(0.9, 0), (0.1, 0), (0.1, 1), (0.9, 1)], [(0.1, 0.5), (0.7, 0.5)]],
        'N': [[(0.1, 1), (0.1, 0), (0.9, 1), (0.9, 0)]],
        'D': [[(0.1, 0), (0.1, 1), (0.55, 1), (0.9, 0.7), (0.9, 0.3), (0.55, 0), (0.1, 0)]],
        'A': [[(0, 1), (0.5, 0), (1, 1)], [(0.22, 0.6), (0.78, 0.6)]],
    }
    rnd = random.Random(len(texto) * 31 + int(x0))
    out = []
    ancho = alto * 0.78
    x = x0
    for i, ch in enumerate(texto):
        # cada letra con su propio leve vaivén: pintada a mano, no tipografía
        ang = rnd.uniform(-3, 3)
        dy = rnd.uniform(-0.04, 0.04) * alto
        g = []
        for trazo in formas.get(ch, []):
            d = 'M' + ' L'.join(f"{f(x + px * ancho)},{f(y_base - alto + py * alto + dy)}" for px, py in trazo)
            g.append(f'<path d="{d}" stroke="{color}" stroke-width="{f(sw)}" fill="none" stroke-linecap="square" stroke-linejoin="miter"/>')
        cx = x + ancho / 2
        out.append(f'<g transform="rotate({f(ang)} {f(cx)} {f(y_base - alto/2)})">{"".join(g)}</g>')
        x += ancho * 1.3
    return ''.join(out)


def afiche(x0, y0, w, h, m, sw, rnd, color=ROJO, estrella=True):
    """Afiche político genérico del color del partido (doc 03 §1: el color cuenta la división).
    Sin texto ni emblemas reales."""
    ang = rnd.uniform(-3, 3)
    cx, cy = x0 + w / 2, y0 + h / 2
    out = [f'<g transform="rotate({f(ang)} {f(cx)} {f(cy)})" data-p="afiche genérico sin consignas ni nombres reales">']
    out.append(f'<path d="M{f(x0)},{f(y0)} L{f(x0+w)},{f(y0)} L{f(x0+w)},{f(y0+h*0.85)} L{f(x0+w*0.82)},{f(y0+h)} L{f(x0)},{f(y0+h)} Z" fill="{PALETA["papel-viejo"]}" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
    out.append(f'<rect x="{f(x0+w*0.06)}" y="{f(y0+h*0.06)}" width="{f(w*0.88)}" height="{f(h*0.26)}" fill="{color}"/>')
    if estrella:
        # estrella blanca sobre la banda (motivo gráfico, no un emblema real)
        r1, r2 = h * 0.09, h * 0.04
        ex, ey = x0 + w * 0.5, y0 + h * 0.19
        estrella = [(ex + math.cos(-math.pi/2 + k*math.pi/5) * (r1 if k % 2 == 0 else r2),
                     ey + math.sin(-math.pi/2 + k*math.pi/5) * (r1 if k % 2 == 0 else r2)) for k in range(10)]
        out.append(f'<polygon points="{pts(estrella)}" fill="#fff"/>')
    for i in range(5):
        yy = y0 + h * (0.42 + i * 0.1)
        largo = w * (0.8 if i % 2 == 0 else 0.6)
        out.append(f'<line x1="{f(x0+w*0.1)}" y1="{f(yy)}" x2="{f(x0+w*0.1+largo)}" y2="{f(yy)}" stroke="#000" stroke-width="{f(sw*(1.1 if i==0 else 0.6))}"/>')
    out.append(f'<path d="M{f(x0+w)},{f(y0+h*0.85)} L{f(x0+w*0.82)},{f(y0+h)} L{f(x0+w*0.86)},{f(y0+h*0.84)} Z" fill="url(#t-fina)" stroke="#000" stroke-width="{f(sw*0.4)}"/>')
    out.append('</g>')
    return ''.join(out)


# ================================== capa juego (200 px/m) ==================================

def fachada_con_corredor(W, rnd, color, pilares, huecos, notas_extra=''):
    """Fachada de un nivel con corredor bajo el alero (doc 03 §3.1 [V]). Base del viewBox = suelo."""
    m, sw = ppm('juego'), TRAZO['juego']
    H = 900
    y_piso = H - 0.25 * m           # piso del corredor, elevado sobre la plaza
    y_viga = H - 3.0 * m            # cara inferior de la viga del corredor
    y_borde = y_viga - 0.32 * m     # borde de la teja
    out = []
    # tejado (sale por arriba del cuadro: con 200 px/m solo se ven 4,5 m)
    out.append(tejado_frente(0, W, y_borde, 0, m, sw, rnd))
    # muro del fondo del corredor
    out.append(muro_cal(0, W, y_viga, y_piso, m, sw, rnd, grietas=6, desconchados=4))
    # sombra del alero sobre el muro
    out.append(f'<rect x="0" y="{f(y_viga)}" width="{f(W)}" height="{f(0.22*m)}" fill="url(#t-fina)"/>')
    out.append(zocalo(0, W, y_piso, 0.85 * m, m, sw, rnd, color=color))
    for h in huecos:
        out.append(h(m, sw, y_piso, rnd))
    out.append(alero(0, W, y_viga, m, sw, rnd))
    for x in pilares:
        out.append(pilar(x, y_piso, y_viga, m, sw))
    # piso del corredor: lajas de piedra en el borde
    out.append(f'<rect x="0" y="{f(y_piso)}" width="{f(W)}" height="{f(H-y_piso)}" fill="{lav("piedra", m)}" stroke="#000" stroke-width="{f(sw)}"/>')
    out.append(f'<rect x="0" y="{f(y_piso+0.07*m)}" width="{f(W)}" height="{f(H-y_piso-0.07*m)}" fill="url(#t-media)"/>')
    x = 0
    juntas = []
    while x < W:
        x += rnd.uniform(0.45, 0.9) * m
        juntas.append(f'M{f(x)},{f(y_piso)} L{f(x+rnd.uniform(-0.03,0.03)*m)},{f(H)}')
    out.append(f'<path d="{" ".join(juntas)}" stroke="#000" stroke-width="{f(sw*0.5)}" fill="none"/>')
    out.append(f'<line x1="0" y1="{f(y_piso+0.07*m)}" x2="{f(W)}" y2="{f(y_piso+0.07*m)}" stroke="#000" stroke-width="{f(sw*0.5)}"/>')
    # esquinas del edificio
    for xx in (0, W):
        out.append(f'<line x1="{f(xx)}" y1="0" x2="{f(xx)}" y2="{f(H)}" stroke="#000" stroke-width="{f(sw*1.6)}"/>')
    return '\n'.join(out)


def portón_tienda(x0, ancho_m, alto_m, color):
    """Puerta de la tienda abierta de par en par: interior oscuro con estantes y mostrador."""
    def dibujar(m, sw, y_piso, rnd):
        w, h = ancho_m * m, alto_m * m
        y0 = y_piso - h
        out = [f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="#000"/>']
        # estantes con botellas y frascos (negativo en blanco)
        hoja = 0.22 * m
        for i, fy in enumerate((0.2, 0.38, 0.56)):
            yy = y0 + h * fy
            out.append(f'<line x1="{f(x0+hoja+0.05*m)}" y1="{f(yy)}" x2="{f(x0+w-hoja-0.05*m)}" y2="{f(yy)}" stroke="#fff" stroke-width="{f(sw*0.5)}"/>')
            x = x0 + hoja + 0.12 * m
            while x < x0 + w - hoja - 0.15 * m:
                tipo = rnd.random()
                if tipo < 0.45:   # botella
                    bh = rnd.uniform(0.18, 0.26) * m
                    out.append(f'<path d="M{f(x)},{f(yy)} L{f(x)},{f(yy-bh*0.6)} Q{f(x)},{f(yy-bh*0.72)} {f(x+0.02*m)},{f(yy-bh*0.78)} L{f(x+0.02*m)},{f(yy-bh)} L{f(x+0.05*m)},{f(yy-bh)} L{f(x+0.05*m)},{f(yy-bh*0.78)} Q{f(x+0.07*m)},{f(yy-bh*0.72)} {f(x+0.07*m)},{f(yy-bh*0.6)} L{f(x+0.07*m)},{f(yy)}" fill="none" stroke="#fff" stroke-width="{f(sw*0.35)}"/>')
                    x += 0.11 * m
                elif tipo < 0.75:  # frasco
                    out.append(f'<rect x="{f(x)}" y="{f(yy-0.12*m)}" width="{f(0.09*m)}" height="{f(0.12*m)}" rx="{f(0.015*m)}" fill="none" stroke="#fff" stroke-width="{f(sw*0.35)}"/>')
                    x += 0.13 * m
                else:              # paquetes apilados
                    out.append(f'<rect x="{f(x)}" y="{f(yy-0.1*m)}" width="{f(0.16*m)}" height="{f(0.1*m)}" fill="#fff" opacity="0.85"/>')
                    x += 0.2 * m
        # mostrador
        my = y0 + h * 0.66
        out.append(f'<rect x="{f(x0+hoja)}" y="{f(my)}" width="{f(w-2*hoja)}" height="{f(y_piso-my)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
        out.append(f'<rect x="{f(x0+hoja)}" y="{f(my)}" width="{f(w-2*hoja)}" height="{f(y_piso-my)}" fill="url(#t-madera-v)"/>')
        out.append(f'<rect x="{f(x0+hoja)}" y="{f(my)}" width="{f(w-2*hoja)}" height="{f(0.06*m)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
        # balanza de platillos sobre el mostrador
        bx = x0 + w * 0.62
        out.append(f'<path d="M{f(bx)},{f(my)} L{f(bx)},{f(my-0.22*m)} M{f(bx-0.14*m)},{f(my-0.2*m)} L{f(bx+0.14*m)},{f(my-0.2*m)}" stroke="#fff" stroke-width="{f(sw*0.45)}" fill="none"/>')
        for s in (-1, 1):
            px = bx + s * 0.14 * m
            out.append(f'<path d="M{f(px-0.07*m)},{f(my-0.1*m)} Q{f(px)},{f(my-0.04*m)} {f(px+0.07*m)},{f(my-0.1*m)} M{f(px)},{f(my-0.2*m)} L{f(px-0.06*m)},{f(my-0.1*m)} M{f(px)},{f(my-0.2*m)} L{f(px+0.06*m)},{f(my-0.1*m)}" stroke="#fff" stroke-width="{f(sw*0.35)}" fill="none"/>')
        # hojas abiertas contra el vano (pintadas)
        out.append(puerta_tablas(x0, y0, hoja, h, m, sw * 0.8, rnd, color=color))
        out.append(puerta_tablas(x0 + w - hoja, y0, hoja, h, m, sw * 0.8, rnd, color=color))
        # dintel de madera y marco
        out.append(f'<rect x="{f(x0-0.08*m)}" y="{f(y0-0.1*m)}" width="{f(w+0.16*m)}" height="{f(0.1*m)}" fill="{lav("madera", m)}" stroke="#000" stroke-width="{f(sw*0.7)}"/>')
        out.append(f'<rect x="{f(x0-0.08*m)}" y="{f(y0-0.1*m)}" width="{f(w+0.16*m)}" height="{f(0.1*m)}" fill="url(#t-madera)"/>')
        out.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="none" stroke="#000" stroke-width="{f(sw)}"/>')
        # umbral
        out.append(f'<rect x="{f(x0-0.05*m)}" y="{f(y_piso-0.04*m)}" width="{f(w+0.1*m)}" height="{f(0.04*m)}" fill="{lav("piedra", m)}" stroke="#000" stroke-width="{f(sw*0.5)}"/>')
        return ''.join(out)
    return dibujar


def hueco(fn):
    """Adapta un dibujo que solo necesita (m, sw, y_piso, rnd)."""
    return fn


def tienda_roja():
    rnd = random.Random(1946)
    W = 1900

    def rotulo(m, sw, y_piso, rnd):
        return letras_pintadas('TIENDA', 590, y_piso - 2.27 * m, 0.27 * m, sw * 2.4, ROJO)

    def ventana(m, sw, y_piso, rnd):
        return ventana_reja(1250, y_piso - 2.0 * m, 1.25 * m, 1.1 * m, m, sw, color=ROJO)

    def puerta_casa(m, sw, y_piso, rnd):
        return puerta_tablas(1650, y_piso - 2.05 * m, 0.95 * m, 2.05 * m, m, sw, rnd)

    def cartel(m, sw, y_piso, rnd):
        return afiche(230, y_piso - 1.95 * m, 0.7 * m, 0.95 * m, m, sw, rnd)

    def banca(m, sw, y_piso, rnd):
        x0, x1 = 1170, 1560
        ys = y_piso - 0.45 * m
        out = [f'<rect x="{f(x0)}" y="{f(ys)}" width="{f(x1-x0)}" height="{f(0.07*m)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw*0.7)}"/>',
               f'<rect x="{f(x0)}" y="{f(ys)}" width="{f(x1-x0)}" height="{f(0.07*m)}" fill="url(#t-madera)"/>']
        for xx in (x0 + 0.1 * m, x1 - 0.18 * m):
            out.append(f'<rect x="{f(xx)}" y="{f(ys+0.07*m)}" width="{f(0.08*m)}" height="{f(y_piso-ys-0.07*m)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
            out.append(f'<rect x="{f(xx+0.04*m)}" y="{f(ys+0.07*m)}" width="{f(0.04*m)}" height="{f(y_piso-ys-0.07*m)}" fill="url(#t-media)"/>')
        # un sombrero olvidado sobre la banca
        sx = x0 + 0.55 * m
        out.append(f'<path d="M{f(sx-0.2*m)},{f(ys)} Q{f(sx)},{f(ys-0.03*m)} {f(sx+0.2*m)},{f(ys)} Z M{f(sx-0.1*m)},{f(ys-0.01*m)} Q{f(sx-0.1*m)},{f(ys-0.13*m)} {f(sx)},{f(ys-0.13*m)} Q{f(sx+0.1*m)},{f(ys-0.13*m)} {f(sx+0.1*m)},{f(ys-0.01*m)} Z" fill="#000"/>')
        out.append(f'<path d="M{f(sx-0.1*m)},{f(ys-0.04*m)} L{f(sx+0.1*m)},{f(ys-0.04*m)}" stroke="#fff" stroke-width="{f(sw*0.4)}"/>')
        return ''.join(out)

    def materas(m, sw, y_piso, rnd):
        out = []
        for mx in (1580, 1600 + 0.35 * m):
            out.append(maceta(mx, y_piso, m, sw, rnd))
        return ''.join(out)

    cuerpo = fachada_con_corredor(
        W, rnd, ROJO,
        pilares=[60, 470, 1060, 1590, 1845],
        huecos=[cartel, rotulo, portón_tienda(560, 1.9, 2.1, ROJO), ventana, puerta_casa, banca, materas],
    )
    archivo('tienda-roja', W, 900, 'juego', 'tienda de los rojos (liberales), con corredor',
            cuerpo, notas='Rojo en zócalo, hojas de la puerta, postigos, rótulo y afiche: fachada partidista (doc 03 §1). '
                          'Portón de madera y rótulo pintado: doc 03 §3.1 [P]; composición, no un local real.')


def maceta(x, y_piso, m, sw, rnd):
    """Matera de barro con geranios sobre el piso del corredor. Flores rosadas: el rojo es del
    partido (paleta.md §3)."""
    w, h = 0.22 * m, 0.24 * m
    out = [f'<path d="M{f(x)},{f(y_piso-h)} L{f(x+w)},{f(y_piso-h)} L{f(x+w*0.88)},{f(y_piso)} L{f(x+w*0.12)},{f(y_piso)} Z" fill="{lav("teja", m)}" stroke="#000" stroke-width="{f(sw*0.6)}"/>',
           f'<path d="M{f(x+w*0.55)},{f(y_piso-h)} L{f(x+w)},{f(y_piso-h)} L{f(x+w*0.88)},{f(y_piso)} L{f(x+w*0.5)},{f(y_piso)} Z" fill="url(#t-fina)"/>',
           f'<rect x="{f(x-0.01*m)}" y="{f(y_piso-h-0.02*m)}" width="{f(w+0.02*m)}" height="{f(0.04*m)}" fill="{lav("teja", m)}" stroke="#000" stroke-width="{f(sw*0.5)}"/>']
    for _ in range(9):
        lx = x + w / 2 + rnd.uniform(-0.2, 0.2) * m
        ly = y_piso - h - rnd.uniform(0.04, 0.3) * m
        r = rnd.uniform(0.04, 0.07) * m
        out.append(f'<circle cx="{f(lx)}" cy="{f(ly)}" r="{f(r)}" fill="{lav("sementera", m, 0.8)}" stroke="#000" stroke-width="{f(sw*0.4)}"/>')
        out.append(f'<path d="M{f(lx-r*0.5)},{f(ly)} Q{f(lx)},{f(ly+r*0.4)} {f(lx+r*0.5)},{f(ly)}" stroke="#000" stroke-width="{f(sw*0.25)}" fill="none"/>')
    for _ in range(4):
        fx = x + w / 2 + rnd.uniform(-0.12, 0.12) * m
        fy = y_piso - h - rnd.uniform(0.25, 0.4) * m
        out.append(f'<circle cx="{f(fx)}" cy="{f(fy)}" r="{f(0.04*m)}" fill="{lav("cinta-rosa", m)}" stroke="#000" stroke-width="{f(sw*0.35)}"/>')
    return ''.join(out)


def casa_porton():
    rnd = random.Random(1948)
    W = 1700

    def porton(m, sw, y_piso, rnd):
        x0, w, h = 230, 2.0 * m, 2.25 * m
        y0 = y_piso - h
        out = [puerta_tablas(x0, y0, w, h, m, sw, rnd, hojas=2)]
        # postigo (puerta pequeña) en la hoja derecha
        out.append(f'<rect x="{f(x0+w*0.6)}" y="{f(y0+h*0.3)}" width="{f(w*0.28)}" height="{f(h*0.62)}" fill="none" stroke="#000" stroke-width="{f(sw*0.7)}"/>')
        # arco rebajado de piedra sobre el portón
        out.append(f'<path d="M{f(x0-0.12*m)},{f(y0)} Q{f(x0+w/2)},{f(y0-0.35*m)} {f(x0+w+0.12*m)},{f(y0)} L{f(x0+w)},{f(y0)} Q{f(x0+w/2)},{f(y0-0.22*m)} {f(x0)},{f(y0)} Z" fill="{lav("piedra", m)}" stroke="#000" stroke-width="{f(sw*0.8)}"/>')
        out.append(f'<path d="M{f(x0-0.12*m)},{f(y0)} Q{f(x0+w/2)},{f(y0-0.35*m)} {f(x0+w+0.12*m)},{f(y0)} L{f(x0+w)},{f(y0)} Q{f(x0+w/2)},{f(y0-0.22*m)} {f(x0)},{f(y0)} Z" fill="url(#t-puntos-ralos)"/>')
        # cerrojo de hierro
        out.append(f'<rect x="{f(x0+w*0.4)}" y="{f(y0+h*0.5)}" width="{f(0.2*m)}" height="{f(0.04*m)}" fill="#000"/>')
        return ''.join(out)

    def ventanas(m, sw, y_piso, rnd):
        return (ventana_reja(860, y_piso - 2.0 * m, 1.15 * m, 1.1 * m, m, sw)
                + ventana_reja(1330, y_piso - 2.0 * m, 0.9 * m, 1.1 * m, m, sw))

    def materas(m, sw, y_piso, rnd):
        return maceta(720, y_piso, m, sw, rnd) + maceta(1190, y_piso, m, sw, rnd)

    def leña(m, sw, y_piso, rnd):
        """Atado de leña recostado contra el muro."""
        out = []
        x0 = 1560
        for i in range(7):
            xx = x0 + i * 0.045 * m + rnd.uniform(-0.01, 0.01) * m
            out.append(f'<path d="M{f(xx)},{f(y_piso)} L{f(xx+0.22*m)},{f(y_piso-1.1*m)}" stroke="#000" stroke-width="{f(sw*1.3)}" stroke-linecap="round"/>'
                       f'<path d="M{f(xx)},{f(y_piso)} L{f(xx+0.22*m)},{f(y_piso-1.1*m)}" stroke="{lav("madera", m, 0.7)}" stroke-width="{f(sw*0.7)}" stroke-linecap="round"/>')
            out.append(f'<path d="M{f(xx+0.01*m)},{f(y_piso-0.02*m)} L{f(xx+0.22*m)},{f(y_piso-1.08*m)}" stroke="#fff" stroke-width="{f(sw*0.35)}"/>')
        out.append(f'<path d="M{f(x0-0.02*m)},{f(y_piso-0.45*m)} Q{f(x0+0.25*m)},{f(y_piso-0.4*m)} {f(x0+0.4*m)},{f(y_piso-0.5*m)}" stroke="#000" stroke-width="{f(sw*0.7)}" fill="none"/>')
        return ''.join(out)

    cuerpo = fachada_con_corredor(
        W, rnd, None,
        pilares=[55, 690, 1160, 1650],
        huecos=[porton, ventanas, materas, leña],
    )
    archivo('casa-porton', W, 900, 'juego', 'casa con portón y corredor', cuerpo,
            notas='Portón de madera: doc 03 §3.1 [P]. Sin color: casa no partidista.')


def empedrado():
    """Mosaico de empedrado (repetible en x). Se coloca por arriba en el suelo de la capa [P: empedrado o tierra]."""
    rnd = random.Random(7)
    m, sw = ppm('juego'), TRAZO['juego']
    W, H = 1024, 180
    out = [f'<g data-p="plaza empedrada o de tierra: confirmar con fotos del norte de Boyacá años 40">',
           f'<rect x="0" y="0" width="{W}" height="{H}" fill="{lav("tierra", m, 0.8)}"/>',
           f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#t-puntos-ralos)"/>']
    y = 2.0
    fila = 0
    while y < H:
        alto = 13 + fila * 5.5  # perspectiva: más grandes hacia el frente
        x = -rnd.uniform(0, alto)
        while x < W:
            ancho = alto * rnd.uniform(1.2, 1.9)
            for dx in (0, -W, W):
                xx = x + dx
                if xx + ancho < 0 or xx > W:
                    continue
                cy = y + alto * 0.5
                rx, ry = ancho * 0.46, alto * 0.42
                p = []
                for k in range(8):
                    a = k * math.pi / 4
                    jit = random.Random(int(x * 13 + y * 7) + k).uniform(0.85, 1.1)
                    p.append((xx + ancho / 2 + math.cos(a) * rx * jit, cy + math.sin(a) * ry * jit))
                d = 'M' + ' Q'.join(
                    f"{f(p[k][0])},{f(p[k][1])} {f((p[k][0]+p[(k+1)%8][0])/2)},{f((p[k][1]+p[(k+1)%8][1])/2)}" for k in range(8)) + ' Z'
                out.append(f'<path d="{d}" fill="{lav("piedra", m, 0.75)}" stroke="#000" stroke-width="{f(sw*0.5)}"/>')
                out.append(f'<path d="M{f(xx+ancho*0.18)},{f(cy+ry*0.35)} Q{f(xx+ancho/2)},{f(cy+ry*1.05)} {f(xx+ancho*0.82)},{f(cy+ry*0.35)} Q{f(xx+ancho/2)},{f(cy+ry*0.65)} {f(xx+ancho*0.18)},{f(cy+ry*0.35)} Z" fill="url(#t-media)"/>')
            x += ancho + rnd.uniform(1.5, 4)
        y += alto + 1.5
        fila += 1
    out.append('</g>')
    archivo('empedrado', W, H, 'juego', 'empedrado de la plaza (mosaico)', '\n'.join(out),
            notas='Mosaico horizontal sin costura: se repite cada 1024 px.')


def costal(x, y_suelo, w, h, m, sw, rnd, abierto=False):
    """Costal de fique: tejido en trama cruzada, amarre arriba o boca abierta con papas."""
    out = []
    d = (f'M{f(x)},{f(y_suelo)} Q{f(x-0.04*m)},{f(y_suelo-h*0.55)} {f(x+w*0.12)},{f(y_suelo-h*0.92)} '
         f'Q{f(x+w*0.5)},{f(y_suelo-h*1.04)} {f(x+w*0.88)},{f(y_suelo-h*0.92)} '
         f'Q{f(x+w+0.04*m)},{f(y_suelo-h*0.55)} {f(x+w)},{f(y_suelo)} Z')
    out.append(f'<path d="{d}" fill="{lav("paja", m)}" stroke="#000" stroke-width="{f(sw*0.8)}"/>')
    out.append(f'<path d="{d}" fill="url(#t-tejido)"/>')
    # cara en sombra (luz de la izquierda), pliegues que salen del amarre y costura
    sombra = (f'M{f(x+w*0.62)},{f(y_suelo)} Q{f(x+w*0.75)},{f(y_suelo-h*0.5)} {f(x+w*0.7)},{f(y_suelo-h*0.96)} '
              f'Q{f(x+w*0.8)},{f(y_suelo-h*0.95)} {f(x+w*0.88)},{f(y_suelo-h*0.92)} Q{f(x+w+0.04*m)},{f(y_suelo-h*0.55)} {f(x+w)},{f(y_suelo)} Z')
    out.append(f'<path d="{sombra}" fill="url(#t-fina)"/>')
    out.append(f'<path d="M{f(x+w*0.44)},{f(y_suelo-h*0.95)} Q{f(x+w*0.3)},{f(y_suelo-h*0.8)} {f(x+w*0.22)},{f(y_suelo-h*0.55)} '
               f'M{f(x+w*0.56)},{f(y_suelo-h*0.95)} Q{f(x+w*0.68)},{f(y_suelo-h*0.78)} {f(x+w*0.74)},{f(y_suelo-h*0.5)} '
               f'M{f(x+w*0.15)},{f(y_suelo-h*0.2)} Q{f(x+w*0.5)},{f(y_suelo-h*0.12)} {f(x+w*0.85)},{f(y_suelo-h*0.2)}" stroke="#000" stroke-width="{f(sw*0.45)}" fill="none"/>')
    out.append(f'<path d="M{f(x+w*0.12)},{f(y_suelo-h*0.08)} Q{f(x+w*0.06)},{f(y_suelo-h*0.5)} {f(x+w*0.16)},{f(y_suelo-h*0.86)}" stroke="#000" stroke-width="{f(sw*0.4)}" fill="none" stroke-dasharray="{f(sw*1.2)} {f(sw*1.2)}"/>')
    out.append(f'<path d="M{f(x+w*0.05)},{f(y_suelo)} Q{f(x+w*0.5)},{f(y_suelo-0.05*m)} {f(x+w*0.95)},{f(y_suelo)} Z" fill="url(#t-media)"/>')
    if abierto:
        for _ in range(7):
            px = x + w * rnd.uniform(0.2, 0.8)
            py = y_suelo - h * rnd.uniform(0.92, 1.12)
            r = 0.045 * m
            out.append(f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="{f(r*1.2)}" ry="{f(r)}" fill="{lav("tapia", m)}" stroke="#000" stroke-width="{f(sw*0.45)}"/>')
            out.append(f'<circle cx="{f(px+r*0.3)}" cy="{f(py-r*0.2)}" r="{f(r*0.12)}" fill="#000"/>')
    else:
        out.append(f'<path d="M{f(x+w*0.4)},{f(y_suelo-h*0.98)} L{f(x+w*0.5)},{f(y_suelo-h*1.12)} L{f(x+w*0.6)},{f(y_suelo-h*0.98)}" stroke="#000" stroke-width="{f(sw*0.7)}" fill="{lav("paja", m)}"/>')
    return ''.join(out)


def canasto(x, y_suelo, w, h, m, sw, rnd, carga='papas'):
    """Canasto de mimbre con su carga (papas, mazorcas o cebollas)."""
    out = []
    d = f'M{f(x)},{f(y_suelo-h)} L{f(x+w)},{f(y_suelo-h)} L{f(x+w*0.9)},{f(y_suelo)} L{f(x+w*0.1)},{f(y_suelo)} Z'
    # carga asomando
    if carga == 'mazorcas':
        for i in range(5):
            cx = x + w * (0.15 + i * 0.17)
            out.append(f'<ellipse cx="{f(cx)}" cy="{f(y_suelo-h-0.05*m)}" rx="{f(0.05*m)}" ry="{f(0.11*m)}" transform="rotate({f(rnd.uniform(-35,35))} {f(cx)} {f(y_suelo-h)})" fill="{lav("trigo", m)}" stroke="#000" stroke-width="{f(sw*0.45)}"/>')
            out.append(f'<ellipse cx="{f(cx)}" cy="{f(y_suelo-h-0.05*m)}" rx="{f(0.05*m)}" ry="{f(0.11*m)}" transform="rotate({f(rnd.uniform(-35,35))} {f(cx)} {f(y_suelo-h)})" fill="url(#t-puntos)"/>')
    elif carga == 'cebollas':
        for i in range(6):
            cx = x + w * (0.12 + i * 0.15)
            out.append(f'<circle cx="{f(cx)}" cy="{f(y_suelo-h-0.03*m)}" r="{f(0.05*m)}" fill="{lav("cebada", m)}" stroke="#000" stroke-width="{f(sw*0.45)}"/>')
            out.append(f'<path d="M{f(cx)},{f(y_suelo-h-0.08*m)} Q{f(cx+rnd.uniform(-0.1,0.1)*m)},{f(y_suelo-h-0.3*m)} {f(cx+rnd.uniform(-0.15,0.15)*m)},{f(y_suelo-h-0.42*m)}" stroke="#000" stroke-width="{f(sw*0.5)}" fill="none"/>')
    else:
        for i in range(8):
            cx = x + w * (0.1 + i * 0.11) + rnd.uniform(-0.01, 0.01) * m
            cy = y_suelo - h - rnd.uniform(0.0, 0.06) * m
            out.append(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(0.05*m)}" ry="{f(0.04*m)}" fill="{lav("tapia", m)}" stroke="#000" stroke-width="{f(sw*0.45)}"/>')
    out.append(f'<path d="{d}" fill="{lav("paja", m)}" stroke="#000" stroke-width="{f(sw*0.8)}"/>')
    # tejido: bandas horizontales y varillas
    for i in range(1, 5):
        yy = y_suelo - h + h * i / 5
        out.append(f'<line x1="{f(x+w*0.02*i)}" y1="{f(yy)}" x2="{f(x+w-w*0.02*i)}" y2="{f(yy)}" stroke="#000" stroke-width="{f(sw*0.4)}"/>')
    out.append(f'<path d="{d}" fill="url(#t-vert)" opacity="0.6"/>')
    out.append(f'<rect x="{f(x-0.02*m)}" y="{f(y_suelo-h-0.03*m)}" width="{f(w+0.04*m)}" height="{f(0.05*m)}" rx="{f(0.02*m)}" fill="{lav("paja", m)}" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
    return ''.join(out)


def olla(x, y_suelo, w, h, m, sw, rnd, tipo='olla'):
    """Loza de barro: olla de boca ancha o múcura de cuello estrecho."""
    out = []
    if tipo == 'mucura':
        d = (f'M{f(x+w*0.38)},{f(y_suelo-h)} L{f(x+w*0.62)},{f(y_suelo-h)} L{f(x+w*0.6)},{f(y_suelo-h*0.8)} '
             f'Q{f(x+w*1.05)},{f(y_suelo-h*0.62)} {f(x+w*0.82)},{f(y_suelo-h*0.08)} Q{f(x+w*0.5)},{f(y_suelo+h*0.02)} {f(x+w*0.18)},{f(y_suelo-h*0.08)} '
             f'Q{f(x-w*0.05)},{f(y_suelo-h*0.62)} {f(x+w*0.4)},{f(y_suelo-h*0.8)} Z')
    else:
        d = (f'M{f(x+w*0.1)},{f(y_suelo-h)} L{f(x+w*0.9)},{f(y_suelo-h)} '
             f'Q{f(x+w*1.06)},{f(y_suelo-h*0.55)} {f(x+w*0.78)},{f(y_suelo-h*0.05)} Q{f(x+w*0.5)},{f(y_suelo+h*0.03)} {f(x+w*0.22)},{f(y_suelo-h*0.05)} '
             f'Q{f(x-w*0.06)},{f(y_suelo-h*0.55)} {f(x+w*0.1)},{f(y_suelo-h)} Z')
    out.append(f'<path d="{d}" fill="{lav("teja", m)}" stroke="#000" stroke-width="{f(sw*0.7)}"/>')
    out.append(f'<path d="{d}" fill="url(#t-fina)"/>')
    # brillo y franja decorativa
    out.append(f'<path d="M{f(x+w*0.28)},{f(y_suelo-h*0.75)} Q{f(x+w*0.2)},{f(y_suelo-h*0.45)} {f(x+w*0.3)},{f(y_suelo-h*0.2)}" stroke="#fff" stroke-width="{f(sw*1.2)}" fill="none" stroke-linecap="round"/>')
    out.append(f'<path d="M{f(x+w*0.12)},{f(y_suelo-h*0.7)} Q{f(x+w*0.5)},{f(y_suelo-h*0.62)} {f(x+w*0.88)},{f(y_suelo-h*0.7)}" stroke="#000" stroke-width="{f(sw*0.4)}" fill="none" stroke-dasharray="{f(0.02*m)} {f(0.015*m)}"/>')
    if tipo != 'mucura':
        out.append(f'<ellipse cx="{f(x+w/2)}" cy="{f(y_suelo-h)}" rx="{f(w*0.4)}" ry="{f(0.035*m)}" fill="#000"/>')
    return ''.join(out)


def objetos_juego():
    m, sw = ppm('juego'), TRAZO['juego']
    rnd = random.Random(11)
    # costales apilados
    H = 220
    cuerpo = (costal(10, H, 0.75 * m, 0.7 * m, m, sw, rnd)
              + costal(150, H, 0.7 * m, 0.65 * m, m, sw, rnd, abierto=True)
              + costal(70, H - 0.55 * m, 0.7 * m, 0.5 * m, m, sw, rnd))
    archivo('costales', 0.75 * m + 160, H, 'juego', 'costales de papa', cuerpo)
    H = 160
    cuerpo = (canasto(10, H, 0.65 * m, 0.42 * m, m, sw, rnd, 'papas')
              + canasto(155, H, 0.55 * m, 0.38 * m, m, sw, rnd, 'mazorcas')
              + canasto(280, H, 0.6 * m, 0.4 * m, m, sw, rnd, 'cebollas'))
    archivo('canastos', 410, H, 'juego', 'canastos de mimbre con papas, mazorcas y cebollas', cuerpo,
            notas='Canastos en el mercado: Hernán Díaz, "Mercado campesino en Boyacá" (BanRep, hacia 1960).')
    H = 130
    cuerpo = (olla(10, H, 0.55 * m, 0.42 * m, m, sw, rnd)
              + olla(125, H, 0.4 * m, 0.55 * m, m, sw, rnd, 'mucura')
              + olla(200, H, 0.45 * m, 0.34 * m, m, sw, rnd))
    archivo('ollas', 300, H, 'juego', 'loza de barro', cuerpo, notas='Loza de barro genérica [P: tipos de loza en el mercado de 1946].')


# ================================ capa cielo (fija, paralaje 0) ================================

def curva(p, cerrar=False):
    """Curva suave que pasa por los puntos (Catmull-Rom convertida a Bézier)."""
    n = len(p)
    d = f'M{f(p[0][0])},{f(p[0][1])}'
    for i in range(n if cerrar else n - 1):
        p0 = p[(i - 1) % n] if (cerrar or i > 0) else p[i]
        p1, p2 = p[i], p[(i + 1) % n]
        p3 = p[(i + 2) % n] if (cerrar or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p2[0])},{f(p2[1])}'
    return d + (' Z' if cerrar else '')


def perfil(control, x0, x1, rnd, rugosidad, paso=6):
    """Cresta de un cerro: pasa por los puntos de control, con quiebres de roca."""
    out, ruido, x = [], 0.0, x0
    while x <= x1 + 0.01:
        i = 0
        while i < len(control) - 2 and control[i + 1][0] < x:
            i += 1
        (xa, ya), (xb, yb) = control[i], control[i + 1]
        t = 0 if xb == xa else min(1, max(0, (x - xa) / (xb - xa)))
        ruido = ruido * 0.6 + rnd.uniform(-1, 1) * rugosidad
        out.append((x, ya + (yb - ya) * (1 - math.cos(t * math.pi)) / 2 + ruido))
        x += paso
    return out


def y_de(perf, x):
    """Altura de un perfil en x (interpolación lineal)."""
    for (xa, ya), (xb, yb) in zip(perf, perf[1:]):
        if xa <= x <= xb:
            return ya + (yb - ya) * (x - xa) / (xb - xa)
    return perf[0][1] if x < perf[0][0] else perf[-1][1]


# Cultivos vistos de lejos (paleta.md §4 «Boyacá: campo»): trigo y cebada de la franja triguera
# [V], sementera de papa, potrero, tierra arada y barbecho (papel). Lavado + trama; pesos por repetición.
CULTIVOS = [('trigo', 't-surco-a'), ('trigo', None), ('trigo', 't-surco-b'), ('cebada', 't-surco-a'),
            ('cebada', None), ('sementera', 't-surco-c'), ('sementera', 't-fina'), ('potrero', 't-puntos-ralos'),
            ('potrero', None), ('potrero', 't-puntos-ralos'), ('tapia', 't-horiz'), ('tierra', 't-surco-b'),
            (None, None), (None, 't-puntos-ralos')]


def defs_cultivo():
    """Surcos en varias direcciones: siguen la ladera, no la pantalla."""
    return '''
  <defs>
    <pattern id="t-surco-a" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(12)"><line x1="0" y1="2.5" x2="5" y2="2.5" stroke="#000" stroke-width="0.7"/></pattern>
    <pattern id="t-surco-b" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(-14)"><line x1="0" y1="2.5" x2="5" y2="2.5" stroke="#000" stroke-width="0.7"/></pattern>
    <pattern id="t-surco-c" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(72)"><line x1="0" y1="2" x2="4" y2="2" stroke="#000" stroke-width="0.6"/></pattern>
  </defs>'''


def ladera(perf, x0, x1, desde, pie, rnd, sw, alto0, crece, casitas=0.06, fuerza=0.5):
    """Parcelas en franjas que siguen la ladera (cultivos, potreros, barbecho), con cercas de
    piedra, cercos vivos y casitas. Sin recortar: el llamador lo mete en el clipPath del cerro.
    fuerza: del lavado (perspectiva aérea: más lejos, más papel)."""
    media = sum(y for _, y in perf) / len(perf)
    xs = list(range(int(x0) - 30, int(x1) + 40, 10))
    bordes, desplaz, k = [], desde, 0
    while True:
        fase = rnd.uniform(0, 6)
        w = min(1.0, (desplaz - desde) / 160)  # abajo las franjas se aplanan hacia el pie
        borde = [(x, (1 - w) * (y_de(perf, x) + desplaz) + w * (media + desplaz) + 3 * math.sin(x / 80 + fase))
                 for x in xs]
        bordes.append(borde)
        if min(y for _, y in borde) > pie:
            break
        desplaz += alto0 + crece * k + rnd.uniform(-2, 3)
        k += 1
    rellenos, cercas, piedra, arbustos, casas = [], [], [], [], []

    def en(borde, x):
        return y_de(borde, x)

    for sup, inf in zip(bordes, bordes[1:]):
        alto = sum(b[1] - a[1] for a, b in zip(sup, inf)) / len(sup)
        x = x0 - 30 - rnd.uniform(0, 60)
        while x < x1 + 30:
            ancho = alto * rnd.uniform(2.4, 6.0)
            inclina = rnd.uniform(-0.3, 0.3) * alto
            xa_s, xa_i = x + inclina, x - inclina
            xb_s, xb_i = x + ancho + inclina, x + ancho - inclina
            arriba = [(xx, en(sup, xx)) for xx in [xa_s] + [v for v in xs if xa_s < v < xb_s] + [xb_s]]
            abajo = [(xx, en(inf, xx)) for xx in [xb_i] + [v for v in reversed(xs) if xa_i < v < xb_i] + [xa_i]]
            cultivo, trama = rnd.choice(CULTIVOS)
            forma = pts(arriba + abajo)
            if cultivo:
                rellenos.append(f'<polygon points="{forma}" fill="{diluir(PALETA[cultivo], fuerza)}"/>')
            if trama:
                rellenos.append(f'<polygon points="{forma}" fill="url(#{trama})"/>')
            # lindero lateral: unas veces cerca de piedra, otras cerco vivo, otras solo raya
            lado = f'M{f(xb_s)},{f(en(sup, xb_s))} L{f(xb_i)},{f(en(inf, xb_i))}'
            tipo = rnd.random()
            (piedra if tipo < 0.3 else arbustos if tipo < 0.45 else cercas).append(lado)
            if rnd.random() < casitas:
                cx, cy = xb_s + rnd.uniform(-alto, 0), en(sup, xb_s) + alto * 0.55
                casas.append((cx, cy))
            x += ancho
    out = rellenos
    for borde in bordes:
        d = f'M{f(borde[0][0])},{f(borde[0][1])}' + ''.join(f' L{f(a)},{f(b)}' for a, b in borde[1:])
        (piedra if rnd.random() < 0.4 else cercas).append(d)
    out.append(f'<path d="{" ".join(cercas)}" stroke="#000" stroke-width="{f(sw*0.45)}" fill="none"/>')
    # cercas de piedra: hilera de piedritas
    out.append(f'<path d="{" ".join(piedra)}" stroke="#000" stroke-width="{f(sw*0.4)}" fill="none"/>')
    out.append(f'<path d="{" ".join(piedra)}" stroke="#000" stroke-width="{f(sw*1.5)}" fill="none" stroke-dasharray="1 2.2" stroke-linecap="round"/>')
    # cercos vivos: matorral oscuro a lo largo del lindero
    monte = diluir(PALETA['monte'], min(1.0, fuerza + 0.35))
    out.append(f'<path d="{" ".join(arbustos)}" stroke="{monte}" stroke-width="{f(sw*2.6)}" fill="none" stroke-dasharray="2.4 1.2 1.2 1.6" stroke-linecap="round"/>')
    for cx, cy in casas:
        # casita de teja con su mancha de árboles al lado
        out.append(f'<rect x="{f(cx)}" y="{f(cy)}" width="7" height="4.5" fill="{PALETA["cal"]}" stroke="#000" stroke-width="{f(sw*0.55)}"/>'
                   f'<path d="M{f(cx-1.2)},{f(cy)} L{f(cx+8.2)},{f(cy)} L{f(cx+6.6)},{f(cy-2.8)} L{f(cx+0.4)},{f(cy-2.8)} Z" fill="{diluir(PALETA["teja"], min(1.0, fuerza + 0.3))}" stroke="#000" stroke-width="{f(sw*0.4)}"/>'
                   f'<rect x="{f(cx+2.6)}" y="{f(cy+1.6)}" width="1.6" height="2.9" fill="#000"/>')
        if rnd.random() < 0.6:
            for _ in range(rnd.randint(2, 3)):
                ax, ay = cx + rnd.choice((-1, 1)) * rnd.uniform(6, 11), cy + rnd.uniform(-2, 2)
                out.append(f'<ellipse cx="{f(ax)}" cy="{f(ay)}" rx="{f(rnd.uniform(2.2, 3.4))}" ry="{f(rnd.uniform(3, 4.5))}" fill="{monte}" stroke="#000" stroke-width="{f(sw*0.4)}"/>')
    return ''.join(out)


def paramo(perf, x0, x1, hasta, rnd, sw, n):
    """Parte alta sin cultivar: macollas de pajonal y peñas con su cara en sombra."""
    out, macollas = [], []
    for _ in range(n):
        x = rnd.uniform(x0, x1)
        y = rnd.uniform(y_de(perf, x) + 4, y_de(perf, x) + hasta)
        macollas.append(f'M{f(x-1.6)},{f(y)} L{f(x-0.4)},{f(y-2.6)} M{f(x)},{f(y)} L{f(x+0.2)},{f(y-3.2)} M{f(x+1.6)},{f(y)} L{f(x+0.7)},{f(y-2.4)}')
    out.append(f'<path d="{" ".join(macollas)}" stroke="#000" stroke-width="{f(sw*0.45)}" fill="none"/>')
    for _ in range(n // 12):
        x = rnd.uniform(x0 + 20, x1 - 20)
        y = y_de(perf, x) + rnd.uniform(3, hasta * 0.6)
        w, h = rnd.uniform(8, 18), rnd.uniform(4, 8)
        roca = [(x, y), (x + w * 0.3, y - h), (x + w * 0.75, y - h * 0.8), (x + w, y)]
        out.append(f'<polygon points="{pts(roca)}" fill="{diluir(PALETA["piedra"], 0.55)}" stroke="#000" stroke-width="{f(sw*0.5)}"/>'
                   f'<polygon points="{pts([(x + w*0.55, y - h*0.85), (x + w*0.75, y - h*0.8), (x + w, y), (x + w*0.6, y)])}" fill="url(#t-media)"/>')
    return ''.join(out)


def camino(puntos, sw):
    """Camino de herradura: dos orillas de tinta con el piso claro en medio."""
    d = curva(puntos)
    return (f'<path d="{d}" stroke="#000" stroke-width="{f(sw*2.6)}" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="{diluir(PALETA["tierra"], 0.45)}" stroke-width="{f(sw*1.3)}" fill="none" stroke-linecap="round"/>')


def cañada(puntos, sw):
    """Cañada que baja de un portillo: monte en el fondo, raya de tinta y su lado en sombra."""
    d = curva(puntos)
    sombra = puntos + [(x + 9, y + 2) for x, y in reversed(puntos)]
    monte = puntos + [(x + 14, y + 3) for x, y in reversed(puntos)]
    return (f'<polygon points="{pts(monte)}" fill="{diluir(PALETA["monte"], 0.55)}"/>'
            f'<polygon points="{pts(sombra)}" fill="url(#t-fina)"/>'
            f'<path d="{d}" stroke="#000" stroke-width="{f(sw*0.6)}" fill="none"/>')


def cerro(id_clip, perf, pie, sw_cresta, dentro, relleno=PAPEL, linea='#000'):
    """Silueta de cerro con su lavado (tapa lo de atrás), contenido recortado y cresta entintada."""
    forma = pts(perf + [(perf[-1][0], pie), (perf[0][0], pie)])
    cresta = f'M{f(perf[0][0])},{f(perf[0][1])}' + ''.join(f' L{f(x)},{f(y)}' for x, y in perf[1:])
    return (f'<clipPath id="{id_clip}"><polygon points="{forma}"/></clipPath>'
            f'<polygon points="{forma}" fill="{relleno}"/>'
            f'<g clip-path="url(#{id_clip})">{dentro}</g>'
            f'<path d="{cresta}" stroke="{linea}" stroke-width="{f(sw_cresta)}" fill="none" stroke-linejoin="round"/>')


def cordillera():
    """Cordillera detrás del pueblo: cerro mayor cultivado hasta el páramo, sierra lejana y
    estribos cercanos. Norte de Boyacá genérico [P: paisaje]; se coloca arriba en y=0."""
    rnd = random.Random(19460)
    sw = TRAZO['cielo']
    W, H = 1920, 700
    pie = H
    out = [defs_cultivo(), '<g data-p="paisaje genérico del norte de Boyacá">']
    # sierra lejana: solo contorno y unas pocas rayas de ladera (perspectiva aérea)
    lejana = perfil([(0, 318), (240, 292), (470, 338), (690, 306), (930, 350), (1210, 322),
                     (1480, 286), (1700, 316), (1920, 298)], 0, W, rnd, 1.2)
    rayas = []
    for _ in range(70):
        x = rnd.uniform(0, W)
        y = y_de(lejana, x) + rnd.uniform(6, 60)
        rayas.append(f'M{f(x)},{f(y)} l{f(rnd.uniform(5, 14))},{f(rnd.uniform(2, 6))}')
    # bruma: la sierra lejana en gris claro y línea de trama (paleta.md §6.4)
    out.append(cerro('c-lejana', lejana, pie, sw * 0.8,
                     f'<path d="{" ".join(rayas)}" stroke="{GRIS_TRAMA}" stroke-width="{f(sw*0.35)}" fill="none"/>',
                     relleno=diluir(PALETA['gris-claro'], 0.55), linea=GRIS_TRAMA))
    # cerro mayor: cumbre a la derecha del centro, flanco derecho en sombra
    mayor = perfil([(0, 472), (190, 446), (400, 456), (590, 404), (770, 352), (920, 333),
                    (1050, 292), (1170, 250), (1262, 262), (1385, 303), (1515, 336),
                    (1655, 372), (1795, 394), (1920, 412)], 0, W, rnd, 2.0)
    dentro = [ladera(mayor, 0, W, 52, pie, rnd, sw, alto0=9, crece=2.2, fuerza=0.5)]
    sombra = [(1170, 250), (1262, 262), (1385, 303), (1515, 336), (1655, 372), (1795, 394),
              (1920, 412), (1920, 520), (1700, 470), (1480, 420), (1330, 360), (1215, 300)]
    dentro.append(f'<polygon points="{pts(sombra)}" fill="url(#t-fina)"/>')
    dentro.append(paramo(mayor, 520, 1820, 50, rnd, sw, 260))
    for portillo in ((780, 352), (1060, 292), (1400, 306), (1580, 350)):
        x, y = portillo
        dentro.append(cañada([(x, y + 6), (x + 8, y + 40), (x - 4, y + 80), (x + 10, y + 130), (x + 2, y + 190)], sw))
    dentro.append(camino([(1300, 520), (1340, 470), (1250, 440), (1310, 405), (1220, 372), (1250, 330), (1190, 292)], sw))
    dentro.append(camino([(240, 540), (300, 500), (230, 476), (330, 458)], sw))
    # arriba, el páramo gris plateado del frailejón; abajo, los cultivos
    out.append(cerro('c-mayor', mayor, pie, sw * 1.4, ''.join(dentro), relleno=diluir(PALETA['frailejon'], 0.55)))
    # estribos cercanos: más grandes, más trama, cresta más gruesa
    oeste = perfil([(0, 486), (150, 470), (330, 478), (520, 500), (700, 560), (820, 640)], 0, 820, rnd, 1.6)
    out.append(cerro('c-oeste', oeste, pie, sw * 1.6, ladera(oeste, 0, 820, 10, pie, rnd, sw, alto0=13, crece=3.2, casitas=0.1, fuerza=0.6),
                     relleno=diluir(PALETA['potrero'], 0.5)))
    este = perfil([(1260, 640), (1400, 548), (1560, 470), (1720, 448), (1860, 458), (1920, 452)], 1260, W, rnd, 1.6)
    out.append(cerro('c-este', este, pie, sw * 1.6, ladera(este, 1260, W, 10, pie, rnd, sw, alto0=13, crece=3.2, casitas=0.1, fuerza=0.6),
                     relleno=diluir(PALETA['potrero'], 0.5)))
    out.append('</g>')
    archivo('cordillera', W, H, 'cielo', 'cordillera con cultivos, páramo y fincas', '\n'.join(out),
            notas='Fija (paralaje 0): a kilómetros no se mueve. Se coloca arriba (y=0); la base queda tapada por el plano lejano.')


def nube(nombre, W, H, semilla):
    """Cúmulo de tinta: borde de arcos, panza casi plana con trama (sin degradados)."""
    rnd = random.Random(semilla)
    sw = TRAZO['cielo']
    base = H - 4
    n = max(4, int(W / 75))
    cima = []
    for i in range(n):
        t = (i + 0.5) / n
        x = 6 + (W - 12) * t + rnd.uniform(-0.2, 0.2) * (W - 12) / n
        alto = (0.3 + 0.65 * math.sin(math.pi * t) ** 0.7) * rnd.uniform(0.78, 1.0)
        cima.append((x, base - (H - 10) * alto))
    p = [(6, base - 5)] + cima + [(W - 6, base - 3)]
    d = f'M{f(p[0][0])},{f(p[0][1])}'
    for (xa, ya), (xb, yb) in zip(p, p[1:]):
        r = math.hypot(xb - xa, yb - ya) * rnd.uniform(0.56, 0.72)
        d += f' A{f(r)},{f(r)} 0 0 1 {f(xb)},{f(yb)}'
    x = W - 6
    while x > 6:
        xn = max(6, x - rnd.uniform(0.18, 0.32) * W)
        r = (x - xn) * rnd.uniform(1.4, 2.2)
        d += f' A{f(r)},{f(r)} 0 0 1 {f(xn)},{f(base - 5 if xn == 6 else base - rnd.uniform(0, 3))}'
        x = xn
    d += ' Z'
    # sombra de la panza con borde ondulado: cada bola tiene su parte baja en sombra
    ys = base - H * 0.42
    sombra = f'M0,{f(base + 2)} L0,{f(ys)}'
    x = 0
    while x < W:
        xn = min(W, x + rnd.uniform(0.14, 0.26) * W)
        sombra += f' Q{f((x + xn) / 2)},{f(ys - H * rnd.uniform(0.04, 0.12))} {f(xn)},{f(ys + H * rnd.uniform(-0.03, 0.05))}'
        x = xn
    sombra += f' L{W},{f(base + 2)} Z'
    out = [f'<clipPath id="c-{nombre}"><path d="{d}"/></clipPath>',
           f'<path d="{d}" fill="{PALETA["cielo-llano"]}"/>',
           f'<g clip-path="url(#c-{nombre})">',
           f'<path d="{sombra}" fill="{PALETA["niebla"]}"/>',
           f'<path d="{sombra}" fill="url(#t-fina)"/>',
           f'<rect x="0" y="{f(base - H*0.12)}" width="{W}" height="{f(H*0.14)}" fill="url(#t-horiz)"/>',
           '</g>']
    # volúmenes interiores: arcos de las bolas de atrás
    vol = []
    for (xa, ya), (xb, yb) in zip(cima, cima[1:]):
        if rnd.random() < 0.75:
            xm, ym = (xa + xb) / 2, max(ya, yb) + (H - 10) * 0.18
            r = (xb - xa) * 0.42
            vol.append(f'M{f(xm - r)},{f(ym + r*0.35)} A{f(r)},{f(r)} 0 0 1 {f(xm + r*0.6)},{f(ym - r*0.55)}')
    out.append(f'<path d="{" ".join(vol)}" stroke="#000" stroke-width="{f(sw*0.5)}" fill="none"/>')
    out.append(f'<path d="{d}" fill="none" stroke="#000" stroke-width="{f(sw)}" stroke-linejoin="round"/>')
    archivo(nombre, W, H, 'cielo', 'nube (deriva despacio)', '\n'.join(out),
            notas='Frame suelto: la escena lo desplaza en x (deriva) y lo repite al salir de cuadro.')


# ============================ figuras compartidas (lejos y medio) ============================

def sombra_suelo(x0, x1, base, m):
    """Sombra de contacto en el suelo (sol de la mañana desde la izquierda)."""
    return f'<path d="M{f(x0)},{f(base)} Q{f((x0 + x1) / 2)},{f(base - 0.1 * m)} {f(x1)},{f(base)} Z" fill="url(#t-fina)"/>'


def persona(x, base, m, sw, tipo='hombre', espejo=False, k=1.0, sombrero='negro', ruana='oscura',
            falda='negro-anil', lleva=None, panuelo=None):
    """Campesino o campesina de fondo, sin rostro (doc 03 §1): solo silueta, sombrero, ruana o
    pañolón. tipo: 'hombre' (ruana, pantalón de dril, alpargatas), 'mujer' (pañolón negro,
    falda larga), 'sentada' (vendedora en el suelo). k escala la figura (niños). x: eje de la
    figura; mira a la derecha salvo espejo. falda: token de la paleta (faldas oscuras teñidas con
    añil, Ocampo López, 1977)."""
    s = -1 if espejo else 1

    def P(dx, dy):
        return f'{f(x + s * dx * k * m)},{f(base - dy * k * m)}'

    det = m * k >= 60  # flecos y pliegues solo de cerca
    lw = sw
    out = []

    def cabeza(dy):
        # perfil sin rasgos: nuca redonda y la nariz apenas insinuada hacia donde mira
        d = (f'M{P(-0.06, dy - 0.06)} Q{P(-0.09, dy + 0.02)} {P(-0.05, dy + 0.08)} L{P(0.09, dy + 0.08)} '
             f'L{P(0.1, dy + 0.03)} L{P(0.124, dy + 0.005)} L{P(0.1, dy - 0.012)} Q{P(0.1, dy - 0.07)} {P(0.03, dy - 0.088)} Z')
        return (f'<path d="{d}" fill="{lav("piel", m)}" stroke="#000" stroke-width="{f(lw * 0.7)}" stroke-linejoin="round"/>'
                f'<path d="M{P(-0.07, dy + 0.035)} L{P(0.1, dy + 0.035)} L{P(0.1, dy + 0.08)} L{P(-0.06, dy + 0.08)} Z" fill="{lav("piel-sombra", m)}"/>'
                f'<path d="M{P(-0.06, dy - 0.05)} Q{P(-0.095, dy + 0.02)} {P(-0.05, dy + 0.08)} L{P(-0.015, dy + 0.08)} Q{P(-0.05, dy + 0.01)} {P(-0.025, dy - 0.04)} Z" fill="#000"/>')

    def sombrero_(dy, ala, copa, clase):
        negro = clase == 'negro'
        relleno = '#000' if negro else lav('paja', m)
        ala_d = (f'M{P(-ala, dy + 0.012)} Q{P(0, dy - 0.004)} {P(ala + 0.015, dy + 0.012)} Q{P(ala + 0.035, dy + 0.03)} {P(ala, dy + 0.04)} '
                 f'Q{P(0, dy + 0.05)} {P(-ala + 0.01, dy + 0.04)} Q{P(-ala - 0.03, dy + 0.03)} {P(-ala, dy + 0.012)} Z')
        copa_d = (f'M{P(-0.088, dy + 0.035)} L{P(-0.078, dy + copa)} Q{P(0, dy + copa + 0.03)} {P(0.085, dy + copa)} '
                  f'L{P(0.098, dy + 0.035)} Z')
        r = [f'<path d="{copa_d}" fill="{relleno}" stroke="#000" stroke-width="{f(lw * 0.7)}" stroke-linejoin="round"/>',
             f'<path d="{ala_d}" fill="{relleno}" stroke="#000" stroke-width="{f(lw * 0.7)}"/>']
        cinta = f'M{P(-0.086, dy + 0.06)} L{P(0.096, dy + 0.06)}'
        if negro:
            r.append(f'<path d="{cinta}" stroke="#fff" stroke-width="{f(lw * 0.45)}"/>')
        else:
            r.append(f'<path d="{copa_d}" fill="url(#t-fina)"/>')
            r.append(f'<path d="{cinta}" stroke="#000" stroke-width="{f(lw * 1.1)}"/>')
        if det:
            r.append(f'<path d="M{P(-0.03, dy + copa + 0.012)} Q{P(0.0, dy + copa - 0.015)} {P(0.035, dy + copa + 0.01)}" '
                     f'stroke="{"#fff" if negro else "#000"}" stroke-width="{f(lw * 0.4)}" fill="none"/>')
        return ''.join(r)

    def flecos(xa, ya, xc, yc, xb, yb, n, color):
        # flecos a lo largo de una curva cuadrática (borde de ruana o pañolón)
        d = []
        for i in range(n + 1):
            u = i / n
            px = (1 - u) ** 2 * xa + 2 * u * (1 - u) * xc + u * u * xb
            py = (1 - u) ** 2 * ya + 2 * u * (1 - u) * yc + u * u * yb
            d.append(f'M{P(px, py)} L{P(px, py - 0.035)}')
        return f'<path d="{" ".join(d)}" stroke="{color}" stroke-width="{f(lw * 0.4)}"/>'

    if tipo == 'hombre':
        atras = f'M{P(-0.13, 0.84)} L{P(-0.02, 0.84)} L{P(-0.04, 0.04)} L{P(-0.13, 0.04)} Z'
        # pantalón de dril y alpargatas blancas (Ocampo López, 1977)
        dril = lav('blanco-tela', m)
        out.append(f'<path d="{atras}" fill="{dril}" stroke="#000" stroke-width="{f(lw * 0.6)}"/><path d="{atras}" fill="url(#t-fina)"/>')
        out.append(f'<path d="M{P(-0.01, 0.84)} L{P(0.11, 0.84)} L{P(0.13, 0.04)} L{P(0.03, 0.04)} Z" fill="{dril}" stroke="#000" stroke-width="{f(lw * 0.6)}"/>')
        out.append(f'<path d="M{P(-0.15, 0)} L{P(-0.03, 0)} L{P(-0.04, 0.05)} L{P(-0.14, 0.05)} Z '
                   f'M{P(0.02, 0)} L{P(0.19, 0)} Q{P(0.19, 0.04)} {P(0.13, 0.05)} L{P(0.03, 0.05)} Z" fill="{dril}" stroke="#000" stroke-width="{f(lw * 0.4)}"/>')
        if lleva == 'vara':
            out.append(f'<path d="M{P(0.34, 1.0)} L{P(0.46, 0.0)}" stroke="#000" stroke-width="{f(lw * 0.9)}" stroke-linecap="round"/>')
        ru = (f'M{P(-0.07, 1.43)} L{P(0.08, 1.43)} Q{P(0.2, 1.42)} {P(0.26, 1.32)} L{P(0.41, 0.82)} '
              f'Q{P(0.02, 0.73)} {P(-0.39, 0.8)} L{P(-0.25, 1.32)} Q{P(-0.2, 1.42)} {P(-0.07, 1.43)} Z')
        # lana en tonos naturales (Ruanas de Nobsa; Ocampo: «en tonos oscuros»)
        fondo, trama, linea = {'oscura': (lav('lana-parda', m), 't-fina', '#fff'),
                               'gris': (lav('lana-gris', m), 't-puntos-ralos', '#fff'),
                               'clara': (lav('lana-cruda', m), 't-puntos-ralos', '#000'),
                               'negra': (lav('pano-oscuro', m), None, '#fff')}[ruana]
        out.append(f'<path d="{ru}" fill="{fondo}" stroke="#000" stroke-width="{f(lw * 0.8)}" stroke-linejoin="round"/>')
        if trama:
            out.append(f'<path d="{ru}" fill="url(#{trama})"/>')
        # listas tejidas cerca del borde y caída de la ruana sobre el pecho
        out.append(f'<path d="M{P(-0.37, 0.86)} Q{P(0.02, 0.79)} {P(0.39, 0.88)} M{P(-0.36, 0.9)} Q{P(0.02, 0.83)} {P(0.38, 0.92)} '
                   f'M{P(0.03, 1.42)} Q{P(0.06, 1.1)} {P(0.07, 0.77)}" stroke="{linea}" stroke-width="{f(lw * 0.45)}" fill="none"/>')
        if det:
            out.append(flecos(-0.39, 0.8, 0.02, 0.73, 0.41, 0.82, 16, '#000'))
        if lleva == 'vara':
            out.append(f'<ellipse cx="{P(0.345, 1.0).split(",")[0]}" cy="{P(0.345, 1.0).split(",")[1]}" rx="{f(0.03 * k * m)}" ry="{f(0.035 * k * m)}" fill="{lav("piel", m)}" stroke="#000" stroke-width="{f(lw * 0.5)}"/>')
        if panuelo:
            out.append(f'<path d="M{P(-0.05, 1.43)} L{P(0.1, 1.43)} L{P(0.035, 1.33)} Z" fill="{panuelo}" stroke="#000" stroke-width="{f(lw * 0.4)}" data-p="pañuelo partidista: uso en 1946 por confirmar"/>')
        out.append(cabeza(1.52))
        out.append(sombrero_(1.6, 0.21, 0.165, sombrero))
    elif tipo in ('mujer', 'sentada'):
        sentada = tipo == 'sentada'
        if sentada:
            fa = (f'M{P(-0.42, 0.0)} Q{P(-0.43, 0.27)} {P(-0.16, 0.42)} L{P(0.14, 0.42)} Q{P(0.4, 0.3)} {P(0.47, 0.0)} Z')
            pa = (f'M{P(-0.05, 0.84)} Q{P(-0.19, 0.81)} {P(-0.22, 0.7)} L{P(-0.28, 0.36)} Q{P(-0.02, 0.3)} {P(0.2, 0.38)} '
                  f'L{P(0.2, 0.7)} Q{P(0.15, 0.81)} {P(0.07, 0.83)} Z')
            y_cab, borde_pa, manos = 0.915, (-0.28, 0.36, -0.02, 0.3, 0.2, 0.38), [(0.24, 0.43)]
        else:
            fa = (f'M{P(-0.14, 0.98)} L{P(0.15, 0.98)} Q{P(0.25, 0.5)} {P(0.31, 0.05)} '
                  f'Q{P(0.0, 0.0)} {P(-0.29, 0.05)} Q{P(-0.24, 0.5)} {P(-0.14, 0.98)} Z')
            pa = (f'M{P(-0.06, 1.4)} Q{P(-0.19, 1.38)} {P(-0.23, 1.27)} L{P(-0.3, 0.84)} Q{P(-0.04, 0.78)} {P(0.22, 0.9)} '
                  f'L{P(0.21, 1.27)} Q{P(0.16, 1.39)} {P(0.07, 1.41)} Z')
            y_cab, borde_pa, manos = 1.475, (-0.3, 0.84, -0.04, 0.78, 0.22, 0.9), [(0.16, 1.1)]
            out.append(f'<path d="M{P(0.12, 0.0)} L{P(0.25, 0.0)} Q{P(0.25, 0.035)} {P(0.19, 0.04)} L{P(0.12, 0.04)} Z" fill="#000"/>')
        out.append(f'<path d="{fa}" fill="{lav(falda, m)}" stroke="#000" stroke-width="{f(lw * 0.75)}" stroke-linejoin="round"/>')
        if not sentada:
            # el ruedo de la enagua blanca asoma bajo la falda
            out.append(f'<path d="M{P(-0.29, 0.05)} Q{P(0.0, 0.0)} {P(0.31, 0.05)} L{P(0.3, 0.1)} Q{P(0.0, 0.055)} {P(-0.28, 0.1)} Z" '
                       f'fill="{lav("blanco-tela", m)}" stroke="#000" stroke-width="{f(lw * 0.45)}"/>')
        if det and not sentada:
            out.append(f'<path d="M{P(-0.05, 0.96)} Q{P(-0.1, 0.5)} {P(-0.14, 0.06)} M{P(0.06, 0.96)} Q{P(0.1, 0.5)} {P(0.14, 0.04)} '
                       f'M{P(-0.27, 0.16)} Q{P(0.0, 0.11)} {P(0.29, 0.16)}" stroke="#fff" stroke-width="{f(lw * 0.35)}" fill="none"/>')
        out.append(f'<path d="{pa}" fill="#000" stroke="#000" stroke-width="{f(lw * 0.6)}" stroke-linejoin="round"/>')
        if det:
            xa, ya, xc, yc, xb, yb = borde_pa
            out.append(f'<path d="M{P(xa + 0.08, ya + 0.38)} Q{P(xa + 0.1, ya + 0.15)} {P(xa + 0.14, ya + 0.0)} '
                       f'M{P(xb - 0.05, yb + 0.33)} Q{P(xb - 0.08, yb + 0.15)} {P(xb - 0.1, yb + 0.02)}" stroke="#fff" stroke-width="{f(lw * 0.45)}" fill="none"/>')
            out.append(flecos(xa, ya, xc, yc, xb, yb, 14, '#000'))
        for mx, my in manos:
            out.append(f'<ellipse cx="{P(mx, my).split(",")[0]}" cy="{P(mx, my).split(",")[1]}" rx="{f(0.032 * k * m)}" ry="{f(0.036 * k * m)}" fill="{lav("piel", m)}" stroke="#000" stroke-width="{f(lw * 0.5)}"/>')
        out.append(cabeza(y_cab))
        out.append(sombrero_(y_cab + 0.08, 0.17, 0.17, sombrero))
        if lleva == 'canasto':
            cv = f'M{P(0.1, 0.96)} L{P(0.44, 0.96)} L{P(0.4, 0.74)} L{P(0.14, 0.74)} Z'
            out.append(f'<path d="M{P(0.12, 0.96)} Q{P(0.2, 1.2)} {P(0.42, 0.96)}" stroke="#000" stroke-width="{f(lw * 0.7)}" fill="none"/>')
            out.append(f'<path d="{cv}" fill="{lav("paja", m)}" stroke="#000" stroke-width="{f(lw * 0.7)}"/><path d="{cv}" fill="url(#t-vert)"/>')
            out.append(f'<path d="M{P(0.12, 0.89)} L{P(0.42, 0.89)} M{P(0.13, 0.82)} L{P(0.41, 0.82)}" stroke="#000" stroke-width="{f(lw * 0.45)}"/>')
        elif lleva == 'paraguas':
            # paraguas negro abierto contra el sol del mercado (Hernán Díaz, BanRep)
            out.append(f'<path d="M{P(0.15, 1.1)} L{P(0.05, 2.04)}" stroke="#000" stroke-width="{f(lw * 0.7)}"/>')
            puntas = [(-0.47 + 1.04 * i / 6, 1.92 + (0.02 if i % 6 else 0)) for i in range(7)]
            d = f'M{P(*puntas[0])} Q{P(-0.42, 2.18)} {P(0.05, 2.22)} Q{P(0.52, 2.18)} {P(*puntas[-1])}'
            for (xa, ya), (xb, yb) in zip(reversed(puntas), list(reversed(puntas))[1:]):
                d += f' Q{P((xa + xb) / 2, 1.97)} {P(xb, yb)}'
            out.append(f'<path d="{d} Z" fill="#000"/>')
            out.append(f'<path d="{" ".join(f"M{P(0.05, 2.22)} L{P(px, py)}" for px, py in puntas[1:-1])}" stroke="#fff" stroke-width="{f(lw * 0.35)}"/>')
            out.append(f'<path d="M{P(0.05, 2.22)} L{P(0.05, 2.29)}" stroke="#000" stroke-width="{f(lw * 0.8)}"/>')
    return ''.join(out)


def mula(x, base, m, sw, espejo=False, oscura=True, carga=True):
    """Mula de carga con enjalma y costales (mercado: Hernán Díaz, BanRep). x: centro del lomo."""
    s = -1 if espejo else 1

    def P(dx, dy):
        return f'{f(x + s * dx * m)},{f(base - dy * m)}'

    # pelaje: la paleta no tiene token de animales; se usa el más cercano (decisión, paleta.md §11)
    pelo = lav('madera', m, 0.85) if oscura else lav('tapia', m)
    out = []

    def pata(d, lejos_):
        return (f'<path d="{d}" fill="{pelo}" stroke="#000" stroke-width="{f(sw * 0.6)}" stroke-linejoin="round"/>'
                f'<path d="{d}" fill="url(#{"t-media" if lejos_ else "t-fina"})"/>')

    def casco(xc):
        return f'<path d="M{P(xc - 0.045, 0.07)} L{P(xc + 0.05, 0.07)} L{P(xc + 0.065, 0)} L{P(xc - 0.06, 0)} Z" fill="#000"/>'

    # patas del otro lado, detrás
    out.append(pata(f'M{P(0.36, 0.9)} L{P(0.48, 0.9)} L{P(0.47, 0.48)} L{P(0.46, 0.07)} L{P(0.39, 0.07)} L{P(0.4, 0.48)} Z', True) + casco(0.425))
    out.append(pata(f'M{P(-0.42, 0.86)} L{P(-0.58, 0.86)} L{P(-0.62, 0.46)} L{P(-0.55, 0.07)} L{P(-0.48, 0.07)} L{P(-0.53, 0.47)} Z', True) + casco(-0.515))
    # cola
    out.append(f'<path d="M{P(-0.8, 1.24)} Q{P(-0.93, 1.0)} {P(-0.88, 0.62)}" stroke="#000" stroke-width="{f(sw * 1.6)}" fill="none" stroke-linecap="round"/>'
               f'<path d="M{P(-0.88, 0.7)} Q{P(-0.95, 0.55)} {P(-0.86, 0.45)} Q{P(-0.82, 0.58)} {P(-0.85, 0.7)} Z" fill="#000"/>')
    cuerpo = (f'M{P(0.45, 1.33)} Q{P(0.0, 1.24)} {P(-0.55, 1.32)} Q{P(-0.83, 1.32)} {P(-0.85, 1.08)} '
              f'Q{P(-0.85, 0.86)} {P(-0.62, 0.8)} Q{P(0.0, 0.74)} {P(0.45, 0.82)} Q{P(0.68, 0.88)} {P(0.72, 1.05)} L{P(0.78, 1.18)} Z')
    cuello = f'M{P(0.4, 1.3)} Q{P(0.7, 1.55)} {P(0.92, 1.67)} L{P(1.04, 1.5)} Q{P(0.86, 1.22)} {P(0.72, 1.0)} Z'
    # cabeza larga de mula: frente recta, hocico redondo y quijada ancha
    cabeza = (f'M{P(0.9, 1.68)} Q{P(1.0, 1.72)} {P(1.08, 1.64)} L{P(1.38, 1.27)} Q{P(1.45, 1.16)} {P(1.38, 1.1)} '
              f'Q{P(1.31, 1.06)} {P(1.25, 1.1)} L{P(1.12, 1.2)} Q{P(1.0, 1.26)} {P(0.98, 1.4)} Q{P(0.97, 1.52)} {P(1.02, 1.55)} Z')
    orejas = (f'M{P(0.9, 1.67)} Q{P(0.8, 1.84)} {P(0.82, 1.98)} Q{P(0.93, 1.87)} {P(0.98, 1.69)} Z '
              f'M{P(0.98, 1.7)} Q{P(0.96, 1.88)} {P(1.02, 1.99)} Q{P(1.07, 1.85)} {P(1.05, 1.67)} Z')
    for d in (orejas, cuello, cuerpo, cabeza):
        out.append(f'<path d="{d}" fill="{pelo}" stroke="#000" stroke-width="{f(sw * 0.7)}" stroke-linejoin="round"/><path d="{d}" fill="url(#t-fina)"/>')
    # crin corta, ojo, ollar y jáquima
    out.append(f'<path d="M{P(0.42, 1.33)} Q{P(0.7, 1.56)} {P(0.9, 1.68)} L{P(0.88, 1.73)} Q{P(0.68, 1.61)} {P(0.4, 1.38)} Z" fill="#000"/>')
    out.append(f'<circle cx="{P(1.08, 1.55).split(",")[0]}" cy="{P(1.08, 1.55).split(",")[1]}" r="{f(0.028 * m)}" fill="#fff"/>')
    # jáquima de soga: testera, muserola y carrillera
    out.append(f'<path d="M{P(0.97, 1.62)} L{P(1.06, 1.24)} M{P(1.04, 1.3)} L{P(1.32, 1.2)} M{P(1.0, 1.42)} L{P(1.2, 1.16)}" stroke="#fff" stroke-width="{f(sw * 0.55)}"/>')
    # patas de este lado
    out.append(pata(f'M{P(0.5, 0.9)} L{P(0.64, 0.9)} L{P(0.62, 0.48)} L{P(0.6, 0.07)} L{P(0.53, 0.07)} L{P(0.53, 0.48)} Z', False) + casco(0.565))
    out.append(pata(f'M{P(-0.52, 0.86)} L{P(-0.72, 0.86)} L{P(-0.76, 0.46)} L{P(-0.67, 0.07)} L{P(-0.6, 0.07)} L{P(-0.66, 0.47)} Z', False) + casco(-0.635))
    if carga:
        enjalma = f'M{P(-0.44, 1.27)} Q{P(0.0, 1.42)} {P(0.43, 1.32)} L{P(0.4, 1.16)} Q{P(0.0, 1.22)} {P(-0.42, 1.12)} Z'
        bulto = f'M{P(-0.3, 1.36)} Q{P(-0.32, 1.6)} {P(0.0, 1.62)} Q{P(0.34, 1.6)} {P(0.32, 1.38)} Z'
        costal_ = f'M{P(-0.36, 1.24)} Q{P(-0.44, 0.96)} {P(-0.28, 0.84)} L{P(0.27, 0.86)} Q{P(0.4, 0.98)} {P(0.31, 1.26)} Z'
        for d, tono, tr in ((enjalma, 'lana-gris', 't-horiz'), (bulto, 'lana-cruda', 't-fina'), (costal_, 'paja', 't-tejido')):
            out.append(f'<path d="{d}" fill="{lav(tono, m)}" stroke="#000" stroke-width="{f(sw * 0.7)}" stroke-linejoin="round"/><path d="{d}" fill="url(#{tr})"/>')
        # sogas: cincha y amarres en cruz
        out.append(f'<path d="M{P(0.08, 1.6)} L{P(0.12, 0.8)} M{P(-0.3, 1.2)} L{P(0.26, 0.9)} M{P(-0.3, 0.9)} L{P(0.28, 1.2)} '
                   f'M{P(-0.28, 1.5)} Q{P(0.0, 1.44)} {P(0.3, 1.5)}" stroke="#000" stroke-width="{f(sw * 0.75)}" fill="none"/>')
    return ''.join(out)


# =============================== capa lejos (0,15 · 30 px/m) ===============================

def tejado_lejos(x0, x1, y_alero, y_cumbre, m, sw, rnd, cuatro_aguas=False):
    """Tejado visto desde el otro lado de la plaza: banda de teja más oscura que la cal."""
    vuelo = 0.3 * m
    a, b = x0 - vuelo, x1 + vuelo
    lim = 0.9 * m if cuatro_aguas else 0.05 * m
    forma = [(a, y_alero), (b, y_alero), (b - lim, y_cumbre), (a + lim, y_cumbre)]
    out = [f'<polygon points="{pts(forma)}" fill="{lav("teja", m)}"/>', f'<polygon points="{pts(forma)}" fill="url(#t-fina)"/>']
    paso, canales, x = 0.26 * m, [], a + 0.13 * m
    while x < b:
        tope = y_cumbre
        if x < a + lim:
            tope = y_alero + (y_cumbre - y_alero) * (x - a) / lim
        elif x > b - lim:
            tope = y_alero + (y_cumbre - y_alero) * (b - x) / lim
        canales.append(f'M{f(x)},{f(y_alero - 0.05 * m)} L{f(x + rnd.uniform(-0.4, 0.4))},{f(tope)}')
        x += paso
    out.append(f'<path d="{" ".join(canales)}" stroke="#000" stroke-width="{f(sw * 0.35)}"/>')
    # tejas cambiadas, musgo y matas sobre el tejado viejo
    for _ in range(int((b - a) / (3 * m)) + 1):
        tx = rnd.uniform(a + 0.5 * m, b - 0.8 * m)
        ty = rnd.uniform(y_cumbre + 0.2 * m, y_alero - 0.3 * m)
        out.append(f'<rect x="{f(tx)}" y="{f(ty)}" width="{f(rnd.uniform(0.3, 0.7) * m)}" height="{f(0.2 * m)}" fill="url(#t-media)"/>')
    matas = []
    for _ in range(rnd.randint(1, 3)):
        mx = rnd.uniform(a + lim + 4, b - lim - 4)
        matas.append(f'M{f(mx-2)},{f(y_cumbre)} L{f(mx-1)},{f(y_cumbre-3)} M{f(mx)},{f(y_cumbre)} L{f(mx+0.4)},{f(y_cumbre-4)} M{f(mx+2)},{f(y_cumbre)} L{f(mx+1.6)},{f(y_cumbre-2.6)}')
    out.append(f'<path d="{" ".join(matas)}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
    # bocas de teja en el borde, borde del alero y caballete combado
    out.append(f'<line x1="{f(a)}" y1="{f(y_alero - 1.2)}" x2="{f(b)}" y2="{f(y_alero - 1.2)}" stroke="#000" stroke-width="2" stroke-dasharray="2 {f(paso - 2)}"/>')
    out.append(f'<polygon points="{pts(forma)}" fill="none" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
    out.append(f'<line x1="{f(a)}" y1="{f(y_alero)}" x2="{f(b)}" y2="{f(y_alero)}" stroke="#000" stroke-width="{f(sw * 1.1)}"/>')
    out.append(f'<path d="M{f(a + lim)},{f(y_cumbre)} Q{f((a + b) / 2)},{f(y_cumbre + 0.5)} {f(b - lim)},{f(y_cumbre)} '
               f'M{f(a + lim)},{f(y_cumbre + 0.1 * m)} Q{f((a + b) / 2)},{f(y_cumbre + 0.1 * m + 0.6)} {f(b - lim)},{f(y_cumbre + 0.1 * m)}" '
               f'stroke="#000" stroke-width="{f(sw * 0.8)}" fill="none"/>')
    return ''.join(out)


def huecos_lejos(x0, y_piso, m, sw, color, puertas, ventanas):
    """Puertas (pos, ancho, alto, abierta) y ventanas (pos, ancho, alto, alféizar) en metros."""
    out = []
    for pos, an, al, abierta in puertas:
        px, pw, ph = x0 + pos * m, an * m, al * m
        py = y_piso - ph
        if abierta:
            # interior en penumbra con las hojas abiertas contra el vano
            out.append(f'<rect x="{f(px)}" y="{f(py)}" width="{f(pw)}" height="{f(ph)}" fill="{lav("madera", m)}"/>'
                       f'<rect x="{f(px)}" y="{f(py)}" width="{f(pw)}" height="{f(ph)}" fill="url(#t-densa)"/>')
            hoja = min(0.22 * m, pw * 0.2)
            for hx in (px, px + pw - hoja):
                out.append(f'<rect x="{f(hx)}" y="{f(py)}" width="{f(hoja)}" height="{f(ph)}" fill="{color or lav("madera", m)}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
                if not color:
                    out.append(f'<rect x="{f(hx)}" y="{f(py)}" width="{f(hoja)}" height="{f(ph)}" fill="url(#t-madera-v)"/>')
        else:
            out.append(f'<rect x="{f(px)}" y="{f(py)}" width="{f(pw)}" height="{f(ph)}" fill="{color or lav("madera", m)}"/>')
            if not color:
                out.append(f'<rect x="{f(px)}" y="{f(py)}" width="{f(pw)}" height="{f(ph)}" fill="url(#t-madera-v)"/>')
            out.append(f'<line x1="{f(px + pw / 2)}" y1="{f(py)}" x2="{f(px + pw / 2)}" y2="{f(y_piso)}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
        out.append(f'<rect x="{f(px)}" y="{f(py)}" width="{f(pw)}" height="{f(ph)}" fill="none" stroke="#000" stroke-width="{f(sw * 0.8)}"/>')
        out.append(f'<rect x="{f(px - 0.08 * m)}" y="{f(py - 0.1 * m)}" width="{f(pw + 0.16 * m)}" height="{f(0.1 * m)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
    for pos, an, al, alf in ventanas:
        wx, ww, wh = x0 + pos * m, an * m, al * m
        wy = y_piso - (alf + al) * m
        out.append(f'<rect x="{f(wx)}" y="{f(wy)}" width="{f(ww)}" height="{f(wh)}" fill="{lav("madera", m)}"/>'
                   f'<rect x="{f(wx)}" y="{f(wy)}" width="{f(ww)}" height="{f(wh)}" fill="url(#t-densa)"/>')
        barrotes, bx = [], wx + 0.12 * m
        while bx < wx + ww - 0.05 * m:
            barrotes.append(f'M{f(bx)},{f(wy)} L{f(bx)},{f(wy + wh)}')
            bx += 0.13 * m
        out.append(f'<path d="{" ".join(barrotes)}" stroke="#fff" stroke-width="{f(sw * 0.7)}"/>')
        out.append(f'<rect x="{f(wx)}" y="{f(wy)}" width="{f(ww)}" height="{f(wh)}" fill="none" stroke="#000" stroke-width="{f(sw * 0.8)}"/>')
        pw = ww * 0.42
        for hx in (wx - pw, wx + ww):
            out.append(f'<rect x="{f(hx)}" y="{f(wy)}" width="{f(pw)}" height="{f(wh)}" fill="{color or lav("madera", m)}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
            if not color:
                out.append(f'<rect x="{f(hx)}" y="{f(wy)}" width="{f(pw)}" height="{f(wh)}" fill="url(#t-madera-v)"/>')
        out.append(f'<rect x="{f(wx - 0.06 * m)}" y="{f(wy + wh)}" width="{f(ww + 0.12 * m)}" height="{f(0.07 * m)}" fill="{lav("cal", m)}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
    return ''.join(out)


def muro_lejos(x0, x1, y0, y1, m, sw, rnd, fondo=True):
    """Tapia encalada lejana: blanca, con alguna grieta y desconchado pequeños."""
    out = [f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1 - x0)}" height="{f(y1 - y0)}" fill="{lav("cal", m)}" stroke="#000" stroke-width="{f(sw * 0.8)}"/>'] if fondo else []
    for _ in range(max(1, int((x1 - x0) / (5 * m)))):
        gx, gy = rnd.uniform(x0 + 0.4 * m, x1 - 0.4 * m), rnd.uniform(y0 + 0.3 * m, y1 - 1.2 * m)
        out.append(f'<path d="M{f(gx)},{f(gy)} l{f(rnd.uniform(-2, 2))},{f(5)} l{f(rnd.uniform(-2, 2))},{f(6)} l{f(rnd.uniform(-2, 2))},{f(5)}" stroke="#000" stroke-width="{f(sw * 0.35)}" fill="none"/>')
        dx, dy = rnd.uniform(x0 + 0.5 * m, x1 - 0.5 * m), rnd.uniform(y0 + 0.4 * m, y1 - 1.0 * m)
        out.append(f'<ellipse cx="{f(dx)}" cy="{f(dy)}" rx="{f(rnd.uniform(1.5, 3.5))}" ry="{f(rnd.uniform(1, 2))}" fill="{lav("tapia", m)}" stroke="#000" stroke-width="{f(sw * 0.25)}"/>')
    return ''.join(out)


def zocalo_lejos(x0, x1, y_piso, m, sw, rnd, color):
    zy = y_piso - 0.8 * m
    out = [f'<rect x="{f(x0)}" y="{f(zy)}" width="{f(x1 - x0)}" height="{f(0.8 * m)}" fill="{color or lav("tapia", m)}"/>']
    if not color:
        out.append(f'<rect x="{f(x0)}" y="{f(zy)}" width="{f(x1 - x0)}" height="{f(0.8 * m)}" fill="url(#t-fina)"/>')
    borde, x = f'M{f(x0)},{f(zy)}', x0
    while x < x1:
        x = min(x1, x + rnd.uniform(0.4, 0.9) * m)
        borde += f' L{f(x)},{f(zy + rnd.uniform(-0.4, 0.4))}'
    out.append(f'<path d="{borde}" stroke="#000" stroke-width="{f(sw * 0.6)}" fill="none"/>')
    return ''.join(out)


def casa_lejos(x0, w_m, base, rnd, muro_m=3.0, techo_m=1.3, corredor=True, color=None,
               puertas=(), ventanas=(), pilares=None, cuatro_aguas=False, encima=''):
    """Casa de un nivel del otro lado de la plaza, con o sin corredor (doc 03 §3.1 [V])."""
    m, sw = ppm('lejos'), TRAZO['lejos']
    x1 = x0 + w_m * m
    y_alero = base - muro_m * m
    y_piso = base - (0.25 * m if corredor else 0)
    out = [muro_lejos(x0, x1, y_alero, y_piso, m, sw, rnd)]
    if corredor:
        out.append(f'<rect x="{f(x0)}" y="{f(y_alero)}" width="{f(x1 - x0)}" height="{f(y_piso - y_alero)}" fill="url(#t-fina)"/>')
    out.append(zocalo_lejos(x0, x1, y_piso, m, sw, rnd, color))
    out.append(huecos_lejos(x0, y_piso, m, sw, color, puertas, ventanas))
    out.append(encima)
    if corredor:
        y_viga = y_alero + 0.34 * m
        out.append(f'<rect x="{f(x0)}" y="{f(y_alero)}" width="{f(x1 - x0)}" height="{f(0.22 * m)}" fill="url(#t-densa)"/>')
        out.append(f'<rect x="{f(x0)}" y="{f(y_alero + 0.22 * m)}" width="{f(x1 - x0)}" height="{f(0.12 * m)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
        n = max(2, round(w_m / 2.7))
        for xp in pilares or [x0 + 0.15 * m + (x1 - x0 - 0.3 * m) * i / n for i in range(n + 1)]:
            pw = 0.2 * m
            out.append(f'<rect x="{f(xp - pw / 2)}" y="{f(y_viga)}" width="{f(pw)}" height="{f(y_piso - 0.28 * m - y_viga)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
            out.append(f'<path d="M{f(xp - 0.17 * m)},{f(y_piso)} L{f(xp - 0.14 * m)},{f(y_piso - 0.28 * m)} L{f(xp + 0.14 * m)},{f(y_piso - 0.28 * m)} L{f(xp + 0.17 * m)},{f(y_piso)} Z" fill="{lav("piedra", m)}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
            out.append(f'<line x1="{f(xp - 0.3 * m)}" y1="{f(y_viga + 0.5)}" x2="{f(xp + 0.3 * m)}" y2="{f(y_viga + 0.5)}" stroke="#000" stroke-width="{f(sw * 1.2)}"/>')
        out.append(f'<rect x="{f(x0)}" y="{f(y_piso)}" width="{f(x1 - x0)}" height="{f(base - y_piso)}" fill="{lav("piedra", m)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>'
                   f'<rect x="{f(x0)}" y="{f(y_piso + 0.1 * m)}" width="{f(x1 - x0)}" height="{f(base - y_piso - 0.1 * m)}" fill="url(#t-media)"/>')
    else:
        out.append(f'<rect x="{f(x0)}" y="{f(y_alero)}" width="{f(x1 - x0)}" height="{f(0.3 * m)}" fill="url(#t-media)"/>')
    out.append(tejado_lejos(x0, x1, y_alero, y_alero - techo_m * m, m, sw, rnd, cuatro_aguas))
    for xx in (x0, x1):
        out.append(f'<line x1="{f(xx)}" y1="{f(y_alero)}" x2="{f(xx)}" y2="{f(base)}" stroke="#000" stroke-width="{f(sw * 1.1)}"/>')
    return ''.join(out)


def casa_balcon_lejos(x0, w_m, base, rnd, color=None, puertas=(), ventanas=()):
    """Casa de dos pisos con balcón corrido de madera (tipología boyacense, doc 03 §3.1 [P])."""
    m, sw = ppm('lejos'), TRAZO['lejos']
    x1 = x0 + w_m * m
    y_alero = base - 6.3 * m
    y_bal = base - 3.3 * m
    bx0, bx1 = x0 + 0.5 * m, x1 - 0.5 * m
    out = [muro_lejos(x0, x1, y_alero, base, m, sw, rnd), zocalo_lejos(x0, x1, base, m, sw, rnd, color),
           huecos_lejos(x0, base, m, sw, color, puertas, ventanas)]
    # sombra del balcón sobre el primer piso
    out.append(f'<rect x="{f(bx0)}" y="{f(y_bal)}" width="{f(bx1 - bx0)}" height="{f(0.35 * m)}" fill="url(#t-media)"/>')
    # puertas del segundo piso que dan al balcón
    n = max(2, round((bx1 - bx0) / (2.6 * m)))
    for i in range(n):
        px = bx0 + (bx1 - bx0) * (i + 0.5) / n - 0.45 * m
        out.append(f'<rect x="{f(px)}" y="{f(y_bal - 2.15 * m)}" width="{f(0.9 * m)}" height="{f(2.15 * m)}" fill="{lav("madera", m)}" stroke="#000" stroke-width="{f(sw * 0.7)}"/>'
                   f'<rect x="{f(px)}" y="{f(y_bal - 2.15 * m)}" width="{f(0.9 * m)}" height="{f(2.15 * m)}" fill="url(#t-densa)"/>')
    # piso del balcón con canes, baranda de balaústres y pies derechos hasta el alero
    out.append(f'<rect x="{f(bx0 - 0.15 * m)}" y="{f(y_bal)}" width="{f(bx1 - bx0 + 0.3 * m)}" height="{f(0.16 * m)}" fill="{lav("madera", m)}" stroke="#000" stroke-width="{f(sw * 0.7)}"/>'
               f'<rect x="{f(bx0 - 0.15 * m)}" y="{f(y_bal)}" width="{f(bx1 - bx0 + 0.3 * m)}" height="{f(0.16 * m)}" fill="url(#t-madera)"/>')
    cx = bx0
    while cx <= bx1:
        out.append(f'<path d="M{f(cx - 0.08 * m)},{f(y_bal + 0.16 * m)} L{f(cx + 0.08 * m)},{f(y_bal + 0.16 * m)} L{f(cx)},{f(y_bal + 0.42 * m)} Z" fill="{lav("madera", m)}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
        cx += 1.2 * m
    bal, bx = [], bx0 + 0.08 * m
    while bx < bx1 - 0.05 * m:
        bal.append(f'<rect x="{f(bx)}" y="{f(y_bal - 0.9 * m)}" width="{f(0.055 * m)}" height="{f(0.9 * m)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw * 0.3)}"/>')
        bx += 0.16 * m
    out.extend(bal)
    out.append(f'<rect x="{f(bx0 - 0.1 * m)}" y="{f(y_bal - 0.98 * m)}" width="{f(bx1 - bx0 + 0.2 * m)}" height="{f(0.1 * m)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
    for i in range(n + 1):
        px = bx0 + (bx1 - bx0) * i / n
        out.append(f'<rect x="{f(px - 0.08 * m)}" y="{f(y_alero + 0.3 * m)}" width="{f(0.16 * m)}" height="{f(y_bal - y_alero - 0.3 * m)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
    out.append(f'<rect x="{f(x0)}" y="{f(y_alero)}" width="{f(x1 - x0)}" height="{f(0.3 * m)}" fill="url(#t-densa)"/>')
    out.append(tejado_lejos(x0, x1, y_alero, y_alero - 1.3 * m, m, sw, rnd))
    for xx in (x0, x1):
        out.append(f'<line x1="{f(xx)}" y1="{f(y_alero)}" x2="{f(xx)}" y2="{f(base)}" stroke="#000" stroke-width="{f(sw * 1.1)}"/>')
    return ''.join(out)


def calle_lejos(x0, w_m, base, rnd):
    """Boca de calle: al fondo, casas más pequeñas (≈18 px/m) y más claras."""
    m2, sw = 18, TRAZO['lejos'] * 0.8
    W = w_m * ppm('lejos')
    base2 = base - 19  # suelo de un plano a paralaje ≈0,09
    id_clip = f'c-calle-{int(x0)}'
    out = [f'<clipPath id="{id_clip}"><rect x="{f(x0)}" y="0" width="{f(W)}" height="{f(base)}"/></clipPath>',
           f'<g clip-path="url(#{id_clip})">',
           f'<rect x="{f(x0)}" y="{f(base2)}" width="{f(W)}" height="{f(base - base2)}" fill="{lav("tierra", m2)}"/>',
           f'<rect x="{f(x0)}" y="{f(base2)}" width="{f(W)}" height="{f(base - base2)}" fill="url(#t-puntos-ralos)"/>']
    x = x0 - rnd.uniform(0.5, 2) * m2
    while x < x0 + W:
        cw, alto = rnd.uniform(3.5, 6) * m2, rnd.uniform(2.7, 3.3) * m2
        ya = base2 - alto
        out.append(f'<rect x="{f(x)}" y="{f(ya)}" width="{f(cw)}" height="{f(alto)}" fill="{lav("cal", m2)}" stroke="#000" stroke-width="{f(sw * 0.7)}"/>')
        out.append(f'<rect x="{f(x + cw * 0.3)}" y="{f(base2 - 2 * m2)}" width="{f(m2)}" height="{f(2 * m2)}" fill="url(#t-cruz)" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
        out.append(f'<rect x="{f(x + cw * 0.65)}" y="{f(base2 - 1.9 * m2)}" width="{f(0.8 * m2)}" height="{f(0.9 * m2)}" fill="url(#t-cruz)" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
        out.append(f'<rect x="{f(x)}" y="{f(ya)}" width="{f(cw)}" height="{f(0.25 * m2)}" fill="url(#t-media)"/>')
        techo = [(x - 0.2 * m2, ya), (x + cw + 0.2 * m2, ya), (x + cw + 0.1 * m2, ya - 1.1 * m2), (x - 0.1 * m2, ya - 1.1 * m2)]
        out.append(f'<polygon points="{pts(techo)}" fill="{lav("teja", m2)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/><polygon points="{pts(techo)}" fill="url(#t-fina)"/>')
        x += cw
    out.append('</g>')
    # esquinas de las casas que forman la boca de la calle
    out.append(f'<line x1="{f(x0)}" y1="{f(base2 - 4 * m2)}" x2="{f(x0)}" y2="{f(base)}" stroke="#000" stroke-width="{f(sw)}"/>')
    return ''.join(out)


def tienda_azul(x0, base, rnd):
    """Tienda de los azules (conservadores), al otro lado de la plaza, frente a la roja."""
    m, sw = ppm('lejos'), TRAZO['lejos']
    y_piso = base - 0.25 * m
    rotulo = letras_pintadas('TIENDA', x0 + 3.55 * m, y_piso - 2.42 * m, 0.42 * m, sw * 2.0, AZUL)
    cartel = afiche(x0 + 1.0 * m, y_piso - 2.0 * m, 0.7 * m, 0.95 * m, m, sw, rnd, color=AZUL, estrella=False)
    # parroquianos en el corredor, mirando hacia la plaza (y hacia la tienda roja)
    gente = (persona(x0 + 6.4 * m, y_piso, m, sw, 'hombre', ruana='oscura', sombrero='negro', panuelo=AZUL)
             + persona(x0 + 7.3 * m, y_piso, m, sw, 'hombre', espejo=True, ruana='clara', sombrero='paja')
             + persona(x0 + 11.2 * m, y_piso, m, sw, 'hombre', ruana='gris', sombrero='negro'))
    return casa_lejos(x0, 12.0, base, rnd, muro_m=3.65, techo_m=1.4, corredor=True, color=AZUL,
                      puertas=[(3.3, 1.9, 2.15, True), (9.5, 1.0, 2.05, False)],
                      ventanas=[(6.9 - 0.3, 1.2, 1.1, 0.95)],
                      pilares=[x0 + 0.2 * m, x0 + 2.6 * m, x0 + 5.6 * m, x0 + 8.6 * m, x0 + 11.8 * m],
                      encima=rotulo + cartel + gente)


def iglesia():
    """Iglesia de una nave con torre a la derecha, sobre atrio con gradas (tipología del norte
    de Boyacá, p. ej. La Uvita; Puente Alto no la copia) [P]. Base del viewBox = suelo lejano."""
    rnd = random.Random(1600)
    m, sw = ppm('lejos'), TRAZO['lejos']
    W, H = 420, 560
    base = H
    y_atrio = base - 1.0 * m
    fx0, fx1 = 14, 14 + 8.8 * m
    cx = (fx0 + fx1) / 2
    tx0, tx1 = fx1, fx1 + 4.4 * m
    y_cornisa = y_atrio - 9.5 * m
    y_pico = y_cornisa - 2.6 * m
    out = ['<g data-p="iglesia: tipología colonial del norte de Boyacá, sin copiar una iglesia real">']
    # --- fachada
    fachada = [(fx0, y_atrio), (fx0, y_cornisa), (cx, y_pico), (fx1, y_cornisa), (fx1, y_atrio)]
    remate = [(fx0 - 0.25 * m, y_cornisa - 0.35 * m), (cx, y_pico - 0.4 * m), (fx1 + 0.25 * m, y_cornisa - 0.35 * m)]
    cal, piedra_ = lav('cal', m), lav('piedra', m, 0.8)
    out.append(f'<polygon points="{pts(remate)}" fill="{cal}"/>')
    out.append(f'<polygon points="{pts(fachada)}" fill="{cal}" stroke="#000" stroke-width="{f(sw)}"/>')
    out.append(f'<rect x="{f(fx0)}" y="{f(y_atrio - 0.6 * m)}" width="{f(fx1 - fx0)}" height="{f(0.6 * m)}" fill="url(#t-puntos-ralos)"/>')
    # pilastras de esquina con su canto en sombra
    for px in (fx0, fx1 - 0.6 * m):
        out.append(f'<rect x="{f(px)}" y="{f(y_cornisa)}" width="{f(0.6 * m)}" height="{f(y_atrio - y_cornisa)}" fill="none" stroke="#000" stroke-width="{f(sw * 0.6)}"/>'
                   f'<rect x="{f(px + 0.42 * m)}" y="{f(y_cornisa)}" width="{f(0.18 * m)}" height="{f(y_atrio - y_cornisa)}" fill="url(#t-fina)"/>')
    # grietas y desconchados de la cal
    out.append(muro_lejos(fx0 + 0.7 * m, fx1 - 0.7 * m, y_cornisa + 0.5 * m, y_atrio, m, sw, rnd, fondo=False))
    # cornisa y frontón con su sombra
    out.append(f'<rect x="{f(fx0 - 0.25 * m)}" y="{f(y_cornisa - 0.35 * m)}" width="{f(fx1 - fx0 + 0.5 * m)}" height="{f(0.35 * m)}" fill="{cal}" stroke="#000" stroke-width="{f(sw * 0.8)}"/>'
               f'<rect x="{f(fx0)}" y="{f(y_cornisa)}" width="{f(fx1 - fx0)}" height="{f(0.18 * m)}" fill="url(#t-media)"/>')
    out.append(f'<path d="M{f(fx0 - 0.25 * m)},{f(y_cornisa - 0.35 * m)} L{f(cx)},{f(y_pico - 0.4 * m)} L{f(fx1 + 0.25 * m)},{f(y_cornisa - 0.35 * m)}" stroke="#000" stroke-width="{f(sw * 1.2)}" fill="none"/>'
               f'<path d="M{f(fx0 + 0.3 * m)},{f(y_cornisa - 0.35 * m)} L{f(cx)},{f(y_pico - 0.05 * m)} L{f(fx1 - 0.3 * m)},{f(y_cornisa - 0.35 * m)}" stroke="#000" stroke-width="{f(sw * 0.6)}" fill="none"/>')
    # óculo del frontón y cruz de remate
    out.append(f'<circle cx="{f(cx)}" cy="{f(y_cornisa - 1.15 * m)}" r="{f(0.32 * m)}" fill="{piedra_}" stroke="#000" stroke-width="{f(sw * 0.8)}"/>'
               f'<circle cx="{f(cx)}" cy="{f(y_cornisa - 1.15 * m)}" r="{f(0.22 * m)}" fill="url(#t-densa)"/>')
    out.append(f'<rect x="{f(cx - 0.3 * m)}" y="{f(y_pico - 0.6 * m)}" width="{f(0.6 * m)}" height="{f(0.25 * m)}" fill="{piedra_}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>'
               f'<path d="M{f(cx)},{f(y_pico - 0.6 * m)} L{f(cx)},{f(y_pico - 2.0 * m)} M{f(cx - 0.4 * m)},{f(y_pico - 1.55 * m)} L{f(cx + 0.4 * m)},{f(y_pico - 1.55 * m)}" stroke="#000" stroke-width="{f(sw * 1.8)}"/>')
    # --- portada de piedra: arco de medio punto entre pilastras, entablamento y hornacina
    pw, pr = 2.4 * m, 1.2 * m
    y_arranque = y_atrio - 3.0 * m
    piedra = f'fill="{piedra_}" stroke="#000"'
    out.append(f'<rect x="{f(cx - 2.6 * m)}" y="{f(y_atrio - 5.6 * m)}" width="{f(5.2 * m)}" height="{f(5.6 * m)}" fill="{lav("piedra", m, 0.6)}"/>'
               f'<rect x="{f(cx - 2.6 * m)}" y="{f(y_atrio - 5.6 * m)}" width="{f(5.2 * m)}" height="{f(5.6 * m)}" fill="url(#t-puntos-ralos)"/>')
    for sx in (-1, 1):
        px = cx + sx * (pw / 2 + 0.55 * m) - 0.22 * m
        out.append(f'<rect x="{f(px)}" y="{f(y_atrio - 5.0 * m)}" width="{f(0.45 * m)}" height="{f(5.0 * m)}" {piedra} stroke-width="{f(sw * 0.7)}"/>'
                   f'<rect x="{f(px - 0.08 * m)}" y="{f(y_atrio - 5.1 * m)}" width="{f(0.61 * m)}" height="{f(0.2 * m)}" {piedra} stroke-width="{f(sw * 0.6)}"/>'
                   f'<rect x="{f(px + 0.3 * m)}" y="{f(y_atrio - 4.9 * m)}" width="{f(0.15 * m)}" height="{f(4.9 * m)}" fill="url(#t-fina)"/>')
    arco = (f'M{f(cx - pw / 2)},{f(y_atrio)} L{f(cx - pw / 2)},{f(y_arranque)} A{f(pr)},{f(pr)} 0 0 1 {f(cx + pw / 2)},{f(y_arranque)} '
            f'L{f(cx + pw / 2)},{f(y_atrio)} Z')
    out.append(f'<path d="{arco}" fill="{lav("madera", m)}"/><path d="{arco}" fill="url(#t-densa)"/>')
    # hojas de la puerta abiertas hacia adentro y dovelas del arco
    for hx in (cx - pw / 2, cx + pw / 2 - 0.35 * m):
        out.append(f'<rect x="{f(hx)}" y="{f(y_arranque)}" width="{f(0.35 * m)}" height="{f(y_atrio - y_arranque)}" fill="{lav("madera", m)}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>'
                   f'<rect x="{f(hx)}" y="{f(y_arranque)}" width="{f(0.35 * m)}" height="{f(y_atrio - y_arranque)}" fill="url(#t-madera-v)"/>')
    ra = pr + 0.4 * m
    out.append(f'<path d="M{f(cx - pw / 2 - 0.4 * m)},{f(y_arranque)} A{f(ra)},{f(ra)} 0 0 1 {f(cx + pw / 2 + 0.4 * m)},{f(y_arranque)} '
               f'L{f(cx + pw / 2)},{f(y_arranque)} A{f(pr)},{f(pr)} 0 0 0 {f(cx - pw / 2)},{f(y_arranque)} Z" {piedra} stroke-width="{f(sw * 0.7)}"/>')
    dovelas = []
    for i in range(1, 9):
        a = math.pi * i / 9
        dovelas.append(f'M{f(cx - math.cos(a) * pr)},{f(y_arranque - math.sin(a) * pr)} L{f(cx - math.cos(a) * ra)},{f(y_arranque - math.sin(a) * ra)}')
    out.append(f'<path d="{" ".join(dovelas)}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
    out.append(f'<path d="{arco}" fill="none" stroke="#000" stroke-width="{f(sw * 0.9)}"/>')
    y_ent = y_atrio - 5.6 * m
    out.append(f'<rect x="{f(cx - 2.7 * m)}" y="{f(y_ent)}" width="{f(5.4 * m)}" height="{f(0.5 * m)}" {piedra} stroke-width="{f(sw * 0.8)}"/>'
               f'<rect x="{f(cx - 2.6 * m)}" y="{f(y_ent + 0.5 * m)}" width="{f(5.2 * m)}" height="{f(0.12 * m)}" fill="url(#t-media)"/>')
    # hornacina con la imagen del santo (silueta, sin rasgos) y pináculos
    hw, hh = 0.8 * m, 1.4 * m
    y_h = y_ent - 0.3 * m
    out.append(f'<path d="M{f(cx - hw / 2)},{f(y_h)} L{f(cx - hw / 2)},{f(y_h - hh + hw / 2)} A{f(hw / 2)},{f(hw / 2)} 0 0 1 {f(cx + hw / 2)},{f(y_h - hh + hw / 2)} L{f(cx + hw / 2)},{f(y_h)} Z" fill="{cal}" stroke="#000" stroke-width="{f(sw * 0.7)}"/>'
               f'<path d="M{f(cx - hw / 2)},{f(y_h)} L{f(cx - hw / 2)},{f(y_h - hh + hw / 2)} A{f(hw / 2)},{f(hw / 2)} 0 0 1 {f(cx + hw / 2)},{f(y_h - hh + hw / 2)} L{f(cx + hw / 2)},{f(y_h)} Z" fill="url(#t-cruz)"/>')
    out.append(f'<path d="M{f(cx - 0.18 * m)},{f(y_h)} L{f(cx - 0.12 * m)},{f(y_h - 0.95 * m)} L{f(cx + 0.12 * m)},{f(y_h - 0.95 * m)} L{f(cx + 0.18 * m)},{f(y_h)} Z" fill="{lav("piedra", m, 0.6)}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>'
               f'<circle cx="{f(cx)}" cy="{f(y_h - 1.08 * m)}" r="{f(0.12 * m)}" fill="{lav("piedra", m, 0.6)}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>'
               f'<path d="M{f(cx - 0.2 * m)},{f(y_h - 1.1 * m)} A{f(0.2 * m)},{f(0.2 * m)} 0 0 1 {f(cx + 0.2 * m)},{f(y_h - 1.1 * m)}" stroke="#000" stroke-width="{f(sw * 0.4)}" fill="none"/>')
    for sx in (-1, 1):
        pxn = cx + sx * 2.3 * m
        out.append(f'<path d="M{f(pxn - 0.12 * m)},{f(y_ent)} L{f(pxn - 0.12 * m)},{f(y_ent - 0.3 * m)} L{f(pxn + 0.12 * m)},{f(y_ent - 0.3 * m)} L{f(pxn + 0.12 * m)},{f(y_ent)} Z" fill="{piedra_}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>'
                   f'<circle cx="{f(pxn)}" cy="{f(y_ent - 0.45 * m)}" r="{f(0.15 * m)}" fill="{piedra_}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
    # ventana del coro
    vy = y_atrio - 9.05 * m
    out.append(f'<path d="M{f(cx - 0.5 * m)},{f(vy + 1.3 * m)} L{f(cx - 0.5 * m)},{f(vy + 0.5 * m)} A{f(0.5 * m)},{f(0.5 * m)} 0 0 1 {f(cx + 0.5 * m)},{f(vy + 0.5 * m)} L{f(cx + 0.5 * m)},{f(vy + 1.3 * m)} Z" fill="{piedra_}" stroke="#000" stroke-width="{f(sw * 0.8)}"/>'
               f'<path d="M{f(cx - 0.4 * m)},{f(vy + 1.25 * m)} L{f(cx - 0.4 * m)},{f(vy + 0.55 * m)} A{f(0.4 * m)},{f(0.4 * m)} 0 0 1 {f(cx + 0.4 * m)},{f(vy + 0.55 * m)} L{f(cx + 0.4 * m)},{f(vy + 1.25 * m)} Z" fill="url(#t-densa)"/>'
               f'<path d="M{f(cx)},{f(vy + 0.2 * m)} L{f(cx)},{f(vy + 1.25 * m)} M{f(cx - 0.4 * m)},{f(vy + 0.8 * m)} L{f(cx + 0.4 * m)},{f(vy + 0.8 * m)}" stroke="#fff" stroke-width="{f(sw * 0.6)}"/>')
    # --- torre: cuerpo, campanario con campana, cupulín con linterna y cruz
    y_t1 = y_atrio - 11.4 * m
    y_t2 = y_t1 - 3.1 * m
    out.append(f'<rect x="{f(tx0)}" y="{f(y_t1)}" width="{f(tx1 - tx0)}" height="{f(y_atrio - y_t1)}" fill="{cal}" stroke="#000" stroke-width="{f(sw)}"/>'
               f'<rect x="{f(tx1 - 0.5 * m)}" y="{f(y_t1)}" width="{f(0.5 * m)}" height="{f(y_atrio - y_t1)}" fill="url(#t-fina)"/>'
               f'<rect x="{f(tx0)}" y="{f(y_atrio - 0.6 * m)}" width="{f(tx1 - tx0)}" height="{f(0.6 * m)}" fill="url(#t-puntos-ralos)"/>')
    for yy in (y_atrio - 6.0 * m, y_t1 + 0.3 * m):
        out.append(f'<rect x="{f(tx0 - 0.15 * m)}" y="{f(yy - 0.3 * m)}" width="{f(tx1 - tx0 + 0.3 * m)}" height="{f(0.3 * m)}" fill="{cal}" stroke="#000" stroke-width="{f(sw * 0.7)}"/>'
                   f'<rect x="{f(tx0)}" y="{f(yy)}" width="{f(tx1 - tx0)}" height="{f(0.14 * m)}" fill="url(#t-media)"/>')
    tcx = (tx0 + tx1) / 2
    out.append(f'<rect x="{f(tcx - 0.45 * m)}" y="{f(y_atrio - 1.95 * m)}" width="{f(0.9 * m)}" height="{f(1.95 * m)}" fill="{lav("madera", m)}" stroke="#000" stroke-width="{f(sw * 0.7)}"/>'
               f'<rect x="{f(tcx - 0.45 * m)}" y="{f(y_atrio - 1.95 * m)}" width="{f(0.9 * m)}" height="{f(1.95 * m)}" fill="url(#t-madera-v)"/>'
               f'<rect x="{f(tcx - 0.1 * m)}" y="{f(y_atrio - 4.6 * m)}" width="{f(0.2 * m)}" height="{f(0.9 * m)}" fill="url(#t-densa)" stroke="#000" stroke-width="{f(sw * 0.5)}"/>'
               f'<rect x="{f(tcx - 0.35 * m)}" y="{f(y_atrio - 9.4 * m)}" width="{f(0.7 * m)}" height="{f(1.1 * m)}" fill="url(#t-densa)" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
    # campanario
    out.append(f'<rect x="{f(tx0 + 0.1 * m)}" y="{f(y_t2)}" width="{f(tx1 - tx0 - 0.2 * m)}" height="{f(y_t1 - y_t2)}" fill="{cal}" stroke="#000" stroke-width="{f(sw)}"/>'
               f'<rect x="{f(tx1 - 0.6 * m)}" y="{f(y_t2)}" width="{f(0.5 * m)}" height="{f(y_t1 - y_t2)}" fill="url(#t-fina)"/>')
    aw, ar = 2.0 * m, 1.0 * m
    y_arr = y_t1 - 0.3 * m - 1.3 * m
    vano = f'M{f(tcx - aw / 2)},{f(y_t1 - 0.3 * m)} L{f(tcx - aw / 2)},{f(y_arr)} A{f(ar)},{f(ar)} 0 0 1 {f(tcx + aw / 2)},{f(y_arr)} L{f(tcx + aw / 2)},{f(y_t1 - 0.3 * m)} Z'
    out.append(f'<path d="{vano}" fill="{lav("madera", m)}"/><path d="{vano}" fill="url(#t-densa)"/><path d="{vano}" fill="none" stroke="#000" stroke-width="{f(sw * 0.8)}"/>')
    yb = y_arr - 0.55 * m
    campana = (f'M{f(tcx - 0.12 * m)},{f(yb)} Q{f(tcx - 0.3 * m)},{f(yb + 0.1 * m)} {f(tcx - 0.32 * m)},{f(yb + 0.7 * m)} L{f(tcx - 0.45 * m)},{f(yb + 0.9 * m)} '
               f'L{f(tcx + 0.45 * m)},{f(yb + 0.9 * m)} L{f(tcx + 0.32 * m)},{f(yb + 0.7 * m)} Q{f(tcx + 0.3 * m)},{f(yb + 0.1 * m)} {f(tcx + 0.12 * m)},{f(yb)} Z')
    out.append(f'<path d="M{f(tcx - aw / 2)},{f(yb - 0.08 * m)} L{f(tcx + aw / 2)},{f(yb - 0.08 * m)}" stroke="#000" stroke-width="{f(sw * 1.2)}"/>'
               f'<path d="{campana}" fill="#000" stroke="#fff" stroke-width="{f(sw * 0.4)}"/>')
    out.append(f'<rect x="{f(tx0 - 0.2 * m)}" y="{f(y_t2 - 0.35 * m)}" width="{f(tx1 - tx0 + 0.4 * m)}" height="{f(0.35 * m)}" fill="{cal}" stroke="#000" stroke-width="{f(sw * 0.8)}"/>'
               f'<rect x="{f(tx0 + 0.1 * m)}" y="{f(y_t2)}" width="{f(tx1 - tx0 - 0.2 * m)}" height="{f(0.15 * m)}" fill="url(#t-media)"/>')
    for px in (tx0 + 0.1 * m, tx1 - 0.1 * m):
        out.append(f'<path d="M{f(px - 0.12 * m)},{f(y_t2 - 0.35 * m)} L{f(px - 0.08 * m)},{f(y_t2 - 0.75 * m)} L{f(px + 0.08 * m)},{f(y_t2 - 0.75 * m)} L{f(px + 0.12 * m)},{f(y_t2 - 0.35 * m)} Z" fill="{piedra_}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>'
                   f'<circle cx="{f(px)}" cy="{f(y_t2 - 0.9 * m)}" r="{f(0.16 * m)}" fill="{piedra_}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
    # cupulín de teja sobre tambor, linterna y cruz
    y_tam = y_t2 - 0.35 * m
    out.append(f'<rect x="{f(tx0 + 0.6 * m)}" y="{f(y_tam - 0.45 * m)}" width="{f(tx1 - tx0 - 1.2 * m)}" height="{f(0.45 * m)}" fill="{cal}" stroke="#000" stroke-width="{f(sw * 0.7)}"/>')
    rw, rh = (tx1 - tx0) / 2 - 0.7 * m, 1.25 * m
    y_c = y_tam - 0.45 * m
    cupula = f'M{f(tcx - rw)},{f(y_c)} A{f(rw)},{f(rh)} 0 0 1 {f(tcx + rw)},{f(y_c)} Z'
    out.append(f'<path d="{cupula}" fill="{lav("teja", m)}"/><path d="{cupula}" fill="url(#t-fina)"/>')
    meridianos = ' '.join(f'M{f(tcx + rw * u)},{f(y_c)} Q{f(tcx + rw * u * 0.85)},{f(y_c - rh * 0.8)} {f(tcx)},{f(y_c - rh)}' for u in (-0.6, -0.25, 0.25, 0.6))
    out.append(f'<path d="{meridianos}" stroke="#000" stroke-width="{f(sw * 0.45)}" fill="none"/><path d="{cupula}" fill="none" stroke="#000" stroke-width="{f(sw * 0.9)}"/>')
    y_l = y_c - rh
    out.append(f'<rect x="{f(tcx - 0.22 * m)}" y="{f(y_l - 0.55 * m)}" width="{f(0.44 * m)}" height="{f(0.55 * m)}" fill="{cal}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>'
               f'<rect x="{f(tcx - 0.08 * m)}" y="{f(y_l - 0.45 * m)}" width="{f(0.16 * m)}" height="{f(0.35 * m)}" fill="#000"/>'
               f'<path d="M{f(tcx - 0.3 * m)},{f(y_l - 0.55 * m)} Q{f(tcx)},{f(y_l - 0.95 * m)} {f(tcx + 0.3 * m)},{f(y_l - 0.55 * m)} Z" fill="{lav("teja", m)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>'
               f'<path d="M{f(tcx)},{f(y_l - 0.85 * m)} L{f(tcx)},{f(y_l - 2.1 * m)} M{f(tcx - 0.35 * m)},{f(y_l - 1.7 * m)} L{f(tcx + 0.35 * m)},{f(y_l - 1.7 * m)}" stroke="#000" stroke-width="{f(sw * 1.6)}"/>')
    # --- atrio de piedra con gradas, cruz atrial y feligreses
    out.append(f'<rect x="0" y="{f(y_atrio)}" width="{W}" height="{f(base - y_atrio)}" fill="{lav("piedra", m)}" stroke="#000" stroke-width="{f(sw)}"/>'
               f'<rect x="0" y="{f(y_atrio)}" width="{W}" height="{f(base - y_atrio)}" fill="url(#t-puntos-ralos)"/>')
    juntas, yy, fila = [], y_atrio + 0.33 * m, 0
    while yy < base - 1:
        juntas.append(f'M0,{f(yy)} L{W},{f(yy)}')
        xx = (fila % 2) * 0.5 * m
        while xx < W:
            juntas.append(f'M{f(xx)},{f(yy - 0.33 * m)} L{f(xx)},{f(yy)}')
            xx += rnd.uniform(0.8, 1.3) * m
        yy += 0.33 * m
        fila += 1
    out.append(f'<path d="{" ".join(juntas)}" stroke="#000" stroke-width="{f(sw * 0.4)}"/>')
    for i in range(4):
        gy = y_atrio + i * 0.25 * m
        gw = 4.4 * m + i * 0.5 * m
        out.append(f'<rect x="{f(cx - gw / 2)}" y="{f(gy)}" width="{f(gw)}" height="{f(0.25 * m)}" fill="{lav("piedra", m, 0.7)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>'
                   f'<rect x="{f(cx - gw / 2)}" y="{f(gy + 0.08 * m)}" width="{f(gw)}" height="{f(0.17 * m)}" fill="url(#t-fina)"/>')
    kx = fx0 + 1.4 * m
    out.append(f'<path d="M{f(kx - 0.5 * m)},{f(y_atrio)} L{f(kx - 0.5 * m)},{f(y_atrio - 0.3 * m)} L{f(kx - 0.3 * m)},{f(y_atrio - 0.3 * m)} L{f(kx - 0.3 * m)},{f(y_atrio - 0.6 * m)} '
               f'L{f(kx + 0.3 * m)},{f(y_atrio - 0.6 * m)} L{f(kx + 0.3 * m)},{f(y_atrio - 0.3 * m)} L{f(kx + 0.5 * m)},{f(y_atrio - 0.3 * m)} L{f(kx + 0.5 * m)},{f(y_atrio)} Z" fill="{piedra_}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>'
               f'<path d="M{f(kx)},{f(y_atrio - 0.6 * m)} L{f(kx)},{f(y_atrio - 3.2 * m)} M{f(kx - 0.55 * m)},{f(y_atrio - 2.5 * m)} L{f(kx + 0.55 * m)},{f(y_atrio - 2.5 * m)}" stroke="#000" stroke-width="{f(sw * 2.4)}"/>'
               f'<path d="M{f(kx)},{f(y_atrio - 0.6 * m)} L{f(kx)},{f(y_atrio - 3.2 * m)} M{f(kx - 0.55 * m)},{f(y_atrio - 2.5 * m)} L{f(kx + 0.55 * m)},{f(y_atrio - 2.5 * m)}" stroke="{piedra_}" stroke-width="{f(sw * 0.9)}"/>')
    out.append(persona(cx - 1.2 * m, y_atrio, m, sw, 'mujer', sombrero='negro'))
    out.append(persona(cx + 3.4 * m, base, m, sw, 'mujer', espejo=True, sombrero='paja', lleva='canasto'))
    out.append('</g>')
    archivo('iglesia', W, H, 'lejos', 'iglesia de una nave con torre, atrio y gradas', '\n'.join(out),
            notas='Se coloca con la base en el suelo lejano (y=628). Sin color: la Iglesia no lleva acento partidista.')


def lejos_oeste():
    rnd = random.Random(1810)
    m = ppm('lejos')
    W, base = 1340, 260
    cuerpo = [calle_lejos(610, 180 / m, base, rnd), calle_lejos(1150, 190 / m, base, rnd),
              casa_lejos(0, 230 / m, base, rnd, muro_m=3.1, techo_m=1.3,
                         puertas=[(1.4, 1.1, 2.1, False), (5.2, 1.1, 2.1, True)], ventanas=[(3.0, 0.9, 1.0, 1.0)]),
              casa_balcon_lejos(230, 380 / m, base, rnd, puertas=[(2.0, 1.2, 2.2, False), (8.6, 1.0, 2.1, True)],
                                ventanas=[(4.6, 1.0, 1.1, 0.95), (11.0, 0.9, 1.1, 0.95)]),
              tienda_azul(790, base, rnd)]
    archivo('lejos-oeste', W, base, 'lejos', 'otro lado de la plaza (oeste): casas, boca de calle y tienda azul',
            '\n'.join(cuerpo), notas='Azul en zócalo, puertas, postigos, rótulo, afiche y un pañuelo: tienda conservadora (doc 03 §1). '
                                     'Va de lx 0 a 1340; la iglesia sigue en lx 1340.')


def lejos_este():
    rnd = random.Random(1820)
    m = ppm('lejos')
    W, base = 1034, 260
    cuerpo = [calle_lejos(300, 150 / m, base, rnd),
              casa_balcon_lejos(0, 300 / m, base, rnd, puertas=[(4.2, 1.4, 2.3, False)], ventanas=[(1.4, 1.0, 1.1, 0.95), (7.6, 1.0, 1.1, 0.95)]),
              casa_lejos(450, 310 / m, base, rnd, muro_m=2.9, techo_m=1.25, cuatro_aguas=True,
                         puertas=[(2.2, 1.0, 2.0, True), (7.4, 1.0, 2.0, False)], ventanas=[(4.6, 1.0, 1.0, 1.0)]),
              casa_lejos(760, 274 / m, base, rnd, muro_m=3.2, techo_m=1.3, corredor=False,
                         puertas=[(3.6, 1.1, 2.1, False)], ventanas=[(1.2, 0.9, 1.1, 0.95), (6.0, 0.9, 1.1, 0.95)]),
              persona(560, base, m, TRAZO['lejos'], 'mujer', espejo=True, sombrero='negro', lleva='paraguas'),
              persona(890, base, m, TRAZO['lejos'], 'hombre', ruana='gris', sombrero='paja', lleva='vara')]
    archivo('lejos-este', W, base, 'lejos', 'otro lado de la plaza (este): casa cural, boca de calle y casas',
            '\n'.join(cuerpo), notas='Va de lx 1750 a 2784, junto a la torre.')


def suelo_plaza(nombre, capa, H, semilla):
    """Mosaico de suelo de la plaza en una capa lejana (repetible cada 1024 px). Las piedras
    crecen con la perspectiva (alto ∝ (y−horizonte)², ancho ∝ y−horizonte) y a lo lejos
    quedan solo como la raya de sombra de su borde."""
    rnd = random.Random(semilla)
    sw, m = TRAZO[capa], ppm(capa)
    W = 1024
    y0 = 580 + 320 * PARALAJE[capa]
    out = ['<g data-p="plaza empedrada o de tierra: confirmar con fotos del norte de Boyacá años 40">',
           f'<rect x="0" y="0" width="{W}" height="{H}" fill="{lav("tierra", m, 0.8)}"/>',
           f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#t-puntos-ralos)"/>']
    rayas, piedras = [], []
    y = 1.0
    while y < H:
        prof = (y0 + y - 580) / 320
        alto = max(1.0, 13 * prof ** 2)
        # anchos de la fila escalados para que sumen exactamente W: el mosaico no tiene costura
        anchos, total = [], 0.0
        while total < W:
            a = alto * rnd.uniform(1.2, 1.9) / prof
            g = rnd.uniform(1.0, 3.0) * max(0.6, prof * 2)
            anchos.append((a, g))
            total += a + g
        k = W / total
        x = rnd.uniform(0, W)
        for a, g in anchos:
            a, g = a * k, g * k
            # lo aleatorio se decide una vez por piedra: sus dos mitades en la costura coinciden
            visible = alto >= 4.5 or rnd.random() < 0.2 + alto / 6
            jit = [rnd.uniform(0.86, 1.08) for _ in range(8)]
            for dx in (0, -W):
                xx = x + dx
                if xx + a < 0 or xx > W or not visible:
                    continue
                if alto < 4.5:
                    rayas.append(f'M{f(xx + a * 0.12)},{f(y + alto)} h{f(a * 0.76)}')
                else:
                    cy, rx, ry = y + alto * 0.5, a * 0.47, alto * 0.43
                    p = [(xx + a / 2 + math.cos(i * math.pi / 4) * rx * jit[i],
                          cy + math.sin(i * math.pi / 4) * ry * jit[i]) for i in range(8)]
                    d = 'M' + ' Q'.join(f'{f(p[i][0])},{f(p[i][1])} {f((p[i][0] + p[(i + 1) % 8][0]) / 2)},{f((p[i][1] + p[(i + 1) % 8][1]) / 2)}' for i in range(8)) + ' Z'
                    piedras.append(f'<path d="{d}" fill="{lav("piedra", m, 0.75)}" stroke="#000" stroke-width="{f(sw * 0.45)}"/>'
                                   f'<path d="M{f(xx + a * 0.2)},{f(cy + ry * 0.35)} Q{f(xx + a / 2)},{f(cy + ry * 1.05)} {f(xx + a * 0.8)},{f(cy + ry * 0.35)} Q{f(xx + a / 2)},{f(cy + ry * 0.65)} {f(xx + a * 0.2)},{f(cy + ry * 0.35)} Z" fill="url(#t-media)"/>')
            x += a + g
            if x > W:
                x -= W
        y += alto + max(2.4, 1.6 * prof)
    out.append(f'<path d="{" ".join(rayas)}" stroke="#000" stroke-width="{f(sw * 0.4)}"/>')
    out.extend(piedras)
    out.append('</g>')
    archivo(nombre, W, H, capa, f'suelo de la plaza (mosaico, capa {capa})', '\n'.join(out),
            notas=f'Se coloca arriba, en el suelo de la capa (y={f(y0)}), y se repite cada 1024 px.')


# ============================== capa medio (0,45 · 90 px/m) ==============================
# El mercado (Hernán Díaz, "Mercado campesino en Boyacá", BanRep, hacia 1960; detalles de 1946 [P]):
# tendidos en el suelo, toldos de lona sobre palos, mulas, gente sin rostro, pila de piedra.

def monton(cx, base, m, sw, rnd, filas=3, r=0.045, clase='papa'):
    """Montoncito de venta (papas, cebollas, coles, cubios) apilado en pirámide."""
    tono = lav({'papa': 'tapia', 'cebolla': 'cebada', 'col': 'potrero', 'cubio': 'trigo'}[clase], m)
    out = []
    for fila in range(filas):
        n = filas - fila
        for i in range(n):
            px = cx + (i - (n - 1) / 2) * r * 2.05 * m + rnd.uniform(-0.15, 0.15) * r * m
            py = base - r * m - fila * r * 1.7 * m
            if clase == 'cebolla':
                out.append(f'<path d="M{f(px)},{f(py - r * m)} Q{f(px + rnd.uniform(-1, 1) * r * m)},{f(py - r * 3 * m)} {f(px + rnd.uniform(-2, 2) * r * m)},{f(py - r * 4.5 * m)}" stroke="#000" stroke-width="{f(sw * 0.45)}" fill="none"/>')
            out.append(f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="{f(r * m * 1.08)}" ry="{f(r * m)}" fill="{tono}" stroke="#000" stroke-width="{f(sw * 0.4)}"/>')
            if clase == 'papa':
                out.append(f'<circle cx="{f(px + r * m * 0.3)}" cy="{f(py - r * m * 0.2)}" r="{f(r * m * 0.14)}" fill="#000"/>')
            else:
                out.append(f'<path d="M{f(px - r * m * 0.5)},{f(py + r * m * 0.2)} Q{f(px)},{f(py + r * m * 0.9)} {f(px + r * m * 0.5)},{f(py + r * m * 0.2)}" fill="url(#t-media)"/>')
    return ''.join(out)


def manta_suelo(x0, x1, base, m, sw):
    """Costal abierto o manta tendida en el suelo, vista casi de canto."""
    h = 0.07 * m
    return (f'<path d="M{f(x0)},{f(base)} L{f(x1)},{f(base)} L{f(x1 - 0.12 * m)},{f(base - h)} L{f(x0 + 0.1 * m)},{f(base - h)} Z" fill="{lav("lana-cruda", m)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>'
            f'<path d="M{f(x0)},{f(base)} L{f(x1)},{f(base)} L{f(x1 - 0.12 * m)},{f(base - h)} L{f(x0 + 0.1 * m)},{f(base - h)} Z" fill="url(#t-tejido)"/>')


def paraguas_clavado(x, base, m, sw, alto=1.55):
    """Paraguas negro clavado en el suelo para dar sombra a la vendedora."""
    ap = base - alto * m
    puntas = [(x - 0.5 * m + 1.0 * m * i / 6, ap + 0.32 * m + (0 if i in (0, 6) else 0.02 * m)) for i in range(7)]
    d = f'M{f(puntas[0][0])},{f(puntas[0][1])} Q{f(x - 0.45 * m)},{f(ap + 0.03 * m)} {f(x)},{f(ap)} Q{f(x + 0.45 * m)},{f(ap + 0.03 * m)} {f(puntas[-1][0])},{f(puntas[-1][1])}'
    for (xa, ya), (xb, yb) in zip(reversed(puntas), list(reversed(puntas))[1:]):
        d += f' Q{f((xa + xb) / 2)},{f(ya - 0.07 * m)} {f(xb)},{f(yb)}'
    varillas = ' '.join(f'M{f(x)},{f(ap)} L{f(px)},{f(py)}' for px, py in puntas[1:-1])
    return (f'<path d="M{f(x + 0.03 * m)},{f(base)} L{f(x)},{f(ap)}" stroke="#000" stroke-width="{f(sw * 0.8)}"/>'
            f'<path d="{d} Z" fill="#000"/><path d="{varillas}" stroke="#fff" stroke-width="{f(sw * 0.35)}"/>'
            f'<path d="M{f(x)},{f(ap)} L{f(x)},{f(ap - 0.08 * m)}" stroke="#000" stroke-width="{f(sw * 0.9)}"/>')


def toldo(x0, base, m, sw, rnd, ancho_m=3.4, mercancia='papas'):
    """Puesto con toldo de lona sobre palos y mesa rústica; la vendedora detrás."""
    W = ancho_m * m
    x1 = x0 + W
    out = [sombra_suelo(x0 - 0.2 * m, x1 + 0.6 * m, base, m)]
    y_frente, y_fondo = base - 2.05 * m, base - 2.45 * m
    # palos de atrás y vientos
    for px in (x0 + 0.2 * m, x1 - 0.1 * m):
        out.append(f'<path d="M{f(px)},{f(base - 0.1 * m)} L{f(px)},{f(y_fondo)}" stroke="#000" stroke-width="{f(sw * 1.1)}"/>')
    out.append(f'<path d="M{f(x0 + 0.1 * m)},{f(y_frente)} L{f(x0 - 0.55 * m)},{f(base)} M{f(x1 - 0.1 * m)},{f(y_frente)} L{f(x1 + 0.55 * m)},{f(base)}" stroke="#000" stroke-width="{f(sw * 0.45)}"/>')
    for px in (x0 - 0.55 * m, x1 + 0.55 * m):
        out.append(f'<path d="M{f(px)},{f(base)} L{f(px + 0.03 * m)},{f(base - 0.15 * m)}" stroke="#000" stroke-width="{f(sw * 1.2)}"/>')
    # la vendedora queda detrás de la mesa
    out.append(persona(x0 + W * 0.58, base, m, sw, 'mujer', espejo=True, sombrero='paja' if mercancia == 'papas' else 'negro'))
    # mesa: tablero, patas y travesaño
    ym = base - 0.8 * m
    for px in (x0 + 0.4 * m, x1 - 0.48 * m):
        out.append(f'<rect x="{f(px)}" y="{f(ym)}" width="{f(0.07 * m)}" height="{f(0.8 * m)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
    out.append(f'<path d="M{f(x0 + 0.47 * m)},{f(base - 0.25 * m)} L{f(x1 - 0.48 * m)},{f(base - 0.25 * m)}" stroke="#000" stroke-width="{f(sw * 0.8)}"/>')
    out.append(f'<rect x="{f(x0 + 0.3 * m)}" y="{f(ym)}" width="{f(W - 0.6 * m)}" height="{f(0.08 * m)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw * 0.7)}"/>'
               f'<rect x="{f(x0 + 0.3 * m)}" y="{f(ym)}" width="{f(W - 0.6 * m)}" height="{f(0.08 * m)}" fill="url(#t-madera)"/>')
    if mercancia == 'papas':
        out.append(monton(x0 + 0.75 * m, ym, m, sw, rnd, 3) + monton(x0 + 1.35 * m, ym, m, sw, rnd, 3, clase='cebolla')
                   + monton(x0 + 2.0 * m, ym, m, sw, rnd, 2, r=0.09, clase='col') + monton(x0 + 2.75 * m, ym, m, sw, rnd, 3))
        out.append(costal(x1 - 0.55 * m, base, 0.55 * m, 0.55 * m, m, sw, rnd, abierto=True))
        out.append(canasto(x0 - 0.15 * m, base, 0.5 * m, 0.32 * m, m, sw, rnd, 'mazorcas'))
    else:
        out.append(olla(x0 + 0.45 * m, ym, 0.42 * m, 0.32 * m, m, sw, rnd) + olla(x0 + 0.95 * m, ym, 0.32 * m, 0.42 * m, m, sw, rnd, 'mucura')
                   + olla(x0 + 1.35 * m, ym, 0.5 * m, 0.28 * m, m, sw, rnd) + olla(x0 + 1.95 * m, ym, 0.36 * m, 0.48 * m, m, sw, rnd, 'mucura')
                   + olla(x0 + 2.4 * m, ym, 0.45 * m, 0.3 * m, m, sw, rnd))
        out.append(olla(x0 - 0.2 * m, base, 0.5 * m, 0.4 * m, m, sw, rnd) + olla(x1 - 0.7 * m, base, 0.38 * m, 0.55 * m, m, sw, rnd, 'mucura')
                   + olla(x1 - 0.3 * m, base, 0.42 * m, 0.3 * m, m, sw, rnd))
    # lona: envés en sombra (se ve desde abajo), costuras y faldón al sol con remiendo
    lona = f'M{f(x0)},{f(y_frente)} Q{f((x0 + x1) / 2)},{f(y_frente + 0.07 * m)} {f(x1)},{f(y_frente)} L{f(x1 - 0.05 * m)},{f(y_fondo)} L{f(x0 + 0.08 * m)},{f(y_fondo)} Z'
    lona_ = lav('blanco-tela', m)
    out.append(f'<path d="{lona}" fill="{lona_}" stroke="#000" stroke-width="{f(sw * 0.7)}"/><path d="{lona}" fill="url(#t-fina)"/>')
    costuras = ' '.join(f'M{f(x0 + W * u)},{f(y_frente + 0.05 * m)} L{f(x0 + W * u + 0.02 * m)},{f(y_fondo)}' for u in (0.33, 0.66))
    out.append(f'<path d="{costuras}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
    falda = f'M{f(x0 - 0.05 * m)},{f(y_frente)} Q{f((x0 + x1) / 2)},{f(y_frente + 0.07 * m)} {f(x1 + 0.05 * m)},{f(y_frente)}'
    x, borde = x1 + 0.05 * m, ''
    while x > x0 - 0.05 * m:
        xn = max(x0 - 0.05 * m, x - rnd.uniform(0.3, 0.5) * m)
        borde += f' Q{f((x + xn) / 2)},{f(y_frente + 0.32 * m)} {f(xn)},{f(y_frente + 0.2 * m + rnd.uniform(-0.02, 0.03) * m)}'
        x = xn
    falda += f' L{f(x1 + 0.05 * m)},{f(y_frente + 0.2 * m)}{borde} Z'
    out.append(f'<path d="{falda}" fill="{lona_}" stroke="#000" stroke-width="{f(sw * 0.8)}" stroke-linejoin="round"/>')
    rx = x0 + W * rnd.uniform(0.15, 0.6)
    out.append(f'<rect x="{f(rx)}" y="{f(y_frente + 0.05 * m)}" width="{f(0.35 * m)}" height="{f(0.14 * m)}" fill="{lav("lana-cruda", m)}" stroke="#000" stroke-width="{f(sw * 0.4)}" stroke-dasharray="{f(sw)} {f(sw)}"/>')
    # palos de adelante (amarrados a la lona)
    for px in (x0 + 0.1 * m, x1 - 0.1 * m):
        out.append(f'<rect x="{f(px - 0.035 * m)}" y="{f(y_frente - 0.05 * m)}" width="{f(0.07 * m)}" height="{f(base - y_frente + 0.05 * m)}" fill="{lav("madera", m, 0.55)}" stroke="#000" stroke-width="{f(sw * 0.7)}"/>'
                   f'<path d="M{f(px - 0.06 * m)},{f(y_frente + 0.04 * m)} L{f(px + 0.06 * m)},{f(y_frente + 0.1 * m)} M{f(px - 0.06 * m)},{f(y_frente + 0.1 * m)} L{f(px + 0.06 * m)},{f(y_frente + 0.04 * m)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
    return ''.join(out)


def tendido(x0, base, m, sw, rnd, ancho_m=2.5, clase='papa', comprador=False):
    """Venta en el suelo: manta con montoncitos y la vendedora sentada bajo su paraguas."""
    W = ancho_m * m
    out = [sombra_suelo(x0, x0 + W + 0.4 * m, base, m), paraguas_clavado(x0 + 0.45 * m, base, m, sw)]
    out.append(persona(x0 + 0.42 * m, base, m, sw, 'sentada', sombrero='negro', falda='pano-oscuro'))
    out.append(manta_suelo(x0 + 0.85 * m, x0 + W, base, m, sw))
    n = int((W - 1.0 * m) / (0.42 * m))
    for i in range(n):
        out.append(monton(x0 + 1.1 * m + i * 0.42 * m, base - 0.05 * m, m, sw, rnd, rnd.choice((2, 3)), clase=clase if i % 3 else 'papa'))
    out.append(canasto(x0 - 0.05 * m, base, 0.42 * m, 0.3 * m, m, sw, rnd, 'cebollas' if clase == 'papa' else 'papas'))
    if comprador:
        out.append(persona(x0 + W - 0.1 * m, base, m, sw, 'mujer', espejo=True, sombrero='paja', lleva='canasto', falda='lana-parda'))
    return ''.join(out)


def pila(cx, base, m, sw, rnd):
    """Pila de piedra en el centro de la plaza: pilón ochavado, columna, taza y chorros [P]."""
    out = ['<g data-p="pila de piedra en la plaza: confirmar con fotos del norte de Boyacá años 40">',
           sombra_suelo(cx - 1.7 * m, cx + 2.0 * m, base, m)]
    h, y_borde = 0.75 * m, base - 0.75 * m
    y_atras = y_borde - 0.25 * m
    # agua y borde de atrás del pilón (se ve un poco desde la altura de los ojos)
    agua = [(cx - 1.5 * m, y_borde), (cx - 0.75 * m, y_atras), (cx + 0.75 * m, y_atras), (cx + 1.5 * m, y_borde)]
    # el agua no es azul: el azul es del partido (paleta.md §3)
    out.append(f'<polygon points="{pts(agua)}" fill="{lav("agua", m)}" stroke="#000" stroke-width="{f(sw * 0.7)}"/><polygon points="{pts(agua)}" fill="url(#t-horiz)"/>')
    piedra = lav('piedra', m)
    # columna, taza y remate
    out.append(f'<rect x="{f(cx - 0.17 * m)}" y="{f(base - 1.75 * m)}" width="{f(0.34 * m)}" height="{f(1.0 * m)}" fill="{piedra}" stroke="#000" stroke-width="{f(sw * 0.8)}"/>'
               f'<rect x="{f(cx + 0.05 * m)}" y="{f(base - 1.75 * m)}" width="{f(0.12 * m)}" height="{f(1.0 * m)}" fill="url(#t-fina)"/>'
               f'<rect x="{f(cx - 0.24 * m)}" y="{f(base - 1.0 * m)}" width="{f(0.48 * m)}" height="{f(0.12 * m)}" fill="{piedra}" stroke="#000" stroke-width="{f(sw * 0.7)}"/>')
    taza = f'M{f(cx - 0.6 * m)},{f(base - 1.95 * m)} L{f(cx + 0.6 * m)},{f(base - 1.95 * m)} Q{f(cx + 0.5 * m)},{f(base - 1.72 * m)} {f(cx)},{f(base - 1.7 * m)} Q{f(cx - 0.5 * m)},{f(base - 1.72 * m)} {f(cx - 0.6 * m)},{f(base - 1.95 * m)} Z'
    out.append(f'<path d="{taza}" fill="{piedra}" stroke="#000" stroke-width="{f(sw * 0.8)}"/>'
               f'<path d="M{f(cx)},{f(base - 1.7 * m)} Q{f(cx + 0.5 * m)},{f(base - 1.72 * m)} {f(cx + 0.6 * m)},{f(base - 1.95 * m)} L{f(cx + 0.3 * m)},{f(base - 1.9 * m)} Z" fill="url(#t-fina)"/>')
    out.append(f'<rect x="{f(cx - 0.1 * m)}" y="{f(base - 2.2 * m)}" width="{f(0.2 * m)}" height="{f(0.25 * m)}" fill="{piedra}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>'
               f'<ellipse cx="{f(cx)}" cy="{f(base - 2.3 * m)}" rx="{f(0.13 * m)}" ry="{f(0.11 * m)}" fill="{piedra}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>'
               f'<path d="M{f(cx + 0.02 * m)},{f(base - 2.26 * m)} Q{f(cx + 0.1 * m)},{f(base - 2.3 * m)} {f(cx + 0.06 * m)},{f(base - 2.38 * m)} Z" fill="url(#t-fina)"/>'
               f'<path d="M{f(cx)},{f(base - 2.41 * m)} L{f(cx)},{f(base - 2.5 * m)}" stroke="#000" stroke-width="{f(sw * 0.9)}"/>')
    # chorros que caen de la taza al pilón
    chorros = []
    for sx in (-1, 1):
        for d_ in (0.0, 0.05):
            chorros.append(f'M{f(cx + sx * (0.58 - d_) * m)},{f(base - 1.93 * m)} Q{f(cx + sx * (0.82 - d_) * m)},{f(base - 1.7 * m)} {f(cx + sx * (0.86 - d_) * m)},{f(y_borde - 0.08 * m)}')
    out.append(f'<path d="{" ".join(chorros)}" stroke="#000" stroke-width="{f(sw * 0.45)}" fill="none"/>')
    # pilón ochavado de sillares: cara de frente al sol, caras de los lados más oscuras
    caras = [((cx - 1.5 * m, cx - 0.75 * m), 't-puntos-ralos'), ((cx - 0.75 * m, cx + 0.75 * m), None),
             ((cx + 0.75 * m, cx + 1.5 * m), 't-fina')]
    for (xa, xb), tr in caras:
        out.append(f'<rect x="{f(xa)}" y="{f(y_borde)}" width="{f(xb - xa)}" height="{f(h)}" fill="{piedra}" stroke="#000" stroke-width="{f(sw * 0.8)}"/>')
        if tr:
            out.append(f'<rect x="{f(xa)}" y="{f(y_borde)}" width="{f(xb - xa)}" height="{f(h)}" fill="url(#{tr})"/>')
        juntas = [f'M{f(xa)},{f(y_borde + h * 0.5)} L{f(xb)},{f(y_borde + h * 0.5)}']
        for fila, (ya, yb) in enumerate(((y_borde, y_borde + h * 0.5), (y_borde + h * 0.5, base))):
            jx = xa + (0.25 if fila else 0.5) * m
            while jx < xb - 0.1 * m:
                juntas.append(f'M{f(jx)},{f(ya)} L{f(jx)},{f(yb)}')
                jx += 0.6 * m
        out.append(f'<path d="{" ".join(juntas)}" stroke="#000" stroke-width="{f(sw * 0.4)}"/>')
    out.append(f'<rect x="{f(cx - 1.55 * m)}" y="{f(y_borde - 0.06 * m)}" width="{f(3.1 * m)}" height="{f(0.1 * m)}" fill="{lav("piedra", m, 0.75)}" stroke="#000" stroke-width="{f(sw * 0.8)}"/>')
    # musgo y humedad al pie
    out.append(f'<rect x="{f(cx - 1.5 * m)}" y="{f(base - 0.12 * m)}" width="{f(3.0 * m)}" height="{f(0.12 * m)}" fill="url(#t-puntos)"/>')
    # mujer que viene por agua con su múcura
    out.append(olla(cx + 1.25 * m, y_borde - 0.06 * m, 0.3 * m, 0.42 * m, m, sw, rnd, 'mucura'))
    out.append(persona(cx + 1.95 * m, base, m, sw, 'mujer', espejo=True, sombrero='negro', falda='lana-parda'))
    out.append(persona(cx - 1.75 * m, base, m, sw, 'hombre', k=0.62, ruana='gris', sombrero='paja'))
    out.append('</g>')
    return ''.join(out)


def modulo_medio(nombre, W, H, titulo, dibujo, notas=''):
    """Un módulo del plano medio: base del viewBox = suelo de la capa (y=724)."""
    archivo(nombre, W, H, 'medio', titulo, dibujo, notas=notas)


def mercado():
    m, sw = ppm('medio'), TRAZO['medio']
    rnd = random.Random(1946)
    modulo_medio('toldo-papas', 420, 236, 'puesto de papas, cebollas y coles con toldo',
                 toldo(60, 236, m, sw, rnd, mercancia='papas'))
    modulo_medio('toldo-loza', 420, 236, 'puesto de loza de barro con toldo',
                 toldo(60, 236, m, sw, rnd, mercancia='loza'), notas='Loza genérica [P: tipos de loza del mercado de 1946].')
    modulo_medio('tendido-papas', 270, 160, 'venta en el suelo: papas y cebollas',
                 tendido(30, 160, m, sw, rnd, 2.6, 'papa'))
    modulo_medio('tendido-cubios', 330, 210, 'venta en el suelo: cubios y papas, con compradora',
                 tendido(30, 210, m, sw, rnd, 2.7, 'cubio', comprador=True))
    modulo_medio('mula-carga', 340, 182, 'mula cargada y su arriero',
                 sombra_suelo(10, 330, 182, m) + mula(90, 182, m, sw) + persona(290, 182, m, sw, 'hombre', espejo=True, ruana='negra', sombrero='paja', lleva='vara')
                 + f'<path d="M{f(90 + 1.28 * m)},{f(182 - 1.18 * m)} Q{f(240)},{f(182 - 0.7 * m)} {f(290 - 0.33 * m)},{f(182 - 1.0 * m)}" stroke="#000" stroke-width="{f(sw * 0.5)}" fill="none"/>')
    modulo_medio('mula-atada', 250, 182, 'mula atada a una estaca',
                 sombra_suelo(10, 240, 182, m) + f'<path d="M{f(40)},{f(182)} L{f(42)},{f(182 - 0.55 * m)}" stroke="#000" stroke-width="{f(sw * 1.6)}"/>'
                 + mula(150, 182, m, sw, espejo=True, oscura=False)
                 + f'<path d="M{f(150 - 1.28 * m)},{f(182 - 1.18 * m)} Q{f(60)},{f(182 - 0.4 * m)} {f(42)},{f(182 - 0.5 * m)}" stroke="#000" stroke-width="{f(sw * 0.5)}" fill="none"/>')
    modulo_medio('gente-corrillo', 230, 175, 'corrillo de hombres con ruana',
                 sombra_suelo(5, 225, 175, m)
                 + persona(45, 175, m, sw, 'hombre', ruana='oscura', sombrero='negro', lleva='vara')
                 + persona(118, 175, m, sw, 'hombre', espejo=True, ruana='clara', sombrero='paja', panuelo=ROJO)
                 + persona(185, 175, m, sw, 'hombre', espejo=True, ruana='gris', sombrero='negro'),
                 notas='Un pañuelo rojo: el color cuenta la división también en la plaza [P: uso en 1946].')
    modulo_medio('gente-mujeres', 230, 210, 'mujeres con pañolón, paraguas negro y un niño',
                 sombra_suelo(5, 225, 210, m)
                 + persona(55, 210, m, sw, 'mujer', sombrero='negro', lleva='paraguas', falda='pano-oscuro')
                 + persona(120, 210, m, sw, 'hombre', k=0.62, ruana='clara', sombrero='paja')
                 + persona(175, 210, m, sw, 'mujer', espejo=True, sombrero='paja', lleva='canasto'))
    modulo_medio('gente-pareja', 150, 175, 'pareja que cruza la plaza',
                 sombra_suelo(5, 145, 175, m)
                 + persona(45, 175, m, sw, 'hombre', ruana='gris', sombrero='negro', panuelo=AZUL)
                 + persona(105, 175, m, sw, 'mujer', sombrero='negro', falda='negro-anil', lleva='canasto'),
                 notas='Un pañuelo azul [P: uso en 1946].')
    modulo_medio('pila', 380, 220, 'pila de piedra con mujer y niño', pila(170, 220, m, sw, rnd))


# ============================= capa frente (1,3 · 260 px/m) =============================
# Repoussoir: siluetas negras con pocas líneas blancas, cortadas por el borde del cuadro.
# Escaso: enmarca sin tapar el camino del personaje (su suelo está en y=900).

def frente_canastos():
    m, sw = ppm('frente'), TRAZO['frente']
    rnd = random.Random(5)
    W, H = 560, 250  # se coloca con la base por debajo del cuadro (y≈1160): solo asoma la boca
    out = []
    for x0, w, h, carga in ((20, 0.8, 0.62, 'papas'), (250, 0.95, 0.72, 'mazorcas')):
        x1, y0 = x0 + w * m, H - h * m
        if carga == 'papas':
            for i in range(9):
                px = x0 + w * m * (0.1 + i * 0.1) + rnd.uniform(-4, 4)
                py = y0 - rnd.uniform(0.0, 0.07) * m
                out.append(f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="{f(0.06 * m)}" ry="{f(0.05 * m)}" fill="#000" stroke="#fff" stroke-width="{f(sw * 0.35)}"/>')
        else:
            for i in range(6):
                px = x0 + w * m * (0.12 + i * 0.15)
                out.append(f'<ellipse cx="{f(px)}" cy="{f(y0 - 0.06 * m)}" rx="{f(0.055 * m)}" ry="{f(0.14 * m)}" transform="rotate({f(rnd.uniform(-35, 35))} {f(px)} {f(y0)})" fill="#000" stroke="#fff" stroke-width="{f(sw * 0.35)}"/>')
        cuerpo = f'M{f(x0)},{f(y0)} L{f(x1)},{f(y0)} L{f(x1 - 0.08 * m)},{f(H)} L{f(x0 + 0.08 * m)},{f(H)} Z'
        out.append(f'<path d="{cuerpo}" fill="#000"/>')
        tejido = []
        for i in range(1, 6):
            yy = y0 + h * m * i / 6
            tejido.append(f'M{f(x0 + 0.015 * m * i)},{f(yy)} L{f(x1 - 0.015 * m * i)},{f(yy)}')
        out.append(f'<path d="{" ".join(tejido)}" stroke="#fff" stroke-width="{f(sw * 0.3)}"/>')
        out.append(f'<rect x="{f(x0 - 0.03 * m)}" y="{f(y0 - 0.03 * m)}" width="{f(w * m + 0.06 * m)}" height="{f(0.06 * m)}" rx="{f(0.02 * m)}" fill="#000" stroke="#fff" stroke-width="{f(sw * 0.4)}"/>')
    archivo('frente-canastos', W, H, 'frente', 'canastos en primer plano (silueta)', '\n'.join(out),
            notas='Base por debajo del cuadro: se coloca con y > 1080 para que asome solo la parte de arriba.')


def frente_costal():
    m, sw = ppm('frente'), TRAZO['frente']
    W, H = 330, 300
    d = (f'M{f(20)},{f(H)} Q{f(5)},{f(H - 0.6 * m)} {f(40)},{f(H - 0.95 * m)} Q{f(130)},{f(H - 1.12 * m)} {f(150)},{f(H - 1.0 * m)} '
         f'L{f(165)},{f(H - 1.12 * m)} L{f(185)},{f(H - 0.98 * m)} Q{f(280)},{f(H - 0.98 * m)} {f(300)},{f(H - 0.6 * m)} Q{f(315)},{f(H - 0.3 * m)} {f(305)},{f(H)} Z')
    out = [f'<path d="{d}" fill="#000"/>',
           f'<path d="M{f(60)},{f(H - 0.75 * m)} Q{f(160)},{f(H - 0.85 * m)} {f(270)},{f(H - 0.7 * m)} M{f(150)},{f(H - 0.98 * m)} Q{f(140)},{f(H - 0.5 * m)} {f(150)},{f(H)}" stroke="#fff" stroke-width="{f(sw * 0.35)}" fill="none"/>',
           f'<path d="M{f(40)},{f(H - 0.9 * m)} Q{f(160)},{f(H - 1.05 * m)} {f(295)},{f(H - 0.62 * m)}" stroke="#fff" stroke-width="{f(sw * 0.3)}" fill="none" stroke-dasharray="{f(sw)} {f(sw * 1.4)}"/>',
           f'<path d="M{f(150)},{f(H - 1.0 * m)} L{f(165)},{f(H - 1.12 * m)} L{f(185)},{f(H - 0.98 * m)}" stroke="#fff" stroke-width="{f(sw * 0.45)}" fill="none"/>']
    archivo('frente-costal', W, H, 'frente', 'costal en primer plano (silueta)', '\n'.join(out),
            notas='Base por debajo del cuadro (y > 1080).')


def frente_toldo():
    m, sw = ppm('frente'), TRAZO['frente']
    rnd = random.Random(9)
    W, H = 1100, 200
    borde, x = '', W
    while x > 0:
        xn = max(0, x - rnd.uniform(0.35, 0.55) * m)
        borde += f' Q{f((x + xn) / 2)},{f(0.5 * m + rnd.uniform(-0.03, 0.04) * m)} {f(xn)},{f(0.36 * m + rnd.uniform(-0.02, 0.02) * m)}'
        x = xn
    d = f'M0,0 L{W},0 L{W},{f(0.36 * m)}{borde} Z'
    out = [f'<path d="{d}" fill="#000"/>',
           f'<path d="M0,{f(0.12 * m)} Q{f(W / 2)},{f(0.16 * m)} {W},{f(0.12 * m)}" stroke="#fff" stroke-width="{f(sw * 0.35)}" fill="none"/>',
           f'<path d="M{f(W * 0.3)},0 L{f(W * 0.31)},{f(0.36 * m)} M{f(W * 0.66)},0 L{f(W * 0.65)},{f(0.36 * m)}" stroke="#fff" stroke-width="{f(sw * 0.3)}"/>']
    # ristra de cebollas colgada del borde
    rx, ry = W * 0.78, 0.4 * m
    out.append(f'<path d="M{f(rx)},{f(0.3 * m)} L{f(rx + 3)},{f(ry + 0.22 * m)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
    r = 0.04 * m
    for i in range(5):
        cy = ry + i * 0.07 * m
        for sx in ((-1, 1) if i < 4 else (0,)):
            cx = rx + 2 + sx * 0.042 * m
            gota = (f'M{f(cx)},{f(cy - r * 1.9)} Q{f(cx + r * 0.3)},{f(cy - r)} {f(cx + r)},{f(cy - r * 0.1)} '
                    f'Q{f(cx + r)},{f(cy + r)} {f(cx)},{f(cy + r)} Q{f(cx - r)},{f(cy + r)} {f(cx - r)},{f(cy - r * 0.1)} '
                    f'Q{f(cx - r * 0.3)},{f(cy - r)} {f(cx)},{f(cy - r * 1.9)} Z')
            out.append(f'<path d="{gota}" fill="#000" stroke="#fff" stroke-width="{f(sw * 0.25)}"/>'
                       f'<path d="M{f(cx - r * 0.5)},{f(cy - r * 0.3)} Q{f(cx - r * 0.55)},{f(cy + r * 0.4)} {f(cx - r * 0.1)},{f(cy + r * 0.7)}" stroke="#fff" stroke-width="{f(sw * 0.3)}" fill="none"/>')
    archivo('frente-toldo', W, H, 'frente', 'borde de un toldo arriba, con una ristra de cebollas', '\n'.join(out),
            notas='Se coloca arriba (y=0).')


tienda_roja()
casa_porton()
empedrado()
objetos_juego()
cordillera()
iglesia()
mercado()
frente_canastos()
frente_costal()
frente_toldo()
suelo_plaza('suelo-medio', 'medio', 200, 34)
lejos_oeste()
lejos_este()
suelo_plaza('suelo-lejos', 'lejos', 110, 21)
nube('nube-a', 620, 170, 3)
nube('nube-b', 420, 120, 5)
nube('nube-c', 260, 82, 8)
