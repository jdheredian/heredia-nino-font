# Instrucciones del proyecto — tipografía Heredia Niño

Copiar el contenido de este archivo en las instrucciones del proyecto, y subir a los archivos del proyecto: `especificacion_tipografia.md`, `glyphs.py`, `build_font.py`, `preview.py` y `HerediaNino-Regular.ttf`.

---

## Qué es esto

Estamos diseñando una tipografía llamada **Heredia Niño**, reconstruida a partir del rótulo del Edificio Félix Restrepo. Es una sans-serif geométrica condensada, monolineal, solo mayúsculas, de aire Art Deco.

`especificacion_tipografia.md` es la fuente de verdad: contiene las métricas, las reglas de construcción, las coordenadas de cada glifo y el estado de cada uno. **Consúltalo antes de proponer cualquier cambio y actualízalo después de cada cambio aceptado.**

## Las tres reglas del sistema

1. **Regla de los tercios.** Ningún trazo horizontal medio va centrado: va al 66% de la altura, contado desde arriba. Excepciones documentadas en la especificación.
2. **Regla de tangencia.** Toda unión entre curva y recta debe ser tangente. En una fuente monolineal no hay modulación de grosor que disimule un empate mal resuelto.
3. **Regla de contorno único.** Cada glifo se dibuja como uno o más contornos cerrados, nunca como piezas superpuestas. El contorno interior se dibuja aparte, no se deriva restándole el grosor al exterior.

## Cómo trabajar

El flujo es: editar `glyphs.py` → ejecutar `build_font.py` → renderizar una muestra con PIL → mirarla → iterar.

```bash
pip install fonttools svgpathtools shapely --break-system-packages
python3 build_font.py
```

`preview.py` sirve para comparar variantes de un glifo sin reconstruir la fuente entera.

**Adjunta siempre una imagen del resultado** después de cada ajuste. No describas cómo quedó: muéstralo.

## Verificaciones obligatorias después de cada cambio

Ejecutar y reportar:

```python
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
f = TTFont('HerediaNino-Regular.ttf'); gs = f.getGlyphSet(); hm = f['hmtx']
for n in f.getGlyphOrder():
    if n in ('.notdef','space'): continue
    bp = BoundsPen(gs); gs[n].draw(bp)
    if not bp.bounds: continue
    x0,y0,x1,y1 = bp.bounds; adv,_ = hm[n]
    if x0 < 0 or adv-x1 < 0: print(n, 'se sale de la caja horizontal')
    if y1 > 730 or y0 < -20: print(n, 'se sale de la caja vertical', y0, y1)
```

Los acentos, la Ñ, los paréntesis, las llaves, la coma, la barra vertical, el subrayado y el signo de dólar sí exceden legítimamente esos límites. Todo lo demás no.

## Errores ya cometidos — no repetirlos

- **Límite de inglete.** El buffer de shapely debe llevar `mitre_limit=2.0`. Con el valor por defecto (5.0) los giros cerrados generan espigas de hasta 9 unidades.
- **Márgenes laterales.** El segundo valor de cada entrada en `GLYPHS` es el **margen lateral**, no el paso de avance. El paso se calcula solo, a partir de la tinta real.
- **Radios de arco insuficientes.** Si la distancia entre extremos excede lo que los radios permiten, SVG los escala y el arco sale más grande de lo calculado. Se detecta porque el glifo se sale de la caja vertical. La solución es partir el arco en dos segmentos de menos de 180°, que dejan el centro determinado.
- **Ensamblaje en vez de contorno.** Un rectángulo con una diagonal encima deja costura visible. Pasó con la Z, la G, el 8, el 4, el 7 y el porcentaje.
- **Barra horizontal en el 3.** Una barra plana arriba seguida de una diagonal descendente es el trazado del 7, la Z y la Ʒ. El 3 necesita que la parte alta sobresalga hacia la derecha.

## Decisiones tomadas que no hay que reabrir sin motivo

- Grosor de trazo en 22 (11% de la altura). Se probó 28 y pesa demasiado.
- Proporción condensada: 80 de ancho para rectas, 84 para redondas, sobre 200 de altura.
- El 6 es la rotación exacta de 180° del 9. Esto pone la unión del 6 al 34% en lugar del 66%: se aceptó a cambio de la simetría del par.
- La S se construye por tercios: arco + diagonal recta tangente + arco. El ángulo de contacto es 130.7°.

## Pendientes

1. Aplicar la corrección óptica de horizontales (19 en vez de 22) a los glifos que aún tienen trazo parejo.
2. Rehacer como contorno único: 6, 9 y el porcentaje.
3. Decidir si el 2 y el 5 se vuelven angulares para acompañar al 3.
4. Decidir si los números serán tabulares.
5. Pasar el kerning de la tabla `kern` clásica a GPOS.
6. Completar la tabla de kerning: hoy solo tiene cuatro pares.
7. Redibujar los contornos con curvas reales en un editor. El archivo actual tiene todas las curvas poligonizadas, con unos 16.000 puntos frente a los ~1.500 de una fuente bien dibujada.

## Cómo quiero que trabajes

- Antes de proponer un cambio, mira qué dice la especificación sobre ese glifo.
- Si un ajuste rompe una regla del sistema, dilo explícitamente en vez de aplicarlo en silencio.
- Si algo no funciona después de dos o tres intentos, dilo y explica por qué en lugar de seguir probando.
- Distingue siempre entre lo medido en la foto original y lo decidido por diseño. La sección "Procedencia" de la especificación lleva esa cuenta.
