# Metodología técnica — v0.8.3

**Proyecto:** *Panorama de la electricidad en Argentina 2025*  
**Estado:** corrección quirúrgica sobre el baseline canónico v0.8.2; candidato a congelamiento científico para revisión externa de aceptación.

## 1. Principios

La metodología sigue cuatro reglas. Primero, cada magnitud conserva universo, período, unidad y denominador. Segundo, una identidad contable no se presenta como causalidad. Tercero, los estados administrativos de proyectos y obras se conservan en vez de reducirse a una variable binaria. Cuarto, una falta de datos se registra como falta y no como cero.

El relato principal abarca 2012–2025. La comparación estructural usa 2018 y 2025. Los modelos y cálculos horarios cubren 2023–2025. La capacidad territorial se fecha a junio de 2026 y sólo se trata como stock. Los datos 2005–2011 permanecen en archivos de control, pero no extienden la narrativa.

## 2. Integridad y congelamiento

El ZIP canónico de entrada fue `argentina_electricity_transition_v0.8.2.zip`, con SHA-256 `aad2e9d001d8b7d46c05d06fe72209f4fd6f5e776841b1e6363c4a4d7c6017f7`. Antes de editar se comprobaron: integridad ZIP sin errores, 639/639 entradas de `MANIFEST.sha256`, 640 archivos totales incluido el manifiesto y 43 archivos bajo `data/raw/`.

El baseline verificado es v0.8.2 y el árbol nuevo es `argentina_electricity_transition_v0.8.3/`. La comparación de inmutabilidad es v0.8.2 → v0.8.3. Ningún script v083 escribe dentro de `data/raw/`; sus hashes se cotejan contra `qa/raw_file_hashes_baseline_v082.csv`. Los productos v0.8.2 sustituidos se preservan bajo `archive_v082_products/`, con marcador `SUPERSEDED_BY_V083.md` y manifiesto propio. Los scripts con sufijo v082 son reproductores históricos, no la secuencia vigente.

## 3. Fuentes y vintages

### 3.1 CAMMESA anual

`Estadisticas anuales 2005-2025.xlsx`, hoja `Evolución anual`, es el vintage canónico para balances 2012–2025, punta anual, mezcla y emisiones. Las filas se extraen por número y se verifica además el rótulo, evitando que un desplazamiento de hoja cambie silenciosamente una métrica.

### 3.2 Bases mensuales y horarias

Las bases del informe mensual tienen corte junio de 2026. Se usan sólo datos completos hasta diciembre de 2025 para flujos. Las principales son:

- `Balance Mensual.xlsx` para conciliación;
- `Oferta Total Horaria.xlsx` para generación por tecnología;
- `Demanda Horaria por Provincia.xlsx` y `...por Tipo.xlsx`;
- `Import-Export Horaria.xlsx` y `...Mensual.xlsx`;
- `Generación Local Mensual.xlsx`, `Hidro Binacional.xlsx` y `Cotas Diarias.xlsx`;
- `Combustibles Diarios.xlsx`, `Combustibles Mensual.xlsx` y `Factor de Emisión.xlsx`;
- `Potencia Instalada.xlsx`, tratada como stock con fecha;
- `Energía Renovables - Base de Datos 2026-06.xlsx` para central, programa y provincia.

Los vintages mensual, horario y anual pueden contener revisiones. Se reconcilian cuando comparten frontera y se documentan las diferencias; no se fuerza igualdad reemplazando una fuente.

### 3.3 Meteorología y geografía

NASA POWER provee temperatura, viento y radiación horaria de reanálisis/grilla para centroides provinciales 2023–2025. Los centroides y geometrías provienen de Georef. La temperatura nacional se pondera con la participación de la demanda acumulada 2023–2025 de cada categoría CAMMESA; esos pesos son fijos para aislar la corrección geográfica. Los instrumentos de viento/radiación se ponderan por capacidad renovable activa. Un centroide provincial no representa el micrositio de un parque.

