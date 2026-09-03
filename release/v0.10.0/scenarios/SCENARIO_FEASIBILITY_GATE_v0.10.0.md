# Puerta de factibilidad de pruebas de esfuerzo v0.10.0

## Pregunta

¿Existe evidencia suficiente para una prueba transparente que explore punta de carga neta y rampas sin fingir un modelo de expansión, despacho o red?

## Criterios previos

| Criterio | Evidencia | Estado |
|---|---|---|
| serie horaria 2025 reconciliada | demanda, eólica y solar en una frontera común | PASS |
| definición algebraica | carga neta = demanda − eólica − solar | PASS |
| supuestos observables | factores 1,05 y 1,25 declarados | PASS |
| métrica reproducible | máximo anual y P99 de rampas firmadas | PASS |
| factibilidad de despacho | no disponible | NOT_APPLICABLE |
| red y contingencias | no disponibles | NOT_APPLICABLE |
| almacenamiento y vertimiento | no modelados | NOT_APPLICABLE |
| conducta y perfil futuro | no modelados | NOT_APPLICABLE |

## Decisión de puerta

**GO — SENSIBILIDAD ACOTADA.** Se autorizan cuatro transformaciones mecánicas del perfil observado: observado, demanda +5 %, eólica y solar +25 %, y combinado. No se autorizan escenarios de capacidad, cronogramas, despacho óptimo, flujos de red ni promesas de confiabilidad.

## Resultados

| Caso | Punta neta | Rampa P99 |
|---|---:|---:|
| observado | 24,272 GW | 2,026 GW/h |
| demanda +5 % | 25,618 GW | 2,095 GW/h |
| eólica + solar +25 % | 23,874 GW | 2,184 GW/h |
| combinado | 25,148 GW | 2,246 GW/h |

## Comunicación obligatoria

Los resultados son sensibilidad, no pronóstico. El aumento renovable conserva el perfil temporal observado: puede bajar la punta residual y elevar la rampa extrema. El ejercicio no prueba factibilidad ni identifica una solución tecnológica. Estado general: **PASS_WITH_LIMITATION**.
