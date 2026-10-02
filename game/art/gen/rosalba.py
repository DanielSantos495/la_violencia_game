"""Generador de los SVG de Rosalba (game/art/src/personajes/rosalba*.svg).

Fuente del dibujo: los SVG se generan desde aquí para que las partes compartidas (cabeza,
manos, alpargatas, falda) sean idénticas en todas las poses y variantes.
  python3 art/gen/rosalba.py            (desde game/; sin dependencias)
Si editas un SVG a mano, porta el cambio aquí o se perderá al regenerar.
Hoja de personaje y fuentes: planeacion/arte/tomo1/personajes/rosalba.md.
"""
import math, os, sys

OUTDIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'personajes')
R = '#c1121f'  # rojo liberal PROVISIONAL [P] (doc 03 §6.1)

def f(x): return f"{x:.1f}".rstrip('0').rstrip('.')

# ---------- helpers ----------
def fringes(points, step=2.6, length=16, sway=-2.5):
    """Flecos a lo largo de una polilínea: halo blanco + hebra negra."""
    segs = []
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        d = math.hypot(x2 - x1, y2 - y1)
        n = max(1, int(d / step))
        for i in range(n):
            t = i / n
            x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
            L = length + 3 * math.sin(i * 1.7 + x)  # largos desiguales
            segs.append((x, y, x + sway + 1.2 * math.sin(i * 2.3), y + L))
    halo = ''.join(f"M{f(a)},{f(b)} Q{f(a+0.4)},{f((b+d)/2)} {f(c)},{f(d)} " for a, b, c, d in segs)
    hebra = halo
    return (f'<path d="{halo}" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
            f'<path d="{hebra}" stroke="#000" stroke-width="0.9" fill="none" stroke-linecap="round"/>')

def flor(x, y, r=2.4, color='#fff'):
    petals = ''.join(f'<circle cx="{f(x + r*math.cos(a))}" cy="{f(y + r*math.sin(a))}" r="{f(r*0.48)}" fill="{color}"/>'
                     for a in [k * 2 * math.pi / 5 - math.pi / 2 for k in range(5)])
    return petals + f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r*0.42)}" fill="#000" stroke="{color}" stroke-width="0.6"/>'

def hoja(x, y, ang, color='#fff'):
    return f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="2.4" ry="0.9" transform="rotate({ang} {f(x)} {f(y)})" fill="{color}"/>'

def quad(p0, p1, p2, t):
    a = (1-t)**2; b = 2*(1-t)*t; c = t*t
    return (a*p0[0]+b*p1[0]+c*p2[0], a*p0[1]+b*p1[1]+c*p2[1])