La planilla horaria contiene 22 categorías y publica la etiqueta literal `BUENOS AIRES`, sin diccionario que permita equipararla a provincia, CABA o AMBA. El archivo meteorológico contiene además un punto CABA. La unión heredada asignaba todo el peso de la categoría al centroide provincial y dejaba CABA sin uso. Se conservan tres sensibilidades explícitas:

- `ba_province_centroid_proxy` (origen v0.8.0): centroide de la provincia de Buenos Aires como proxy de reproducción;
- `caba_point_proxy_extreme` (origen v0.8.1): punto CABA como proxy extremo, sin equivalencia territorial afirmada;
- `caba80_ba_interior20_proxy` (origen v0.8.1): combinación proxy 80/20 entre punto CABA e interior bonaerense.

Los pesos 80/20 son aproximados y no censales. Para cada observación horaria y cada punto se calculan los excesos térmicos $C_t=\max(T_t-22,0)$ y $H_t=\max(15-T_t,0)$, ambos en °C, antes de ponderar. No se acumulan por día: los nombres históricos CDD/HDD describían incorrectamente su semántica temporal. En la regresión horaria, el resultado es energía de un bloque de una hora y el coeficiente se interpreta como potencia media asociada por grado, GW/°C. Ningún escenario define la composición territorial de la categoría CAMMESA.

### 3.4 Fuentes externas

Normas y obras se verifican en Argentina.gob.ar, CAMMESA y Boletín Oficial. La hidrología pública se toma de siete boletines mensuales AIC de 2025. Brasil se compara con EPE/BEN 2026, Chile con el Coordinador y Uruguay con MIEM. La trayectoria regional 2018–2025 usa un extracto OWID/Ember versionado sólo como serie armonizada secundaria. Todas las entradas están en `sources/source_registry_v083.csv`, con uso exacto, resolución, cobertura, territorialidad, limitaciones y afirmaciones no respaldadas.

## 4. Contratos de universos

| Magnitud | Definición operativa | Incluye | Excluye/advertencia |
|---|---|---|---|
| Generación local | Producción de centrales en frontera CAMMESA | Térmica, gran hidro, nuclear, renovables legales | Importaciones; Tierra del Fuego |
| Oferta total | Generación local + importaciones | Energía disponible en balance | No es demanda local |
| Demanda local | Consumo local publicado | Categorías residencial, comercial y gran demanda | Exportaciones, bombeo y pérdidas |
| Demanda total | Demanda local + exportaciones + bombeo + pérdidas | Cierre del balance | No equivale a ventas finales |
| Renovables legales | Categoría Ley 26.190/27.191 CAMMESA | Eólica, solar, bioenergías, pequeños aprovechamientos | Gran hidráulica >50 MW |
| Renovables comparables | Renovables legales + gran hidráulica | Comparación internacional aproximada | Persisten diferencias de distribuida/autoproducción |
| No fósil | Renovables comparables + nuclear | Generación local sin térmica | No es una categoría de impacto ambiental homogénea |
| Capacidad | Potencia nominal en fecha | Equipos registrados | No equivale a disponible o firme |

## 5. Balance anual

La identidad principal es:

\[
G^{local}_y + I_y = D^{local}_y + X_y + B_y + L_y + \epsilon_y,
\]

donde \(G^{local}\) es generación local, \(I\) importaciones, \(D^{local}\) demanda local, \(X\) exportaciones, \(B\) bombeo, \(L\) pérdidas y \(\epsilon\) el residuo de redondeo/vintage.

Para 2025, el residuo absoluto es 0,110 GWh. La prueba de aceptación no exige cero binario: exige que el residuo sea materialmente insignificante respecto de la oferta y que su origen quede documentado.

El puente 2018–2025 suma cambios de térmica, gran hidráulica, nuclear, renovables legales e importaciones. Es una descomposición de extremos. No controla condiciones intermedias ni asigna causalidad.

