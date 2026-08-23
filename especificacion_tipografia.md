# Heredia Niño — especificación tipográfica

Fuente reconstruida a partir del rótulo del Edificio Félix Restrepo.

Documento de trabajo para llevar el diseño a un editor tipográfico (Glyphs, FontForge, Birdfont). Recoge las métricas, las reglas de construcción, el estado de cada glifo y las coordenadas de trazado desarrolladas durante el proceso.

**Advertencia general:** esto no es una digitalización del rótulo original. La foto de partida tenía una resolución de apenas 10–14 píxeles por letra, así que solo unas pocas medidas son fieles. El resto es un sistema de diseño coherente construido a partir de esas medidas. Ver la sección "Procedencia" para saber qué viene de dónde.

---

## 1. Métricas maestras

Todas las medidas en unidades de un espacio de diseño donde la altura de mayúscula es 200.

| Parámetro | Valor | Nota |
|---|---|---|
| Altura de mayúscula | 200 (y = 20 a 220) | |
| Trazo vertical | 22 | 11% de la altura |
| Trazo horizontal | 19 | Corrección óptica |
| Ancho de letra recta | 80 | 40% de la altura |
| Ancho de letra redonda | 84 | 42% de la altura |
| Ancho de letra ancha (A, M, W) | 110 | |
| Descendente (coma, punto y coma) | 252 | |

### Desbordamiento óptico

| Tipo de terminal | Desborde | Glifos |
|---|---|---|
| Curvo | +2 arriba y abajo | O, C, G, Q, S, U, J, 0 |
| Vértice truncado | +2 abajo | A, V, W |
| Plano | 0 | B, D, E, F, H, I, K, L, M, N, P, R, T, X, Y, Z |

### Espaciado

| Tipo | Margen lateral | Paso |
|---|---|---|
| Recta (E, F, H, L, T, N…) | 13 | 106 |
| Redonda (O, C, G, Q, S) | 10 | 104 |
| I | 14 | 50 |
| Ancha (A, M, W) | 6 | 122 |
| Espacio entre palabras | — | 60 |

### Pares de kerning identificados

| Par | Ajuste |
|---|---|
| R + E | +8 |
| T + R | −6 |
| D + I | −6 |
| I + A | −14 |

Esta tabla está incompleta. Se identificaron probando tres palabras; un set real necesita revisar todas las combinaciones problemáticas, sobre todo diagonales junto a letras estrechas.

---

## 2. Las tres reglas de construcción

### Regla de los tercios

**Todo trazo horizontal medio va al 66%** de la altura, contada desde arriba. Nunca centrado.

Aplica a E, F, H, A, K, Y, Z, G, P, R, B y al número 4.

**Los números van al 33%, no al 66%**, con dos excepciones. Se probaron ambas alturas: al 66% el 3 y el 5 pierden legibilidad y el 8 queda volcado hacia arriba; al 33% recuperan una silueta natural. Las excepciones son el **9**, que conserva la unión al 66% y queda como el acento de la serie, y el **4**, cuyo travesaño divide espacio en vez de cerrar curva y cuyo contraojal se reduce a un triángulo diminuto si sube. El 6 acompaña al 33% por ser rotación del 9. Salió de medir dos E distintas del rótulo original, que dieron 65% y 66% de forma independiente; la P del rótulo midió ~60%, coherente con la misma regla.

Durante el proceso se probó una segunda dirección (34%, cintura alta) para las letras que cierran curvas. Se descartó: con el trazo delgado y los contraojales dibujados aparte, el 66% funciona mejor en P, R y B, y además deja los huecos alargados como los del resto de la fuente en lugar de casi cuadrados.

**Excepciones:**

- La **S no tiene cintura**: se construye por tercios (ver abajo). Se probó con el cruce al 66% y no funciona — la curva inferior se queda sin altura para completar la reversión.
- El **3** también va al 66%, construido con dos arcos elípticos que se unen en el centro exacto de la letra. Se probó primero uniéndolos en el borde izquierdo y no funciona: los dos extremos coinciden en la misma vertical y la cifra se lee como una "Ǝ".
- **El 6 es la rotación exacta de 180° del 9.** Esto pone su unión al 34% en lugar del 66%: no se puede tener simetría del par y la regla al mismo tiempo, porque la unión del 9 medida desde arriba equivale a la del 6 medida desde abajo. Se privilegió la simetría, porque el par 6/9 es de los pocos sitios donde el ojo compara dos glifos directamente.
- El **2** no tiene unión horizontal que reglar; su hombro se resuelve por proporción del arco.
- La **cintura de la B se comparte** entre las dos panzas: un solo trazo de 22, no el trazo de cierre de la panza superior más el de apertura de la inferior, que daría 44.
- El **puente del 8** en la cintura no debe estrangularse hasta el grosor de un trazo, o las dos panzas se leen como óvalos separados. Se dejó en 48 unidades.
- La **cintura del 8 se comparte** entre las dos panzas, igual que en la B: un solo trazo horizontal de 19, no el de cierre de la panza superior más el de apertura de la inferior.

