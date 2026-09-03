# Auditoría de citas y referencias v0.10.0

## Resultado

**PASS_WITH_LIMITATION.** La bibliografía de publicación contiene 30 obras; 29 tienen URL oficial o DOI y la planilla AlmaMDI conserva su procedencia adjunta sin inventar una URL. El sistema institucional autor–año distingue las ocho obras CAMMESA de 2026 mediante sufijos `a`–`h`.

| Control | Resultado | Estado |
|---|---|---|
| referencias en bibliografía | 30 | PASS |
| URL oficial o DOI | 29 | PASS_WITH_LIMITATION |
| obra adjunta sin URL inventada | 1, AlmaMDI | PASS |
| autor/institución, título y año | completos en 30/30 | PASS |
| afirmación y límite registrados | completos en 30/30 | PASS |
| fecha de consulta web | 2026-08-18 | PASS |
| copias locales con huella disponible | 6 registradas | PASS |
| nombres de archivo usados como título en PDF | cero | PASS |
| estilo autor–año | coherente en cuerpo y anexos | PASS |
| bibliografía visible | títulos editoriales, enlaces activos y sin lista cruda de archivos | PASS |
| tokens `TODO`, `TBD` o claves internas en PDF | cero | PASS |

## Trazabilidad

`sources/publication_references_v0.10.0.bib` es la exportación bibliográfica UTF-8. `sources/PUBLICATION_SOURCE_REGISTER_v0.10.0.csv` vincula cada obra con afirmaciones, límite de uso, disponibilidad local y SHA-256 cuando corresponde. `sources/BIBLIOGRAPHY_v0.10.0.json` es la fuente estructurada que consume el compositor del PDF.

## Límite residual

La presencia de una URL y su consulta no constituyen revisión institucional de la interpretación. Las fuentes empresariales e institucionales usadas para capacidades prueban existencia, no escala industrial ni integración nacional completa; esa restricción aparece también en la matriz estratégica y el informe.