## 6. Demanda, punta y factor de carga

El factor de carga anual reproduce la fórmula visible en la hoja `Evolución anual` del anuario CAMMESA:

\[
FC_y = \frac{(D^{local}_y + L_y)\,1000}{P^{max}_y \times h_y},
\]

donde `DEMANDA LOCAL` y `Pérdidas` se expresan en GWh, `POTENCIA MÁX` en MW y `h_y` es 8.760 o 8.784 horas calendario. Exportaciones y bombeo no integran el numerador. `load_factor_formula_parity_v083.csv` conserva valores, fórmula de celda y diferencia: los 21 años 2005–2025 reproducen exactamente la serie publicada dentro de 1×10⁻¹². La diferencia 2018–2025 se expresa en puntos porcentuales.

Se distinguen:

- `peak_mw`: máximo instantáneo anual del anuario CAMMESA;
- máximo horario local: mayor bloque de `TOTAL` de la demanda provincial, MWh durante una hora.

La base CAMMESA etiqueta `HORA=1` para el primer bloque del día. En el archivo analítico se representa como 00:00 al comienzo del intervalo: `datetime = FECHA + (HORA − 1) horas`. La suma de categorías provinciales coincide con `load` dentro de 3,64×10⁻¹² MWh.

La curva de duración ordena cada año por demanda descendente. Las tablas de horas extremas seleccionan los 10, 50 y 100 bloques mayores por año y promedian tecnologías. Los cocientes respecto de demanda no se presentan como participaciones cerradas porque oferta y demanda horaria incluyen pérdidas, exportaciones y residuo.

## 7. Carga neta y rampas

La carga neta se define como:

\[
NL_t = D_t - W_t - S_t,
\]

donde \(D\) es demanda local, \(W\) eólica y \(S\) solar. No se restan hidráulica, nuclear, bioenergías ni importaciones. El campo heredado `residual_requirements` es un residuo contable y no se usa como carga neta.

La rampa horaria firmada es:

\[
R^x_t = x_t - x_{t-1},
\]

sólo para horas consecutivas dentro del mismo año. Como $x_t$ se expresa como potencia media del bloque de una hora, $R_t$ se informa como cambio de potencia media por unidad de tiempo, GW/h. Se calculan por separado:

- P95/P99 de toda la distribución firmada;
- P95/P99 condicionados a $R_t>0$, rampas ascendentes;
- P95/P99 de $-R_t$ condicionados a $R_t<0$, magnitud de descensos;
- conteos positivos, negativos, ceros y faltantes; máximos y fecha final.

El 1 de marzo de 2023 se conserva en una tabla de eventos. Para `regular_operation_screened`, cada rampa se trata como transición y se excluye si su extremo inicial o final pertenece a ese día; así se eliminan entrada, transiciones internas y salida del evento. La muestra 2023 queda en 8.734 transiciones. Las otras fechas no se criban sin evidencia oficial. La prueba principal exige que el P99 firmado de carga neta 2025 sea 2,02557998 GW/h y que difiera del P99 ascendente 2,23318954 GW/h; esa desigualdad evita confundir métricas.

Las rampas observadas no equivalen a reserva requerida, capacidad flexible ni necesidad óptima de almacenamiento. Para esas magnitudes harían falta criterios de confiabilidad y resolución subhoraria.

## 8. Análisis territorial

Las categorías territoriales CAMMESA se conservan con sus etiquetas de fuente. `BUENOS AIRES` se reporta literalmente y con frontera no documentada: no se equipara a provincia, CABA, AMBA ni a una composición específica de agentes. Tierra del Fuego está ausente.

La generación renovable se agrega por ubicación de central. La capacidad provincial se calcula desde equipos y fecha de habilitación al corte junio 2026. No se calcula “autosuficiencia” con cocientes generación/demanda porque el despacho y los flujos son sistémicos.