### Regla de tangencia

Toda unión entre una curva y una recta debe ser tangente: el trazo que se desprende sale siguiendo la dirección de la curva, nunca cruzándola en ángulo. En una fuente monolineal esto pesa más que en una con contraste, porque no hay modulación de grosor que disimule el empate.

Se aplica sobre todo en la G (la barra sale del punto donde el óvalo tiene tangente vertical), la Q, la J, el 6 y el 9.

### Construcción por tercios de la S

La S no se dibuja con curvas libres sino con **arco + diagonal recta + arco**: un tercio de altura para cada elemento. Los dos arcos son elipses idénticas de rx 31 y ry 36, centradas en (80, 65) y (80, 175), y giran 230° cada una. La diagonal las une pasando por el centro exacto de la letra, en (80, 120).

El punto clave es el ángulo de contacto. Para que la diagonal salga tangente de los dos arcos sin producir un quiebre, tiene que tocarlos a **130.7°**, lo que sitúa los puntos de contacto en y=88.5 y y=151.5 — prácticamente los tercios. Ese ángulo se resuelve igualando la pendiente de la tangente del arco, que es (ry/rx)·tan(t), con la pendiente de la diagonal.

Esto tiene una consecuencia importante: al quedar definida por elipses de radio conocido en lugar de curvas dibujadas a ojo, la S pasa a ser calculable. Se le puede derivar el contorno interior y aplicarle la corrección óptica de horizontales, cosa que antes era imposible.

### Regla de contorno único

Cada glifo se dibuja como uno o más contornos cerrados, nunca como piezas superpuestas. Un rectángulo más una diagonal encima deja una costura visible donde se tocan. El contorno interior se dibuja aparte del exterior, no se deriva restándole el grosor del trazo — si se deriva, las curvas interiores quedan pinchadas cuando el radio exterior es pequeño.

Truco práctico: en la panza de la P el contorno exterior empieza a curvarse en x=94 y el interior en x=84. Así el hueco tiene radio 16 en vez de 6, y el grosor se mantiene en 22 arriba y al costado.

---

## 3. Estado de cada glifo

Esto es lo más importante del documento para el trabajo en Glyphs.

### Resueltos como contorno único

Listos para trazar directo. A, B, D, E, F, H, I, L, N, P, R, T, Z, 1, 4, 7, 8, y toda la puntuación salvo el porcentaje.

### Resueltos como contorno, con corrección óptica aplicada

O, C, G, Q, 0. Tienen los trazos horizontales en 19 y los verticales en 22, con contornos interior y exterior independientes.

### Trazo simple sin corrección óptica

K, M, U, V, W, X, Y, J, S, 2, 3, 5, 6, 9, & y @. La S, el 3, el & y la @ ya son geométricamente calculables, así que son las primeras candidatas a recibirla. Dibujados con grosor parejo de 22. Funcionan, pero les falta el afinado de horizontales.

### Pendientes de rehacer desde cero

Estos siguen siendo ensamblaje de piezas y hay que redibujarlos:

- **6 y 9** — óvalo más cola. La unión es tangente (la cola arranca del punto más ancho del óvalo, donde la tangente es vertical), pero siguen siendo dos piezas y no un contorno.
- **%** — tres piezas superpuestas; la barra pasa por detrás de los óvalos sin fundirse.
- **Ñ (tilde)** — el único elemento de toda la fuente con curva libre. Se puede rehacer como dos arcos de círculo tangentes para que sea coherente con la lógica geométrica.

### Sin diseñar

- Minúsculas. El rótulo original era solo mayúsculas, así que no hay base de partida.

---

## 4. Procedencia de las decisiones

