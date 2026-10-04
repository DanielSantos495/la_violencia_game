"""Generador de la casa de los Insuasty, de noche (game/art/src/fondos/casa-insuasty/*/*.svg).

Prólogo b4 (junio de 1946: la reunión liberal para oír la radio, P27) y Misión 2 (abril de 1948:
la partida, P24–P28) (doc 02 §5). Composición, fuentes y [V]/[P]:
planeacion/arte/tomo1/escenarios/casa-insuasty.md. Escala y capas: contrato_escala.md.

Interior en corte: se mira desde el solar, sin el muro de atrás. Cada cuarto es una viñeta de la
página: los muros cortados y el suelo quedan en papel (el margen y el canal entre viñetas) y por
las puertas de esos canales se pasa de un cuarto a otro. La noche es una aguada de tinta plana
con charcos de luz escalonados alrededor de la lámpara y del fogón, sin degradados (doc 03 §1).

Vocabulario de dibujo y paleta: puente_alto.py. Cada acto sale en su carpeta, con el croma de su
guion de color (paleta.md §5): el Prólogo ×1 y la Misión 2 (Acto I) ×0,65.

  python3 art/gen/casa_insuasty.py      (desde game/; sin dependencias)

Edita este script, no los SVG generados.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import puente_alto as pa  # noqa: E402
from puente_alto import (  # noqa: E402
    SOMBRA, SOMBRA_FUERTE, SOMBRA_HONDA, SOMBRA_SUAVE, TRAZO, archivo, canto, costal, f, lav, muro_cal,
    olla, ppm, pts, puerta_tablas, recortar, zocalo,
)

pa.ESCENA, pa.GENERADOR = 'Casa Insuasty', 'game/art/gen/casa_insuasty.py'
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'fondos', 'casa-insuasty')

M, SW = ppm('juego'), TRAZO['juego']
H = 1080
Y_MARCO, Y_PISO, Y_BAJO = 44, 900, 924   # borde de arriba de la viñeta, suelo, borde de abajo
Y_SOLERA = Y_PISO - 2.7 * M              # remate de la tapia: encima, el envés del tejado
Y_DINTEL = Y_PISO - 1.9 * M              # dintel de las puertas entre cuartos
# Aguada de la noche por escalones (fill-opacity de la tinta): sin degradados.
# Tratamiento de la noche (muestras A–D, casa-insuasty.md §7). 'adentro': escalones de la aguada en
# los cuartos (oscuro, penumbra, media luz); 'nucleo': lavado de la llama en el centro del charco;
# 'afuera' y 'lejos': cuánto se mezcla con la tinta lo de fuera; 'sepia': la noche quita el color y
# solo lo guardan la luz y el partido; 'luna': luna de papel y corredor en sombra; 'halo': fuerza de
# la luz que se cuela por las rendijas.
ESTILOS_NOCHE = {
    'escalonada': {'adentro': (0.8, 0.58, 0.32), 'nucleo': 0.35, 'afuera': 0.84, 'lejos': 0.86,
                   'sepia': False, 'luna': False, 'halo': 1.0},
    'tinta': {'adentro': (0.93, 0.74, 0.46), 'nucleo': 0.42, 'afuera': 0.95, 'lejos': 0.95,
              'sepia': False, 'luna': False, 'halo': 1.6},
    'sepia': {'adentro': (0.8, 0.58, 0.32), 'nucleo': 0.4, 'afuera': 0.8, 'lejos': 0.84,
              'sepia': True, 'luna': False, 'halo': 1.2},
    'luna': {'adentro': (0.8, 0.58, 0.32), 'nucleo': 0.35, 'afuera': 0.7, 'lejos': 0.74,
             'sepia': False, 'luna': True, 'halo': 1.0},
}
NOCHE = dict(ESTILOS_NOCHE['escalonada'])


def usar_noche(nombre):
    NOCHE.clear()
    NOCHE.update(ESTILOS_NOCHE[nombre])

# Cuartos en x del nivel (plano de juego). Los muros cortados miden 0,5 m y su módulo se monta
# 10 px sobre cada viñeta para que no quede costura.
ALCOBA, SALA, COCINA = (110, 910), (1010, 2210), (2310, 3110)
ANCHO_NIVEL = 3220


def col(token):
    """Color de la paleta (no del mundo): luz de lámpara, papel, tinta."""
    return pa.PALETA[token]


MUEBLES = 'mobiliario campesino de los años 40: por verificar con fotos'


def marcar(motivo, dibujo):
    """Lo que sigue [P] va en un grupo marcado: se ve en la escena pero no es versión final."""
    return f'<g data-p="{motivo}">{dibujo}</g>'


# ===================================== luz y noche =====================================

def charco(cx, cy, rx, ry, rnd, n=16):
    """Contorno de un charco de luz: elipse a mano, sin punta."""
    p = []
    for k in range(n):
        a = k * 2 * math.pi / n
        j = rnd.uniform(0.86, 1.1)
        p.append((cx + math.cos(a) * rx * j, cy + math.sin(a) * ry * j))
    return canto(p)


def rect_d(x0, y0, x1, y1):
    return f'M{f(x0)},{f(y0)} L{f(x1)},{f(y0)} L{f(x1)},{f(y1)} L{f(x0)},{f(y1)} Z'


def noche(W, fuente=None, derrame=None, tinte='lampara'):
    """Aguada de la noche sobre la viñeta. fuente=(cx, cy, escala): charcos escalonados de luz
    alrededor de una llama; derrame: polígono de media luz que entra por una puerta."""
    rnd = random.Random(int(W) * 7 + (int(fuente[0]) if fuente else 0))
    OSCURO, PENUMBRA, MEDIA = NOCHE['adentro']
    todo = rect_d(0, Y_MARCO, W, Y_BAJO)
    out = [f'<clipPath id="vineta"><path d="{todo}"/></clipPath><g clip-path="url(#vineta)">']
    if fuente:
        cx, cy, e = fuente
        c1 = charco(cx, cy, 170 * e, 135 * e, rnd)
        c2 = charco(cx, cy, 370 * e, 300 * e, rnd)
        c3 = charco(cx, cy, 580 * e, 460 * e, rnd)
        out.append(f'<path d="{todo} {c3}" fill-rule="evenodd" fill="#000" fill-opacity="{OSCURO}"/>')
        out.append(f'<path d="{c3} {c2}" fill-rule="evenodd" fill="#000" fill-opacity="{PENUMBRA}"/>')
        out.append(f'<path d="{c2} {c1}" fill-rule="evenodd" fill="#000" fill-opacity="{MEDIA}"/>')
        out.append(f'<path d="{c1}" fill="{col(tinte)}" fill-opacity="{NOCHE["nucleo"]}"/>')
    elif derrame:
        d = 'M' + ' L'.join(f'{f(x)},{f(y)}' for x, y in derrame) + ' Z'
        out.append(f'<path d="{todo} {d}" fill-rule="evenodd" fill="#000" fill-opacity="{OSCURO}"/>')
        out.append(f'<path d="{d}" fill="#000" fill-opacity="{PENUMBRA}"/>')
    else:
        out.append(f'<path d="{todo}" fill="#000" fill-opacity="{OSCURO}"/>')
    # el envés del tejado queda lejos de la llama y de espaldas a ella: un escalón más oscuro
    out.append(f'<rect x="0" y="{f(Y_MARCO)}" width="{f(W)}" height="{f(Y_SOLERA - Y_MARCO)}" fill="#000" fill-opacity="0.3"/>')
    out.append('</g>')
    return ''.join(out)


def llama(cx, cy, k=1.0):
    """Llama de mecha: ocre, nunca roja (paleta.md §3); se dibuja encima de la noche."""
    h, w = 0.11 * M * k, 0.035 * M * k
    d = f'M{f(cx)},{f(cy - h)} Q{f(cx + w * 1.3)},{f(cy - h * 0.35)} {f(cx)},{f(cy)} Q{f(cx - w * 1.3)},{f(cy - h * 0.35)} {f(cx)},{f(cy - h)} Z'
    nucleo = f'M{f(cx)},{f(cy - h * 0.6)} Q{f(cx + w * 0.6)},{f(cy - h * 0.25)} {f(cx)},{f(cy - h * 0.05)} Q{f(cx - w * 0.6)},{f(cy - h * 0.25)} {f(cx)},{f(cy - h * 0.6)} Z'
    return (f'<path d="{d}" fill="{col("llama")}" stroke="#000" stroke-width="{f(SW * 0.3)}"/>'
            f'<path d="{nucleo}" fill="{col("llama-nucleo")}"/>')


# ================================ la viñeta: tejado, muro, suelo ================================

def envés_tejado(W, rnd, humo=False):
    """Envés del tejado sobre la tapia: cañizo entre varas, la solera encima del muro."""
    cañizo = lav('cebada', M, 0.75) if not humo else lav('tapia', M, 0.8)
    out = [f'<rect x="0" y="{f(Y_MARCO)}" width="{f(W)}" height="{f(Y_SOLERA - Y_MARCO)}" fill="{cañizo}"/>',
           f'<rect x="0" y="{f(Y_MARCO)}" width="{f(W)}" height="{f(Y_SOLERA - Y_MARCO)}" {SOMBRA}/>']
    # pocas cañas sueltas del cañizo: detalle, no textura
    for _ in range(int(W / 160)):
        y = rnd.uniform(Y_MARCO + 30, Y_SOLERA - 40)
        x = rnd.uniform(0, W - 120)
        out.append(f'<path d="M{f(x)},{f(y)} l{f(rnd.uniform(70, 130))},{f(rnd.uniform(-3, 3))}" stroke="#000" stroke-width="{f(SW * 0.3)}"/>')
    # varas (pares) que suben de la solera a la cumbrera
    x = rnd.uniform(40, 90)
    while x < W - 10:
        w = rnd.uniform(16, 22)
        out.append(f'<path d="M{f(x)},{f(Y_SOLERA)} L{f(x + rnd.uniform(-4, 4))},{f(Y_MARCO)} L{f(x + w)},{f(Y_MARCO)} L{f(x + w)},{f(Y_SOLERA)} Z" fill="{lav("madera", M, 0.7)}" stroke="#000" stroke-width="{f(SW * 0.6)}"/>'
                   f'<rect x="{f(x + w * 0.55)}" y="{f(Y_MARCO)}" width="{f(w * 0.45)}" height="{f(Y_SOLERA - Y_MARCO)}" {SOMBRA_FUERTE}/>')
        x += rnd.uniform(118, 140)
    if humo:
        out.append(f'<rect x="0" y="{f(Y_MARCO)}" width="{f(W)}" height="{f(Y_SOLERA - Y_MARCO)}" {SOMBRA_FUERTE}/>')
    # solera: viga sobre la tapia
    out.append(f'<rect x="0" y="{f(Y_SOLERA - 18)}" width="{f(W)}" height="26" fill="{lav("madera", M, 0.6)}" stroke="#000" stroke-width="{f(SW * 0.8)}"/>'
               f'<rect x="0" y="{f(Y_SOLERA - 4)}" width="{f(W)}" height="12" {SOMBRA}/>')
    return ''.join(out)


def muro(W, rnd, grietas=3, desconchados=2):
    """Tapia encalada por dentro (doc 03 §3.1 [V]; encalado interior [P]), con zócalo de tierra."""
    return (muro_cal(0, W, Y_SOLERA + 8, Y_PISO, M, SW, rnd, grietas=grietas, desconchados=desconchados)
            + zocalo(0, W, Y_PISO, 0.45 * M, M, SW, rnd))


def piso(W, rnd):
    """Piso de tierra pisada [P] visto de canto, hasta el borde de la viñeta."""
    out = [f'<rect x="0" y="{f(Y_PISO)}" width="{f(W)}" height="{f(Y_BAJO - Y_PISO)}" fill="{lav("tierra", M, 0.85)}"/>',
           f'<rect x="0" y="{f(Y_PISO)}" width="{f(W)}" height="6" {SOMBRA}/>']
    for _ in range(int(W / 140)):
        x = rnd.uniform(10, W - 60)
        y = rnd.uniform(Y_PISO + 9, Y_BAJO - 5)
        out.append(f'<path d="M{f(x)},{f(y)} l{f(rnd.uniform(20, 50))},{f(rnd.uniform(-1, 1))}" stroke="#000" stroke-width="{f(SW * 0.3)}"/>')
    out.append(f'<line x1="0" y1="{f(Y_PISO)}" x2="{f(W)}" y2="{f(Y_PISO)}" stroke="#000" stroke-width="{f(SW * 0.9)}"/>')
    return marcar('piso de tierra pisada: por verificar', ''.join(out))


def margenes(W, rnd):
    """Papel arriba y abajo de la viñeta (los globos de diálogo van abajo, contrato §1), con el
    borde de tinta. Abajo, unas piedras sueltas dicen que la casa está sobre la tierra."""
    out = [f'<rect x="0" y="0" width="{f(W)}" height="{f(Y_MARCO)}" fill="#fff"/>',
           f'<rect x="0" y="{f(Y_BAJO)}" width="{f(W)}" height="{f(H - Y_BAJO)}" fill="#fff"/>']
    for _ in range(max(1, int(W / 420))):
        x, y = rnd.uniform(30, W - 60), rnd.uniform(Y_BAJO + 26, Y_BAJO + 70)
        r = rnd.uniform(6, 11)
        p = [(x + math.cos(k * math.pi / 4) * r * rnd.uniform(0.8, 1.15), y + math.sin(k * math.pi / 4) * r * 0.62) for k in range(8)]
        out.append(f'<path d="{canto(p)}" fill="none" stroke="#000" stroke-width="{f(SW * 0.35)}" opacity="0.55"/>')
    out.append(f'<line x1="0" y1="{f(Y_MARCO)}" x2="{f(W)}" y2="{f(Y_MARCO)}" stroke="#000" stroke-width="{f(SW * 1.5)}"/>'
               f'<line x1="0" y1="{f(Y_BAJO)}" x2="{f(W)}" y2="{f(Y_BAJO)}" stroke="#000" stroke-width="{f(SW * 1.5)}"/>')
    return ''.join(out)


# ======================================= muebles y objetos =======================================

def madera(luz=0.65):
    return lav('madera', M, luz)


def tabla(x0, y0, x1, y1, luz=0.65, sw=0.7):
    return f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1 - x0)}" height="{f(y1 - y0)}" fill="{madera(luz)}" stroke="#000" stroke-width="{f(SW * sw)}"/>'


def mesa(x0, x1, alto=0.75):
    """Mesa de tablas, de lado: tablero, faldón y dos patas a la vista [P: mobiliario]."""
    yt = Y_PISO - alto * M
    out = [tabla(x0, yt, x1, yt + 0.06 * M, 0.6), tabla(x0 + 8, yt + 0.06 * M, x1 - 8, yt + 0.16 * M, 0.7, 0.6),
           f'<rect x="{f(x0 + 8)}" y="{f(yt + 0.06 * M)}" width="{f(x1 - x0 - 16)}" height="{f(0.1 * M)}" {SOMBRA_SUAVE}/>']
    for xp in (x0 + 14, x1 - 34):
        out.append(tabla(xp, yt + 0.16 * M, xp + 20, Y_PISO, 0.7, 0.6)
                   + f'<rect x="{f(xp + 11)}" y="{f(yt + 0.16 * M)}" width="9" height="{f(Y_PISO - yt - 0.16 * M)}" {SOMBRA}/>')
    # travesaño bajo, cerca del suelo
    out.append(tabla(x0 + 30, Y_PISO - 0.2 * M, x1 - 30, Y_PISO - 0.2 * M + 10, 0.7, 0.5))
    return marcar(MUEBLES, ''.join(out)), yt


def banca(x0, x1, alto=0.45):
    ys = Y_PISO - alto * M
    out = [tabla(x0, ys, x1, ys + 0.07 * M, 0.6)]
    for xx in (x0 + 0.12 * M, x1 - 0.2 * M):
        out.append(tabla(xx, ys + 0.07 * M, xx + 0.08 * M, Y_PISO, 0.7, 0.6)
                   + f'<rect x="{f(xx + 0.04 * M)}" y="{f(ys + 0.07 * M)}" width="{f(0.04 * M)}" height="{f(Y_PISO - ys - 0.07 * M)}" {SOMBRA}/>')
    return marcar(MUEBLES, ''.join(out))


def taburete(x0):
    """Taburete de cuero [P]."""
    ys = Y_PISO - 0.48 * M
    w = 0.42 * M
    out = [f'<path d="M{f(x0)},{f(ys)} Q{f(x0 + w / 2)},{f(ys + 10)} {f(x0 + w)},{f(ys)} L{f(x0 + w)},{f(ys + 14)} Q{f(x0 + w / 2)},{f(ys + 22)} {f(x0)},{f(ys + 14)} Z" fill="{lav("pelaje-castano", M, 0.8)}" stroke="#000" stroke-width="{f(SW * 0.6)}"/>']
    for xx in (x0 + 6, x0 + w - 18):
        out.append(tabla(xx, ys + 14, xx + 12, Y_PISO, 0.7, 0.5))
    out.append(tabla(x0 + 10, Y_PISO - 0.18 * M, x0 + w - 10, Y_PISO - 0.18 * M + 7, 0.7, 0.4))
    return marcar(MUEBLES, ''.join(out))


def radio_valvulas(x0, y_base):
    """Radio de válvulas de mesa, de caja de madera: forma genérica de los años 40 [P: modelo,
    doc 03 §2]. Placa del dial clara, rejilla de tela y dos perillas."""
    w, h = 0.52 * M, 0.34 * M
    y0 = y_base - h
    caja = (f'M{f(x0)},{f(y_base)} L{f(x0)},{f(y0 + 16)} Q{f(x0)},{f(y0)} {f(x0 + 16)},{f(y0)} '
            f'L{f(x0 + w - 16)},{f(y0)} Q{f(x0 + w)},{f(y0)} {f(x0 + w)},{f(y0 + 16)} L{f(x0 + w)},{f(y_base)} Z')
    tela = rect_d(x0 + 12, y0 + 14, x0 + w * 0.56, y_base - 12)
    out = [f'<g data-p="radio de válvulas de época: modelo por verificar (doc 03 §2)">',
           f'<path d="{caja}" fill="{madera(0.55)}" stroke="#000" stroke-width="{f(SW * 0.8)}"/>',
           f'<path d="{tela}" fill="{lav("cebada", M, 0.8)}" stroke="#000" stroke-width="{f(SW * 0.5)}"/>',
           recortar(tela, ''.join(f'<line x1="{f(x0 + 12 + i * 14)}" y1="{f(y0 + 14)}" x2="{f(x0 + 12 + i * 14)}" y2="{f(y_base - 12)}" stroke="#000" stroke-width="{f(SW * 0.25)}"/>' for i in range(1, 4))),
           # placa del dial con su aguja
           f'<path d="M{f(x0 + w * 0.62)},{f(y0 + 52)} A{f(w * 0.16)},{f(w * 0.16)} 0 0 1 {f(x0 + w * 0.94)},{f(y0 + 52)} Z" fill="{col("papel-viejo")}" stroke="#000" stroke-width="{f(SW * 0.5)}"/>',
           f'<line x1="{f(x0 + w * 0.78)}" y1="{f(y0 + 52)}" x2="{f(x0 + w * 0.72)}" y2="{f(y0 + 34)}" stroke="#000" stroke-width="{f(SW * 0.45)}"/>']
    for k in (0.68, 0.88):
        out.append(f'<circle cx="{f(x0 + w * k)}" cy="{f(y_base - 22)}" r="8" fill="{madera(0.4)}" stroke="#000" stroke-width="{f(SW * 0.5)}"/>')
    out.append(recortar(caja, f'<rect x="{f(x0 + w * 0.6)}" y="{f(y0)}" width="{f(w * 0.4)}" height="{f(h)}" {SOMBRA_SUAVE}/>'))
    out.append('</g>')
    return ''.join(out), x0 + w


def lampara_petroleo(cx, y_base):
    """Lámpara de petróleo de tubo de vidrio (doc 03 §2). Devuelve el dibujo y dónde va la llama."""
    out = [f'<path d="M{f(cx - 30)},{f(y_base)} Q{f(cx)},{f(y_base - 8)} {f(cx + 30)},{f(y_base)} Z" fill="{lav("piedra", M, 0.6)}" stroke="#000" stroke-width="{f(SW * 0.6)}"/>',
           # depósito del petróleo
           f'<path d="M{f(cx - 8)},{f(y_base - 4)} L{f(cx - 8)},{f(y_base - 14)} Q{f(cx - 34)},{f(y_base - 30)} {f(cx - 20)},{f(y_base - 52)} '
           f'L{f(cx + 20)},{f(y_base - 52)} Q{f(cx + 34)},{f(y_base - 30)} {f(cx + 8)},{f(y_base - 14)} L{f(cx + 8)},{f(y_base - 4)} Z" fill="{lav("agua", M, 0.7)}" stroke="#000" stroke-width="{f(SW * 0.6)}"/>',
           f'<rect x="{f(cx - 14)}" y="{f(y_base - 62)}" width="28" height="11" fill="{lav("piedra", M, 0.5)}" stroke="#000" stroke-width="{f(SW * 0.5)}"/>']
    # tubo de vidrio con la llama dentro
    tubo = (f'M{f(cx - 11)},{f(y_base - 62)} Q{f(cx - 20)},{f(y_base - 84)} {f(cx - 11)},{f(y_base - 104)} L{f(cx - 7)},{f(y_base - 132)} '
            f'L{f(cx + 7)},{f(y_base - 132)} L{f(cx + 11)},{f(y_base - 104)} Q{f(cx + 20)},{f(y_base - 84)} {f(cx + 11)},{f(y_base - 62)} Z')
    vidrio = f'<path d="{tubo}" fill="{col("lampara")}" fill-opacity="0.85" stroke="#000" stroke-width="{f(SW * 0.5)}"/>'
    return ''.join(out), vidrio + llama(cx, y_base - 70, 0.9), (cx, y_base - 84)


def repisa(x0, x1, y):
    out = [tabla(x0, y, x1, y + 12, 0.6, 0.6)]
    for xx in (x0 + 20, x1 - 34):
        out.append(f'<path d="M{f(xx)},{f(y + 12)} L{f(xx + 14)},{f(y + 12)} L{f(xx + 14)},{f(y + 40)} Z" fill="{madera(0.7)}" stroke="#000" stroke-width="{f(SW * 0.5)}"/>')
    return marcar(MUEBLES, ''.join(out))


def libreta(x0, y_base):
    """Libreta escolar de Rosalba (doc 02 §3: sabe leer gracias a Custodia), con su lápiz."""
    w, h = 0.2 * M, 0.05 * M
    return (f'<rect x="{f(x0)}" y="{f(y_base - h)}" width="{f(w)}" height="{f(h)}" fill="{col("papel-viejo")}" stroke="#000" stroke-width="{f(SW * 0.5)}"/>'
            f'<line x1="{f(x0 + 3)}" y1="{f(y_base - h * 0.5)}" x2="{f(x0 + w - 3)}" y2="{f(y_base - h * 0.5)}" stroke="#000" stroke-width="{f(SW * 0.3)}"/>'
            f'<path d="M{f(x0 + w * 0.2)},{f(y_base - h - 3)} L{f(x0 + w * 0.95)},{f(y_base - h - 6)}" stroke="{lav("cinta-amarilla", M)}" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M{f(x0 + w * 0.2)},{f(y_base - h - 3)} L{f(x0 + w * 0.95)},{f(y_base - h - 6)}" stroke="#000" stroke-width="{f(SW * 0.2)}" fill="none"/>')


def botella(x, y_base, h=0.24):
    hh = h * M
    d = (f'M{f(x)},{f(y_base)} L{f(x)},{f(y_base - hh * 0.6)} Q{f(x)},{f(y_base - hh * 0.72)} {f(x + 6)},{f(y_base - hh * 0.78)} '
         f'L{f(x + 6)},{f(y_base - hh)} L{f(x + 14)},{f(y_base - hh)} L{f(x + 14)},{f(y_base - hh * 0.78)} '
         f'Q{f(x + 20)},{f(y_base - hh * 0.72)} {f(x + 20)},{f(y_base - hh * 0.6)} L{f(x + 20)},{f(y_base)} Z')
    return (f'<path d="{d}" fill="{lav("sementera", M, 0.6)}" stroke="#000" stroke-width="{f(SW * 0.5)}"/>'
            + recortar(d, f'<rect x="{f(x + 11)}" y="{f(y_base - hh)}" width="10" height="{f(hh)}" {SOMBRA}/>'))


def estaca(x, y):
    return f'<path d="M{f(x)},{f(y)} l16,-5 l3,7 l-17,4 Z" fill="{madera(0.5)}" stroke="#000" stroke-width="{f(SW * 0.5)}"/>'


def sombrero_colgado(x, y, tipo='negro'):
    """Sombrero de los vecinos colgado de una estaca, junto a la puerta: hay visita."""
    fill = '#000' if tipo == 'negro' else lav('paja', M)
    ala, copa = 0.24 * M, 0.11 * M
    out = [estaca(x - 6, y),
           f'<path d="M{f(x - ala)},{f(y + 30)} Q{f(x)},{f(y + 40)} {f(x + ala)},{f(y + 30)} Q{f(x)},{f(y + 24)} {f(x - ala)},{f(y + 30)} Z" fill="{fill}" stroke="#000" stroke-width="{f(SW * 0.5)}"/>',
           f'<path d="M{f(x - copa)},{f(y + 30)} Q{f(x - copa)},{f(y + 4)} {f(x)},{f(y + 2)} Q{f(x + copa)},{f(y + 4)} {f(x + copa)},{f(y + 30)} Z" fill="{fill}" stroke="#000" stroke-width="{f(SW * 0.5)}"/>']
    if tipo == 'negro':
        out.append(f'<path d="M{f(x - copa)},{f(y + 24)} Q{f(x)},{f(y + 27)} {f(x + copa)},{f(y + 24)}" stroke="#fff" stroke-width="{f(SW * 0.4)}" fill="none"/>')
    else:
        out.append(f'<path d="M{f(x - copa)},{f(y + 23)} Q{f(x)},{f(y + 26)} {f(x + copa)},{f(y + 23)} L{f(x + copa)},{f(y + 28)} Q{f(x)},{f(y + 31)} {f(x - copa)},{f(y + 28)} Z" fill="#000"/>')
    return ''.join(out)


def ruana_colgada(x, y, token='lana-gris'):
    w, h = 0.5 * M, 0.85 * M
    d = (f'M{f(x - 6)},{f(y + 6)} Q{f(x - w * 0.5)},{f(y + 20)} {f(x - w * 0.55)},{f(y + h)} '
         f'L{f(x + w * 0.45)},{f(y + h + 6)} Q{f(x + w * 0.5)},{f(y + 24)} {f(x + 6)},{f(y + 6)} Z')
    pliegues = (f'<path d="M{f(x - 4)},{f(y + 20)} Q{f(x - w * 0.18)},{f(y + h * 0.6)} {f(x - w * 0.2)},{f(y + h)} '
                f'M{f(x + 6)},{f(y + 24)} Q{f(x + w * 0.16)},{f(y + h * 0.6)} {f(x + w * 0.2)},{f(y + h + 4)}" stroke="#000" stroke-width="{f(SW * 0.4)}" fill="none"/>'
                f'<path d="M{f(x + w * 0.1)},{f(y)} L{f(x + w * 0.6)},{f(y)} L{f(x + w * 0.6)},{f(y + h + 10)} L{f(x + w * 0.12)},{f(y + h + 10)} Z" {SOMBRA_SUAVE}/>'
                f'<path d="M{f(x - w * 0.6)},{f(y + h - 14)} L{f(x + w * 0.6)},{f(y + h - 8)}" stroke="#000" stroke-width="{f(SW * 0.35)}"/>')
    return estaca(x - 6, y) + f'<path d="{d}" fill="{lav(token, M)}"/>' + recortar(d, pliegues) + f'<path d="{d}" fill="none" stroke="#000" stroke-width="{f(SW * 0.6)}"/>'


def escopeta(x0, y):
    """Escopeta del padre en dos estacas: silueta genérica de un cañón [P: modelo, doc 03 §2 y
    hoja de Rosalba]. Se dibuja como marcador hasta resolver el modelo."""
    largo = 1.15 * M
    culata = (f'M{f(x0)},{f(y + 4)} L{f(x0 + 0.34 * M)},{f(y - 2)} L{f(x0 + 0.42 * M)},{f(y + 2)} L{f(x0 + 0.42 * M)},{f(y + 10)} '
              f'L{f(x0 + 0.3 * M)},{f(y + 12)} Q{f(x0 + 0.12 * M)},{f(y + 26)} {f(x0 + 2)},{f(y + 30)} Z')
    return (f'<g data-p="escopeta del padre: modelo por verificar (doc 03 §2); silueta de marcador">'
            + estaca(x0 + 0.3 * M, y + 8) + estaca(x0 + 0.95 * M, y + 4)
            + f'<path d="{culata}" fill="{madera(0.5)}" stroke="#000" stroke-width="{f(SW * 0.6)}"/>'
            + f'<rect x="{f(x0 + 0.42 * M)}" y="{f(y - 1)}" width="{f(largo - 0.42 * M)}" height="7" fill="#000"/>'
            + f'<rect x="{f(x0 + 0.42 * M)}" y="{f(y + 6)}" width="{f(0.36 * M)}" height="6" fill="{madera(0.5)}" stroke="#000" stroke-width="{f(SW * 0.4)}"/>'
            + '</g>')


def ventana_cerrada(x0, w, y0, h):
    """Ventana vista desde dentro con los postigos cerrados y su aldaba (reunión a puerta cerrada)."""
    out = [f'<rect x="{f(x0 - 10)}" y="{f(y0 - 10)}" width="{f(w + 20)}" height="{f(h + 20)}" fill="{lav("cal", M, 0.85)}" stroke="#000" stroke-width="{f(SW * 0.6)}"/>',
           f'<rect x="{f(x0 - 10)}" y="{f(y0 - 10)}" width="{f(w + 20)}" height="{f(h + 20)}" {SOMBRA_SUAVE}/>',
           puerta_tablas(x0, y0, w, h, M, SW * 0.8, random.Random(3), hojas=2),
           f'<rect x="{f(x0 + w / 2 - 14)}" y="{f(y0 + h * 0.48)}" width="28" height="7" fill="#000"/>',
           tabla(x0 - 16, y0 + h + 10, x0 + w + 16, y0 + h + 22, 0.6, 0.6)]
    return ''.join(out)


def puerta_trancada(x0, w, h):
    """Puerta de la casa vista desde dentro, con la tranca puesta en sus dos ganchos."""
    y0 = Y_PISO - h
    out = [tabla(x0 - 14, y0 - 16, x0 + w + 14, y0, 0.55, 0.7),
           puerta_tablas(x0, y0, w, h, M, SW, random.Random(5)),
           f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" {SOMBRA_SUAVE}/>']
    ty = y0 + h * 0.5
    for gx in (x0 - 8, x0 + w - 6):
        out.append(f'<path d="M{f(gx)},{f(ty - 4)} l14,0 l0,22 l-14,0" fill="none" stroke="#000" stroke-width="{f(SW * 0.9)}"/>')
    out.append(tabla(x0 - 22, ty, x0 + w + 22, ty + 16, 0.6, 0.7))
    out.append(f'<rect x="{f(x0 - 22)}" y="{f(ty + 10)}" width="{f(w + 44)}" height="6" {SOMBRA}/>')
    # umbral
    out.append(f'<rect x="{f(x0 - 6)}" y="{f(Y_PISO - 8)}" width="{f(w + 12)}" height="8" fill="{lav("piedra", M)}" stroke="#000" stroke-width="{f(SW * 0.5)}"/>')
    return ''.join(out)


def cama(x0, x1):
    """Cama de tablas con cobijas de lana y almohada [P: mobiliario]; debajo, oscuro (escondite)."""
    y_tabla = Y_PISO - 0.42 * M
    out = [f'<rect x="{f(x0 + 10)}" y="{f(y_tabla)}" width="{f(x1 - x0 - 20)}" height="{f(Y_PISO - y_tabla)}" fill="#000" fill-opacity="0.55"/>']
    # cabecera (izquierda) y pie (derecha)
    out.append(tabla(x0, Y_PISO - 1.0 * M, x0 + 0.1 * M, Y_PISO, 0.55, 0.8))
    out.append(tabla(x1 - 0.1 * M, Y_PISO - 0.7 * M, x1, Y_PISO, 0.55, 0.8))
    out.append(tabla(x0 + 0.1 * M, Y_PISO - 0.9 * M, x0 + 0.14 * M, Y_PISO - 0.55 * M, 0.6, 0.4))
    # larguero
    out.append(tabla(x0 + 0.1 * M, y_tabla, x1 - 0.1 * M, y_tabla + 0.12 * M, 0.6, 0.7))
    # colchón y cobijas que cuelgan por el lado
    yc = y_tabla - 0.14 * M
    cobija = (f'M{f(x0 + 0.1 * M)},{f(yc)} Q{f((x0 + x1) / 2)},{f(yc - 10)} {f(x1 - 0.1 * M)},{f(yc + 2)} '
              f'L{f(x1 - 0.12 * M)},{f(y_tabla + 0.22 * M)} Q{f((x0 + x1) / 2 + 40)},{f(y_tabla + 0.28 * M)} {f(x0 + 0.5 * M)},{f(y_tabla + 0.2 * M)} '
              f'L{f(x0 + 0.1 * M)},{f(y_tabla + 0.1 * M)} Z')
    out.append(f'<path d="{cobija}" fill="{lav("lana-cruda", M)}"/>')
    out.append(recortar(cobija, f'<path d="M{f(x0 + 0.1 * M)},{f(yc + 30)} L{f(x1)},{f(yc + 36)}" stroke="{lav("lana-parda", M)}" stroke-width="12"/>'
                                f'<path d="M{f(x0 + 0.1 * M)},{f(yc + 52)} L{f(x1)},{f(yc + 58)}" stroke="{lav("lana-parda", M)}" stroke-width="5"/>'
                                f'<path d="M{f(x0 + 0.9 * M)},{f(yc + 6)} Q{f(x0 + 0.95 * M)},{f(y_tabla + 0.1 * M)} {f(x0 + 0.85 * M)},{f(y_tabla + 0.25 * M)}" stroke="#000" stroke-width="{f(SW * 0.4)}" fill="none"/>'
                                f'<rect x="{f(x0)}" y="{f(y_tabla + 0.04 * M)}" width="{f(x1 - x0)}" height="{f(0.3 * M)}" {SOMBRA}/>'))
    out.append(f'<path d="{cobija}" fill="none" stroke="#000" stroke-width="{f(SW * 0.7)}"/>')
    # almohada
    out.append(f'<path d="M{f(x0 + 0.14 * M)},{f(yc)} Q{f(x0 + 0.16 * M)},{f(yc - 0.16 * M)} {f(x0 + 0.42 * M)},{f(yc - 0.14 * M)} Q{f(x0 + 0.58 * M)},{f(yc - 0.12 * M)} {f(x0 + 0.56 * M)},{f(yc)} Z" fill="{lav("blanco-tela", M)}" stroke="#000" stroke-width="{f(SW * 0.6)}"/>')
    return marcar(MUEBLES, ''.join(out))


def baul(x0, w, h):
    """Baúl de madera con herrajes [P]: donde se guarda lo de valor (y se esconde)."""
    y0 = Y_PISO - h
    tapa = f'M{f(x0)},{f(y0 + 16)} Q{f(x0 + w / 2)},{f(y0 - 8)} {f(x0 + w)},{f(y0 + 16)} Z'
    out = [tabla(x0, y0 + 16, x0 + w, Y_PISO, 0.5, 0.8),
           f'<path d="{tapa}" fill="{madera(0.45)}" stroke="#000" stroke-width="{f(SW * 0.8)}"/>',
           f'<rect x="{f(x0 + w * 0.62)}" y="{f(y0 + 16)}" width="{f(w * 0.38)}" height="{f(h - 16)}" {SOMBRA}/>']
    for k in (0.12, 0.88):
        out.append(f'<rect x="{f(x0 + w * k - 6)}" y="{f(y0 + 8)}" width="12" height="{f(h - 8)}" fill="#000"/>')
    out.append(f'<rect x="{f(x0 + w / 2 - 9)}" y="{f(y0 + 22)}" width="18" height="22" fill="{lav("piedra", M, 0.6)}" stroke="#000" stroke-width="{f(SW * 0.5)}"/>')
    return marcar(MUEBLES, ''.join(out))


def ropa_en_cuerda(x0, x1, y, rnd):
    """Cuerda con la ropa de las mujeres de la casa: pañolón, falda de añil y blusa (Ocampo López, 1977)."""
    out = [f'<path d="M{f(x0)},{f(y)} Q{f((x0 + x1) / 2)},{f(y + 26)} {f(x1)},{f(y)}" stroke="#000" stroke-width="{f(SW * 0.5)}" fill="none"/>',
           estaca(x0 - 14, y - 4), estaca(x1 - 4, y - 4)]
    piezas = [('negro-anil', 0.55, 0.7), ('blanco-tela', 0.42, 0.45), ('tinta-plena', 0.7, 0.62)]
    x = x0 + 40
    for token, w_m, h_m in piezas:
        w, h = w_m * M, h_m * M
        t = (x + w / 2 - x0) / (x1 - x0)
        yy = y + 26 * 4 * t * (1 - t) * 0.5 + 2
        d = (f'M{f(x)},{f(yy)} L{f(x + w)},{f(yy + 2)} L{f(x + w * 1.04)},{f(yy + h)} '
             f'Q{f(x + w / 2)},{f(yy + h + 8)} {f(x - w * 0.04)},{f(yy + h - 4)} Z')
        fill = col('tinta-plena') if token == 'tinta-plena' else lav(token, M)
        out.append(f'<path d="{d}" fill="{fill}"/>')
        out.append(recortar(d, f'<path d="M{f(x + w * 0.3)},{f(yy + 6)} L{f(x + w * 0.26)},{f(yy + h)} M{f(x + w * 0.66)},{f(yy + 6)} L{f(x + w * 0.72)},{f(yy + h)}" stroke="{"#fff" if token == "tinta-plena" else "#000"}" stroke-width="{f(SW * 0.35)}" fill="none" opacity="0.7"/>'))
        out.append(f'<path d="{d}" fill="none" stroke="#000" stroke-width="{f(SW * 0.6)}"/>')
        x += w + rnd.uniform(18, 34)
    return ''.join(out)


def fogon(x0, x1, rnd):
    """Fogón de leña sobre poyo de barro con su boca de brasas [P: forma del fogón, doc 03 §3.1]."""
    alto = 0.62 * M
    y0 = Y_PISO - alto
    poyo = f'M{f(x0)},{f(Y_PISO)} L{f(x0 + 6)},{f(y0 + 8)} Q{f(x0 + 8)},{f(y0)} {f(x0 + 20)},{f(y0)} L{f(x1 - 20)},{f(y0)} Q{f(x1 - 8)},{f(y0)} {f(x1 - 6)},{f(y0 + 8)} L{f(x1)},{f(Y_PISO)} Z'
    boca = f'M{f(x0 + 70)},{f(Y_PISO)} L{f(x0 + 70)},{f(Y_PISO - 0.22 * M)} Q{f(x0 + 110)},{f(Y_PISO - 0.36 * M)} {f(x0 + 150)},{f(Y_PISO - 0.22 * M)} L{f(x0 + 150)},{f(Y_PISO)} Z'
    out = [f'<g data-p="fogón de leña: forma por verificar (poyo de barro o tulpas)">',
           f'<path d="{poyo}" fill="{lav("tapia", M)}" stroke="#000" stroke-width="{f(SW * 0.9)}"/>',
           recortar(poyo, f'<rect x="{f(x1 - 70)}" y="{f(y0)}" width="80" height="{f(alto)}" {SOMBRA_SUAVE}/>'
                          f'<path d="M{f(x0 + 190)},{f(y0 + 30)} l8,22 l-4,16" stroke="#000" stroke-width="{f(SW * 0.35)}" fill="none"/>'),
           # hollín sobre la boca
           recortar(poyo, f'<path d="M{f(x0 + 60)},{f(y0)} Q{f(x0 + 110)},{f(y0 + 40)} {f(x0 + 160)},{f(y0)} Z" fill="#000" fill-opacity="0.5"/>'),
           f'<path d="{boca}" fill="#000"/>', '</g>']
    return ''.join(out), boca, (x0 + 110, Y_PISO - 0.12 * M), y0


def brasas(boca_x0, boca_x1, rnd):
    """Brasas y lenguas de fuego en la boca del fogón: ocre y amarillo, nunca rojo (paleta.md §3)."""
    out = []
    for i in range(5):
        bx = boca_x0 + 12 + i * (boca_x1 - boca_x0 - 24) / 4
        out.append(f'<ellipse cx="{f(bx)}" cy="{f(Y_PISO - 8)}" rx="11" ry="6" fill="{col("brasa")}" stroke="#000" stroke-width="{f(SW * 0.3)}"/>')
    for i in range(3):
        bx = boca_x0 + 24 + i * (boca_x1 - boca_x0 - 48) / 2
        out.append(llama(bx, Y_PISO - 12, 1.1 + 0.2 * (i == 1)))
    return ''.join(out)


def zarzo(x0, x1, y, rnd):
    """Zarzo sobre el fogón: tablado de varas donde el humo cura el maíz [P]."""
    out = [f'<g data-p="zarzo de varas sobre el fogón: por verificar">']
    # carga encima: mazorcas, un atado de leña y un costal
    for i in range(14):
        mx = x0 + 30 + i * (x1 - x0 - 200) / 14 + rnd.uniform(-4, 4)
        my = y - 12 - (i % 3) * 9
        out.append(f'<ellipse cx="{f(mx)}" cy="{f(my)}" rx="{f(0.1 * M)}" ry="{f(0.045 * M)}" transform="rotate({f(rnd.uniform(-12, 12))} {f(mx)} {f(my)})" fill="{lav("trigo", M, 0.85)}" stroke="#000" stroke-width="{f(SW * 0.4)}"/>')
    out.append(costal(x1 - 170, y, 0.55 * M, 0.42 * M, M, SW, rnd))
    # el tablado visto de canto: varas y una viga
    out.append(tabla(x0, y, x1, y + 14, 0.55, 0.7))
    for i in range(int((x1 - x0) / 34)):
        vx = x0 + 10 + i * 34
        out.append(f'<circle cx="{f(vx)}" cy="{f(y + 22)}" r="8" fill="{madera(0.6)}" stroke="#000" stroke-width="{f(SW * 0.4)}"/>')
    out.append(tabla(x1 - 18, y + 14, x1, Y_PISO, 0.6, 0.7))
    out.append(f'<rect x="{f(x1 - 9)}" y="{f(y + 14)}" width="9" height="{f(Y_PISO - y - 14)}" {SOMBRA}/>')
    out.append('</g>')
    return ''.join(out)


def escalera(xb, xt, yt):
    """Escalera de palo recostada contra el zarzo."""
    out = []
    for dx in (0, 46):
        out.append(f'<path d="M{f(xb + dx)},{f(Y_PISO)} L{f(xt + dx)},{f(yt)}" stroke="#000" stroke-width="{f(SW * 3.4)}" stroke-linecap="round"/>'
                   f'<path d="M{f(xb + dx)},{f(Y_PISO)} L{f(xt + dx)},{f(yt)}" stroke="{madera(0.7)}" stroke-width="{f(SW * 2.2)}" stroke-linecap="round"/>')
    n = 7
    for i in range(1, n):
        t = i / n
        x = xb + (xt - xb) * t
        y = Y_PISO + (yt - Y_PISO) * t
        out.append(f'<path d="M{f(x - 2)},{f(y)} L{f(x + 48)},{f(y)}" stroke="#000" stroke-width="{f(SW * 2.6)}" stroke-linecap="round"/>'
                   f'<path d="M{f(x - 2)},{f(y)} L{f(x + 48)},{f(y)}" stroke="{madera(0.7)}" stroke-width="{f(SW * 1.4)}" stroke-linecap="round"/>')
    return ''.join(out)


def mazorcas_colgadas(x, y_viga, rnd, n=5):
    """Racimo de mazorcas colgado por las hojas de una vara."""
    out = [f'<path d="M{f(x)},{f(y_viga)} L{f(x)},{f(y_viga + 30)}" stroke="#000" stroke-width="{f(SW * 0.6)}"/>']
    for i in range(n):
        a = -40 + i * 80 / (n - 1) + rnd.uniform(-6, 6)
        cx = x + math.sin(math.radians(a)) * 40
        cy = y_viga + 30 + math.cos(math.radians(a)) * 40
        out.append(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="9" ry="22" transform="rotate({f(-a)} {f(cx)} {f(cy)})" fill="{lav("trigo", M, 0.85)}" stroke="#000" stroke-width="{f(SW * 0.45)}"/>')
    return ''.join(out)


def leña_apilada(x0, x1, rnd, y_suelo=Y_PISO, filas=4):
    """Leña apilada de canto: troncos que se ven por la punta."""
    out = []
    for fila in range(filas):
        y = y_suelo - 14 - fila * 24
        x = x0 + (fila % 2) * 12
        while x < x1 - 20 - fila * 6:
            r = rnd.uniform(10, 13)
            out.append(f'<circle cx="{f(x + r)}" cy="{f(y)}" r="{f(r)}" fill="{lav("madera", M, 0.8)}" stroke="#000" stroke-width="{f(SW * 0.5)}"/>'
                       f'<circle cx="{f(x + r)}" cy="{f(y)}" r="{f(r * 0.4)}" fill="none" stroke="#000" stroke-width="{f(SW * 0.25)}"/>')
            x += 2 * r + 2
    return ''.join(out)


def humo(x, y0, y1, rnd):
    """Hilo de humo del fogón hacia el zarzo: humo claro, apenas."""
    d, y, xx = f'M{f(x)},{f(y0)}', y0, x
    while y > y1:
        y -= 40
        xx += rnd.uniform(-22, 22)
        d += f' Q{f(xx + rnd.uniform(-20, 20))},{f(y + 20)} {f(xx)},{f(y)}'
    return f'<path d="{d}" stroke="{col("humo-claro")}" stroke-width="10" stroke-opacity="0.35" fill="none" stroke-linecap="round"/>'


# =========================================== cuartos ===========================================

def vineta(nombre, W, titulo, fondo, luz_y_brillos, notas=''):
    """Una viñeta: lo de la escena, la noche encima, lo que brilla y los márgenes de papel."""
    rnd = random.Random(sum(map(ord, nombre)))
    fondo_dibujo = fondo(rnd)
    if NOCHE['sepia']:
        # la noche quita el color: el cuarto pasa a sepia y solo la llama lo conserva
        fondo_dibujo = de_noche(W, H, fondo_dibujo, a=0, id_='sepia')
    noche_, brillos = luz_y_brillos
    cuerpo = '\n'.join([fondo_dibujo, noche_, brillos, margenes(W, rnd)])
    archivo(nombre, W, H, 'juego', titulo, cuerpo,
            notas=f'Viñeta del interior en corte: se coloca arriba (y=0) en x={notas}')


def sala():
    W = SALA[1] - SALA[0]
    lamp_x, mesa_x0, mesa_x1 = 1000, 800, 1090

    def fondo(rnd):
        out = [envés_tejado(W, rnd), muro(W, rnd, grietas=4, desconchados=3), piso(W, rnd)]
        out.append(sombrero_colgado(46, 520, 'negro') + sombrero_colgado(96, 506, 'paja') + ruana_colgada(60, 600))
        out.append(puerta_trancada(170, 0.95 * M, 2.05 * M))
        out.append(escopeta(470, 432))
        out.append(ventana_cerrada(500, 1.05 * M, Y_PISO - 1.95 * M, 1.0 * M))
        out.append(banca(430, 760))
        m_, yt = mesa(mesa_x0, mesa_x1)
        # sombra del radio en la tapia, más grande y corrida a la izquierda: la lámpara está a su derecha
        out.append(f'<path d="M{f(mesa_x0 + 24)},{f(yt)} L{f(mesa_x0 - 96)},{f(yt + 6)} L{f(mesa_x0 - 104)},{f(yt - 0.36 * M)} '
                   f'Q{f(mesa_x0 - 100)},{f(yt - 0.44 * M)} {f(mesa_x0 - 84)},{f(yt - 0.44 * M)} L{f(mesa_x0 + 24)},{f(yt - 0.4 * M)} Z" {SOMBRA_HONDA}/>')
        out.append(repisa(1070, 1186, 540))
        out.append(botella(1086, 540) + botella(1116, 540, 0.18) + f'<rect x="1144" y="514" width="30" height="26" fill="{madera(0.5)}" stroke="#000" stroke-width="{f(SW * 0.5)}"/>')
        out.append(m_)
        # bajo el tablero no llega la luz
        out.append(f'<rect x="{mesa_x0 + 8}" y="{f(yt + 0.16 * M)}" width="{mesa_x1 - mesa_x0 - 16}" height="{f(Y_PISO - yt - 0.16 * M)}" {SOMBRA_HONDA}/>')
        r_, _ = radio_valvulas(mesa_x0 + 20, yt)
        out.append(r_)
        out.append(libreta(1034, yt))
        base_lampara, _, _ = lampara_petroleo(lamp_x, yt)
        out.append(base_lampara)
        out.append(taburete(1110))
        return '\n'.join(out)

    _, yt = mesa(mesa_x0, mesa_x1)
    _, brillo, (fx, fy) = lampara_petroleo(lamp_x, yt)
    vineta('sala', W, 'sala: la reunión para oír la radio (Prólogo b4)', fondo,
           (noche(W, (fx, fy, 1.0)), brillo),
           notas=f'{SALA[0]}. Lámpara en x local {lamp_x}; puerta trancada en 170–360; radio [P] y escopeta [P].')


def alcoba():
    W = ALCOBA[1] - ALCOBA[0]

    def fondo(rnd):
        out = [envés_tejado(W, rnd), muro(W, rnd, grietas=2, desconchados=2), piso(W, rnd)]
        out.append(ventana_cerrada(560, 0.55 * M, Y_PISO - 2.2 * M, 0.5 * M))
        out.append(ropa_en_cuerda(60, 470, 470, rnd))
        out.append(cama(40, 480))
        out.append(baul(530, 1.0 * M, 0.58 * M))
        return '\n'.join(out)

    # media luz que entra de la sala por la puerta (a la derecha)
    derrame = [(W, Y_DINTEL + 30), (W - 200, Y_DINTEL + 120), (W - 330, Y_BAJO), (W, Y_BAJO)]
    vineta('alcoba', W, 'alcoba: cama, baúl y la ropa de las mujeres', fondo, (noche(W, derrame=derrame), ''),
           notas=f'{ALCOBA[0]}. Oscura: debajo de la cama y el baúl, escondites.')


def cocina():
    W = COCINA[1] - COCINA[0]
    fogon_x0, fogon_x1 = 110, 420
    rnd0 = random.Random(77)
    _, boca, (fx, fy), _ = fogon(fogon_x0, fogon_x1, rnd0)

    def fondo(rnd):
        out = [envés_tejado(W, rnd, humo=True), muro(W, rnd, grietas=2, desconchados=1), piso(W, rnd)]
        # hollín del humo sobre el fogón, hasta el zarzo: mancha de borde a mano
        hollin = [(fogon_x0 - 10, Y_PISO - 0.6 * M), (fogon_x0 + 10, Y_PISO - 1.3 * M), (fogon_x0 - 6, Y_PISO - 1.9 * M),
                  (fogon_x0 + 30, Y_SOLERA + 30), (fogon_x0 + 120, Y_SOLERA + 6), (fogon_x1 - 40, Y_SOLERA + 20),
                  (fogon_x1 + 30, Y_SOLERA + 40), (fogon_x1 + 10, Y_PISO - 1.7 * M), (fogon_x1 + 28, Y_PISO - 1.1 * M),
                  (fogon_x1 + 14, Y_PISO - 0.6 * M), ((fogon_x0 + fogon_x1) / 2, Y_PISO - 0.66 * M)]
        out.append(f'<path d="{canto(hollin)}" fill="#000" fill-opacity="0.3"/>')
        out.append(puerta_tablas(610, Y_PISO - 2.0 * M, 0.9 * M, 2.0 * M, M, SW, rnd))
        out.append(tabla(596, Y_PISO - 2.0 * M - 14, 610 + 0.9 * M + 14, Y_PISO - 2.0 * M, 0.55, 0.7))
        out.append(repisa(496, 594, 590) + olla(500, 590, 0.24 * M, 0.22 * M, M, SW, rnd) + olla(552, 590, 0.18 * M, 0.26 * M, M, SW, rnd, 'mucura'))
        out.append(mazorcas_colgadas(560, Y_SOLERA + 8, rnd) + mazorcas_colgadas(700, Y_SOLERA + 8, rnd, 4))
        out.append(leña_apilada(14, 104, rnd))
        f_, _, _, y0 = fogon(fogon_x0, fogon_x1, rnd0)
        out.append(f_)
        out.append(olla(fogon_x0 + 140, y0, 0.55 * M, 0.42 * M, M, SW, rnd) + olla(fogon_x0 + 30, y0, 0.32 * M, 0.26 * M, M, SW, rnd))
        out.append(humo(fogon_x0 + 195, y0 - 0.42 * M, Y_SOLERA + 150, rnd))
        out.append(zarzo(0, 470, Y_SOLERA + 100, rnd))
        out.append(escalera(470, 430, Y_SOLERA + 100))
        out.append(costal(500, Y_PISO, 0.45 * M, 0.5 * M, M, SW, rnd, abierto=True))
        return '\n'.join(out)

    brillo = brasas(fogon_x0 + 70, fogon_x0 + 150, rnd0)
    vineta('cocina', W, 'cocina de humo: fogón, zarzo y la puerta del solar', fondo,
           (noche(W, (fx, fy, 0.62), tinte='llama'), brillo),
           notas=f'{COCINA[0]}. Fogón en x local {fogon_x0}–{fogon_x1}; puerta al solar (huida de la M2) en 610–790.')


def muro_cortado(nombre, puerta=None):
    """Muro de tapia cortado (0,5 m): papel del canal entre viñetas, con el borde de tinta. Si tiene
    puerta, se ve su hueco: el telar de la tapia en sombra, el dintel y el umbral."""
    W = 120
    x0, x1 = 10, 110
    _, PENUMBRA, MEDIA = NOCHE['adentro']
    out = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>']
    if puerta:
        hueco = rect_d(x0, Y_DINTEL, x1, Y_PISO)
        out.append(f'<path d="{hueco}" fill="{lav("cal", M, 0.85)}"/>')
        out.append(f'<path d="{hueco}" fill="#000" fill-opacity="{PENUMBRA if puerta == "cortina" else MEDIA}"/>')
        out.append(f'<rect x="{x0}" y="{f(Y_PISO)}" width="{x1 - x0}" height="{f(Y_BAJO - Y_PISO)}" fill="{lav("tierra", M, 0.85)}"/>'
                   f'<rect x="{x0}" y="{f(Y_PISO)}" width="{x1 - x0}" height="{f(Y_BAJO - Y_PISO)}" fill="#000" fill-opacity="{PENUMBRA}"/>')
        out.append(tabla(x0 - 4, Y_DINTEL - 20, x1 + 4, Y_DINTEL, 0.55, 0.8))
        for xx in (x0, x1 - 12):
            out.append(tabla(xx, Y_DINTEL, xx + 12, Y_PISO, 0.6, 0.6))
        if puerta == 'cortina':
            # cortina de lienzo recogida hacia la alcoba
            d = (f'M{f(x0 + 12)},{f(Y_DINTEL)} L{f(x0 + 70)},{f(Y_DINTEL)} Q{f(x0 + 46)},{f(Y_DINTEL + 150)} {f(x0 + 30)},{f(Y_PISO - 150)} '
                 f'Q{f(x0 + 42)},{f(Y_PISO - 60)} {f(x0 + 26)},{f(Y_PISO - 6)} L{f(x0 + 12)},{f(Y_PISO - 6)} Z')
            out.append(f'<path d="{d}" fill="{lav("lana-cruda", M)}"/>'
                       + recortar(d, f'<path d="M{f(x0 + 24)},{f(Y_DINTEL)} Q{f(x0 + 30)},{f(Y_DINTEL + 200)} {f(x0 + 18)},{f(Y_PISO)}" stroke="#000" stroke-width="{f(SW * 0.4)}" fill="none"/>'
                                     f'<rect x="{f(x0)}" y="{f(Y_DINTEL)}" width="80" height="{f(Y_PISO - Y_DINTEL)}" fill="#000" fill-opacity="{PENUMBRA}"/>')
                       + f'<path d="{d}" fill="none" stroke="#000" stroke-width="{f(SW * 0.6)}"/>')
            out.append(f'<line x1="{x0}" y1="{f(Y_DINTEL + 6)}" x2="{x1}" y2="{f(Y_DINTEL + 6)}" stroke="#000" stroke-width="{f(SW * 0.9)}"/>')
    borde = []
    for x in (x0, x1):
        if puerta:
            borde.append(f'M{x},{Y_MARCO} L{x},{f(Y_DINTEL - 20)} M{x},{f(Y_PISO)} L{x},{Y_BAJO}')
        else:
            borde.append(f'M{x},{Y_MARCO} L{x},{Y_BAJO}')
    out.append(f'<path d="{" ".join(borde)}" stroke="#000" stroke-width="{f(SW * 1.5)}" fill="none"/>')
    if puerta:
        out.append(f'<path d="M{x0},{f(Y_DINTEL - 20)} L{x1},{f(Y_DINTEL - 20)}" stroke="#000" stroke-width="{f(SW * 1.5)}"/>')
    # unas juntas de los cajones del tapial en el corte
    rnd = random.Random(sum(map(ord, nombre)))
    for _ in range(5):
        y = rnd.uniform(Y_MARCO + 40, (Y_DINTEL - 40) if puerta else (Y_PISO - 40))
        out.append(f'<path d="M{f(x0 + rnd.uniform(14, 40))},{f(y)} l{f(rnd.uniform(24, 44))},{f(rnd.uniform(-2, 2))}" stroke="#000" stroke-width="{f(SW * 0.3)}" opacity="0.45"/>')
    archivo(nombre, W, H, 'juego', f'muro de tapia cortado{" con puerta" if puerta else ""}', ''.join(out),
            notas='Canal de papel entre viñetas; se coloca arriba (y=0) y monta 10 px sobre cada cuarto.')


def interior():
    sala()
    alcoba()
    cocina()
    muro_cortado('muro-oeste')
    muro_cortado('puerta-alcoba', 'cortina')
    muro_cortado('puerta-cocina', 'abierta')
    muro_cortado('muro-este')


# ============================================ exterior ============================================
# La casa vista desde el patio, de noche y sin luna [decisión]. De izquierda a derecha: el solar (por
# ahí se huye hacia los cultivos y la quebrada, M2 b4), la cocina, la sala con la reunión (la luz se
# cuela por los postigos y bajo la puerta), la alcoba y el patio con el portillo al camino de Puente
# Alto. Visto desde fuera el orden de los cuartos es el contrario que en el corte del interior.

EXT_ANCHO = 4600
EXT = {'solar': (0, 900), 'casa-cocina': (900, 1900), 'casa-sala': (1900, 3100),
       'casa-alcoba': (3100, 3800), 'patio': (3800, 4600)}
Y_CORREDOR = 900 - 0.25 * M  # piso del corredor (fachada_con_corredor)


def matriz_noche(a, sepia):
    """Matriz de color de la noche: mezcla con la tinta en la proporción a; con sepia, antes deja
    cada color en su luz sobre el papel (la noche quita el color)."""
    tinta = [int(pa.TINTA[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    papel = [int(pa.PAPEL[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    k = 1 - a
    filas = []
    for i, t in enumerate(tinta):
        if sepia:
            p = papel[i]
            filas.append(f'{k * p * 0.2126:.4f} {k * p * 0.7152:.4f} {k * p * 0.0722:.4f} 0 {t * a:.3f}')
        else:
            fila = ['0', '0', '0']
            fila[i] = f'{k:.3f}'
            filas.append(f'{" ".join(fila)} 0 {t * a:.3f}')
    return ' '.join(filas) + ' 0 0 0 1 0'


def filtro_noche(W, Hh, a=None, id_='noche'):
    """Aguada de tinta plana sobre lo dibujado, no sobre lo transparente: mezcla cada color con la
    tinta en la proporción a (por defecto, la del estilo de noche). Así el cielo de los módulos
    sigue transparente."""
    a = NOCHE['afuera'] if a is None else a
    return (f'<filter id="{id_}" filterUnits="userSpaceOnUse" x="0" y="0" width="{f(W)}" height="{f(Hh)}" color-interpolation-filters="sRGB">'
            f'<feColorMatrix type="matrix" values="{matriz_noche(a, NOCHE["sepia"])}"/></filter>')


def de_noche(W, Hh, dibujo, a=None, id_='noche'):
    return f'{filtro_noche(W, Hh, a, id_)}<g filter="url(#{id_})">{dibujo}</g>'


def rendija(x0, y0, x1, y1, ancho=3):
    """Luz de lámpara que se cuela por una rendija: línea clara con un halo plano."""
    halo = NOCHE['halo']
    return (f'<line x1="{f(x0)}" y1="{f(y0)}" x2="{f(x1)}" y2="{f(y1)}" stroke="{col("lampara")}" stroke-width="{f(ancho * 3 * halo)}" stroke-opacity="{min(0.4, 0.22 * halo):.2f}" stroke-linecap="round"/>'
            f'<line x1="{f(x0)}" y1="{f(y0)}" x2="{f(x1)}" y2="{f(y1)}" stroke="{col("lampara")}" stroke-width="{f(ancho)}" stroke-linecap="round"/>')


def suelo_patio(W, rnd, y0=900):
    """Patio de tierra pisada [P] delante de la casa, con alguna piedra suelta."""
    out = [f'<rect x="0" y="{f(y0)}" width="{f(W)}" height="{f(H - y0)}" fill="{lav("tierra", M, 0.9)}"/>',
           f'<rect x="0" y="{f(y0)}" width="{f(W)}" height="10" {SOMBRA}/>']
    for _ in range(int(W / 150)):
        x, y = rnd.uniform(10, W - 40), rnd.uniform(y0 + 30, H - 20)
        r = rnd.uniform(7, 16) * (0.6 + (y - y0) / (H - y0))
        p = [(x + math.cos(k * math.pi / 4) * r * rnd.uniform(0.82, 1.12), y + math.sin(k * math.pi / 4) * r * 0.55) for k in range(8)]
        out.append(f'<path d="{canto(p)}" fill="{lav("piedra", M, 0.8)}" stroke="#000" stroke-width="{f(SW * 0.45)}"/>')
    for _ in range(int(W / 120)):
        x, y = rnd.uniform(0, W - 60), rnd.uniform(y0 + 20, H - 10)
        out.append(f'<path d="M{f(x)},{f(y)} l{f(rnd.uniform(25, 60))},{f(rnd.uniform(-2, 2))}" stroke="#000" stroke-width="{f(SW * 0.35)}"/>')
    return marcar('patio de tierra pisada: por verificar', ''.join(out))


def cerca_piedra(x0, x1, y_base, alto, rnd, m=M, sw=SW, hueco=None):
    """Cerca de piedra seca [P: paleta.md, «piedra»]: una masa de piedra con el borde de arriba
    hecho de piedras de coronación y pocas juntas dentro (detalle, no textura)."""
    tramos = [(x0, x1)] if not hueco else [(x0, hueco[0]), (hueco[1], x1)]
    out = []
    for a, b in tramos:
        y_top = y_base - alto
        d, x, juntas = f'M{f(a)},{f(y_base)} L{f(a)},{f(y_top)}', a, []
        while x < b - 1:
            w = min(b - x, rnd.uniform(0.4, 0.75) * m)
            h = rnd.uniform(0.1, 0.2) * m
            d += f' Q{f(x + w * 0.1)},{f(y_top - h)} {f(x + w / 2)},{f(y_top - h)} Q{f(x + w * 0.9)},{f(y_top - h)} {f(x + w)},{f(y_top)}'
            juntas.append(f'M{f(x + w)},{f(y_top - 2)} L{f(x + w + rnd.uniform(-3, 3))},{f(y_top + h * 0.6)}')
            x += w
        d += f' L{f(b)},{f(y_base)} Z'
        dentro = [f'<rect x="{f(a)}" y="{f(y_top + 0.04 * m)}" width="{f(b - a)}" height="{f(0.08 * m)}" {SOMBRA}/>',
                  f'<path d="{" ".join(juntas)}" stroke="#000" stroke-width="{f(sw * 0.4)}" fill="none"/>']
        # unas pocas piedras sueltas en el cuerpo de la cerca, con su cara en sombra
        for _ in range(max(1, int((b - a) / (1.3 * m)))):
            cx, cy = rnd.uniform(a + 0.2 * m, b - 0.2 * m), rnd.uniform(y_top + 0.25 * alto, y_base - 0.15 * alto)
            w, h = rnd.uniform(0.3, 0.5) * m, rnd.uniform(0.15, 0.24) * m
            p = [(cx + math.cos(k * math.pi / 4) * w * 0.5 * rnd.uniform(0.85, 1.08), cy + math.sin(k * math.pi / 4) * h * 0.5 * rnd.uniform(0.85, 1.08)) for k in range(8)]
            dentro.append(f'<path d="{canto(p)}" fill="none" stroke="#000" stroke-width="{f(sw * 0.4)}"/>'
                          f'<path d="M{f(cx - w * 0.4)},{f(cy + h * 0.3)} Q{f(cx)},{f(cy + h * 0.55)} {f(cx + w * 0.4)},{f(cy + h * 0.3)}" stroke="#000" stroke-width="{f(sw * 0.3)}" fill="none"/>')
        out.append(f'<path d="{d}" fill="{lav("piedra", m, 0.85)}"/>' + recortar(d, ''.join(dentro))
                   + f'<path d="{d}" fill="none" stroke="#000" stroke-width="{f(sw * 0.7)}"/>')
    return marcar('cerca de piedra seca: por verificar (paleta.md, «piedra»)', ''.join(out))


def arbol(cx, y_base, alto, ancho, rnd, m=M, sw=SW):
    """Árbol de cerca (capulí o aliso, [P]): tronco torcido y copa de masas redondas."""
    out = []
    tronco = (f'M{f(cx - 0.12 * m)},{f(y_base)} Q{f(cx - 0.05 * m)},{f(y_base - alto * 0.3)} {f(cx - 0.18 * m)},{f(y_base - alto * 0.55)} '
              f'L{f(cx + 0.02 * m)},{f(y_base - alto * 0.6)} Q{f(cx + 0.08 * m)},{f(y_base - alto * 0.3)} {f(cx + 0.14 * m)},{f(y_base)} Z')
    out.append(f'<path d="{tronco}" fill="{lav("madera", m, 0.75)}" stroke="#000" stroke-width="{f(sw * 0.8)}"/>')
    out.append(f'<path d="M{f(cx - 0.1 * m)},{f(y_base - alto * 0.5)} Q{f(cx - 0.5 * m)},{f(y_base - alto * 0.62)} {f(cx - 0.7 * m)},{f(y_base - alto * 0.72)}" stroke="#000" stroke-width="{f(sw * 2.2)}" fill="none" stroke-linecap="round"/>')
    masas = []
    for _ in range(9):
        mx = cx + rnd.uniform(-0.5, 0.5) * ancho
        my = y_base - alto * rnd.uniform(0.58, 0.95)
        r = ancho * rnd.uniform(0.2, 0.32)
        masas.append((mx, my, r))
    for mx, my, r in sorted(masas, key=lambda t: -t[1]):
        p = [(mx + math.cos(k * math.pi / 5) * r * rnd.uniform(0.85, 1.1), my + math.sin(k * math.pi / 5) * r * 0.8 * rnd.uniform(0.85, 1.1)) for k in range(10)]
        d = canto(p)
        out.append(f'<path d="{d}" fill="{lav("monte", m, 0.9)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>'
                   + recortar(d, f'<path d="M{f(mx - r)},{f(my + r * 0.3)} Q{f(mx)},{f(my + r * 0.9)} {f(mx + r)},{f(my + r * 0.3)} L{f(mx + r)},{f(my + r)} L{f(mx - r)},{f(my + r)} Z" {SOMBRA}/>'))
    return f'<g data-p="árbol de cerca: especie por verificar (capulí, aliso)">{"".join(out)}</g>'


def ventana_trancada(x0, y0, w, h):
    """Ventana de la sala por fuera: reja de balaústres y, detrás, los postigos cerrados. Devuelve
    (lo de detrás, la luz que se cuela por las juntas, la reja de delante)."""
    detras = (f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="#000"/>'
              + puerta_tablas(x0 + 6, y0 + 6, w - 12, h - 12, M, SW * 0.8, random.Random(9), hojas=2))
    riel = 0.07 * M + 4  # las juntas de arriba y abajo quedan por dentro de los rieles de la reja
    luz = (rendija(x0 + w / 2, y0 + 10, x0 + w / 2, y0 + h - 10, 3)
           + rendija(x0 + 12, y0 + riel, x0 + w - 12, y0 + riel, 2)
           + rendija(x0 + 14, y0 + h - riel, x0 + w * 0.42, y0 + h - riel, 2)
           + rendija(x0 + w * 0.72, y0 + 16, x0 + w * 0.72, y0 + h * 0.55, 1.5))
    delante = []
    n = max(5, int(w / (0.11 * M)))
    for i in range(1, n):
        x = x0 + w * i / n
        r = 0.022 * M
        delante.append(f'<path d="M{f(x - r)},{f(y0 + 0.06 * M)} L{f(x - r)},{f(y0 + h * 0.3)} Q{f(x - r * 2)},{f(y0 + h * 0.4)} {f(x - r)},{f(y0 + h * 0.5)} L{f(x - r)},{f(y0 + h - 0.06 * M)} '
                       f'L{f(x + r)},{f(y0 + h - 0.06 * M)} L{f(x + r)},{f(y0 + h * 0.5)} Q{f(x + r * 2)},{f(y0 + h * 0.4)} {f(x + r)},{f(y0 + h * 0.3)} L{f(x + r)},{f(y0 + 0.06 * M)} Z" '
                       f'fill="{madera(0.55)}" stroke="#000" stroke-width="{f(SW * 0.35)}"/>')
    delante.append(tabla(x0, y0, x0 + w, y0 + 0.07 * M, 0.55, 0.6) + tabla(x0, y0 + h - 0.07 * M, x0 + w, y0 + h, 0.55, 0.6))
    delante.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="none" stroke="#000" stroke-width="{f(SW)}"/>')
    delante.append(f'<rect x="{f(x0 - 0.06 * M)}" y="{f(y0 + h)}" width="{f(w + 0.12 * M)}" height="{f(0.06 * M)}" fill="{lav("cal", M)}" stroke="#000" stroke-width="{f(SW * 0.6)}"/>')
    return detras, luz, ''.join(delante)


def casa_modulo(nombre, pilares, huecos, esquinas, luz='', delante='', titulo='', notas=''):
    """Un tramo de la fachada con corredor, de noche: la fachada de la plaza, la aguada de la noche,
    lo que brilla encima y lo que va delante de la luz (también de noche)."""
    x0, x1 = EXT[nombre]
    W = x1 - x0
    rnd = random.Random(sum(map(ord, nombre)) + 400)
    # En los empalmes la fachada se dibuja 40 px más larga y se recorta en el borde del módulo:
    # el borde del muro, del piso y del alero no deja una raya donde se juntan dos módulos.
    izq, der = (0 if esquinas[0] else 40), (0 if esquinas[1] else 40)

    def corrido(h):
        return lambda m, sw, y, r: f'<g transform="translate({izq} 0)">{h(m, sw, y, r)}</g>'

    fachada = pa.fachada_con_corredor(W + izq + der, rnd, None, [p + izq for p in pilares],
                                      [corrido(h) for h in huecos], esquinas=esquinas)
    fachada = f'<g transform="translate({-izq} 0)">{fachada}</g>'
    # con luna, el tejado y el patio quedan a la luz y el corredor, bajo el alero, en sombra
    sombra_luna = (f'<rect x="0" y="{f(Y_CORREDOR - 3.32 * M)}" width="{f(W)}" height="{f(3.32 * M)}" fill="#000" fill-opacity="0.45"/>'
                   if NOCHE['luna'] else '')
    cuerpo = (de_noche(W, H, fachada + suelo_patio(W, rnd))
              + sombra_luna
              + luz
              + (de_noche(W, H, delante, id_='noche2') if delante else ''))
    archivo(nombre, W, H, 'juego', titulo, cuerpo,
            notas=f'Se coloca arriba (y=0) en x={x0} del exterior de noche. {notas}')


def humo_tejado(x, rnd):
    """Humo que se filtra entre las tejas de la cocina (sin chimenea [P])."""
    d, y, xx = f'M{f(x)},{f(200)}', 200, x
    while y > 0:
        y -= 46
        xx += rnd.uniform(-10, 28)
        d += f' Q{f(xx - rnd.uniform(-24, 24))},{f(y + 23)} {f(xx)},{f(y)}'
    return f'<path d="{d}" stroke="{col("humo-claro")}" stroke-width="{f(rnd.uniform(12, 20))}" stroke-opacity="0.28" fill="none" stroke-linecap="round"/>'


def exterior_casa():
    # Pilares cada ≈2,7 m a lo largo de toda la fachada, lejos de los empalmes de los módulos.
    def leña(m, sw, y_piso, rnd):
        return leña_apilada(150, 340, rnd, y_suelo=y_piso, filas=5)

    def puerta_cocina(m, sw, y_piso, rnd):
        return puerta_tablas(720, y_piso - 2.0 * m, 0.9 * m, 2.0 * m, m, sw, rnd)

    rnd = random.Random(5)
    casa_modulo('casa-cocina', [80, 620], [leña, puerta_cocina], (True, False),
                luz=(rendija(726, Y_CORREDOR - 3, 714 + 0.9 * M, Y_CORREDOR - 3, 2).replace(col('lampara'), col('brasa'))
                     + ''.join(humo_tejado(x, rnd) for x in (260, 420, 610, 770))),
                titulo='fachada: la cocina con su puerta y la leña; el humo sale entre las tejas',
                notas='Bajo la puerta, el resplandor del fogón (brasa).')

    v_x0, v_w, v_h = 330, 1.25 * M, 1.1 * M
    v_y0 = Y_CORREDOR - 2.0 * M
    detras, luz_v, delante = ventana_trancada(v_x0, v_y0, v_w, v_h)
    p_x0, p_w = 860, 0.95 * M

    def ventana(m, sw, y_piso, rnd):
        return detras

    def puerta(m, sw, y_piso, rnd):
        return puerta_tablas(p_x0, y_piso - 2.05 * m, p_w, 2.05 * m, m, sw, rnd)

    def banca_corredor(m, sw, y_piso, rnd):
        ys = y_piso - 0.45 * m
        return (f'<rect x="{f(v_x0 - 20)}" y="{f(ys)}" width="{f(v_w + 40)}" height="{f(0.07 * m)}" fill="{madera(0.55)}" stroke="#000" stroke-width="{f(sw * 0.7)}"/>'
                + ''.join(f'<rect x="{f(xx)}" y="{f(ys + 0.07 * m)}" width="{f(0.08 * m)}" height="{f(y_piso - ys - 0.07 * m)}" fill="{madera(0.55)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>'
                          for xx in (v_x0, v_x0 + v_w - 0.08 * m)))

    # la luz de la reunión: juntas de los postigos, bajo la puerta, el ojo de la cerradura, y
    # rayas sobre el corredor y el patio
    luz_puerta = (rendija(p_x0 + 4, Y_CORREDOR - 2, p_x0 + p_w - 4, Y_CORREDOR - 2, 3)
                  + rendija(p_x0 + p_w - 3, Y_CORREDOR - 2.0 * M, p_x0 + p_w - 3, Y_CORREDOR - 10, 1.5)
                  + f'<circle cx="{f(p_x0 + p_w * 0.85)}" cy="{f(Y_CORREDOR - 2.05 * M * 0.48)}" r="3" fill="{col("lampara")}"/>')
    halo = NOCHE['halo']
    rayas = (f'<path d="M{f(p_x0 + 6)},{f(Y_CORREDOR)} L{f(p_x0 + p_w - 6)},{f(Y_CORREDOR)} L{f(p_x0 + p_w + 40)},{f(900)} L{f(p_x0 - 30)},{f(900)} Z" fill="{col("lampara")}" fill-opacity="{0.22 * halo:.2f}"/>'
             f'<path d="M{f(p_x0 - 30)},{f(900)} L{f(p_x0 + p_w + 40)},{f(900)} L{f(p_x0 + p_w + 90)},{f(960)} L{f(p_x0 - 70)},{f(960)} Z" fill="{col("lampara")}" fill-opacity="{0.1 * halo:.2f}"/>')
    casa_modulo('casa-sala', [160, 700], [ventana, banca_corredor, puerta], (False, False),
                luz=luz_v + luz_puerta + rayas, delante=delante,
                titulo='fachada: la sala con los postigos cerrados; la luz se cuela por las juntas y bajo la puerta',
                notas=f'Ventana en x local {v_x0}; puerta de la casa en {p_x0}–{f(p_x0 + p_w)}.')

    def ventanuco(m, sw, y_piso, rnd):
        x0, w, h = 300, 0.6 * m, 0.55 * m
        y0 = y_piso - 2.1 * m
        return (f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" fill="#000"/>'
                + puerta_tablas(x0 + 4, y0 + 4, w - 8, h - 8, m, sw * 0.7, rnd, hojas=2)
                + f'<rect x="{f(x0 - 0.05 * m)}" y="{f(y0 + h)}" width="{f(w + 0.1 * m)}" height="{f(0.05 * m)}" fill="{lav("cal", m)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')

    casa_modulo('casa-alcoba', [100, 620], [ventanuco], (False, True),
                titulo='fachada: la alcoba, oscura, y la esquina de la casa')


def solar():
    """Solar a la izquierda de la casa: huerta en surcos, la cerca con su boquete hacia los
    cultivos y la quebrada (huida de la M2) y un árbol."""
    x0, x1 = EXT['solar']
    W = x1 - x0
    rnd = random.Random(1201)
    out = [arbol(560, 860, 3.9 * M, 2.6 * M, rnd),
           cerca_piedra(-20, W + 20, 880, 0.75 * M, rnd, hueco=(250, 420))]
    # huerta: surcos de tierra con matas (papa y haba [P])
    out.append(f'<rect x="0" y="880" width="{W}" height="{H - 880}" fill="{lav("tierra", M, 0.95)}"/>')
    y, fila = 906, 0
    while y < H:
        alto = 22 + fila * 10
        out.append(f'<path d="M0,{f(y)} Q{f(W / 2)},{f(y - 6)} {W},{f(y)} L{W},{f(y + alto * 0.35)} Q{f(W / 2)},{f(y + alto * 0.35 - 6)} 0,{f(y + alto * 0.35)} Z" {SOMBRA}/>')
        x = rnd.uniform(0, 90)
        while x < W:
            r = alto * rnd.uniform(0.5, 0.75)
            p = [(x + math.cos(k * math.pi / 5) * r * rnd.uniform(0.75, 1.1), y - r * 0.4 + math.sin(k * math.pi / 5) * r * 0.55) for k in range(10)]
            out.append(f'<path d="{canto(p)}" fill="{lav("sementera", M)}" stroke="#000" stroke-width="{f(SW * 0.45)}"/>')
            x += r * rnd.uniform(4.5, 6.5)
        y += alto + 14
        fila += 1
    # el boquete de la cerca: senda que baja hacia la quebrada
    out.append(f'<path d="M250,880 Q330,860 420,880 L460,{H} L190,{H} Z" fill="{lav("tierra", M, 0.75)}"/>')
    cuerpo = de_noche(W, H, '\n'.join(out))
    archivo('solar', W, H, 'juego', 'solar con huerta, cerca de piedra y la senda de la huida', cuerpo,
            notas=f'Se coloca arriba (y=0) en x={x0}. El boquete de la cerca (x 250–420) es la salida hacia los cultivos y la quebrada (M2 b4).')


def patio_portillo():
    """El patio sigue hasta el portillo de varas que da al camino de Puente Alto."""
    x0, x1 = EXT['patio']
    W = x1 - x0
    rnd = random.Random(1202)
    out = [suelo_patio(W, rnd),
           cerca_piedra(120, 470, 880, 0.75 * M, rnd), cerca_piedra(690, W + 20, 880, 0.75 * M, rnd)]
    # portillo: dos postes y varas cruzadas, entreabierto
    for px in (470, 690):
        out.append(tabla(px - 12, 880 - 1.35 * M, px + 12, 900, 0.6, 0.8))
    for k in range(4):
        yy = 880 - 0.25 * M - k * 0.27 * M
        out.append(f'<path d="M{f(482)},{f(yy)} L{f(650)},{f(yy + 18)}" stroke="#000" stroke-width="{f(SW * 3.2)}" stroke-linecap="round"/>'
                   f'<path d="M{f(482)},{f(yy)} L{f(650)},{f(yy + 18)}" stroke="{madera(0.7)}" stroke-width="{f(SW * 2)}" stroke-linecap="round"/>')
    out.append(f'<path d="M470,{H} L520,880 L640,880 L760,{H} Z" fill="{lav("tierra", M, 0.75)}"/>')
    cuerpo = de_noche(W, H, '\n'.join(out))
    archivo('patio', W, H, 'juego', 'patio y portillo de varas al camino de Puente Alto', cuerpo,
            notas=f'Se coloca arriba (y=0) en x={x0}. Por el portillo (x 470–690) llegan los vecinos, la Seccional y la partida.')


def cielo_noche():
    """Cielo sin luna [decisión] en sepia oscuro (paleta.md §3: la noche no es azul): el fondo de
    cámara pone el color; aquí van una franja más clara sobre el horizonte, la sierra lejana en
    silueta, Puente Alto a lo lejos y pocas estrellas."""
    rnd = random.Random(1946)
    W, Hh = 1920, 700
    out = []
    franja = [(0, 470)] + [(x, 470 + 25 * math.sin(x / 260) + rnd.uniform(-6, 6)) for x in range(80, 1921, 80)]
    out.append(f'<path d="{pa.curva(franja)} L1920,{Hh} L0,{Hh} Z" fill="{col("sepia")}" fill-opacity="0.55"/>')
    perf = pa.perfil([(0, 560), (300, 520), (620, 548), (900, 500), (1250, 540), (1500, 525), (1920, 556)], 0, 1920, rnd, 4, paso=12)
    # en el cielo la línea es grafito, más clara que la noche: las siluetas van en tinta plena
    out.append(f'<path d="M0,{Hh} L{" L".join(f"{f(x)},{f(y)}" for x, y in perf)} L1920,{Hh} Z" fill="{col("tinta-plena")}" fill-opacity="0.72"/>')
    # Puente Alto en la loma: torre y tejados, sin luces [P: luz eléctrica en 1946]
    tx, ty = 1560, pa.y_de(perf, 1560) + 2
    pueblo = [f'<rect x="{f(tx - 7)}" y="{f(ty - 44)}" width="14" height="44"/>',
              f'<path d="M{f(tx - 8)},{f(ty - 44)} Q{f(tx)},{f(ty - 56)} {f(tx + 8)},{f(ty - 44)} Z"/>',
              f'<path d="M{f(tx)},{f(ty - 56)} L{f(tx)},{f(ty - 64)} M{f(tx - 3)},{f(ty - 61)} L{f(tx + 3)},{f(ty - 61)}" stroke="{col("tinta-plena")}" stroke-width="1.2"/>',
              f'<path d="M{f(tx - 40)},{f(ty)} L{f(tx - 40)},{f(ty - 16)} L{f(tx - 20)},{f(ty - 26)} L{f(tx - 8)},{f(ty - 16)} L{f(tx - 8)},{f(ty)} Z"/>']
    for k, (dx, w, h) in enumerate([(-110, 30, 9), (-76, 24, 8), (22, 34, 10), (62, 26, 8), (96, 30, 7)]):
        pueblo.append(f'<path d="M{f(tx + dx)},{f(ty)} L{f(tx + dx)},{f(ty - h)} L{f(tx + dx + w / 2)},{f(ty - h - 5)} L{f(tx + dx + w)},{f(ty - h)} L{f(tx + dx + w)},{f(ty)} Z"/>')
    out.append(f'<g data-p="Puente Alto a lo lejos (iglesia [P])" fill="{col("tinta-plena")}" fill-opacity="0.85">{"".join(pueblo)}</g>')
    # pocas estrellas, separadas: nada de cielo punteado
    estrellas = []
    while len(estrellas) < 26:
        x, y = rnd.uniform(20, 1900), rnd.uniform(24, 400)
        if all((x - a) ** 2 + (y - b) ** 2 > 140 ** 2 for a, b in estrellas):
            estrellas.append((x, y))
    for i, (x, y) in enumerate(estrellas):
        r = 2.4 if i % 7 == 0 else rnd.uniform(1.5, 2)
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="#fff" fill-opacity="{0.9 if i % 7 == 0 else 0.65}"/>')
        if i % 7 == 0:
            out.append(f'<path d="M{f(x - 7)},{f(y)} L{f(x + 7)},{f(y)} M{f(x)},{f(y - 7)} L{f(x)},{f(y + 7)}" stroke="#fff" stroke-width="1" stroke-opacity="0.6"/>')
    if NOCHE['luna']:
        # luna de papel con un halo plano [P: la fase de la luna en las fechas del guion]
        out.append('<circle cx="1480" cy="150" r="84" fill="#fff" fill-opacity="0.08"/>'
                   '<circle cx="1480" cy="150" r="46" fill="#fff" fill-opacity="0.12"/>'
                   '<circle cx="1480" cy="150" r="26" fill="#fff"/>'
                   f'<path d="M1470,140 q6,-4 12,2 M1488,158 q4,2 2,8" stroke="{col("sepia-claro")}" stroke-width="2" fill="none"/>')
    archivo('cielo-noche', W, Hh, 'cielo', 'cielo de noche, sierra y Puente Alto a lo lejos', '\n'.join(out),
            notas='Se coloca arriba (y=0). El color del cielo lo pone el fondo de cámara (sepia-oscuro).')


def lomas(nombre, x_capa0, W, semilla, casas):
    """Lomas de la vereda en la capa lejana (30 px/m), de noche: siluetas con pocas lindes y alguna
    ventana con lámpara (las casas de los vecinos)."""
    rnd = random.Random(semilla)
    m, sw = ppm('lejos'), TRAZO['lejos']
    Hh, y0 = 380, 380            # se coloca arriba en y=380: cubre de 380 a 760
    suelo = 628 - y0
    ctrl = [(0, suelo - 80 - rnd.uniform(0, 40))]
    for x in range(260, W + 260, 260):
        ctrl.append((x, suelo - rnd.uniform(40, 150)))
    perf = pa.perfil(ctrl, 0, W, rnd, 2.5, paso=10)
    loma = f'M0,{Hh} L{" L".join(f"{f(x)},{f(y)}" for x, y in perf)} L{W},{Hh} Z'
    out = [f'<path d="{loma}" fill="{lav("potrero", m)}" stroke="#000" stroke-width="{f(sw)}"/>']
    lindes = []
    for _ in range(int(W / 200)):
        x = rnd.uniform(40, W - 200)
        y = pa.y_de(perf, x) + rnd.uniform(14, 60)
        lindes.append(f'M{f(x)},{f(y)} q{f(rnd.uniform(60, 120))},{f(rnd.uniform(-10, 14))} {f(rnd.uniform(120, 200))},{f(rnd.uniform(-4, 22))}')
    out.append(recortar(loma, f'<path d="{" ".join(lindes)}" stroke="#000" stroke-width="{f(sw * 0.6)}" fill="none"/>'))
    luces = []
    for cx in casas:
        cy = pa.y_de(perf, cx) + 26
        out.append(f'<path d="M{f(cx - 14)},{f(cy)} L{f(cx - 14)},{f(cy - 10)} L{f(cx)},{f(cy - 17)} L{f(cx + 14)},{f(cy - 10)} L{f(cx + 14)},{f(cy)} Z" fill="{lav("cal", m)}" stroke="#000" stroke-width="{f(sw * 0.7)}"/>')
        luces.append(f'<circle cx="{f(cx + 5)}" cy="{f(cy - 5)}" r="7" fill="{col("lampara")}" fill-opacity="0.25"/>'
                     f'<rect x="{f(cx + 3)}" y="{f(cy - 7)}" width="4" height="4" fill="{col("lampara")}"/>')
    cuerpo = de_noche(W, Hh, '\n'.join(out), a=NOCHE['lejos']) + ''.join(luces)
    archivo(nombre, W, Hh, 'lejos', 'lomas de la vereda de noche, con alguna lámpara', cuerpo,
            notas=f'Se coloca arriba en y={y0} (cubre el suelo lejano, y=628) y en x={x_capa0}.')


def campo(nombre, x_capa0, W, semilla, vecina=None):
    """Cultivos de la vereda en la capa media (90 px/m): papa en surcos, una cerca y árboles; en el
    lado del camino, la casa de los vecinos con su lámpara (la que Heliodoro no deja quemar, M2 b3)."""
    rnd = random.Random(semilla)
    m, sw = ppm('medio'), TRAZO['medio']
    Hh, y0 = 800, 120           # se coloca arriba en y=120: cubre de 120 a 920 (caben los árboles)
    suelo = 724 - y0
    out = []
    for cx in (rnd.uniform(80, W * 0.4), rnd.uniform(W * 0.55, W - 80)):
        out.append(arbol(cx, suelo + 10, 6.5 * m, 4.2 * m, rnd, m, sw))
    luz = ''
    if vecina is not None:
        vx, vw = vecina, 4.6 * m
        yb = suelo + 6
        techo = f'M{f(vx - 0.3 * m)},{f(yb - 2.6 * m)} L{f(vx + vw + 0.3 * m)},{f(yb - 2.6 * m)} L{f(vx + vw)},{f(yb - 3.9 * m)} L{f(vx)},{f(yb - 3.9 * m)} Z'
        out.append(f'<rect x="{f(vx)}" y="{f(yb - 2.6 * m)}" width="{f(vw)}" height="{f(2.6 * m)}" fill="{lav("cal", m)}" stroke="#000" stroke-width="{f(sw)}"/>'
                   f'<path d="{techo}" fill="{lav("teja", m)}" stroke="#000" stroke-width="{f(sw * 0.8)}"/>'
                   f'<rect x="{f(vx + 0.6 * m)}" y="{f(yb - 2.0 * m)}" width="{f(0.85 * m)}" height="{f(2.0 * m)}" fill="{madera(0.6)}" stroke="#000" stroke-width="{f(sw * 0.7)}"/>'
                   f'<rect x="{f(vx + 2.4 * m)}" y="{f(yb - 1.9 * m)}" width="{f(0.9 * m)}" height="{f(0.8 * m)}" fill="#000"/>')
        wx, wy = vx + 2.4 * m, yb - 1.9 * m
        luz = (rendija(wx + 0.45 * m, wy + 4, wx + 0.45 * m, wy + 0.8 * m - 4, 2)
               + rendija(wx + 6, wy + 0.8 * m - 4, wx + 0.9 * m - 6, wy + 0.8 * m - 4, 1.5))
    out.append(cerca_piedra(-10, W + 10, suelo + 30, 0.7 * m, rnd, m, sw))
    # surcos de papa del lado de acá de la cerca
    out.append(f'<rect x="0" y="{f(suelo + 30)}" width="{W}" height="{f(Hh - suelo - 30)}" fill="{lav("tierra", m)}"/>')
    y = suelo + 40
    while y < Hh:
        out.append(f'<path d="M0,{f(y)} Q{f(W / 2)},{f(y - 4)} {W},{f(y)}" stroke="#000" stroke-width="{f(sw * 0.5)}" fill="none"/>')
        x = rnd.uniform(0, 60)
        while x < W:
            r = rnd.uniform(5, 8) * (1 + (y - suelo) / 200)
            out.append(f'<circle cx="{f(x)}" cy="{f(y - r * 0.6)}" r="{f(r)}" fill="{lav("sementera", m)}" stroke="#000" stroke-width="{f(sw * 0.4)}"/>')
            x += r * rnd.uniform(6, 10)
        y += 18 + (y - suelo) * 0.16
    cuerpo = de_noche(W, Hh, '\n'.join(out), a=NOCHE['lejos']) + luz
    archivo(nombre, W, Hh, 'medio', 'cultivos de la vereda de noche' + (', con la casa de los vecinos' if vecina else ''), cuerpo,
            notas=f'Se coloca arriba en y={y0} (cubre el suelo medio, y=724) y en x={x_capa0}.')


def maguey(nombre, semilla):
    """Mata de fique en primer plano [P]: silueta de tinta con la base bajo el cuadro."""
    rnd = random.Random(semilla)
    m, sw = ppm('frente'), TRAZO['frente']
    W, Hh = 520, 340
    cx = W / 2
    hojas = []
    for k in range(11):
        a = -80 + k * 16 + rnd.uniform(-5, 5)
        largo = rnd.uniform(0.75, 1.2) * m
        ex, ey = cx + math.sin(math.radians(a)) * largo, Hh - math.cos(math.radians(a)) * largo
        bx = cx + math.sin(math.radians(a)) * 18
        hojas.append(f'<path d="M{f(bx - 14)},{f(Hh)} Q{f((bx + ex) / 2 - 10)},{f((Hh + ey) / 2)} {f(ex)},{f(ey)} Q{f((bx + ex) / 2 + 12)},{f((Hh + ey) / 2 + 8)} {f(bx + 14)},{f(Hh)} Z" fill="#000"/>'
                     f'<path d="M{f(bx)},{f(Hh - 10)} Q{f((bx + ex) / 2)},{f((Hh + ey) / 2 + 4)} {f(ex)},{f(ey)}" stroke="{col("sepia")}" stroke-width="{f(sw * 0.4)}" fill="none"/>')
    archivo(nombre, W, Hh, 'frente', 'mata de fique en primer plano', marcar('mata de fique: por verificar', ''.join(hojas)),
            notas='Se coloca con la base por debajo del cuadro: solo asoman las puntas.')


def exterior():
    cielo_noche()
    lomas('lomas-oeste', 0, 1100, 31, casas=[260, 820])
    lomas('lomas-este', 1300, 1022, 32, casas=[420, 900])
    campo('campo-oeste', 0, 1000, 41)
    campo('campo-este', 2200, 926, 42, vecina=380)
    solar()
    exterior_casa()
    patio_portillo()
    maguey('maguey', 51)


if __name__ == '__main__':
    for acto, sufijo in (('prologo', 'prologo'), ('acto1', 'acto1')):
        pa.usar_acto(acto)
        pa.OUTDIR = os.path.join(BASE, f'interior-{sufijo}')
        interior()
        pa.OUTDIR = os.path.join(BASE, f'exterior-{sufijo}')
        exterior()