La red se representa con nodos y aristas analíticos, sin escala ni coordenadas. Los corredores topológicos se separan de refuerzos planificados. El inventario registra activo, alcance, tensión cuando está publicada, estado verificable, fuente y límite. Los estados `prioritaria` o `preparación concesional` no se recodifican como `en construcción`. Topología, capacidad, flujo, congestión, generación forzada, recorte y estabilidad son variables distintas; ninguna se infiere de distancia, mapa o existencia de obra.

## 9. Programas y proyectos

La cronología institucional incluye Ley 26.190; GENREN/Resolución 712/2009; Resolución 108/2011; Ley 27.191, Decreto 531/2016 y FODER; Resolución 202/2016; RenovAr Rondas 1, 1.5, 2 y 3/MiniRen; MATER/Resolución 281/2017; y RenMDI/Resoluciones 36 y 609/2023. Para cada instrumento se separan convocatoria/elegibilidad, adjudicación, contrato, cierre financiero, construcción, habilitación, operación, rescisión y garantía cuando la fuente lo permite.

La base renovable publica una etiqueta administrativa por central. Se agrupa en:

- RenovAr;
- MATER y variantes;
- “Renovar 202” (etiqueta conservada);
- RenMDI;
- resto/legado;
- otra etiqueta, si aparece.

La contribución al crecimiento es:

\[
c_p = \frac{G_{p,2025}-G_{p,2018}}{\sum_j(G_{j,2025}-G_{j,2018})}.
\]

Es una atribución contable de generación observada a grupos, no un efecto causal. La cronología separa ley, convocatoria, adjudicación, contrato, construcción, habilitación y operación. Los montos se clasifican como garantía, PPA, inversión anunciada, referencia regulatoria, penalidad o ingreso ilustrativo.

## 10. Hidráulica

La gran hidráulica se extrae de la categoría CAMMESA >50 MW. Yacyretá usa la base binacional. La descomposición de su cambio argentino separa producción total y asignación mediante una descomposición exacta de dos factores; no explica causas hidrológicas.

Comahue se analiza con generación, potencia, disponibilidad y utilización. La disponibilidad es una capacidad declarada/agregada; la utilización relaciona generación con potencia y tiempo. Una mejora de disponibilidad junto con menor utilización debilita la indisponibilidad agregada como explicación única, pero no descarta eventos por unidad.

Las cotas se describen sin convertirlas a volumen. La generación mensual por central se explota para 2023–2025 y se reconcilia con el anuario; la brecha máxima es 0,149 GWh (0,0019 % en 2025), se conserva y no se crea una categoría residual. La fuente no contiene 2018–2022, por lo que el cambio 2018–2025 queda agregado. Se descomponen 2024–2025 por central, mes calendario y estación. No se calcula factor de capacidad por central porque el único denominador de potencia disponible es un stock posterior y no una serie anual homogénea.

Los boletines AIC de enero, abril, mayo, julio, agosto, octubre y diciembre se usan como evidencia de cada mes, no como explicación anual. La matriz clasifica hipótesis como `COMPATIBLE`, `DEBILITADA` o `NO_EVALUABLE`. El documento de solicitud enumera los datos necesarios para un balance:

\[
\Delta V = Afluencias - Turbinado - Vertido - Otras\ salidas - Evaporacion + Precipitacion.
\]

La ecuación sólo podrá aplicarse cuando unidades, puntos de medición y volúmenes de control estén armonizados.

## 11. Inventario de CO₂ y CEM

El notebook `04_thermal_generation_and_emissions.ipynb` lee la hoja `Evolución anual` y verifica rótulos exactos:

- filas 171–174: generación con gas natural, gas oil, fuel oil y carbón;
- filas 177–180: CEM por combustible;
- filas 183–186: emisiones de CO₂ por combustible;
- fila 187: emisiones totales de energía térmica;
- filas 66, 71, 72, 78–80: componentes de generación, importaciones y oferta.

