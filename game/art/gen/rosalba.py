"""Generador de los SVG de Rosalba (game/art/src/personajes/rosalba*.svg).

Fuente del dibujo: los SVG se generan desde aquí para que las partes compartidas (cabeza,
manos, alpargatas, falda) sean idénticas en todas las poses y variantes.
  python3 art/gen/rosalba.py            (desde game/; sin dependencias)
Si editas un SVG a mano, porta el cambio aquí o se perderá al regenerar.
Hoja de personaje y fuentes: planeacion/arte/tomo1/personajes/rosalba.md.

Variantes por acto (guion de color, paleta.md §5): sin argumentos genera todos los actos, cada uno
en su proceso; con --acto=<id> solo ese. El Prólogo (croma ×1) va en art/src/personajes/; los demás
actos, en art/src/personajes/<acto>/ (un atlas por carpeta), solo con los dibujos que usan.
"""
import json, math, os, re, subprocess, sys

_AQUI = os.path.dirname(os.path.abspath(__file__))
_DATOS = json.load(open(os.path.join(_AQUI, '..', 'paleta.json'), encoding='utf-8'))
_MONTE = ('rosalba-monte', 'rosalba-agachada', 'rosalba-corriendo', 'rosalba-cabezas', 'rosalba-agachada-cabezas', 'rosalba-retrato')
_LLANO = ('rosalba-llano', 'rosalba-llano-agachada', 'rosalba-llano-corriendo')
# Qué dibujos necesita cada acto (doc 02). Mercado: Prólogo y Acto I antes del ataque; la cinta
# suelta es del Prólogo b2; monte: desde la M2 (Acto I); Llano: Acto II en adelante (gastado en el
# Acto III y el Epílogo). El monte sigue en los actos II, III y el Epílogo: llega al Llano con la
# ruana (M4) y puede volver al altiplano (M7, final 1).
ACTOS_ROSALBA = {
    'prologo': ('rosalba', 'rosalba-cabezas', 'rosalba-retrato', 'cinta-roja'),
    'acto1': ('rosalba',) + _MONTE,
    'acto2': _MONTE + _LLANO,
    'acto3': _MONTE + _LLANO,
    'epilogo': _MONTE + _LLANO,
}
_GENERADOS = {n for nombres in ACTOS_ROSALBA.values() for n in nombres}
_args = [a for a in sys.argv[1:] if not a.startswith('--acto=')]
_RAIZ = _args[0] if _args else os.path.join(_AQUI, '..', 'src', 'personajes')
ACTO = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--acto=')), None)
if ACTO is None:
    # Cada acto en su proceso: los colores son constantes del módulo y dependen del acto.
    for acto, nombres in ACTOS_ROSALBA.items():
        carpeta = _RAIZ if acto == 'prologo' else os.path.join(_RAIZ, acto)
        # Fuera las copias que este acto ya no lleva (solo archivos que genera este script).
        if os.path.isdir(carpeta):
            for archivo in os.listdir(carpeta):
                if archivo.endswith('.svg') and archivo[:-4] in _GENERADOS and archivo[:-4] not in nombres:
                    os.remove(os.path.join(carpeta, archivo))
        subprocess.run([sys.executable, os.path.abspath(__file__), f'--acto={acto}', *_args], check=True)
    sys.exit(0)
GUION = next(a for a in _DATOS['guion'] if a['id'] == ACTO)
OUTDIR = _RAIZ if ACTO == 'prologo' else os.path.join(_RAIZ, ACTO)
os.makedirs(OUTDIR, exist_ok=True)

def _oklch_a_hex(L, C, h):
    """OKLCH → hex sRGB (como oklch_a_hex de la skill paleta-tematica, sin buscar gama: bajar el
    croma de un color que ya está en sRGB no lo saca de la gama)."""
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    lin = (4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
           -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
           -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_)
    srgb = (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055 for c in (max(0.0, min(1.0, v)) for v in lin))
    return '#' + ''.join(f'{round(c * 255):02x}' for c in srgb)

def _en_acto(c):
    """Color de la paleta en el acto: solo el registro que cambia con el guion (iluminacion) escala su
    croma. El partido no: la cinta de Rosalba sigue roja también en el epílogo (paleta.md §5)."""
    if c['registro'] == _DATOS.get('registro_guion', 'iluminacion') and GUION['croma_mundo'] != 1:
        L, C, h = c['oklch']
        return _oklch_a_hex(L, C * GUION['croma_mundo'], h)
    return c['hex']

# Paleta del juego (game/art/paleta.json; reglas y fuentes en planeacion/arte/tomo1/paleta.md).
# El dibujo se escribe en tinta (#000) y papel (#fff); al guardar, #000 pasa a `tinta` y #fff
# (brillos y reflejos) a `papel`. Los lavados de color se asignan aquí por material.
PALETA = {c['id']: _en_acto(c) for c in _DATOS['colores']}
TINTA, PAPEL = PALETA['tinta'], PALETA['papel']
PIEL, CHAPAS, TELA, PAJA = PALETA['piel'], PALETA['chapas'], PALETA['blanco-tela'], PALETA['paja']
FALDA, RUANA, LANA, BARRO = PALETA['negro-anil'], PALETA['lana-parda'], PALETA['lana-cruda'], PALETA['barro']
CINTAS = (PALETA['cinta-amarilla'], PALETA['cinta-verde'], PALETA['cinta-rosa'])  # cintas y abalorios
DORADO = PALETA['cinta-amarilla']  # zarcillos
R = PALETA['rojo-liberal']  # cinta de la trenza (Ocampo: «van las cintas rojas generalmente»)
# Llano (sección 8): camisa caqui, falda de dril oscuro, cuero de faja, cotizas y barbuquejo.
CAQUI, DRIL = PALETA['caqui'], PALETA['pano-oscuro']
CUERO, CUERO_CRUDO = PALETA['madera'], PALETA['tierra-llanera']  # la paleta no tiene token de cuero
GASTADO = ACTO in ('acto3', 'epilogo')  # el traje del Llano, remendado en el Acto III y el Epílogo

def f(x): return f"{x:.1f}".rstrip('0').rstrip('.')

