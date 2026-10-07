"""Generador de la iglesia de Puente Alto por dentro: los fondos de la página de cómic de la misa
del Prólogo (b3) (game/art/src/fondos/iglesia/*.svg).

Prólogo b3 (doc 02 §5): misa dominical; el padre Evaristo predica sobre «el peligro rojo» y Rosalba
y Efraín salen antes (sin interacción). Daniel aprobó el 05-oct-2026 que vaya como página de cómic
de cuatro viñetas: la nave alta con el púlpito, el púlpito, la salida y el atrio. Composición,
fuentes y [V]/[P]: planeacion/arte/tomo1/escenarios/iglesia.md.

La iglesia es la misma de la plaza (puente_alto.py, `iglesia`): colonial, de una nave, con portada
de piedra y torre a la derecha. Todo es [P] (doc 03 §3.1) y va marcado con data-p. El padre
Evaristo, Rosalba y Efraín van como figuras provisionales (gris y borde discontinuo) hasta que
tengan hoja en la página. El marco de las viñetas y los globos son de la página (PaginaComic,
doc 04 §4), no de estos fondos.

  python3 art/gen/iglesia.py      (desde game/; sin dependencias)

Además compone la página de revisión en art/build/revision/pagina-misa.svg (no va al atlas).
Edita este script, no los SVG generados.
"""
import math
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import puente_alto as pa  # noqa: E402
from puente_alto import SOMBRA, SOMBRA_FUERTE, SOMBRA_HONDA, SOMBRA_SUAVE, f, lav, recortar  # noqa: E402

pa.ESCENA, pa.GENERADOR = 'Iglesia de Puente Alto', 'game/art/gen/iglesia.py'
AQUI = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(AQUI, '..', 'src', 'fondos', 'iglesia')
REVISION = os.path.join(AQUI, '..', 'build', 'revision')

# Página de 1920×1080 con margen de 44 px y canal de 28 (iglesia.md §2): x, y, ancho, alto.
PAGINA = {
    'misa-1-nave': (44, 44, 560, 992),
    'misa-2-pulpito': (632, 44, 1244, 470),
    'misa-3-salida': (632, 542, 608, 494),
    'misa-4-atrio': (1268, 542, 608, 494),
}
DIBUJOS = {}

# La nave (metros) [P]: muros encalados de 7 m hasta la solera, armadura de par y nudillo con
# tirantes, pasillo central entre bancas.
ANCHO = 3.8          # media nave
MURO = 7.0           # solera
NUDILLO, XN = 9.0, 1.5
PASILLO = 0.75       # medio pasillo
BANCA = 3.3          # punta de la banca contra el muro
LUZ = 'fill="#fff" fill-opacity="0.3"'
RESPLANDOR = 'fill="#fff" fill-opacity="0.07"'


def c(token, luz=1.0):
    """Color pleno de la paleta: todo está cerca (lav a 200 px/m)."""
    return lav(token, 200, luz)


def guardar(nombre, titulo, cuerpo, notas=''):
    x, y, w, h = PAGINA[nombre]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <!--
    {pa.ESCENA} · {titulo}
    Viñeta de la página de la misa (Prólogo b3), {w}×{h} px. En la página va en x={x}, y={y}
    (iglesia.md §2); el marco y los globos los pone la página.
    {notas}
    Colores: paleta del juego (game/art/paleta.json, planeacion/arte/tomo1/paleta.md), croma del
    Prólogo. Lo [P] va marcado con data-p; las figuras grises de borde discontinuo son provisionales.
    GENERADO por {pa.GENERADOR}: edita el script, no este archivo.
  -->{pa.tramas()}
