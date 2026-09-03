# Auditoría visual y técnica del PDF v0.10.0

## Resultado

**PASS.** Se renderizaron las 46 páginas finales con Poppler a 110 ppp, se decodificaron todos los PNG, se generó `PDF_CONTACT_SHEET_v0.10.0.png` y se inspeccionaron las 46 miniaturas. Luego se revisaron a tamaño real portada, primera y última página de la carta, índice, gráficos dobles, F10, F27, F28, los cuatro mapas, tablas, glosario, bibliografía y colofón.

| Control | Resultado | Estado |
|---|---|---|
| tamaño | 595,276 × 841,890 pt, A4 real | PASS |
| orientación | 46 páginas verticales | PASS |
| portada | nueva, sin conteo de figuras | PASS |
| carta | comienza en página posterior a portada; firma visible | PASS |
| índice | enlaces y folios coherentes con portada no numerada | PASS |
| fuentes | Source Serif 4 y Source Sans 3 incrustadas | PASS |
| texto | seleccionable y extraíble | PASS |
| marcadores | jerarquía de capítulos y material final | PASS |
| enlaces | índice interno y bibliografía externa anotados | PASS |
| imágenes | 28 PNG decodificados; resolución efectiva suficiente | PASS |
| contraste | texto, ejes, leyendas y recuadros conservan jerarquía a tamaño A4 | PASS |
| escala de grises | contact sheet convertida e inspeccionada; series conservan etiquetas, contornos o diferencias tonales | PASS |
| mapas | relieve, leyendas, límites y pies legibles | PASS |
| tablas | dentro de margen; encabezados repetibles | PASS |
| glifos | acentos, CO₂, signos menos y comillas correctos | PASS |
| páginas vacías | cero páginas involuntarias | PASS |
| superposición/corte | cero defectos observados | PASS |
| pies separados | cero | PASS |
| hipervínculos crudos | cero URLs impresas como residuo | PASS |
| carta alterada | comparación textual normalizada exacta | PASS |

La página de cierre de la carta y algunas transiciones conservan espacio en blanco deliberado para no adelantar el índice o un capítulo. No se clasifican como páginas vacías.
