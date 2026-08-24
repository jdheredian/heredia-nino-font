# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

El proyecto se trabaja en español: escribe la documentación, los comentarios y las respuestas en español.

## Qué es este repositorio

Diseño de la tipografía **Heredia Niño**: sans-serif geométrica condensada, monolineal, solo mayúsculas, reconstruida a partir del rótulo del Edificio Félix Restrepo. No hay editor tipográfico de por medio: los glifos se definen como paths SVG en Python y la fuente se compila con fontTools.

Documentos rectores, que hay que leer antes de tocar nada:

- [especificacion_tipografia.md](especificacion_tipografia.md) — **fuente de verdad**. Métricas, reglas de construcción, coordenadas por glifo, estado de cada glifo y procedencia de cada decisión. Consúltalo antes de proponer un cambio y actualízalo después de cada cambio aceptado.
- [INSTRUCCIONES_PROYECTO.md](INSTRUCCIONES_PROYECTO.md) — reglas de trabajo, errores ya cometidos que no hay que repetir y decisiones cerradas.

## Comandos

```bash
pip install fonttools svgpathtools shapely pillow --break-system-packages
python3 build_font.py     # glyphs.py -> HerediaNino-Regular.ttf
python3 preview.py        # compara variantes de un glifo sin recompilar la fuente
```

Las dependencias **no** están instaladas en este entorno; hay que instalarlas antes de compilar.

Tanto `build_font.py` como `preview.py` escriben en `/mnt/user-data/outputs/`, una ruta heredada del entorno donde se creó el proyecto y que aquí no existe. Al ejecutarlos en local hay que apuntar la salida al directorio del repo (el `.ttf` versionado está en la raíz).

`preview.py` no tiene interfaz: se edita el bloque `__main__` para meter ahí las variantes que se quieren comparar, en el mismo formato de `shapes` que usa `GLYPHS`.

### Verificación obligatoria después de cada cambio

Ejecutar y reportar (script completo en [INSTRUCCIONES_PROYECTO.md](INSTRUCCIONES_PROYECTO.md)): recorrer todos los glifos del `.ttf` con `BoundsPen` y detectar los que se salen de la caja horizontal (`x0 < 0` o `adv - x1 < 0`) o de la vertical (`y1 > 730`, `y0 < -20`). Exceden legítimamente: acentos, Ñ, paréntesis, llaves, coma, barra vertical, subrayado y dólar. Nada más.

Además, **adjunta siempre una imagen del resultado** después de cada ajuste; no describas cómo quedó.

## Arquitectura

Flujo: editar `glyphs.py` → `build_font.py` → renderizar muestra → mirarla → iterar.

**[glyphs.py](glyphs.py)** — datos, sin lógica. `GLYPHS` es `{nombre: (margen_lateral, [shapes])}`. Ojo: el segundo valor es el **margen lateral**, no el paso de avance; el paso lo calcula `build_font.py` a partir de la tinta real. Tipos de `shape`: `rect`, `fill` (path relleno, regla par-impar), `stroke` (path engrosado), `strokeclip` (engrosado y recortado en Y, para diagonales que rebasan la caja) y `ellipse`. `KERN` guarda los pares de kerning.

**[build_font.py](build_font.py)** — pipeline geométrico:

1. Cada `shape` se convierte en un polígono de shapely. Las curvas se **muestrean** a paso `STEP = 1.6` y los trazos se engrosan con `LineString.buffer(w/2, join_style=2, mitre_limit=2.0)`. El `mitre_limit` es obligatorio: con el valor por defecto los giros cerrados generan espigas.
2. `unary_union` funde los shapes de un glifo en una sola geometría.
3. `to_font` convierte SVG → coordenadas de fuente: `(x·3.5, (220 − y)·3.5)`. Altura de mayúscula 200 en SVG → 700 sobre 1000 upem.
4. Cada glifo se traslada para que la tinta empiece en el margen lateral, y el avance sale de `ancho_de_tinta + 2·margen`.
5. `FontBuilder` arma glyf, cmap (`CMAP_EXTRA` mapea los nombres no ASCII a codepoints), métricas, nombres, OS/2 y la tabla `kern` clásica formato 0.

Consecuencia de diseño: **toda curva sale poligonizada** (~16.000 puntos). El `.ttf` sirve para evaluar y componer, no como archivo maestro.

**Sistema de coordenadas.** Todo en `glyphs.py` y en la especificación está en convención SVG (origen arriba a la izquierda, Y hacia abajo; mayúscula de y=20 a y=220). La inversión ocurre solo en `to_font`.

## Las tres reglas del sistema

1. **Regla de los tercios.** Ningún trazo horizontal medio va centrado: va al 66% de la altura contado desde arriba (los números, al 33%). Excepciones documentadas en la especificación.
2. **Regla de tangencia.** Toda unión curva-recta debe ser tangente. Al ser monolineal no hay modulación de grosor que disimule un empate mal resuelto.
3. **Regla de contorno único.** Cada glifo se dibuja como contornos cerrados, nunca como piezas superpuestas; el contorno interior se dibuja aparte, no restándole grosor al exterior. Un rectángulo con una diagonal encima deja costura visible.

Si un ajuste rompe una de estas reglas, dilo explícitamente en vez de aplicarlo en silencio.

## Cómo trabajar

- Distingue siempre entre lo **medido** en la foto original y lo **decidido** por diseño; la sección "Procedencia" de la especificación lleva esa cuenta.
- No reabras sin motivo las decisiones cerradas (grosor 22, proporción 80/84 sobre 200, el 6 como rotación del 9, la S por tercios a 130.7°).
- Si algo no sale después de dos o tres intentos, dilo y explica por qué en lugar de seguir probando.