# ---------- trenza ----------
def trenza(x0=134.0, y0=110.0, x1=124.0, y1=214.0, n=14):
    out = []
    h = (y1 - y0) / n
    for i in range(n):
        t = i / (n - 1)
        cx = x0 + (x1 - x0) * (i + 0.5) / n + 1.2 * math.sin(t * 3.0)
        cy = y0 + h * (i + 0.5)
        w = 11.5 - 4.5 * t
        dx = (1 if i % 2 == 0 else -1) * w * 0.17
        rot = 32 if i % 2 == 0 else -32
        rx, ry = w * 0.36, h * 1.05
        ex = cx + dx
        out.append(f'<g transform="rotate({rot} {f(ex)} {f(cy)})">'
                   f'<ellipse cx="{f(ex)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="#000" stroke="#fff" stroke-width="0.6"/>'
                   f'<path d="M{f(ex-rx*0.15)},{f(cy-ry*0.6)} Q{f(ex+rx*0.45)},{f(cy)} {f(ex-rx*0.1)},{f(cy+ry*0.6)}" stroke="#fff" stroke-width="0.7" fill="none"/>'
                   f'</g>')
    # moño de cinta al final (cintas rojas en las trenzas: Ocampo López, cap. 4)
    bx, by = x1 + 0.5, y1 + 3
    out.append(
        f'<g data-p="color de la cinta: rojo provisional; hex pendiente de la hoja de estilo">'
        f'<path d="M{f(bx)},{f(by)} C{f(bx-10)},{f(by-9)} {f(bx-14)},{f(by+2)} {f(bx-4)},{f(by+3)} Z" fill="{R}" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/>'
        f'<path d="M{f(bx)},{f(by)} C{f(bx+10)},{f(by-9)} {f(bx+14)},{f(by+2)} {f(bx+4)},{f(by+3)} Z" fill="{R}" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/>'
        f'<path d="M{f(bx-1)},{f(by+2)} C{f(bx-5)},{f(by+9)} {f(bx-6)},{f(by+14)} {f(bx-9)},{f(by+19)} L{f(bx-5)},{f(by+18)} C{f(bx-3)},{f(by+13)} {f(bx-1)},{f(by+8)} {f(bx+1)},{f(by+3)} Z" fill="{R}" stroke="#000" stroke-width="1.2" stroke-linejoin="round"/>'
        f'<path d="M{f(bx+1)},{f(by+2)} C{f(bx+4)},{f(by+8)} {f(bx+4)},{f(by+13)} {f(bx+7)},{f(by+17)} L{f(bx+3)},{f(by+18)} C{f(bx+1)},{f(by+13)} {f(bx)},{f(by+8)} {f(bx-1)},{f(by+3)} Z" fill="{R}" stroke="#000" stroke-width="1.2" stroke-linejoin="round"/>'
        f'<ellipse cx="{f(bx)}" cy="{f(by+1)}" rx="2.6" ry="2.2" fill="{R}" stroke="#000" stroke-width="1.3"/>'
        f'<path d="M{f(bx-9)},{f(by-1)} C{f(bx-7)},{f(by-4)} {f(bx-4)},{f(by-4)} {f(bx-3)},{f(by-1)} M{f(bx+9)},{f(by-1)} C{f(bx+7)},{f(by-4)} {f(bx+4)},{f(by-4)} {f(bx+3)},{f(by-1)}" stroke="#fff" stroke-width="0.8" fill="none"/>'
        f'</g>')
    # puntas del pelo que asoman bajo el moño
    out.append(f'<path d="M{f(bx-1)},{f(by+4)} C{f(bx-3)},{f(by+10)} {f(bx-2)},{f(by+14)} {f(bx-4)},{f(by+17)} M{f(bx)},{f(by+4)} C{f(bx)},{f(by+10)} {f(bx+1)},{f(by+14)} {f(bx)},{f(by+18)} M{f(bx+1)},{f(by+4)} C{f(bx+3)},{f(by+9)} {f(bx+3)},{f(by+12)} {f(bx+4)},{f(by+15)}" stroke="#000" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
    return ''.join(out)

# ---------- collar de abalorios ----------
def collar():
    out = []
    P0, P1, P2 = (150, 134), (157, 154), (172, 150)
    for i in range(13):
        x, y = quad(P0, P1, P2, i / 12)
        fill = '#000' if i % 2 == 0 else '#fff'
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="1.7" fill="{fill}" stroke="#000" stroke-width="0.8"/>')
    return ''.join(out)

# ---------- bordados de la pechera ----------
def pechera():
    out = []
    pts = [(165, 139), (168.5, 146), (170.5, 154), (171.2, 162), (170.6, 170), (169, 178)]
    for i, (x, y) in enumerate(pts):
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="0.9" fill="#000"/>')
        if i % 2 == 1:
            out.append(flor(x - 5, y + 1, 1.9, '#000').replace('fill="#000" stroke="#000"', 'fill="#fff" stroke="#000"'))
    out.append('<path d="M160,140 L163,144 L161,148 L164,152 L162,156 L165,160 L163,164 L166,168 L164,172 L166,176" stroke="#000" stroke-width="0.8" fill="none"/>')
    return ''.join(out)

# ---------- bordado del pañolón (blanco sobre negro) ----------
def bordado_panolon():
    out = ['<path d="M155,140 C152,165 154,200 160,228 M159,229 C150,229 143,228 138,232 C130,240 122,248 116,255" stroke="#fff" stroke-width="0.9" fill="none"/>']
    for (x, y) in [(154.5, 150), (154, 172), (156, 196), (159, 219), (146, 229), (131, 239), (121, 249)]:
        out.append(flor(x, y, 2.2))
        out.append(hoja(x + 3, y + 4, 40))
        out.append(hoja(x - 3, y - 4, 40))
    return ''.join(out)

# ---------- bandas del ruedo de la falda ----------
def xl(y): return 126 - (y - 230) * 32 / 202
def xr(y): return 166 + (y - 230) * 32 / 202
def banda(y1, y2, fill, extra=''):
    return (f'<path d="M{f(xl(y1))},{y1} Q146,{y1+3} {f(xr(y1))},{y1} L{f(xr(y2))},{y2} Q146,{y2+3} {f(xl(y2))},{y2} Z" fill="{fill}" stroke="#000" stroke-width="1.2"/>' + extra)

def zigzag(y1, y2):
    pts = []
    x = xl(y2) + 2
    up = True
    while x < xr(y2) - 2:
        pts.append(f"{f(x)},{f((y1+1.5) if up else (y2-1.5))}")
        x += 4; up = not up
    return f'<path d="M{" L".join(pts)}" stroke="#000" stroke-width="1" fill="none"/>'

def rombos(y1, y2):
    out = []
    x = xl(y2) + 5
    cy = (y1 + y2) / 2 + 1.5
    while x < xr(y2) - 4:
        out.append(f'<path d="M{f(x)},{f(cy-3.5)} L{f(x+3)},{f(cy)} L{f(x)},{f(cy+3.5)} L{f(x-3)},{f(cy)} Z" fill="#000"/>')
        out.append(f'<circle cx="{f(x+5)}" cy="{f(cy)}" r="0.9" fill="#000"/>')
        x += 10
    return ''.join(out)

# ---------- encaje de la enagua ----------
def enagua():
    # largo desigual: más larga atrás (a trechos desiguales)
    xs = [96 + i * 6.4 for i in range(16)]
    bottom = lambda x: 446 - (x - 96) / 100 * 6
    path = 'M97,426 L196,426 L197,' + f(bottom(197))
    for x in reversed(xs):
        b = bottom(x)
        path += f' Q{f(x+3.2)},{f(b+4)} {f(x)},{f(b)}'
    path += ' Z'
    holes = ''.join(f'<circle cx="{f(x+3.2)}" cy="{f(bottom(x)-2.5)}" r="1.1" fill="none" stroke="#000" stroke-width="0.7"/>' for x in xs[:-1])
    return (f'<path d="{path}" fill="#fff" stroke="#000" stroke-width="1.8" stroke-linejoin="round"/>' + holes +
            '<path d="M98,434 C130,437 165,435 196,432" stroke="#000" stroke-width="0.7" stroke-dasharray="1.5 1.5" fill="none"/>')

# ---------- alpargata ----------
def alpargata(dx, lejana=False):
    def P(x, y): return f"{f(x+dx)},{f(y)}"
    sw = 2.0 if lejana else 2.4
    s = []
    # canilla (asoma bajo la enagua)
    s.append(f'<path d="M{P(151,430)} L{P(163,430)} C{P(163,440)} {P(163,447)} {P(164,452)} L{P(152,452)} C{P(152,446)} {P(151,438)} {P(151,430)} Z" fill="#fff" stroke="#000" stroke-width="{sw}"/>')
    # suela de fique trenzado
    sole = f'M{P(145,466)} C{P(153,469.5)} {P(173,470.5)} {P(188,466)} C{P(190,468)} {P(189.5,472.5)} {P(186,474)} C{P(171,476.5)} {P(151,476)} {P(145,473)} C{P(143.5,471)} {P(143.5,468)} {P(145,466)} Z'
    s.append(f'<path d="{sole}" fill="#fff" stroke="#000" stroke-width="{sw}"/>')
    s.append(f'<path d="{sole}" fill="url(#fique-trenza)"/>')
    # talonera
    s.append(f'<path d="M{P(146,456)} C{P(144.5,460)} {P(144.5,464)} {P(146,467)} L{P(152,467)} C{P(151,463)} {P(151,459)} {P(152,455)} Z" fill="#fff" stroke="#000" stroke-width="{sw*0.8}"/>')
    # capellada de algodón, labrada
    cap = f'M{P(150,453)} C{P(154,448)} {P(163,447)} {P(168,451)} C{P(175,454)} {P(184,458)} {P(188,465)} C{P(186,467.5)} {P(183,468)} {P(180,468)} L{P(151,467)} C{P(150,462)} {P(149,457)} {P(150,453)} Z'
    s.append(f'<path d="{cap}" fill="#fff" stroke="#000" stroke-width="{sw}"/>')
    s.append(f'<path d="M{P(160,458)} L{P(163,461)} L{P(166,458)} L{P(169,461)} L{P(172,458)} L{P(175,461)} L{P(178,459)} M{P(165,464)} L{P(168,466)} L{P(171,464)} L{P(174,466)} L{P(177,464)} L{P(180,466)}" stroke="#000" stroke-width="0.8" fill="none"/>')
    s.append(f'<path d="M{P(152,456)} C{P(162,455)} {P(176,458)} {P(186,464)}" stroke="#000" stroke-width="0.8" stroke-dasharray="1.6 1.4" fill="none"/>')
    # galones negros cruzados al tobillo y nudo en rosa sobre el empeine
    s.append(f'<path d="M{P(150,449)} C{P(155,445.5)} {P(161,445.5)} {P(166,448.5)} M{P(150,445)} C{P(156,448.5)} {P(160,449.5)} {P(166,452)} M{P(147,457)} C{P(152,454)} {P(158,451)} {P(166,449)}" stroke="#000" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    rx, ry = 167 + dx, 449
    s.append(f'<circle cx="{f(rx)}" cy="{ry}" r="4.6" fill="#000"/>')
    s.append(f'<path d="M{f(rx-2.6)},{f(ry-0.5)} C{f(rx-2)},{f(ry-3)} {f(rx+2.4)},{f(ry-3)} {f(rx+2.4)},{f(ry)} C{f(rx+2.4)},{f(ry+2.4)} {f(rx-1)},{f(ry+2.6)} {f(rx-1.2)},{f(ry+0.4)} C{f(rx-1.2)},{f(ry-1)} {f(rx+0.8)},{f(ry-1.2)} {f(rx+0.8)},{f(ry+0.2)}" stroke="#fff" stroke-width="0.8" fill="none"/>')
    s.append(f'<path d="M{f(rx+1)},{f(ry+3.5)} C{f(rx+3)},{f(ry+6)} {f(rx+3)},{f(ry+8)} {f(rx+5)},{f(ry+10)} M{f(rx-1)},{f(ry+3.5)} C{f(rx-1)},{f(ry+6)} {f(rx-3)},{f(ry+8)} {f(rx-3)},{f(ry+10)}" stroke="#000" stroke-width="2" fill="none" stroke-linecap="round"/>')
    if lejana:
        s.append(f'<path d="{cap}" fill="url(#trama-fina)"/>')
        s.append(f'<path d="M{P(151,430)} L{P(163,430)} C{P(163,440)} {P(163,447)} {P(164,452)} L{P(152,452)} C{P(152,446)} {P(151,438)} {P(151,430)} Z" fill="url(#trama-fina)"/>')
    return ''.join(s)

# ---------- brazo + antebrazo ----------
def brazo(dx, lejano=False):
    def P(x, y): return f"{f(x+dx)},{f(y)}"
    sw = 2.2 if lejano else 2.7
    up = (f'<path d="M{P(138,138)} C{P(146,128)} {P(166,130)} {P(168,146)} C{P(169,160)} {P(167,182)} {P(166,200)} C{P(162,208)} {P(150,208)} {P(147,200)} C{P(144,180)} {P(141,160)} {P(138,138)} Z" fill="#fff" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>'
          f'<path d="M{P(146,134)} C{P(147,140)} {P(148,146)} {P(148,150)} M{P(153,132)} C{P(154,138)} {P(155,144)} {P(155,150)} M{P(160,134)} C{P(160,140)} {P(161,145)} {P(161,150)}" stroke="#000" stroke-width="0.9" fill="none"/>'
          f'<path d="M{P(142,160)} C{P(144,178)} {P(146,192)} {P(148,200)} L{P(152,201)} C{P(150,190)} {P(148,176)} {P(147,158)} Z" fill="url(#trama-fina)"/>')
    if lejano:
        up += f'<path d="M{P(138,138)} C{P(146,128)} {P(166,130)} {P(168,146)} C{P(169,160)} {P(167,182)} {P(166,200)} C{P(162,208)} {P(150,208)} {P(147,200)} C{P(144,180)} {P(141,160)} {P(138,138)} Z" fill="url(#trama-media)"/>'
    fore = (
        # manga larga hasta la muñeca
        f'<path d="M{P(148,196)} L{P(166,195)} C{P(168,218)} {P(170,236)} {P(171.5,250)} L{P(156.5,253)} C{P(155,238)} {P(151,218)} {P(148,196)} Z" fill="#fff" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>'
        f'<path d="M{P(150,206)} C{P(152,222)} {P(154,236)} {P(157,250)} L{P(161,249)} C{P(158,236)} {P(155,222)} {P(153,206)} Z" fill="url(#trama-fina)"/>'
        f'<path d="M{P(160,212)} C{P(162,224)} {P(164,236)} {P(165,246)}" stroke="#000" stroke-width="0.9" fill="none"/>'
        # puño bordado con abalorios
        f'<path d="M{P(155.5,249)} L{P(172,246.5)} L{P(173.5,257)} L{P(157,260)} Z" fill="#fff" stroke="#000" stroke-width="{sw*0.85}" stroke-linejoin="round"/>'
        f'<path d="M{P(157,254)} L{P(160,251.5)} L{P(163,254)} L{P(166,251)} L{P(169,253.5)} L{P(172,250.5)}" stroke="#000" stroke-width="0.8" fill="none"/>'
        + ''.join(f'<circle cx="{f(x+dx)}" cy="{f(y)}" r="0.8" fill="#000"/>' for x, y in [(158.5, 257.5), (162, 257), (165.5, 256.4), (169, 255.8), (172, 255.2)]) +
        # mano: dorso hacia el espectador, pulgar adelante separado del índice
        f'<path d="M{P(158,260)} C{P(156.5,266)} {P(156.6,272)} {P(157.4,277)} C{P(158,284)} {P(159.5,290)} {P(162,294.5)} C{P(163.6,297)} {P(166.4,297.2)} {P(167.6,295)} C{P(168.4,296.8)} {P(171,297)} {P(172,294.8)} C{P(173.4,292)} {P(172.6,287)} {P(171.2,283)} C{P(170.6,280.6)} {P(170.6,278.6)} {P(171.6,277.2)} C{P(173.4,277.6)} {P(176.4,277.8)} {P(178.6,276.4)} C{P(180.6,275)} {P(180.4,272.4)} {P(178.4,271)} C{P(176.4,269.6)} {P(174.4,268.2)} {P(172.6,264.6)} L{P(172,258)} Z" fill="#fff" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>'
        # borde interno del pulgar: deja ver el hueco entre pulgar e índice
        f'<path d="M{P(171.6,277.2)} C{P(171,275.4)} {P(171.4,273)} {P(172.6,271)}" stroke="#000" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
        f'<path d="M{P(178.3,272.3)} Q{P(179.6,273.4)} {P(179.4,275.2)}" stroke="#000" stroke-width="0.8" fill="none"/>'
        # dedos escalonados y línea de nudillos
        f'<path d="M{P(161,279)} C{P(161.6,286)} {P(163,291)} {P(165,295)} M{P(165.5,279)} C{P(166,286)} {P(167.4,291)} {P(168.8,295)}" stroke="#000" stroke-width="1" fill="none" stroke-linecap="round"/>'
        f'<path d="M{P(158,276.4)} C{P(162,274.8)} {P(166,275.2)} {P(170,277)}" stroke="#000" stroke-width="0.6" fill="none"/>'
        f'<path d="M{P(164.6,295.4)} Q{P(165.8,296.4)} {P(166.8,295.6)} M{P(169.4,295.6)} Q{P(170.6,296.6)} {P(171.6,295.4)}" stroke="#000" stroke-width="0.7" fill="none"/>'
        # tendones y sombra del canto
        f'<path d="M{P(161,263)} C{P(161.4,267)} {P(161.8,271)} {P(161.8,274)} M{P(165,262.5)} C{P(165.4,267)} {P(165.8,271)} {P(165.8,274)}" stroke="#000" stroke-width="0.55" fill="none"/>'
        f'<path d="M{P(157.4,266)} C{P(156.8,274)} {P(157.6,283)} {P(160,290)} L{P(161.4,289)} C{P(159.6,282)} {P(159,274)} {P(159.8,266)} Z" fill="url(#semitono)"/>'
    )
    if lejano:
        fore += (f'<path d="M{P(148,196)} L{P(166,195)} C{P(168,218)} {P(170,236)} {P(171.5,250)} L{P(156.5,253)} C{P(155,238)} {P(151,218)} {P(148,196)} Z" fill="url(#trama-media)"/>'
                 f'<path d="M{P(158,260)} C{P(156,266)} {P(156,272)} {P(157,277)} C{P(157,283)} {P(158,288)} {P(161,292)} C{P(163,295)} {P(167,295.5)} {P(169,293.5)} C{P(171,291)} {P(171.5,287)} {P(171,284)} C{P(173,282)} {P(175.5,280)} {P(177.5,277.5)} C{P(179.5,275)} {P(179,271.5)} {P(177,270)} C{P(175,268.5)} {P(173,267.5)} {P(172,264)} L{P(172,258)} Z" fill="url(#trama-fina)"/>')
    return up, fore

def piece(gid, pivot, body, comment='', extra=''):
    c = f'\n  <!-- {comment} -->' if comment else ''
    return f'{c}\n  <g id="{gid}" data-pieza="" data-pivote="{pivot}"{extra}>\n    {body}\n  </g>'

# ================= ensamblaje =================
defs = '''
  <defs>
    <pattern id="trama-fina" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="5" stroke="#000" stroke-width="0.8"/></pattern>
    <pattern id="trama-media" width="3.4" height="3.4" patternUnits="userSpaceOnUse" patternTransform="rotate(60)"><line x1="0" y1="0" x2="0" y2="3.4" stroke="#000" stroke-width="1.1"/></pattern>
    <pattern id="trama-cruzada" width="3.2" height="3.2" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="3.2" stroke="#000" stroke-width="1.1"/><line x1="0" y1="0" x2="3.2" y2="0" stroke="#000" stroke-width="1.1"/></pattern>
    <pattern id="trama-densa" width="2.6" height="2.6" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="2.6" stroke="#000" stroke-width="1.3"/><line x1="0" y1="0" x2="2.6" y2="0" stroke="#000" stroke-width="1.1"/></pattern>
    <pattern id="semitono" width="3.2" height="3.2" patternUnits="userSpaceOnUse"><circle cx="1.6" cy="1.6" r="0.75" fill="#000"/></pattern>
    <pattern id="trencilla" width="6" height="4" patternUnits="userSpaceOnUse"><path d="M0,1 L1.5,3 L3,1 L4.5,3 L6,1" stroke="#000" stroke-width="0.6" fill="none"/></pattern>
    <pattern id="lana-blanca" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)"><line x1="0" y1="0" x2="0" y2="4" stroke="#fff" stroke-width="0.5" stroke-opacity="0.85"/><line x1="0" y1="2" x2="1.6" y2="2" stroke="#fff" stroke-width="0.5"/></pattern>
    <pattern id="fique-trenza" width="4" height="3" patternUnits="userSpaceOnUse"><path d="M0,0 L2,1.5 L4,0 M0,1.5 L2,3 L4,1.5" stroke="#000" stroke-width="0.7" fill="none"/></pattern>
  </defs>'''

bi_up, bi_fore = brazo(-12, lejano=True)
bd_up, bd_fore = brazo(0)

cabeza = '''
    <!-- cuello -->
    <path d="M140,108 L161,118 C161,125 161,131 163,137 L137,137 C138,128 139,118 140,108 Z" fill="#fff" stroke="#000" stroke-width="2.4"/>
    <path d="M141,114 C142,124 141,131 140,136 L147,136 C146,129 146,121 148,116 Z" fill="url(#trama-fina)"/>
    <path d="M149,118 C153,124 157,130 159,136" stroke="#000" stroke-width="0.8" fill="none"/>
    <!-- rostro de perfil: frente, entrecejo, nariz recta con punta redonda, labios definidos, mentón firme -->
    <path d="M166,58 C169,62 171,68 172,74 C173,77 172,79 171,81 C174,86 178,90 180,93 C181.5,95.5 180,98 177,98.5 C175.5,98.8 174.5,99.5 174,100.5 C175,102 176.2,103.5 176,105 C175.6,106.2 174,106.6 173.2,107 C174.5,107.8 175.4,109 175,110.2 C174.6,111.2 173,111.5 172.4,112 C173.6,113.4 174.4,115.4 173.4,117.4 C172,119.6 168.5,120.6 164,120.8 C158,121 152,119 147,115 C138,108 128,96 126,80 C125,62 136,47 152,46 C159,46 164,50 166,58 Z" fill="#fff" stroke="#000" stroke-width="2.8" stroke-linejoin="round"/>
    <!-- sombra del ala del sombrero sobre la frente -->
    <path d="M154,60 C160,60 166,61 170,64 C169,67 166,68 160,67 C156,66 154,64 154,60 Z" fill="url(#trama-fina)"/>
    <!-- sombra bajo la mandíbula -->
    <path d="M150,116 C156,119 162,120.5 168,120.5 C163,123 155,122 150,119 Z" fill="url(#trama-media)"/>
    <!-- rubor de campo: tres trazos cortos en la mejilla -->
    <path d="M158,95 L156.5,99 M160.5,95.5 L159,99.5 M163,96 L161.5,100" stroke="#000" stroke-width="0.8" stroke-linecap="round"/>
    <path d="M155,90 C157,93 159,95 162,96" stroke="#000" stroke-width="0.7" fill="none"/>
    <!-- ojo -->
    <path id="ojo-der" d="M157.5,80.5 C160.5,78.2 164.5,78 168,79.6 C165.5,82.4 161.5,83.4 157.5,80.5 Z" fill="#fff" stroke="#000" stroke-width="0.9"/>
    <ellipse cx="164.4" cy="80.7" rx="2" ry="2.5" fill="#000"/>
    <circle cx="165.2" cy="79.8" r="0.65" fill="#fff"/>
    <path d="M156.2,80.6 C159.5,77.3 164.5,77 168.6,79.2 C169.4,78.6 170,77.8 170.3,77" stroke="#000" stroke-width="2" fill="none" stroke-linecap="round"/>
    <path d="M168.6,79.2 L171,78.6 M167.4,78.5 L169.4,77" stroke="#000" stroke-width="0.9" stroke-linecap="round"/>
    <path d="M158.4,76.6 C161.5,75.4 165,75.4 167.6,76.6" stroke="#000" stroke-width="0.8" fill="none"/>
    <path d="M159.5,82.8 C162,83.8 165,83.6 167.2,82.2" stroke="#000" stroke-width="0.6" fill="none"/>
    <!-- ceja: gruesa adentro, fina afuera, levemente fruncida -->
    <path id="ceja-der" d="M171.2,72.6 C166,69.4 159.5,69.6 154,72.8 C159.5,71.6 165,71.8 170.6,74.4 Z" fill="#000" stroke="#000" stroke-width="0.8" stroke-linejoin="round"/>
    <!-- nariz: ala y fosa -->
    <path d="M173.2,94.6 C175,92.4 178.2,92.8 178.6,95.6" stroke="#000" stroke-width="1.2" fill="none" stroke-linecap="round"/>
    <ellipse cx="176.2" cy="97.2" rx="1.3" ry="0.6" fill="#000"/>
    <path d="M171,88 C172.4,90.5 173.2,92 173.2,94.6" stroke="#000" stroke-width="0.6" fill="none"/>
    <!-- boca -->
    <path d="M173.3,107 L169,107.4" stroke="#000" stroke-width="1.5" stroke-linecap="round"/>
    <path d="M171.5,110.2 C172.6,110.8 173.8,110.6 174.4,110" stroke="#000" stroke-width="0.8" fill="none"/>
    <path d="M169,107.4 C168.2,106.6 168.4,105.8 169.2,105.4" stroke="#000" stroke-width="0.8" fill="none"/>
    <!-- pelo: raya al medio, peinado hacia atrás, recogido en trenzas -->
    <path d="M166,57 C160,48 146,44 134,50 C122,57 118,74 121,92 C123,103 129,110 137,113 L142,109 C138,105 136,100 137.5,96 C137,90 136,84 140,80.5 C143,78 147,77 150,75 C155,71 160,64 166,62 Z" fill="#000"/>
    <path d="M162,58 C152,58 142,64 136,74 M157,55 C146,59 135,70 130,86 M151,53 C140,59 129,74 127,94 M146,62 C140,70 136,80 134,92" stroke="#fff" stroke-width="0.8" fill="none" stroke-linecap="round"/>
    <path d="M150,75 C148,77 146.5,79 146.8,82" stroke="#000" stroke-width="1.1" fill="none" stroke-linecap="round"/>
    <!-- oreja: hélix, antihélix, trago, concha y lóbulo -->
    <path id="oreja-der" d="M146,83 C141,79.5 136.5,82.5 136.5,89 C136.5,95.5 139.5,100.8 144,100.8 C146.5,100.8 147.6,98.8 147,96.6 L147.6,92.4 C148.6,89.2 148.6,85.6 146,83 Z" fill="#fff" stroke="#000" stroke-width="1.8" stroke-linejoin="round"/>
    <path d="M144.6,84.6 C140.6,83.8 139.2,87.6 139.6,91.6 C139.9,94.2 141,96.4 142.6,97.4" stroke="#000" stroke-width="0.9" fill="none"/>
    <path d="M143.4,86.4 C141.8,88.6 142,91.6 143.6,94.2 M142.4,88.2 L144.4,87.2" stroke="#000" stroke-width="0.8" fill="none"/>
    <path d="M144.5,90 C146,90.2 146.6,91.4 146.4,92.8 C145.2,93.6 144,92.8 144.2,91.4 Z" fill="#000"/>
    <path d="M147.6,92.4 C146.8,93 146.6,94.4 147.2,95.2" stroke="#000" stroke-width="0.8" fill="none"/>
    <path d="M141.4,97.6 C142.4,99.2 143.6,99.8 145,99.6" stroke="#000" stroke-width="0.7" fill="none"/>'''

zarcillo = '''<path d="M143.6,100.6 C143.4,102 143.4,103 143.6,104" stroke="#000" stroke-width="0.9" fill="none"/>
    ''' + flor(143.6, 107, 2.4, '#000').replace('fill="#000" stroke="#000"', 'fill="#fff" stroke="#000"') + '''
    <path d="M143.6,109.8 C141.6,112 141.8,114.6 143.6,115.8 C145.4,114.6 145.6,112 143.6,109.8 Z" fill="#000"/>
    <circle cx="143" cy="113" r="0.5" fill="#fff"/>'''

sombrero = '''
    <!-- copa de caña: trencilla enrollada -->
    <path d="M128,58 C127,40 136,30 151,29 C166,29 174,38 172,58 Z" fill="#fff" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M128,58 C127,40 136,30 151,29 C166,29 174,38 172,58 Z" fill="url(#trencilla)"/>
    <path d="M131,46 C144,43.5 158,43.5 171,46 M130,40 C142,37 160,37 170.5,40 M134,34 C144,32 158,32 167,34" stroke="#000" stroke-width="0.9" fill="none"/>
    <path d="M128,58 C127.5,48 129,41 133,36 C131,44 131,51 132,58 Z" fill="url(#trama-media)"/>
    <!-- cinta negra con moño atrás -->
    <path d="M128.5,50 C142,47 158,47 171.5,50 L171.8,57 C158,54.5 142,54.5 128.4,57 Z" fill="#000"/>
    <path d="M129,53.4 C142,50.8 158,50.8 171.4,53.4" stroke="#fff" stroke-width="0.6" fill="none" stroke-dasharray="2 1.5"/>
    <path d="M129,52 C125,50.5 123.5,52.5 125,54.5 C126.5,55.5 128,55 129,54.5 M129,55 C127,57 126.5,59.5 127.5,61.5" stroke="#000" stroke-width="1.6" fill="none" stroke-linecap="round"/>
    <!-- ala -->
    <path d="M102,60 C120,53 180,51 200,57 C195,63 180,66 151,65 C128,65 110,66 102,60 Z" fill="#fff" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M102,60 C120,53 180,51 200,57 C195,63 180,66 151,65 C128,65 110,66 102,60 Z" fill="url(#trencilla)"/>
    <path d="M106,60.5 C128,57 172,55 196,57.5" stroke="#000" stroke-width="0.8" fill="none"/>
    <path d="M110,62.6 C132,65 176,64 196,59.6 C186,64.5 168,66.5 150,66.2 C132,66 118,66 110,62.6 Z" fill="#000"/>
    <!-- barbuquejo: cinta que baja por la mejilla y se ata bajo el mentón -->
    <path d="M148.5,64 C149,74 149.6,84 150.2,94 C151,104 155,113 161,118 C163.5,120 165.5,121 167,121.5" stroke="#000" stroke-width="2.2" fill="none" stroke-linecap="round"/>
    <path d="M148.5,64 C149,74 149.6,84 150.2,94 C151,104 155,113 161,118 C163.5,120 165.5,121 167,121.5" stroke="#fff" stroke-width="0.8" fill="none" stroke-linecap="round" stroke-dasharray="2.5 2"/>
    <path d="M166,121 C163,124 161,128 162,131 M167,122 C168,126 168,129 170,131" stroke="#000" stroke-width="1.8" fill="none" stroke-linecap="round"/>
    <circle cx="166.8" cy="121.6" r="1.8" fill="#000"/>'''

torso = '''
    <path d="M136,130 C150,126 163,128 167,136 C173,150 175,168 171,184 C168,200 166,216 165,232 L128,232 C126,210 123,188 125,164 C126,148 128,138 136,130 Z" fill="#fff" stroke="#000" stroke-width="2.8"/>
    <path d="M125,164 C125,190 126,212 128,231 L135,231 C132,208 131,186 132,160 Z" fill="url(#trama-fina)"/>
    <!-- escote redondo con festón -->
    <path d="M141,131 C148,136 157,137 163,134" stroke="#000" stroke-width="1.2" fill="none"/>
    <path d="M142,133.5 Q144,136 146,134.6 Q148,137 150,135.4 Q152,137.6 154,135.8 Q156,137.8 158,135.6 Q160,137.2 162,135" stroke="#000" stroke-width="0.7" fill="none"/>
    <!-- pechera bordada con abalorios -->
    ''' + pechera() + '''
    <!-- collar de abalorios (cuentas negras y blancas) -->
    ''' + collar()

falda = (
    '<path d="M126,230 L166,230 C172,280 186,360 198,432 Q146,438 94,432 C106,360 118,280 126,230 Z" fill="#fff" stroke="#000" stroke-width="3.2" stroke-linejoin="round"/>'
    '<path d="M126,230 L166,230 C172,280 186,360 198,432 Q146,438 94,432 C106,360 118,280 126,230 Z" fill="url(#trama-densa)"/>'
    '<path d="M126,230 C118,280 106,360 94,432 Q104,434 112,434.6 C114,360 120,290 132,232 Z" fill="#000"/>'
    # pliegues como reflejos blancos sobre la frisa oscura
    '<path d="M138,236 C134,300 126,360 120,392 M147,236 C146,300 143,360 140,392 M155,236 C158,300 162,360 164,392 M162,238 C169,300 177,350 184,392 M131,250 C125,300 116,350 108,392" stroke="#fff" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
    # cintas de colores en el ruedo (doc: "cintas con colores vistosos"): se traducen a tramas distintas
    + banda(394, 402, '#fff', zigzag(394, 402))
    + banda(406, 412, 'url(#trama-cruzada)')
    + banda(416, 428, '#fff', rombos(416, 428)) +
    '<path d="M126,232 L166,232" stroke="#000" stroke-width="1"/>'
    '<path d="M124,226 L168,226 L168.6,236 L123.4,236 Z" fill="#000"/>'
    '<path d="M126,231 L166,231" stroke="#fff" stroke-width="0.7" stroke-dasharray="3 2"/>'
)

panolon = (
    '<path d="M138,126 C147,123 157,127 161,135 C158,160 160,200 167,236 C158,238 148,236 140,233 C131,244 121,254 112,262 C110,230 112,180 121,142 C126,133 131,128 138,126 Z" fill="#000" stroke="#000" stroke-width="2.8" stroke-linejoin="round"/>'
    '<path d="M140,134 C134,170 126,215 120,252 M148,134 C146,170 144,205 142,230 M131,140 C124,180 118,215 115,250" stroke="#fff" stroke-width="0.9" fill="none" stroke-linecap="round" stroke-opacity="0.9"/>'
    + bordado_panolon()
    + fringes([(167, 236), (140, 233), (112, 262)])
)

# ======================= utilidades geométricas =======================
def rot_punto(x, y, ang, cx, cy):
    a = math.radians(ang)
    dx, dy = x - cx, y - cy
    return (cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a))

def tubo(p1, p2, r1, r2, extra='', sw=2.6):
    """Segmento de miembro con extremos redondeados (manga o brazo)."""
    (x1, y1), (x2, y2) = p1, p2
    L = math.hypot(x2 - x1, y2 - y1); dx, dy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = -dy, dx
    a1 = (x1 + nx * r1, y1 + ny * r1); a2 = (x2 + nx * r2, y2 + ny * r2)
    b2 = (x2 - nx * r2, y2 - ny * r2); b1 = (x1 - nx * r1, y1 - ny * r1)
    k = 1.3
    d = (f"M{f(a1[0])},{f(a1[1])} L{f(a2[0])},{f(a2[1])} "
         f"C{f(a2[0]+dx*r2*k)},{f(a2[1]+dy*r2*k)} {f(b2[0]+dx*r2*k)},{f(b2[1]+dy*r2*k)} {f(b2[0])},{f(b2[1])} "
         f"L{f(b1[0])},{f(b1[1])} C{f(b1[0]-dx*r1*k)},{f(b1[1]-dy*r1*k)} {f(a1[0]-dx*r1*k)},{f(a1[1]-dy*r1*k)} {f(a1[0])},{f(a1[1])} Z")
    return d

def punto_en(p1, p2, t, off=0.0):
    (x1, y1), (x2, y2) = p1, p2
    L = math.hypot(x2 - x1, y2 - y1); dx, dy = (x2 - x1) / L, (y2 - y1) / L
    return (x1 + (x2 - x1) * t - dy * off, y1 + (y2 - y1) * t + dx * off)

def zigzag_x(x1, x2, y1, y2):
    pts, x, up = [], x1 + 2, True
    while x < x2 - 2:
        pts.append(f"{f(x)},{f((y1+1.5) if up else (y2-1.5))}"); x += 4; up = not up
    return f'<path d="M{" L".join(pts)}" stroke="#000" stroke-width="1" fill="none"/>'

def rombos_x(x1, x2, y1, y2):
    out, x, cy = [], x1 + 5, (y1 + y2) / 2
    while x < x2 - 4:
        out.append(f'<path d="M{f(x)},{f(cy-3.5)} L{f(x+3)},{f(cy)} L{f(x)},{f(cy+3.5)} L{f(x-3)},{f(cy)} Z" fill="#000"/>')
        out.append(f'<circle cx="{f(x+5)}" cy="{f(cy)}" r="0.9" fill="#000"/>'); x += 10
    return ''.join(out)

def barro(puntos, semilla=3):
    """Salpicaduras de barro: manchas irregulares pequeñas (huida por la quebrada)."""
    out = []
    for i, (x, y) in enumerate(puntos):
        r = 0.8 + ((i * 7 + semilla) % 5) * 0.35
        out.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r*1.4)}" ry="{f(r)}" transform="rotate({(i*37)%180} {f(x)} {f(y)})" fill="#000"/>')
    return ''.join(out)