| Decisión | Origen |
|---|---|
| Barra de la E al 66% | Medido en dos instancias de la foto (15/7 px y 14.5/7.5 px) |
| Proporción angosta (~42%) | Medido: O de 11 × 26 px |
| Ancho de la D mayor que la O | Medido: 14 px vs 11 px |
| Grosor de trazo (11%) | **Decisión de diseño.** La medición dio 25% pero estaba inflada por el desenfoque de la foto; se fijó en 11% por criterio visual |
| Cintura de B, P y R al 66% | Medido indirectamente: la P del rótulo dio ~60%. No hay B ni S en el rótulo |
| Excepción del 34% en S y 3 | **Decisión de diseño.** Probado al 66% y descartado |
| Uniones tangentes | **Decisión de diseño.** Práctica estándar |
| Desbordamiento óptico | **Decisión de diseño.** Práctica estándar |
| Espaciado y kerning | **Decisión de diseño.** No hay forma de medirlo en la foto |
| Todo el set de números y puntuación | **Decisión de diseño.** El rótulo no tiene ninguno |

Letras del rótulo que nunca se pudieron medir por estar borrosas o en sombra: F, R, S, T, L, X.

---

## 5. Coordenadas de trazado

**Importante — conversión de ejes.** Todas las coordenadas de esta sección están en convención SVG: el origen está arriba a la izquierda y la Y crece hacia abajo. Glyphs, FontForge y cualquier editor tipográfico trabajan al revés: el origen está en la línea de base y la Y crece hacia arriba.

Al importar hay que invertir el eje. La fórmula es:

```
y_editor = (220 - y_svg) × escala
```

donde 220 es la línea de base en coordenadas SVG. Con una escala de 3.5 se obtiene una altura de mayúscula de 700 unidades sobre un cuerpo de 1000, que es la convención habitual. Con esa escala:

| Referencia | SVG | Editor (1000 upem) |
|---|---|---|
| Altura de mayúscula | y = 20 | 700 |
| Línea de base | y = 220 | 0 |
| Desborde superior de curvas | y = 18 | 707 |
| Desborde inferior de curvas | y = 222 | −7 |
| Fondo de la coma | y = 252 | −112 |
| Alto de la tilde de la Ñ | y = −30 | 875 |

Si se omite la inversión, todos los glifos salen reflejados verticalmente.

### Mayúsculas

```
A  M25 223 L68 17 L92 17 L135 223 Z
   M80 76 L66 141 L94 141 Z
   M61 163 L99 163 L111 223 L49 223 Z          (regla par-impar)

B  M40 20 H94 A28 66 0 0 1 94 152 H92 A30 34 0 0 1 92 220 H40 Z
   M62 42 H80 A20 49.5 0 0 1 80 141 H62 Z
   M62 163 H84 A16 17.5 0 0 1 84 198 H62 Z

C  M110.5 50 A42 102 0 1 0 110.5 190 L90.7 190 A20 83 0 1 1 90.7 50 Z

D  M40 20 H91 A31 100 0 0 1 91 220 H40 Z
   M62 42 H78 A22 78 0 0 1 78 198 H62 Z

E  rect(40,20,22,200) rect(40,20,80,22) rect(40,141,62,22) rect(40,198,80,22)

F  rect(40,20,22,200) rect(40,20,80,22) rect(40,141,62,22)

G  M110.5 50 A42 102 0 1 0 121 142 H80 V161 H97.4 A20 83 0 1 1 90.7 50 Z

H  rect(40,20,22,200) rect(98,20,22,200) rect(40,141,80,22)

I  rect(69,20,22,200)

J  M109 20 V160 A28 51 0 0 1 53 160                     (trazo 22)

K  rect(40,20,22,200)
   M58 152 L112 8    /    M58 152 L112 232               (trazo 22, recortar y 20–220)

L  rect(40,20,22,200) rect(40,198,80,22)

M  rect(25,20,22,200) rect(113,20,22,200)
   M36 12 L80 152 L124 12                                (trazo 22, recortar y 20–220)

N  rect(40,20,22,200) rect(98,20,22,200)
   M51 12 L109 228                                       (trazo 22, recortar y 20–220)

O  M38 120 A42 102 0 1 0 122 120 A42 102 0 1 0 38 120 Z
   M60 120 A20 83 0 1 0 100 120 A20 83 0 1 0 60 120 Z

P  M40 20 H94 A28 71.5 0 0 1 94 163 H62 V220 H40 Z
   M62 42 H80 A20 49.5 0 0 1 80 141 H62 Z

Q  igual que O, más rect(80,203,45,19)

R  contorno de P, más M70 158 L112 226                   (trazo 22, recortar y 20–220)

S  M110.5 71.25 A31 36 0 1 0 56.5 88.5
   L103.5 151.5
   A31 36 0 1 1 49.5 168.75                              (trazo 22)

T  rect(40,20,80,22) rect(69,20,22,200)

U  M51 20 V160 A29 51 0 0 0 109 160 V20                  (trazo 22)

V  M51 12 L80 235 L109 12                                (trazo 22, recortar y 20–222)

W  M36 12 L55 235 L80 70 L105 235 L124 12                (trazo 22, recortar y 20–222)

X  M53 12 L107 228  /  M107 12 L53 228                   (trazo 22, recortar y 20–220)

Y  M53 12 L80 152 L107 12                                (trazo 22, recortar y 20–220)
   rect(69,141,22,79)

Z  M40 20 L120 20 L75 198 L120 198 L120 220 L40 220 L85 42 L40 42 Z

Ñ  contorno de N, más tilde:
   M46 -12 C54 -30, 68 -30, 80 -20 C92 -10, 106 -10, 114 -26   (trazo 20 — rehacer)
```

