"""Generador de los fondos de la plaza de Puente Alto (game/art/src/fondos/puente-alto/*.svg).

Mañana de mercado, mayo–junio de 1946 (doc 02 §5, prólogo). Puente Alto es ficticio (doc 01):
se compone a partir de tipologías del norte de Boyacá, sin copiar un pueblo real.
Escala y capas: planeacion/arte/tomo1/escenarios/contrato_escala.md (200 px/m en el plano de
juego; cada capa a 200 × paralaje). Fuentes y [V]/[P]: planeacion/arte/tomo1/escenarios/puente-alto.md.

  python3 art/gen/puente_alto.py        (desde game/; sin dependencias)

Edita este script, no los SVG generados.
"""
import math
import os
import random
import sys

OUTDIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'fondos', 'puente-alto')

ROJO = '#c1121f'  # rojo liberal PROVISIONAL [P] (hoja de estilo, doc 03 §6.1)
AZUL = '#1f3d8a'  # azul conservador PROVISIONAL [P]
NEGRO, BLANCO = '#000', '#fff'

PARALAJE = {'cielo': 0, 'lejos': 0.15, 'medio': 0.45, 'juego': 1.0, 'frente': 1.3}
# Trazo base por capa: grueso cerca, fino lejos (doc 03 §1).
TRAZO = {'cielo': 1.0, 'lejos': 1.1, 'medio': 1.7, 'juego': 2.6, 'frente': 3.6}


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
    <pattern id="t-madera-v" width="{f(6*s)}" height="{f(40*s)}" patternUnits="userSpaceOnUse"><path d="M{f(3*s)},0 C{f(2*s)},{f(10*s)} {f(4*s)},{f(20*s)} {f(3*s)},{f(40*s)}" stroke="#000" stroke-width="{f(0.6*s)}" fill="none"/></pattern>
  </defs>'''


def archivo(nombre, w, h, capa, titulo, cuerpo, notas='', esc_trama=1.0):
    contenido = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{f(w)}" height="{f(h)}" viewBox="0 0 {f(w)} {f(h)}">
  <!--
    Puente Alto · {titulo}
    Capa: {capa} (paralaje {PARALAJE[capa]}, {f(ppm(capa))} px/m). La base del viewBox es el suelo de la capa
    salvo que el módulo se coloque por arriba (cielo, mosaicos de suelo).
    {notas}
    Colores: tinta (#000) y papel (#fff) placeholders; acentos rojo/azul provisionales [P].
    GENERADO por game/art/gen/puente_alto.py: edita el script, no este archivo.
  -->{tramas(esc_trama)}
{cuerpo}
</svg>
'''
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
    out = [f'<rect x="{f(x0)}" y="{f(y_arriba)}" width="{f(x1-x0)}" height="{f(alto)}" fill="#fff"/>']
    # valor del tejado: la teja de barro es más oscura que la cal (trama, nunca degradado)
    out.append(f'<rect x="{f(x0)}" y="{f(y_arriba)}" width="{f(x1-x0)}" height="{f(alto)}" fill="url(#t-fina)"/>')
    if oscuro:
        out.append(f'<rect x="{f(x0)}" y="{f(y_arriba)}" width="{f(x1-x0)}" height="{f(alto*0.45)}" fill="url(#t-media)"/>')
    # cobijas: lomos convexos con su sombra a la derecha; canales: surcos entre ellas
    x = x0
    while x < x1:
        dx = rnd.uniform(-0.03, 0.03) * m
        xc = x + paso * 0.5
        lomo = (f'M{f(xc-paso*0.3+dx)},{f(y_arriba)} L{f(xc-paso*0.3)},{f(y_borde-0.08*m)} '
                f'Q{f(xc)},{f(y_borde-0.16*m)} {f(xc+paso*0.3)},{f(y_borde-0.08*m)} L{f(xc+paso*0.3+dx)},{f(y_arriba)} Z')
        out.append(f'<path d="{lomo}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.45)}"/>')
        out.append(f'<path d="M{f(xc+paso*0.08+dx)},{f(y_arriba)} L{f(xc+paso*0.08)},{f(y_borde-0.12*m)} L{f(xc+paso*0.3)},{f(y_borde-0.08*m)} L{f(xc+paso*0.3+dx)},{f(y_arriba)} Z" fill="url(#t-media)"/>')
        # juntas entre piezas de teja a lo largo del lomo
        for k in range(1, 6):
            yy = y_arriba + alto * k / 6 + rnd.uniform(-0.03, 0.03) * m
            if yy < y_borde - 0.2 * m:
                out.append(f'<path d="M{f(xc-paso*0.3)},{f(yy)} Q{f(xc)},{f(yy-0.05*m)} {f(xc+paso*0.3)},{f(yy)}" stroke="#000" stroke-width="{f(sw*0.35)}" fill="none"/>')
        x += paso
    # velo de trama sobre todo el tejado: más oscuro que la cal de los muros
    out.append(f'<rect x="{f(x0)}" y="{f(y_arriba)}" width="{f(x1-x0)}" height="{f(alto-0.08*m)}" fill="url(#t-fina)"/>')
    # bocas de las cobijas en el borde: medias lunas oscuras
    x = x0
    bocas = []
    while x < x1:
        xc = x + paso * 0.5
        r = paso * 0.3
        bocas.append(f'M{f(xc-r)},{f(y_borde-0.08*m)} Q{f(xc)},{f(y_borde-0.08*m-r*1.1)} {f(xc+r)},{f(y_borde-0.08*m)} Q{f(xc)},{f(y_borde-0.08*m-r*0.35)} {f(xc-r)},{f(y_borde-0.08*m)} Z')
        x += paso
    out.append(f'<path d="{" ".join(bocas)}" fill="#000"/>')
    out.append(f'<rect x="{f(x0)}" y="{f(y_borde-0.08*m)}" width="{f(x1-x0)}" height="{f(0.08*m)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.7)}"/>')
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
        canes.append(f'<path d="{cab}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
        canes.append(f'<path d="M{f(x+w*0.62)},{f(y0)} L{f(x+w)},{f(y0)} L{f(x+w)},{f(y0+0.16*m)} Q{f(x+w)},{f(y0+0.26*m)} {f(x+w*0.62)},{f(y0+0.255*m)} Z" fill="url(#t-media)"/>')
        x += paso
    out.extend(canes)
    # viga
    out.append(f'<rect x="{f(x0)}" y="{f(y_viga-0.12*m)}" width="{f(x1-x0)}" height="{f(0.14*m)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.8)}"/>')
    out.append(f'<rect x="{f(x0)}" y="{f(y_viga-0.12*m)}" width="{f(x1-x0)}" height="{f(0.14*m)}" fill="url(#t-madera)"/>')
    return ''.join(out)


def pilar(x, y_piso, y_viga, m, sw, color=None):
    """Pie derecho de madera sobre basa de piedra, con zapata bajo la viga."""
    w = 0.2 * m
    basa_h, basa_w = 0.3 * m, 0.34 * m
    zap_w, zap_h = 0.7 * m, 0.15 * m
    relleno = color or '#fff'
    alto_fuste = y_piso - basa_h - y_viga
    out = [
        # fuste de madera: veta, cara en sombra y una grieta
        f'<rect x="{f(x-w/2)}" y="{f(y_viga+0.02*m)}" width="{f(w)}" height="{f(alto_fuste)}" fill="{relleno}" stroke="#000" stroke-width="{f(sw*0.9)}"/>',
        f'<rect x="{f(x-w/2)}" y="{f(y_viga+0.02*m)}" width="{f(w)}" height="{f(alto_fuste)}" fill="url(#t-madera-v)"/>',
        f'<rect x="{f(x+w*0.12)}" y="{f(y_viga+0.02*m)}" width="{f(w*0.38)}" height="{f(alto_fuste)}" fill="url(#t-cruz)"/>',
        f'<path d="M{f(x-w*0.22)},{f(y_viga+0.35*m)} L{f(x-w*0.18)},{f(y_viga+0.8*m)} L{f(x-w*0.24)},{f(y_viga+1.1*m)}" stroke="#000" stroke-width="{f(sw*0.45)}" fill="none"/>',
        # zapata
        f'<path d="M{f(x-zap_w/2)},{f(y_viga+0.02*m)} L{f(x+zap_w/2)},{f(y_viga+0.02*m)} L{f(x+zap_w/2)},{f(y_viga+0.06*m)} Q{f(x+zap_w/2-0.08*m)},{f(y_viga+zap_h)} {f(x+w/2)},{f(y_viga+zap_h)} L{f(x-w/2)},{f(y_viga+zap_h)} Q{f(x-zap_w/2+0.08*m)},{f(y_viga+zap_h)} {f(x-zap_w/2)},{f(y_viga+0.06*m)} Z" fill="#fff" stroke="#000" stroke-width="{f(sw*0.7)}"/>',
        f'<path d="M{f(x-zap_w/2)},{f(y_viga+0.02*m)} L{f(x+zap_w/2)},{f(y_viga+0.02*m)} L{f(x+zap_w/2)},{f(y_viga+0.06*m)} Q{f(x+zap_w/2-0.08*m)},{f(y_viga+zap_h)} {f(x+w/2)},{f(y_viga+zap_h)} L{f(x-w/2)},{f(y_viga+zap_h)} Q{f(x-zap_w/2+0.08*m)},{f(y_viga+zap_h)} {f(x-zap_w/2)},{f(y_viga+0.06*m)} Z" fill="url(#t-madera)"/>',
        # basa de piedra
        f'<path d="M{f(x-basa_w/2)},{f(y_piso)} L{f(x-basa_w/2+0.03*m)},{f(y_piso-basa_h)} L{f(x+basa_w/2-0.03*m)},{f(y_piso-basa_h)} L{f(x+basa_w/2)},{f(y_piso)} Z" fill="#fff" stroke="#000" stroke-width="{f(sw*0.8)}"/>',
        f'<path d="M{f(x)},{f(y_piso-basa_h)} L{f(x+basa_w/2)},{f(y_piso)} L{f(x+basa_w/2-0.08*m)},{f(y_piso)} Z" fill="url(#t-media)"/>',
    ]
    return ''.join(out)


def muro_cal(x0, x1, y_arriba, y_abajo, m, sw, rnd, grietas=4, desconchados=3):
    """Tapia encalada: blanco con grietas finas y desconchados donde asoma la tierra (doc 03 §3.1 [V])."""
    out = [f'<rect x="{f(x0)}" y="{f(y_arriba)}" width="{f(x1-x0)}" height="{f(y_abajo-y_arriba)}" fill="#fff" stroke="#000" stroke-width="{f(sw)}"/>']
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
        out.append(f'<polygon points="{pts(pts_)}" fill="url(#t-media)" stroke="#000" stroke-width="{f(sw*0.3)}"/>')
    return ''.join(out)


def zocalo(x0, x1, y_abajo, alto, m, sw, rnd, color=None):
    """Zócalo de la fachada: franja baja pintada, gastada (color de tienda partidista o trama)."""
    y = y_abajo - alto
    out = [f'<rect x="{f(x0)}" y="{f(y)}" width="{f(x1-x0)}" height="{f(alto)}" fill="{color or "#fff"}" stroke="#000" stroke-width="{f(sw*0.8)}"/>']
    if not color:
        out.append(f'<rect x="{f(x0)}" y="{f(y)}" width="{f(x1-x0)}" height="{f(alto)}" fill="url(#t-media)"/>')
    else:
        # pintura gastada: sombreado ralo de tinta sobre el color
        out.append(f'<rect x="{f(x0)}" y="{f(y)}" width="{f(x1-x0)}" height="{f(alto)}" fill="url(#t-fina)" opacity="0.35"/>')
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
        out.append(f'<polygon points="{pts(p)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.25)}"/>')
    # barro salpicado al pie
    out.append(f'<rect x="{f(x0)}" y="{f(y_abajo-0.1*m)}" width="{f(x1-x0)}" height="{f(0.1*m)}" fill="url(#t-puntos)"/>')
    return ''.join(out)


def puerta_tablas(x0, y0, w, h, m, sw, rnd, color=None, hojas=1):
    """Puerta de tablas con clavos (portón de madera: doc 03 §3.1 [P])."""
    out = [f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="{color or "#fff"}" stroke="#000" stroke-width="{f(sw*0.9)}"/>']
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
        out.append(f'<path d="M{f(x-r)},{f(y0+0.06*m)} L{f(x-r)},{f(y0+h*0.3)} Q{f(x-r*2)},{f(y0+h*0.4)} {f(x-r)},{f(y0+h*0.5)} L{f(x-r)},{f(y0+h-0.06*m)} L{f(x+r)},{f(y0+h-0.06*m)} L{f(x+r)},{f(y0+h*0.5)} Q{f(x+r*2)},{f(y0+h*0.4)} {f(x+r)},{f(y0+h*0.3)} L{f(x+r)},{f(y0+0.06*m)} Z" fill="#fff" stroke="#000" stroke-width="{f(sw*0.35)}"/>')
    out.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(0.07*m)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
    out.append(f'<rect x="{f(x0)}" y="{f(y0+h-0.07*m)}" width="{f(w)}" height="{f(0.07*m)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
    out.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="none" stroke="#000" stroke-width="{f(sw)}"/>')
    # postigos abiertos a los lados
    pw = w * 0.42
    for lado, xx in ((-1, x0 - pw), (1, x0 + w)):
        out.append(puerta_tablas(xx, y0, pw, h, m, sw * 0.8, random.Random(1), color=color))
    # alféizar y sombra
    out.append(f'<rect x="{f(x0-0.06*m)}" y="{f(y0+h)}" width="{f(w+0.12*m)}" height="{f(0.06*m)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
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


def afiche(x0, y0, w, h, m, sw, rnd):
    """Afiche político genérico, rojo (doc 03 §1: el color cuenta la división). Sin texto real."""
    ang = rnd.uniform(-3, 3)
    cx, cy = x0 + w / 2, y0 + h / 2
    out = [f'<g transform="rotate({f(ang)} {f(cx)} {f(cy)})" data-p="afiche genérico sin consignas ni nombres reales">']
    out.append(f'<path d="M{f(x0)},{f(y0)} L{f(x0+w)},{f(y0)} L{f(x0+w)},{f(y0+h*0.85)} L{f(x0+w*0.82)},{f(y0+h)} L{f(x0)},{f(y0+h)} Z" fill="#fff" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
    out.append(f'<rect x="{f(x0+w*0.06)}" y="{f(y0+h*0.06)}" width="{f(w*0.88)}" height="{f(h*0.26)}" fill="{ROJO}"/>')
    # estrella blanca sobre la banda roja (motivo gráfico, no un emblema real)
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
    out.append(f'<rect x="0" y="{f(y_piso)}" width="{f(W)}" height="{f(H-y_piso)}" fill="#fff" stroke="#000" stroke-width="{f(sw)}"/>')
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
        out.append(f'<rect x="{f(x0+hoja)}" y="{f(my)}" width="{f(w-2*hoja)}" height="{f(y_piso-my)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
        out.append(f'<rect x="{f(x0+hoja)}" y="{f(my)}" width="{f(w-2*hoja)}" height="{f(y_piso-my)}" fill="url(#t-madera-v)"/>')
        out.append(f'<rect x="{f(x0+hoja)}" y="{f(my)}" width="{f(w-2*hoja)}" height="{f(0.06*m)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
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
        out.append(f'<rect x="{f(x0-0.08*m)}" y="{f(y0-0.1*m)}" width="{f(w+0.16*m)}" height="{f(0.1*m)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.7)}"/>')
        out.append(f'<rect x="{f(x0-0.08*m)}" y="{f(y0-0.1*m)}" width="{f(w+0.16*m)}" height="{f(0.1*m)}" fill="url(#t-madera)"/>')
        out.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="none" stroke="#000" stroke-width="{f(sw)}"/>')
        # umbral
        out.append(f'<rect x="{f(x0-0.05*m)}" y="{f(y_piso-0.04*m)}" width="{f(w+0.1*m)}" height="{f(0.04*m)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.5)}"/>')
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
        out = [f'<rect x="{f(x0)}" y="{f(ys)}" width="{f(x1-x0)}" height="{f(0.07*m)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.7)}"/>',
               f'<rect x="{f(x0)}" y="{f(ys)}" width="{f(x1-x0)}" height="{f(0.07*m)}" fill="url(#t-madera)"/>']
        for xx in (x0 + 0.1 * m, x1 - 0.18 * m):
            out.append(f'<rect x="{f(xx)}" y="{f(ys+0.07*m)}" width="{f(0.08*m)}" height="{f(y_piso-ys-0.07*m)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
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
    """Lata con geranios sobre el piso del corredor."""
    w, h = 0.22 * m, 0.24 * m
    out = [f'<rect x="{f(x)}" y="{f(y_piso-h)}" width="{f(w)}" height="{f(h)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.6)}"/>',
           f'<rect x="{f(x)}" y="{f(y_piso-h)}" width="{f(w)}" height="{f(h)}" fill="url(#t-vert)"/>']
    for _ in range(9):
        lx = x + w / 2 + rnd.uniform(-0.2, 0.2) * m
        ly = y_piso - h - rnd.uniform(0.04, 0.3) * m
        r = rnd.uniform(0.04, 0.07) * m
        out.append(f'<circle cx="{f(lx)}" cy="{f(ly)}" r="{f(r)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.4)}"/>')
        out.append(f'<path d="M{f(lx-r*0.5)},{f(ly)} Q{f(lx)},{f(ly+r*0.4)} {f(lx+r*0.5)},{f(ly)}" stroke="#000" stroke-width="{f(sw*0.25)}" fill="none"/>')
    for _ in range(4):
        fx = x + w / 2 + rnd.uniform(-0.12, 0.12) * m
        fy = y_piso - h - rnd.uniform(0.25, 0.4) * m
        out.append(f'<circle cx="{f(fx)}" cy="{f(fy)}" r="{f(0.035*m)}" fill="#000"/>')
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
        out.append(f'<path d="M{f(x0-0.12*m)},{f(y0)} Q{f(x0+w/2)},{f(y0-0.35*m)} {f(x0+w+0.12*m)},{f(y0)} L{f(x0+w)},{f(y0)} Q{f(x0+w/2)},{f(y0-0.22*m)} {f(x0)},{f(y0)} Z" fill="#fff" stroke="#000" stroke-width="{f(sw*0.8)}"/>')
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
            out.append(f'<path d="M{f(xx)},{f(y_piso)} L{f(xx+0.22*m)},{f(y_piso-1.1*m)}" stroke="#000" stroke-width="{f(sw*1.3)}" stroke-linecap="round"/>')
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
           f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>',
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
                out.append(f'<path d="{d}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.5)}"/>')
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
    out.append(f'<path d="{d}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.8)}"/>')
    out.append(f'<path d="{d}" fill="url(#t-cruz)" opacity="0.55"/>')
    out.append(f'<path d="M{f(x+w*0.15)},{f(y_suelo-h*0.2)} Q{f(x+w*0.5)},{f(y_suelo-h*0.12)} {f(x+w*0.85)},{f(y_suelo-h*0.2)}" stroke="#000" stroke-width="{f(sw*0.35)}" fill="none"/>')
    if abierto:
        for _ in range(7):
            px = x + w * rnd.uniform(0.2, 0.8)
            py = y_suelo - h * rnd.uniform(0.92, 1.12)
            r = 0.045 * m
            out.append(f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="{f(r*1.2)}" ry="{f(r)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.45)}"/>')
            out.append(f'<circle cx="{f(px+r*0.3)}" cy="{f(py-r*0.2)}" r="{f(r*0.12)}" fill="#000"/>')
    else:
        out.append(f'<path d="M{f(x+w*0.4)},{f(y_suelo-h*0.98)} L{f(x+w*0.5)},{f(y_suelo-h*1.12)} L{f(x+w*0.6)},{f(y_suelo-h*0.98)}" stroke="#000" stroke-width="{f(sw*0.7)}" fill="#fff"/>')
    return ''.join(out)


def canasto(x, y_suelo, w, h, m, sw, rnd, carga='papas'):
    """Canasto de mimbre con su carga (papas, mazorcas o cebollas)."""
    out = []
    d = f'M{f(x)},{f(y_suelo-h)} L{f(x+w)},{f(y_suelo-h)} L{f(x+w*0.9)},{f(y_suelo)} L{f(x+w*0.1)},{f(y_suelo)} Z'
    # carga asomando
    if carga == 'mazorcas':
        for i in range(5):
            cx = x + w * (0.15 + i * 0.17)
            out.append(f'<ellipse cx="{f(cx)}" cy="{f(y_suelo-h-0.05*m)}" rx="{f(0.05*m)}" ry="{f(0.11*m)}" transform="rotate({f(rnd.uniform(-35,35))} {f(cx)} {f(y_suelo-h)})" fill="#fff" stroke="#000" stroke-width="{f(sw*0.45)}"/>')
            out.append(f'<ellipse cx="{f(cx)}" cy="{f(y_suelo-h-0.05*m)}" rx="{f(0.05*m)}" ry="{f(0.11*m)}" transform="rotate({f(rnd.uniform(-35,35))} {f(cx)} {f(y_suelo-h)})" fill="url(#t-puntos)"/>')
    elif carga == 'cebollas':
        for i in range(6):
            cx = x + w * (0.12 + i * 0.15)
            out.append(f'<circle cx="{f(cx)}" cy="{f(y_suelo-h-0.03*m)}" r="{f(0.05*m)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.45)}"/>')
            out.append(f'<path d="M{f(cx)},{f(y_suelo-h-0.08*m)} Q{f(cx+rnd.uniform(-0.1,0.1)*m)},{f(y_suelo-h-0.3*m)} {f(cx+rnd.uniform(-0.15,0.15)*m)},{f(y_suelo-h-0.42*m)}" stroke="#000" stroke-width="{f(sw*0.5)}" fill="none"/>')
    else:
        for i in range(8):
            cx = x + w * (0.1 + i * 0.11) + rnd.uniform(-0.01, 0.01) * m
            cy = y_suelo - h - rnd.uniform(0.0, 0.06) * m
            out.append(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(0.05*m)}" ry="{f(0.04*m)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.45)}"/>')
    out.append(f'<path d="{d}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.8)}"/>')
    # tejido: bandas horizontales y varillas
    for i in range(1, 5):
        yy = y_suelo - h + h * i / 5
        out.append(f'<line x1="{f(x+w*0.02*i)}" y1="{f(yy)}" x2="{f(x+w-w*0.02*i)}" y2="{f(yy)}" stroke="#000" stroke-width="{f(sw*0.4)}"/>')
    out.append(f'<path d="{d}" fill="url(#t-vert)" opacity="0.6"/>')
    out.append(f'<rect x="{f(x-0.02*m)}" y="{f(y_suelo-h-0.03*m)}" width="{f(w+0.04*m)}" height="{f(0.05*m)}" rx="{f(0.02*m)}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.6)}"/>')
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
    out.append(f'<path d="{d}" fill="#fff" stroke="#000" stroke-width="{f(sw*0.7)}"/>')
    out.append(f'<path d="{d}" fill="url(#t-media)" opacity="0.7"/>')
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


tienda_roja()
casa_porton()
empedrado()
objetos_juego()