# ======================= piezas compartidas =======================
cabeza_monte = cabeza.replace('''    <!-- sombra del ala del sombrero sobre la frente -->
    <path d="M154,60 C160,60 166,61 170,64 C169,67 166,68 160,67 C156,66 154,64 154,60 Z" fill="url(#trama-fina)"/>
''', '').replace(
    '<path id="ceja-der" d="M171.2,72.6 C166,69.4 159.5,69.6 154,72.8 C159.5,71.6 165,71.8 170.6,74.4 Z"',
    '<path id="ceja-der" d="M171.4,70.8 C166.4,67 159.6,68.2 154,72.2 C159.6,70.4 165.4,69.8 170.8,72.6 Z"'
).replace('''    <!-- pelo: raya al medio''', '''    <!-- alerta: arruga de preocupación sobre la ceja -->
    <path d="M165,65.4 C167,65 169,65.4 170.4,66.4" stroke="#000" stroke-width="0.7" fill="none"/>
    <!-- pelo: raya al medio''').replace('''    <path d="M150,75 C148,77 146.5,79 146.8,82"''', '''    <!-- mechones sueltos: despeinada tras la noche de huida -->
    <path d="M140,50 C136,44 130,44 127,47 M131,58 C125,55 120,57 118,61 M124,78 C119,77 116,80 116,84" stroke="#000" stroke-width="1" fill="none" stroke-linecap="round"/>
    <path d="M150,75 C148,77 146.5,79 146.8,82"''')
