# Auditoría de comparabilidad regional v0.10.0

## Frontera común

La trayectoria 2018–2025 usa la adaptación OWID de Ember Yearly Electricity Data 2026 para Argentina, Brasil, Chile y Uruguay. Esta serie es la única que entra en comparaciones de participación, cambio e índice de velocidad. Los cierres nacionales se usan como conciliación, no como reemplazo parcial de una barra.

## Controles

| Control | Resultado | Estado |
|---|---|---|
| años comunes 2018–2025 | ocho observaciones por país | PASS |
| generación total | denominador armonizado dentro de cada país-año | PASS |
| gran hidráulica | categoría separada | PASS |
| eólica + solar | suma sólo para el índice de velocidad | PASS |
| nuclear en Chile y Uruguay | cero estructural, no faltante | PASS |
| cambio 2018–2025 | puntos porcentuales, no porcentaje relativo | PASS |
| índice | 2018 = 100 con base absoluta visible | PASS |
| población | WDI 2025, misma actualización para cuatro países | PASS |
| emisiones | no se construye ranking con fronteras incompatibles | NOT_APPLICABLE |
| lectura | lecciones por fase, sin ranking normativo | PASS |

## Conciliación y límites

Los valores armonizados no sustituyen CAMMESA, EPE, Coordinador Eléctrico Nacional ni MIEM. Diferencias residuales pueden deberse a importaciones, generación distribuida, autoconsumo, revisión o clasificación. La vista per cápita controla tamaño poblacional, pero no clima, estructura productiva, electrificación ni exportaciones. Estado general: **PASS_WITH_LIMITATION** por las diferencias inevitables entre una base armonizada y los cierres nacionales.