Las emisiones del inventario son las publicadas por CAMMESA. Se suman por combustible y se concilian con el total; el máximo error es inferior a 10⁻⁹ Mt. El CEM tiene unidad kcal/kWh. La generación por combustible cierra con la térmica atribuida y su brecha con la térmica total es inferior al umbral documentado.

La tasa observada por combustible es:

\[
r_{i,y}=\frac{C_{i,y}\times 1000}{Q_{i,y}}\quad [tCO_2/MWh].
\]

Para LMDI se deriva un factor implícito \(f_{i,y}=r_{i,y}/u_{i,y}\), donde \(u\) es CEM. Esa transformación sirve a la identidad; no reemplaza los valores de CAMMESA.

La frontera es CO₂ directo de combustión. No incluye ciclo de vida, construcción, emisiones aguas arriba, otros gases ni importaciones.

## 12. Descomposición LMDI

Las emisiones se representan como:

\[
C = \sum_i f_i\,u_i\,m_i\,s\,A,
\]

donde \(A\) es generación local, \(s\) participación térmica atribuida, \(m_i\) mezcla de combustibles, \(u_i\) CEM y \(f_i\) factor implícito. El método IDA-LMDI aditivo usa medias logarítmicas y produce residuo numérico despreciable.

Se calculan una descomposición directa 2018→2025 y descomposiciones anuales encadenadas. Ambas cierran el mismo cambio neto, pero pueden repartirlo de forma distinta por la trayectoria intermedia. El manuscrito usa la directa para el puente principal.

LMDI es exacto respecto de la identidad especificada. No identifica el efecto de eólica, solar, RenovAr o MATER.

## 13. Modelos horarios y sensibilidad geográfica

La especificación asociativa principal tiene generación térmica horaria como resultado y eólica, solar, demanda, nuclear y otras renovables como regresores. Incluye efectos fijos mes-año y hora-día de semana; la incertidumbre usa covarianza HAC Bartlett con 24 rezagos.

Dos referencias cambian el estimando:

- `hydro_control` agrega gran hidráulica y puede controlar una variable que también responde a renovables;
- `realized_trade` agrega además importaciones netas y se aproxima a una identidad contable.

El diseño instrumental usa meteorología ponderada por capacidad para instrumentar eólica y solar. Las salidas heredadas, originalmente construidas con `linearmodels`, se cotejaron con una implementación matricial independiente de 2SLS/HAC. La especificación dinámica agrega estados rezagados 1 y 24 horas. Se reportan intervalos HAC de 168 horas para modelos horarios y 14 días para emisiones diarias.

Para cada escenario geográfico se reemplazan temperatura y excesos térmicos horarios de refrigeración/calefacción; viento, radiación, generación, demanda y demás controles permanecen iguales. Se reestiman la especificación horaria base y la dinámica, con efectos fijos fecha y hora-mes. Se comparan coeficientes, errores, intervalos, R² parcial y Wald HAC de primera etapa. La reproducción del escenario centroide debe coincidir con la estimación validada a menos de 10⁻⁹ en coeficientes.

La validez exige relevancia y exclusión. Los diagnósticos apoyan relevancia; la exclusión sigue siendo un supuesto. La estadística condicional Sanderson–Windmeijer fue auditada. La prueba Kleibergen–Paap con HAC temporal y la revisión econométrica externa permanecen pendientes. Ninguna cifra IV se promueve a hallazgo de apertura.

## 14. Comparación regional