assert cabeza_monte.count('arruga') == 1 and 'sombra del ala' not in cabeza_monte

torso_monte = torso.split('    <!-- collar de abalorios')[0]

barro_ruedo = barro([(104, 425), (112, 419), (121, 429), (133, 422), (147, 430), (160, 424), (171, 431), (183, 421), (193, 428), (100, 438), (126, 440), (152, 441), (178, 439)])
falda_monte = falda + barro_ruedo
enagua_monte = enagua() + '<path d="M97,437 C130,441 165,439 197,435 L197,442 C165,446 130,448 97,444 Z" fill="url(#semitono)"/>' + barro([(105, 440), (118, 445), (131, 441), (146, 446), (160, 442), (174, 445), (188, 440)], 5)

RUANA_PIE = 'M144,124 C134,122 124,128 119,140 C111,170 106,220 104,272 C120,280 150,282 172,276 C174,236 172,190 168,156 C165,140 157,127 144,124 Z'
ruana_pie = (
    f'<path d="{RUANA_PIE}" fill="#000" stroke="#000" stroke-width="2.8" stroke-linejoin="round"/>'
    f'<path d="{RUANA_PIE}" fill="url(#lana-blanca)"/>'
    '<path d="M131,142 C124,180 118,225 116,272 M144,140 C142,185 141,230 142,276 M156,144 C160,190 161,235 162,276" stroke="#fff" stroke-width="1.3" fill="none" stroke-linecap="round"/>'
    '<path d="M108,264 C125,271 150,273 170,268" stroke="#fff" stroke-width="1.4" fill="none" stroke-dasharray="3 2"/>'
    '<path d="M134,124 C144,131 158,133 168,128" stroke="#000" stroke-width="5" fill="none" stroke-linecap="round"/>'
    '<path d="M136,123.5 C146,129.5 158,131 166,127" stroke="#fff" stroke-width="0.8" fill="none" stroke-linecap="round"/>'
)
DOBLEZ_PIE = 'M138,124 C152,122 167,129 171,140 C170,154 162,163 151,165 C147,156 143,142 138,130 Z'
doblez_pie = (
    f'<path d="{DOBLEZ_PIE}" fill="#000" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>'
    f'<path d="{DOBLEZ_PIE}" fill="url(#lana-blanca)"/>'
    '<path d="M145,132 C151,140 155,150 156,160 M154,130 C160,137 164,146 165,153" stroke="#fff" stroke-width="1.2" fill="none" stroke-linecap="round"/>'
    '<path d="M151,165 C160,163 168,156 171,146" stroke="#fff" stroke-width="1.4" fill="none" stroke-dasharray="3 2"/>'
)

