# Entrega final v0.10.0

## Resultado

Se entrega **Electricidad argentina: cambio, límites y decisiones**, subtitulado *Evolución del sistema 2005–2025, red 2026 y capacidades para una transición con criterio nacional*. Es un PDF A4 de 46 páginas, en español, acompañado por fuente narrativa, datos, scripts, 28 visuales —cuatro mapas—, registros de procedencia, controles y material de revisión.

Estado editorial: **revisión del autor**. El trabajo no fue publicado, validado institucionalmente ni revisado por pares.

## Integridad de entrada

- Única base científica: ZIP v0.8.3, SHA-256 `dc5f5348f5f82f78ec252cbc607703543f7186702bea790c6606c329e30749dc`.
- Verificación: 84.190.072 bytes, 801 entradas, prueba ZIP sana y 800/800 huellas internas coincidentes.
- Carta incorporada: `Carta a IA(2).odt`, SHA-256 `829f571e4f50bd213354f756eff3aa99d1661c1c02e1a053bfd8d027bfa95d7f`; comparación normalizada exacta contra el texto extraído del PDF.
- La primera carta adjunta se descartó al ser reemplazada por la versión indicada por el autor.
- Los materiales v0.9.0 se usaron sólo como referencia visual y editorial; no como base científica.
- Los siete PDF CAMMESA fueron inspeccionados visualmente. AlmaMDI se auditó como planilla técnica, sin interpretar campos carentes de diccionario.

## Superficie entregada

- PDF: 46 páginas A4 verticales; texto seleccionable; 74 enlaces; 18 marcadores; siete variantes tipográficas incrustadas.
- Narrativa: once capítulos, cinco anexos metodológicos, glosario, abreviaturas, listas combinadas, bibliografía y colofón.
- Visuales: 24 figuras y cuatro mapas, cada uno con fuente, lectura, significado, relevancia y límite.
- GIS recuperado: 1.299 líneas de alta tensión, 323 estaciones, 445 centrales IGN, límites provinciales y relieve Argenmap; control topológico CAMMESA 2026.
- AlmaMDI: 411 nodos; 408 georreferenciados; 94 coincidencias espaciales y nominales, seis sólo espaciales, 308 sin coincidencia confiable y tres sin coordenadas.
- Región: Argentina, Brasil, Chile y Uruguay bajo frontera 2018–2025 común, índice 2018 = 100 y métricas 2025 por habitante.
- Estrategia: matriz de nueve implicancias y matriz tecnológica preliminar, con actores, horizontes, incertidumbre y dato faltante.
- Pruebas de esfuerzo: cuatro sensibilidades horarias acotadas; no son pronóstico ni modelo de expansión, despacho o red.
- Release: 214 archivos físicos, de los cuales 213 figuran en `MANIFEST.sha256`; el manifiesto mismo es el archivo adicional.

## QA

Estado automático final: **30 PASS, 0 FAIL**. Los controles incluyen baseline, carta literal, orden frontal, A4, fuentes, texto, enlaces, marcadores, capítulos, alcance, figuras, métricas, ceros estructurales, escenarios, crosswalk, imágenes y manifiesto. La inspección visual cubrió las 46 páginas y las 28 imágenes de publicación.

El estado global del release es **PASS_WITH_LIMITATION**: no quedan fallas internas activas, pero existen límites externos que no corresponde convertir en certeza.

## Límites residuales

1. La capa de red no contiene un modelo eléctrico completo con parámetros, estados, flujos, contingencias o margen horario; los mapas no demuestran congestión.
2. La hidráulica carece de una serie integrada de caudales, niveles, restricciones, otros usos, asignación y despacho por complejo y hora.
3. La armonización regional gana comparabilidad y pierde detalle respecto de los cierres nacionales; la población no controla clima ni estructura productiva.
4. Las fuentes sobre capacidades tecnológicas prueban existencia, no escala industrial, integración nacional completa ni desempeño comparativo.
5. La sensibilidad conserva perfiles 2025 y no modela almacenamiento, vertimiento, red, fallas o despacho endógeno.
6. Las estimaciones cuantitativas heredadas siguen condicionadas a sus instrumentos, controles, frontera y resolución.

## Revisión pendiente

La siguiente secuencia es lectura integral del autor y luego revisión externa dirigida. Se recomienda examen por especialistas en transmisión y operación, hidrología e hidroelectricidad, métodos cuantitativos, planificación energética e industrial y edición generalista. `review/EXTERNAL_REVIEW_BRIEF_v0.10.0.md` contiene preguntas y material para cada perfil; no contiene dictámenes inventados.

## Reproducción

`README.md` documenta el flujo completo. La fuente narrativa canónica es `editorial/source/INFORME_v0.10.0.md`. Los scripts preparan datos, generan visuales y referencias, componen el PDF, validan el release y crean un ZIP determinista. La base v0.8.3 debe suministrarse externamente y superar el SHA-256 vinculante; no se duplica dentro del paquete.