Se construyen tres tablas que no se fusionan: (1) trayectoria armonizada secundaria OWID/Ember 2018–2025, (2) cambios 2018–2025 y 2024–2025, y (3) cierres oficiales nacionales. Los TWh hidráulicos, eólicos y solares son generación total por la participación publicada; otras renovables completan el nivel renovable publicado; nuclear completa el nivel de bajas emisiones; fósil completa la generación total. Todo componente físico se restringe a no negativo. Para Chile y Uruguay entre 2018 y 2025, `nuclear_electricity_twh` es un cero estructural exacto en las 16 filas. Cualquier cierre algebraico minúsculo —positivo o negativo— derivado de participaciones publicadas redondeadas se conserva por separado como `rounding_residual_twh`, que puede tener signo y no es una fuente física. No se alteran los porcentajes publicados. La demanda/oferta y los intercambios no se imputan cuando la serie armonizada no los ofrece.

Argentina tiene cobertura oficial 2018–2025; Brasil, cierre 2025; Chile y Uruguay, cierres 2024–2025. La matriz de cobertura hace visible lo faltante. No se fuerza una participación “homogénea” si las fuentes incluyen universos distintos. Para cada país se registra:

- autoridad y edición;
- magnitud: generación, oferta o energía entregada;
- tratamiento de importaciones;
- gran hidráulica;
- generación distribuida y autoproducción;
- carácter preliminar;
- limitación.

No se comparan intensidades de emisiones porque CAMMESA publica CO₂ térmico directo, Uruguay un factor del SIN y Ember CO₂ equivalente con otra metodología. Un ranking violaría la regla de frontera común.

## 15. Control de cifras y prosa

`unit_registry_v083.csv` define magnitud, símbolo, unidad y uso de cada variable crítica. `correction_trace_v083.csv` registra la reproducción previa de las seis correcciones; `numeric_consistency_v082_v083.csv` prueba la regresión numérica; `version_provenance_audit_v083.csv` clasifica cada token de release; `active_reference_integrity_v083.csv` verifica rutas; y `scientific_acceptance_checklist_v083.csv` evalúa los 24 criterios duros. La rutina `replicate_v083_alternative.py` es una réplica computacional alternativa: no constituye revisión científica externa.

La revisión editorial se limita a erratas evidentes, conjunciones inmediatamente repetidas y contradicciones semánticas comprendidas en el mandato. No reabre títulos, resumen, conclusión ni estilo general.

## 16. Reproducción

1. Crear el entorno indicado por `environment.lock`.
2. Verificar el SHA-256 del ZIP canónico v0.8.2, su prueba de compresión y las 639 entradas del manifiesto.
3. Desde una copia limpia del árbol v0.8.2 llamada `argentina_electricity_transition_v0.8.3/`, ejecutar `python scripts/build_v083_corrections.py --baseline-zip <ruta-al-zip-v0.8.2>`.
4. Ejecutar `python scripts/build_v083_documents.py`.
5. Ejecutar `python scripts/regenerate_f04_v083.py`.
6. Ejecutar `python scripts/replicate_v083_alternative.py`.
7. Inspeccionar visualmente las quince figuras, registrar la atestación con sus hashes y ejecutar `python scripts/validate_v083.py`.
8. Ejecutar `python scripts/generate_manifest_v083.py`.
9. Ejecutar `python scripts/package_v083_release.py --output-dir ..` y comprobar el ZIP resultante en modo lectura.

Los scripts no descargan datos, no modifican `data/raw/`, no dependen de rutas absolutas y fallan ante entradas ausentes o discrepantes. Los nombres v082 se conservan sólo para el baseline, la procedencia histórica y los reproductores no vigentes.

## 17. Alcance final

v0.8.3 es un candidato a congelamiento científico para revisión externa de aceptación y paso posterior a la etapa editorial. No es una publicación, un estudio de suficiencia, un modelo nodal, un balance hídrico completo ni una evaluación económica. Tampoco es el futuro TFI de prefactibilidad de infraestructura de centros de datos/IA en Patagonia: no modela cargas de 100/250/500 MW, no selecciona sitio ni recomienda conexión o inversión. Permanecen abiertos economía energética, diseño editorial final, imágenes editoriales, PDF, inglés, web y las revisiones econométrica, eléctrica, científica y editorial externas.