def encabezado(titulo, extra):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="500" viewBox="0 0 300 500">
  <!--
    {titulo}
    Personaje ficticio (doc 01); hoja de personaje: planeacion/arte/tomo1/personajes/rosalba.md.
    Vestuario: doc 03 §3.1 [V] y J. Ocampo López, "El pueblo boyacense y su folclor", cap. 4 (BanRep).
    {extra}
    Colores: tinta (#000) y papel (#fff) placeholders; único acento: rojo de la cinta, provisional [P].
    Lado visible = lado DERECHO del personaje: piezas "-der" delante, "-izq" detrás.
    GENERADO por game/art/gen/rosalba.py: edita el script, no este archivo.
  -->{defs}'''

def guardar(nombre, cuerpo):
    ruta = os.path.join(OUTDIR, nombre)
    open(ruta, 'w').write(cuerpo + '\n</svg>\n')
    print('ok', nombre, len(cuerpo))

# ======================= 1. de pie, mercado =======================
guardar('rosalba.svg', encabezado('Rosalba Insuasty — de pie, traje de mercado (prólogo y Acto I).',
        'Pañolón negro con bordado y flecos, sombrero de caña con barbuquejo, collar de abalorios.') + f'''
{piece('brazo-izq', '141 144', bi_up, 'Brazo izquierdo (lejano)')}
{piece('antebrazo-izq', '145 202', bi_fore, 'Antebrazo y mano izquierdos; hijo de brazo-izq', extra=' data-padre="brazo-izq"')}
{piece('pierna-izq', '138 250', alpargata(-24, lejana=True), 'Pierna izquierda (lejana): canilla y alpargata')}
{piece('pierna-der', '150 250', alpargata(0), 'Pierna derecha: alpargata de fique, capellada labrada, galones con nudo en rosa')}
{piece('enagua', '146 232', enagua(), 'Enagua blanca de encaje que asoma desigual bajo la falda')}
{piece('falda', '146 232', falda, 'Falda negra de frisa con cintas en el ruedo (tramas en lugar de color)')}
{piece('torso', '146 232', torso, 'Torso: blusa blanca con pechera bordada y collar de abalorios')}
{piece('cabeza', '150 130', cabeza, 'Cabeza con cuello')}
{piece('zarcillo', '143.6 100.8', zarcillo, 'Zarcillo en flor con gota; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('sombrero', '150 60', sombrero, 'Sombrero de caña con cinta negra y barbuquejo; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('brazo-der', '153 140', bd_up, 'Brazo derecho: manga abullonada (queda bajo el pañolón)')}
{piece('antebrazo-der', '157 200', bd_fore, 'Antebrazo derecho con puño bordado y mano; hijo de brazo-der', extra=' data-padre="brazo-der"')}
{piece('panolon', '148 130', panolon, 'Pañolón negro de paño con bordado blanco y flecos largos')}
{piece('trenza', '134 110', trenza(), 'Trenza con cinta roja al extremo (acento liberal)')}''')

# ======================= 2. de pie, monte =======================
guardar('rosalba-monte.svg', encabezado('Rosalba Insuasty — de pie, variante monte (Misión 2 en adelante).',
        'Sin sombrero ni pañolón; ruana oscura y pequeña terciada sobre el hombro derecho (decisión de diseño). Barro en el ruedo; expresión alerta.') + f'''
{piece('brazo-izq', '141 144', bi_up, 'Brazo izquierdo (lejano)')}
{piece('antebrazo-izq', '145 202', bi_fore, 'Antebrazo y mano izquierdos; hijo de brazo-izq', extra=' data-padre="brazo-izq"')}
{piece('pierna-izq', '138 250', alpargata(-24, lejana=True), 'Pierna izquierda (lejana)')}
{piece('pierna-der', '150 250', alpargata(0), 'Pierna derecha')}
{piece('enagua', '146 232', enagua_monte, 'Enagua con el ruedo embarrado')}
{piece('falda', '146 232', falda_monte, 'Falda negra con salpicaduras de barro')}
{piece('torso', '146 232', torso_monte, 'Torso: blusa bordada, sin collar')}
{piece('cabeza', '150 130', cabeza_monte, 'Cabeza sin sombrero, ceja alzada (alerta) y mechones sueltos')}
{piece('zarcillo', '143.6 100.8', zarcillo, 'Zarcillo; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('ruana', '145 128', ruana_pie, 'Ruana oscura de lana (doc 03 [V]; Ocampo: tonos oscuros, pequeña)')}
{piece('trenza', '134 110', trenza(), 'Trenza con cinta roja')}
{piece('brazo-der', '153 140', bd_up, 'Brazo derecho libre')}
{piece('antebrazo-der', '157 200', bd_fore, 'Antebrazo y mano derechos; hijo de brazo-der', extra=' data-padre="brazo-der"')}
{piece('ruana-doblez', '145 128', doblez_pie, 'Doblez de la ruana terciada sobre el hombro derecho')}''')

# ======================= 3. agachada, monte =======================
# Cabeza: la misma, trasladada e inclinada hacia adelante.
CAB_T, CAB_R = (38, 186), 14
def cab_punto(x, y):
    rx, ry = rot_punto(x, y, CAB_R, 150, 130)
    return (rx + CAB_T[0], ry + CAB_T[1])
cuello = cab_punto(150, 130)
z = cab_punto(143.6, 100.8)
nuca = cab_punto(134, 110)
cabeza_ag = f'<g transform="translate({CAB_T[0]} {CAB_T[1]}) rotate({CAB_R} 150 130)">{cabeza_monte}</g>'
zarcillo_ag = f'<g transform="translate({CAB_T[0]} {CAB_T[1]}) rotate({CAB_R} 150 130)">{zarcillo}</g>'

FALDA_AG = 'M118,404 C126,384 150,374 176,370 C192,368 204,370 212,378 C218,386 219,400 219,414 C219,436 220,452 222,466 Q166,472 104,466 C102,446 104,424 110,412 C112,408 115,405 118,404 Z'
cuerpo_ag = (
    # talón de la alpargata asomando atrás (en cuclillas)
    '<path d="M93,466 C93,461 96,457 101,456 L112,456 L112,468 L95,469 Z" fill="#fff" stroke="#000" stroke-width="2"/>'
    '<path d="M92,468 C96,470 106,471 114,470 L114,474 C106,475.5 96,475 92,473 Z" fill="#fff" stroke="#000" stroke-width="2"/>'
    '<path d="M92,468 C96,470 106,471 114,470 L114,474 C106,475.5 96,475 92,473 Z" fill="url(#fique-trenza)"/>'
    '<path d="M97,458 C101,460 106,460 111,458" stroke="#000" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
    # enagua al ras del suelo, con barro
    '<path d="M102,458 L222,458 L223,470 Q220,474.5 216,471 Q212,475 208,471 Q204,475 200,471 Q196,475 192,471 Q188,475 184,471 Q180,475 176,471 Q172,475 168,471 Q164,475 160,471 Q156,475 152,471 Q148,475 144,471 Q140,475 136,471 Q132,475 128,471 Q124,475 120,471 Q116,475 112,471 Q108,475 104,471 Q101,474 101,469 Z" fill="#fff" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/>'
    '<path d="M103,466 L222,466 L222,472 L103,472 Z" fill="url(#semitono)"/>'
    + barro([(108, 469), (123, 471), (139, 468), (157, 471), (171, 468), (189, 471), (205, 469), (217, 471)], 2) +
    # falda en domo sobre las rodillas
    f'<clipPath id="clip-falda-agachada"><path d="{FALDA_AG}"/></clipPath>'
    f'<path d="{FALDA_AG}" fill="#fff" stroke="#000" stroke-width="3" stroke-linejoin="round"/>'
    f'<path d="{FALDA_AG}" fill="url(#trama-densa)"/>'
    '<path d="M118,404 C110,414 104,440 104,466 L118,467 C116,440 120,420 128,400 Z" fill="#000"/>'
    '<path d="M206,388 C210,420 212,445 214,462 M194,380 C196,414 196,440 196,462 M178,376 C176,410 172,440 170,462 M160,380 C154,410 148,440 144,462 M140,388 C132,414 124,440 120,462" stroke="#fff" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
    '<path d="M196,376 C204,374 210,378 213,384" stroke="#fff" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
    '<g clip-path="url(#clip-falda-agachada)">'
    '<rect x="98" y="436" width="130" height="8" fill="#fff" stroke="#000" stroke-width="1.2"/>' + zigzag_x(98, 226, 436, 444) +
    '<rect x="98" y="447" width="130" height="5" fill="url(#trama-cruzada)" stroke="#000" stroke-width="1.2"/>'
    '<rect x="98" y="455" width="130" height="11" fill="#fff" stroke="#000" stroke-width="1.2"/>' + rombos_x(98, 226, 455, 466) +
    barro([(110, 440), (131, 446), (152, 439), (175, 448), (199, 441), (214, 446), (122, 460), (186, 462)], 4) +
    '</g>'
    f'<path d="{FALDA_AG}" fill="none" stroke="#000" stroke-width="3" stroke-linejoin="round"/>'
)

RUANA_AG = 'M180,288 C190,290 197,296 199,305 C203,330 205,356 206,382 C190,394 172,406 154,420 C138,432 120,442 104,448 C102,400 110,346 128,316 C142,296 160,286 180,288 Z'
ruana_ag = '<g transform="translate(2 14)">' + (
    f'<path d="{RUANA_AG}" fill="#000" stroke="#000" stroke-width="2.8" stroke-linejoin="round"/>'
    f'<path d="{RUANA_AG}" fill="url(#lana-blanca)"/>'
    '<path d="M150,300 C134,330 122,380 116,440 M168,296 C160,330 150,380 140,428 M186,300 C188,330 186,360 182,394" stroke="#fff" stroke-width="1.3" fill="none" stroke-linecap="round"/>'
    '<path d="M110,440 C130,433 150,422 168,406 C182,396 194,388 202,380" stroke="#fff" stroke-width="1.4" fill="none" stroke-dasharray="3 2"/>'
    '<path d="M170,290 C180,296 192,298 198,296" stroke="#000" stroke-width="5" fill="none" stroke-linecap="round"/>'
    '<path d="M172,289 C181,294 191,296 196,294.6" stroke="#fff" stroke-width="0.8" fill="none" stroke-linecap="round"/>'
) + '</g>'
DOBLEZ_AG = 'M176,298 C188,296 200,302 204,312 C204,324 198,332 190,334 C186,326 181,312 176,302 Z'
doblez_ag = '<g transform="translate(2 14)">' + (
    f'<path d="{DOBLEZ_AG}" fill="#000" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>'
    f'<path d="{DOBLEZ_AG}" fill="url(#lana-blanca)"/>'
    '<path d="M182,304 C187,312 190,320 191,328 M190,302 C195,308 198,316 199,322" stroke="#fff" stroke-width="1.2" fill="none" stroke-linecap="round"/>'
    '<path d="M190,334 C198,332 203,326 204,316" stroke="#fff" stroke-width="1.4" fill="none" stroke-dasharray="3 2"/>'
) + '</g>'

HOMBRO, CODO, MUNECA = (188, 330), (215, 385), (222, 446)
brazo_ag = (
    f'<path d="{tubo(HOMBRO, CODO, 10, 8)}" fill="#fff" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>'
    + ''.join(f'<path d="M{f(a[0])},{f(a[1])} L{f(b[0])},{f(b[1])}" stroke="#000" stroke-width="0.9"/>'
              for a, b in [(punto_en(HOMBRO, CODO, 0.05, o), punto_en(HOMBRO, CODO, 0.22, o * 0.9)) for o in (-5, 0, 5)])
    + f'<path d="M{f(punto_en(HOMBRO, CODO, 0.2, -7)[0])},{f(punto_en(HOMBRO, CODO, 0.2, -7)[1])} L{f(punto_en(HOMBRO, CODO, 0.95, -5.5)[0])},{f(punto_en(HOMBRO, CODO, 0.95, -5.5)[1])} L{f(punto_en(HOMBRO, CODO, 0.95, -2.5)[0])},{f(punto_en(HOMBRO, CODO, 0.95, -2.5)[1])} L{f(punto_en(HOMBRO, CODO, 0.2, -3.5)[0])},{f(punto_en(HOMBRO, CODO, 0.2, -3.5)[1])} Z" fill="url(#trama-fina)"/>'
)
pu1, pu2 = punto_en(CODO, MUNECA, 0.8, 0), punto_en(CODO, MUNECA, 0.97, 0)
antebrazo_ag = (
    f'<path d="{tubo(CODO, MUNECA, 7.6, 6.2)}" fill="#fff" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>'
    f'<path d="M{f(punto_en(CODO, MUNECA, 0.1, -5)[0])},{f(punto_en(CODO, MUNECA, 0.1, -5)[1])} L{f(punto_en(CODO, MUNECA, 0.78, -4)[0])},{f(punto_en(CODO, MUNECA, 0.78, -4)[1])} L{f(punto_en(CODO, MUNECA, 0.78, -1.5)[0])},{f(punto_en(CODO, MUNECA, 0.78, -1.5)[1])} L{f(punto_en(CODO, MUNECA, 0.1, -2)[0])},{f(punto_en(CODO, MUNECA, 0.1, -2)[1])} Z" fill="url(#trama-fina)"/>'
    # puño bordado
    f'<path d="{tubo(pu1, pu2, 7.4, 7.2)}" fill="#fff" stroke="#000" stroke-width="2"/>'
    + ''.join(f'<circle cx="{f(punto_en(pu1, pu2, 0.5, o)[0])}" cy="{f(punto_en(pu1, pu2, 0.5, o)[1])}" r="0.8" fill="#000"/>' for o in (-4.5, -1.5, 1.5, 4.5)) +
    # mano apoyada en el suelo, palma abajo, dedos hacia adelante
    '<path d="M216,452 C219,447 226,444 229,447 C233,451 236,456 240,460 C244,463 249,466 252,468 C254,470 253,473 250,473.6 L220,474 C216,473 214,470 214.4,466 C214.6,461 215,456 216,452 Z" fill="#fff" stroke="#000" stroke-width="2.4" stroke-linejoin="round"/>'
    '<path d="M236,461 C240,465 244,468 248,470 M232,464 C236,467 240,470 244,472" stroke="#000" stroke-width="1" fill="none" stroke-linecap="round"/>'
    '<path d="M228,452 C231,454 234,457 236,460" stroke="#000" stroke-width="0.6" fill="none"/>'
    # pulgar del lado visible, separado
    '<path d="M224,462 C229,463 234,465 238,468 C240,469.6 239.4,472.4 237,472.6 C232,472.6 227,470.6 223.6,467.6" fill="#fff" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/>'
    '<path d="M235.6,469.4 Q237.4,469.6 237.8,471.4 M248.6,470.4 Q250.4,470.8 250.6,472.6" stroke="#000" stroke-width="0.7" fill="none"/>'
    '<path d="M216,456 C215.4,462 216,468 219,472 L221,471 C218.6,467 218,462 218.4,456 Z" fill="url(#semitono)"/>'
)

guardar('rosalba-agachada.svg', encabezado('Rosalba Insuasty — agachada (sigilo), variante monte. Pose dibujada aparte.',
        'En cuclillas tras un escondite: falda sobre las rodillas, ruana sobre la espalda, mano apoyada en el suelo.') + f'''
{piece('cuerpo', '150 440', cuerpo_ag, 'Cuerpo en cuclillas: falda en domo, enagua al ras, talón de la alpargata')}
{piece('cabeza', f'{f(cuello[0])} {f(cuello[1])}', cabeza_ag, 'Cabeza (la de pie, inclinada hacia adelante)')}
{piece('zarcillo', f'{f(z[0])} {f(z[1])}', zarcillo_ag, 'Zarcillo; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('ruana', '182 310', ruana_ag, 'Ruana sobre la espalda curvada')}
{piece('trenza', f'{f(nuca[0])} {f(nuca[1])}', trenza(nuca[0], nuca[1] + 1, nuca[0] - 4, nuca[1] + 96, 12), 'Trenza colgando por gravedad')}
{piece('brazo-der', f'{HOMBRO[0]} {HOMBRO[1]}', brazo_ag, 'Brazo derecho hacia el suelo')}
{piece('antebrazo-der', f'{CODO[0]} {CODO[1]}', antebrazo_ag, 'Antebrazo y mano apoyada; hijo de brazo-der', extra=' data-padre="brazo-der"')}
{piece('ruana-doblez', '182 310', doblez_ag, 'Doblez de la ruana sobre el hombro derecho')}''')