# ---------- helpers ----------
def fringes(points, step=4.4, length=16, sway=-2.5):
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
                   f'</g>')
    # amarre de hilo oscuro: la trenza queda atada aunque no lleve la cinta (doc 10 P31–P32)
    bx, by = x1 + 0.5, y1 + 3
    out.append(f'<path d="M{f(bx-3)},{f(by-0.6)} C{f(bx-1)},{f(by-1.6)} {f(bx+1)},{f(by-1.6)} {f(bx+3)},{f(by-0.6)} '
               f'L{f(bx+2.6)},{f(by+2.4)} C{f(bx+1)},{f(by+1.6)} {f(bx-1)},{f(by+1.6)} {f(bx-2.6)},{f(by+2.4)} Z" fill="#000"/>')
    # puntas del pelo que asoman bajo el moño
    out.append(f'<path d="M{f(bx-1)},{f(by+4)} C{f(bx-3)},{f(by+10)} {f(bx-2)},{f(by+14)} {f(bx-4)},{f(by+17)} M{f(bx)},{f(by+4)} C{f(bx)},{f(by+10)} {f(bx+1)},{f(by+14)} {f(bx)},{f(by+18)} M{f(bx+1)},{f(by+4)} C{f(bx+3)},{f(by+9)} {f(bx+3)},{f(by+12)} {f(bx+4)},{f(by+15)}" stroke="#000" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
    return ''.join(out)

def cinta(x1=124.0, y1=214.0):
    """Moño de cinta roja al final de la trenza (cintas rojas en las trenzas: Ocampo López, cap. 4).
    Pieza propia, hija de `trenza`: en la historia se la quitan y ella vuelve a atársela (doc 10 P31–P32)."""
    bx, by = x1 + 0.5, y1 + 3
    out = []
    out.append(
        '<g>'
        f'<path d="M{f(bx)},{f(by)} C{f(bx-10)},{f(by-9)} {f(bx-14)},{f(by+2)} {f(bx-4)},{f(by+3)} Z" fill="{R}" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/>'
        f'<path d="M{f(bx)},{f(by)} C{f(bx+10)},{f(by-9)} {f(bx+14)},{f(by+2)} {f(bx+4)},{f(by+3)} Z" fill="{R}" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/>'
        f'<path d="M{f(bx-1)},{f(by+2)} C{f(bx-5)},{f(by+9)} {f(bx-6)},{f(by+14)} {f(bx-9)},{f(by+19)} L{f(bx-5)},{f(by+18)} C{f(bx-3)},{f(by+13)} {f(bx-1)},{f(by+8)} {f(bx+1)},{f(by+3)} Z" fill="{R}" stroke="#000" stroke-width="1.2" stroke-linejoin="round"/>'
        f'<path d="M{f(bx+1)},{f(by+2)} C{f(bx+4)},{f(by+8)} {f(bx+4)},{f(by+13)} {f(bx+7)},{f(by+17)} L{f(bx+3)},{f(by+18)} C{f(bx+1)},{f(by+13)} {f(bx)},{f(by+8)} {f(bx-1)},{f(by+3)} Z" fill="{R}" stroke="#000" stroke-width="1.2" stroke-linejoin="round"/>'
        f'<ellipse cx="{f(bx)}" cy="{f(by+1)}" rx="2.6" ry="2.2" fill="{R}" stroke="#000" stroke-width="1.3"/>'
        f'<path d="M{f(bx-9)},{f(by-1)} C{f(bx-7)},{f(by-4)} {f(bx-4)},{f(by-4)} {f(bx-3)},{f(by-1)} M{f(bx+9)},{f(by-1)} C{f(bx+7)},{f(by-4)} {f(bx+4)},{f(by-4)} {f(bx+3)},{f(by-1)}" stroke="#fff" stroke-width="0.8" fill="none"/>'
        f'</g>')
    return ''.join(out)

# ---------- collar de abalorios ----------
def collar():
    out = []
    P0, P1, P2 = (150, 134), (157, 154), (172, 150)
    for i in range(13):
        x, y = quad(P0, P1, P2, i / 12)
        fill = '#000' if i % 2 == 0 else CINTAS[(i // 2) % 3]
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="1.7" fill="{fill}" stroke="#000" stroke-width="0.8"/>')
    return ''.join(out)

# ---------- bordados de la pechera ----------
def pechera():
    out = []
    pts = [(165, 139), (168.5, 146), (170.5, 154), (171.2, 162), (170.6, 170), (169, 178)]
    for i, (x, y) in enumerate(pts):
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="0.9" fill="#000"/>')
        if i % 2 == 1:
            out.append(flor(x - 5, y + 1, 1.9, CINTAS[(i // 2) % 3]).replace(f'stroke="{CINTAS[(i // 2) % 3]}" stroke-width="0.6"', 'stroke="#000" stroke-width="0.6"'))
    out.append('<path d="M160,140 L163,144 L161,148 L164,152 L162,156 L165,160 L163,164 L166,168 L164,172 L166,176" stroke="#000" stroke-width="0.8" fill="none"/>')
    return ''.join(out)

# ---------- bordado del pañolón (blanco sobre negro) ----------
def bordado_panolon():
    out = [f'<path d="M155,140 C152,165 154,200 160,228 M159,229 C150,229 143,228 138,232 C130,240 122,248 116,255" stroke="{LANA}" stroke-width="0.9" fill="none"/>']
    for (x, y) in [(154.5, 150), (154, 172), (156, 196), (159, 219), (146, 229), (131, 239), (121, 249)]:
        out.append(flor(x, y, 2.2, LANA))
        out.append(hoja(x + 3, y + 4, 40, LANA))
        out.append(hoja(x - 3, y - 4, 40, LANA))
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
        x += 8; up = not up
    return f'<path d="M{" L".join(pts)}" stroke="#000" stroke-width="1.3" fill="none"/>'

def rombos(y1, y2):
    out = []
    x = xl(y2) + 5
    cy = (y1 + y2) / 2 + 1.5
    while x < xr(y2) - 4:
        out.append(f'<path d="M{f(x)},{f(cy-3.5)} L{f(x+3)},{f(cy)} L{f(x)},{f(cy+3.5)} L{f(x-3)},{f(cy)} Z" fill="#000"/>')
        x += 13
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
    return f'<path d="{path}" fill="{TELA}" stroke="#000" stroke-width="1.8" stroke-linejoin="round"/>'

# ---------- alpargata ----------
def alpargata(dx, lejana=False):
    def P(x, y): return f"{f(x+dx)},{f(y)}"
    sw = 2.0 if lejana else 2.4
    s = []
    # canilla (asoma bajo la enagua)
    s.append(f'<path d="M{P(151,430)} L{P(163,430)} C{P(163,440)} {P(163,447)} {P(164,452)} L{P(152,452)} C{P(152,446)} {P(151,438)} {P(151,430)} Z" fill="{PIEL}" stroke="#000" stroke-width="{sw}"/>')
    # suela de fique trenzado
    sole = f'M{P(145,466)} C{P(153,469.5)} {P(173,470.5)} {P(188,466)} C{P(190,468)} {P(189.5,472.5)} {P(186,474)} C{P(171,476.5)} {P(151,476)} {P(145,473)} C{P(143.5,471)} {P(143.5,468)} {P(145,466)} Z'
    s.append(f'<path d="{sole}" fill="{PAJA}" stroke="#000" stroke-width="{sw}"/>')
    # talonera
    s.append(f'<path d="M{P(146,456)} C{P(144.5,460)} {P(144.5,464)} {P(146,467)} L{P(152,467)} C{P(151,463)} {P(151,459)} {P(152,455)} Z" fill="{TELA}" stroke="#000" stroke-width="{sw*0.8}"/>')
    # capellada de algodón, labrada
    cap = f'M{P(150,453)} C{P(154,448)} {P(163,447)} {P(168,451)} C{P(175,454)} {P(184,458)} {P(188,465)} C{P(186,467.5)} {P(183,468)} {P(180,468)} L{P(151,467)} C{P(150,462)} {P(149,457)} {P(150,453)} Z'
    s.append(f'<path d="{cap}" fill="{TELA}" stroke="#000" stroke-width="{sw}"/>')
    s.append(f'<path d="M{P(159,459)} L{P(164,463)} L{P(169,459)} L{P(174,463)} L{P(179,460)}" stroke="#000" stroke-width="1.1" fill="none"/>')
    # galones negros cruzados al tobillo y nudo en rosa sobre el empeine
    s.append(f'<path d="M{P(150,449)} C{P(155,445.5)} {P(161,445.5)} {P(166,448.5)} M{P(150,445)} C{P(156,448.5)} {P(160,449.5)} {P(166,452)} M{P(147,457)} C{P(152,454)} {P(158,451)} {P(166,449)}" stroke="#000" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    rx, ry = 167 + dx, 449
    s.append(f'<circle cx="{f(rx)}" cy="{ry}" r="4.6" fill="#000"/>')
    s.append(f'<path d="M{f(rx-2.6)},{f(ry-0.5)} C{f(rx-2)},{f(ry-3)} {f(rx+2.4)},{f(ry-3)} {f(rx+2.4)},{f(ry)} C{f(rx+2.4)},{f(ry+2.4)} {f(rx-1)},{f(ry+2.6)} {f(rx-1.2)},{f(ry+0.4)} C{f(rx-1.2)},{f(ry-1)} {f(rx+0.8)},{f(ry-1.2)} {f(rx+0.8)},{f(ry+0.2)}" stroke="#fff" stroke-width="0.8" fill="none"/>')
    s.append(f'<path d="M{f(rx+1)},{f(ry+3.5)} C{f(rx+3)},{f(ry+6)} {f(rx+3)},{f(ry+8)} {f(rx+5)},{f(ry+10)} M{f(rx-1)},{f(ry+3.5)} C{f(rx-1)},{f(ry+6)} {f(rx-3)},{f(ry+8)} {f(rx-3)},{f(ry+10)}" stroke="#000" stroke-width="2" fill="none" stroke-linecap="round"/>')
    if lejana:
        s.append(f'<path d="{cap}" fill="#000" fill-opacity="0.1"/>')
        s.append(f'<path d="M{P(151,430)} L{P(163,430)} C{P(163,440)} {P(163,447)} {P(164,452)} L{P(152,452)} C{P(152,446)} {P(151,438)} {P(151,430)} Z" fill="#000" fill-opacity="0.1"/>')
    return ''.join(s)

# ---------- mano (dorso hacia el espectador) ----------
def mano(dx, sw):
    """Mano colgando del antebrazo (muñeca en y≈258), con el pulgar adelante."""
    def P(x, y): return f"{f(x+dx)},{f(y)}"
    return (
        # mano: dorso hacia el espectador, pulgar adelante separado del índice
        f'<path d="M{P(158,260)} C{P(156.5,266)} {P(156.6,272)} {P(157.4,277)} C{P(158,284)} {P(159.5,290)} {P(162,294.5)} C{P(163.6,297)} {P(166.4,297.2)} {P(167.6,295)} C{P(168.4,296.8)} {P(171,297)} {P(172,294.8)} C{P(173.4,292)} {P(172.6,287)} {P(171.2,283)} C{P(170.6,280.6)} {P(170.6,278.6)} {P(171.6,277.2)} C{P(173.4,277.6)} {P(176.4,277.8)} {P(178.6,276.4)} C{P(180.6,275)} {P(180.4,272.4)} {P(178.4,271)} C{P(176.4,269.6)} {P(174.4,268.2)} {P(172.6,264.6)} L{P(172,258)} Z" fill="{PIEL}" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>'
        # borde interno del pulgar: deja ver el hueco entre pulgar e índice
        f'<path d="M{P(171.6,277.2)} C{P(171,275.4)} {P(171.4,273)} {P(172.6,271)}" stroke="#000" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
        f'<path d="M{P(178.3,272.3)} Q{P(179.6,273.4)} {P(179.4,275.2)}" stroke="#000" stroke-width="0.8" fill="none"/>'
        # dedos escalonados y línea de nudillos
        f'<path d="M{P(161,279)} C{P(161.6,286)} {P(163,291)} {P(165,295)} M{P(165.5,279)} C{P(166,286)} {P(167.4,291)} {P(168.8,295)}" stroke="#000" stroke-width="1" fill="none" stroke-linecap="round"/>'
        f'<path d="M{P(158,276.4)} C{P(162,274.8)} {P(166,275.2)} {P(170,277)}" stroke="#000" stroke-width="0.6" fill="none"/>'
        f'<path d="M{P(164.6,295.4)} Q{P(165.8,296.4)} {P(166.8,295.6)} M{P(169.4,295.6)} Q{P(170.6,296.6)} {P(171.6,295.4)}" stroke="#000" stroke-width="0.7" fill="none"/>'
        # tendones y sombra del canto
        f'<path d="M{P(161,263)} C{P(161.4,267)} {P(161.8,271)} {P(161.8,274)} M{P(165,262.5)} C{P(165.4,267)} {P(165.8,271)} {P(165.8,274)}" stroke="#000" stroke-width="0.55" fill="none"/>'
        f'<path d="M{P(157.4,266)} C{P(156.8,274)} {P(157.6,283)} {P(160,290)} L{P(161.4,289)} C{P(159.6,282)} {P(159,274)} {P(159.8,266)} Z" fill="#000" fill-opacity="0.1"/>'
    )

# ---------- brazo + antebrazo ----------
def brazo(dx, lejano=False):
    def P(x, y): return f"{f(x+dx)},{f(y)}"
    sw = 2.2 if lejano else 2.7
    up = (f'<path d="M{P(138,138)} C{P(146,128)} {P(166,130)} {P(168,146)} C{P(169,160)} {P(167,182)} {P(166,200)} C{P(162,208)} {P(150,208)} {P(147,200)} C{P(144,180)} {P(141,160)} {P(138,138)} Z" fill="{TELA}" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>'
          f'<path d="M{P(146,134)} C{P(147,140)} {P(148,146)} {P(148,150)} M{P(153,132)} C{P(154,138)} {P(155,144)} {P(155,150)} M{P(160,134)} C{P(160,140)} {P(161,145)} {P(161,150)}" stroke="#000" stroke-width="0.9" fill="none"/>'
          f'<path d="M{P(142,160)} C{P(144,178)} {P(146,192)} {P(148,200)} L{P(152,201)} C{P(150,190)} {P(148,176)} {P(147,158)} Z" fill="#000" fill-opacity="0.1"/>')
    if lejano:
        up += f'<path d="M{P(138,138)} C{P(146,128)} {P(166,130)} {P(168,146)} C{P(169,160)} {P(167,182)} {P(166,200)} C{P(162,208)} {P(150,208)} {P(147,200)} C{P(144,180)} {P(141,160)} {P(138,138)} Z" fill="#000" fill-opacity="0.18"/>'
    fore = (
        # manga larga hasta la muñeca
        f'<path d="M{P(148,196)} L{P(166,195)} C{P(168,218)} {P(170,236)} {P(171.5,250)} L{P(156.5,253)} C{P(155,238)} {P(151,218)} {P(148,196)} Z" fill="{TELA}" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>'
        f'<path d="M{P(150,206)} C{P(152,222)} {P(154,236)} {P(157,250)} L{P(161,249)} C{P(158,236)} {P(155,222)} {P(153,206)} Z" fill="#000" fill-opacity="0.1"/>'
        f'<path d="M{P(160,212)} C{P(162,224)} {P(164,236)} {P(165,246)}" stroke="#000" stroke-width="0.9" fill="none"/>'
        # puño bordado con abalorios
        f'<path d="M{P(155.5,249)} L{P(172,246.5)} L{P(173.5,257)} L{P(157,260)} Z" fill="{TELA}" stroke="#000" stroke-width="{sw*0.85}" stroke-linejoin="round"/>'
        f'<path d="M{P(157,254)} L{P(160,251.5)} L{P(163,254)} L{P(166,251)} L{P(169,253.5)} L{P(172,250.5)}" stroke="#000" stroke-width="0.8" fill="none"/>'
        + ''.join(f'<circle cx="{f(x+dx)}" cy="{f(y)}" r="0.8" fill="#000"/>' for x, y in [(158.5, 257.5), (162, 257), (165.5, 256.4), (169, 255.8), (172, 255.2)])
        + mano(dx, sw)
    )
    if lejano:
        fore += (f'<path d="M{P(148,196)} L{P(166,195)} C{P(168,218)} {P(170,236)} {P(171.5,250)} L{P(156.5,253)} C{P(155,238)} {P(151,218)} {P(148,196)} Z" fill="#000" fill-opacity="0.18"/>'
                 f'<path d="M{P(158,260)} C{P(156,266)} {P(156,272)} {P(157,277)} C{P(157,283)} {P(158,288)} {P(161,292)} C{P(163,295)} {P(167,295.5)} {P(169,293.5)} C{P(171,291)} {P(171.5,287)} {P(171,284)} C{P(173,282)} {P(175.5,280)} {P(177.5,277.5)} C{P(179.5,275)} {P(179,271.5)} {P(177,270)} C{P(175,268.5)} {P(173,267.5)} {P(172,264)} L{P(172,258)} Z" fill="#000" fill-opacity="0.1"/>')
    return up, fore

def piece(gid, pivot, body, comment='', extra=''):
    c = f'\n  <!-- {comment} -->' if comment else ''
    return f'{c}\n  <g id="{gid}" data-pieza="" data-pivote="{pivot}"{extra}>\n    {body}\n  </g>'

# ================= ensamblaje =================
# Detalle limpio (doc 03 §1 «Relleno», 04-oct-2026): el color de la paleta da el valor y la
# trama solo dice sombra. Rosalba no tiene sombras grandes de primer plano: todas sus sombras
# son aguada plana de tinta (cuatro niveles) y las texturas, pocas marcas dibujadas.
SOMBRA_SUAVE = 'fill="#000" fill-opacity="0.1"'
SOMBRA = 'fill="#000" fill-opacity="0.18"'
SOMBRA_FUERTE = 'fill="#000" fill-opacity="0.26"'
SOMBRA_HONDA = 'fill="#000" fill-opacity="0.4"'
defs = ''

def recortar(cid, silueta, marcas):
    """Marcas interiores (pliegues, cintas, listas) recortadas a la silueta: nada se sale del borde."""
    return f'<clipPath id="{cid}"><path d="{silueta}"/></clipPath><g clip-path="url(#{cid})">{marcas}</g>'

bi_up, bi_fore = brazo(-12, lejano=True)
bd_up, bd_fore = brazo(0)

cabeza = f'''
    <!-- cuello -->
    <path d="M140,108 L161,118 C161,125 161,131 163,137 L137,137 C138,128 139,118 140,108 Z" fill="{PIEL}" stroke="#000" stroke-width="2.4"/>
    <path d="M141,114 C142,124 141,131 140,136 L147,136 C146,129 146,121 148,116 Z" fill="#000" fill-opacity="0.1"/>
    <path d="M149,118 C153,124 157,130 159,136" stroke="#000" stroke-width="0.8" fill="none"/>
    <!-- rostro de perfil: frente, entrecejo, nariz recta con punta redonda, labios definidos, mentón firme -->
    <path d="M166,58 C169,62 171,68 172,74 C173,77 172,79 171,81 C174,86 178,90 180,93 C181.5,95.5 180,98 177,98.5 C175.5,98.8 174.5,99.5 174,100.5 C175,102 176.2,103.5 176,105 C175.6,106.2 174,106.6 173.2,107 C174.5,107.8 175.4,109 175,110.2 C174.6,111.2 173,111.5 172.4,112 C173.6,113.4 174.4,115.4 173.4,117.4 C172,119.6 168.5,120.6 164,120.8 C158,121 152,119 147,115 C138,108 128,96 126,80 C125,62 136,47 152,46 C159,46 164,50 166,58 Z" fill="{PIEL}" stroke="#000" stroke-width="2.8" stroke-linejoin="round"/>
    <!-- sombra del ala del sombrero sobre la frente -->
    <path d="M154,60 C160,60 166,61 170,64 C169,67 166,68 160,67 C156,66 154,64 154,60 Z" fill="#000" fill-opacity="0.1"/>
    <!-- sombra bajo la mandíbula -->
    <path d="M150,116 C156,119 162,120.5 168,120.5 C163,123 155,122 150,119 Z" fill="#000" fill-opacity="0.18"/>
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
    <path id="oreja-der" d="M146,83 C141,79.5 136.5,82.5 136.5,89 C136.5,95.5 139.5,100.8 144,100.8 C146.5,100.8 147.6,98.8 147,96.6 L147.6,92.4 C148.6,89.2 148.6,85.6 146,83 Z" fill="{PIEL}" stroke="#000" stroke-width="1.8" stroke-linejoin="round"/>
    <path d="M144.6,84.6 C140.6,83.8 139.2,87.6 139.6,91.6 C139.9,94.2 141,96.4 142.6,97.4" stroke="#000" stroke-width="0.9" fill="none"/>
    <path d="M143.4,86.4 C141.8,88.6 142,91.6 143.6,94.2 M142.4,88.2 L144.4,87.2" stroke="#000" stroke-width="0.8" fill="none"/>
    <path d="M144.5,90 C146,90.2 146.6,91.4 146.4,92.8 C145.2,93.6 144,92.8 144.2,91.4 Z" fill="#000"/>
    <path d="M147.6,92.4 C146.8,93 146.6,94.4 147.2,95.2" stroke="#000" stroke-width="0.8" fill="none"/>
    <path d="M141.4,97.6 C142.4,99.2 143.6,99.8 145,99.6" stroke="#000" stroke-width="0.7" fill="none"/>'''

zarcillo = '''<path d="M143.6,100.6 C143.4,102 143.4,103 143.6,104" stroke="#000" stroke-width="0.9" fill="none"/>
    ''' + flor(143.6, 107, 2.4, DORADO).replace(f'stroke="{DORADO}"', 'stroke="#000"') + f'''
    <path d="M143.6,109.8 C141.6,112 141.8,114.6 143.6,115.8 C145.4,114.6 145.6,112 143.6,109.8 Z" fill="{DORADO}" stroke="#000" stroke-width="0.8"/>
    <circle cx="143" cy="113" r="0.5" fill="#fff"/>'''

sombrero = f'''
    <!-- copa de caña: trencilla enrollada -->
    <path d="M128,58 C127,40 136,30 151,29 C166,29 174,38 172,58 Z" fill="{PAJA}" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M131,46 C144,43.5 158,43.5 171,46 M130,40 C142,37 160,37 170.5,40 M134,34 C144,32 158,32 167,34" stroke="#000" stroke-width="0.9" fill="none"/>
    <path d="M128,58 C127.5,48 129,41 133,36 C131,44 131,51 132,58 Z" fill="#000" fill-opacity="0.18"/>
    <!-- cinta negra con moño atrás -->
    <path d="M128.5,50 C142,47 158,47 171.5,50 L171.8,57 C158,54.5 142,54.5 128.4,57 Z" fill="#000"/>
    <path d="M129,52 C125,50.5 123.5,52.5 125,54.5 C126.5,55.5 128,55 129,54.5 M129,55 C127,57 126.5,59.5 127.5,61.5" stroke="#000" stroke-width="1.6" fill="none" stroke-linecap="round"/>
    <!-- ala -->
    <path d="M102,60 C120,53 180,51 200,57 C195,63 180,66 151,65 C128,65 110,66 102,60 Z" fill="{PAJA}" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M106,60.5 C128,57 172,55 196,57.5" stroke="#000" stroke-width="0.8" fill="none"/>
    <path d="M110,62.6 C132,65 176,64 196,59.6 C186,64.5 168,66.5 150,66.2 C132,66 118,66 110,62.6 Z" fill="#000"/>
    <!-- barbuquejo: cinta que baja por la mejilla y se ata bajo el mentón -->
    <path d="M148.5,64 C149,74 149.6,84 150.2,94 C151,104 155,113 161,118 C163.5,120 165.5,121 167,121.5" stroke="#000" stroke-width="2.2" fill="none" stroke-linecap="round"/>
    <path d="M148.5,64 C149,74 149.6,84 150.2,94 C151,104 155,113 161,118 C163.5,120 165.5,121 167,121.5" stroke="{CINTAS[1]}" stroke-width="1.1" fill="none" stroke-linecap="round"/>
    <path d="M166,121 C163,124 161,128 162,131 M167,122 C168,126 168,129 170,131" stroke="#000" stroke-width="1.8" fill="none" stroke-linecap="round"/>
    <circle cx="166.8" cy="121.6" r="1.8" fill="#000"/>'''

torso = '''
    <path d="M136,130 C150,126 163,128 167,136 C173,150 175,168 171,184 C168,200 166,216 165,232 L128,232 C126,210 123,188 125,164 C126,148 128,138 136,130 Z" fill="''' + TELA + '''" stroke="#000" stroke-width="2.8"/>
    <path d="M125,164 C125,190 126,212 128,231 L135,231 C132,208 131,186 132,160 Z" fill="#000" fill-opacity="0.1"/>
    <!-- escote redondo con festón -->
    <path d="M141,131 C148,136 157,137 163,134" stroke="#000" stroke-width="1.2" fill="none"/>
    <path d="M142,133.5 Q144,136 146,134.6 Q148,137 150,135.4 Q152,137.6 154,135.8 Q156,137.8 158,135.6 Q160,137.2 162,135" stroke="#000" stroke-width="0.7" fill="none"/>
    <!-- pechera bordada con abalorios -->
    ''' + pechera() + '''
    <!-- collar de abalorios (cuentas negras y blancas) -->
    ''' + collar()

FALDA_D = 'M126,230 L166,230 C172,280 186,360 198,432 Q146,438 94,432 C106,360 118,280 126,230 Z'
falda = (
    f'<path d="{FALDA_D}" fill="{FALDA}" stroke="#000" stroke-width="3.2" stroke-linejoin="round"/>'
    + recortar('falda-marcas', FALDA_D,
    f'<path d="M126,230 C118,280 106,360 94,432 Q104,434 112,434.6 C114,360 120,290 132,232 Z" {SOMBRA_HONDA}/>'
    # pliegues como reflejos blancos sobre la frisa oscura
    '<path d="M138,236 C134,300 126,360 120,392 M147,236 C146,300 143,360 140,392 M155,236 C158,300 162,360 164,392 M162,238 C169,300 177,350 184,392 M131,250 C125,300 116,350 108,392" stroke="#fff" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-opacity="0.5"/>'
    # cintas de colores vistosos en el ruedo (Ocampo López): lavados de la paleta, con su labor en tinta
    + banda(394, 402, CINTAS[0], zigzag(394, 402))
    + banda(406, 412, CINTAS[1])
    + banda(416, 428, CINTAS[2], rombos(416, 428))) +
    f'<path d="{FALDA_D}" fill="none" stroke="#000" stroke-width="3.2" stroke-linejoin="round"/>'
    '<path d="M126,232 L166,232" stroke="#000" stroke-width="1"/>'
    '<path d="M124,226 L168,226 L168.6,236 L123.4,236 Z" fill="#000"/>'
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
        pts.append(f"{f(x)},{f((y1+1.5) if up else (y2-1.5))}"); x += 8; up = not up
    return f'<path d="M{" L".join(pts)}" stroke="#000" stroke-width="1.3" fill="none"/>'

def rombos_x(x1, x2, y1, y2):
    out, x, cy = [], x1 + 5, (y1 + y2) / 2
    while x < x2 - 4:
        out.append(f'<path d="M{f(x)},{f(cy-3.5)} L{f(x+3)},{f(cy)} L{f(x)},{f(cy+3.5)} L{f(x-3)},{f(cy)} Z" fill="#000"/>')
        x += 13
    return ''.join(out)

def barro(puntos, semilla=3):
    """Salpicaduras de barro: manchas irregulares pequeñas (huida por la quebrada)."""
    out = []
    for i, (x, y) in enumerate(puntos):
        r = 0.8 + ((i * 7 + semilla) % 5) * 0.35
        out.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r*1.4)}" ry="{f(r)}" transform="rotate({(i*37)%180} {f(x)} {f(y)})" fill="{BARRO}" stroke="#000" stroke-width="0.4"/>')
    return ''.join(out)

def remiendo(puntos, tela, cid):
    """Parche cosido a mano: retazo de otra tela con puntadas sueltas alrededor."""
    d = polilinea(puntos, True)
    cx = sum(x for x, _ in puntos) / len(puntos)
    cy = sum(y for _, y in puntos) / len(puntos)
    adentro = [mezcla(p, (cx, cy), 0.22) for p in puntos]
    puntadas = []
    for a, b in zip(adentro, adentro[1:] + adentro[:1]):
        for t in (0.15, 0.5, 0.85):
            px, py = mezcla(a, b, t)
            ux, uy = b[0] - a[0], b[1] - a[1]
            l = math.hypot(ux, uy) or 1.0
            nx, ny = -uy / l * 2.6, ux / l * 2.6
            puntadas.append(f'M{f(px - nx)},{f(py - ny)} L{f(px + nx)},{f(py + ny)}')
    return (f'<path d="{d}" fill="{tela}" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/>'
            f'<path d="{" ".join(puntadas)}" stroke="#000" stroke-width="0.9" fill="none" stroke-linecap="round"/>')

def hilachas(puntos):
    """Ruedo deshilachado: pocas hebras sueltas que cuelgan del borde."""
    return ''.join(f'<path d="M{f(x)},{f(y)} C{f(x - 0.6)},{f(y + l * 0.5)} {f(x + 0.8)},{f(y + l * 0.7)} {f(x + 0.2)},{f(y + l)}" '
                   'stroke="#000" stroke-width="0.9" fill="none" stroke-linecap="round"/>' for x, y, l in puntos)

# ======================= cabeza y expresiones =======================
# La cabeza = partes fijas (cuello, contorno, nariz, pelo, oreja) + rasgos por expresión
# (ojo, ceja, boca, mejilla). Rostro simplificado (doc 03 §2): la expresión vive en ojos,
# cejas, boca y postura. Cada expresión es una cabeza completa con el mismo pivote (cuello),
# así el juego la intercambia sin mover sombrero ni zarcillo.
def _tramo(texto, desde, hasta=None):
    i = texto.index(desde)
    j = texto.index(hasta, i) if hasta else len(texto)
    return texto[i:j]

CUELLO_CONTORNO = _tramo(cabeza, '    <!-- cuello -->', '    <!-- sombra del ala')
SOMBRA_ALA = _tramo(cabeza, '    <!-- sombra del ala', '    <!-- sombra bajo la mandíbula')
SOMBRA_MANDIBULA = _tramo(cabeza, '    <!-- sombra bajo la mandíbula', '    <!-- rubor de campo')
NARIZ = _tramo(cabeza, '    <!-- nariz: ala y fosa -->', '    <!-- boca -->')
PELO_OREJA = _tramo(cabeza, '    <!-- pelo: raya al medio')
MECHONES = '<path d="M140,50 C136,44 130,44 127,47 M131,58 C125,55 120,57 118,61 M124,78 C119,77 116,80 116,84" stroke="#000" stroke-width="1" fill="none" stroke-linecap="round"/>'

def ojo(clave, almendra, iris, brillo, pestana, puntas, pliegue, inferior, extra='', grosor=2.1):
    """Ojo de perfil: almendra blanca, iris recortado por la almendra, pestañas y párpados."""
    cx, cy, rx, ry = iris
    bx, by, br = brillo
    return (f'<clipPath id="ojo-{clave}"><path d="{almendra}"/></clipPath>'
            f'<path d="{almendra}" fill="{TELA}" stroke="#000" stroke-width="0.9"/>'
            f'<g clip-path="url(#ojo-{clave})"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#000"/>'
            f'<circle cx="{bx}" cy="{by}" r="{br}" fill="#fff"/></g>'
            f'<path d="{pestana}" stroke="#000" stroke-width="{grosor}" fill="none" stroke-linecap="round"/>'
            f'<path d="{puntas}" stroke="#000" stroke-width="0.9" stroke-linecap="round"/>'
            + (f'<path d="{pliegue}" stroke="#000" stroke-width="0.8" fill="none"/>' if pliegue else '')
            + f'<path d="{inferior}" stroke="#000" stroke-width="0.7" fill="none"/>' + extra)

def ceja(d):
    return f'<path d="{d}" fill="#000" stroke="#000" stroke-width="0.8" stroke-linejoin="round"/>'

POMULO = '<path d="M155,90 C157,93 159,95 162,96" stroke="#000" stroke-width="0.7" fill="none"/>'
RUBOR = f'<ellipse cx="160.2" cy="97.6" rx="6.4" ry="3.8" fill="{CHAPAS}"/>' + '<path d="M158,95 L156.5,99 M160.5,95.5 L159,99.5 M163,96 L161.5,100" stroke="#000" stroke-width="0.8" stroke-linecap="round"/>'
BOCA_NEUTRAL = ('<path d="M173.3,107 L169,107.4" stroke="#000" stroke-width="1.5" stroke-linecap="round"/>'
                '<path d="M171.5,110.2 C172.6,110.8 173.8,110.6 174.4,110" stroke="#000" stroke-width="0.8" fill="none"/>'
                '<path d="M169,107.4 C168.2,106.6 168.4,105.8 169.2,105.4" stroke="#000" stroke-width="0.8" fill="none"/>')

CEJAS = {
    'neutral': 'M171.2,72.6 C166,69.4 159.5,69.6 154,72.8 C159.5,71.6 165,71.8 170.6,74.4 Z',
    'alerta': 'M171.4,70.8 C166.4,67 159.6,68.2 154,72.2 C159.6,70.4 165.4,69.8 170.8,72.6 Z',
    'miedo': 'M171.6,69.6 C166.6,64.8 159.8,66.2 154,70.8 C159.8,68.8 165.8,67.8 171,71.4 Z',
    'rabia': 'M171.8,75.6 C166.4,71.6 160,70.6 154,72 C159.8,72.4 165.6,73.6 170.4,77.4 Z',
    'duelo': 'M171.4,70 C166.8,68 160.8,69.6 155,74.6 C160.8,71.4 166.2,70.6 170.8,72 Z',
}

OJO_NEUTRAL = dict(
    almendra='M157.5,80.5 C160.5,78.2 164.5,78 168,79.6 C165.5,82.4 161.5,83.4 157.5,80.5 Z',
    iris=(164.4, 80.7, 2, 2.5), brillo=(165.2, 79.8, 0.65),
    pestana='M156.2,80.6 C159.5,77.3 164.5,77 168.6,79.2 C169.4,78.6 170,77.8 170.3,77',
    puntas='M168.6,79.2 L171,78.6 M167.4,78.5 L169.4,77',
    pliegue='M158.4,76.6 C161.5,75.4 165,75.4 167.6,76.6',
    inferior='M159.5,82.8 C162,83.8 165,83.6 167.2,82.2',
)

RASGOS = {
    # Mirada tranquila; rubor de campo.
    'neutral': RUBOR + POMULO + ojo('neutral', **OJO_NEUTRAL) + ceja(CEJAS['neutral']) + '{NARIZ}' + BOCA_NEUTRAL,
    # Atenta: ceja alzada, arruga de preocupación, párpado algo más abierto.
    'alerta': RUBOR + POMULO + ojo('alerta', **{**OJO_NEUTRAL,
        'pestana': 'M156.2,80.4 C159.5,76.7 164.5,76.4 168.6,78.8 C169.4,78.2 170,77.4 170.3,76.6',
        'pliegue': 'M158.4,75.8 C161.5,74.6 165,74.6 167.6,75.8'})
        + ceja(CEJAS['alerta'])
        + '<path d="M165,65.4 C167,65 169,65.4 170.4,66.4" stroke="#000" stroke-width="0.7" fill="none"/>'
        + '{NARIZ}' + BOCA_NEUTRAL,
    # Miedo: ojo muy abierto con blanco alrededor del iris, ceja arqueada hacia arriba,
    # frente arrugada, labios entreabiertos, gota de sudor; sin rubor (palidez).
    'miedo': POMULO + ojo('miedo',
        almendra='M157,80.6 C160.2,76.6 164.8,76.2 168.4,78.8 C166,83.6 161.4,84.8 157,80.6 Z',
        iris=(163.8, 80.6, 1.6, 1.9), brillo=(164.4, 79.8, 0.55),
        pestana='M155.8,80.4 C159.4,75.6 164.8,75.2 168.8,78.4 C169.6,77.6 170.2,76.8 170.6,76',
        puntas='M168.8,78.4 L171.2,77.6 M167.6,77.4 L169.6,75.8',
        pliegue='M158.2,73.8 C161.4,72.6 165.2,72.6 167.8,73.8',
        inferior='M159,84 C161.8,85.4 165,85.2 167.6,83.4')
        + ceja(CEJAS['miedo'])
        + '<path d="M164.2,62.6 C166.4,62 168.6,62.4 170.2,63.4 M163.4,65.2 C165.6,64.8 167.8,65.2 169.4,66" stroke="#000" stroke-width="0.6" fill="none"/>'
        + '<path d="M154.6,84.6 C153.2,87.4 152.6,89.2 153.4,90.6 C154.2,91.8 156,91.6 156.4,90.2 C156.8,88.8 155.8,87 154.6,84.6 Z" fill="#fff" stroke="#000" stroke-width="0.8"/>'
        + '<path d="M154.2,88.4 L154,89.6" stroke="#000" stroke-width="0.5"/>'
        + '{NARIZ}'
        + '<path d="M173.4,106.6 C171.8,106.8 170.4,107 169,107.2" stroke="#000" stroke-width="1.2" fill="none" stroke-linecap="round"/>'
        + '<path d="M173.6,107.2 L169.2,107.6 C169.6,108.4 171.2,108.8 173.8,108.6 Z" fill="#000"/>'
        + '<path d="M171.4,111 C172.6,111.6 173.8,111.4 174.6,110.6" stroke="#000" stroke-width="0.8" fill="none"/>',
    # Rabia: ceja baja hacia la nariz, entrecejo marcado, ojo entrecerrado y tenso,
    # aleta de la nariz abierta, labios apretados, mandíbula tensa, rubor intenso.
    'rabia': f'<ellipse cx="160.6" cy="97.6" rx="7.6" ry="4.4" fill="{CHAPAS}"/>' + '<path d="M157.6,94.6 L156,99 M160,95 L158.4,99.4 M162.4,95.4 L160.8,99.8 M164.8,96 L163.4,100" stroke="#000" stroke-width="0.95" stroke-linecap="round"/>'
        + POMULO + ojo('rabia',
        almendra='M157.8,81 C160.8,79.6 164.8,79.4 168,80.6 C165.4,82.8 161.6,83.4 157.8,81 Z',
        iris=(164.2, 81.6, 2, 2.5), brillo=(164.9, 80.9, 0.5),
        pestana='M156.4,80.6 C159.8,79.4 164.6,79.2 169.2,80.8',
        puntas='M169.2,80.8 L171.2,80.6',
        pliegue='M158.6,77.8 C161.6,77.2 165,77.2 167.6,78',
        inferior='M159.2,82.6 C162,83.2 165,83 167.8,82',
        extra='<path d="M160,85 C162.6,85.6 165.2,85.4 167,84.6" stroke="#000" stroke-width="0.6" fill="none"/>', grosor=2.6)
        + ceja(CEJAS['rabia'])
        + '<path d="M170.2,70.6 C170.8,72 170.8,73.2 170.4,74.4" stroke="#000" stroke-width="0.7" fill="none"/>'
        + '{NARIZ}'
        + '<path d="M172.8,94.4 C174.8,91.8 178.4,92.4 178.8,95.6" stroke="#000" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
        + '<path d="M173.4,107.2 C171.8,107.5 170.2,107.9 168.6,108.6 C168.2,109.2 168.1,109.9 168.3,110.6" stroke="#000" stroke-width="1.9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        + '<path d="M171.6,110.4 C172.6,110.8 173.6,110.6 174.2,110.2" stroke="#000" stroke-width="0.8" fill="none"/>',
    # Duelo: párpado pesado y mirada baja, ceja de tristeza (adentro alta, afuera caída),
    # ojeras, una lágrima en tinta (sin color), comisura hacia abajo, mentón tenso.
    'duelo': POMULO + ojo('duelo',
        almendra='M157.6,81.4 C160.6,80.4 164.8,80.2 168,81 C165.6,83.6 161.4,84.2 157.6,81.4 Z',
        iris=(163.6, 82.6, 1.9, 2.3), brillo=(164.2, 82.2, 0.5),
        pestana='M156.4,81.2 C159.6,79.6 164.6,79.2 168.4,80.8 C169.2,80.6 169.8,80.4 170.2,80',
        puntas='M168.4,80.8 L170.4,81.4',
        pliegue='M157.8,78.4 C161,76.8 165,76.8 167.8,78.2',
        inferior='M159.6,84.8 C162.4,85.8 165.4,85.4 167.4,84',
        extra='<path d="M160.4,86.8 C162.8,87.6 165.4,87.4 167,86.2" stroke="#000" stroke-width="0.5" fill="none"/>')
        + ceja(CEJAS['duelo'])
        + '<path d="M166.6,85.4 C166.2,89.2 165.2,93 164.8,96.2" stroke="#000" stroke-width="0.6" fill="none"/>'
        + '<path d="M165.2,96.2 C163.8,98.6 163.2,100.4 164,101.6 C164.8,102.8 166.6,102.6 167,101.2 C167.4,99.8 166.6,98.2 165.2,96.2 Z" fill="#fff" stroke="#000" stroke-width="0.8"/>'
        + '<path d="M164.6,99.4 L164.4,100.6" stroke="#000" stroke-width="0.5"/>'
        + '{NARIZ}'
        + '<path d="M173.2,107.4 C171.8,107.8 170.4,108.6 169,109.8" stroke="#000" stroke-width="1.5" fill="none" stroke-linecap="round"/>'
        + '<path d="M171.6,110.8 C172.6,111.2 173.6,111 174.2,110.4" stroke="#000" stroke-width="0.7" fill="none"/>'
        + '<path d="M170.8,114.4 C171.6,114.8 172.4,114.8 173,114.4" stroke="#000" stroke-width="0.6" fill="none"/>',
}
EXPRESIONES = list(RASGOS)

def cabeza_de(expr):
    """Cabeza completa (sin sombra de sombrero ni mechones) con los rasgos de la expresión."""
    return CUELLO_CONTORNO + SOMBRA_MANDIBULA + RASGOS[expr].replace('{NARIZ}', NARIZ) + PELO_OREJA

def parpado_de(expr):
    """Parpadeo: tapa el ojo con piel, dibuja el ojo cerrado y repone la ceja de la expresión."""
    return (f'<path d="M155.2,80.8 C158.2,75.2 165.2,74.6 170.4,77.6 L170.2,85 C165.8,87 159.8,87 155.2,82.8 Z" fill="{PIEL}"/>'
            '<path d="M156.4,81 C159.8,83.2 164.6,83.4 168.8,81.2" stroke="#000" stroke-width="2" fill="none" stroke-linecap="round"/>'
            '<path d="M161,82.8 L160.6,84.4 M164.4,83 L164.4,84.8 M167.4,82.2 L168,83.8" stroke="#000" stroke-width="0.8" stroke-linecap="round"/>'
            '<path d="M158.2,78.6 C161.6,77.4 165.2,77.4 167.8,78.6" stroke="#000" stroke-width="0.7" fill="none"/>'
            + ceja(CEJAS[expr]))

# La cabeza de pie por defecto es la neutral; la sombra del ala pasa al sombrero.
cabeza_monte = cabeza_de('alerta')
sombrero = SOMBRA_ALA + sombrero
cabeza = cabeza_de('neutral')

torso_monte = torso.split('    <!-- collar de abalorios')[0]

barro_ruedo = barro([(104, 425), (112, 419), (121, 429), (133, 422), (147, 430), (160, 424), (171, 431), (183, 421), (193, 428), (100, 438), (126, 440), (152, 441), (178, 439)])
falda_monte = falda + barro_ruedo
enagua_monte = enagua() + '<path d="M97,437 C130,441 165,439 197,435 L197,442 C165,446 130,448 97,444 Z" fill="#000" fill-opacity="0.1"/>' + barro([(105, 440), (118, 445), (131, 441), (146, 446), (160, 442), (174, 445), (188, 440)], 5)

RUANA_PIE = 'M144,124 C134,122 124,128 119,140 C111,170 106,220 104,272 C120,280 150,282 172,276 C174,236 172,190 168,156 C165,140 157,127 144,124 Z'
ruana_pie = (
    f'<path d="{RUANA_PIE}" fill="{RUANA}" stroke="#000" stroke-width="2.8" stroke-linejoin="round"/>'
    '<path d="M131,142 C124,180 118,225 116,272 M144,140 C142,185 141,230 142,276 M156,144 C160,190 161,235 162,276" stroke="#fff" stroke-width="1.3" fill="none" stroke-linecap="round"/>'
    + recortar('ruana-listas', RUANA_PIE, f'<path d="M100,258 C122,266 150,268 176,262" stroke="{LANA}" stroke-width="2.4" fill="none"/>'
                                         f'<path d="M100,264 C122,272 150,274 176,268" stroke="{LANA}" stroke-width="1.3" fill="none"/>') +
    '<path d="M134,124 C144,131 158,133 168,128" stroke="#000" stroke-width="5" fill="none" stroke-linecap="round"/>'
    '<path d="M136,123.5 C146,129.5 158,131 166,127" stroke="#fff" stroke-width="0.8" fill="none" stroke-linecap="round"/>'
)
DOBLEZ_PIE = 'M138,124 C152,122 167,129 171,140 C170,154 162,163 151,165 C147,156 143,142 138,130 Z'
doblez_pie = (
    f'<path d="{DOBLEZ_PIE}" fill="{RUANA}" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>'
    '<path d="M145,132 C151,140 155,150 156,160 M154,130 C160,137 164,146 165,153" stroke="#fff" stroke-width="1.2" fill="none" stroke-linecap="round"/>'
    f'<path d="M151,165 C160,163 168,156 171,146" stroke="{LANA}" stroke-width="2" fill="none"/>'
)

def encabezado(titulo, extra):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="500" viewBox="0 0 300 500">
  <!--
    {titulo}
    Personaje ficticio (doc 01); hoja de personaje: planeacion/arte/tomo1/personajes/rosalba.md.
    Vestuario: doc 03 §3.1 [V] y J. Ocampo López, "El pueblo boyacense y su folclor", cap. 4 (BanRep).
    {extra}
    Colores: paleta del juego (game/art/paleta.json, planeacion/arte/tomo1/paleta.md); acento: rojo liberal de la cinta.
    Lado visible = lado DERECHO del personaje: piezas "-der" delante, "-izq" detrás.
    GENERADO por game/art/gen/rosalba.py: edita el script, no este archivo.
  -->{defs}'''

def escribir(ruta, texto):
    """Guarda el SVG pasando la tinta (#000) y los brillos (#fff) a la paleta; solo si el acto lo lleva."""
    if os.path.basename(ruta)[:-4] not in ACTOS_ROSALBA[ACTO]:
        return False
    texto = re.sub(r'"#000"', f'"{TINTA}"', texto)
    texto = re.sub(r'"#fff"', f'"{PAPEL}"', texto)
    open(ruta, 'w', encoding='utf-8').write(texto)
    print('ok', ACTO, os.path.basename(ruta))
    return True

def guardar(nombre, cuerpo):
    ruta = os.path.join(OUTDIR, nombre)
    escribir(ruta, cuerpo + '\n</svg>\n')

# ======================= 1. de pie, mercado =======================
guardar('rosalba.svg', encabezado('Rosalba Insuasty — de pie, traje de mercado (prólogo y Acto I).',
        'Pañolón negro con bordado y flecos, sombrero de caña con barbuquejo, collar de abalorios.') + f'''
{piece('brazo-izq', '141 144', bi_up, 'Brazo izquierdo (lejano)')}
{piece('antebrazo-izq', '145 202', bi_fore, 'Antebrazo y mano izquierdos; hijo de brazo-izq', extra=' data-padre="brazo-izq"')}
{piece('pierna-izq', '133 462', alpargata(-24, lejana=True), 'Pierna izquierda (lejana): canilla y alpargata; pivote en el tobillo (pies bajo falda larga)')}
{piece('pierna-der', '157 462', alpargata(0), 'Pierna derecha: alpargata de fique, capellada labrada, galones con nudo en rosa; pivote en el tobillo')}
{piece('enagua', '146 232', enagua(), 'Enagua blanca de encaje que asoma desigual bajo la falda')}
{piece('falda', '146 232', falda, 'Falda de frisa negra de añil con cintas de colores en el ruedo')}
{piece('torso', '146 232', torso, 'Torso: blusa blanca con pechera bordada y collar de abalorios')}
{piece('cabeza', '150 130', cabeza, 'Cabeza con cuello')}
{piece('zarcillo', '143.6 100.8', zarcillo, 'Zarcillo en flor con gota; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('sombrero', '150 60', sombrero, 'Sombrero de caña con cinta negra y barbuquejo; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('brazo-der', '153 140', bd_up, 'Brazo derecho: manga abullonada (queda bajo el pañolón)')}
{piece('antebrazo-der', '157 200', bd_fore, 'Antebrazo derecho con puño bordado y mano; hijo de brazo-der', extra=' data-padre="brazo-der"')}
{piece('panolon', '148 130', panolon, 'Pañolón negro de paño con bordado claro y flecos largos')}
{piece('trenza', '134 110', trenza(), 'Trenza atada con hilo oscuro')}
{piece('cinta', '124.5 217', cinta(), 'Cinta roja de la trenza (rojo liberal); hija de trenza: se quita y se pone (doc 10 P31–P32)', extra=' data-padre="trenza"')}''')

# ======================= 2. de pie, monte =======================
guardar('rosalba-monte.svg', encabezado('Rosalba Insuasty — de pie, variante monte (Misión 2 en adelante).',
        'Sin sombrero ni pañolón; ruana oscura y pequeña terciada sobre el hombro derecho (decisión de diseño). Barro en el ruedo; expresión alerta.') + f'''
{piece('brazo-izq', '141 144', bi_up, 'Brazo izquierdo (lejano)')}
{piece('antebrazo-izq', '145 202', bi_fore, 'Antebrazo y mano izquierdos; hijo de brazo-izq', extra=' data-padre="brazo-izq"')}
{piece('pierna-izq', '133 462', alpargata(-24, lejana=True), 'Pierna izquierda (lejana)')}
{piece('pierna-der', '157 462', alpargata(0), 'Pierna derecha')}
{piece('enagua', '146 232', enagua_monte, 'Enagua con el ruedo embarrado')}
{piece('falda', '146 232', falda_monte, 'Falda negra con salpicaduras de barro')}
{piece('torso', '146 232', torso_monte, 'Torso: blusa bordada, sin collar')}
{piece('cabeza', '150 130', cabeza_monte, 'Cabeza sin sombrero, expresión alerta (las demás en rosalba-cabezas.svg)')}
{piece('zarcillo', '143.6 100.8', zarcillo, 'Zarcillo; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('mechones', '150 130', MECHONES, 'Mechones sueltos tras la noche de huida; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('ruana', '145 128', ruana_pie, 'Ruana oscura de lana (doc 03 [V]; Ocampo: tonos oscuros, pequeña)')}
{piece('trenza', '134 110', trenza(), 'Trenza atada con hilo oscuro')}
{piece('cinta', '124.5 217', cinta(), 'Cinta roja; hija de trenza (sin ella desde la M2 hasta el Acto II)', extra=' data-padre="trenza"')}
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
mechones_ag = f'<g transform="translate({CAB_T[0]} {CAB_T[1]}) rotate({CAB_R} 150 130)">{MECHONES}</g>'

FALDA_AG = 'M118,404 C126,384 150,374 176,370 C192,368 204,370 212,378 C218,386 219,400 219,414 C219,436 220,452 222,466 Q166,472 104,466 C102,446 104,424 110,412 C112,408 115,405 118,404 Z'
cuerpo_ag = (
    # talón de la alpargata asomando atrás (en cuclillas)
    f'<path d="M93,466 C93,461 96,457 101,456 L112,456 L112,468 L95,469 Z" fill="{TELA}" stroke="#000" stroke-width="2"/>'
    f'<path d="M92,468 C96,470 106,471 114,470 L114,474 C106,475.5 96,475 92,473 Z" fill="{PAJA}" stroke="#000" stroke-width="2"/>'
    '<path d="M97,458 C101,460 106,460 111,458" stroke="#000" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
    # enagua al ras del suelo, con barro
    '<path d="M102,458 L222,458 L223,470 Q220,474.5 216,471 Q212,475 208,471 Q204,475 200,471 Q196,475 192,471 Q188,475 184,471 Q180,475 176,471 Q172,475 168,471 Q164,475 160,471 Q156,475 152,471 Q148,475 144,471 Q140,475 136,471 Q132,475 128,471 Q124,475 120,471 Q116,475 112,471 Q108,475 104,471 Q101,474 101,469 Z" fill="' + TELA + '" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/>'
    '<path d="M103,466 L222,466 L222,472 L103,472 Z" fill="#000" fill-opacity="0.1"/>'
    + barro([(108, 469), (123, 471), (139, 468), (157, 471), (171, 468), (189, 471), (205, 469), (217, 471)], 2) +
    # falda en domo sobre las rodillas
    f'<clipPath id="clip-falda-agachada"><path d="{FALDA_AG}"/></clipPath>'
    f'<path d="{FALDA_AG}" fill="{FALDA}" stroke="#000" stroke-width="3" stroke-linejoin="round"/>'
    '<path d="M118,404 C110,414 104,440 104,466 L118,467 C116,440 120,420 128,400 Z" fill="#000"/>'
    '<path d="M206,388 C210,420 212,445 214,462 M194,380 C196,414 196,440 196,462 M178,376 C176,410 172,440 170,462 M160,380 C154,410 148,440 144,462 M140,388 C132,414 124,440 120,462" stroke="#fff" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-opacity="0.5"/>'
    '<path d="M196,376 C204,374 210,378 213,384" stroke="#fff" stroke-width="1.1" fill="none" stroke-linecap="round"/>'
    '<g clip-path="url(#clip-falda-agachada)">'
    f'<rect x="98" y="436" width="130" height="8" fill="{CINTAS[0]}" stroke="#000" stroke-width="1.2"/>' + zigzag_x(98, 226, 436, 444) +
    f'<rect x="98" y="447" width="130" height="5" fill="{CINTAS[1]}" stroke="#000" stroke-width="1.2"/>'
    f'<rect x="98" y="455" width="130" height="11" fill="{CINTAS[2]}" stroke="#000" stroke-width="1.2"/>' + rombos_x(98, 226, 455, 466) +
    barro([(110, 440), (131, 446), (152, 439), (175, 448), (199, 441), (214, 446), (122, 460), (186, 462)], 4) +
    '</g>'
    f'<path d="{FALDA_AG}" fill="none" stroke="#000" stroke-width="3" stroke-linejoin="round"/>'
)

RUANA_AG = 'M180,288 C190,290 197,296 199,305 C203,330 205,356 206,382 C190,394 172,406 154,420 C138,432 120,442 104,448 C102,400 110,346 128,316 C142,296 160,286 180,288 Z'
ruana_ag = '<g transform="translate(2 14)">' + (
    f'<path d="{RUANA_AG}" fill="{RUANA}" stroke="#000" stroke-width="2.8" stroke-linejoin="round"/>'
    '<path d="M150,300 C134,330 122,380 116,440 M168,296 C160,330 150,380 140,428 M186,300 C188,330 186,360 182,394" stroke="#fff" stroke-width="1.3" fill="none" stroke-linecap="round"/>'
    + recortar('ruana-ag-listas', RUANA_AG, f'<path d="M104,438 C126,431 148,420 166,404 C180,394 194,386 206,377" stroke="{LANA}" stroke-width="2.4" fill="none"/>'
                                            f'<path d="M104,444 C127,437 150,426 168,410 C182,400 196,392 208,383" stroke="{LANA}" stroke-width="1.3" fill="none"/>') +
    '<path d="M170,290 C180,296 192,298 198,296" stroke="#000" stroke-width="5" fill="none" stroke-linecap="round"/>'
    '<path d="M172,289 C181,294 191,296 196,294.6" stroke="#fff" stroke-width="0.8" fill="none" stroke-linecap="round"/>'
) + '</g>'
DOBLEZ_AG = 'M176,298 C188,296 200,302 204,312 C204,324 198,332 190,334 C186,326 181,312 176,302 Z'
doblez_ag = '<g transform="translate(2 14)">' + (
    f'<path d="{DOBLEZ_AG}" fill="{RUANA}" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>'
    '<path d="M182,304 C187,312 190,320 191,328 M190,302 C195,308 198,316 199,322" stroke="#fff" stroke-width="1.2" fill="none" stroke-linecap="round"/>'
    f'<path d="M190,334 C198,332 203,326 204,316" stroke="{LANA}" stroke-width="2" fill="none"/>'
) + '</g>'

HOMBRO, CODO, MUNECA = (188, 330), (215, 385), (222, 446)
brazo_ag = (
    f'<path d="{tubo(HOMBRO, CODO, 10, 8)}" fill="{TELA}" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>'
    + ''.join(f'<path d="M{f(a[0])},{f(a[1])} L{f(b[0])},{f(b[1])}" stroke="#000" stroke-width="0.9"/>'
              for a, b in [(punto_en(HOMBRO, CODO, 0.05, o), punto_en(HOMBRO, CODO, 0.22, o * 0.9)) for o in (-5, 0, 5)])
    + f'<path d="M{f(punto_en(HOMBRO, CODO, 0.2, -7)[0])},{f(punto_en(HOMBRO, CODO, 0.2, -7)[1])} L{f(punto_en(HOMBRO, CODO, 0.95, -5.5)[0])},{f(punto_en(HOMBRO, CODO, 0.95, -5.5)[1])} L{f(punto_en(HOMBRO, CODO, 0.95, -2.5)[0])},{f(punto_en(HOMBRO, CODO, 0.95, -2.5)[1])} L{f(punto_en(HOMBRO, CODO, 0.2, -3.5)[0])},{f(punto_en(HOMBRO, CODO, 0.2, -3.5)[1])} Z" fill="#000" fill-opacity="0.1"/>'
)
pu1, pu2 = punto_en(CODO, MUNECA, 0.8, 0), punto_en(CODO, MUNECA, 0.97, 0)
antebrazo_ag = (
    f'<path d="{tubo(CODO, MUNECA, 7.6, 6.2)}" fill="{TELA}" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>'
    f'<path d="M{f(punto_en(CODO, MUNECA, 0.1, -5)[0])},{f(punto_en(CODO, MUNECA, 0.1, -5)[1])} L{f(punto_en(CODO, MUNECA, 0.78, -4)[0])},{f(punto_en(CODO, MUNECA, 0.78, -4)[1])} L{f(punto_en(CODO, MUNECA, 0.78, -1.5)[0])},{f(punto_en(CODO, MUNECA, 0.78, -1.5)[1])} L{f(punto_en(CODO, MUNECA, 0.1, -2)[0])},{f(punto_en(CODO, MUNECA, 0.1, -2)[1])} Z" fill="#000" fill-opacity="0.1"/>'
    # puño bordado
    f'<path d="{tubo(pu1, pu2, 7.4, 7.2)}" fill="{TELA}" stroke="#000" stroke-width="2"/>'
    + ''.join(f'<circle cx="{f(punto_en(pu1, pu2, 0.5, o)[0])}" cy="{f(punto_en(pu1, pu2, 0.5, o)[1])}" r="0.8" fill="#000"/>' for o in (-4.5, -1.5, 1.5, 4.5)) +
    # mano apoyada en el suelo, palma abajo, dedos hacia adelante
    f'<path d="M216,452 C219,447 226,444 229,447 C233,451 236,456 240,460 C244,463 249,466 252,468 C254,470 253,473 250,473.6 L220,474 C216,473 214,470 214.4,466 C214.6,461 215,456 216,452 Z" fill="{PIEL}" stroke="#000" stroke-width="2.4" stroke-linejoin="round"/>'
    '<path d="M236,461 C240,465 244,468 248,470 M232,464 C236,467 240,470 244,472" stroke="#000" stroke-width="1" fill="none" stroke-linecap="round"/>'
    '<path d="M228,452 C231,454 234,457 236,460" stroke="#000" stroke-width="0.6" fill="none"/>'
    # pulgar del lado visible, separado
    f'<path d="M224,462 C229,463 234,465 238,468 C240,469.6 239.4,472.4 237,472.6 C232,472.6 227,470.6 223.6,467.6" fill="{PIEL}" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/>'
    '<path d="M235.6,469.4 Q237.4,469.6 237.8,471.4 M248.6,470.4 Q250.4,470.8 250.6,472.6" stroke="#000" stroke-width="0.7" fill="none"/>'
    '<path d="M216,456 C215.4,462 216,468 219,472 L221,471 C218.6,467 218,462 218.4,456 Z" fill="#000" fill-opacity="0.1"/>'
)

guardar('rosalba-agachada.svg', encabezado('Rosalba Insuasty — agachada (sigilo), variante monte. Pose dibujada aparte.',
        'En cuclillas tras un escondite: falda sobre las rodillas, ruana sobre la espalda, mano apoyada en el suelo.') + f'''
{piece('cuerpo', '150 440', cuerpo_ag, 'Cuerpo en cuclillas: falda en domo, enagua al ras, talón de la alpargata')}
{piece('cabeza', f'{f(cuello[0])} {f(cuello[1])}', cabeza_ag, 'Cabeza (la de pie, inclinada hacia adelante)')}
{piece('zarcillo', f'{f(z[0])} {f(z[1])}', zarcillo_ag, 'Zarcillo; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('mechones', f'{f(cuello[0])} {f(cuello[1])}', mechones_ag, 'Mechones sueltos; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('ruana', '182 310', ruana_ag, 'Ruana sobre la espalda curvada')}
{piece('trenza', f'{f(nuca[0])} {f(nuca[1])}', trenza(nuca[0], nuca[1] + 1, nuca[0] - 4, nuca[1] + 96, 12), 'Trenza colgando por gravedad')}
{piece('cinta', f'{f(nuca[0] - 3.5)} {f(nuca[1] + 99)}', cinta(nuca[0] - 4, nuca[1] + 96), 'Cinta roja; hija de trenza', extra=' data-padre="trenza"')}
{piece('brazo-der', f'{HOMBRO[0]} {HOMBRO[1]}', brazo_ag, 'Brazo derecho hacia el suelo')}
{piece('antebrazo-der', f'{CODO[0]} {CODO[1]}', antebrazo_ag, 'Antebrazo y mano apoyada; hijo de brazo-der', extra=' data-padre="brazo-der"')}
{piece('ruana-doblez', '182 310', doblez_ag, 'Doblez de la ruana sobre el hombro derecho')}''')

# ======================= 4. cabezas por expresión =======================
# Una cabeza completa por expresión y su capa de parpadeo, puestas en fila para revisarlas
# juntas. Cada pieza lleva el pivote en su cuello: en el juego reemplaza el frame de la
# cabeza (mismo pivote), así sombrero, zarcillo y mechones siguen en su sitio.
def hoja_cabezas(nombre, titulo, rotacion, ancho, alto, dx0, dy):
    piezas = []
    ranuras = [(e, cabeza_de(e), f'Cabeza: {e}') for e in EXPRESIONES] + \
              [(f'parpado-{e}', parpado_de(e), f'Parpadeo sobre la cabeza {e}') for e in EXPRESIONES]
    for i, (pid, cuerpo, comentario) in enumerate(ranuras):
        tx, ty = dx0 + i * ancho, dy
        rot = f' rotate({rotacion} 150 130)' if rotacion else ''
        # Los ids internos (clipPath de cada ojo) deben ser únicos en el archivo.
        cuerpo = cuerpo.replace('id="ojo-', f'id="{pid}-ojo-').replace('url(#ojo-', f'url(#{pid}-ojo-')
        piezas.append(piece(pid, f'{f(150 + tx)} {f(130 + ty)}', f'<g transform="translate({f(tx)} {f(ty)}){rot}">{cuerpo}</g>', comentario))
    ruta = os.path.join(OUTDIR, nombre)
    ancho_total = ancho * len(ranuras)
    cuerpo = encabezado(titulo, 'Expresiones: ' + ', '.join(EXPRESIONES) + '. Rostro simplificado: ojos, cejas, boca y postura (doc 03 §2).')
    cuerpo = cuerpo.replace('width="300" height="500" viewBox="0 0 300 500"', f'width="{ancho_total}" height="{alto}" viewBox="0 0 {ancho_total} {alto}"')
    escribir(ruta, cuerpo + ''.join(piezas) + '\n</svg>\n')

hoja_cabezas('rosalba-cabezas.svg', 'Rosalba Insuasty — cabezas por expresión (de pie).', 0, 90, 104, -110, -40)
hoja_cabezas('rosalba-agachada-cabezas.svg', 'Rosalba Insuasty — cabezas por expresión (agachada, inclinada).', CAB_R, 100, 116, -104, -30)

# ======================= 5. retrato en tres cuartos (viñetas y diálogos) =======================
# Busto girado 3/4 hacia la derecha (hacia donde camina). Capas: base por variante (ropa, pelo,
# cuello, rostro sin rasgos, nariz, oreja, zarcillo, sombrero) + rasgos por expresión (ojos, cejas,
# boca, mejillas) + parpadeo. Todas las piezas comparten el pivote al pie del busto.
# Construcción de la cabeza: eje del rostro en x≈236 (nariz 254), cejas y≈157, ojos 175, base de
# la nariz 212, boca 232, mentón 265; ojo lejano más estrecho y con el lagrimal hacia la nariz.
# Luz de arriba a la izquierda: lado lejano del rostro, bajo la nariz y bajo la mandíbula en trama.
# Trazo de tinta de grosor variable (pincel) en párpados, cejas, labios y contornos.
# El sombrero se proyecta en 3D: ala caída, copa redonda y trencilla cosida en espiral.
RET_W, RET_H = 400, 480
PIEL_SOMBRA = PALETA['piel-sombra']

def cadena(puntos, n=16):
    """Muestrea una cadena de cúbicas [p0, c1, c2, p1, c1, c2, p2, ...]."""
    out = []
    for k in range(0, len(puntos) - 1, 3):
        p0, p1, p2, p3 = puntos[k:k + 4]
        for i in range(n + 1 if k + 4 >= len(puntos) else n):
            t = i / n
            a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
            out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out

def polilinea(pts, cerrar=False):
    return 'M' + ' L'.join(f'{f(x)},{f(y)}' for x, y in pts) + (' Z' if cerrar else '')

def pincel(puntos, ancho, ini=0.25, fin=0.25, color='#000', n=16, extra=''):
    """Trazo de pincel: grueso al centro y afinado hacia los extremos (ini/fin = grosor relativo)."""
    pts = cadena(puntos, n)
    m = len(pts)
    izq, der = [], []
    for i, (x, y) in enumerate(pts):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, m - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        largo = math.hypot(dx, dy) or 1.0
        t = i / (m - 1)
        base = ini + (fin - ini) * t
        w = ancho / 2 * (base + (1 - base) * math.sin(math.pi * t) ** 0.6)
        izq.append((x - dy / largo * w, y + dx / largo * w))
        der.append((x + dy / largo * w, y - dx / largo * w))
    return f'<path d="{polilinea(izq + der[::-1], True)}" fill="{color}"{extra}/>'

def suave(pts, tension=1.0):
    """Cadena de cúbicas que pasa por los puntos (Catmull-Rom)."""
    out = [pts[0]]
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        out += [(p1[0] + (p2[0] - p0[0]) / 6 * tension, p1[1] + (p2[1] - p0[1]) / 6 * tension),
                (p2[0] - (p3[0] - p1[0]) / 6 * tension, p2[1] - (p3[1] - p1[1]) / 6 * tension), p2]
    return out

def ruta(cad):
    d = f'M{f(cad[0][0])},{f(cad[0][1])}'
    for k in range(1, len(cad), 3):
        d += ' C' + ' '.join(f'{f(x)},{f(y)}' for x, y in cad[k:k + 3])
    return d

def mezcla(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)

# ---------- sombrero en 3D ----------
SOMB_C = (198.0, 93.0)            # centro de la base de la copa en la imagen
SOMB_R0, SOMB_R, SOMB_H = 64.0, 118.0, 50.0
SOMB_CAIDA = math.tan(math.radians(9))
SOMB_ANG = (math.radians(-3), math.radians(-2), math.radians(15))  # giro en el plano, echado atrás, cámara arriba
SOMB_EXP = 2.4                    # forma de la copa: 2,4 redonda (caña); más alto, más plana arriba
# Sombrero de cogollo del Llano: ala más ancha y casi plana, copa más baja y plana con hendidura.
SOMB_LLANERO = dict(SOMB_R=138.0, SOMB_H=40.0, SOMB_CAIDA=math.tan(math.radians(4)), SOMB_EXP=4.0)

def con_sombrero(params, fn):
    """Llama a fn con otra forma de sombrero (las funciones 3D leen estas constantes del módulo)."""
    g = globals()
    antes = {k: g[k] for k in params}
    g.update(params)
    try:
        return fn()
    finally:
        g.update(antes)
LUZ = (-0.55, 0.65, 0.52)

def unit(v):
    l = math.sqrt(sum(c * c for c in v)) or 1.0
    return tuple(c / l for c in v)

def s_cam(p):
    x, y, z = p
    g, a, c = SOMB_ANG
    x, y = x * math.cos(g) - y * math.sin(g), x * math.sin(g) + y * math.cos(g)
    y, z = y * math.cos(a) - z * math.sin(a), y * math.sin(a) + z * math.cos(a)
    y, z = y * math.cos(c) - z * math.sin(c), y * math.sin(c) + z * math.cos(c)
    return x, y, z

def s_px(p):
    x, y, _ = s_cam(p)
    return (SOMB_C[0] + x, SOMB_C[1] - y)

def ala_y(r):
    return -SOMB_CAIDA * (r - SOMB_R0) - 0.2 * max(0.0, r - (SOMB_R - 6)) ** 2

def ala_p(th, r):
    return (r * math.cos(th), ala_y(r), r * math.sin(th))

def ala_visible(th, r):
    k = SOMB_CAIDA + 0.4 * max(0.0, r - (SOMB_R - 6))
    return s_cam((k * math.cos(th), 1.0, k * math.sin(th)))[2] > 0

def copa_r(h):
    u = min(max(h / SOMB_H, 0.0), 1.0)
    return (SOMB_R0 - 1) * (1 - 0.1 * u) * (1 - u ** SOMB_EXP) ** (1 / SOMB_EXP)

def copa_p(th, h):
    r = copa_r(h)
    return (r * math.cos(th), h, r * math.sin(th))

def copa_n(th, h):
    d = copa_r(min(h + 0.5, SOMB_H)) - copa_r(max(h - 0.5, 0))
    return (math.cos(th), -d, math.sin(th))

def arcos(punto, visible, n=144):
    """Tramos visibles de una curva cerrada param. por ángulo (empieza atrás para no partir el frente)."""
    tramos, actual = [], []
    for i in range(n + 1):
        th = -math.pi / 2 + 2 * math.pi * i / n
        if visible(th):
            actual.append(s_px(punto(th)))
        elif actual:
            tramos.append(actual)
            actual = []
    if actual:
        tramos.append(actual)
    return tramos

def envolvente(pts):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in pts))
    def giro(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    bajo, alto = [], []
    for p in pts:
        while len(bajo) >= 2 and giro(bajo[-2], bajo[-1], p) <= 0:
            bajo.pop()
        bajo.append(p)
    for p in reversed(pts):
        while len(alto) >= 2 and giro(alto[-2], alto[-1], p) <= 0:
            alto.pop()
        alto.append(p)
    return bajo[:-1] + alto[:-1]

def sombrero_34(llanero=False):
    v = []
    # --- ala: silueta, cara de abajo a la vista (en sombra) y trencilla cosida en espiral
    borde = [s_px(ala_p(2 * math.pi * i / 160, SOMB_R)) for i in range(160)]
    v.append(f'<path d="{polilinea(borde, True)}" fill="{PAJA}" stroke="#000" stroke-width="2.8" stroke-linejoin="round"/>')
    bajo = []
    for i in range(160):
        t0, t1 = 2 * math.pi * i / 160, 2 * math.pi * (i + 1.02) / 160
        if not ala_visible((t0 + t1) / 2, (SOMB_R0 + SOMB_R) / 2):
            bajo.append(polilinea([s_px(ala_p(t0, SOMB_R0)), s_px(ala_p(t1, SOMB_R0)), s_px(ala_p(t1, SOMB_R)), s_px(ala_p(t0, SOMB_R))], True))
    if bajo:
        v.append(f'<path d="{" ".join(bajo)}" fill="#000" fill-opacity="0.26"/>')
    # sombra que la copa arroja sobre el ala (luz de la izquierda)
    sombra_ala = []
    for i in range(60):
        t0, t1 = math.radians(-60 + i * 2), math.radians(-60 + (i + 1.05) * 2)
        tm = (t0 + t1) / 2
        largo = 26 * max(0.0, math.cos(tm - math.radians(8))) ** 1.5
        if largo > 1 and ala_visible(tm, SOMB_R0 + 4):
            sombra_ala.append(polilinea([s_px(ala_p(t0, SOMB_R0)), s_px(ala_p(t1, SOMB_R0)), s_px(ala_p(t1, SOMB_R0 + largo)), s_px(ala_p(t0, SOMB_R0 + largo))], True))
    v.append(f'<path d="{" ".join(sombra_ala)}" fill="#000" fill-opacity="0.1"/>')
    # pocas marcas: dos vueltas de la trenza de paja en el ala (doc 03 §1 «Relleno»)
    for r in ((SOMB_R0 + 34,) if llanero else (SOMB_R0 + 17, SOMB_R0 + 35)):
        for t in arcos(lambda th, r=r: ala_p(th, r), lambda th, r=r: ala_visible(th, r)):
            if len(t) > 1:
                v.append(f'<path d="{polilinea(t)}" stroke="#000" stroke-width="1.2" fill="none"/>')
    # ribete del borde (la última vuelta de trencilla, doblada)
    for t in arcos(lambda th: ala_p(th, SOMB_R - 3), lambda th: ala_visible(th, SOMB_R - 3)):
        v.append(f'<path d="{polilinea(t)}" stroke="#000" stroke-width="1.4" fill="none"/>')
    # --- copa redonda
    pts = [s_px(copa_p(2 * math.pi * i / 72, SOMB_H * k / 30)) for i in range(72) for k in range(31)]
    v.append(f'<path d="{polilinea(envolvente(pts), True)}" fill="{PAJA}" stroke="#000" stroke-width="2.8" stroke-linejoin="round"/>')
    luz = unit(LUZ)
    sombra = []
    for i in range(96):
        for k in range(30):
            th0, th1 = 2 * math.pi * i / 96, 2 * math.pi * (i + 1.02) / 96
            h0, h1 = SOMB_H * k / 30, SOMB_H * (k + 1.02) / 30
            nc = unit(s_cam(copa_n((th0 + th1) / 2, (h0 + h1) / 2)))
            if nc[2] > 0 and sum(a * b for a, b in zip(nc, luz)) < 0.18:
                sombra.append(polilinea([s_px(copa_p(th0, h0)), s_px(copa_p(th1, h0)), s_px(copa_p(th1, h1)), s_px(copa_p(th0, h1))], True))
    v.append(f'<path d="{" ".join(sombra)}" fill="#000" fill-opacity="0.1"/>')
    vis_c = lambda th, h: s_cam(copa_n(th, h))[2] > 0
    # y tres vueltas en la copa (dos en la de cogollo, que es más baja)
    for h in ((14, 25) if llanero else (15, 27, 38)):
        for t in arcos(lambda th, h=h: copa_p(th, h), lambda th, h=h: vis_c(th, h)):
            if len(t) > 1:
                v.append(f'<path d="{polilinea(t)}" stroke="#000" stroke-width="1.2" fill="none"/>')
    if llanero:
        # hendidura de adelante atrás en la copa plana: línea hundida y su sombra
        frente = math.radians(40)
        rc = copa_r(SOMB_H * 0.78)
        pts = []
        for i in range(25):
            t = -1 + 2 * i / 24
            r = abs(t) * rc
            h = SOMB_H * (0.78 + 0.22 * (1 - abs(t) ** 2)) - 6 * (1 - t * t)
            th = frente if t >= 0 else frente + math.pi
            pts.append(s_px((r * math.cos(th), h, r * math.sin(th))))
        v.append(pincel(suave(pts[::4] + [pts[-1]]), 2.2, 0.2, 0.2))
        v.append(pincel(suave([(x, y + 3) for x, y in pts[::4]] + [(pts[-1][0], pts[-1][1] + 3)]), 3, 0.1, 0.1, '#000', extra=' fill-opacity="0.18"'))
    else:
        tope = s_px(copa_p(0, SOMB_H))
        v.append(f'<ellipse cx="{f(tope[0])}" cy="{f(tope[1] + 3)}" rx="3.2" ry="1.4" fill="none" stroke="#000" stroke-width="0.8"/>')
    # --- cinta negra con puntada y moño al costado de atrás
    def franja(h0, h1):
        ths = [-math.pi / 2 + 2 * math.pi * i / 180 for i in range(181)]
        ths = [th for th in ths if vis_c(th, (h0 + h1) / 2)]
        return [s_px(copa_p(th, h0)) for th in ths] + [s_px(copa_p(th, h1)) for th in reversed(ths)]
    if llanero:
        # cinta de cuero delgada con un nudo de puntas sueltas atrás
        v.append(f'<path d="{polilinea(franja(0, 6), True)}" fill="{CUERO}" stroke="#000" stroke-width="1.2"/>')
        mx, my = s_px(copa_p(math.radians(165), 3))
        v.append(f'<g transform="translate({f(mx)} {f(my)})">'
                 f'<ellipse cx="0" cy="0" rx="3.4" ry="3" fill="{CUERO}" stroke="#000" stroke-width="1"/>'
                 '<path d="M-1,2 C-3,8 -4,13 -7,18 M1,2 C1,8 2,12 1,17" stroke="#000" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
                 f'<path d="M-1,2 C-3,8 -4,13 -7,18 M1,2 C1,8 2,12 1,17" stroke="{CUERO}" stroke-width="1.2" fill="none" stroke-linecap="round"/></g>')
        return ''.join(v)
    v.append(f'<path d="{polilinea(franja(0, 9.5), True)}" fill="#000"/>')
    mx, my = s_px(copa_p(math.radians(170), 5))
    v.append(f'<g transform="translate({f(mx)} {f(my)})">'
             '<path d="M0,0 C-5,-9 -15,-12 -19,-5 C-21,0 -12,2 0,0 Z" fill="#000" stroke="#fff" stroke-width="0.7"/>'
             '<path d="M0,0 C-4,5 -13,11 -18,8 C-21,4 -12,0 0,0 Z" fill="#000" stroke="#fff" stroke-width="0.7"/>'
             '<path d="M-2,2 C-5,10 -7,17 -11,24 L-7.5,22 L-6,26 C-3,18 -1,10 0,3 Z" fill="#000"/>'
             '<path d="M0,2 C0,10 1,17 -1,25 L2,23 L4,26 C4,17 3,10 2,3 Z" fill="#000"/>'
             '<path d="M-4,-2 C-8,-5 -12,-6 -15,-4 M-4,2 C-8,4 -12,6 -14,6" stroke="#fff" stroke-width="0.6" fill="none"/>'
             '<ellipse cx="0" cy="0.5" rx="3" ry="4" fill="#000" stroke="#fff" stroke-width="0.7"/></g>')
    return ''.join(v)

def ala_frente():
    """Borde delantero del ala (de la sien cercana a la lejana) para la sombra que arroja en la frente."""
    pts = [s_px(ala_p(th, SOMB_R)) for th in [math.radians(a) for a in range(20, 150, 4)]]
    return sorted(pts)

# ---------- rostro (base) ----------
CARA_34 = ('M170,152 C176,128 204,106 232,104 C250,104 262,112 266,126 C268,136 268,150 267,157 '
           'C266,163 263,167 263,172 C264,178 268,183 268,192 C268,204 264,214 261,222 '
           'C259,228 260,234 257,240 C253,249 246,256 238,260 C230,264 218,264 208,259 '
           'C196,254 186,247 180,240 C174,230 170,218 170,204 C170,190 168,170 170,152 Z')
CONTORNO_LEJANO = [(267, 155), (266, 163), (263, 167), (263, 172), (264, 178), (268, 183), (268, 192),
                   (268, 204), (264, 214), (261, 222), (259, 228), (260, 234), (257, 240),
                   (253, 249), (246, 256), (238, 260)]
MANDIBULA = [(240, 259), (230, 264), (218, 264), (208, 259), (196, 254), (186, 247), (180, 240),
             (176, 233), (173, 226), (171, 216)]
CUELLO_34 = 'M180,232 C183,258 181,280 172,304 C196,316 222,318 240,310 C233,292 228,278 227,262 Z'
PELO_ATRAS = ('M150,96 C176,74 222,68 248,84 C266,96 274,116 273,138 C273,150 270,158 266,162 L232,170 '
              'L190,196 C182,212 178,226 174,236 C170,246 166,252 160,252 C152,250 144,242 138,230 '
              'C130,214 124,194 122,170 C121,140 132,110 150,96 Z')
PELO_SIEN = ('M150,116 C170,108 192,106 210,110 C198,118 188,130 181,144 C176,156 174,168 175,180 '
             'C170,176 164,174 158,174 C152,174 147,177 144,182 C140,166 140,138 150,116 Z')
OREJA_34 = ('M171,176 C166,166 154,164 149,174 C145,186 148,200 154,208 C157,213 161,217 165,216 '
            'C169,215 171,211 170,206 C172,198 173,186 171,176 Z')
MECHAS_BRILLO = [  # brillos del pelo: de la raya hacia la nuca, siguiendo el cráneo
    ([(232, 104), (214, 104), (190, 112), (176, 132)], 1.6), ([(229, 96), (206, 94), (178, 104), (160, 124)], 1.8),
    ([(224, 86), (200, 84), (170, 94), (150, 116)], 1.6), ([(216, 78), (190, 78), (160, 92), (142, 116)], 1.3),
    ([(160, 134), (148, 150), (142, 170), (142, 190)], 1.1), ([(144, 128), (132, 148), (128, 172), (130, 196)], 1.3),
    ([(134, 202), (138, 218), (146, 232), (156, 244)], 1.0), ([(146, 198), (150, 214), (156, 228), (162, 242)], 0.9),
    ([(180, 120), (164, 140), (154, 162), (150, 178)], 1.0), ([(172, 128), (162, 138), (156, 150), (154, 162)], 0.8),
    ([(236, 104), (250, 106), (262, 114), (268, 128)], 1.2), ([(232, 92), (250, 94), (264, 106), (271, 122)], 1.0),
]

def trenza_34(camino, ancho0, ancho1, n):
    """Trenza de tres cabos: banda negra con muescas alternas y separaciones de papel en V."""
    eje = cadena(camino, 30)
    acum = [0.0]
    for i in range(1, len(eje)):
        acum.append(acum[-1] + math.dist(eje[i - 1], eje[i]))
    total = acum[-1]
    def en(u):
        s_ = min(max(u, 0.0), 1.0) * total
        i = min(range(1, len(acum)), key=lambda j: abs(acum[j] - s_))
        a, b = eje[i - 1], eje[i]
        l = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
        return b, (-(b[1] - a[1]) / l, (b[0] - a[0]) / l), ancho0 + (ancho1 - ancho0) * u
    def borde(u, lado, frac):
        p, nn, w = en(u)
        return (p[0] + nn[0] * w / 2 * lado * frac, p[1] + nn[1] * w / 2 * lado * frac)
    def muesca(u, lado):
        par = 0 if lado == 1 else 1
        return max(math.exp(-((u * n - k) / 0.22) ** 2) for k in range(par, n + 1, 2))
    us = [i / 120 for i in range(121)]
    izq = [borde(u, 1, 1 - 0.16 * muesca(u, 1)) for u in us]
    der = [borde(u, -1, 1 - 0.16 * muesca(u, -1)) for u in us]
    out = [f'<path d="{polilinea(izq + der[::-1], True)}" fill="#000" stroke="#fff" stroke-width="0.8" stroke-linejoin="round"/>']
    for k in range(n):
        lado = 1 if k % 2 == 0 else -1
        u0 = k / n
        sep = [borde(u0, lado, 0.9), borde(u0 + 0.5 / n, lado, 0.25), borde(u0 + 0.95 / n, -lado, 0.35)]
        out.append(pincel(suave(sep), 1.9, 0.9, 0.1, '#fff', 10))
    fin, _, _ = en(1.0)
    return ''.join(out), fin

def mono_34(x, y):
    """Moño de cinta al final de la trenza: dos lazadas, nudo y colas en cola de golondrina."""
    return (f'<g transform="translate({f(x)} {f(y)})">'
            f'<path d="M-2,3 C-6,14 -9,24 -15,34 L-10,32 L-8,37 C-3,26 0,14 1,4 Z" fill="{R}" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/>'
            f'<path d="M1,3 C4,13 6,22 10,31 L5,30 L4,35 C1,25 -1,14 -1,4 Z" fill="{R}" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/>'
            f'<path d="M0,0 C-8,-14 -24,-16 -26,-5 C-27,3 -14,5 0,1 Z" fill="{R}" stroke="#000" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M0,0 C8,-14 24,-15 26,-5 C27,3 14,5 0,1 Z" fill="{R}" stroke="#000" stroke-width="1.5" stroke-linejoin="round"/>'
            '<path d="M-4,-2 C-10,-8 -17,-9 -21,-6 M-5,1 C-11,0 -17,-1 -21,1 M4,-2 C10,-8 17,-9 21,-6 M5,1 C11,0 17,-1 21,1" stroke="#000" stroke-width="0.8" fill="none"/>'
            f'<ellipse cx="0" cy="0.5" rx="4.2" ry="5" fill="{R}" stroke="#000" stroke-width="1.5"/>'
            '<path d="M-1.5,-2.5 C-0.5,0 -0.5,2 -1.5,4" stroke="#000" stroke-width="0.7" fill="none"/></g>')

def zarcillo_34(x, y):
    """Zarcillo de flor con gota (Ocampo López: «zarcillos muy vistosos»)."""
    s = [f'<path d="M{f(x)},{f(y)} C{f(x - 2)},{f(y + 3)} {f(x - 1)},{f(y + 5)} {f(x)},{f(y + 6)}" stroke="#000" stroke-width="1.2" fill="none"/>']
    cy = y + 12
    for i in range(6):
        a = math.pi * 2 * i / 6 - math.pi / 2
        s.append(f'<ellipse cx="{f(x + 4 * math.cos(a))}" cy="{f(cy + 4 * math.sin(a))}" rx="2.6" ry="1.9" '
                 f'transform="rotate({f(math.degrees(a))} {f(x + 4 * math.cos(a))} {f(cy + 4 * math.sin(a))})" fill="{DORADO}" stroke="#000" stroke-width="0.9"/>')
    s.append(f'<circle cx="{f(x)}" cy="{f(cy)}" r="2.2" fill="#000"/><circle cx="{f(x - 0.6)}" cy="{f(cy - 0.6)}" r="0.6" fill="#fff"/>')
    s.append(f'<path d="M{f(x)},{f(cy + 6)} L{f(x)},{f(cy + 9)}" stroke="#000" stroke-width="1"/>')
    s.append(f'<path d="M{f(x)},{f(cy + 9)} C{f(x - 5)},{f(cy + 15)} {f(x - 5)},{f(cy + 21)} {f(x)},{f(cy + 22)} '
             f'C{f(x + 5)},{f(cy + 21)} {f(x + 5)},{f(cy + 15)} {f(x)},{f(cy + 9)} Z" fill="{DORADO}" stroke="#000" stroke-width="1.1"/>')
    s.append(f'<path d="M{f(x)},{f(cy + 13)} C{f(x - 2.6)},{f(cy + 16)} {f(x - 2.6)},{f(cy + 19)} {f(x)},{f(cy + 19.5)} '
             f'C{f(x + 2.6)},{f(cy + 19)} {f(x + 2.6)},{f(cy + 16)} {f(x)},{f(cy + 13)} Z" fill="#000"/>')
    s.append(f'<circle cx="{f(x - 0.8)}" cy="{f(cy + 16.5)}" r="0.7" fill="#fff"/>')
    return ''.join(s)

def borde_bordado(camino, paso, lado, color='#fff', semilla=0, flores=None, hojas=None):
    """Guarda bordada a lo largo de un borde: tallo ondulado con flores y hojas en ritmo fijo."""
    pts = cadena(camino, 60)
    acum = [0.0]
    for i in range(1, len(pts)):
        acum.append(acum[-1] + math.dist(pts[i - 1], pts[i]))
    s, tallo = [], []
    for i, (x, y) in enumerate(pts):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
        l = math.dist(a, b) or 1.0
        nx, ny = -(b[1] - a[1]) / l, (b[0] - a[0]) / l
        o = 2.4 * math.sin(acum[i] / paso * math.pi)
        tallo.append((x + nx * o, y + ny * o))
    s.append(f'<path d="{polilinea(tallo)}" stroke="{color}" stroke-width="0.9" fill="none"/>')
    d, k = paso / 2, semilla
    while d < acum[-1]:
        i = min(range(len(acum)), key=lambda j: abs(acum[j] - d))
        x, y = tallo[i]
        if k % 2 == 0:
            if flores:
                c = flores[(k // 2) % len(flores)]
                s.append(flor(x, y, 3.0, c).replace(f'stroke="{c}" stroke-width="0.6"', 'stroke="#000" stroke-width="0.6"'))
            else:
                s.append(flor(x, y, 3.0, color))
        else:
            a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
            ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
            s.append(hoja(x, y, ang + 40 * lado, hojas or color) + hoja(x, y, ang - 40 * lado + 180, hojas or color))
        d += paso / 2
        k += 1
    return ''.join(s)

TRENZA_34 = ([(166, 252), (150, 284), (146, 300), (142, 330), (138, 360), (136, 400), (134, 432)], 26, 16, 13)

def cinta_34():
    """Capa del retrato con la cinta roja al final de la trenza (se quita y se pone: doc 10 P31–P32)."""
    _, fin = trenza_34(*TRENZA_34)
    return mono_34(fin[0], fin[1] + 2)

def busto_34(variante):
    v = ['<clipPath id="r34-cara"><path d="' + CARA_34 + '"/></clipPath>',
         f'<clipPath id="r34-cuello"><path d="{CUELLO_34}"/></clipPath>']
    # pelo de atrás (nuca y cráneo; el rostro y el sombrero lo tapan)
    v.append(f'<path d="{PELO_ATRAS}" fill="#000"/>')
    if variante == 'mercado':
        # blusa con pechera bordada entre los paños del pañolón
        v.append('<path d="M172,296 C150,304 112,316 86,332 C70,346 62,390 58,480 L346,480 C342,400 338,356 326,336 '
                 f'C308,320 276,308 240,304 Z" fill="{TELA}" stroke="#000" stroke-width="2.6"/>')
        v.append(borde_bordado([(200, 330), (218, 337), (240, 336), (258, 328)], 10, 1, '#000', flores=(CINTAS[2], CINTAS[0]), hojas=CINTAS[1]))
        v.append('<path d="M196,334 L200,342 L196,350 L200,358 L196,366 L200,374 L196,382 L200,390 L196,398 L200,406 L196,414 L200,422 L196,430 L200,438 L196,446 L200,454 L196,462 L200,470 L196,478 '
                 'M258,334 L254,342 L258,350 L254,358 L258,366 L254,374 L258,382 L254,390 L258,398 L254,406 L258,414 L254,422 L258,430 L254,438 L258,446 L254,454 L258,462 L254,470 L258,478" stroke="#000" stroke-width="1" fill="none"/>')
        # motivo central: flor grande de ocho pétalos con hojas y abalorios
        cx, cy = 228, 368
        for i in range(8):
            a = math.pi * 2 * i / 8
            px, py = cx + 6.4 * math.cos(a), cy + 6.4 * math.sin(a)
            v.append(f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="3.8" ry="2.3" transform="rotate({f(math.degrees(a))} {f(px)} {f(py)})" fill="{CINTAS[2]}" stroke="#000" stroke-width="1"/>')
        v.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="#000"/>')
        v.append('<path d="M228,377 L228,446" stroke="#000" stroke-width="1.1" fill="none"/>')
        for y in (392, 412, 432):
            v.append(hoja(222, y, -30, CINTAS[1]).replace('/>', ' stroke="#000" stroke-width="0.5"/>') + hoja(234, y, 210, CINTAS[1]).replace('/>', ' stroke="#000" stroke-width="0.5"/>'))
        v.append(f'<path d="M228,446 L236,456 L228,466 L220,456 Z" fill="{CINTAS[0]}" stroke="#000" stroke-width="1"/>'
                 '<path d="M228,450 L232,456 L228,462 L224,456 Z" fill="none" stroke="#000" stroke-width="0.8"/>')
        for y in range(350, 476, 12):
            v.append(f'<circle cx="208" cy="{y}" r="1.5" fill="#000"/><circle cx="248" cy="{y}" r="1.5" fill="#000"/>')
        # pañolón negro de paño, con guarda bordada en los bordes delanteros
        cerca = ('M178,290 C150,298 112,312 86,330 C66,346 58,392 52,480 L178,480 C180,430 184,372 190,326 '
                 'C192,312 188,300 178,290 Z')
        lejos = ('M236,302 C268,306 302,318 322,336 C336,354 342,410 348,480 L266,480 C264,420 262,362 260,328 '
                 'C258,316 250,308 236,302 Z')
        v.append(f'<path d="{cerca}" fill="#000" stroke="#000" stroke-width="2.4" stroke-linejoin="round"/>')
        v.append(f'<path d="{lejos}" fill="#000" stroke="#000" stroke-width="2.4" stroke-linejoin="round"/>')
        v.append(borde_bordado([(182, 320), (178, 370), (174, 420), (170, 480)], 22, 1, flores=(CINTAS[2], CINTAS[0]), hojas=CINTAS[1]))
        v.append(borde_bordado([(266, 332), (268, 380), (270, 430), (272, 480)], 22, -1, semilla=1, flores=(CINTAS[0], CINTAS[2]), hojas=CINTAS[1]))
        v.append(pincel(suave([(174, 294), (140, 304), (106, 320), (84, 338)]), 2.4, 0.1, 0.5, '#fff'))
        for pts, w in [([(132, 316), (122, 350), (118, 384), (120, 412)], 1.7), ([(158, 312), (150, 344), (148, 372)], 1.3),
                       ([(102, 334), (90, 370), (84, 404), (82, 430)], 1.5), ([(118, 400), (112, 430), (110, 470)], 1.1),
                       ([(282, 314), (292, 342), (298, 376)], 1.2), ([(306, 328), (318, 360), (322, 392)], 1.0)]:
            v.append(pincel(suave(pts), w, 0.1, 0.1, '#fff'))
    elif variante == 'llano':
        # camisa caqui de hombre: hombro caído, dos bolsillos con tapa (el lejano más estrecho por la
        # perspectiva), tapeta con botones; cuello abierto en V (se dibuja después del cuello)
        cuerpo = ('M172,296 C150,304 112,316 86,332 C70,346 62,390 58,480 L346,480 C342,400 338,356 326,336 '
                  'C308,320 276,308 240,304 Z')
        v.append(f'<path d="{cuerpo}" fill="{CAQUI}" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>')
        v.append(recortar('r34-camisa', cuerpo,
            # lado lejano y bajo el brazo cercano en sombra
            f'<path d="M290,300 C310,330 322,380 330,480 L360,480 L360,300 Z" {SOMBRA_SUAVE}/>'
            f'<path d="M60,400 C74,420 88,450 96,480 L50,480 Z" {SOMBRA_SUAVE}/>'
            # costuras de las mangas (hombro caído) y pliegues que bajan del hombro
            + pincel(suave([(110, 318), (96, 356), (92, 404), (96, 452), (100, 480)]), 1.6, 0.3, 0.3)
            + pincel(suave([(308, 318), (320, 356), (326, 404), (330, 452)]), 1.3, 0.3, 0.3)
            + ''.join(pincel(suave(pts), w, 0.1, 0.1) for pts, w in [([(140, 330), (134, 356), (132, 380)], 1.1),
                                                                    ([(286, 330), (292, 352), (294, 372)], 1.0),
                                                                    ([(176, 440), (182, 460), (184, 480)], 1.0)])
            # bolsillos de pecho con tapa y botón
            + f'<path d="M116,382 L170,376 L172,436 L120,442 Z" fill="none" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/>'
            + f'<path d="M114,380 L172,373 L172,392 L144,400 L116,396 Z" fill="{CAQUI}" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/>'
            + '<circle cx="144" cy="394" r="2.4" fill="#fff" stroke="#000" stroke-width="1"/>'
            + f'<path d="M260,374 L298,378 L298,432 L262,428 Z" fill="none" stroke="#000" stroke-width="1.4" stroke-linejoin="round"/>'
            + f'<path d="M259,372 L299,376 L299,392 L280,397 L260,390 Z" fill="{CAQUI}" stroke="#000" stroke-width="1.4" stroke-linejoin="round"/>'
            + '<circle cx="280" cy="392" r="2" fill="#fff" stroke="#000" stroke-width="0.9"/>'
            # tapeta con botones bajo la V del cuello
            + pincel(suave([(222, 352), (224, 400), (226, 440), (228, 480)]), 1.3, 0.4, 0.4)
            + ''.join(f'<circle cx="{f(x)}" cy="{y}" r="2.6" fill="#fff" stroke="#000" stroke-width="1"/>' for x, y in [(219.6, 380), (221.2, 420), (222.8, 460)])
            + (remiendo([(88, 346), (126, 336), (132, 370), (94, 380)], LANA, 'r34-remiendo') if GASTADO else '')))
        # banda del cuello por detrás de la nuca
        v.append(f'<path d="M160,298 C170,284 196,278 222,282 C238,286 246,296 248,306 L240,310 C226,300 200,296 174,304 Z" fill="{CAQUI}" stroke="#000" stroke-width="2" stroke-linejoin="round"/>')
    else:
        # blusa: manga abullonada del brazo cercano, libre porque la ruana va terciada sobre ese hombro
        v.append('<path d="M156,300 C124,310 92,324 74,342 C60,360 56,420 54,480 L136,480 C134,430 132,382 138,344 Z" '
                 f'fill="{TELA}" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>')
        v.append('<path d="M84,336 C92,356 98,372 102,392 M104,326 C108,348 112,366 112,388 M124,318 C126,340 126,360 124,384 M76,360 C88,376 96,392 100,410" stroke="#000" stroke-width="1" fill="none"/>')
        # ruana de lana oscura: cuerpo, doblez terciado sobre el hombro cercano y cuello en rollo
        cuerpo = ('M178,292 C164,300 150,318 142,342 C132,372 126,430 124,480 L352,480 C348,410 342,360 330,338 '
                  'C314,318 280,304 244,300 C234,312 212,316 196,308 Z')
        v.append(f'<path d="{cuerpo}" fill="{RUANA}" stroke="#000" stroke-width="2.4" stroke-linejoin="round"/>')
        for pts, w in [([(166, 338), (158, 372), (154, 404)], 1.6), ([(212, 346), (210, 374), (208, 398)], 1.0),
                       ([(262, 326), (268, 360), (272, 394)], 1.6), ([(300, 336), (312, 370), (318, 404)], 1.2),
                       ([(150, 420), (146, 446), (144, 472)], 1.1), ([(282, 412), (288, 440), (290, 470)], 1.1)]:
            v.append(pincel(suave(pts), w, 0.1, 0.1, '#fff'))
        doblez = 'M180,288 C152,292 118,304 92,322 C82,330 84,344 96,346 C120,334 150,326 174,322 C188,316 190,300 180,288 Z'
        v.append(f'<path d="{doblez}" fill="{RUANA}" stroke="#000" stroke-width="2.4" stroke-linejoin="round"/>')
        v.append(pincel([(96, 344), (120, 332), (150, 324), (174, 320)], 2.2, 0.2, 0.4, '#fff'))
        v.append(f'<path d="M100,340 C124,330 150,322 172,318" stroke="{LANA}" stroke-width="2" fill="none"/>')
        v.append(recortar('r34-ruana-listas', cuerpo, f'<path d="M110,452 C180,446 280,446 360,454" stroke="{LANA}" stroke-width="3.2" fill="none"/>'
                                                     f'<path d="M110,462 C180,456 280,456 360,464" stroke="{LANA}" stroke-width="1.8" fill="none"/>'))
        v.append(pincel([(172, 292), (190, 314), (226, 320), (246, 302)], 12, 0.6, 0.7))
        v.append(pincel([(173, 293), (190, 313), (226, 318.5), (245, 302.5)], 8.4, 0.6, 0.7, RUANA))
        v.append(pincel([(176, 296), (194, 312), (224, 316), (242, 304)], 1.4, 0.2, 0.2, '#fff'))
    # cuello: sombra bajo la mandíbula, esternocleidomastoideo y hueco del esternón
    v.append(f'<path d="{CUELLO_34}" fill="{PIEL}" stroke="#000" stroke-width="2.4" stroke-linejoin="round"/>')
    v.append('<g clip-path="url(#r34-cuello)">'
             f'<path d="M176,236 C196,256 222,268 244,262 L244,284 C222,290 196,282 176,262 Z" fill="{PIEL_SOMBRA}"/>'
             '<path d="M176,250 C184,270 186,290 182,312 L170,312 L170,250 Z" fill="#000" fill-opacity="0.1"/></g>')
    v.append(pincel([(200, 276), (208, 288), (216, 298), (222, 305)], 1.0, 0.05, 0.5))
    v.append('<path d="M222,306 C226,310 230,310 234,306" stroke="#000" stroke-width="1" fill="none"/>')
    if variante == 'llano':
        # cuello abierto: la piel del pecho en V y las dos puntas del cuello camisero
        # (sin trazo arriba: tapa el borde del cuello, que aquí no termina en la blusa)
        v.append(f'<path d="M172,298 C192,314 206,334 218,356 C226,336 234,320 245,302 C226,310 198,310 172,298 Z" fill="{PIEL}"/>')
        v.append(pincel(suave([(220, 312), (225, 318), (231, 316)]), 1.2, 0.2, 0.2))
        v.append(f'<path d="M190,316 C200,328 210,342 217,354 C222,342 228,330 236,318 C220,322 204,322 190,316 Z" fill="{PIEL_SOMBRA}"/>')
        v.append(f'<path d="M168,292 C178,308 192,330 208,356 C190,350 168,336 146,318 C152,306 160,298 168,292 Z" fill="{CAQUI}" stroke="#000" stroke-width="2.2" stroke-linejoin="round"/>')
        v.append(pincel(suave([(170, 300), (182, 318), (196, 336)]), 1.0, 0.2, 0.2))
        v.append(f'<path d="M244,300 C240,318 234,334 226,350 C238,344 254,332 266,318 C260,310 252,304 244,300 Z" fill="{CAQUI}" stroke="#000" stroke-width="2" stroke-linejoin="round"/>')
        v.append(f'<path d="M244,300 C240,318 234,334 226,350 C236,342 246,330 252,318 Z" {SOMBRA_SUAVE}/>')
    else:
        escote = cadena([(172, 304), (196, 316), (222, 318), (240, 310)], 40)
        feston = []
        for i in range(0, len(escote) - 3, 3):
            (x0, y0), (x1, y1) = escote[i], escote[i + 3]
            feston.append(f'M{f(x0)},{f(y0 + 1)} Q{f((x0 + x1) / 2)},{f((y0 + y1) / 2 + 5.5)} {f(x1)},{f(y1 + 1)}')
        v.append(f'<path d="{" ".join(feston)}" stroke="#000" stroke-width="1" fill="none"/>')
    if variante == 'mercado':
        # gargantilla de abalorios en dos vueltas, en perspectiva (más chicas del lado lejano)
        for (amp, r, paso, oscura) in [(10, 2.6, 0, True), (20, 2.2, 0.5, False)]:
            for i in range(19):
                t = (i + paso) / 19
                x = 174 + (240 - 174) * t
                y = 298 + amp * math.sin(math.pi * t ** 0.85) + 8 * t
                rr = r * (1.1 - 0.35 * t)
                fill = '#000' if (i % 2 == 0) == oscura else CINTAS[(i // 2) % 3]
                v.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rr)}" fill="{fill}" stroke="#000" stroke-width="0.9"/>')
    # trenza por delante del hombro cercano, con la cinta roja
    trz, fin = trenza_34(*TRENZA_34)
    v.append(trz)
    v.append(f'<path d="M{f(fin[0] - 6)},{f(fin[1] - 1)} C{f(fin[0] - 2)},{f(fin[1] - 3)} {f(fin[0] + 2)},{f(fin[1] - 3)} {f(fin[0] + 6)},{f(fin[1] - 1)} '
             f'L{f(fin[0] + 5)},{f(fin[1] + 5)} C{f(fin[0] + 2)},{f(fin[1] + 3.4)} {f(fin[0] - 2)},{f(fin[1] + 3.4)} {f(fin[0] - 5)},{f(fin[1] + 5)} Z" fill="#000" stroke="#fff" stroke-width="0.8"/>')
    for (dx, dy, cx) in [(-7, 30, -4), (-3, 34, -1), (1, 33, 1), (5, 29, 4), (8, 24, 6)]:
        v.append(pincel([(fin[0] + dx * 0.3, fin[1] + 6), (fin[0] + cx, fin[1] + dy * 0.5), (fin[0] + dx, fin[1] + dy * 0.8), (fin[0] + dx, fin[1] + dy)], 2.2, 0.8, 0.05))
    # rostro, sombras y contorno de tinta variable
    v.append(f'<path d="{CARA_34}" fill="{PIEL}" stroke="#000" stroke-width="2" stroke-linejoin="round"/>')
    v.append('<g clip-path="url(#r34-cara)">'
             # lado lejano en sombra: de la sien al mentón, más ancho bajo el pómulo
             f'<path d="M270,182 C264,190 263,200 261,210 C258,220 254,230 252,240 C248,250 242,258 234,266 L280,280 L280,182 Z" fill="{PIEL_SOMBRA}"/>'
             # sombra que arroja la nariz
             f'<path d="M246,212 C252,213 257,215 259,220 C254,222.5 248,221 245,216 Z" fill="{PIEL_SOMBRA}"/>'
             '</g>')
    v.append(pincel(CONTORNO_LEJANO, 3.6, 0.5, 0.7))
    v.append(pincel(MANDIBULA, 3.2, 0.8, 0.3))
    # nariz: puente del lado lejano, punta redonda, ala y fosa cercanas
    v.append(pincel([(235, 163), (235.2, 167), (235.5, 171), (236, 175)], 0.9, 0.1, 0.1))
    v.append(pincel([(239.5, 186), (241.5, 190), (244, 193.5), (246.5, 196)], 1.4, 0.1, 0.6))
    v.append(pincel([(246, 196), (251, 200), (255, 205), (252, 210), (250, 213), (246, 214), (243, 212)], 2.0, 0.4, 0.3))
    v.append(pincel([(232, 199), (226, 202), (226, 210), (233, 212)], 1.8, 0.2, 0.6))
    v.append('<path d="M236,211 C238,208 242,208 244,210 C242,212 238,212.5 236,211 Z" fill="#000"/>')
    v.append('<ellipse cx="249.5" cy="201" rx="1.6" ry="1.1" fill="#fff"/>')
    # oreja cercana con zarcillo; el pelo tapa su borde de arriba
    v.append(f'<path d="{OREJA_34}" fill="{PIEL}" stroke="#000" stroke-width="2.2" stroke-linejoin="round"/>')
    v.append('<path d="M162,186 C158,190 158,198 163,203 L167,200 C165,194 165,190 166,186 Z" fill="#000" fill-opacity="0.18"/>')
    v.append(pincel([(167, 172), (157, 168), (150, 178), (151, 192), (153, 200), (156, 206), (160, 209)], 1.4, 0.2, 0.4))
    v.append(pincel([(165, 180), (159, 182), (157, 190), (161, 198)], 1.2, 0.3, 0.2))
    v.append('<path d="M170,192 C168,194 168,197 170,199" stroke="#000" stroke-width="1.1" fill="none"/>')
    v.append(zarcillo_34(164, 215))
    # pelo de la sien, que tapa el borde de la oreja, y brillos
    v.append(f'<path d="{PELO_SIEN}" fill="#000"/>')
    for pts, w in MECHAS_BRILLO:
        v.append(pincel([pts[0], pts[1], pts[2], pts[3]], w, 0.1, 0.1, '#fff'))
    if variante == 'monte':
        # raya al medio y mechones sueltos (la huida de noche)
        v.append(pincel([(234, 104), (230, 96), (222, 84), (206, 74)], 1.8, 0.6, 0.1, '#fff'))
        for pts, w in [([(214, 108), (208, 118), (204, 128), (202, 140)], 1.6), ([(206, 110), (196, 122), (190, 134), (190, 146)], 1.3),
                       ([(268, 120), (274, 132), (276, 146), (274, 158)], 1.3), ([(176, 130), (168, 140), (166, 152), (168, 162)], 1.2)]:
            v.append(pincel([pts[0], pts[1], pts[2], pts[3]], w, 0.8, 0.05))
        v.append('<path d="M156,90 C150,84 144,84 140,88 M188,74 C184,66 176,64 170,66 M246,82 C252,74 260,74 264,78 M126,150 C118,146 114,150 112,156" stroke="#000" stroke-width="1.3" fill="none" stroke-linecap="round"/>')
    else:
        # sombra del ala en la frente, barbuquejo por la mejilla cercana y bajo el mentón, sombrero
        llanero = variante == 'llano'
        borde = con_sombrero(SOMB_LLANERO, ala_frente) if llanero else ala_frente()
        franja = polilinea(borde) + ' ' + ' '.join(f'L{f(x)},{f(y + 6 + 9 * min(max((x - 168) / 100, 0), 1))}' for x, y in reversed(borde)) + ' Z'
        v.append(f'<g clip-path="url(#r34-cara)"><path d="{franja}" fill="{PIEL_SOMBRA}"/></g>')
        barb = [(170, 128), (173, 150), (174, 174), (174, 198), (176, 220), (182, 238), (194, 250), (210, 259), (224, 264)]
        d = ruta(suave(barb))
        puntas = 'M223,266 C221,270 220,274 221,278 M226,266 C228,269 230,272 232,274'
        v.append(f'<path d="{d} {puntas}" stroke="#000" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        barb_color = CUERO if llanero else CINTAS[1]  # barbuquejo de cuero en el Llano
        v.append(f'<path d="{d} {puntas}" stroke="{barb_color}" stroke-width="1.1" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        v.append(f'<circle cx="224" cy="264.5" r="2.6" fill="{barb_color}" stroke="#000" stroke-width="1"/>')
        v.append(con_sombrero(SOMB_LLANERO, lambda: sombrero_34(True)) if llanero else sombrero_34())
    return ''.join(v)

# ---------- rasgos por expresión ----------
def ojo_34(clave, cx, cy, ancho, arriba, abajo, iris, mira, lado, peso=1.0, tension=0.0):
    """Ojo en 3/4. lado=+1: lagrimal a la derecha (ojo cercano); -1: a la izquierda (ojo lejano).
    iris=(rx, ry); mira=(dx, dy) desde el centro; tension aplana el párpado de abajo (rabia)."""
    s = lado
    I = (cx + s * ancho / 2, cy + 1.0)
    O = (cx - s * ancho / 2, cy - 1.6)
    sup = [O, (O[0] + s * ancho * 0.22, cy - arriba * 1.35), (I[0] - s * ancho * 0.38, cy - arriba * 1.4), I]
    inf = [I, (I[0] - s * ancho * 0.3, cy + abajo * (1.25 - tension)), (O[0] + s * ancho * 0.28, cy + abajo * 1.25), O]
    almendra = (f'M{f(O[0])},{f(O[1])} C{f(sup[1][0])},{f(sup[1][1])} {f(sup[2][0])},{f(sup[2][1])} {f(I[0])},{f(I[1])} '
                f'C{f(inf[1][0])},{f(inf[1][1])} {f(inf[2][0])},{f(inf[2][1])} {f(O[0])},{f(O[1])} Z')
    ix, iy = cx + mira[0], cy + mira[1]
    rx, ry = iris
    out = [f'<clipPath id="r34-{clave}"><path d="{almendra}"/></clipPath>',
           f'<path d="{almendra}" fill="#fff"/>',
           f'<g clip-path="url(#r34-{clave})">'
           f'<ellipse cx="{f(ix)}" cy="{f(iy)}" rx="{f(rx)}" ry="{f(ry)}" fill="#000"/>'
           f'<ellipse cx="{f(ix)}" cy="{f(iy)}" rx="{f(rx * 0.62)}" ry="{f(ry * 0.62)}" fill="none" stroke="#fff" stroke-width="0.5" stroke-opacity="0.55"/>'
           f'<circle cx="{f(ix - rx * 0.35)}" cy="{f(iy - ry * 0.38)}" r="{f(min(rx, ry) * 0.3)}" fill="#fff"/>'
           f'<circle cx="{f(ix + rx * 0.38)}" cy="{f(iy + ry * 0.36)}" r="{f(min(rx, ry) * 0.13)}" fill="#fff"/>'
           f'<path d="M{f(O[0])},{f(O[1])} C{f(sup[1][0])},{f(sup[1][1])} {f(sup[2][0])},{f(sup[2][1])} {f(I[0])},{f(I[1])}" stroke="#000" stroke-opacity="0.26" stroke-width="5" fill="none"/>'
           '</g>']
    # párpado de arriba: grueso hacia afuera, con el remate de las pestañas
    out.append(pincel([(O[0] - s * 1.5, O[1] + 0.6), sup[1], sup[2], I], 3.4 * peso, 0.9, 0.25))
    k = 1.0 if s == 1 else 0.55
    out.append(pincel([(O[0] + s * 1, O[1] - 0.4), (O[0] - s * 2 * k, O[1] - 1.6 * k), (O[0] - s * 4 * k, O[1] - 2.6 * k), (O[0] - s * 6 * k, O[1] - 2.8 * k)], 2.2 * peso, 0.9, 0.05))
    # pliegue del párpado (bajo y que muere hacia el lagrimal) y párpado de abajo
    p0 = mezcla(sup[0], sup[1], 0.6)
    out.append(pincel([(p0[0], p0[1] - 3.2), (sup[1][0] + s * 2, sup[1][1] - 3.6), (sup[2][0], sup[2][1] - 2.6), (I[0] - s * 5, I[1] - arriba * 0.9 - 1.2)], 1.1, 0.2, 0.05))
    out.append(pincel([(I[0] - s * ancho * 0.25, inf[1][1] - abajo * 0.15), inf[2], inf[2], (O[0] + s * 1.5, O[1] + 0.8)], 1.1, 0.05, 0.6))
    out.append(f'<path d="M{f(I[0] - s * 2.4)},{f(I[1] - 1.2)} C{f(I[0] - s * 0.6)},{f(I[1] - 0.4)} {f(I[0] - s * 0.6)},{f(I[1] + 0.8)} {f(I[0] - s * 2.2)},{f(I[1] + 1.6)}" stroke="#000" stroke-width="0.8" fill="none"/>')
    return ''.join(out), almendra

def ceja_34(dentro, fuera, arco, grueso, lado):
    """Ceja gruesa en la cabeza (hacia la nariz) y fina en la cola, con pelos marcados al inicio."""
    m = mezcla(dentro, fuera, 0.45)
    s = [pincel([dentro, (m[0], m[1] + arco), (m[0] - lado * 4, m[1] + arco), fuera], grueso, 0.9, 0.08),
         f'<ellipse cx="{f(dentro[0] - lado * 0.6)}" cy="{f(dentro[1] + 0.3)}" rx="{f(grueso * 0.42)}" ry="{f(grueso * 0.5)}" fill="#000"/>']
    return ''.join(s)

# Parámetros por expresión: ojo cercano y lejano (centro, ancho, apertura arriba/abajo, iris, mirada),
# cejas (cabeza, cola, arco, grosor) y boca. Ver la tabla de expresiones de la hoja de personaje.
OJOS_34 = {
    'neutral': (dict(cx=197, cy=175, ancho=31, arriba=6.4, abajo=4.4, iris=(6.6, 6.8), mira=(3.0, 0.8)),
                dict(cx=249, cy=176, ancho=20, arriba=5.8, abajo=4.0, iris=(4.4, 5.8), mira=(1.6, 0.8))),
    'alerta': (dict(cx=197, cy=174.5, ancho=31, arriba=8.8, abajo=4.8, iris=(6.0, 6.3), mira=(5.4, -0.4)),
               dict(cx=249, cy=175.5, ancho=20, arriba=7.8, abajo=4.4, iris=(4.0, 5.3), mira=(3.0, -0.4))),
    'miedo': (dict(cx=197, cy=174, ancho=32, arriba=9.0, abajo=5.2, iris=(5.6, 5.8), mira=(1.8, 0.6)),
              dict(cx=249, cy=175, ancho=21, arriba=8.0, abajo=4.6, iris=(3.8, 5.0), mira=(1.0, 0.6))),
    'rabia': (dict(cx=197, cy=176, ancho=31, arriba=4.0, abajo=3.0, iris=(6.6, 6.8), mira=(3.4, 0.4), tension=0.55),
              dict(cx=249, cy=177, ancho=20, arriba=3.6, abajo=2.8, iris=(4.4, 5.8), mira=(1.8, 0.4), tension=0.55)),
    'duelo': (dict(cx=197, cy=176, ancho=30, arriba=3.8, abajo=4.4, iris=(6.6, 6.8), mira=(1.0, 3.2)),
              dict(cx=249, cy=177, ancho=19, arriba=3.4, abajo=4.0, iris=(4.4, 5.8), mira=(0.4, 3.2))),
}
CEJAS_34 = {  # (cabeza, cola, arco, grosor) cercana y lejana
    'neutral': (((213, 158), (178, 160), -5, 5.0), ((238, 159), (264, 160), -3.5, 4.2)),
    'alerta': (((213, 155), (178, 154), -2, 5.2), ((238, 156), (264, 154), -1.5, 4.4)),
    'miedo': (((212, 148), (178, 156), -6, 4.6), ((239, 149), (264, 155), -4.5, 3.9)),
    'rabia': (((214, 165), (178, 156), -1.5, 6.0), ((237, 166), (264, 157), -1, 5.0)),
    'duelo': (((212, 152), (178, 163), -2, 4.8), ((239, 153), (264, 163), -1.5, 4.0)),
}
BOCAS_34 = {
    'neutral': ('',
                [(218, 233.6), (228, 232.4), (236, 231.4), (241, 231.4), (246, 231), (250, 231), (254, 231.6), (258, 233)],
                [(229, 239), (236, 241.4), (244, 241.4), (250, 239)]),
    'alerta': ('',
               [(223, 233), (229, 232.4), (236, 232), (241, 232.2), (246, 232), (250, 232), (253, 232.4), (255, 233)],
               [(232, 238.2), (237, 239.2), (243, 239.2), (248, 238)]),
    'miedo': ('<path d="M228,232.6 C233,230.8 239,230.4 244,230.6 C248,230.8 251,231.6 253,233 '
              'C252,238.4 248,241.8 241.4,242.2 C234.6,242.2 229.6,238.6 228,232.6 Z" fill="#000"/>'
              f'<ellipse cx="241" cy="240" rx="6.4" ry="1.9" fill="{PIEL_SOMBRA}"/>'
              '<path d="M231,233 C236,231.8 244,231.6 250.6,233 C249,234.6 244,235 240.4,235 C236,235 233,234.4 231,233 Z" fill="#fff"/>',
              [(225, 234), (231, 231.6), (237, 230.6), (243, 230.6), (248, 231), (252, 232), (255, 233.6)],
              [(231, 245.6), (237, 247.2), (244, 247), (249, 245.2)]),
    'rabia': ('',
              [(219, 235.6), (226, 233.4), (234, 232.4), (241, 232.4), (247, 232.4), (252, 233), (255, 234), (258, 236)],
              [(231, 240.6), (237, 241.6), (244, 241.6), (249, 240.4)]),
    'duelo': ('',
              [(219, 237), (226, 234), (234, 232.6), (241, 232.4), (246, 232.4), (251, 233), (255, 234.6), (258, 237.4)],
              [(229, 241.6), (236, 243.6), (244, 243.4), (250, 241.4)]),
}

def labios_34(labio, inferior):
    """Labio superior (mira abajo: en sombra, con arco de Cupido) e inferior (recibe luz)."""
    x0, x1 = labio[0][0], labio[-1][0]
    def alto(x):
        t = min(max((x - x0) / (x1 - x0), 0.0), 1.0)
        return 4.4 * math.sin(math.pi * t) ** 0.8 - 1.5 * math.exp(-((x - 242.5) / 2.0) ** 2)
    linea = cadena(suave(labio), 6)
    sup = linea + [(x, y - alto(x)) for x, y in reversed(linea)]
    medio = [(x, y) for x, y in linea if inferior[0][0] - 5 <= x <= inferior[-1][0] + 3]
    inf = medio + cadena(suave([(inferior[-1][0] + 1.5, inferior[-1][1] - 1.6)] + inferior[::-1] + [(inferior[0][0] - 3, inferior[0][1] - 2)]), 6)
    a, d = inferior[1], inferior[2]
    return (f'<path d="{polilinea(inf, True)}" fill="{CHAPAS}"/>'
            f'<path d="{polilinea(sup, True)}" fill="{PIEL_SOMBRA}"/>'
            f'<path d="M{f(a[0] - 3)},{f(a[1] + 1.4)} C{f(a[0] + 1)},{f(a[1] + 5.4)} {f(d[0] - 1)},{f(d[1] + 5.4)} {f(d[0] + 3)},{f(d[1] + 1.4)} Z" fill="{PIEL_SOMBRA}"/>')

def boca_34(expr):
    relleno, labio, inferior = BOCAS_34[expr]
    s = [labios_34(labio, inferior), relleno]
    l = labio
    s.append(pincel(suave(labio), 3.0 if expr != 'rabia' else 3.6, 0.35, 0.3, n=8))
    s.append(f'<path d="M{f(l[0][0] - 1)},{f(l[0][1] - 1.6)} C{f(l[0][0] - 2.4)},{f(l[0][1])} {f(l[0][0] - 2)},{f(l[0][1] + 1.6)} {f(l[0][0])},{f(l[0][1] + 2.6)}" stroke="#000" stroke-width="1" fill="none"/>')
    s.append(pincel(suave(inferior), 1.4, 0.1, 0.1, n=8))
    if expr != 'miedo':
        a, d = inferior[1], inferior[2]
        s.append(f'<path d="M{f(a[0] + 1.5)},{f(a[1] - 3.2)} C{f(a[0] + 3)},{f(a[1] - 3.8)} {f(d[0] - 3)},{f(d[1] - 3.8)} {f(d[0] - 1.5)},{f(d[1] - 3.4)}" stroke="#fff" stroke-width="0.9" fill="none" stroke-linecap="round"/>')
    return ''.join(s)

CHAPAS_34 = f'<ellipse cx="188" cy="205" rx="13" ry="6.5" transform="rotate(-8 188 205)" fill="{CHAPAS}"/>'
RUBOR_34 = ''.join(pincel([(180 + 5.5 * i, 202.5 - 0.6 * i), (178.6 + 5.5 * i, 205), (177.6 + 5.5 * i, 207), (176.4 + 5.5 * i, 209)], 0.9, 0.2, 0.2) for i in range(3))

def ojos_cejas_34(expr, peso):
    (c, l) = OJOS_34[expr]
    (cc, cl) = CEJAS_34[expr]
    ojo_c, alm_c = ojo_34(f'{expr}-c', lado=1, peso=peso, **c)
    ojo_l, alm_l = ojo_34(f'{expr}-l', lado=-1, peso=peso * 0.85, **l)
    cejas = ceja_34(cc[0], cc[1], cc[2], cc[3], 1) + ceja_34(cl[0], cl[1], cl[2], cl[3], -1)
    return ojo_c, ojo_l, alm_c, alm_l, cejas

GOTA_MIEDO = ('<path d="M263,158 C261.2,162 260.6,164.6 261.2,166.4 C261.8,168.2 264.4,168.2 265,166.4 C265.6,164.6 264.8,162 263,158 Z" fill="#fff" stroke="#000" stroke-width="0.9"/>'
              '<path d="M262,164.6 C262,165.6 262.6,166.4 263.4,166.6" stroke="#000" stroke-width="0.5" fill="none"/>')

def rasgos_34(expr):
    peso = 1.15 if expr == 'rabia' else 1.0
    ojo_c, ojo_l, _, _, cejas = ojos_cejas_34(expr, peso)
    s = []
    if expr in ('neutral', 'alerta', 'rabia'):
        s.append(CHAPAS_34)
    if expr in ('neutral', 'alerta', 'duelo'):
        s.append(RUBOR_34)
    if expr == 'rabia':
        s.append(RUBOR_34.replace('fill="#000"', 'fill="#000" transform="translate(0 -1)"') + RUBOR_34.replace('fill="#000"', 'fill="#000" transform="translate(2 4)"'))
        s.append(pincel([(224, 158), (225, 162), (225, 166), (224, 170)], 1.4, 0.2, 0.2) + pincel([(229, 159), (230, 163), (230, 167), (229, 170)], 1.2, 0.2, 0.2))
        s.append(pincel([(230, 198), (222, 204), (216, 216), (216, 228)], 1.5, 0.6, 0.1))
        s.append(pincel([(226, 196), (230, 194), (236, 194), (240, 197)], 1.4, 0.2, 0.6))
        s.append(pincel([(184, 224), (188, 230), (190, 236), (190, 242)], 1.2, 0.1, 0.1))
    if expr == 'miedo':
        s.append(pincel([(219, 151), (222, 147.4), (226, 146.6), (230, 148)], 0.9, 0.1, 0.1))
        s.append(GOTA_MIEDO)
        s.append(pincel([(230, 199), (225, 202), (224, 211), (232, 214)], 1.4, 0.2, 0.5))
    if expr == 'duelo':
        s.append(pincel([(184, 186), (190, 189.6), (198, 190), (206, 187)], 0.9, 0.1, 0.1))
        s.append('<path d="M210,180 C211,190 212,198 212,206" stroke="#000" stroke-width="0.9" fill="none"/>'
                 '<path d="M212,205 C209,210 208,214 210,217 C212,220 216,219 217,216 C218,213 215,209 212,205 Z" fill="#fff" stroke="#000" stroke-width="1.1"/>'
                 '<path d="M211,213 C211,215 212,216 213.4,216.4" stroke="#000" stroke-width="0.6" fill="none"/>')
        s.append('<path d="M232,249 L233,252 M237,250 L238,253 M242,249.6 L243,252.6" stroke="#000" stroke-width="0.9" stroke-linecap="round"/>')
    s += [ojo_c, ojo_l, cejas, boca_34(expr)]
    return ''.join(s)

def parpado_34(expr):
    """Ojos cerrados: papel sobre la almendra y el párpado abierto, párpado cerrado con pestañas y las cejas."""
    peso = 1.15 if expr == 'rabia' else 1.0
    (c, l) = OJOS_34[expr]
    _, _, _, _, cejas = ojos_cejas_34(expr, peso)
    s = [f'<clipPath id="r34-cara"><path d="{CARA_34}"/></clipPath><g clip-path="url(#r34-cara)">']
    for o, lado in ((c, 1), (l, -1)):
        cx, cy, w = o['cx'], o['cy'], o['ancho']
        I = (cx + lado * w / 2, cy + 1.0)
        O = (cx - lado * w / 2, cy - 1.6)
        arr = o['arriba'] * 1.4 + 5.5
        s.append(f'<path d="M{f(O[0] - lado * 7.5)},{f(O[1] - 3.5)} C{f(O[0] + lado * w * 0.1)},{f(cy - arr)} {f(I[0] - lado * w * 0.3)},{f(cy - arr - 1)} {f(I[0] + lado * 0.6)},{f(I[1] - 1)} '
                 f'C{f(I[0])},{f(cy + o["abajo"] * 1.5 + 1)} {f(O[0] + lado * w * 0.3)},{f(cy + o["abajo"] * 1.6 + 1.5)} {f(O[0] - lado * 4)},{f(O[1] + 2)} Z" fill="{PIEL}"/>')
        cierre = [(O[0] - lado * 1.5, O[1] + 0.6), (O[0] + lado * w * 0.3, cy + 4.2), (I[0] - lado * w * 0.3, cy + 4.0), I]
        s.append(pincel(cierre, 3.0 * peso * (1 if lado == 1 else 0.85), 0.9, 0.3))
        for t in (0.18, 0.32, 0.46):
            x = O[0] + lado * w * t
            y = cy + 2.6 + 1.6 * math.sin(math.pi * t)
            s.append(f'<path d="M{f(x)},{f(y)} L{f(x - lado * 1.6)},{f(y + 3.4)}" stroke="#000" stroke-width="1" stroke-linecap="round"/>')
        s.append(pincel([(O[0] + lado * 3, cy - 2.4), (O[0] + lado * w * 0.35, cy - 1), (I[0] - lado * w * 0.3, cy - 1), (I[0] - lado * 4, cy - 1.6)], 1.0, 0.1, 0.1))
    s.append('</g>')
    s.append(cejas)
    if expr == 'miedo':
        s.append(GOTA_MIEDO)
    return ''.join(s)

def hoja_retrato():
    ranuras = [('base-mercado', busto_34('mercado'), 'Base del retrato, traje de mercado (rostro sin rasgos)'),
               ('base-monte', busto_34('monte'), 'Base del retrato, variante monte (rostro sin rasgos)')]
    if 'rosalba-llano' in ACTOS_ROSALBA[ACTO]:
        ranuras.append(('base-llano', busto_34('llano'), 'Base del retrato, variante Llano (rostro sin rasgos)'
                        + (', traje gastado' if GASTADO else '')))
    ranuras += [('cinta', cinta_34(), 'Cinta roja de la trenza, sobre la base (se quita y se pone)')]
    ranuras += [(f'rasgos-{e}', rasgos_34(e), f'Rasgos del retrato: {e}') for e in EXPRESIONES]
    ranuras += [(f'parpado-{e}', parpado_34(e), f'Parpadeo del retrato: {e}') for e in EXPRESIONES]
    piezas = []
    for i, (pid, cuerpo, comentario) in enumerate(ranuras):
        tx = i * RET_W
        cuerpo = cuerpo.replace('id="r34-', f'id="{pid}-r34-').replace('url(#r34-', f'url(#{pid}-r34-')
        piezas.append(piece(pid, f'{f(tx + RET_W / 2)} {RET_H}', f'<g transform="translate({tx} 0)">{cuerpo}</g>', comentario))
    ancho = RET_W * len(ranuras)
    cuerpo = encabezado('Rosalba Insuasty — retrato en tres cuartos (viñetas y diálogos).',
                        'Base por variante + rasgos por expresión + parpadeo; todas las piezas con el pivote al pie del busto.')
    cuerpo = cuerpo.replace('width="300" height="500" viewBox="0 0 300 500"', f'width="{ancho}" height="{RET_H}" viewBox="0 0 {ancho} {RET_H}"')
    escribir(os.path.join(OUTDIR, 'rosalba-retrato.svg'), cuerpo + ''.join(piezas) + '\n</svg>\n')

hoja_retrato()

# ======================= 6. la cinta suelta (objeto del Prólogo b2) =======================
# Aurelio le jala la trenza y se queda con la cinta; Heliodoro se la devuelve (doc 02 Prólogo b2,
# doc 10 P32). Cinta desatada, cogida por un punto: dos tiras que cuelgan con alguna vuelta,
# tinta plana de partido (rojo liberal, revés en rojo-sombra) con borde de tinta (paleta.md).
ROJO_SOMBRA = PALETA['rojo-sombra']

def cinta_suelta(escala, ox, oy):
    """Cinta cogida por (ox, oy); escala 1 = la del personaje en escena, 2,2 = la del retrato."""
    tiras = [  # (eje que pasa por los puntos, vueltas en t, ancho)
        ([(0, 0), (-2, 12), (-7, 24), (-4, 38), (2, 50), (-1, 63), (-6, 76)], (0.42, 0.8), 3.8),
        ([(0, 0), (3, 10), (9, 20), (7, 32), (10, 44), (15, 53)], (0.58,), 3.6),
    ]
    out = []
    for eje, vueltas, ancho in tiras:
        pts = cadena(suave([(ox + x * escala, oy + y * escala) for x, y in eje]), 10)
        m = len(pts)
        tramos, actual, cara = [], [], True
        for i, (x, y) in enumerate(pts):
            t = i / (m - 1)
            a, b = pts[max(i - 1, 0)], pts[min(i + 1, m - 1)]
            l = math.dist(a, b) or 1.0
            nx, ny = -(b[1] - a[1]) / l, (b[0] - a[0]) / l
            fase = min([abs(t - v) for v in vueltas] + [1])
            w = ancho * escala / 2 * min(1.0, 0.12 + fase / 0.07)
            actual.append(((x + nx * w, y + ny * w), (x - nx * w, y - ny * w)))
            if fase < 0.004 and len(actual) > 2:
                tramos.append((actual, cara))
                actual, cara = [actual[-1]], not cara
        tramos.append((actual, cara))
        for k, (par, frente) in enumerate(tramos):
            izq = [p for p, _ in par]
            der = [q for _, q in par]
            if k == len(tramos) - 1:  # punta cortada en cola de golondrina
                (x, y) = pts[-1]
                medio = (x - (pts[-1][0] - pts[-3][0]) * 0.6, y - (pts[-1][1] - pts[-3][1]) * 0.6)
                izq = izq + [medio]
            out.append(f'<path d="{polilinea(izq + der[::-1], True)}" fill="{R if frente else ROJO_SOMBRA}" stroke="#000" '
                       f'stroke-width="{f(1.1 * escala ** 0.6)}" stroke-linejoin="round"/>')
    # la arruga donde estuvo el nudo, entre los dedos
    out.append(f'<ellipse cx="{f(ox)}" cy="{f(oy + 1 * escala)}" rx="{f(2.2 * escala)}" ry="{f(1.5 * escala)}" fill="{R}" stroke="#000" stroke-width="{f(1.1 * escala ** 0.6)}"/>'
               f'<path d="M{f(ox - 1.6 * escala)},{f(oy)} C{f(ox - 0.4 * escala)},{f(oy + 1.4 * escala)} {f(ox + 0.6 * escala)},{f(oy + 1.4 * escala)} {f(ox + 1.6 * escala)},{f(oy + 0.2 * escala)}" '
               f'stroke="{ROJO_SOMBRA}" stroke-width="{f(0.9 * escala ** 0.6)}" fill="none"/>')
    return ''.join(out)

def hoja_cinta():
    piezas = [piece('cinta-suelta', '40 10', cinta_suelta(1, 40, 10), 'Cinta suelta a la escala del personaje; pivote donde se coge'),
              piece('cinta-suelta-vineta', '168 22', cinta_suelta(2.2, 168, 22), 'Cinta suelta a la escala del retrato (viñetas)')]
    cuerpo = encabezado('Cinta roja de Rosalba, suelta (objeto del Prólogo b2).',
                        'Doc 02 Prólogo b2 y doc 10 P31–P32: Aurelio se queda con la cinta y Heliodoro se la devuelve.')
    cuerpo = cuerpo.replace('width="300" height="500" viewBox="0 0 300 500"', 'width="256" height="200" viewBox="0 0 256 200"')
    escribir(os.path.join(OUTDIR, 'cinta-roja.svg'), cuerpo + ''.join(piezas) + '\n</svg>\n')

hoja_cinta()

# ======================= 7. corriendo, monte (huida de la M2) =======================
# Doc 02, M2 «sigilo y huida», beat 4: huida por los cultivos y la quebrada. Con la falda de
# frisa casi al tobillo no se corre: la mano derecha la recoge por delante, a la altura del
# muslo, y el ruedo sube hasta la rodilla (se ven la enagua y las canillas). El torso se
# inclina adelante y el cuerpo baja; la cabeza va derecha, así le sirven las cabezas por
# expresión de pie. Las canillas giran en la rodilla, oculta bajo la falda
# (core/animacion/carrera.ts); misma base de apoyo (150, 474) que las demás poses.
INCL, AGACHE = 14, 10
TRANS_TORSO = f'translate(0 {AGACHE}) rotate({INCL} 146 240)'

def T(x, y):
    px, py = rot_punto(x, y, INCL, 146, 240)
    return (px, py + AGACHE)

CUELLO_C = T(150, 130)
DXC, DYC = CUELLO_C[0] - 150, CUELLO_C[1] - 130
TRANS_CABEZA = f'translate({f(DXC)} {f(DYC)})'
GIRO_TRENZA = 22
TRANS_TRENZA = f'{TRANS_CABEZA} rotate({GIRO_TRENZA} 134 110)'
RODILLA_DER, RODILLA_IZQ = (157, 346), (133, 346)

def pierna_carrera(dx, lejana=False):
    """Canilla entera (de la rodilla al tobillo) con su alpargata; pivote en la rodilla."""
    def P(x, y): return f"{f(x + dx)},{f(y)}"
    sw = 2.2 if lejana else 2.6
    d = (f'M{P(151,338)} L{P(163,338)} C{P(164,370)} {P(163,410)} {P(163,430)} L{P(164,452)} L{P(152,452)} '
         f'C{P(151,436)} {P(152,424)} {P(150,410)} C{P(146,392)} {P(146,370)} {P(151,338)} Z')
    s = f'<path d="{d}" fill="{PIEL}" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>'
    s += f'<path d="M{P(150,372)} C{P(149,392)} {P(150,410)} {P(152,426)} L{P(155,426)} C{P(153,410)} {P(152,392)} {P(153,372)} Z" {SOMBRA_SUAVE}/>'
    if lejana:
        s += f'<path d="{d}" {SOMBRA}/>'
    # la canilla corta de la alpargata (la de pie) sobra: aquí la pierna entera ya está dibujada
    pie = re.sub(r'<path d="M' + re.escape(f'{f(151 + dx)},430') + r' [^"]*" [^>]*/>', '', alpargata(dx, lejana))
    return s + pie

# ruedo recogido: de la esquina delantera (bajo el puño) a la de atrás, que vuela hacia atrás
RUEDO_C = cadena(suave([(187, 366), (172, 375), (156, 385), (138, 398), (118, 411), (99, 419), (84, 418)]), 12)

def ruedo_y(x, sube=0.0):
    pts = sorted(RUEDO_C)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / ((x1 - x0) or 1) - sube
    return (pts[0][1] if x < pts[0][0] else pts[-1][1]) - sube

FALDA_C = ('M124,236 L170,244 C174,250 178,262 184,274 C190,286 194,300 193,316 C192,332 190,350 187,366 '
           + ' '.join(f'L{f(x)},{f(y)}' for x, y in RUEDO_C[1:]) +
           ' C86,396 92,350 101,310 C108,280 116,254 124,236 Z')

def banda_c(o1, o2, color):
    xs = [84 + i * 2 for i in range(53)]
    arriba = [(x, ruedo_y(x, o2)) for x in xs]
    abajo = [(x, ruedo_y(x, o1)) for x in reversed(xs)]
    return f'<path d="{polilinea(arriba + abajo, True)}" fill="{color}" stroke="#000" stroke-width="1.2" stroke-linejoin="round"/>'

def zigzag_c(o1, o2):
    pts, x, arriba = [], 86, True
    while x < 188:
        pts.append((x, ruedo_y(x, (o2 - 1.5) if arriba else (o1 + 1.5))))
        x += 8; arriba = not arriba
    return f'<path d="{polilinea(pts)}" stroke="#000" stroke-width="1.3" fill="none"/>'

def rombos_c(o1, o2):
    out, x = [], 90
    while x < 184:
        cy = ruedo_y(x, (o1 + o2) / 2)
        out.append(f'<path d="M{f(x)},{f(cy - 3.5)} L{f(x + 3)},{f(cy)} L{f(x)},{f(cy + 3.5)} L{f(x - 3)},{f(cy)} Z" fill="#000"/>')
        x += 13
    return ''.join(out)

PUNO_C = (185, 279)
falda_c = (
    f'<path d="{FALDA_C}" fill="{FALDA}" stroke="#000" stroke-width="3.2" stroke-linejoin="round"/>'
    + recortar('falda-c-marcas', FALDA_C,
        f'<path d="M124,236 C114,262 104,300 96,340 C90,370 86,396 84,418 L104,418 C104,380 110,320 128,250 Z" {SOMBRA_HONDA}/>'
        f'<path d="M{PUNO_C[0]},{PUNO_C[1]} L176,372 L150,390 Z" {SOMBRA_SUAVE}/>'
        # la tela recogida tira desde el puño: pliegues que abren hacia el ruedo
        + ''.join(pincel(suave([PUNO_C, mezcla(PUNO_C, h, 0.45), h]), w, 0.7, 0.1)
                  for h, w in [((178, 372), 1.6), ((160, 384), 1.5), ((138, 400), 1.4), ((116, 413), 1.2)])
        + ''.join(pincel(suave([(PUNO_C[0] - 3, PUNO_C[1] + 6), mezcla(PUNO_C, h, 0.5), h]), 1.3, 0.2, 0.1, '#fff', extra=' fill-opacity="0.5"')
                  for h in [(168, 378), (148, 392), (127, 406)])
        + pincel(suave([(132, 252), (124, 300), (112, 360), (100, 412)]), 1.4, 0.1, 0.1, '#fff', extra=' fill-opacity="0.5"')
        + banda_c(4, 16, CINTAS[2]) + rombos_c(4, 16)
        + banda_c(20, 26, CINTAS[1])
        + banda_c(30, 38, CINTAS[0]) + zigzag_c(30, 38)
        + barro([(100, 414), (124, 406), (146, 394), (170, 380)], 4))
    + f'<path d="{FALDA_C}" fill="none" stroke="#000" stroke-width="3.2" stroke-linejoin="round"/>'
    + '<path d="M124,236 L170,244 L169.4,252 L123,244 Z" fill="#000"/>'
)

# enagua: asoma bajo el ruedo recogido, con su festón y barro
ENAGUA_C = ('M188,' + f(ruedo_y(188, 30)) + ' ' + ' '.join(f'L{f(x)},{f(ruedo_y(x, 30))}' for x in range(184, 86, -6))
            + f' L86,{f(ruedo_y(86, 30))} L86,{f(ruedo_y(86, -9))} '
            + ' '.join(f'Q{f(x - 3)},{f(ruedo_y(x - 3, -13))} {f(x)},{f(ruedo_y(x, -9))}' for x in range(92, 190, 6))
            + ' Z')
enagua_c = (f'<path d="{ENAGUA_C}" fill="{TELA}" stroke="#000" stroke-width="1.8" stroke-linejoin="round"/>'
            + recortar('enagua-c-sombra', ENAGUA_C, f'<path d="M80,{f(ruedo_y(80, 40))} L190,{f(ruedo_y(190, 40))} L190,{f(ruedo_y(190, -3))} L80,{f(ruedo_y(80, -3))} Z" {SOMBRA}/>')
            + barro([(96, 425), (122, 416), (150, 400), (176, 386)], 5))

# brazo derecho recogiendo la falda: hombro → codo → muñeca (IK con el codo atrás) y puño
def ik(s, w, l1, l2):
    d = math.dist(s, w)
    a = math.acos(max(-1.0, min(1.0, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d))))
    base = math.atan2(w[1] - s[1], w[0] - s[0])
    ang = base + a  # codo hacia atrás (a la izquierda de la línea hombro → muñeca)
    return (s[0] + l1 * math.cos(ang), s[1] + l1 * math.sin(ang))

HOMBRO_C = T(153, 140)
MUNECA_C = (180, 262)
CODO_C = ik(HOMBRO_C, MUNECA_C, 60, 54)
_u = ((MUNECA_C[0] - CODO_C[0]) / math.dist(CODO_C, MUNECA_C), (MUNECA_C[1] - CODO_C[1]) / math.dist(CODO_C, MUNECA_C))

def puno_c(muneca=None, u=None, tela=True, escala=1.0):
    """Puño cerrado: nudillos adelante, pulgar encima del índice; con tela, la falda asoma."""
    muneca = muneca or MUNECA_C
    u = u or _u
    cx, cy = muneca[0] + u[0] * 14 * escala, muneca[1] + u[1] * 14 * escala
    ang = math.degrees(math.atan2(u[1], u[0])) - 90
    g = f'<g transform="translate({f(cx)} {f(cy)}) rotate({f(ang)}) scale({f(escala)})">'
    if tela:
        # tela recogida que sale por arriba y por abajo del puño
        g += f'<path d="M-6,-9 C-9,-14 -4,-17 0,-13 C3,-17 8,-14 6,-9 Z" fill="{FALDA}" stroke="#000" stroke-width="1.4"/>'
        g += f'<path d="M-5,8 C-9,14 -6,19 -1,15 C2,20 8,17 5,9 Z" fill="{FALDA}" stroke="#000" stroke-width="1.4"/>'
    g += (f'<path d="M-8,-8 C-9,-2 -9,4 -7,9 C-3,11 3,11 7,9 C10,4 10,-2 8,-8 C4,-11 -4,-11 -8,-8 Z" fill="{PIEL}" stroke="#000" stroke-width="2" stroke-linejoin="round"/>')
    # nudillos y pliegues de los dedos, y el pulgar cruzado
    g += '<path d="M8,-6 C10,-4 10,-1 8.6,0.6 M8.8,1.6 C10.4,3.4 10,6 8,7.4" stroke="#000" stroke-width="1.1" fill="none"/>'
    g += '<path d="M2,-7 L2.4,7 M-2.6,-7.4 L-2.4,7.6" stroke="#000" stroke-width="0.8" fill="none"/>'
    g += f'<path d="M-8,-2 C-4,-4 2,-4 6,-1 C5,1 1,1.6 -3,1 C-6,0.6 -8,0 -8,-2 Z" fill="{PIEL}" stroke="#000" stroke-width="1.4" stroke-linejoin="round"/>'
    return g + '</g>'

brazo_c = (f'<path d="{tubo(HOMBRO_C, CODO_C, 10.5, 8)}" fill="{TELA}" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>'
           + ''.join(f'<path d="M{f(a[0])},{f(a[1])} L{f(b[0])},{f(b[1])}" stroke="#000" stroke-width="0.9"/>'
                     for a, b in [(punto_en(HOMBRO_C, CODO_C, 0.06, o), punto_en(HOMBRO_C, CODO_C, 0.24, o * 0.9)) for o in (-5, 0, 5)])
           + f'<path d="{tubo(punto_en(HOMBRO_C, CODO_C, 0.25, -5), punto_en(HOMBRO_C, CODO_C, 0.92, -4), 2.6, 2)}" {SOMBRA_SUAVE}/>')
_pu1, _pu2 = punto_en(CODO_C, MUNECA_C, 0.8), punto_en(CODO_C, MUNECA_C, 1.02)
antebrazo_c = (f'<path d="{tubo(CODO_C, MUNECA_C, 7.8, 6.4)}" fill="{TELA}" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>'
               + f'<path d="{tubo(punto_en(CODO_C, MUNECA_C, 0.1, -4.5), punto_en(CODO_C, MUNECA_C, 0.76, -3.6), 2, 1.6)}" {SOMBRA_SUAVE}/>'
               + puno_c()
               + f'<path d="{tubo(_pu1, _pu2, 7.4, 7.2)}" fill="{TELA}" stroke="#000" stroke-width="2"/>'
               + ''.join(f'<circle cx="{f(punto_en(_pu1, _pu2, 0.5, o)[0])}" cy="{f(punto_en(_pu1, _pu2, 0.5, o)[1])}" r="0.9" fill="#000"/>' for o in (-4, 0, 4)))

# brazo izquierdo (lejano) de la carrera: cuelga en reposo; la animación lo dobla y bracea
HOMBRO_IZQ_C = T(141, 144)
CODO_IZQ_C = (HOMBRO_IZQ_C[0] + 2, HOMBRO_IZQ_C[1] + 57)
MUNECA_IZQ_C = (CODO_IZQ_C[0] + 2, CODO_IZQ_C[1] + 50)
_ui = (2 / math.hypot(2, 50), 50 / math.hypot(2, 50))
brazo_izq_c = (f'<path d="{tubo(HOMBRO_IZQ_C, CODO_IZQ_C, 9.5, 7.6)}" fill="{TELA}" stroke="#000" stroke-width="2.2" stroke-linejoin="round"/>'
               f'<path d="{tubo(HOMBRO_IZQ_C, CODO_IZQ_C, 9.5, 7.6)}" {SOMBRA}/>')
_pi1, _pi2 = punto_en(CODO_IZQ_C, MUNECA_IZQ_C, 0.8), punto_en(CODO_IZQ_C, MUNECA_IZQ_C, 1.02)
antebrazo_izq_c = (f'<path d="{tubo(CODO_IZQ_C, MUNECA_IZQ_C, 7.2, 6)}" fill="{TELA}" stroke="#000" stroke-width="2.2" stroke-linejoin="round"/>'
                   + puno_c(MUNECA_IZQ_C, _ui, tela=False, escala=0.92)
                   + f'<path d="{tubo(_pi1, _pi2, 7, 6.8)}" fill="{TELA}" stroke="#000" stroke-width="1.8"/>'
                   + f'<path d="{tubo(CODO_IZQ_C, MUNECA_IZQ_C, 7.2, 6)} {tubo(_pi1, _pi2, 7, 6.8)}" {SOMBRA}/>')

def en_trenza(x, y):
    px, py = rot_punto(x, y, GIRO_TRENZA, 134, 110)
    return (px + DXC, py + DYC)

_cinta_c = en_trenza(124.5, 217)
guardar('rosalba-corriendo.svg', encabezado('Rosalba Insuasty — corriendo, variante monte (huida de la M2).',
        'La mano derecha recoge la falda; canillas con pivote en la rodilla, oculta bajo el ruedo (core/animacion/carrera.ts).') + f'''
{piece('brazo-izq', '{} {}'.format(*map(f, HOMBRO_IZQ_C)), brazo_izq_c, 'Brazo izquierdo (lejano), bracea')}
{piece('antebrazo-izq', '{} {}'.format(*map(f, CODO_IZQ_C)), antebrazo_izq_c, 'Antebrazo y puño izquierdos; hijo de brazo-izq', extra=' data-padre="brazo-izq"')}
{piece('pierna-izq', '{} {}'.format(*RODILLA_IZQ), pierna_carrera(-24, lejana=True), 'Canilla izquierda (lejana); pivote en la rodilla')}
{piece('pierna-der', '{} {}'.format(*RODILLA_DER), pierna_carrera(0), 'Canilla derecha; pivote en la rodilla')}
{piece('enagua', '146 248', enagua_c, 'Enagua que asoma bajo el ruedo recogido')}
{piece('falda', '146 248', falda_c, 'Falda recogida por delante; pliegues desde el puño, cintas del ruedo y barro')}
{piece('torso', '{} {}'.format(*map(f, T(146, 232))), f'<g transform="{TRANS_TORSO}">{torso_monte}</g>', 'Torso inclinado adelante')}
{piece('cabeza', f'{f(150 + DXC)} {f(130 + DYC)}', f'<g transform="{TRANS_CABEZA}">{cabeza_monte}</g>', 'Cabeza derecha (sirven las cabezas por expresión de pie)')}
{piece('zarcillo', f'{f(143.6 + DXC)} {f(100.8 + DYC)}', f'<g transform="{TRANS_CABEZA}">{zarcillo}</g>', 'Zarcillo; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('mechones', f'{f(150 + DXC)} {f(130 + DYC)}', f'<g transform="{TRANS_CABEZA}">{MECHONES}</g>', 'Mechones; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('ruana', '{} {}'.format(*map(f, T(145, 128))), f'<g transform="{TRANS_TORSO}">{ruana_pie}</g>', 'Ruana inclinada con el torso')}
{piece('trenza', f'{f(134 + DXC)} {f(110 + DYC)}', f'<g transform="{TRANS_TRENZA}">{trenza()}</g>', 'Trenza echada atrás por la carrera')}
{piece('cinta', f'{f(_cinta_c[0])} {f(_cinta_c[1])}', f'<g transform="{TRANS_TRENZA}">{cinta()}</g>', 'Cinta roja; hija de trenza (en la M2 va oculta)', extra=' data-padre="trenza"')}
{piece('brazo-der', '{} {}'.format(*map(f, HOMBRO_C)), brazo_c, 'Brazo derecho tendido hacia la falda')}
{piece('antebrazo-der', '{} {}'.format(*map(f, CODO_C)), antebrazo_c, 'Antebrazo y puño que recoge la falda; hijo de brazo-der', extra=' data-padre="brazo-der"')}
{piece('ruana-doblez', '{} {}'.format(*map(f, T(145, 128))), f'<g transform="{TRANS_TORSO}">{doblez_pie}</g>', 'Doblez de la ruana sobre el hombro derecho')}''')

# ======================= 8. Llano (Acto II en adelante) =======================
# Doc 02 M4: Rosalba llega al Llano con desplazados boyacenses (con la ruana del monte) y entra
# a la columna del Gaván. Traje del Llano (hoja de personaje §2):
# - Doc 03 §3.3 [V]: camisa blanca o caqui, cotizas, sombrero de ala ancha (cogollo para faena),
#   faja ancha de cuero con cuchillo.
# - M. A. Hoyos Vega (1943), citado por O. Pabón: en el campo, ropa de dril oscuro; alpargatas de
#   cuero con tejidos de hilo de colores.
# - O. Villanueva Martínez (2012): mujeres en los comandos; dotación de sombrero de paja y quimbas.
# Decisión de diseño (no dato): camisa caqui de hombre, remangada y metida en una falda de dril
# oscuro a media canilla, sin enagua ni cintas (el calor y la guerra); cotizas de suela de cuero
# con capellada tejida; sombrero de cogollo de ala ancha con barbuquejo de cuero. Faja y cuchillo
# son pieza propia (`faja`): se quitan si se desmoviliza (M7). Acto III y Epílogo: el mismo traje
# gastado (remiendos, ruedo deshilachado, ala rota): «apenas cambió de ropa» (doc 02 M7).
# Con la falda a media canilla se ven las canillas: pivote en la rodilla, oculta bajo la falda,
# también al caminar (core/animacion/caminata.ts, modo canilla).
RODILLA_LL_DER, RODILLA_LL_IZQ = (157, 346), (137, 346)  # la lejana, 20 px atrás

def canilla_llano(dx, lejana=False):
    """Canilla desde la rodilla (oculta bajo la falda) hasta el tobillo."""
    def P(x, y): return f"{f(x + dx)},{f(y)}"
    sw = 2.0 if lejana else 2.4
    d = (f'M{P(151,334)} L{P(164,334)} C{P(165.5,350)} {P(164.5,366)} {P(163.5,382)} C{P(162.5,404)} {P(162.5,428)} {P(164,452)} '
         f'L{P(153,453)} C{P(152.5,442)} {P(151.5,432)} {P(149.5,420)} C{P(143,404)} {P(141.4,388)} {P(143.4,372)} C{P(145.4,356)} {P(149,344)} {P(151,334)} Z')
    s = f'<path d="{d}" fill="{PIEL}" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>'
    # pantorrilla en sombra, arista de la tibia y tobillo
    s += f'<path d="M{P(145.4,376)} C{P(144.8,396)} {P(147.4,412)} {P(151.5,428)} L{P(154.5,427)} C{P(151.4,412)} {P(149.4,396)} {P(149.6,376)} Z" {SOMBRA_SUAVE}/>'
    s += f'<path d="M{P(161.6,390)} C{P(160.9,406)} {P(160.9,422)} {P(161.6,438)}" stroke="#000" stroke-width="0.6" fill="none"/>'
    s += f'<path d="M{P(155.6,446)} C{P(157.2,444.4)} {P(159.4,444.4)} {P(160.6,446.4)}" stroke="#000" stroke-width="0.7" fill="none"/>'
    if lejana:
        s += f'<path d="{d}" {SOMBRA}/>'
    return s

def cotiza(dx, lejana=False):
    """Pie descalzo en su cotiza: suela de cuero crudo de dos capas, capellada tejida en hilo con una
    lista de color sobre el empeine y talonera de cuero (doc 03 §3.3; Hoyos Vega 1943)."""
    def P(x, y): return f"{f(x + dx)},{f(y)}"
    sw = 2.0 if lejana else 2.4
    pie = (f'M{P(153,450)} L{P(164,450)} C{P(167,455)} {P(172,458)} {P(178,460)} C{P(183,461.5)} {P(187.5,463)} {P(189.5,466.5)} '
           f'L{P(146,467.5)} C{P(145,462)} {P(147.5,455)} {P(153,450)} Z')
    s = [f'<path d="{pie}" fill="{PIEL}" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>']
    # puntas de los dedos delante de la capellada
    s.append(f'<path d="M{P(183.6,462.2)} C{P(185,463.6)} {P(185.6,465)} {P(185.6,466.6)} M{P(186.8,463.4)} C{P(188,464.6)} {P(188.6,465.6)} {P(188.6,466.6)}" stroke="#000" stroke-width="0.7" fill="none"/>')
    suela = (f'M{P(144,466)} L{P(190,465.4)} C{P(192.4,467)} {P(192.4,471.4)} {P(189.6,473.4)} C{P(175,475.8)} {P(156,475.6)} {P(146,474.6)} '
             f'C{P(142.8,472.8)} {P(142.6,468)} {P(144,466)} Z')
    s.append(f'<path d="{suela}" fill="{CUERO_CRUDO}" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>')
    s.append(f'<path d="M{P(145,470.2)} C{P(160,471)} {P(176,470.8)} {P(191,469.6)}" stroke="#000" stroke-width="0.8" fill="none"/>')
    cap = (f'M{P(158,453)} C{P(163,452.6)} {P(169,456.4)} {P(175,459.4)} C{P(179,461.4)} {P(182,463.4)} {P(183,466.2)} '
           f'L{P(157,466.6)} C{P(156,461.4)} {P(156.4,456.4)} {P(158,453)} Z')
    s.append(f'<path d="{cap}" fill="{TELA}" stroke="#000" stroke-width="{f(sw * 0.85)}" stroke-linejoin="round"/>')
    s.append(f'<path d="M{P(160,457.4)} L{P(163,460.4)} L{P(166,458)} L{P(169,461.4)} L{P(172,459.6)} L{P(175,462.8)} L{P(178,461.8)}" stroke="#000" stroke-width="0.9" fill="none"/>')
    s.append(f'<path d="M{P(157.6,464)} C{P(166,463.8)} {P(174,464.2)} {P(181.6,465.2)}" stroke="{CINTAS[1]}" stroke-width="1.8" fill="none"/>')
    # talonera de cuero
    talon = f'M{P(157.6,457)} C{P(153,456)} {P(149,457.6)} {P(146.6,461.6)}'
    s.append(f'<path d="{talon}" stroke="#000" stroke-width="3.8" fill="none" stroke-linecap="round"/>')
    s.append(f'<path d="{talon}" stroke="{CUERO}" stroke-width="2" fill="none" stroke-linecap="round"/>')
    if lejana:
        s.append(f'<path d="{pie}" {SOMBRA_SUAVE}/><path d="{cap}" {SOMBRA_SUAVE}/>')
    return ''.join(s)

def pierna_llano(dx, lejana=False):
    return canilla_llano(dx, lejana) + cotiza(dx, lejana)

# ---------- falda de dril a media canilla ----------
FALDA_LL = 'M126,230 L166,230 C171,270 181,334 189,394 Q144,401.6 99,394 C106,334 119,268 126,230 Z'

falda_ll = (
    f'<path d="{FALDA_LL}" fill="{DRIL}" stroke="#000" stroke-width="3" stroke-linejoin="round"/>'
    + recortar('falda-ll-marcas', FALDA_LL,
        f'<path d="M126,230 C119,268 106,334 99,394 Q107,396.8 115,397.8 C117,334 124,270 132,232 Z" {SOMBRA_HONDA}/>'
        # pocos pliegues largos del dril, como reflejos de papel
        '<path d="M139,240 C136,290 131,340 127,390 M151,240 C152,290 154,340 156,394 M161,242 C166,290 172,336 178,390" stroke="#fff" stroke-width="1.3" fill="none" stroke-linecap="round" stroke-opacity="0.45"/>'
        # dobladillo cosido a mano
        '<path d="M102,386.6 Q144,393.6 186,386.6" stroke="#fff" stroke-width="0.8" fill="none" stroke-dasharray="4 3" stroke-opacity="0.6"/>'
        + (remiendo([(149, 300), (166, 298), (168, 318), (151, 321)], CAQUI, 'falda') if GASTADO else ''))
    + f'<path d="{FALDA_LL}" fill="none" stroke="#000" stroke-width="3" stroke-linejoin="round"/>'
    + (hilachas([(112, 395.4, 5), (121, 396.6, 4), (136, 397.6, 6), (160, 397.4, 4), (171, 396.6, 5), (182, 395, 4)]) if GASTADO else '')
    # pretina
    + f'<path d="M125,227 L167,227 L167.6,236 L124.4,236 Z" fill="{DRIL}" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/>'
)

# ---------- camisa caqui de hombre, metida en la falda ----------
TORSO_LL = 'M136,130 C150,126 163,128 167,136 C174,150 177,168 175,186 C173,202 171,216 169,232 L125,232 C123,210 122,188 124,164 C125,148 128,138 136,130 Z'
torso_ll = (
    f'<path d="{TORSO_LL}" fill="{CAQUI}" stroke="#000" stroke-width="2.8" stroke-linejoin="round"/>'
    + recortar('torso-ll-marcas', TORSO_LL,
        f'<path d="M124,160 C124,190 125,212 127,232 L135,232 C132,208 131,186 132,158 Z" {SOMBRA_SUAVE}/>'
        # la camisa ancha se abolsa sobre la pretina
        f'<path d="M124,220 C140,216 156,216 172,220 L172,232 L124,232 Z" {SOMBRA_SUAVE}/>'
        '<path d="M135,207 C138,216 140,223 142,230 M150,210 C151,218 151,224 151,230 M163,206 C162,215 161,222 161,230" stroke="#000" stroke-width="0.8" fill="none"/>'
        # tapeta delantera con botones
        '<path d="M168.6,148 C171,168 171.4,190 170,214" stroke="#000" stroke-width="0.9" fill="none"/>'
        + ''.join(f'<circle cx="{f(x)}" cy="{f(y)}" r="1.6" fill="#fff" stroke="#000" stroke-width="0.8"/>' for x, y in [(169.8, 162), (170.6, 180), (170.4, 198)])
        # bolsillo de pecho con tapa
        + '<path d="M151.4,156 L163.6,156.6 L163.4,175 L152,174.4 Z" fill="none" stroke="#000" stroke-width="1"/>'
        + f'<path d="M150.8,155.4 L164,156 L163.4,161.6 L157.6,163.4 L151.4,161 Z" fill="{CAQUI}" stroke="#000" stroke-width="1" stroke-linejoin="round"/>')
    + f'<path d="{TORSO_LL}" fill="none" stroke="#000" stroke-width="2.8" stroke-linejoin="round"/>'
    # banda del cuello por detrás de la nuca
    + f'<path d="M135,130.6 C142,126.4 150,126.4 157,129.4 L158,134 C151,131.6 143,131.8 135.4,133.6 Z" fill="{CAQUI}" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/>'
)
# Cuello abierto de la camisa: la garganta en V y la punta del cuello caen por delante del hombro,
# así que van en una pieza propia dibujada después del brazo derecho.
cuello_ll = (
    f'<path d="M156.6,131 L166.6,134.4 C167,140 166.4,145 165.4,150.6 Z" fill="{PIEL}" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/>'
    f'<path d="M157.6,132.6 L165.8,135.6 L165.4,141 Z" {SOMBRA}/>'
    f'<path d="M151.4,129 C155.6,129.4 159,131 161.4,133.4 L167.6,151.4 C163.4,147 158.6,143 154,140.6 C152.4,137 151.6,133 151.4,129 Z" fill="{CAQUI}" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/>'
    '<path d="M154.6,135 C158,138.6 162,143.6 165,148.4" stroke="#000" stroke-width="0.6" fill="none"/>'
)

# ---------- faja de cuero con cuchillo (pieza propia: se quita al desmovilizarse, M7) ----------
faja_ll = (
    # vaina de cuero crudo con costura, metida bajo la faja en la cadera derecha
    f'<path d="M138,221 L148,221 C147,240 144,262 139,282 C138,286 135,287 134,284 C134,264 136,242 138,221 Z" fill="{CUERO_CRUDO}" stroke="#000" stroke-width="1.8" stroke-linejoin="round"/>'
    '<path d="M140.6,238 C140.2,254 138.8,268 136.6,280" stroke="#000" stroke-width="0.7" fill="none" stroke-dasharray="2.4 2"/>'
    f'<path d="M138,236 L147.2,236 C146.6,246 145.2,256 143.6,264 L137.2,262 C137,252 137.4,244 138,236 Z" {SOMBRA_SUAVE}/>'
    # faja ancha de cuero con pespunte, hebilla de hierro y la punta colgando
    f'<path d="M123.6,221 C138,218.6 156,218.6 170.4,221 L171,235 C156,232.8 138,232.8 123,235 Z" fill="{CUERO}" stroke="#000" stroke-width="2" stroke-linejoin="round"/>'
    '<path d="M125.4,224 C140,222 156,222 169.4,224 M124.8,232 C140,230 156,230 169.8,232" stroke="#fff" stroke-width="0.7" fill="none" stroke-dasharray="2.4 2.2" stroke-opacity="0.7"/>'
    f'<path d="M167.4,234.4 C168,242 167.6,250 166.4,256.4 L171.4,257.2 C172.4,250 172.8,242 172.2,234.4 Z" fill="{CUERO}" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/>'
    '<path d="M166.4,219 L174,219.4 L174.2,236.6 L166.6,236.2 Z" fill="none" stroke="#000" stroke-width="2.2" stroke-linejoin="round"/>'
    '<path d="M168,221 L168.2,234.6" stroke="#fff" stroke-width="0.7"/>'
    # cacha de madera con dos remaches y guarnición
    '<g transform="rotate(-14 143.4 221)">'
    f'<path d="M139.2,221 L147.6,221 C148.6,213 149,205 148,197.6 C147.6,194.4 143,194 141.8,196.6 C140.2,205 139.4,213 139.2,221 Z" fill="{CUERO}" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/>'
    '<circle cx="143.8" cy="214" r="1.1" fill="#fff"/><circle cx="144.2" cy="204.6" r="1.1" fill="#fff"/>'
    '<path d="M137,221.4 L150,221.4" stroke="#000" stroke-width="2.8" stroke-linecap="round"/></g>'
)

# ---------- brazo remangado: manga caqui, rollo sobre el codo y antebrazo descubierto ----------
def brazo_llano(dx, lejano=False):
    """(brazo, antebrazo con mano, rollo de la manga). El rollo va aparte, encima del antebrazo,
    para tapar la articulación del codo cuando el antebrazo se dobla."""
    def P(x, y): return f"{f(x + dx)},{f(y)}"
    sw = 2.2 if lejano else 2.7
    up_d = f'M{P(138,138)} C{P(146,128)} {P(166,130)} {P(168,146)} C{P(169,160)} {P(167.5,178)} {P(167,194)} L{P(147.6,195)} C{P(144.6,178)} {P(141,160)} {P(138,138)} Z'
    up = (f'<path d="{up_d}" fill="{CAQUI}" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>'
          # costura del hombro caído (camisa de hombre) y un pliegue
          f'<path d="M{P(140.6,147)} C{P(147,142)} {P(157,140.6)} {P(166.6,143)}" stroke="#000" stroke-width="0.9" fill="none"/>'
          f'<path d="M{P(158,158)} C{P(159.5,168)} {P(160,178)} {P(159.6,188)}" stroke="#000" stroke-width="0.7" fill="none"/>'
          f'<path d="M{P(142,160)} C{P(144,176)} {P(146,188)} {P(148,195)} L{P(152,195)} C{P(150,186)} {P(148,174)} {P(147,158)} Z" {SOMBRA_SUAVE}/>')
    if GASTADO and not lejano:
        up += remiendo([(151.4, 154), (161.6, 153.2), (162.6, 165.6), (152.4, 166.6)], LANA, 'manga')
    fore_d = f'M{P(148.6,196)} L{P(165.6,195)} C{P(168,214)} {P(170.6,236)} {P(172,258.6)} L{P(157.8,260.4)} C{P(155.6,238)} {P(151.6,216)} {P(148.6,196)} Z'
    fore = (f'<path d="{fore_d}" fill="{PIEL}" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<path d="M{P(150.6,206)} C{P(152.6,222)} {P(155,238)} {P(158,254)} L{P(161,253)} C{P(158.4,238)} {P(156,222)} {P(154,206)} Z" {SOMBRA_SUAVE}/>'
            f'<path d="M{P(163.6,204)} C{P(165.6,214)} {P(166.6,224)} {P(166.8,234)}" stroke="#000" stroke-width="0.7" fill="none"/>'
            + mano(dx, sw))
    rollo_d = f'M{P(145.6,190)} C{P(152,187.4)} {P(162,187)} {P(168.6,189.6)} L{P(169.6,203)} C{P(162,205.6)} {P(152,206)} {P(146.6,204)} Z'
    rollo = (f'<path d="{rollo_d}" fill="{CAQUI}" stroke="#000" stroke-width="{f(sw * 0.9)}" stroke-linejoin="round"/>'
             f'<path d="M{P(146.6,197.6)} C{P(153,196)} {P(162,196)} {P(169.4,198)} L{P(169.6,203)} C{P(162,205.6)} {P(152,206)} {P(146.6,204)} Z" {SOMBRA_SUAVE}/>'
             f'<path d="M{P(146.2,197)} C{P(153,194.6)} {P(162,194.4)} {P(169,196.4)}" stroke="#000" stroke-width="1" fill="none"/>')
    if lejano:
        up += f'<path d="{up_d}" {SOMBRA}/>'
        fore += (f'<path d="{fore_d}" {SOMBRA}/>'
                 f'<path d="M{P(158,260)} C{P(156,266)} {P(156,272)} {P(157,277)} C{P(157,283)} {P(158,288)} {P(161,292)} C{P(163,295)} {P(167,295.5)} {P(169,293.5)} C{P(171,291)} {P(171.5,287)} {P(171,284)} C{P(173,282)} {P(175.5,280)} {P(177.5,277.5)} C{P(179.5,275)} {P(179,271.5)} {P(177,270)} C{P(175,268.5)} {P(173,267.5)} {P(172,264)} L{P(172,258)} Z" {SOMBRA_SUAVE}/>')
        rollo += f'<path d="{rollo_d}" {SOMBRA}/>'
    return up, fore, rollo

# ---------- sombrero de cogollo de ala ancha, con barbuquejo de cuero ----------
sombrero_ll = SOMBRA_ALA + f'''
    <!-- sombra del ala ancha, más larga que la del sombrero de caña -->
    <path d="M152,66 C160,66 168,67 174,70 C172,73 166,74 160,73 C156,72 153,70 152,66 Z" fill="#000" fill-opacity="0.1"/>
    <!-- copa de cogollo con la hendidura arriba -->
    <path d="M129,58 C128,47 130,38 136,34.6 C141,32.4 146,34.6 150,34.8 C154.6,34.8 159,32 164.6,34 C170,36.6 172,46 171.4,58 Z" fill="{PAJA}" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M130.6,46 C144,43.6 158,43.6 171,46 M132,39.6 C140,37.4 146,38.4 150,38.6 C155,38.6 160,36.6 168,38.4" stroke="#000" stroke-width="0.9" fill="none"/>
    <path d="M129,58 C128.6,49 130,42 134,37 C132,45 132,51 133,58 Z" fill="#000" fill-opacity="0.18"/>
    <path d="M146,35.4 C148,36.6 152,36.6 154,35.4" stroke="#000" stroke-width="0.8" fill="none"/>
    <!-- cinta de cuero delgada con su nudo atrás -->
    <path d="M129.2,52.4 C142,50.4 158,50.4 171.4,52.4 L171.6,57.6 C158,55.8 142,55.8 129,57.6 Z" fill="{CUERO}" stroke="#000" stroke-width="1"/>
    <path d="M129.6,53.6 C127,54.4 126.4,56.4 127.4,58 M130,55.6 C128.6,57.6 128.6,60 129.6,61.6" stroke="#000" stroke-width="1.6" fill="none" stroke-linecap="round"/>
    <!-- ala ancha, casi plana -->
    <path d="M92,61.6 C112,54.4 188,52.6 210,58.6 C206,64 188,66.6 152,66 C124,66 104,67.6 92,61.6 Z" fill="{PAJA}" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>
    <path d="M97,61.4 C124,57.6 176,56 205,58.8" stroke="#000" stroke-width="0.8" fill="none"/>
    <path d="M100,64 C126,66.4 178,65.4 205,60.8 C194,65.8 172,67.6 152,67.2 C128,67 110,67.6 100,64 Z" fill="#000"/>
    <!-- barbuquejo: cordón de cuero por la mejilla, atado bajo el mentón -->
    <path d="M148.5,64 C149,74 149.6,84 150.2,94 C151,104 155,113 161,118 C163.5,120 165.5,121 167,121.5" stroke="#000" stroke-width="2.4" fill="none" stroke-linecap="round"/>
    <path d="M148.5,64 C149,74 149.6,84 150.2,94 C151,104 155,113 161,118 C163.5,120 165.5,121 167,121.5" stroke="{CUERO}" stroke-width="1.1" fill="none" stroke-linecap="round"/>
    <path d="M166,121 C163,124 161,128 162,131 M167,122 C168,126 168,129 170,131" stroke="#000" stroke-width="1.8" fill="none" stroke-linecap="round"/>
    <circle cx="166.8" cy="121.6" r="1.8" fill="#000"/>''' + (
    # Acto III y Epílogo: el ala rota atrás, con un pedazo colgando y la paja deshilachada
    f'''
    <path d="M100,63.6 L111,65.4 L107,73.6 C104,72 101.6,68 100,63.6 Z" fill="{PAJA}" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/>
    <path d="M103.6,66 L106.4,71" stroke="#000" stroke-width="0.7"/>
    <path d="M111,65.4 L114,68.6 M110.4,66.4 L112.4,70.6 M100,63.6 L97.4,66.4" stroke="#000" stroke-width="0.8" stroke-linecap="round"/>''' if GASTADO else '')

# ======================= 8a. de pie, Llano =======================
bil_up, bil_fore, bil_rollo = brazo_llano(-12, lejano=True)
bdl_up, bdl_fore, bdl_rollo = brazo_llano(0)
guardar('rosalba-llano.svg', encabezado('Rosalba Insuasty — de pie, variante Llano (Acto II en adelante).',
        'Camisa caqui de hombre remangada, falda de dril a media canilla, cotizas, faja con cuchillo, sombrero de cogollo (doc 03 §3.3 [V]; combinación: decisión de diseño).'
        + (' Traje gastado: remiendos, ruedo deshilachado, ala rota.' if GASTADO else '')) + f'''
{piece('brazo-izq', '141 144', bil_up, 'Brazo izquierdo (lejano): manga caqui')}
{piece('antebrazo-izq', '145 202', bil_fore, 'Antebrazo descubierto y mano izquierdos; hijo de brazo-izq', extra=' data-padre="brazo-izq"')}
{piece('manga-izq', '145 198', bil_rollo, 'Rollo de la manga remangada sobre el codo; hijo de brazo-izq', extra=' data-padre="brazo-izq"')}
{piece('pierna-izq', '{} {}'.format(*RODILLA_LL_IZQ), pierna_llano(-20, lejana=True), 'Canilla izquierda (lejana) con su cotiza; pivote en la rodilla, oculta bajo la falda')}
{piece('pierna-der', '{} {}'.format(*RODILLA_LL_DER), pierna_llano(0), 'Canilla derecha con su cotiza; pivote en la rodilla')}
{piece('falda', '146 232', falda_ll, 'Falda de dril oscuro a media canilla')}
{piece('torso', '146 232', torso_ll, 'Torso: camisa caqui de hombre metida en la falda, cuello abierto')}
{piece('faja', '146 228', faja_ll, 'Faja ancha de cuero con cuchillo en la cadera derecha (se quita al desmovilizarse)')}
{piece('cabeza', '150 130', cabeza, 'Cabeza con cuello (las expresiones en rosalba-cabezas.svg)')}
{piece('zarcillo', '143.6 100.8', zarcillo, 'Zarcillo; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('sombrero', '150 60', sombrero_ll, 'Sombrero de cogollo de ala ancha con barbuquejo de cuero; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('trenza', '134 110', trenza(), 'Trenza atada con hilo oscuro')}
{piece('cinta', '124.5 217', cinta(), 'Cinta roja; hija de trenza (vuelve a atársela en el Acto II)', extra=' data-padre="trenza"')}
{piece('brazo-der', '153 140', bdl_up, 'Brazo derecho: manga caqui')}
{piece('antebrazo-der', '157 200', bdl_fore, 'Antebrazo descubierto y mano derechos; hijo de brazo-der', extra=' data-padre="brazo-der"')}
{piece('manga-der', '157 198', bdl_rollo, 'Rollo de la manga remangada sobre el codo; hijo de brazo-der', extra=' data-padre="brazo-der"')}
{piece('cuello', '152 132', cuello_ll, 'Cuello abierto de la camisa: garganta en V y punta del cuello, por delante del hombro')}''')

# ======================= 8b. agachada, Llano =======================
# Misma cabeza, en el mismo sitio, que la agachada del monte (sirven rosalba-agachada-cabezas). Sin
# ruana: la camisa curva la espalda; la falda a media canilla hace un domo sobre las rodillas y deja
# ver las cotizas; la faja ciñe la cintura, más baja adelante, con el cuchillo sobre la cadera.
CAMISA_AG = ('M172,302 C184,298 198,302 206,314 C212,324 212,336 208,348 L170,420 '
             'C156,414 140,406 125,400 C121,378 123,356 131,338 C141,320 156,306 172,302 Z')
FALDA_LLAG = ('M125,398 C138,404 150,410 161,414 C176,394 192,366 206,346 C214,338 222,342 224,352 '
              'C227,366 226,392 227,414 C227,424 228,432 229,440 Q204,444 180,447 C152,452 124,461 102,470 '
              'C96,450 98,426 108,410 C112,404 118,400 125,398 Z')

def _canilla_ag(dx, lejana):
    """Canilla inclinada hacia la rodilla (casi toda bajo el domo) y la cotiza plana en el suelo."""
    tobillo = (158.5 + dx, 452)
    return (f'<g transform="rotate(22 {f(tobillo[0])} {f(tobillo[1])})">{canilla_llano(dx, lejana)}</g>'
            + cotiza(dx, lejana))

cuerpo_llag = (
    _canilla_ag(2, True) + _canilla_ag(14, False)
    # camisa sobre la espalda curvada, con la sombra de la espalda y el cuello camisero
    + f'<path d="{CAMISA_AG}" fill="{CAQUI}" stroke="#000" stroke-width="2.8" stroke-linejoin="round"/>'
    + recortar('camisa-ag-marcas', CAMISA_AG,
        f'<path d="M131,338 C123,356 121,378 125,400 L136,404 C132,382 134,360 142,342 Z" {SOMBRA_SUAVE}/>'
        # la tela tira sobre la espalda curvada: pliegues del hombro a la cintura
        '<path d="M156,312 C148,330 142,352 141,376 M170,308 C164,328 160,350 158,372" stroke="#000" stroke-width="0.8" fill="none"/>')
    + f'<path d="{CAMISA_AG}" fill="none" stroke="#000" stroke-width="2.8" stroke-linejoin="round"/>'
    + f'<path d="M170,300.6 C180,296 192,297 200,302 L201,307 C193,303 181,302.6 171,305 Z" fill="{CAQUI}" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/>'
    # falda en domo sobre las rodillas; el ruedo sube adelante y deja ver las cotizas
    + f'<path d="{FALDA_LLAG}" fill="{DRIL}" stroke="#000" stroke-width="3" stroke-linejoin="round"/>'
    + recortar('falda-llag-marcas', FALDA_LLAG,
        f'<path d="M108,410 C98,426 96,450 102,470 L118,464 C112,444 114,424 122,408 Z" {SOMBRA_HONDA}/>'
        '<path d="M214,362 C216,390 218,416 220,438 M196,372 C196,400 194,424 192,444 M176,396 C172,418 166,438 160,452 M146,414 C138,432 130,448 122,462" stroke="#fff" stroke-width="1.3" fill="none" stroke-linecap="round" stroke-opacity="0.45"/>'
        '<path d="M200,350 C206,344 214,342 220,346" stroke="#fff" stroke-width="1.1" fill="none" stroke-linecap="round" stroke-opacity="0.6"/>'
        '<path d="M226,432 Q204,436.6 180,439.6 C152,444.6 124,453.6 104,462" stroke="#fff" stroke-width="0.8" fill="none" stroke-dasharray="4 3" stroke-opacity="0.6"/>'
        + (remiendo([(186, 396), (201, 392), (204, 410), (189, 413)], CAQUI, 'falda-ag') if GASTADO else ''))
    + f'<path d="{FALDA_LLAG}" fill="none" stroke="#000" stroke-width="3" stroke-linejoin="round"/>'
    + (hilachas([(222, 440.6, 4), (206, 443, 5), (188, 445.6, 4), (160, 450.6, 5), (134, 458, 4), (114, 465, 5)]) if GASTADO else '')
)

# faja: la de pie, girada con la cintura (más baja adelante) y llevada a la cadera
faja_llag = f'<g transform="translate(-3 177) rotate(25 146 228)">{faja_ll}</g>'

HOMBRO_L, CODO_L, MUNECA_L = HOMBRO, CODO, MUNECA
brazo_llag = (
    f'<path d="{tubo(HOMBRO_L, punto_en(HOMBRO_L, CODO_L, 0.86), 10, 8.6)}" fill="{CAQUI}" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>'
    + f'<path d="M{f(punto_en(HOMBRO_L, CODO_L, 0.08, -6)[0])},{f(punto_en(HOMBRO_L, CODO_L, 0.08, -6)[1])} C{f(punto_en(HOMBRO_L, CODO_L, 0.04, 0)[0])},{f(punto_en(HOMBRO_L, CODO_L, 0.04, 0)[1])} {f(punto_en(HOMBRO_L, CODO_L, 0.06, 4)[0])},{f(punto_en(HOMBRO_L, CODO_L, 0.06, 4)[1])} {f(punto_en(HOMBRO_L, CODO_L, 0.14, 8)[0])},{f(punto_en(HOMBRO_L, CODO_L, 0.14, 8)[1])}" stroke="#000" stroke-width="0.9" fill="none"/>'
    + f'<path d="{tubo(punto_en(HOMBRO_L, CODO_L, 0.2, -5), punto_en(HOMBRO_L, CODO_L, 0.82, -4.4), 2.4, 2)}" {SOMBRA_SUAVE}/>'
    + (remiendo([punto_en(HOMBRO_L, CODO_L, t, o) for t, o in [(0.3, -5), (0.3, 5), (0.55, 5), (0.55, -5)]], LANA, 'manga-ag') if GASTADO else '')
)
_r1, _r2 = punto_en(HOMBRO_L, CODO_L, 0.84), punto_en(HOMBRO_L, CODO_L, 1.06)
manga_llag = (f'<path d="{tubo(_r1, _r2, 10.4, 9.6)}" fill="{CAQUI}" stroke="#000" stroke-width="2.4" stroke-linejoin="round"/>'
              + f'<path d="M{f(punto_en(_r1, _r2, 0.5, -10)[0])},{f(punto_en(_r1, _r2, 0.5, -10)[1])} L{f(punto_en(_r1, _r2, 0.5, 10)[0])},{f(punto_en(_r1, _r2, 0.5, 10)[1])}" stroke="#000" stroke-width="1"/>'
              + f'<path d="{tubo(punto_en(_r1, _r2, 0.5), _r2, 9.6, 9.2)}" {SOMBRA_SUAVE}/>')
antebrazo_llag = (
    f'<path d="{tubo(CODO_L, punto_en(CODO_L, MUNECA_L, 0.98), 7.4, 5.8)}" fill="{PIEL}" stroke="#000" stroke-width="2.6" stroke-linejoin="round"/>'
    + f'<path d="{tubo(punto_en(CODO_L, MUNECA_L, 0.12, -3.6), punto_en(CODO_L, MUNECA_L, 0.84, -2.8), 1.8, 1.4)}" {SOMBRA_SUAVE}/>'
    # mano apoyada en el suelo (la misma de la agachada del monte)
    + antebrazo_ag[antebrazo_ag.index('<path d="M216,452'):]
)

_SOMB_AG = f'translate({CAB_T[0]} {CAB_T[1]}) rotate({CAB_R} 150 130)'
somb = cab_punto(150, 60)
guardar('rosalba-llano-agachada.svg', encabezado('Rosalba Insuasty — agachada (sigilo), variante Llano. Pose dibujada aparte.',
        'En cuclillas: camisa sobre la espalda curvada, falda en domo sobre las rodillas, cotizas a la vista, mano apoyada en el suelo.'
        + (' Traje gastado.' if GASTADO else '')) + f'''
{piece('cuerpo', '150 440', cuerpo_llag, 'Cuerpo en cuclillas: cotizas, camisa y falda en domo')}
{piece('faja', '143 405', faja_llag, 'Faja con cuchillo, ceñida a la cintura (se quita al desmovilizarse)')}
{piece('cabeza', f'{f(cuello[0])} {f(cuello[1])}', cabeza_ag, 'Cabeza (la de pie, inclinada hacia adelante)')}
{piece('zarcillo', f'{f(z[0])} {f(z[1])}', zarcillo_ag, 'Zarcillo; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('sombrero', f'{f(somb[0])} {f(somb[1])}', f'<g transform="{_SOMB_AG}">{sombrero_ll}</g>', 'Sombrero de cogollo; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('trenza', f'{f(nuca[0])} {f(nuca[1])}', trenza(nuca[0], nuca[1] + 1, nuca[0] - 4, nuca[1] + 96, 12), 'Trenza colgando por gravedad')}
{piece('cinta', f'{f(nuca[0] - 3.5)} {f(nuca[1] + 99)}', cinta(nuca[0] - 4, nuca[1] + 96), 'Cinta roja; hija de trenza', extra=' data-padre="trenza"')}
{piece('brazo-der', f'{HOMBRO_L[0]} {HOMBRO_L[1]}', brazo_llag, 'Brazo derecho hacia el suelo: manga caqui')}
{piece('antebrazo-der', f'{CODO_L[0]} {CODO_L[1]}', antebrazo_llag, 'Antebrazo descubierto y mano apoyada; hijo de brazo-der', extra=' data-padre="brazo-der"')}
{piece('manga-der', f'{f(_r1[0])} {f(_r1[1])}', manga_llag, 'Rollo de la manga sobre el codo; hijo de brazo-der', extra=' data-padre="brazo-der"')}''')

# ======================= 8c. corriendo, Llano =======================
# Misma construcción que la huida de la M2 (torso inclinado, cabeza derecha, canillas con pivote en
# la rodilla), pero la falda a media canilla no hay que recogerla: los dos brazos bracean (carrera
# con `bracea: 'ambos'`) y la tela liviana vuela hacia atrás, con el ruedo a la altura de la rodilla.
RUEDO_LC = cadena(suave([(196, 374), (180, 383), (162, 392), (142, 402), (122, 411), (102, 416), (86, 413)]), 12)
FALDA_LC = ('M124,236 L170,244 C176,262 183,290 189,318 C193,338 196,356 196,374 '
            + ' '.join(f'L{f(x)},{f(y)}' for x, y in RUEDO_LC[1:]) +
            ' C84,384 92,340 104,300 C110,276 117,254 124,236 Z')

def ruedo_lc(sube):
    return [(x, y - sube) for x, y in RUEDO_LC]

falda_lc = (
    f'<path d="{FALDA_LC}" fill="{DRIL}" stroke="#000" stroke-width="3" stroke-linejoin="round"/>'
    + recortar('falda-lc-marcas', FALDA_LC,
        f'<path d="M124,236 C114,262 104,300 96,340 C90,370 86,396 86,413 L104,416 C104,380 110,320 128,250 Z" {SOMBRA_HONDA}/>'
        # el viento pega la tela al muslo adelante y la abre atrás: pliegues desde la cintura
        + ''.join(pincel(suave([(a, 246), mezcla((a, 246), h, 0.5), h]), w, 0.2, 0.1, '#fff', extra=' fill-opacity="0.45"')
                  for a, h, w in [(164, (186, 368), 1.4), (152, (160, 388), 1.4), (140, (132, 404), 1.3), (130, (104, 412), 1.2)])
        + f'<path d="{polilinea(ruedo_lc(7))}" stroke="#fff" stroke-width="0.8" fill="none" stroke-dasharray="4 3" stroke-opacity="0.6"/>'
        + (remiendo([(150, 300), (166, 300), (168, 318), (151, 320)], CAQUI, 'falda-lc') if GASTADO else ''))
    + f'<path d="{FALDA_LC}" fill="none" stroke="#000" stroke-width="3" stroke-linejoin="round"/>'
    + (hilachas([(190, 377, 4), (172, 388, 5), (150, 398.6, 4), (128, 409, 5), (106, 415.6, 4)]) if GASTADO else '')
    + f'<path d="M124,236 L170,244 L169.4,252 L123,244 Z" fill="{DRIL}" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/>'
)

def brazo_lc(hombro, lejano):
    """(brazo, antebrazo con puño, rollo) de un brazo que cuelga en reposo; la carrera lo dobla."""
    codo = (hombro[0] + 2, hombro[1] + 57)
    muneca = (codo[0] + 2, codo[1] + 50)
    u = (2 / math.hypot(2, 50), 50 / math.hypot(2, 50))
    sw = 2.2 if lejano else 2.6
    sombra = SOMBRA if lejano else SOMBRA_SUAVE
    sup = tubo(hombro, punto_en(hombro, codo, 0.86), 10.4, 8.6)
    up = (f'<path d="{sup}" fill="{CAQUI}" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>'
          + f'<path d="{tubo(punto_en(hombro, codo, 0.2, -5), punto_en(hombro, codo, 0.8, -4.4), 2.4, 2)}" {SOMBRA_SUAVE}/>'
          + (f'<path d="{sup}" {SOMBRA}/>' if lejano else '')
          + (remiendo([punto_en(hombro, codo, t, o) for t, o in [(0.22, -5), (0.22, 5), (0.5, 5), (0.5, -5)]], LANA, 'manga-lc') if GASTADO and not lejano else ''))
    r1, r2 = punto_en(hombro, codo, 0.84), punto_en(hombro, codo, 1.06)
    rollo_d = tubo(r1, r2, 10.6, 9.8)
    rollo = (f'<path d="{rollo_d}" fill="{CAQUI}" stroke="#000" stroke-width="{f(sw * 0.92)}" stroke-linejoin="round"/>'
             + f'<path d="M{f(punto_en(r1, r2, 0.5, -10)[0])},{f(punto_en(r1, r2, 0.5, -10)[1])} L{f(punto_en(r1, r2, 0.5, 10)[0])},{f(punto_en(r1, r2, 0.5, 10)[1])}" stroke="#000" stroke-width="1"/>'
             + f'<path d="{rollo_d}" {sombra}/>')
    ante = tubo(codo, punto_en(codo, muneca, 0.98), 7.6, 6.2)
    fore = (f'<path d="{ante}" fill="{PIEL}" stroke="#000" stroke-width="{sw}" stroke-linejoin="round"/>'
            + f'<path d="{tubo(punto_en(codo, muneca, 0.12, -3.6), punto_en(codo, muneca, 0.8, -2.8), 1.8, 1.4)}" {SOMBRA_SUAVE}/>'
            + puno_c(muneca, u, tela=False, escala=0.92 if lejano else 1.0)
            + (f'<path d="{ante}" {SOMBRA}/>' if lejano else ''))
    return up, fore, rollo, codo, r1

HOMBRO_DER_LC = T(153, 140)
bil_c, ail_c, mil_c, codo_il_c, rollo_il_c = brazo_lc(HOMBRO_IZQ_C, True)
bdl_c, adl_c, mdl_c, codo_dl_c, rollo_dl_c = brazo_lc(HOMBRO_DER_LC, False)
_somb_c = (150 + DXC, 60 + DYC)
guardar('rosalba-llano-corriendo.svg', encabezado('Rosalba Insuasty — corriendo, variante Llano.',
        'Falda a media canilla al viento, los dos brazos bracean; canillas con pivote en la rodilla, oculta bajo el ruedo (core/animacion/carrera.ts, bracea: ambos).'
        + (' Traje gastado.' if GASTADO else '')) + f'''
{piece('brazo-izq', '{} {}'.format(*map(f, HOMBRO_IZQ_C)), bil_c, 'Brazo izquierdo (lejano), bracea')}
{piece('antebrazo-izq', '{} {}'.format(*map(f, codo_il_c)), ail_c, 'Antebrazo descubierto y puño izquierdos; hijo de brazo-izq', extra=' data-padre="brazo-izq"')}
{piece('manga-izq', '{} {}'.format(*map(f, rollo_il_c)), mil_c, 'Rollo de la manga; hijo de brazo-izq', extra=' data-padre="brazo-izq"')}
{piece('pierna-izq', '{} {}'.format(*RODILLA_LL_IZQ), pierna_llano(-20, lejana=True), 'Canilla izquierda (lejana) con su cotiza; pivote en la rodilla')}
{piece('pierna-der', '{} {}'.format(*RODILLA_LL_DER), pierna_llano(0), 'Canilla derecha con su cotiza; pivote en la rodilla')}
{piece('falda', '146 248', falda_lc, 'Falda de dril al viento, ruedo a la altura de la rodilla')}
{piece('torso', '{} {}'.format(*map(f, T(146, 232))), f'<g transform="{TRANS_TORSO}">{torso_ll}</g>', 'Torso inclinado adelante: camisa caqui')}
{piece('faja', '{} {}'.format(*map(f, T(146, 228))), f'<g transform="{TRANS_TORSO}">{faja_ll}</g>', 'Faja con cuchillo, inclinada con el torso')}
{piece('cabeza', f'{f(150 + DXC)} {f(130 + DYC)}', f'<g transform="{TRANS_CABEZA}">{cabeza_monte}</g>', 'Cabeza derecha (sirven las cabezas por expresión de pie)')}
{piece('zarcillo', f'{f(143.6 + DXC)} {f(100.8 + DYC)}', f'<g transform="{TRANS_CABEZA}">{zarcillo}</g>', 'Zarcillo; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('sombrero', f'{f(_somb_c[0])} {f(_somb_c[1])}', f'<g transform="{TRANS_CABEZA}">{sombrero_ll}</g>', 'Sombrero de cogollo; hijo de cabeza', extra=' data-padre="cabeza"')}
{piece('trenza', f'{f(134 + DXC)} {f(110 + DYC)}', f'<g transform="{TRANS_TRENZA}">{trenza()}</g>', 'Trenza echada atrás por la carrera')}
{piece('cinta', f'{f(_cinta_c[0])} {f(_cinta_c[1])}', f'<g transform="{TRANS_TRENZA}">{cinta()}</g>', 'Cinta roja; hija de trenza', extra=' data-padre="trenza"')}
{piece('brazo-der', '{} {}'.format(*map(f, HOMBRO_DER_LC)), bdl_c, 'Brazo derecho, bracea')}
{piece('antebrazo-der', '{} {}'.format(*map(f, codo_dl_c)), adl_c, 'Antebrazo descubierto y puño derechos; hijo de brazo-der', extra=' data-padre="brazo-der"')}
{piece('manga-der', '{} {}'.format(*map(f, rollo_dl_c)), mdl_c, 'Rollo de la manga; hijo de brazo-der', extra=' data-padre="brazo-der"')}
{piece('cuello', '{} {}'.format(*map(f, T(152, 132))), f'<g transform="{TRANS_TORSO}">{cuello_ll}</g>', 'Cuello abierto de la camisa, por delante del hombro')}''')
