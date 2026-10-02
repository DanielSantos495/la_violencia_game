"""Utilidades de color sin dependencias (Python 3 estándar).

OKLab/OKLCH (Björn Ottosson, 2020), contraste WCAG 2.x, simulación de daltonismo
(Machado, Oliveira y Fernandes, 2009, severidad 1.0, aplicada en RGB lineal) y
distancia perceptual en OKLab. Las funciones trabajan con tuplas de floats.
"""

import math

# --- sRGB <-> lineal -------------------------------------------------------

def hex_a_rgb(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_a_hex(rgb):
    return '#' + ''.join(f'{round(max(0.0, min(1.0, c)) * 255):02x}' for c in rgb)


def a_lineal(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def a_srgb(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


# --- OKLab / OKLCH -----------------------------------------------------------

def _cbrt(x):
    return math.copysign(abs(x) ** (1 / 3), x)


def lineal_a_oklab(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = _cbrt(l), _cbrt(m), _cbrt(s)
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def oklab_a_lineal(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def oklab_a_oklch(L, a, b):
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def oklch_a_oklab(L, C, h):
    return L, C * math.cos(math.radians(h)), C * math.sin(math.radians(h))


def hex_a_oklch(h):
    return oklab_a_oklch(*lineal_a_oklab(*(a_lineal(c) for c in hex_a_rgb(h))))


def _en_gamut(lin, eps=1e-6):
    return all(-eps <= c <= 1 + eps for c in lin)


def oklch_a_hex(L, C, h):
    """Convierte a hex reduciendo croma (no luz ni tono) si el color cae fuera de sRGB.

    Devuelve (hex, croma_usada). Si croma_usada < C, el color pedido no existe en sRGB.
    """
    lo, hi = 0.0, C
    if _en_gamut(oklab_a_lineal(*oklch_a_oklab(L, C, h))):
        lo = C
    else:
        for _ in range(40):
            mid = (lo + hi) / 2
            if _en_gamut(oklab_a_lineal(*oklch_a_oklab(L, mid, h))):
                lo = mid
            else:
                hi = mid
    lin = oklab_a_lineal(*oklch_a_oklab(L, lo, h))
    return rgb_a_hex(tuple(a_srgb(max(0.0, min(1.0, c))) for c in lin)), lo


# --- Contraste y distancia -------------------------------------------------

def luminancia(h):
    r, g, b = (a_lineal(c) for c in hex_a_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(h1, h2):
    """Razón de contraste WCAG 2.x (1 a 21)."""
    l1, l2 = sorted((luminancia(h1), luminancia(h2)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def delta_ok(h1, h2):
    """Distancia euclídea en OKLab (≈ 0,02 apenas perceptible; > 0,1 claramente distinto)."""
    a = lineal_a_oklab(*(a_lineal(c) for c in hex_a_rgb(h1)))
    b = lineal_a_oklab(*(a_lineal(c) for c in hex_a_rgb(h2)))
    return math.dist(a, b)


# --- Daltonismo (Machado et al. 2009, severidad 1.0) ------------------------

MATRICES_CVD = {
    'protan': ((0.152286, 1.052583, -0.204868),
               (0.114503, 0.786281, 0.099216),
               (-0.003882, -0.048116, 1.051998)),
    'deutan': ((0.367322, 0.860646, -0.227968),
               (0.280085, 0.672501, 0.047413),
               (-0.011820, 0.042940, 0.968881)),
    'tritan': ((1.255528, -0.076749, -0.178779),
               (-0.078411, 0.930809, 0.147602),
               (0.004733, 0.691367, 0.303900)),
}


def simular(h, tipo):
    """Simula cómo ve el color una persona con protanopía, deuteranopía o tritanopía."""
    if tipo == 'grises':
        L = hex_a_oklch(h)[0]
        return oklch_a_hex(L, 0, 0)[0]
    lin = [a_lineal(c) for c in hex_a_rgb(h)]
    m = MATRICES_CVD[tipo]
    out = [sum(m[i][j] * lin[j] for j in range(3)) for i in range(3)]
    return rgb_a_hex(tuple(a_srgb(max(0.0, min(1.0, c))) for c in out))


def tono_en(h, rango):
    """True si el tono h (grados) cae en [ini, fin]; admite rangos que cruzan 0°."""
    ini, fin = rango
    return ini <= h <= fin if ini <= fin else (h >= ini or h <= fin)
