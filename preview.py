import sys
from PIL import Image, ImageDraw
from build_font import glyph_polygon

def render(variants, path, scale=1.45, gap=40):
    """variants: lista de (etiqueta, shapes)"""
    geoms = [glyph_polygon(sh) for _, sh in variants]
    W = int((160 * len(geoms) + gap * (len(geoms) + 1)) * scale)
    H = int(300 * scale)
    img = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(img)
    for i, g in enumerate(geoms):
        ox = (gap + i * (160 + gap)) * scale
        polys = list(g.geoms) if g.geom_type == "MultiPolygon" else [g]
        for poly in polys:
            ext = [(ox + x * scale, y * scale) for x, y in poly.exterior.coords]
            d.polygon(ext, fill=0)
            for ring in poly.interiors:
                d.polygon([(ox + x * scale, y * scale) for x, y in ring.coords], fill=255)
    img.save(path)
    return path

if __name__ == "__main__":
    A = [("stroke", "M48 29 H108 L80 152 A32 29.5 0 1 1 55.5 200.5", 22)]
    B = [("stroke", "M48 29 H108 L80 152 L110 205 H48", 22)]
    C = [("stroke", "M51.8 69.5 A30 61.5 0 1 1 80 152 A32 29.5 0 1 1 55.5 200.5", 22)]
    render([("A", A), ("B", B), ("actual", C)], "/mnt/user-data/outputs/variantes_3.png")
    print("ok")
