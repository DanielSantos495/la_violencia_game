"""Generador de la huida de la Misión 2 (game/art/src/fondos/huida/<tramo>/*.svg).

Abril de 1948, Acto I (doc 02 §5, M2 b4–b5): Rosalba sale por el boquete del solar, cruza los
cultivos de noche mientras la casa arde a lo lejos (P28: con la escopeta o la libreta), baja a la
quebrada y amanece en el monte. Composición, fuentes y [V]/[P]:
planeacion/arte/tomo1/escenarios/huida-m2.md. Escala y capas: contrato_escala.md.

Usa el vocabulario de puente_alto.py y la noche de casa_insuasty.py (usar_noche: el estilo que
elija Daniel, casa-insuasty.md §7). Todo va con el croma del Acto I (×0,65, paleta.md §5).

  python3 art/gen/huida.py              (desde game/; sin dependencias)

Edita este script, no los SVG generados.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import casa_insuasty as ci  # noqa: E402
import puente_alto as pa  # noqa: E402
from puente_alto import SOMBRA, SOMBRA_SUAVE, TRAZO, archivo, canto, f, lav, ppm, recortar  # noqa: E402

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'fondos', 'huida')
H = 1080
col, marcar = ci.col, ci.marcar


def preparar(tramo):
    pa.ESCENA, pa.GENERADOR = f'Huida de la M2 · {tramo}', 'game/art/gen/huida.py'
    pa.OUTDIR = os.path.join(BASE, tramo)


# ===================================== plantas y suelo =====================================

def mata_maiz(x, y_base, alto, rnd, m, sw, inclina=0.0):
    """Mata de maíz: caña algo torcida, hojas largas que se doblan y, a veces, una mazorca con su
    pelo y la espiga arriba. Silueta limpia: pocas hojas, sin nervios dibujados."""
    out = []
    top = (x + inclina * alto, y_base - alto)
    cana = f'M{f(x)},{f(y_base)} Q{f(x + inclina * alto * 0.3)},{f(y_base - alto * 0.5)} {f(top[0])},{f(top[1])}'
    out.append(f'<path d="{cana}" stroke="#000" stroke-width="{f(sw * 2.4)}" fill="none" stroke-linecap="round"/>'
               f'<path d="{cana}" stroke="{lav("potrero", m, 0.8)}" stroke-width="{f(sw * 1.3)}" fill="none" stroke-linecap="round"/>')
    n = rnd.randint(5, 7)
    for i in range(n):
        t = 0.18 + 0.72 * i / n
        bx = x + inclina * alto * t * (0.3 + 0.7 * t)
        by = y_base - alto * t
        lado = 1 if i % 2 == 0 else -1
        largo = alto * rnd.uniform(0.32, 0.48) * (1.1 - 0.4 * t)
        caida = rnd.uniform(0.35, 0.7)
        ex, ey = bx + lado * largo, by + largo * caida * 0.6
        cx, cy = bx + lado * largo * 0.55, by - largo * 0.25
        ancho = largo * 0.07
        hoja = (f'M{f(bx)},{f(by)} Q{f(cx)},{f(cy - ancho)} {f(ex)},{f(ey)} Q{f(cx + lado * ancho)},{f(cy + ancho)} {f(bx)},{f(by + ancho * 1.5)} Z')
        out.append(f'<path d="{hoja}" fill="{lav("sementera", m)}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
    if rnd.random() < 0.55:
        my = y_base - alto * rnd.uniform(0.45, 0.6)
        mx = x + inclina * alto * 0.5
        out.append(f'<path d="M{f(mx)},{f(my)} q{f(9)},{f(-8)} {f(14)},{f(-32)} q{f(-12)},{f(6)} {f(-14)},{f(32)} Z" fill="{lav("potrero", m)}" stroke="#000" stroke-width="{f(sw * 0.45)}"/>'
                   f'<path d="M{f(mx + 13)},{f(my - 31)} q{f(4)},{f(-8)} {f(10)},{f(-10)}" stroke="{lav("cebada", m)}" stroke-width="{f(sw * 0.6)}" fill="none"/>')
    # espiga
    out.append(f'<path d="M{f(top[0])},{f(top[1])} l{f(-6)},{f(-22)} M{f(top[0])},{f(top[1])} l{f(2)},{f(-28)} M{f(top[0])},{f(top[1])} l{f(9)},{f(-20)}" stroke="#000" stroke-width="{f(sw * 0.6)}" fill="none" stroke-linecap="round"/>')
    return ''.join(out)


def matas_maizal(x0, x1, semilla, m, alto=(1.9, 2.4), huecos=()):
    """Las matas de un maizal [P: maíz en la vereda en abril de 1948] en x del nivel, a distancias
    desiguales y con claros. Se deciden una vez: los módulos que comparten el maizal dibujan las
    mismas matas en el empalme."""
    rnd, matas, x = random.Random(semilla), [], x0
    while x < x1:
        if not any(a < x < b for a, b in huecos):
            matas.append((x, rnd.uniform(*alto) * m, rnd.uniform(-0.08, 0.08), rnd.uniform(0, 6), rnd.randrange(10 ** 6)))
        x += rnd.uniform(0.28, 0.55) * m * (2.2 if rnd.random() < 0.12 else 1)
    return matas


def maizal(matas, x_mod0, W, y_base, m, sw):
    """Las matas que caen en un módulo (con sus hojas, que pueden pasar del borde)."""
    out = [mata_maiz(x - x_mod0, y_base - dy, alto, random.Random(s), m, sw, inclina)
           for x, alto, inclina, dy, s in matas if x_mod0 - 0.6 * alto < x < x_mod0 + W + 0.6 * alto]
    return marcar('maizal: cultivo por verificar en la vereda en abril de 1948', ''.join(out))


def trigal(x0, x1, y_base, alto, rnd, m, sw, token='cebada'):
    """Sembrado de trigo o cebada (franja triguera, paleta.md [V]): masa con el borde de arriba
    hecho de espigas y unas pocas cañas sueltas."""
    y_top = y_base - alto
    d, x = f'M{f(x0)},{f(y_base)} L{f(x0)},{f(y_top + 8)}', x0
    while x < x1:
        w = rnd.uniform(6, 14)
        h = rnd.uniform(4, 16)
        d += f' Q{f(x + w * 0.3)},{f(y_top - h)} {f(x + w * 0.5)},{f(y_top - h * 0.8)} Q{f(x + w * 0.7)},{f(y_top + 2)} {f(x + w)},{f(y_top + rnd.uniform(-2, 4))}'
        x += w
    d += f' L{f(x1)},{f(y_base)} Z'
    canas = []
    for _ in range(int((x1 - x0) / 60)):
        cx = rnd.uniform(x0 + 10, x1 - 10)
        canas.append(f'M{f(cx)},{f(y_base)} q{f(rnd.uniform(-6, 6))},{f(-alto * 0.5)} {f(rnd.uniform(-8, 8))},{f(-alto * rnd.uniform(0.8, 1.05))}')
    dentro = (f'<path d="{" ".join(canas)}" stroke="#000" stroke-width="{f(sw * 0.4)}" fill="none"/>'
              f'<rect x="{f(x0)}" y="{f(y_base - alto * 0.45)}" width="{f(x1 - x0)}" height="{f(alto * 0.45)}" {SOMBRA_SUAVE}/>')
    return (f'<path d="{d}" fill="{lav(token, m)}"/>' + recortar(d, dentro)
            + f'<path d="{d}" fill="none" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')


def surcos(W, rnd, y0=900, planta='papa'):
    """Suelo de juego: surcos de tierra con matas de papa [P] que crecen con la cercanía."""
    out = [f'<rect x="0" y="{f(y0)}" width="{f(W)}" height="{f(H - y0)}" fill="{lav("tierra", 200, 0.92)}"/>']
    y, fila = y0 + 6, 0
    while y < H:
        alto = 20 + fila * 10
        out.append(f'<path d="M0,{f(y)} Q{f(W / 2)},{f(y - 5)} {f(W)},{f(y)} L{f(W)},{f(y + alto * 0.35)} Q{f(W / 2)},{f(y + alto * 0.35 - 5)} 0,{f(y + alto * 0.35)} Z" {SOMBRA}/>')
        if planta:
            x = rnd.uniform(0, 90)
            while x < W - 10:
                r = alto * rnd.uniform(0.5, 0.75)
                p = [(x + math.cos(k * math.pi / 5) * r * rnd.uniform(0.75, 1.1), y - r * 0.4 + math.sin(k * math.pi / 5) * r * 0.55) for k in range(10)]
                out.append(f'<path d="{canto(p)}" fill="{lav("sementera", 200)}" stroke="#000" stroke-width="{f(TRAZO["juego"] * 0.45)}"/>')
                x += r * rnd.uniform(6, 11)
        y += alto + 14
        fila += 1
    return marcar('cultivo de papa en surcos: por verificar', ''.join(out))


# ====================================== la casa ardiendo ======================================

def lengua(x, y_base, alto, ancho, rnd):
    """Lengua de fuego plana: ocre por fuera, amarilla dentro, núcleo claro (paleta.md §3)."""
    puntas = [(x - ancho / 2, y_base)]
    n = rnd.randint(2, 3)
    for k in range(n):
        px = x - ancho / 2 + ancho * (k + 0.5) / n + rnd.uniform(-4, 4)
        puntas += [(px - ancho / (2 * n) * 0.4, y_base - alto * rnd.uniform(0.35, 0.55)),
                   (px + rnd.uniform(-6, 6), y_base - alto * rnd.uniform(0.75, 1.05)),
                   (px + ancho / (2 * n) * 0.4, y_base - alto * rnd.uniform(0.35, 0.55))]
    puntas.append((x + ancho / 2, y_base))
    d = 'M' + ' L'.join(f'{f(px)},{f(py)}' for px, py in puntas) + ' Z'
    nucleo = (f'M{f(x - ancho * 0.25)},{f(y_base)} Q{f(x - ancho * 0.1)},{f(y_base - alto * 0.45)} {f(x)},{f(y_base - alto * 0.55)} '
              f'Q{f(x + ancho * 0.1)},{f(y_base - alto * 0.45)} {f(x + ancho * 0.25)},{f(y_base)} Z')
    return (f'<path d="{d}" fill="{col("llama")}" stroke="{col("brasa")}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="{nucleo}" fill="{col("llama-nucleo")}"/>')


def casa_ardiendo():
    """La casa de los Insuasty ardiendo vista desde los cultivos, a decenas de metros (capa lejana,
    30 px/m): el tejado hundido, las ventanas encendidas y la columna de humo. Sin gente ni
    espectáculo: se ve lo que se pierde (doc 03 §1, «Violencia»)."""
    rnd = random.Random(1948)
    m, sw = ppm('lejos'), TRAZO['lejos']
    W, Hh = 700, 760                 # se coloca arriba en y=0; el suelo lejano queda en y=628
    suelo = 628
    x0, x1 = 140, 140 + 14 * m
    y_alero = suelo - 3.0 * m
    casa = [f'<rect x="{f(x0)}" y="{f(y_alero)}" width="{f(x1 - x0)}" height="{f(suelo - y_alero)}" fill="{lav("cal", m)}" stroke="#000" stroke-width="{f(sw)}"/>',
            f'<rect x="{f(x0)}" y="{f(suelo - 0.8 * m)}" width="{f(x1 - x0)}" height="{f(0.8 * m)}" fill="{lav("tapia", m)}"/>']
    # tejado a medio hundir: dos aguas rotas
    techo = (f'M{f(x0 - 9)},{f(y_alero)} L{f(x0 + 2.5 * m)},{f(y_alero - 1.3 * m)} L{f(x0 + 5 * m)},{f(y_alero - 0.5 * m)} '
             f'L{f(x0 + 6.2 * m)},{f(y_alero - 0.1 * m)} L{f(x0 + 9 * m)},{f(y_alero - 1.0 * m)} L{f(x1 - 1 * m)},{f(y_alero - 1.3 * m)} L{f(x1 + 9)},{f(y_alero)} Z')
    casa.append(f'<path d="{techo}" fill="{lav("teja", m)}" stroke="#000" stroke-width="{f(sw)}"/>')
    # vigas al aire donde se hundió
    casa.append(f'<path d="M{f(x0 + 5 * m)},{f(y_alero - 0.5 * m)} L{f(x0 + 5.6 * m)},{f(y_alero - 1.6 * m)} M{f(x0 + 6.6 * m)},{f(y_alero - 0.2 * m)} L{f(x0 + 7.3 * m)},{f(y_alero - 1.4 * m)}" stroke="#000" stroke-width="{f(sw * 2.4)}" stroke-linecap="round"/>')
    ventanas = [(x0 + 2.0 * m, 1.1), (x0 + 7.4 * m, 1.0), (x0 + 11.2 * m, 0.9)]
    for vx, vw in ventanas:
        casa.append(f'<rect x="{f(vx)}" y="{f(suelo - 2.1 * m)}" width="{f(vw * m)}" height="{f(1.0 * m)}" fill="#000"/>')
    casa.append(f'<rect x="{f(x0 + 4.4 * m)}" y="{f(suelo - 2.1 * m)}" width="{f(0.95 * m)}" height="{f(2.1 * m)}" fill="#000"/>')
    noche = ci.de_noche(W, Hh, ''.join(casa), a=ci.NOCHE['lejos'], capa='lejos')
    # la luz del fuego: charco plano sobre el suelo y la fachada, ventanas y puerta encendidas
    luz = [f'<ellipse cx="{f((x0 + x1) / 2)}" cy="{f(suelo)}" rx="{f(11 * m)}" ry="{f(1.6 * m)}" fill="{col("llama")}" fill-opacity="0.16"/>',
           f'<rect x="{f(x0)}" y="{f(y_alero)}" width="{f(x1 - x0)}" height="{f(suelo - y_alero)}" fill="{col("brasa")}" fill-opacity="0.18"/>']
    for vx, vw in ventanas:
        luz.append(f'<rect x="{f(vx + 2)}" y="{f(suelo - 2.1 * m + 2)}" width="{f(vw * m - 4)}" height="{f(1.0 * m - 4)}" fill="{col("llama")}"/>'
                   f'<rect x="{f(vx + vw * m * 0.3)}" y="{f(suelo - 2.1 * m + 6)}" width="{f(vw * m * 0.4)}" height="{f(1.0 * m * 0.5)}" fill="{col("llama-nucleo")}"/>')
    luz.append(f'<rect x="{f(x0 + 4.4 * m + 2)}" y="{f(suelo - 2.1 * m + 2)}" width="{f(0.95 * m - 4)}" height="{f(2.1 * m - 2)}" fill="{col("brasa")}"/>')
    # humo: columna que sube y se tuerce con el viento, iluminada por debajo
    humo = []
    cx, cy, r = x0 + 6.2 * m, y_alero - 1.6 * m, 22
    nubes = []
    while cy > 10:
        nubes.append((cx, cy, r))
        cy -= r * 0.9
        cx += r * rnd.uniform(0.25, 0.6)
        r *= rnd.uniform(1.04, 1.12)
    for i, (hx, hy, hr) in enumerate(nubes):
        p = [(hx + math.cos(k * math.pi / 5) * hr * rnd.uniform(0.82, 1.12), hy + math.sin(k * math.pi / 5) * hr * 0.75 * rnd.uniform(0.82, 1.12)) for k in range(10)]
        d = canto(p)
        humo.append(f'<path d="{d}" fill="{col("humo")}" fill-opacity="{0.9 - 0.4 * i / len(nubes):.2f}"/>')
        if i < 4:
            humo.append(recortar(d, f'<ellipse cx="{f(hx)}" cy="{f(hy + hr * 0.7)}" rx="{f(hr)}" ry="{f(hr * 0.5)}" fill="{col("brasa")}" fill-opacity="0.35"/>'))
    # lenguas de fuego que salen por el tejado hundido y unas chispas
    fuego = [lengua(x0 + 5.3 * m, y_alero - 0.2 * m, 2.6 * m, 2.4 * m, rnd), lengua(x0 + 6.9 * m, y_alero, 3.3 * m, 2.2 * m, rnd),
             lengua(x0 + 8.3 * m, y_alero - 0.4 * m, 2.0 * m, 1.6 * m, rnd)]
    for _ in range(9):
        fuego.append(f'<circle cx="{f(x0 + rnd.uniform(4, 10) * m)}" cy="{f(y_alero - rnd.uniform(3, 7) * m)}" r="{f(rnd.uniform(1.4, 2.2))}" fill="{col("llama-nucleo")}"/>')
    cuerpo = ''.join(humo) + noche + ''.join(luz) + ''.join(fuego)
    archivo('casa-ardiendo', W, Hh, 'lejos', 'la casa de los Insuasty ardiendo, vista desde los cultivos', cuerpo,
            notas='Se coloca arriba (y=0); el suelo lejano queda en y=628. Fuego en ocre y amarillo, nunca rojo (paleta.md §3); '
                  'sin personas: la quema se ve a distancia (doc 02 M2 b4).')


# ====================================== tramos del nivel ======================================

def modulo_juego(nombre, W, titulo, dibujo, luz='', notas='', noche=True):
    cuerpo = (ci.de_noche(W, H, dibujo) if noche else dibujo) + luz
    archivo(nombre, W, H, 'juego', titulo, cuerpo, notas=f'Se coloca arriba (y=0). {notas}')


def cultivos():
    preparar('cultivos')
    m, sw = ppm('juego'), TRAZO['juego']
    # El cielo, las lomas y el campo de la vereda son los de la casa (casa_insuasty.py).
    ci.cielo_noche()
    ci.lomas('lomas-1', 0, 900, 61, casas=[620])
    ci.lomas('lomas-2', 860, 900, 62, casas=[300])
    ci.lomas('lomas-3', 1720, 776, 63, casas=[])
    casa_ardiendo()
    # Árboles más bajos y lejos de la casa que arde (lx 290–710 ≈ mx 290–1400 mientras se ve)
    ci.campo('campos-1', 0, 940, 71, arboles=[], alto_arbol=5, ancho_arbol=3.3)
    ci.campo('campos-2', 900, 940, 72, arboles=[700], alto_arbol=5, ancho_arbol=3.3)
    ci.campo('campos-3', 1800, 940, 73, arboles=[240, 640], alto_arbol=5, ancho_arbol=3.3)
    ci.campo('campos-4', 2700, 948, 74, arboles=[420], alto_arbol=5, ancho_arbol=3.3)

    rnd = random.Random(481)
    # 1. salida del solar: cerca con su boquete y papa en surcos
    W = 960
    modulo_juego('salida', W, 'salida del solar: la cerca y la senda entre la papa',
                 ci.cerca_piedra(-20, W - 120, 880, 0.75 * m, rnd, hueco=(120, 300)) + surcos(W, rnd),
                 notas='Por el boquete (x 120–300) entra Rosalba desde la casa.')
    # 2 y 3. maizal alto: donde agacharse (sigilo). Un solo maizal de x 1220 a 2620 del nivel, con
    # un claro en medio, repartido en dos módulos.
    matas = matas_maizal(1220, 2620, 4811, m, huecos=((1840, 1990),))
    for i, nombre in enumerate(('maizal-1', 'maizal-2')):
        modulo_juego(nombre, W, 'maizal alto, donde esconderse',
                     maizal(matas, 960 * (i + 1), W, 896, m, sw) + surcos(W, rnd, planta=None),
                     notas='Maíz de 1,9 a 2,4 m: cubre a Rosalba agachada [P].')
    # 4. trigo o cebada a media altura y una cerca con portillo
    modulo_juego('trigal', W, 'cebada a media altura y cerca con portillo',
                 trigal(60, W - 80, 896, 1.2 * m, rnd, m, sw) + ci.cerca_piedra(420, W - 60, 900, 0.7 * m, rnd, hueco=(560, 700))
                 + surcos(W, rnd, planta=None))
    # 5. papa y un árbol solo
    modulo_juego('papal', W, 'papal en surcos y un árbol solo',
                 ci.arbol(300, 880, 3.3 * m, 2.3 * m, rnd) + surcos(W, rnd))
    # 6. el borde del barranco: matorral de monte y la senda que baja a la quebrada
    monte = []
    for k in range(9):
        cx = 380 + k * 70 + rnd.uniform(-20, 20)
        r = rnd.uniform(0.5, 0.9) * m
        p = [(cx + math.cos(a * math.pi / 6) * r * rnd.uniform(0.8, 1.1), 860 - r * 0.6 + math.sin(a * math.pi / 6) * r * 0.7 * rnd.uniform(0.8, 1.1)) for a in range(12)]
        monte.append(f'<path d="{canto(p)}" fill="{lav("monte", m)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
    modulo_juego('barranco', W, 'borde del barranco: matorral y la senda que baja a la quebrada',
                 marcar('matorral de monte: por verificar', ''.join(monte)) + surcos(W, rnd, planta=None)
                 + f'<path d="M{W - 260},{H} Q{W - 180},960 {W},920 L{W},{H} Z" fill="{lav("tierra", m, 0.7)}"/>',
                 notas='La senda sale por la derecha hacia la quebrada.')
    ci.maguey('maguey', 81)


# ========================================= la quebrada =========================================

def piedra(x, y_base, w, h, rnd, m, sw, token='piedra', luz=0.85):
    """Piedra de río o de ladera: canto redondo con la cara de la derecha en sombra."""
    p = [(x + w / 2 + math.cos(k * math.pi / 5) * w / 2 * rnd.uniform(0.85, 1.08),
          y_base - h / 2 + math.sin(k * math.pi / 5) * h / 2 * rnd.uniform(0.85, 1.08)) for k in range(10)]
    d = canto(p)
    return (f'<path d="{d}" fill="{lav(token, m, luz)}"/>'
            + recortar(d, f'<path d="M{f(x + w * 0.55)},{f(y_base - h * 1.1)} Q{f(x + w * 0.8)},{f(y_base - h * 0.5)} {f(x + w * 0.6)},{f(y_base + 2)} L{f(x + w * 1.1)},{f(y_base + 2)} L{f(x + w * 1.1)},{f(y_base - h * 1.1)} Z" {SOMBRA}/>'
                             f'<rect x="{f(x)}" y="{f(y_base - h * 0.18)}" width="{f(w)}" height="{f(h * 0.2)}" {SOMBRA_SUAVE}/>')
            + f'<path d="{d}" fill="none" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')


def helecho(x, y_base, alto, rnd, m, sw, lado=1):
    """Helecho de quebrada: frondas que se arquean, cada una una hoja larga con su nervio."""
    out = []
    for k in range(rnd.randint(3, 5)):
        a = math.radians(-70 + k * 30 + rnd.uniform(-10, 10)) * lado
        largo = alto * rnd.uniform(0.7, 1.0)
        ex, ey = x + math.sin(a) * largo, y_base - math.cos(a) * largo * 0.8
        cx, cy = x + math.sin(a) * largo * 0.4, y_base - largo * 0.9
        d = f'M{f(x - 3)},{f(y_base)} Q{f(cx - 6)},{f(cy)} {f(ex)},{f(ey)} Q{f(cx + 6)},{f(cy + 10)} {f(x + 3)},{f(y_base)} Z'
        out.append(f'<path d="{d}" fill="{lav("monte", m, 0.9)}" stroke="#000" stroke-width="{f(sw * 0.45)}"/>'
                   + recortar(d, f'<path d="M{f(x)},{f(y_base)} Q{f(cx)},{f(cy + 4)} {f(ex)},{f(ey)}" stroke="#000" stroke-width="{f(sw * 0.3)}" fill="none"/>'))
    return ''.join(out)


def matorral(x0, x1, y_base, alto, rnd, m, sw, token='monte'):
    """Matorral de monte: masa de copas bajas con su sombra abajo (detalle limpio: pocas masas)."""
    out, x = [], x0
    while x < x1:
        r = rnd.uniform(0.45, 0.8) * alto
        cx, cy = x + r * 0.8, y_base - r * rnd.uniform(0.6, 0.9)
        if out and cx + r * 1.1 > x1:
            break  # el matorral no pasa de x1: no se corta en el borde del módulo
        p = [(cx + math.cos(k * math.pi / 6) * r * rnd.uniform(0.82, 1.08), cy + math.sin(k * math.pi / 6) * r * 0.75 * rnd.uniform(0.82, 1.08)) for k in range(12)]
        d = canto(p)
        out.append(f'<path d="{d}" fill="{lav(token, m)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>'
                   + recortar(d, f'<path d="M{f(cx - r)},{f(cy + r * 0.25)} Q{f(cx)},{f(cy + r * 0.8)} {f(cx + r)},{f(cy + r * 0.25)} L{f(cx + r)},{f(cy + r)} L{f(cx - r)},{f(cy + r)} Z" {SOMBRA}/>'))
        x += r * rnd.uniform(1.0, 1.5)
    return ''.join(out)


def orilla(W, rnd, y0=900):
    """Suelo de la orilla: tierra mojada con piedras sueltas."""
    m, sw = ppm('juego'), TRAZO['juego']
    out = [f'<rect x="0" y="{f(y0)}" width="{f(W)}" height="{f(H - y0)}" fill="{lav("barro", m, 0.95)}"/>',
           f'<rect x="0" y="{f(y0)}" width="{f(W)}" height="10" {SOMBRA}/>']
    for _ in range(int(W / 110)):
        x, y = rnd.uniform(0, W - 60), rnd.uniform(y0 + 30, H - 6)
        k = 0.6 + (y - y0) / (H - y0)
        out.append(piedra(x, y, rnd.uniform(28, 60) * k, rnd.uniform(14, 26) * k, rnd, m, sw))
    return ''.join(out)


def cauce(W, rnd, y0=900):
    """El agua de la quebrada atraviesa el camino: corriente gris verdosa (el agua no es azul,
    paleta.md §3) con unas pocas ondas y las piedras por donde se pasa."""
    m, sw = ppm('juego'), TRAZO['juego']
    out = [f'<rect x="0" y="{f(y0)}" width="{f(W)}" height="{f(H - y0)}" fill="{lav("agua", m)}"/>',
           f'<rect x="0" y="{f(y0)}" width="{f(W)}" height="18" {SOMBRA}/>']
    ondas = []
    for _ in range(int(W / 60)):
        x, y = rnd.uniform(0, W - 80), rnd.uniform(y0 + 24, H - 10)
        ondas.append(f'M{f(x)},{f(y)} q{f(18)},{f(-5)} {f(36)},0 q{f(14)},{f(4)} {f(rnd.uniform(26, 50))},{f(rnd.uniform(-2, 2))}')
    out.append(f'<path d="{" ".join(ondas)}" stroke="#fff" stroke-width="{f(sw * 0.6)}" stroke-opacity="0.5" fill="none" stroke-linecap="round"/>')
    # piedras para pasar, de una orilla a la otra
    x = 30
    while x < W - 60:
        w = rnd.uniform(70, 110)
        out.append(piedra(x, y0 + rnd.uniform(70, 110), w, rnd.uniform(26, 34), rnd, m, sw, luz=0.75))
        x += w + rnd.uniform(40, 90)
    return ''.join(out)


# Perfil de las paredes de la quebrada en toda la capa media (2784 px), para que los módulos empalmen
_RND_BARRANCA = random.Random(90)
PERFIL_BARRANCA = pa.perfil([(x, _RND_BARRANCA.uniform(150, 330)) for x in range(0, 2785 + 240, 240)],
                            0, 2784 + 40, _RND_BARRANCA, 2, paso=8)


def _copas_barranca():
    """Copas del borde de la barranca, decididas una vez para toda la capa: los dos módulos de un
    empalme dibujan la misma copa y no queda corte."""
    rnd, copas, x = random.Random(91), [], -40.0
    while x < 2784 + 80:
        r = rnd.uniform(34, 62)
        copas.append((x, r, [rnd.uniform(0.85, 1.08) for _ in range(24)]))
        x += r * rnd.uniform(1.1, 1.5)
    return copas


COPAS_BARRANCA = _copas_barranca()


def barranca(x_capa0, W, semilla, y0=60):
    """Las paredes de la quebrada: ladera de monte que sube y encierra la vista. Arriba, el borde es
    la silueta de las copas; dentro, unos troncos y piedras; abajo, el agua sigue corriendo."""
    rnd = random.Random(semilla)
    m, sw = ppm('medio'), TRAZO['medio']
    Hh = 920 - y0
    suelo = 724 - y0
    perf = [(x - x_capa0, y - y0) for x, y in PERFIL_BARRANCA if x_capa0 - 10 <= x <= x_capa0 + W + 10]
    d = f'M{f(perf[0][0])},{Hh} L{" L".join(f"{f(x)},{f(y)}" for x, y in perf)} L{f(perf[-1][0])},{Hh} Z'
    out = [f'<path d="{d}" fill="{lav("monte", m, 0.9)}"/>']
    # copas que dibujan el borde: masas redondas centradas en el perfil (continuas entre módulos
    # porque salen del mismo perfil)
    copas = []
    for gx, r, j in COPAS_BARRANCA:
        x = gx - x_capa0
        if x < -r * 1.2 or x > W + r * 1.2:
            continue
        cy = pa.y_de(PERFIL_BARRANCA, gx) - y0 + r * 0.55
        p = [(x + math.cos(k * math.pi / 6) * r * j[2 * k], cy + math.sin(k * math.pi / 6) * r * 0.8 * j[2 * k + 1]) for k in range(12)]
        copas.append(f'<path d="{canto(p)}" fill="{lav("monte", m)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>'
                     f'<path d="M{f(x - r * 0.8)},{f(cy + r * 0.2)} Q{f(x)},{f(cy + r * 0.75)} {f(x + r * 0.8)},{f(cy + r * 0.2)}" stroke="#000" stroke-width="{f(sw * 0.4)}" fill="none"/>')
    dentro = []
    for _ in range(int(W / 220)):
        tx = rnd.uniform(30, W - 30)
        ty = pa.y_de(perf, tx) + 60
        dentro.append(f'<path d="M{f(tx - 9)},{f(suelo)} L{f(tx - 4)},{f(ty)} L{f(tx + 4)},{f(ty)} L{f(tx + 10)},{f(suelo)} Z" fill="{lav("madera", m, 0.8)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
    for _ in range(int(W / 300)):
        dentro.append(piedra(rnd.uniform(20, W - 160), suelo - 4, rnd.uniform(90, 160), rnd.uniform(50, 80), rnd, m, sw))
    dentro.append(f'<rect x="0" y="{f(suelo - 60)}" width="{W}" height="{f(Hh - suelo + 60)}" {SOMBRA}/>')
    out.append(recortar(d, ''.join(dentro)))
    out.extend(copas)
    # el agua sigue al pie de la pared
    agua = [f'<rect x="0" y="{f(suelo - 6)}" width="{W}" height="{f(Hh - suelo + 6)}" fill="{lav("agua", m)}"/>']
    for _ in range(int(W / 120)):
        ax, ay = rnd.uniform(0, W - 60), rnd.uniform(suelo + 10, Hh - 10)
        agua.append(f'<path d="M{f(ax)},{f(ay)} q14,-4 28,0 q10,3 {f(rnd.uniform(16, 32))},0" stroke="#fff" stroke-width="{f(sw * 0.5)}" stroke-opacity="0.45" fill="none"/>')
    out.extend(agua)
    return marcar('monte de la quebrada: vegetación por verificar', ''.join(out)), Hh


def quebrada():
    preparar('quebrada')
    m, sw = ppm('juego'), TRAZO['juego']
    ci.cielo_noche()
    # al fondo, por encima de la barranca, el resplandor de la casa que sigue ardiendo
    rnd = random.Random(1949)
    W, Hh = 1100, 700
    humo = []
    cx, cy, r = 260, 560, 26
    while cy > 20:
        p = [(cx + math.cos(k * math.pi / 5) * r * rnd.uniform(0.82, 1.12), cy + math.sin(k * math.pi / 5) * r * 0.75) for k in range(10)]
        humo.append(f'<path d="{canto(p)}" fill="{col("humo")}" fill-opacity="0.7"/>')
        cy -= r * 0.9
        cx += r * rnd.uniform(0.3, 0.6)
        r *= 1.08
    archivo('resplandor', W, Hh, 'lejos', 'humo y resplandor de la casa, detrás de la barranca',
            f'<ellipse cx="260" cy="600" rx="300" ry="120" fill="{col("llama")}" fill-opacity="0.14"/>'
            f'<ellipse cx="260" cy="610" rx="150" ry="60" fill="{col("llama")}" fill-opacity="0.16"/>' + ''.join(humo),
            notas='Se coloca arriba (y=0) en la capa lejana; la barranca tapa la casa y solo se ven el humo y el resplandor.')
    for i, (x, w) in enumerate(((0, 1000), (940, 1000), (1880, 904))):
        dibujo, hh = barranca(x, w, 90 + i)
        archivo(f'barranca-{i + 1}', w, hh, 'medio', 'pared de la quebrada: ladera de monte', ci.de_noche(w, hh, dibujo, a=ci.NOCHE['lejos'], capa='medio'),
                notas=f'Se coloca arriba en y=60 de la capa media, en x={x}.')
    rnd = random.Random(503)
    W = 960
    modulo_juego('bajada', W, 'bajada a la quebrada entre helechos y piedras',
                 matorral(-20, 420, 880, 1.0 * m, rnd, m, sw) + helecho(560, 900, 0.9 * m, rnd, m, sw)
                 + helecho(760, 900, 0.7 * m, rnd, m, sw, -1) + orilla(W, rnd),
                 notas='Viene del borde del barranco de los cultivos.')
    modulo_juego('cauce-1', W, 'el agua de la quebrada y las piedras para pasar',
                 piedra(80, 900, 1.4 * m, 0.7 * m, rnd, m, sw) + helecho(860, 900, 0.8 * m, rnd, m, sw) + cauce(W, rnd))
    modulo_juego('cauce-2', W, 'la otra orilla: un tronco caído sobre el agua',
                 f'<path d="M-40,850 L620,790 L630,820 L-40,880 Z" fill="{lav("madera", m, 0.8)}" stroke="#000" stroke-width="{f(sw)}"/>'
                 f'<path d="M-40,872 L626,812" stroke="#000" stroke-width="{f(sw * 0.4)}" fill="none"/>'
                 + piedra(680, 900, 1.6 * m, 0.9 * m, rnd, m, sw) + cauce(W, rnd))
    modulo_juego('subida', W, 'la subida al monte entre matorrales',
                 matorral(80, 520, 890, 1.4 * m, rnd, m, sw) + helecho(640, 900, 1.0 * m, rnd, m, sw)
                 + matorral(700, W + 40, 880, 1.2 * m, rnd, m, sw) + orilla(W, rnd),
                 notas='Sale por la derecha hacia el monte.')
    ci.maguey('maguey', 82)


# ====================================== el monte al amanecer ======================================

def de_niebla(W, Hh, dibujo, a, capa='juego'):
    """Mezcla cada color con la niebla en la proporción a: lo lejano se pierde en la bruma (como
    la noche de casa_insuasty.py, sin filtro SVG). W y Hh quedan por simetría con de_noche."""
    n = ci._rgb(col('niebla'))
    return ci.mezclar_colores(dibujo, lambda c: [(1 - a) * v + a * k for v, k in zip(c, n)], capa)


def banco_niebla(x0, x1, y, alto, rnd, opacidad=0.55):
    """Banco de niebla plano, de borde suave hecho a mano (sin degradado)."""
    d, x = f'M{f(x0)},{f(y + alto)}', x0
    while x < x1:
        w = rnd.uniform(60, 140)
        d += f' Q{f(x + w / 2)},{f(y - rnd.uniform(0, alto * 0.6))} {f(x + w)},{f(y + rnd.uniform(-6, 6))}'
        x += w
    d += f' L{f(x1)},{f(y + alto)} Z'
    return f'<path d="{d}" fill="{col("niebla")}" fill-opacity="{opacidad}"/>'


def fogata(x, y_base, rnd, m, sw):
    """Fogata de los desplazados: piedras en corro, leña cruzada, fuego bajo y un hilo de humo."""
    out = []
    for k in range(6):
        px = x - 70 + k * 26 + rnd.uniform(-4, 4)
        out.append(piedra(px, y_base + 4, 30, 18, rnd, m, sw))
    out.append(f'<path d="M{f(x - 40)},{f(y_base - 6)} L{f(x + 40)},{f(y_base - 26)} M{f(x - 36)},{f(y_base - 26)} L{f(x + 44)},{f(y_base - 4)}" stroke="#000" stroke-width="{f(sw * 3)}" stroke-linecap="round"/>'
               f'<path d="M{f(x - 40)},{f(y_base - 6)} L{f(x + 40)},{f(y_base - 26)} M{f(x - 36)},{f(y_base - 26)} L{f(x + 44)},{f(y_base - 4)}" stroke="{lav("madera", m, 0.8)}" stroke-width="{f(sw * 1.6)}" stroke-linecap="round"/>')
    out.append(lengua(x, y_base - 10, 70, 60, rnd))
    d, yy, xx = f'M{f(x)},{f(y_base - 80)}', y_base - 80, x
    while yy > y_base - 520:
        yy -= 50
        xx += rnd.uniform(-10, 30)
        d += f' Q{f(xx - rnd.uniform(-25, 25))},{f(yy + 25)} {f(xx)},{f(yy)}'
    out.append(f'<path d="{d}" stroke="{col("humo-claro")}" stroke-width="16" stroke-opacity="0.35" fill="none" stroke-linecap="round"/>')
    return ''.join(out)


def monte():
    preparar('monte')
    m, sw = ppm('juego'), TRAZO['juego']
    rnd = random.Random(1950)
    # cielo del alba: el fondo de cámara es la niebla; una franja ocre donde va a salir el sol
    # (el amanecer va en ocre y amarillo, nunca rojo: paleta.md §3) y las sierras en bruma
    W, Hh = 1920, 700
    cielo = [f'<path d="M0,430 Q480,400 960,420 T1920,410 L1920,{Hh} L0,{Hh} Z" fill="{col("llama")}" fill-opacity="0.18"/>',
             f'<path d="M0,470 Q600,455 1200,468 T1920,462 L1920,{Hh} L0,{Hh} Z" fill="{col("llama-nucleo")}" fill-opacity="0.35"/>']
    for k, (base, amp, op) in enumerate(((520, 60, 0.35), (575, 45, 0.5))):
        perf = pa.perfil([(x, base - rnd.uniform(0, amp)) for x in range(0, 1921, 240)], 0, 1920, rnd, 3, paso=12)
        cielo.append(f'<path d="M0,{Hh} L{" L".join(f"{f(x)},{f(y)}" for x, y in perf)} L1920,{Hh} Z" fill="{col("gris-claro")}" fill-opacity="{op}"/>')
    archivo('cielo-alba', W, Hh, 'cielo', 'cielo del amanecer: franja ocre y sierras en bruma', ''.join(cielo),
            notas='Se coloca arriba (y=0). El fondo de cámara es la niebla.')
    # el valle allá abajo, en bruma, con un hilo de humo: la casa que ya no está
    Hh = 380
    for i, (x, W) in enumerate(((0, 1150), (1100, 1108))):
        valle = [f'<path d="M0,{Hh} L0,190 Q{W * 0.25},150 {W * 0.5},180 T{W},170 L{W},{Hh} Z" fill="{lav("potrero", 30)}" stroke="#000" stroke-width="1.1"/>']
        for _ in range(8):
            vx = rnd.uniform(30, W - 100)
            valle.append(f'<path d="M{f(vx)},{f(rnd.uniform(200, 300))} q{f(rnd.uniform(50, 90))},{f(rnd.uniform(-6, 8))} {f(rnd.uniform(110, 180))},{f(rnd.uniform(-4, 14))}" stroke="#000" stroke-width="0.7" fill="none"/>')
        humo_lejano = (f'<path d="M420,200 q-10,-40 6,-80 q14,-40 -2,-90 q-10,-30 10,-60" stroke="{col("humo-claro")}" stroke-width="7" stroke-opacity="0.45" fill="none" stroke-linecap="round"/>'
                       if i == 0 else '')
        archivo(f'valle-{i + 1}', W, Hh, 'lejos', 'el valle de la vereda en la bruma' + (', con un hilo de humo' if i == 0 else ''),
                de_niebla(W, Hh, ''.join(valle), 0.62, capa='lejos') + humo_lejano + banco_niebla(0, W, 250, 130, rnd, 0.6),
                notas=f'Se coloca arriba en y=380 de la capa lejana, en x={x}.' + (' El humo es el de la casa: lo que ya no está.' if i == 0 else ''))
    # troncos del monte en la bruma (capa media)
    for i, (x, w) in enumerate(((0, 1000), (940, 1000), (1880, 904))):
        rr = random.Random(120 + i)
        mm, ss = ppm('medio'), TRAZO['medio']
        dib = []
        for k in range(rr.randint(2, 3)):
            tx = rr.uniform(240, w - 240)
            dib.append(ci.arbol(tx, 724, rr.uniform(6.5, 7.6) * mm, rr.uniform(3.5, 4.5) * mm, rr, mm, ss))
        dib.append(matorral(40, w - 40, 724, 1.4 * mm, rr, mm, ss))
        dib.append(f'<rect x="0" y="724" width="{w}" height="196" fill="{lav("barro", mm)}"/>')
        archivo(f'monte-{i + 1}', w, 920, 'medio', 'troncos y matorral del monte en la bruma',
                marcar('monte de vertiente: especies por verificar', de_niebla(w, 920, ''.join(dib), 0.42, capa='medio') + banco_niebla(0, w, 640, 140, rr, 0.45)),
                notas=f'Se coloca arriba en y=0 de la capa media, en x={x}: caben las copas enteras.')
    rnd = random.Random(507)
    W = 960
    modulo_juego('sendero-1', W, 'sendero del monte entre raíces y helechos',
                 de_niebla(W, H, ci.arbol(220, 900, 4.2 * m, 2.6 * m, rnd) + helecho(560, 900, 0.9 * m, rnd, m, sw)
                           + matorral(640, W - 160, 890, 1.0 * m, rnd, m, sw) + orilla(W, rnd), 0.12), noche=False)
    modulo_juego('sendero-2', W, 'el sendero sigue; una piedra grande y helechos',
                 de_niebla(W, H, piedra(200, 900, 2.2 * m, 1.2 * m, rnd, m, sw) + helecho(620, 900, 1.0 * m, rnd, m, sw, -1)
                           + helecho(760, 900, 0.8 * m, rnd, m, sw) + orilla(W, rnd), 0.12), noche=False)
    modulo_juego('claro', W, 'el claro de los desplazados: la fogata y sus atados',
                 de_niebla(W, H, matorral(40, 200, 890, 1.0 * m, rnd, m, sw) + orilla(W, rnd)
                           + pa.costal(560, 900, 0.55 * m, 0.6 * m, m, sw, rnd) + pa.costal(640, 900, 0.5 * m, 0.45 * m, m, sw, rnd)
                           + pa.olla(720, 900, 0.4 * m, 0.32 * m, m, sw, rnd), 0.1)
                 + fogata(380, 900, rnd, m, sw),
                 notas='Aquí la esperan otros desplazados (M2 b5); los personajes los pone la escena.', noche=False)
    modulo_juego('salida-monte', W, 'el monte sigue hacia arriba',
                 de_niebla(W, H, matorral(60, 520, 890, 1.3 * m, rnd, m, sw) + ci.arbol(760, 900, 4.6 * m, 2.8 * m, rnd)
                           + orilla(W, rnd), 0.14), noche=False)
    ci.maguey('maguey', 83)


if __name__ == '__main__':
    pa.usar_acto('acto1')
    cultivos()
    quebrada()
    monte()
