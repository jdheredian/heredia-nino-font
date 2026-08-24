# Heredia Niño

Heredia Niño es una tipografía sans-serif geométrica, condensada, monolineal y de solo mayúsculas. Su diseño se reconstruyó a partir del rótulo del Edificio Félix Restrepo. La fuente se define en código Python y se compila a un archivo TrueType mediante fontTools.

## 1. Origen y alcance del proyecto

La fotografía de partida tenía una resolución de apenas 10 a 14 píxeles por letra, así que solo unas pocas medidas pudieron tomarse del rótulo original. El resto del diseño corresponde a un sistema coherente construido a partir de esas medidas. La distinción entre lo medido y lo decidido se documenta en la sección de procedencia de la especificación tipográfica.

Este repositorio no contiene un archivo maestro en el sentido tradicional del diseño de tipografías. No hay un editor tipográfico de por medio. Cada glifo se define como una composición de trayectorias SVG en un diccionario de Python, y esa definición se convierte en contornos mediante una canalización geométrica basada en shapely. El archivo TrueType resultante sirve para evaluar y componer la fuente en uso real, no para su edición directa.

## 2. Documentos de referencia

Antes de proponer o aplicar un cambio, conviene revisar los siguientes documentos:

- [`especificacion_tipografia.md`](especificacion_tipografia.md): fuente de verdad del proyecto. Contiene las métricas maestras, las reglas de construcción, las coordenadas de cada glifo, el estado de avance de cada uno y la procedencia de cada decisión de diseño.
- [`INSTRUCCIONES_PROYECTO.md`](INSTRUCCIONES_PROYECTO.md): reglas de trabajo, errores ya identificados que no deben repetirse y decisiones que se consideran cerradas.

## 3. Requisitos e instalación

La compilación de la fuente requiere Python 3 y las siguientes bibliotecas:

```bash
pip install fonttools svgpathtools shapely pillow --break-system-packages
```

## 4. Flujo de trabajo

El ciclo de edición consiste en modificar la definición de un glifo, recompilar la fuente y observar el resultado antes de continuar con el siguiente ajuste.

```bash
python3 build_font.py     # genera HerediaNino-Regular.ttf a partir de glyphs.py
python3 preview.py        # compara variantes de un glifo sin recompilar la fuente completa
```

Para revisar la fuente compilada en el navegador, se incluye una página de prueba interactiva:

```bash
python3 -m http.server
```

Con el servidor activo, `preview.html` puede abrirse en `http://localhost:8000/preview.html`. La página permite escribir texto libre con la tipografía, observar palabras de prueba y examinar una rejilla con el alfabeto, la puntuación y los símbolos, con guías de altura de mayúscula y línea de base superpuestas para identificar imperfecciones de trazado. Dado que los navegadores conservan en caché los archivos de fuente, se recomienda recargar la página después de cada recompilación.

### Verificación después de cada cambio

Después de cada ajuste, se recomienda recorrer los glifos del archivo compilado en busca de contornos que excedan la caja de diseño:

```python
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

f = TTFont('HerediaNino-Regular.ttf')
gs = f.getGlyphSet()
hm = f['hmtx']

for n in f.getGlyphOrder():
    if n in ('.notdef', 'space'):
        continue
    bp = BoundsPen(gs)
    gs[n].draw(bp)
    if not bp.bounds:
        continue
    x0, y0, x1, y1 = bp.bounds
    adv, _ = hm[n]
    if x0 < 0 or adv - x1 < 0:
        print(n, 'se sale de la caja horizontal')
    if y1 > 730 or y0 < -20:
        print(n, 'se sale de la caja vertical', y0, y1)
```

Los acentos, la eñe, los paréntesis, las llaves, la coma, la barra vertical, el subrayado y el signo de dólar exceden legítimamente esos límites por diseño. Cualquier otro glifo que aparezca en el reporte debe corregirse.

## 5. Estructura del repositorio

| Archivo | Contenido |
|---|---|
| `glyphs.py` | Definición de cada glifo como trayectorias SVG y márgenes laterales, junto con la tabla de pares de kerning |
| `build_font.py` | Canalización que convierte las definiciones en contornos y ensambla el archivo TrueType |
| `preview.py` | Comparación de variantes de un glifo antes de incorporarlas a `glyphs.py` |
| `preview.html` | Banco de pruebas interactivo para la fuente ya compilada |
| `especificacion_tipografia.md` | Especificación completa del diseño |
| `INSTRUCCIONES_PROYECTO.md` | Reglas de trabajo del proyecto |
| `HerediaNino-Regular.ttf` | Fuente compilada, lista para instalación y prueba |
| `muestra.png` | Imagen de referencia del rótulo original o de una muestra compuesta |

## 6. Reglas de construcción

El sistema de diseño se apoya en tres reglas que se aplican a la totalidad del alfabeto:

1. **Regla de los tercios.** Ningún trazo horizontal medio se centra en la altura de la letra. Se ubica al 66 % de la altura contado desde arriba, con excepciones documentadas en la especificación. Los números siguen la misma lógica al 33 %.
2. **Regla de tangencia.** Toda unión entre una curva y una recta debe salir en la misma dirección de la tangente de la curva. Al tratarse de una fuente monolineal, no existe modulación de grosor que disimule una unión mal resuelta.
3. **Regla de contorno único.** Cada glifo se dibuja como uno o más contornos cerrados. El contorno interior se dibuja de manera independiente y no se deriva restando grosor al contorno exterior.

El detalle de cada regla, sus excepciones y la justificación de cada una se documentan en la especificación tipográfica.

## 7. Estado del proyecto

La especificación registra, glifo por glifo, cuáles están resueltos como contorno único, cuáles tienen aplicada la corrección óptica de trazos horizontales y cuáles siguen pendientes de rehacerse desde cero. Entre las tareas pendientes de mayor alcance se encuentran el rediseño de los contornos con curvas reales en un editor tipográfico, dado que el archivo actual poligoniza cada curva, y el paso de la tabla de kerning al formato GPOS. El listado completo de trabajo pendiente se encuentra en la sección final de la especificación.
