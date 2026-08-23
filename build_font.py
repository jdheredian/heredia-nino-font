import math
from svgpathtools import parse_path
from shapely.geometry import Polygon, LineString, box
from shapely.ops import unary_union
from shapely import make_valid
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from glyphs import GLYPHS, KERN

UPEM = 1000
SCALE = 3.5          # 200 unidades de altura de mayuscula -> 700
BASELINE_Y = 220.0   # en coordenadas SVG
STEP = 1.6           # resolucion de muestreo de curvas


def sample(seg):
    """Convierte un segmento en una lista de puntos."""
    try:
        L = seg.length(error=1e-3)
    except Exception:
        L = abs(seg.end - seg.start)
    n = max(2, int(L / STEP) + 1)
    return [seg.point(i / n) for i in range(n + 1)]


def subpath_points(sub):
    pts = []
    for seg in sub:
        for p in sample(seg):
            xy = (p.real, p.imag)
            if not pts or abs(pts[-1][0] - xy[0]) > 1e-9 or abs(pts[-1][1] - xy[1]) > 1e-9:
                pts.append(xy)
    return pts


def poly_from_d_even_odd(d):
    """Path relleno con regla par-impar: subpaths contenidos son huecos."""
    path = parse_path(d)
    subs = path.continuous_subpaths()
    polys = []
    for sub in subs:
        pts = subpath_points(sub)
        if len(pts) < 3:
            continue
        p = Polygon(pts)
        if not p.is_valid:
            p = make_valid(p).buffer(0)
        if not p.is_empty:
            polys.append(p)
    if not polys:
        return None
    # ordenar por area descendente; alternar relleno/hueco por anidamiento
    polys.sort(key=lambda p: p.area, reverse=True)
    result = polys[0]
    for p in polys[1:]:
        result = result.symmetric_difference(p)
    return result


def poly_from_stroke(d, width):
    path = parse_path(d)
    parts = []
    for sub in path.continuous_subpaths():
        pts = subpath_points(sub)
        if len(pts) < 2:
            continue
        ls = LineString(pts)
        parts.append(ls.buffer(width / 2.0, cap_style=2, join_style=2, resolution=16, mitre_limit=2.0))
    return unary_union(parts) if parts else None


def poly_from_ellipse(cx, cy, rx, ry, w):
    n = 180
    outer = [(cx + (rx + w / 2) * math.cos(2 * math.pi * i / n),
              cy + (ry + w / 2) * math.sin(2 * math.pi * i / n)) for i in range(n)]
    inner = [(cx + (rx - w / 2) * math.cos(2 * math.pi * i / n),
              cy + (ry - w / 2) * math.sin(2 * math.pi * i / n)) for i in range(n)]
    return Polygon(outer, [inner])


def build_shape(shape):
    t = shape[0]
    if t == "rect":
        _, x, y, w, h = shape
        return box(x, y, x + w, y + h)
    if t == "fill":
        return poly_from_d_even_odd(shape[1])
    if t == "stroke":
        return poly_from_stroke(shape[1], shape[2])
    if t == "strokeclip":
        _, d, w, y0, y1 = shape
        p = poly_from_stroke(d, w)
        return p.intersection(box(-500, y0, 900, y1)) if p else None
    if t == "ellipse":
        _, cx, cy, rx, ry, w = shape
        return poly_from_ellipse(cx, cy, rx, ry, w)
    raise ValueError(t)


def glyph_polygon(shapes):
    parts = [build_shape(s) for s in shapes]
    parts = [p for p in parts if p is not None and not p.is_empty]
    if not parts:
        return None
    u = unary_union(parts)
    return u.buffer(0)


def to_font(pt):
    """SVG -> coordenadas de fuente (origen en linea base, y hacia arriba)."""
    x, y = pt
    return (round(x * SCALE), round((BASELINE_Y - y) * SCALE))


def draw(pen, geom):
    if geom is None or geom.is_empty:
        return
    polys = list(geom.geoms) if geom.geom_type == "MultiPolygon" else [geom]
    for poly in polys:
        for ring in [poly.exterior] + list(poly.interiors):
            coords = list(ring.coords)[:-1]
            if len(coords) < 3:
                continue
            pen.moveTo(to_font(coords[0]))
            for c in coords[1:]:
                pen.lineTo(to_font(c))
            pen.closePath()