### Números

```
0  M42 120 A38 102 0 1 0 118 120 A38 102 0 1 0 42 120 Z
   M64 120 A16 83 0 1 0 96 120 A16 83 0 1 0 64 120 Z

1  M91 20 V220 H69 V45 H48 Z

2  M49 66 A31 37 0 0 1 111 66 C111 100, 66 145, 47 209 H120     (trazo 22)

3  M52 29 H105.7 L58 88 A36 62 0 1 1 56 204                    (trazo 22)
   Barra superior, diagonal al costado superior izquierdo de la
   panza, y panza que abre de nuevo hacia la izquierda. La barra
   termina en 105.7 para que su vértice derecho quede alineado
   con el borde derecho de la panza: ambos en 116.7 de tinta.

4  M92 20 H114 V220 H92 V161 H38 V142 Z
   M62 142 L92 74 L92 142 Z

5  M118 31 H48 V88 A36 62 0 1 1 56 204                        (trazo 22)

6  elipse(80,149.5,r 30×61.5)
   más M50 149.5 V99 A34 70 0 0 1 84 29 A34 70 0 0 1 110.05 54 (trazo 22)

7  M40 20 H120 L72 220 L48 220 L91.4 39 H40 Z

8  M80 18 C104 18, 122 32, 122 56 C122 72, 110 80, 104 88
   C110 96, 122 114, 122 152 C122 198, 104 222, 80 222
   C56 222, 38 198, 38 152 C38 114, 50 96, 56 88
   C50 80, 38 72, 38 56 C38 32, 56 18, 80 18 Z
   M60 57.75 A20 20.75 0 1 0 100 57.75 A20 20.75 0 1 0 60 57.75 Z
   M60 149.75 A20 52.25 0 1 0 100 149.75 A20 52.25 0 1 0 60 149.75 Z

9  elipse(80,90.5,r 30×61.5)
   más M110 90.5 V141 A34 70 0 0 1 76 211 A34 70 0 0 1 49.95 186 (trazo 22)
   Rotación exacta de 180° del 6.
```

### Puntuación

```
.   rect(69,198,22,22)
,   M69 198 H91 V220 L76 252 H58 L69 220 Z
:   rect(69,128,22,22) rect(69,198,22,22)
;   rect(69,128,22,22) más contorno de la coma
!   M69 20 H91 L88 166 H72 Z   más rect(70,196,20,22)
¡   rect(70,22,20,22)   más M72 74 H88 L91 220 H69 Z
?   M46 66 A31 37 0 0 1 108 66 C108 98, 80 112, 80 152  (trazo 22) más rect(69,198,22,22)
¿   M114 174 A31 37 0 0 1 52 174 C52 142, 80 128, 80 88 (trazo 22) más rect(69,20,22,22)
-   rect(55,110,50,19)
–   rect(40,110,80,19)
(   M98 8 C58 62, 58 178, 98 232                        (trazo 22)
)   M62 8 C102 62, 102 178, 62 232                      (trazo 22)
"   rect(54,20,18,48) rect(88,20,18,48)
'   rect(71,20,18,48)
/   M42 234 L118 6                                      (trazo 22)
+   rect(38,110,84,19) rect(69,78,22,83)
%   elipse(52,56,r14×22 trazo16) elipse(108,184,r14×22 trazo16)
    más M34 214 L126 26 (trazo 20, recortar y 20–220) — rehacer

&   M132 172 L48 76 A30 46 0 0 1 108 76 L44 170
    A44 44 0 0 0 132 188            (trazo 22, recortar y 18–222)

@   M127.3 134.9 A48 86 0 1 0 104 194.5                 (trazo 18)
    elipse(76,120,r23×34 trazo16)
    M99 120 V150 A28 32 0 0 0 132 158                   (trazo 16)

Acento agudo   M68 -12 L94 -38                          (trazo 18)
Diéresis       rect(58,-40,18,24) rect(86,-40,18,24)
$   contorno de la S más rect(69,4,22,232)
€   M108 62 A34 78 0 1 0 108 178 (trazo 22)
    más rect(30,102,74,17) rect(30,138,74,17)
°   elipse(80,46,r16×20 trazo14)
«   M78 84 L54 120 L78 156  /  M104 84 L80 120 L104 156 (trazo 16)
»   M56 84 L80 120 L56 156  /  M82 84 L106 120 L82 156  (trazo 16)
[   M60 8 H106 V30 H82 V210 H106 V232 H60 Z
]   M100 8 H54 V30 H78 V210 H54 V232 H100 Z
{   M106 8 C86 8, 86 30, 86 62 C86 100, 76 120, 60 120
    C76 120, 86 140, 86 178 C86 210, 86 232, 106 232    (trazo 18)
=   rect(38,96,84,19) rect(38,134,84,19)
×   M54 84 L106 156  /  M106 84 L54 156                 (trazo 20)
÷   rect(38,110,84,19) rect(69,62,22,22) rect(69,156,22,22)
<   M108 62 L50 120 L108 178                            (trazo 20)
>   M52 62 L110 120 L52 178                             (trazo 20)
|   rect(69,4,22,232)
\   M42 6 L118 234                     (trazo 22, recortar y 18–222)
_   rect(30,238,100,18)
*   M80 22 V86 / M53 38 L107 70 / M107 38 L53 70        (trazo 16)
```

