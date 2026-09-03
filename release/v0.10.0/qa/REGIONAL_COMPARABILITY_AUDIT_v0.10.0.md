# Auditoría de comparabilidad regional v0.10.0

## Resultado

**PASS_WITH_LIMITATION.** Las cuatro comparaciones publicadas usan una sola frontera armonizada para Argentina, Brasil, Chile y Uruguay entre 2018 y 2025. Los cierres nacionales se conservan como control y nunca reemplazan parcialmente una barra o denominador.

| Control | Evidencia | Estado |
|---|---|---|
| ventana común | ocho observaciones por país, 2018–2025 | PASS |
| generación total | un denominador armonizado por país-año | PASS |
| gran hidráulica | categoría separada de renovables legales | PASS |
| eólica + solar | suma sólo en el índice de velocidad | PASS |
| ceros nucleares | Chile y Uruguay tratados como cero estructural | PASS |
| cambio | puntos porcentuales, no variación porcentual relativa | PASS |
| índice | 2018 = 100 y nivel de base visible | PASS |
| escala | MWh por habitante con población WDI 2025 | PASS |
| emisiones comparadas | excluidas por fronteras incompatibles | NOT_APPLICABLE |
| lectura | lecciones por fase y límite de transferencia; sin ranking | PASS |

## Conciliación y límite

La tabla `regional/REGIONAL_SOURCE_RECONCILIATION_v0.10.0.csv` documenta diferencias con CAMMESA, EPE, Coordinador Eléctrico Nacional y MIEM. Pueden responder a importaciones, generación distribuida, autoconsumo, revisión o clasificación. La normalización por habitante no controla clima, estructura productiva, electrificación ni exportaciones. Ese límite es externo, está explicitado en el cuerpo y justifica el estado **PASS_WITH_LIMITATION**.
