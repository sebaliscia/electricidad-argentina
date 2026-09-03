# Auditoría de balance y sensibilidad v0.10.0

## Resultado

**PASS_WITH_LIMITATION.** La puerta de factibilidad autorizó sólo una sensibilidad mecánica sobre perfiles observados. Los cuatro casos cierran algebraicamente y coinciden entre tabla fuente, F28, cuerpo y anexo.

| Control | Resultado | Estado |
|---|---|---|
| perfil base | demanda, eólica y solar 2025 reconciliadas | PASS |
| carga neta | demanda − eólica − solar en cada hora | PASS |
| factores | 1,05 para demanda; 1,25 para eólica y solar | PASS |
| continuidad | rampas sólo entre horas consecutivas válidas | PASS |
| casos | observado, demanda, renovable y combinado | PASS |
| paridad punta | 24,2715; 25,6177; 23,8740; 25,1477 GW | PASS |
| paridad P99 | 2,02558; 2,09509; 2,18385; 2,24579 GW/h | PASS |
| energía no cubierta | no calculada sin balance de capacidad firme | NOT_APPLICABLE |
| despacho y red | no probados | NOT_APPLICABLE |
| comunicación | “sensibilidad, no pronóstico” visible | PASS |

La sensibilidad renovable baja la punta residual y eleva la rampa extrema con el perfil observado. Ese contraste es apto para advertir contra decisiones de una sola métrica, pero no identifica una solución tecnológica ni demuestra confiabilidad. La limitación es constitutiva y permanece visible.