<clipPath id="cuadro-{nombre}"><rect width="{w}" height="{h}"/></clipPath>
<g clip-path="url(#cuadro-{nombre})">
{cuerpo}
</g>
</svg>
'''
    svg = re.sub(r'"#000"', f'"{pa.TINTA}"', svg)
    svg = re.sub(r'"#fff"', f'"{pa.PAPEL}"', svg)
    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, nombre + '.svg'), 'w') as fh:
        fh.write(svg)
    DIBUJOS[nombre] = svg
    print('ok', nombre, f'{w}x{h}')


def recortar_poligono(q, x0, y0, x1, y1):
    """Sutherland–Hodgman: el polígono de pantalla q recortado al rectángulo."""
    def cruce_x(a, b, x):
        t = (x - a[0]) / (b[0] - a[0])
        return x, a[1] + t * (b[1] - a[1])

    def cruce_y(a, b, y):
        t = (y - a[1]) / (b[1] - a[1])
        return a[0] + t * (b[0] - a[0]), y
    for dentro, cruce in ((lambda p: p[0] >= x0, lambda a, b: cruce_x(a, b, x0)),
                          (lambda p: p[0] <= x1, lambda a, b: cruce_x(a, b, x1)),
                          (lambda p: p[1] >= y0, lambda a, b: cruce_y(a, b, y0)),
                          (lambda p: p[1] <= y1, lambda a, b: cruce_y(a, b, y1))):
        entrada, q = q, []
        for i, p in enumerate(entrada):
            a = entrada[i - 1]
            if dentro(p):
                if not dentro(a):
                    q.append(cruce(a, p))
                q.append(p)
            elif dentro(a):
                q.append(cruce(a, p))
        if not q:
            break
    return q


def recortar_segmento(p, q, x0, y0, x1, y1):
    """Liang–Barsky: el segmento de pantalla p–q recortado al rectángulo (o None)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pp == 0:
            if qq < 0:
                return None
            continue
        r = qq / pp
        if pp < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
    if t0 > t1:
        return None
    return (p[0] + t0 * dx, p[1] + t0 * dy), (p[0] + t1 * dx, p[1] + t1 * dy)


class Vista:
    """Perspectiva de un punto, en metros: x a la derecha, y hacia arriba, z hacia el fondo. El ojo
    está en (0, ojo, 0), mira hacia +z y el punto de fuga cae en (cx, cy).

    Los polígonos y las líneas salen recortados al cuadro (con un margen): lo que queda cerca del
    ojo se proyecta a miles de píxeles y, con un clipPath detrás, resvg cae (geom.rs:27)."""

    def __init__(self, cx, cy, foco, ojo, ancho, alto, margen=24):
        self.cx, self.cy, self.foco, self.ojo = cx, cy, foco, ojo
        self.caja = (-margen, -margen, ancho + margen, alto + margen)

    def p(self, x, y, z):
        return self.cx + self.foco * x / z, self.cy - self.foco * (y - self.ojo) / z

    def d(self, *puntos):
        q = recortar_poligono([self.p(*pt) for pt in puntos], *self.caja)
        if len(q) < 3:
            return ''
        return 'M' + ' L'.join(f'{f(a)},{f(b)}' for a, b in q) + ' Z'

    def linea(self, a, b):
        tramo = recortar_segmento(self.p(*a), self.p(*b), *self.caja)
        if not tramo:
            return ''
        (x0, y0), (x1, y1) = tramo
        return f'M{f(x0)},{f(y0)} L{f(x1)},{f(y1)}'

    def esc(self, z):
        return self.foco / z


def trazo(z, grueso=2.6):
    """Línea más fina cuanto más lejos (doc 03 §1: gruesa cerca, fina al fondo)."""
    return max(0.6, min(grueso, grueso * 2.5 / z))


def plano(v, puntos, relleno, sombra=None, sw=None):
    d = v.d(*puntos)
    if not d:
        return ''
    out = f'<path d="{d}" fill="{relleno}"'
    out += f' stroke="#000" stroke-width="{f(sw)}" stroke-linejoin="round"/>' if sw else '/>'
    if sombra:
        out += f'<path d="{d}" {sombra}/>'
    return out


def seccion(z):
    """Corte de la nave en z: muros, solera y armadura."""
    return [(-ANCHO, 0, z), (-ANCHO, MURO, z), (-XN, NUDILLO, z), (XN, NUDILLO, z), (ANCHO, MURO, z), (ANCHO, 0, z)]


def arco_en(v, z, r, y0, ancho_pie=None, n=24):
    """Vano de medio punto en el plano z: arranca a y0 con radio r (lista de puntos de pantalla)."""
    q = [v.p(-r, 0, z), v.p(-r, y0, z)]
    for k in range(1, n):
        a = math.pi - math.pi * k / n
        q.append(v.p(r * math.cos(a), y0 + r * math.sin(a), z))
    q += [v.p(r, y0, z), v.p(r, 0, z)]
    return q


def camino(q, cerrar=True):
    return 'M' + ' L'.join(f'{f(a)},{f(b)}' for a, b in q) + (' Z' if cerrar else '')


def convexa(puntos):
    """Envolvente convexa (cadena monótona) de puntos de pantalla."""
    p = sorted(set(puntos))
    if len(p) < 3:
        return p

    def giro(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    abajo, arriba = [], []
    for q in p:
        while len(abajo) >= 2 and giro(abajo[-2], abajo[-1], q) <= 0:
            abajo.pop()
        abajo.append(q)
    for q in reversed(p):
        while len(arriba) >= 2 and giro(arriba[-2], arriba[-1], q) <= 0:
            arriba.pop()
        arriba.append(q)
    return abajo[:-1] + arriba[:-1]


# ================================== fieles y figuras provisionales ==================================

def _P(cx, yh, s, espejo=False):
    """Punto en metros respecto a los hombros (dx a la derecha, dy hacia arriba)."""
    k = -1 if espejo else 1
    return lambda dx, dy: f'{f(cx + k * dx * s)},{f(yh - dy * s)}'


def contorno_mujer(P, abajo=-0.45):
    # pañolón sobre la cabeza y los hombros (Ocampo López: pañolón negro) [V]; en misa, cubierta [P].
    # abajo: hasta dónde baja la figura bajo los hombros (de espaldas la tapa el respaldo; de
    # frente llega al suelo con la falda)
    ancho = 0.31 if abajo > -0.7 else 0.36
    return (f'M{P(-0.07, 0.36)} Q{P(0, 0.43)} {P(0.07, 0.36)} Q{P(0.13, 0.27)} {P(0.12, 0.13)} '
            f'Q{P(0.16, 0.03)} {P(0.27, -0.03)} L{P(ancho, abajo)} L{P(-ancho, abajo)} L{P(-0.27, -0.03)} '
            f'Q{P(-0.16, 0.03)} {P(-0.12, 0.13)} Q{P(-0.13, 0.27)} {P(-0.07, 0.36)} Z')


def contorno_ruana(P, abajo=-0.45):
    return (f'M{P(-0.22, -0.02)} Q{P(0, 0.04)} {P(0.22, -0.02)} Q{P(0.29, -0.08)} {P(0.31, -0.2)} '
            f'L{P(0.34, abajo)} L{P(-0.34, abajo)} L{P(-0.31, -0.2)} Q{P(-0.29, -0.08)} {P(-0.22, -0.02)} Z')


def cabeza(P, s, dy=0.26):
    cx, cy = (float(t) for t in P(0, dy).split(','))
    return cx, cy, 0.085 * s, 0.11 * s


def fiel(cx, yh, s, tipo, sw, rnd, de='espalda', gira=0):
    """Fiel sentado, de los hombros arriba (lo de abajo lo tapa la banca). Sin rostro (doc 03 §1).
    de: 'espalda' (se le ve la nuca) o 'frente' (mira hacia la cámara; gira -1/1 vuelve la cabeza)."""
    P = _P(cx, yh, s)
    det = s > 70
    out = []
    if tipo == 'mujer':
        d = contorno_mujer(P, -1.0 if de == 'frente' else -0.45)
        out.append(f'<path d="{d}" fill="#000" stroke="#000" stroke-width="{f(sw)}" stroke-linejoin="round"/>')
        if de == 'frente':
            hx, hy, rx, ry = cabeza(P, s, 0.24)
            hx += gira * 0.03 * s
            out.append(f'<ellipse cx="{f(hx)}" cy="{f(hy)}" rx="{f(rx * (0.62 if gira else 0.78))}" ry="{f(ry * 0.82)}" '
                       f'fill="{c("piel")}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
            out.append(f'<ellipse cx="{f(hx)}" cy="{f(hy + ry * 0.45)}" rx="{f(rx * (0.62 if gira else 0.78))}" ry="{f(ry * 0.3)}" '
                       f'fill="{c("piel-sombra")}" opacity="0.6"/>')
        if det:
            out.append(recortar(d, f'<path d="M{P(0.01, 0.1)} Q{P(0.03, -0.15)} {P(0.0, -0.55)}" stroke="#fff" '
                                   f'stroke-width="{f(sw * 0.6)}" fill="none" opacity="0.5"/>'))
        return ''.join(out)
    # hombre: ruana de lana y la cabeza descubierta (el sombrero en la mano, en misa) [P]
    lana = rnd.choice(['lana-parda', 'lana-gris', 'lana-cruda', 'lana-parda'])
    if de == 'frente':
        # de frente, bajo la ruana asoman el pantalón de dril y las alpargatas hasta el suelo
        out.append(f'<path d="M{P(-0.2, -0.5)} L{P(0.2, -0.5)} L{P(0.19, -1.0)} L{P(-0.19, -1.0)} Z" fill="{c("blanco-tela")}" '
                   f'stroke="#000" stroke-width="{f(sw * 0.7)}"/><path d="M{P(-0.2, -0.5)} L{P(0.2, -0.5)} L{P(0.19, -1.0)} L{P(-0.19, -1.0)} Z" {SOMBRA_HONDA}/>'
                   f'<path d="M{P(0, -0.55)} L{P(0, -1.0)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
    d = contorno_ruana(P, -0.62 if de == 'frente' else -0.45)
    out.append(f'<path d="{d}" fill="{c(lana)}" stroke="#000" stroke-width="{f(sw)}" stroke-linejoin="round"/>')
    if det:
        linea = '#fff' if lana != 'lana-cruda' else '#000'
        out.append(recortar(d, f'<path d="M{P(-0.36, -0.5)} Q{P(0, -0.44)} {P(0.36, -0.5)}" stroke="{linea}" '
                               f'stroke-width="{f(sw * 0.5)}" fill="none" opacity="0.6"/>'))
    out.append(f'<path d="M{P(-0.05, 0.13)} L{P(0.05, 0.13)} L{P(0.06, 0.0)} L{P(-0.06, 0.0)} Z" fill="{c("piel-sombra")}"/>')
    hx, hy, rx, ry = cabeza(P, s)
    if de == 'frente':
        hx += gira * 0.025 * s
        out.append(f'<ellipse cx="{f(hx)}" cy="{f(hy)}" rx="{f(rx * (0.82 if gira else 1))}" ry="{f(ry)}" fill="{c("piel")}" '
                   f'stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
        # pelo: casquete arriba
        out.append(f'<path d="M{f(hx - rx)},{f(hy - ry * 0.15)} Q{f(hx - rx)},{f(hy - ry * 1.15)} {f(hx)},{f(hy - ry * 1.1)} '
                   f'Q{f(hx + rx)},{f(hy - ry * 1.15)} {f(hx + rx)},{f(hy - ry * 0.15)} Q{f(hx)},{f(hy - ry * 0.55)} {f(hx - rx)},{f(hy - ry * 0.15)} Z" '
                   f'fill="{c("pano-oscuro")}"/>')
    else:
        out.append(f'<ellipse cx="{f(hx)}" cy="{f(hy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{c("pano-oscuro")}" '
                   f'stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
        if det:
            for sx in (-1, 1):
                out.append(f'<ellipse cx="{f(hx + sx * rx * 0.98)}" cy="{f(hy + ry * 0.1)}" rx="{f(rx * 0.16)}" ry="{f(ry * 0.24)}" '
                           f'fill="{c("piel")}" stroke="#000" stroke-width="{f(sw * 0.4)}"/>')
    return ''.join(out)


def provisional(d, nombre, sw):
    """Figura provisional (doc 03: lo que no tiene hoja no se dibuja como final): silueta gris con
    borde de tinta discontinuo."""
    return (f'<g data-p="figura provisional: {nombre}">'
            f'<path d="{d}" fill="{pa.PALETA["gris-claro"]}" stroke="#000" stroke-width="{f(sw)}" '
            f'stroke-dasharray="{f(sw * 3)} {f(sw * 2)}" stroke-linejoin="round"/></g>')


def elipse_d(cx, cy, rx, ry):
    return (f'M{f(cx - rx)},{f(cy)} A{f(rx)},{f(ry)} 0 1 0 {f(cx + rx)},{f(cy)} '
            f'A{f(rx)},{f(ry)} 0 1 0 {f(cx - rx)},{f(cy)} Z')


def sentado_prov(cx, yh, s, tipo, sw, nombre):
    P = _P(cx, yh, s)
    if tipo == 'mujer':
        d = contorno_mujer(P)
    else:
        hx, hy, rx, ry = cabeza(P, s)
        d = contorno_ruana(P) + ' ' + elipse_d(hx, hy, rx, ry)
    return provisional(d, nombre, sw)


def de_pie_espalda_prov(cx, base, s, tipo, sw, nombre, alto=1.6):
    """De pie y de espaldas: cabeza, hombros y falda larga (mujer) o ruana y pantalón (hombre)."""
    k = alto / 1.6
    P = _P(cx, base, s)
    yh = 1.36 * k
    if tipo == 'mujer':
        d = (f'M{P(-0.07, yh + 0.36)} Q{P(0, yh + 0.43)} {P(0.07, yh + 0.36)} Q{P(0.13, yh + 0.27)} {P(0.12, yh + 0.13)} '
             f'Q{P(0.16, yh + 0.03)} {P(0.25, yh - 0.03)} L{P(0.27, yh - 0.55)} L{P(0.3, 0.05)} L{P(-0.3, 0.05)} '
             f'L{P(-0.27, yh - 0.55)} L{P(-0.25, yh - 0.03)} Q{P(-0.16, yh + 0.03)} {P(-0.12, yh + 0.13)} '
             f'Q{P(-0.13, yh + 0.27)} {P(-0.07, yh + 0.36)} Z')
    else:
        hx, hy, rx, ry = cabeza(P, s, yh + 0.26)
        d = (f'M{P(-0.22, yh - 0.02)} Q{P(0, yh + 0.04)} {P(0.22, yh - 0.02)} Q{P(0.3, yh - 0.1)} {P(0.33, yh - 0.3)} '
             f'L{P(0.36, yh - 0.66)} L{P(0.16, yh - 0.66)} L{P(0.15, 0.03)} L{P(0.03, 0.03)} L{P(0.0, yh - 0.66)} '
             f'L{P(-0.03, 0.03)} L{P(-0.15, 0.03)} L{P(-0.16, yh - 0.66)} L{P(-0.36, yh - 0.66)} L{P(-0.33, yh - 0.3)} '
             f'Q{P(-0.3, yh - 0.1)} {P(-0.22, yh - 0.02)} Z ' + elipse_d(hx, hy, rx, ry))
    return provisional(d, nombre, sw)


def de_pie_perfil_prov(x, base, s, tipo, sw, nombre, alto=1.6, paso=0.22):
    """De pie y de perfil, caminando hacia la derecha: zancada corta bajo la falda o la ruana."""
    k = alto / 1.6
    P = _P(x, base, s)
    hx, hy = (float(t) for t in P(0.02, 1.49 * k).split(','))
    cab = elipse_d(hx, hy, 0.1 * s, 0.115 * s)
    if tipo == 'mujer':
        d = (f'M{P(-0.08, 1.4 * k)} Q{P(-0.2, 1.36 * k)} {P(-0.22, 1.2 * k)} L{P(-0.27, 0.85 * k)} '
             f'L{P(-0.3, 0.04)} L{P(0.32, 0.04)} L{P(0.24, 0.85 * k)} L{P(0.2, 1.22 * k)} Q{P(0.16, 1.37 * k)} {P(0.06, 1.4 * k)} Z '
             f'M{P(-0.12 - paso / 2, 0.06)} L{P(-0.02 - paso / 2, 0.06)} L{P(-0.04 - paso / 2, 0)} L{P(-0.16 - paso / 2, 0)} Z '
             f'M{P(0.08 + paso / 2, 0.06)} L{P(0.2 + paso / 2, 0.06)} L{P(0.24 + paso / 2, 0)} L{P(0.08 + paso / 2, 0)} Z')
    else:
        d = (f'M{P(-0.08, 1.4 * k)} Q{P(-0.24, 1.36 * k)} {P(-0.3, 1.18 * k)} L{P(-0.36, 0.78 * k)} '
             f'L{P(0.4, 0.8 * k)} L{P(0.24, 1.22 * k)} Q{P(0.18, 1.37 * k)} {P(0.06, 1.4 * k)} Z '
             f'M{P(-0.08, 0.8 * k)} L{P(-0.06 - paso, 0.0)} L{P(0.06 - paso, 0.0)} L{P(0.06, 0.6 * k)} '
             f'L{P(0.1 + paso, 0.0)} L{P(0.24 + paso, 0.0)} L{P(0.14, 0.8 * k)} Z')
    return provisional(d + ' ' + cab, nombre, sw)


# ============================================ viñeta 1 ============================================

def presbiterio(v, rnd, zt, zf):
    """Lo que se ve por el arco toral: el piso alzado, el muro del fondo, el retablo y el altar con
    sus velas y flores de papel (paleta: cinta-amarilla y cinta-rosa) [P]."""
    A, out = ANCHO, ['<g data-p="presbiterio: retablo de madera (dorado o policromado por verificar), altar con mantel, velas y flores de papel">']
    out.append(plano(v, seccion(zf), c('cal'), SOMBRA_SUAVE))
    out.append(plano(v, [(-A, 0.45, zt), (A, 0.45, zt), (A, 0.45, zf), (-A, 0.45, zf)], c('teja', 0.55), SOMBRA))
    # ventana alta del presbiterio, a la derecha: su luz cae sobre el retablo
    zr = zf - 0.15
    out.append(plano(v, [(-2.5, 0.45, zr), (-2.5, 6.0, zr), (2.5, 6.0, zr), (2.5, 0.45, zr)], c('madera', 0.95), SOMBRA, trazo(zr)))
    # ático de medio punto
    ax, ay = v.p(0, 6.0, zr)
    ra = 1.5 * v.esc(zr)
    out.append(f'<path d="M{f(ax - ra)},{f(ay)} A{f(ra)},{f(ra)} 0 0 1 {f(ax + ra)},{f(ay)} Z" fill="{c("madera", 0.95)}" '
               f'stroke="#000" stroke-width="{f(trazo(zr))}"/><path d="M{f(ax - ra)},{f(ay)} A{f(ra)},{f(ra)} 0 0 1 {f(ax + ra)},{f(ay)} Z" {SOMBRA}/>')
    # calles, cuerpos y columnas
    for y in (2.6, 4.5):
        out.append(plano(v, [(-2.5, y, zr), (2.5, y, zr), (2.5, y + 0.22, zr), (-2.5, y + 0.22, zr)], c('madera', 0.8), SOMBRA_FUERTE, trazo(zr) * 0.6))
    for x in (-2.3, -0.85, 0.7, 2.15):
        out.append(plano(v, [(x, 0.6, zr), (x + 0.15, 0.6, zr), (x + 0.15, 6.0, zr), (x, 6.0, zr)], c('madera', 0.75), SOMBRA_SUAVE, trazo(zr) * 0.5))
    # hornacinas con sus imágenes, en silueta y sin rasgos
    for x0, x1, y0, y1 in ((-0.55, 0.55, 2.85, 4.35), (-1.95, -1.25, 2.85, 4.2), (1.25, 1.95, 2.85, 4.2), (-0.45, 0.45, 4.8, 5.9)):
        (ax0, ay1), (ax1, ay0) = v.p(x0, y1, zr), v.p(x1, y0, zr)
        r_ = (ax1 - ax0) / 2
        d = f'M{f(ax0)},{f(ay0)} L{f(ax0)},{f(ay1 + r_)} A{f(r_)},{f(r_)} 0 0 1 {f(ax1)},{f(ay1 + r_)} L{f(ax1)},{f(ay0)} Z'
        out.append(f'<path d="{d}" fill="#000" fill-opacity="0.55" stroke="#000" stroke-width="{f(trazo(zr) * 0.5)}"/>')
        mx, sx = (ax0 + ax1) / 2, (ax1 - ax0)
        out.append(f'<path d="M{f(mx - sx * 0.18)},{f(ay0)} L{f(mx - sx * 0.12)},{f(ay1 + sx * 0.75)} L{f(mx + sx * 0.12)},{f(ay1 + sx * 0.75)} '
                   f'L{f(mx + sx * 0.18)},{f(ay0)} Z" fill="{c("cal", 0.9)}"/><circle cx="{f(mx)}" cy="{f(ay1 + sx * 0.62)}" r="{f(sx * 0.12)}" fill="{c("cal", 0.9)}"/>')
    # altar con mantel, crucifijo y velas
    za = zf - 1.3
    out.append(plano(v, [(-1.3, 1.45, za), (1.3, 1.45, za), (1.3, 1.45, za + 0.7), (-1.3, 1.45, za + 0.7)], c('blanco-tela'), SOMBRA_SUAVE))
    out.append(plano(v, [(-1.3, 0.45, za), (1.3, 0.45, za), (1.3, 1.45, za), (-1.3, 1.45, za)], c('blanco-tela'), None, trazo(za) * 0.6))
    out.append(plano(v, [(-1.3, 0.45, za), (1.3, 0.45, za), (1.3, 1.25, za), (-1.3, 1.25, za)], c('madera', 0.8), SOMBRA_SUAVE))
    s = v.esc(za)
    cx, cy = v.p(0, 1.45, za + 0.35)
    out.append(f'<path d="M{f(cx)},{f(cy)} L{f(cx)},{f(cy - 0.95 * s)} M{f(cx - 0.22 * s)},{f(cy - 0.72 * s)} L{f(cx + 0.22 * s)},{f(cy - 0.72 * s)}" '
               f'stroke="#000" stroke-width="{f(max(1.2, 0.05 * s))}"/>')
    for x in (-1.1, -0.75, -0.4, 0.4, 0.75, 1.1):
        bx, by = v.p(x, 1.45, za + 0.35)
        alto = (0.62 - abs(x) * 0.12) * s
        out.append(f'<path d="M{f(bx)},{f(by)} L{f(bx)},{f(by - alto)}" stroke="{c("blanco-tela")}" stroke-width="{f(max(1.5, 0.05 * s))}"/>'
                   f'<path d="M{f(bx)},{f(by)} L{f(bx)},{f(by - alto)}" stroke="#000" stroke-width="{f(max(1.5, 0.05 * s))}" stroke-opacity="0.3"/>'
                   f'<ellipse cx="{f(bx)}" cy="{f(by - alto - 0.05 * s)}" rx="{f(0.03 * s)}" ry="{f(0.06 * s)}" fill="{c("llama")}"/>'
                   f'<ellipse cx="{f(bx)}" cy="{f(by - alto - 0.045 * s)}" rx="{f(0.015 * s)}" ry="{f(0.03 * s)}" fill="{c("llama-nucleo")}"/>')
    for x in (-0.95, 0.95):
        bx, by = v.p(x, 1.45, za + 0.35)
        for k in range(5):
            col = c('cinta-amarilla') if k % 2 else c('cinta-rosa')
            out.append(f'<circle cx="{f(bx + rnd.uniform(-0.09, 0.09) * s)}" cy="{f(by - rnd.uniform(0.12, 0.3) * s)}" r="{f(0.05 * s)}" '
                       f'fill="{col}" stroke="#000" stroke-width="0.6"/>')
    out.append('</g>')
    return ''.join(out)


def arco_toral(v, zt):
    """Muro del arco toral: el corte de la nave con el vano de medio punto; el intradós en sombra."""
    r, y0, grueso = 2.5, 4.6, 0.8
    fuera = camino([v.p(*pt) for pt in seccion(zt)])
    vano = camino(arco_en(v, zt, r, y0))
    out = [f'<path d="{fuera} {vano}" fill="{c("cal")}" fill-rule="evenodd" stroke="#000" stroke-width="{f(trazo(zt))}"/>',
           f'<path d="{fuera} {vano}" fill-rule="evenodd" {SOMBRA_SUAVE}/>']
    cerca, lejos = arco_en(v, zt, r, y0)[1:-1], arco_en(v, zt + grueso, r, y0)[1:-1]
    out.append(f'<path d="{camino(cerca + list(reversed(lejos)))}" fill="{c("cal")}"/>'
               f'<path d="{camino(cerca + list(reversed(lejos)))}" {SOMBRA_FUERTE}/>'
               f'<path d="{camino(cerca, False)}" fill="none" stroke="#000" stroke-width="{f(trazo(zt))}"/>')
    # gradas del presbiterio
    for k, z in enumerate((zt, zt - 0.3, zt - 0.6)):
        y1 = 0.45 - 0.15 * k
        out.append(plano(v, [(-2.4, y1, z), (2.4, y1, z), (2.4, y1, z + 0.3), (-2.4, y1, z + 0.3)], c('piedra', 0.8), None, trazo(z) * 0.5))
        out.append(plano(v, [(-2.4, y1 - 0.15, z), (2.4, y1 - 0.15, z), (2.4, y1, z), (-2.4, y1, z)], c('piedra', 0.8), SOMBRA, trazo(z) * 0.5))
    return ''.join(out)


def ventana_derecha(v, z, piso_d):
    """Ventana alta del muro derecho con el sol que entra en diagonal y cae en el piso (aguada plana
    de luz, sin degradado)."""
    A = ANCHO
    esquinas = [(A, 4.6, z - 0.5), (A, 6.2, z - 0.5), (A, 6.2, z + 0.5), (A, 4.6, z + 0.5)]
    out = [plano(v, esquinas, '#fff', None, trazo(z))]
    out.append(f'<path d="{v.linea((A, 5.4, z - 0.5), (A, 5.4, z + 0.5))} {v.linea((A, 4.6, z), (A, 6.2, z))}" '
               f'stroke="{c("madera")}" stroke-width="{f(trazo(z) * 1.2)}"/>')
    # rayo: dirección del sol (-1, -1.1, 0.35) por metro de caída
    caida = [(x - y / 1.1, 0, zz + 0.35 * y / 1.1) for x, y, zz in esquinas]
    charco = v.d(*caida)
    hull = convexa([v.p(*q) for q in esquinas + caida])
    out.append(f'<path d="{camino(hull)}" {RESPLANDOR}/>')
    out.append(recortar(piso_d, f'<path d="{charco}" {LUZ}/>'))
    return ''.join(out)


def pulpito(v, sw_base=2.4):
    """Púlpito de madera sobre el muro izquierdo, con copa, respaldo, tornavoz y escalera [P]."""
    A = ANCHO
    z0, z1, xf = 7.0, 8.0, -2.7
    sw = trazo(7.5, sw_base)
    out = ['<g data-p="púlpito: copa de madera con tornavoz y escalera; forma y talla por verificar">']
    # escalera hacia el presbiterio
    out.append(plano(v, [(xf - 0.05, 2.0, z1), (xf - 0.05, 2.15, z1), (xf - 0.05, 0.15, z1 + 2.3), (xf - 0.05, 0.0, z1 + 2.3)], c('madera', 0.9), SOMBRA, sw * 0.6))
    out.append(f'<path d="{v.linea((xf - 0.05, 3.05, z1), (xf - 0.05, 1.05, z1 + 2.3))}" stroke="#000" stroke-width="{f(sw * 0.9)}"/>')
    for k in range(1, 5):
        t = k / 5
        a = (xf - 0.05, 3.05 - 2.0 * t, z1 + 2.3 * t)
        b = (xf - 0.05, 2.1 - 2.0 * t, z1 + 2.3 * t)
        out.append(f'<path d="{v.linea(a, b)}" stroke="#000" stroke-width="{f(sw * 0.45)}"/>')
    # pie
    out.append(plano(v, [(-3.38, 0, 7.5), (-3.12, 0, 7.5), (-3.12, 1.6, 7.5), (-3.38, 1.6, 7.5)], c('madera', 0.85), SOMBRA, sw * 0.6))
    # respaldo contra el muro
    out.append(plano(v, [(-A, 3.1, z0 + 0.1), (-A, 4.55, z0 + 0.1), (-A, 4.55, z1 - 0.1), (-A, 3.1, z1 - 0.1)], c('madera', 0.85), SOMBRA_FUERTE, sw * 0.6))
    # copa: fondo en pirámide, cara de frente (z0), cara hacia la nave (xf) y cornisa
    out.append(plano(v, [(-A, 2.0, z0), (xf, 2.0, z0), (-3.1, 1.6, 7.4), (-3.45, 1.6, 7.4)], c('madera', 0.9), SOMBRA_FUERTE, sw * 0.6))
    out.append(plano(v, [(xf, 2.0, z0), (xf, 2.0, z1), (-3.1, 1.6, 7.6), (-3.1, 1.6, 7.4)], c('madera', 0.9), SOMBRA_HONDA, sw * 0.6))
    out.append(plano(v, [(-A, 2.0, z0), (xf, 2.0, z0), (xf, 3.05, z0), (-A, 3.05, z0)], c('madera', 0.95), SOMBRA_SUAVE, sw))
    out.append(plano(v, [(xf, 2.0, z0), (xf, 2.0, z1), (xf, 3.05, z1), (xf, 3.05, z0)], c('madera', 0.95), SOMBRA, sw))
    for pts3 in ([(-3.6, 2.2, z0), (-2.9, 2.2, z0), (-2.9, 2.85, z0), (-3.6, 2.85, z0)],
                 [(xf, 2.2, z0 + 0.15), (xf, 2.2, z1 - 0.15), (xf, 2.85, z1 - 0.15), (xf, 2.85, z0 + 0.15)]):
        out.append(f'<path d="{v.d(*pts3)}" fill="none" stroke="#000" stroke-width="{f(sw * 0.45)}"/>')
    out.append(plano(v, [(-A, 3.05, z0 - 0.06), (xf + 0.06, 3.05, z0 - 0.06), (xf + 0.06, 3.18, z0 - 0.06), (-A, 3.18, z0 - 0.06)], c('madera', 0.8), SOMBRA, sw * 0.6))
    out.append(plano(v, [(xf + 0.06, 3.05, z0 - 0.06), (xf + 0.06, 3.05, z1 + 0.06), (xf + 0.06, 3.18, z1 + 0.06), (xf + 0.06, 3.18, z0 - 0.06)], c('madera', 0.8), SOMBRA_FUERTE, sw * 0.6))
    out.append('</g>')
    # el padre Evaristo, provisional: de medio cuerpo, el brazo alzado hacia la nave
    s = v.esc(7.5)
    hx, hy = v.p(-3.2, 3.78, 7.5)
    bx, by = v.p(-3.15, 3.1, 7.5)
    mx, my = v.p(-2.55, 4.15, 7.5)
    d = (f'M{f(bx - 0.2 * s)},{f(by)} L{f(bx - 0.17 * s)},{f(hy + 0.2 * s)} Q{f(bx)},{f(hy + 0.12 * s)} {f(bx + 0.17 * s)},{f(hy + 0.2 * s)} '
         f'L{f(mx)},{f(my)} L{f(mx + 0.08 * s)},{f(my + 0.1 * s)} L{f(bx + 0.2 * s)},{f(hy + 0.38 * s)} L{f(bx + 0.2 * s)},{f(by)} Z '
         + elipse_d(hx, hy, 0.1 * s, 0.12 * s))
    out.append(provisional(d, 'padre Evaristo Rincón (doc 01), sin hoja de personaje', max(1.0, sw * 0.6)))
    # tornavoz: se le ve la panza desde abajo
    out.append(f'<g data-p="tornavoz del púlpito, forma por verificar">')
    out.append(plano(v, [(-A, 4.55, z0 - 0.15), (-2.55, 4.55, z0 - 0.15), (-2.55, 4.55, z1 + 0.15), (-A, 4.55, z1 + 0.15)], c('madera', 0.9), SOMBRA_HONDA, sw * 0.7))
    out.append(plano(v, [(-A, 4.55, z0 - 0.15), (-2.55, 4.55, z0 - 0.15), (-2.55, 4.9, z0 - 0.15), (-A, 4.9, z0 - 0.15)], c('madera', 0.9), SOMBRA_SUAVE, sw))
    out.append(plano(v, [(-2.55, 4.55, z0 - 0.15), (-2.55, 4.55, z1 + 0.15), (-2.55, 4.9, z1 + 0.15), (-2.55, 4.9, z0 - 0.15)], c('madera', 0.9), SOMBRA, sw))
    tx, ty = v.p(-3.15, 4.9, 7.5)
    out.append(f'<path d="M{f(tx - 0.12 * s)},{f(ty)} Q{f(tx)},{f(ty - 0.35 * s)} {f(tx + 0.12 * s)},{f(ty)} Z M{f(tx)},{f(ty - 0.3 * s)} L{f(tx)},{f(ty - 0.6 * s)} '
               f'M{f(tx - 0.1 * s)},{f(ty - 0.5 * s)} L{f(tx + 0.1 * s)},{f(ty - 0.5 * s)}" fill="{c("madera", 0.9)}" stroke="#000" stroke-width="{f(sw * 0.7)}"/>')
    out.append('</g>')
    return ''.join(out)


def bancas_de_espaldas(v, rnd, filas, provisionales=None):
    """Filas de bancas con los fieles sentados de espaldas, de la del fondo a la más cercana: cada
    banca tapa de la cintura para abajo a los de su fila. provisionales: {(fila, lado, puesto): (tipo, nombre)}."""
    provisionales = provisionales or {}
    out = []
    for i, z in enumerate(filas):
        sw = trazo(z) * 0.7
        for lado in (-1, 1):
            for k in range(4):
                x = lado * (PASILLO + 0.32 + 0.58 * k)
                cx, yh = v.p(x, 1.0, z)
                if (i, lado, k) in provisionales:
                    tipo, nombre = provisionales[(i, lado, k)]
                    out.append(sentado_prov(cx, yh, v.esc(z), tipo, max(1.2, sw * 1.3), nombre))
                    continue
                if rnd.random() < 0.18:
                    continue
                out.append(fiel(cx, yh, v.esc(z), 'mujer' if rnd.random() < 0.6 else 'hombre', sw, rnd))
            zr = z - 0.22
            x0, x1 = sorted((lado * PASILLO, lado * BANCA))
            out.append(plano(v, [(x0, 0.52, zr), (x1, 0.52, zr), (x1, 0.92, zr), (x0, 0.92, zr)], c('madera', 0.85), SOMBRA, sw))
            out.append(f'<path d="{v.linea((x0, 0.92, zr), (x1, 0.92, zr))}" stroke="#000" stroke-width="{f(sw * 1.4)}"/>')
            xp = lado * PASILLO
            out.append(plano(v, [(xp, 0, z - 0.3), (xp, 0.95, z - 0.3), (xp, 0.95, z + 0.28), (xp, 0, z + 0.28)], c('madera', 0.9), SOMBRA_SUAVE, sw))
    return ''.join(out)


def caja_nave(v, zc, zf):
    """Techo de par y nudillo, muros y piso de la nave (el izquierdo en sombra; la luz entra por la derecha)."""
    A = ANCHO
    out = []
    for pts3 in ([(-A, MURO, zc), (-XN, NUDILLO, zc), (-XN, NUDILLO, zf), (-A, MURO, zf)],
                 [(-XN, NUDILLO, zc), (XN, NUDILLO, zc), (XN, NUDILLO, zf), (-XN, NUDILLO, zf)],
                 [(A, MURO, zc), (XN, NUDILLO, zc), (XN, NUDILLO, zf), (A, MURO, zf)]):
        out.append(plano(v, pts3, c('madera', 0.6), SOMBRA))
    out.append(plano(v, [(-A, 0, zc), (-A, MURO, zc), (-A, MURO, zf), (-A, 0, zf)], c('cal'), SOMBRA_FUERTE))
    out.append(plano(v, [(A, 0, zc), (A, MURO, zc), (A, MURO, zf), (A, 0, zf)], c('cal'), SOMBRA_SUAVE))
    # piso de barro cocido [P], apagado por la penumbra de la nave
    out.append(plano(v, [(-A, 0, zc), (A, 0, zc), (A, 0, zf), (-A, 0, zf)], c('teja', 0.45), SOMBRA_FUERTE))
    return ''.join(out)


def armadura(v, zc, zf, tirantes):
    """Pares de la armadura (pocas líneas: detalle limpio), soleras, nudillos y tirantes."""
    A, out = ANCHO, []
    z = 2.0
    while z < zf:
        out.append(f'<path d="{v.linea((-A, MURO, z), (-XN, NUDILLO, z))} {v.linea((-XN, NUDILLO, z), (XN, NUDILLO, z))} '
                   f'{v.linea((XN, NUDILLO, z), (A, MURO, z))}" stroke="#000" stroke-width="{f(trazo(z) * 0.4)}" fill="none" opacity="0.7"/>')
        z += 2.4
    for x, y in ((-A, MURO), (A, MURO), (-XN, NUDILLO), (XN, NUDILLO)):
        out.append(f'<path d="{v.linea((x, y, zc), (x, y, zf))}" stroke="#000" stroke-width="2"/>')
    for x in (-A, A):
        out.append(f'<path d="{v.linea((x, 0, zc), (x, 0, zf))}" stroke="#000" stroke-width="1.6"/>')
    for z in tirantes:
        out.append(plano(v, [(-A, 6.78, z), (A, 6.78, z), (A, 7.02, z), (-A, 7.02, z)], c('madera', 0.9), SOMBRA_FUERTE, trazo(z)))
    return ''.join(out)


def nave():
    """Viñeta 1, alta: la nave desde atrás, hacia el altar. La altura de la iglesia y el púlpito en
    el muro, por encima de los fieles; Rosalba y Efraín en la última fila."""
    nombre = 'misa-1-nave'
    _, _, W, H = PAGINA[nombre]
    v = Vista(W / 2, 650, 440, 1.55, W, H)
    rnd = random.Random(1946)
    zc, zt, zf = 0.5, 17.0, 22.0
    piso_d = v.d((-ANCHO, 0, zc), (ANCHO, 0, zc), (ANCHO, 0, zt), (-ANCHO, 0, zt))
    out = ['<g data-p="nave colonial de una nave: armadura de par y nudillo, muros encalados, piso de barro cocido y bancas; nada copiado de una iglesia real">']
    out.append(caja_nave(v, zc, zf))
    out.append(presbiterio(v, rnd, zt, zf))
    out.append(arco_toral(v, zt))
    out.append(armadura(v, zc, zt, (4.5, 7.5, 10.5, 13.5)))
    for z in (5.5, 11.0):
        out.append(ventana_derecha(v, z, piso_d))
    out.append(pulpito(v))
    filas = [15.6 - k for k in range(14)]
    out.append(bancas_de_espaldas(v, rnd, filas, {
        (len(filas) - 1, 1, 0): ('mujer', 'Rosalba (su figura la pone su área: personajes/rosalba.md)'),
        (len(filas) - 1, 1, 1): ('hombre', 'Efraín Insuasty (doc 01), sin hoja de personaje'),
    }))
    out.append('</g>')
    guardar(nombre, 'Viñeta 1: la nave y el púlpito', '\n'.join(out),
            notas='Perspectiva de un punto desde el fondo de la nave (ojo a 1,55 m); los fieles, sentados y de espaldas.')


# ============================================ viñeta 2 ============================================

def pulpito_de_cerca():
    """Viñeta 2, ancha: el padre en el púlpito, de medio cuerpo, con el tornavoz encima. A la
    derecha, muro encalado con la luz de la ventana de enfrente: el sitio del globo."""
    nombre = 'misa-2-pulpito'
    _, _, W, H = PAGINA[nombre]
    rnd = random.Random(1947)
    m, sw = 190, 3.0
    y_borde = 300                   # borde de la copa
    cx = 360                        # eje del púlpito
    out = ['<g data-p="púlpito y muro de la nave; talla, tornavoz y ventana por verificar">']
    out.append(pa.muro_cal(-10, W + 10, -10, H + 10, m, sw * 0.5, rnd, grietas=3, desconchados=2))
    out.append(f'<rect width="{W}" height="{H}" {SOMBRA}/>')
    # la luz de la ventana de enfrente cae en el muro, plana y sesgada
    out.append(f'<path d="M640,90 L860,40 L980,{H} L700,{H} Z" fill="#fff" fill-opacity="0.45"/>')
    # ventana alta de este muro, abocinada y con su reja de madera
    vx0, vx1, vy0, vy1 = 1030, 1120, 236, 416
    r_ = (vx1 - vx0) / 2
    hueco = f'M{vx0},{vy1} L{vx0},{vy0 + r_} A{f(r_)},{f(r_)} 0 0 1 {vx1},{vy0 + r_} L{vx1},{vy1} Z'
    derrame = f'M{vx0 - 30},{vy1 + 22} L{vx0 - 30},{vy0 + r_} A{f(r_ + 30)},{f(r_ + 30)} 0 0 1 {vx1 + 30},{vy0 + r_} L{vx1 + 30},{vy1 + 22} Z'
    out.append(f'<path d="{derrame}" fill="{c("cal")}" stroke="#000" stroke-width="{f(sw * 0.7)}"/><path d="{derrame}" {SOMBRA_SUAVE}/>')
    out.append(f'<path d="{hueco}" fill="#fff" stroke="#000" stroke-width="{f(sw * 0.8)}"/>')
    out.append(f'<path d="M{(vx0 + vx1) / 2},{vy0} L{(vx0 + vx1) / 2},{vy1} M{vx0},{vy0 + 95} L{vx1},{vy0 + 95}" stroke="{c("madera")}" stroke-width="{f(sw * 1.4)}"/>')
    out.append('</g>')
    # púlpito
    out.append('<g data-p="púlpito: copa poligonal de madera con tableros, respaldo y tornavoz; por verificar">')
    out.append(f'<rect x="{cx - 120}" y="40" width="240" height="{y_borde - 40}" fill="{c("madera", 0.85)}" stroke="#000" stroke-width="{f(sw)}"/>'
               f'<rect x="{cx - 120}" y="40" width="240" height="{y_borde - 40}" {SOMBRA_FUERTE}/>'
               f'<rect x="{cx - 92}" y="66" width="184" height="{y_borde - 92}" fill="none" stroke="#000" stroke-width="{f(sw * 0.5)}"/>'
               f'<rect x="{cx + 70}" y="40" width="50" height="{y_borde - 40}" {SOMBRA}/>')
    # copa: tres caras, la de frente más clara
    caras = [(cx - 215, cx - 160, SOMBRA_HONDA), (cx - 160, cx + 160, SOMBRA_SUAVE), (cx + 160, cx + 215, SOMBRA_FUERTE)]
    for x0, x1, som in caras:
        out.append(f'<path d="M{x0},{y_borde + 18} L{x1},{y_borde + 18} L{x1},{H + 10} L{x0},{H + 10} Z" fill="{c("madera", 0.95)}" stroke="#000" stroke-width="{f(sw)}"/>'
                   f'<path d="M{x0},{y_borde + 18} L{x1},{y_borde + 18} L{x1},{H + 10} L{x0},{H + 10} Z" {som}/>')
        out.append(f'<rect x="{x0 + (x1 - x0) * 0.16}" y="{y_borde + 48}" width="{(x1 - x0) * 0.68}" height="{H - y_borde - 30}" fill="none" '
                   f'stroke="#000" stroke-width="{f(sw * 0.55)}"/>')
    out.append(f'<path d="M{cx - 232},{y_borde} L{cx + 232},{y_borde} L{cx + 226},{y_borde + 20} L{cx - 226},{y_borde + 20} Z" fill="{c("madera", 0.8)}" '
               f'stroke="#000" stroke-width="{f(sw)}"/><path d="M{cx - 226},{y_borde + 12} L{cx + 226},{y_borde + 12} L{cx + 226},{y_borde + 20} L{cx - 226},{y_borde + 20} Z" {SOMBRA_FUERTE}/>')
    out.append('</g>')
    # el padre Evaristo, provisional: de medio cuerpo, el brazo alzado hacia la nave
    s = m
    hx, hy = cx - 10, y_borde - 0.72 * s
    d = (f'M{f(cx - 0.3 * s)},{y_borde} L{f(cx - 0.26 * s)},{f(hy + 0.2 * s)} Q{f(cx - 0.05 * s)},{f(hy + 0.1 * s)} {f(cx + 0.16 * s)},{f(hy + 0.2 * s)} '
         f'L{f(cx + 0.62 * s)},{f(hy - 0.36 * s)} L{f(cx + 0.7 * s)},{f(hy - 0.27 * s)} L{f(cx + 0.27 * s)},{f(hy + 0.42 * s)} L{f(cx + 0.3 * s)},{y_borde} Z '
         + elipse_d(hx, hy, 0.1 * s, 0.125 * s))
    out.append(provisional(d, 'padre Evaristo Rincón (doc 01), sin hoja de personaje', 2.4))
    # tornavoz, cortado arriba: la panza y el faldón con su lambrequín
    out.append('<g data-p="tornavoz por verificar">')
    out.append(f'<path d="M{cx - 250},-10 L{cx + 250},-10 L{cx + 250},34 L{cx - 250},34 Z" fill="{c("madera", 0.9)}" stroke="#000" stroke-width="{f(sw)}"/>')
    festón = f'M{cx - 250},34'
    for k in range(10):
        x0 = cx - 250 + k * 50
        festón += f' Q{x0 + 25},{60} {x0 + 50},34'
    out.append(f'<path d="{festón} Z" fill="{c("madera", 0.9)}" stroke="#000" stroke-width="{f(sw * 0.8)}"/><path d="{festón} Z" {SOMBRA}/>'
               f'<path d="M{cx - 250},-10 L{cx + 250},-10 L{cx + 250},34 L{cx - 250},34 Z" {SOMBRA_SUAVE}/>')
    out.append('</g>')
    guardar(nombre, 'Viñeta 2: el padre en el púlpito', '\n'.join(out),
            notas='Alzado a 190 px/m: la copa (cortada abajo), el respaldo y la panza del tornavoz (cortada arriba).')


# ============================================ viñeta 3 ============================================

def bancas_de_frente(v, rnd, filas, despues=None):
    """Filas vistas desde el altar hacia la puerta: los fieles miran a la cámara; algunos vuelven la
    cabeza hacia el pasillo. despues(z) dibuja lo que va entre filas (los que salen)."""
    out = []
    for z in filas:
        if despues:
            out.append(despues(z))
        sw = trazo(z) * 0.8
        for lado in (-1, 1):
            zr = z + 0.22
            x0, x1 = sorted((lado * PASILLO, lado * BANCA))
            out.append(plano(v, [(x0, 0.52, zr), (x1, 0.52, zr), (x1, 0.92, zr), (x0, 0.92, zr)], c('madera', 0.85), SOMBRA, sw))
            for k in range(4):
                if rnd.random() < 0.15:
                    continue
                x = lado * (PASILLO + 0.32 + 0.58 * k)
                cx, yh = v.p(x, 1.0, z)
                gira = -lado if (k == 0 and rnd.random() < 0.5) else 0
                out.append(fiel(cx, yh, v.esc(z), 'mujer' if rnd.random() < 0.6 else 'hombre', sw, rnd, de='frente', gira=gira))
            xp = lado * PASILLO
            out.append(plano(v, [(xp, 0, z - 0.28), (xp, 0.95, z - 0.28), (xp, 0.95, z + 0.3), (xp, 0, z + 0.3)], c('madera', 0.9), SOMBRA_SUAVE, sw))
    if despues:
        out.append(despues(0))
    return ''.join(out)


def salida():
    """Viñeta 3: desde el medio de la nave hacia la puerta mayor, abierta y encendida de sol. Bajo
    el coro, Rosalba y Efraín salen por el pasillo; los fieles siguen mirando al púlpito."""
    nombre = 'misa-3-salida'
    _, _, W, H = PAGINA[nombre]
    v = Vista(W / 2, 268, 400, 1.55, W, H)
    rnd = random.Random(1948)
    A, zc, zf = ANCHO, 0.5, 11.5
    out = ['<g data-p="pies de la nave: coro alto de madera sobre la puerta mayor, bancas; por verificar">']
    out.append(caja_nave(v, zc, zf))
    out.append(armadura(v, zc, zf, (4.0, 7.0, 10.0)))
    # muro de los pies con la puerta mayor (medio punto de 2,4 m como la portada de la plaza)
    fuera = camino([v.p(*pt) for pt in seccion(zf)])
    vano_q = arco_en(v, zf, 1.2, 3.0)
    out.append(f'<path d="{fuera} {camino(vano_q)}" fill="{c("cal")}" fill-rule="evenodd" stroke="#000" stroke-width="{f(trazo(zf))}"/>'
               f'<path d="{fuera} {camino(vano_q)}" fill-rule="evenodd" {SOMBRA_FUERTE}/>')
    out.append(f'<path d="{camino(vano_q)}" fill="#fff"/>')
    # afuera, quemado de sol: el borde del atrio y la cruz atrial
    gx, gy = v.p(0, 0.25, zf + 6)
    out.append(f'<path d="{camino(vano_q)}" fill="none" stroke="#000" stroke-width="{f(trazo(zf))}"/>')
    out.append(recortar(camino(vano_q), f'<path d="M0,{f(gy)} L{W},{f(gy)}" stroke="#000" stroke-width="1" opacity="0.35"/>'
                                         f'<path d="M{f(gx + 18)},{f(gy)} L{f(gx + 18)},{f(gy - 52)} M{f(gx + 9)},{f(gy - 40)} L{f(gx + 27)},{f(gy - 40)}" '
                                         f'stroke="#000" stroke-width="2" opacity="0.4"/>'))
    # hojas de la puerta abiertas hacia adentro
    for lado in (-1, 1):
        xh = lado * 1.2
        out.append(plano(v, [(xh, 0, zf), (xh, 3.6, zf), (xh, 3.6, zf - 1.15), (xh, 0, zf - 1.15)], c('madera', 0.9), SOMBRA_FUERTE, trazo(zf - 0.6)))
        out.append(f'<path d="{v.d((xh, 0.4, zf - 0.15), (xh, 1.6, zf - 0.15), (xh, 1.6, zf - 1.0), (xh, 0.4, zf - 1.0))} '
                   f'{v.d((xh, 2.0, zf - 0.15), (xh, 3.3, zf - 0.15), (xh, 3.3, zf - 1.0), (xh, 2.0, zf - 1.0))}" fill="none" stroke="#000" stroke-width="0.8"/>')
    # la luz de la puerta en el piso
    charco = v.d((-1.2, 0, zf), (1.2, 0, zf), (1.7, 0, zf - 3.4), (-1.0, 0, zf - 3.4))
    out.append(f'<path d="{charco}" fill="#fff" fill-opacity="0.4"/>')
    # coro alto: panza, frente, baranda y pies derechos
    zco = 8.6
    out.append(plano(v, [(-A, 4.8, zco), (A, 4.8, zco), (A, 4.8, zf), (-A, 4.8, zf)], c('madera', 0.85), SOMBRA_HONDA, trazo(zco)))
    for x in (-A + 0.6, -1.8, 1.8, A - 0.6):
        out.append(f'<path d="{v.linea((x, 4.8, zco), (x, 4.8, zf))}" stroke="#000" stroke-width="{f(trazo(zco) * 0.6)}"/>')
    out.append(plano(v, [(-A, 4.8, zco), (A, 4.8, zco), (A, 5.1, zco), (-A, 5.1, zco)], c('madera', 0.85), SOMBRA, trazo(zco)))
    baranda = []
    x = -A + 0.2
    while x < A:
        baranda.append(v.linea((x, 5.1, zco), (x, 5.95, zco)))
        x += 0.42
    out.append(f'<path d="{" ".join(baranda)}" stroke="#000" stroke-width="{f(trazo(zco) * 0.7)}"/>')
    out.append(plano(v, [(-A, 5.95, zco), (A, 5.95, zco), (A, 6.08, zco), (-A, 6.08, zco)], c('madera', 0.8), SOMBRA_FUERTE, trazo(zco)))
    for x in (-1.9, 1.9):
        out.append(plano(v, [(x - 0.11, 0, zco + 0.1), (x + 0.11, 0, zco + 0.1), (x + 0.11, 4.8, zco + 0.1), (x - 0.11, 4.8, zco + 0.1)], c('madera', 0.85), SOMBRA, trazo(zco)))
        out.append(plano(v, [(x - 0.4, 4.6, zco + 0.1), (x + 0.4, 4.6, zco + 0.1), (x + 0.4, 4.8, zco + 0.1), (x - 0.4, 4.8, zco + 0.1)], c('madera', 0.8), SOMBRA_FUERTE, trazo(zco) * 0.7))
    out.append('</g>')

    hecho = []

    def los_que_salen(z):
        # Rosalba y Efraín, provisionales, a contraluz en el pasillo: van detrás de las filas más
        # cercanas que 6,1 m y delante de las demás
        if hecho or z >= 6.1:
            return ''
        hecho.append(True)
        s = v.esc(6.1)
        r = []
        for x, tipo, nom, alto in ((-0.22, 'mujer', 'Rosalba (su figura la pone su área: personajes/rosalba.md)', 1.56),
                                   (0.32, 'hombre', 'Efraín Insuasty (doc 01), sin hoja de personaje', 1.68)):
            bx, by = v.p(x, 0, 6.1)
            r.append(de_pie_espalda_prov(bx, by, s, tipo, 1.5, nom, alto))
        return ''.join(r)
    out.append(bancas_de_frente(v, rnd, [7.6, 6.6, 5.6, 4.6, 3.6, 2.6], los_que_salen))
    guardar(nombre, 'Viñeta 3: la salida', '\n'.join(out),
            notas='Perspectiva de un punto hacia la puerta mayor (ojo a 1,55 m); los fieles, sentados y de frente.')


# ============================================ viñeta 4 ============================================

def atrio():
    """Viñeta 4: afuera, en el atrio, a pleno sol. La portada de piedra con la puerta abierta y
    oscura (allá adentro, las velas del altar); Rosalba y Efraín se alejan hacia la derecha."""
    nombre = 'misa-4-atrio'
    _, _, W, H = PAGINA[nombre]
    rnd = random.Random(1949)
    m, sw = 80, 2.2
    y_atrio = 432
    cx = 190
    out = ['<g data-p="portada de piedra y atrio: la misma iglesia de la plaza (puente_alto.py), por verificar">']
    out.append(pa.muro_cal(-10, W + 10, -10, y_atrio, m, sw * 0.6, rnd, grietas=3, desconchados=3))
    # pie de la torre a la derecha, un poco adelantado
    tx0 = cx + 4.4 * m
    out.append(f'<rect x="{f(tx0)}" y="-10" width="{f(W - tx0 + 10)}" height="{y_atrio + 10}" fill="{c("cal")}" stroke="#000" stroke-width="{f(sw)}"/>'
               f'<rect x="{f(tx0)}" y="-10" width="{f(0.3 * m)}" height="{y_atrio + 10}" {SOMBRA}/>')
    # portada: fondo de piedra, pilastras, arco de dovelas y la puerta abierta a la nave oscura
    pw, pr = 2.4 * m, 1.2 * m
    y_arr = y_atrio - 3.0 * m
    piedra = f'fill="{c("piedra", 0.8)}" stroke="#000"'
    out.append(f'<rect x="{f(cx - 2.6 * m)}" y="-10" width="{f(5.2 * m)}" height="{f(y_atrio + 10)}" fill="{c("piedra", 0.6)}"/>')
    for sx in (-1, 1):
        px = cx + sx * (pw / 2 + 0.55 * m) - 0.22 * m
        out.append(f'<rect x="{f(px)}" y="-10" width="{f(0.45 * m)}" height="{f(y_atrio + 10)}" {piedra} stroke-width="{f(sw * 0.8)}"/>'
                   f'<rect x="{f(px + 0.3 * m)}" y="-10" width="{f(0.15 * m)}" height="{f(y_atrio + 10)}" {SOMBRA_SUAVE}/>')
    arco = (f'M{f(cx - pw / 2)},{y_atrio} L{f(cx - pw / 2)},{f(y_arr)} A{f(pr)},{f(pr)} 0 0 1 {f(cx + pw / 2)},{f(y_arr)} '
            f'L{f(cx + pw / 2)},{y_atrio} Z')
    out.append(f'<path d="{arco}" fill="#000"/>')
    # al fondo de la nave, las velas del altar
    for k in range(6):
        vx = cx - 0.42 * m + k * 0.17 * m
        out.append(f'<ellipse cx="{f(vx)}" cy="{f(y_atrio - 1.05 * m)}" rx="1.6" ry="3" fill="{c("llama")}"/>')
    for hx in (cx - pw / 2, cx + pw / 2 - 0.35 * m):
        out.append(f'<rect x="{f(hx)}" y="{f(y_arr)}" width="{f(0.35 * m)}" height="{f(y_atrio - y_arr)}" fill="{c("madera")}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>'
                   f'<rect x="{f(hx)}" y="{f(y_arr)}" width="{f(0.35 * m)}" height="{f(y_atrio - y_arr)}" {SOMBRA}/>')
    ra = pr + 0.4 * m
    out.append(f'<path d="M{f(cx - pw / 2 - 0.4 * m)},{f(y_arr)} A{f(ra)},{f(ra)} 0 0 1 {f(cx + pw / 2 + 0.4 * m)},{f(y_arr)} '
               f'L{f(cx + pw / 2)},{f(y_arr)} A{f(pr)},{f(pr)} 0 0 0 {f(cx - pw / 2)},{f(y_arr)} Z" {piedra} stroke-width="{f(sw * 0.8)}"/>')
    dovelas = []
    for i in range(1, 9):
        a = math.pi * i / 9
        dovelas.append(f'M{f(cx - math.cos(a) * pr)},{f(y_arr - math.sin(a) * pr)} L{f(cx - math.cos(a) * ra)},{f(y_arr - math.sin(a) * ra)}')
    out.append(f'<path d="{" ".join(dovelas)}" stroke="#000" stroke-width="{f(sw * 0.5)}"/>')
    out.append(f'<path d="{arco}" fill="none" stroke="#000" stroke-width="{f(sw)}"/>')
    # jambas en sombra
    for sx in (-1, 1):
        jx = cx + sx * pw / 2
        out.append(f'<path d="M{f(jx)},{y_atrio} L{f(jx)},{f(y_arr)} L{f(jx + sx * 0.4 * m)},{f(y_arr)} L{f(jx + sx * 0.4 * m)},{y_atrio} Z" '
                   f'fill="{c("piedra", 0.8)}" stroke="#000" stroke-width="{f(sw * 0.6)}"/>')
    out.append('</g>')
    # atrio: losas de piedra, el borde y la primera grada
    out.append('<g data-p="atrio de piedra con gradas, por verificar">')
    out.append(f'<rect x="-10" y="{y_atrio}" width="{W + 20}" height="{H - y_atrio + 10}" fill="{c("piedra", 0.85)}" stroke="#000" stroke-width="{f(sw)}"/>')
    juntas = []
    for fila, y in enumerate((y_atrio + 16, y_atrio + 38)):
        x = (fila % 2) * 40 + rnd.uniform(0, 30)
        while x < W:
            juntas.append(f'M{f(x)},{f(y - 14 if fila == 0 else y - 20)} L{f(x - 6)},{f(y)}')
            x += rnd.uniform(70, 120)
        juntas.append(f'M-10,{f(y)} L{W + 10},{f(y)}')
    out.append(f'<path d="{" ".join(juntas)}" stroke="#000" stroke-width="{f(sw * 0.4)}" opacity="0.6"/>')
    out.append(f'<rect x="-10" y="{H - 14}" width="{W + 20}" height="24" fill="{c("piedra", 0.85)}" stroke="#000" stroke-width="{f(sw)}"/>'
               f'<rect x="-10" y="{H - 14}" width="{W + 20}" height="24" {SOMBRA_FUERTE}/>')
    out.append('</g>')
    # Rosalba y Efraín, provisionales, se alejan por el atrio; sus sombras cortas a la derecha
    for x, tipo, nom, alto in ((356, 'mujer', 'Rosalba (su figura la pone su área: personajes/rosalba.md)', 1.56),
                               (446, 'hombre', 'Efraín Insuasty (doc 01), sin hoja de personaje', 1.68)):
        base = y_atrio + 26
        out.append(f'<ellipse cx="{f(x + 0.35 * m)}" cy="{base}" rx="{f(0.45 * m)}" ry="5" {SOMBRA}/>')
        out.append(de_pie_perfil_prov(x, base, m, tipo, 1.6, nom, alto))
    guardar(nombre, 'Viñeta 4: el atrio', '\n'.join(out),
            notas='Alzado a 80 px/m de la portada de la plaza (puente_alto.py `iglesia`): la misma puerta, de cerca.')


# ======================================== página de revisión ========================================

def globo(x0, y0, w, h, cola, lineas, tam=30):
    """Globo de revisión (los de verdad son del DOM, doc 04 §4): blanco-tela con borde de tinta."""
    r = h / 2
    cx_, cy_ = cola
    bx = min(max(cx_, x0 + r), x0 + w - r)
    by = y0 + h if cy_ > y0 + h else y0
    d = (f'M{f(x0 + r)},{f(y0)} L{f(x0 + w - r)},{f(y0)} A{f(r)},{f(r)} 0 0 1 {f(x0 + w - r)},{f(y0 + h)} '
         f'L{f(x0 + r)},{f(y0 + h)} A{f(r)},{f(r)} 0 0 1 {f(x0 + r)},{f(y0)} Z')
    cola_d = f'M{f(bx - 18)},{f(by)} L{f(cx_)},{f(cy_)} L{f(bx + 18)},{f(by)} Z'
    out = [f'<path d="{cola_d}" fill="{pa.PALETA["blanco-tela"]}" stroke="{pa.TINTA}" stroke-width="3" stroke-linejoin="round"/>',
           f'<path d="{d}" fill="{pa.PALETA["blanco-tela"]}" stroke="{pa.TINTA}" stroke-width="3"/>',
           f'<path d="M{f(bx - 15)},{f(by)} L{f(bx + 15)},{f(by)}" stroke="{pa.PALETA["blanco-tela"]}" stroke-width="5"/>']
    alto = tam * 1.25
    y = y0 + h / 2 - alto * (len(lineas) - 1) / 2 + tam * 0.35
    for t in lineas:
        out.append(f'<text x="{f(x0 + w / 2)}" y="{f(y)}" font-family="Georgia, serif" font-size="{tam}" fill="{pa.TINTA}" '
                   f'text-anchor="middle">{t}</text>')
        y += alto
    return ''.join(out)


def pagina():
    """Compone la página para revisión: las cuatro viñetas, su marco y los dos globos (doc 02 §5,
    Prólogo b3, P29)."""
    cuerpo = []
    for nombre, (x, y, w, h) in PAGINA.items():
        svg = DIBUJOS[nombre]
        dentro = svg[svg.index('>', svg.index('<svg')) + 1:svg.rindex('</svg>')]
        cuerpo.append(f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{dentro}</svg>')
        cuerpo.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{pa.TINTA}" stroke-width="4"/>')
    cuerpo.append(globo(1130, 84, 690, 160, (1010, 236),
                        ['Recen por los que se fueron detrás', 'de los que no creen.', 'Yo también rezo por ellos.']))
    cuerpo.append(globo(1440, 578, 410, 110, (1452, 800), ['Pero no les abran', 'la puerta de noche.']))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">'
           f'<rect width="1920" height="1080" fill="{pa.PAPEL}"/>{"".join(cuerpo)}</svg>')
    os.makedirs(REVISION, exist_ok=True)
    ruta = os.path.join(REVISION, 'pagina-misa.svg')
    with open(ruta, 'w') as fh:
        fh.write(svg)
    print('ok página de revisión', os.path.relpath(ruta, os.path.join(AQUI, '..', '..')))


if __name__ == '__main__':
    pa.usar_acto('prologo')
    nave()
    pulpito_de_cerca()
    salida()
    atrio()
    pagina()
