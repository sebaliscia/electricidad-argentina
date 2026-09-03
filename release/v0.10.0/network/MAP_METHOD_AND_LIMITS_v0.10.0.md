# Método y límites del atlas v0.10.0

## Objetivo

El atlas ubica infraestructura publicada, centros de demanda, generación renovable, corredores seleccionados y cobertura de nodos AlmaMDI. No reconstruye operación eléctrica. La regla central es separar la topología 2026 del despacho 2025.

## Fuentes y vintage

| Capa | Autoridad | Vintage usado | Función |
|---|---|---|---|
| líneas de alta tensión | Secretaría de Energía | recurso actualizado 2026; CSV de diciembre de 2025 y SHP de junio de 2026 | geometría y nivel de tensión |
| estaciones transformadoras | Secretaría de Energía | recurso actualizado agosto de 2026 | control de nodos oficiales |
| límites provinciales | IGN | recuperado 18-08-2026 | frontera cartográfica |
| centrales de energía | IGN | recuperado 18-08-2026 | ubicación y tecnología, sin MW |
| relieve | IGN, Argenmap Topo | teselas recuperadas 18-08-2026 | contexto territorial |
| red y unifilares | CAMMESA | agosto de 2026 | control visual de topología |
| nodos | AlmaMDI | 30-01-2024 | cobertura nodal declarada |
| demanda y renovables | CAMMESA | operación 2025 | totales territoriales, no flujos |

## Procesamiento reproducible

1. Verificación SHA-256 de archivos recuperados.
2. Lectura de geometrías y normalización de tensión a valores numéricos.
3. Conversión a GeoJSON liviano; simplificación de límites sólo para representación.
4. Mosaico de teselas Argenmap a zoom 5 con límites geográficos registrados.
5. Unión territorial de demanda y renovables conservando Buenos Aires + CABA según la tabla de origen.
6. Cruce de nodos mediante nombre normalizado y distancia Haversine.
7. Exportación de PNG y SVG con la misma geometría, leyenda y acreditación.

## Resultado del crosswalk nodal

- Registros AlmaMDI: 411.
- Con coordenadas: 408.
- Sin coordenadas: 3 (`AYSA BERNAL`, `SUR`, `LAS BREÑAS`).
- Coincidencia espacial y nominal: 94.
- Coincidencia sólo espacial: 6.
- Sin coincidencia suficientemente confiable: 308.
- Sin coordenadas: 3.

Una coincidencia no prueba identidad eléctrica completa. Alias, niveles múltiples o instalaciones próximas requieren revisión humana y, de ser posible, identificadores oficiales comunes.

## Campos AlmaMDI autorizados

Se usan nombre, coordenadas, tensión y región. No se interpreta `POTENCIA MAXIMA`, `LIMITACION`, `CATEGORIA` ni codificación por color porque el adjunto no incluye un diccionario oficial. Los campos se preservan en el archivo original, pero no alimentan afirmaciones de saturación o prioridad.

## Lo que los mapas sí sostienen

- existencia y ubicación aproximada de activos publicados;
- niveles de tensión declarados;
- distribución territorial de tecnologías por clase;
- desajuste visual entre totales provinciales de demanda y generación renovable;
- presencia de corredores existentes con geometría oficial;
- cobertura y concentración regional de nodos AlmaMDI.

## Lo que los mapas no sostienen

- dirección o magnitud de flujo;
- congestión, capacidad remanente, estabilidad o pérdidas;
- suficiencia frente a contingencias;
- fecha de energización no documentada;
- avance físico de una prioridad administrativa;
- trazado nuevo cuando no existe geometría oficial reconciliada;
- saturación o severidad inferida de colores o campos sin diccionario.

## Control espacial

Se validaron rango de coordenadas, orientación, recuentos, límites, geometría vacía, niveles de tensión, correspondencia visual con los siete PDF CAMMESA y presencia del relieve. Los resultados detallados están en `qa/MAP_SPATIAL_AND_CLAIM_AUDIT_v0.10.0.md`.
