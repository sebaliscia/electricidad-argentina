# Auditoría espacial y de afirmaciones cartográficas v0.10.0

## Resultado general

**PASS_WITH_LIMITATION.** Los cuatro mapas cumplen su función de inventario, comparación territorial, separación de evidencia de corredor y auditoría de cobertura nodal. El límite externo es la ausencia de un modelo público completo con parámetros, flujos y estados horarios.

## Integridad espacial

| Control | Evidencia | Estado |
|---|---|---|
| límites nacionales y provinciales | 24 polígonos oficiales IGN; rango y orientación verificados | PASS |
| relieve | mosaico Argenmap Topo visible en M01–M04 | PASS |
| líneas AT | 1.299 registros; 110 de 500 kV, 6 de 330 kV, 2 de 345 kV, 80 de 220 kV | PASS |
| estaciones | 323 registros oficiales con coordenadas | PASS |
| centrales IGN | 445 puntos con clase tecnológica | PASS_WITH_LIMITATION |
| nodos AlmaMDI | 408/411 con coordenadas | PASS_WITH_LIMITATION |
| geometrías vacías o fuera de Argentina | controladas antes de trazar | PASS |
| proyección | transformación consistente a Web Mercator para superposición | PASS |
| control visual | siete PDF CAMMESA inspeccionados y contrastados | PASS |

La capa de centrales IGN no contiene MW en el recurso usado; los símbolos no se escalan por potencia. Tres registros AlmaMDI carecen de coordenadas. Ninguno de esos límites se convierte en cero ni en ausencia física.

## Auditoría por mapa

### M01 — Infraestructura y generación

- Muestra: líneas 500/345/330/220 kV, centrales por tecnología, relieve y límites.
- Afirmación autorizada: activos y corredores publicados son territorialmente visibles.
- Prohibición comprobada: no hay flechas, MW, congestión, margen, estabilidad ni pérdidas.
- Vintage visible: red 2026; control CAMMESA agosto 2026.
- Estado: **PASS**.

### M02 — Demanda y renovables

- Muestra: dos coropletas con escalas independientes y unidades GWh.
- Frontera visible: Buenos Aires + CABA agregadas; Tierra del Fuego no separada.
- Afirmación autorizada: los totales territoriales de demanda y generación renovable no coinciden.
- Prohibición comprobada: no se afirma déficit provincial ni dirección de flujo.
- Estado: **PASS_WITH_LIMITATION** por la agregación territorial de origen.

### M03 — Corredores y refuerzos

- Muestra: geometría oficial existente y tres tarjetas de evidencia.
- Puerto Madryn–Choele Choel–Bahía Blanca: infraestructura visible; prioridad administrativa 2025; avance físico no verificado.
- Comahue–centro de carga: conexión visible; margen no disponible.
- Río Diamante–Charlone–O’Higgins: corredor citado; tramo nuevo no dibujado sin geometría reconciliada.
- Prohibición comprobada: no se inventan líneas, fechas, flechas ni capacidad.
- Estado: **PASS_WITH_LIMITATION**.

### M04 — AlmaMDI

- Muestra: 408 puntos coloreados por región declarada.
- Recuentos de leyenda reconciliados con la planilla.
- Campos sin diccionario excluidos de la simbología y de las afirmaciones.
- Crosswalk: 94 coincidencias espacial+nombre, 6 sólo espaciales, 308 sin coincidencia confiable y 3 sin coordenadas.
- Estado: **PASS_WITH_LIMITATION**.

## Claims prohibidos — búsqueda final

- “flujo demostrado”, “congestión observada”, “capacidad remanente”, “déficit provincial” y equivalentes: ausentes como afirmaciones.
- Flechas direccionales: cero.
- Trazados inventados: cero.
- Lectura de color AlmaMDI como severidad: cero.
- Confusión operación 2025 / topología 2026: cero.

## Próximo control externo

Un especialista en transmisión debe revisar topología, nomenclatura y suficiencia del pedido de datos. Ese examen no fue fingido ni sustituido por la auditoría editorial.