### Nota sobre la arroba y el ampersand

Ambos se rehicieron con arcos elípticos de centro definido, abandonando las curvas libres.

El **ampersand** es lo que más costó. Los primeros intentos fallaban porque les faltaba lo esencial de la forma: **el cruce**. Un ampersand no es un trazo continuo que serpentea, son dos diagonales que se cruzan. La estructura que funciona es cola → diagonal ascendente → lazo superior → diagonal descendente que cruza a la primera → panza inferior. También hubo que ensancharlo más allá del ancho de una mayúscula; a 72 unidades el lazo superior colapsaba en una rendija.

La **arroba** tuvo un problema distinto: con trazo 18 sobre un óvalo interior de radio 17, el hueco quedaba en 16 unidades y se cerraba. Se agrandó el óvalo y se adelgazó su trazo a 16.

Ninguno de los dos está resuelto como contorno con corrección óptica, pero ambos ya son geométricamente calculables.

---

## 6. El archivo generado

Nombre de familia: **Heredia Niño**. Estilo: Regular. Nombre PostScript: `HerediaNino-Regular` (sin eñe, porque ese campo solo admite caracteres ASCII).

Junto a este documento va un archivo `HerediaNino-Regular.ttf` funcional e instalable, con 82 glifos y 81 puntos de código: mayúsculas A–Z, vocales acentuadas, Ñ, Ü, números, puntuación, símbolos matemáticos y de moneda, arroba y ampersand. Incluye los cuatro pares de kerning y la corrección óptica donde estaba resuelta.

Sirve para probar, componer y ver la fuente en uso real. **No sirve como archivo maestro**, por tres razones:

1. **Todas las curvas están poligonizadas.** Para convertir los trazos en contornos hubo que aproximar cada curva con segmentos rectos. El archivo tiene cerca de 16.000 puntos, cuando una fuente bien dibujada de este tamaño tendría unos 1.500. En tamaños grandes se alcanzan a ver las facetas, y el porcentaje solo —con 954 puntos— pesa más que varias letras juntas.
2. **El kerning va en la tabla `kern` clásica**, no en GPOS. Algunas aplicaciones modernas la ignoran.
3. **El juego de caracteres ya cubre el español completo**: Á, É, Í, Ó, Ú, Ü, Ñ, ¿, ¡ y comillas angulares.

El camino correcto es usar este archivo para evaluar, y redibujar los contornos con curvas reales en un editor a partir de las coordenadas de la sección anterior.

---

## 7. Trabajo pendiente

1. Rehacer como contorno los glifos marcados: S, 3, 6, 9, %, tilde de la Ñ.
2. Aplicar la corrección óptica de horizontales a los glifos que aún tienen trazo parejo.
3. Componer las vocales acentuadas y la Ü.
5. Completar la tabla de kerning probando el alfabeto entero.
6. Decidir si los números serán tabulares (mismo paso para todos) o proporcionales. Ahora mismo el 1 es mucho más angosto.
7. Redibujar los contornos con curvas reales en lugar de la poligonización del archivo generado.
8. Pasar el kerning a GPOS.
9. Considerar una segunda variante de peso con trazo 28, que daría un "Black" para titulares grandes donde los contraojales cerrados dejan de ser defecto y se vuelven carácter.