CMAP_EXTRA = {
    "Ntilde": 0x00D1, "zero": ord("0"), "one": ord("1"), "two": ord("2"),
    "three": ord("3"), "four": ord("4"), "five": ord("5"), "six": ord("6"),
    "seven": ord("7"), "eight": ord("8"), "nine": ord("9"),
    "period": ord("."), "comma": ord(","), "colon": ord(":"), "semicolon": ord(";"),
    "exclam": ord("!"), "exclamdown": 0x00A1, "question": ord("?"), "questiondown": 0x00BF,
    "hyphen": ord("-"), "endash": 0x2013, "parenleft": ord("("), "parenright": ord(")"),
    "quotedbl": ord('"'), "quotesingle": ord("'"), "slash": ord("/"),
    "plus": ord("+"), "percent": ord("%"), "ampersand": ord("&"), "at": ord("@"),
    "Aacute": 0x00C1, "Eacute": 0x00C9, "Iacute": 0x00CD, "Oacute": 0x00D3,
    "Uacute": 0x00DA, "Udieresis": 0x00DC,
    "dollar": ord("$"), "euro": 0x20AC, "degree": 0x00B0,
    "guillemotleft": 0x00AB, "guillemotright": 0x00BB,
    "bracketleft": ord("["), "bracketright": ord("]"),
    "braceleft": ord("{"), "braceright": ord("}"),
    "equal": ord("="), "multiply": 0x00D7, "divide": 0x00F7,
    "less": ord("<"), "greater": ord(">"), "bar": ord("|"),
    "backslash": ord("\\"), "underscore": ord("_"), "asterisk": ord("*"),
}

glyph_order = [".notdef", "space"] + list(GLYPHS.keys())
glyphs, metrics, cmap = {}, {}, {}

pen = TTGlyphPen(None)
glyphs[".notdef"] = pen.glyph()
metrics[".notdef"] = (round(W_ADV := 106 * SCALE), 0)
pen = TTGlyphPen(None)
glyphs["space"] = pen.glyph()
metrics["space"] = (round(60 * SCALE), 0)
cmap[ord(" ")] = "space"

from shapely.affinity import translate as shp_translate

for name, (sb, shapes) in GLYPHS.items():
    geom = glyph_polygon(shapes)
    if geom is None or geom.is_empty:
        pen = TTGlyphPen(None)
        glyphs[name] = pen.glyph()
        metrics[name] = (round(60 * SCALE), 0)
        continue
    minx, _, maxx, _ = geom.bounds
    ink_w = maxx - minx
    geom = shp_translate(geom, xoff=(sb - minx))   # tinta empieza en el margen
    advance = ink_w + 2 * sb
    pen = TTGlyphPen(None)
    draw(pen, geom)
    glyphs[name] = pen.glyph()
    metrics[name] = (round(advance * SCALE), round(sb * SCALE))
    cp = CMAP_EXTRA.get(name, ord(name) if len(name) == 1 else None)
    if cp:
        cmap[cp] = name

fb = FontBuilder(UPEM, isTTF=True)
fb.setupGlyphOrder(glyph_order)
fb.setupCharacterMap(cmap)
fb.setupGlyf(glyphs)
fb.setupHorizontalMetrics(metrics)
fb.setupHorizontalHeader(ascent=780, descent=-220)
fb.setupNameTable({
    "familyName": "Heredia Ni\u00f1o",
    "styleName": "Regular",
    "uniqueFontIdentifier": "HerediaNino-Regular-1.0",
    "fullName": "Heredia Ni\u00f1o Regular",
    "psName": "HerediaNino-Regular",
    "version": "Version 1.0",
})
fb.setupOS2(sTypoAscender=780, sTypoDescender=-220, usWinAscent=800, usWinDescent=250,
            sCapHeight=700, sxHeight=700)
fb.setupPost()

# kerning (tabla kern clasica, formato 0)
from fontTools.ttLib.tables._k_e_r_n import KernTable_format_0
kern_pairs = {(a, b): round(v * SCALE) for (a, b), v in KERN.items()}
st = KernTable_format_0()
st.coverage, st.version, st.format, st.tupleIndex = 1, 0, 0, None
st.kernTable = kern_pairs
kern = fb.font["kern"] = __import__("fontTools.ttLib.tables._k_e_r_n", fromlist=["table__k_e_r_n"]).table__k_e_r_n()
kern.version, kern.kernTables = 0, [st]

fb.save("/mnt/user-data/outputs/HerediaNino-Regular.ttf")
print("glifos:", len(glyphs), "| codepoints:", len(cmap))
