# Electricidad argentina: cambio, límites y decisiones

## 1. Qué cambió en el sistema eléctrico argentino

La electricidad argentina de 2025 no es la de 2005, ni la de 2012, ni la de 2018. El primer corte muestra un sistema que todavía crecía con una presencia térmica muy dominante. El segundo permite ver la etapa previa a la expansión renovable de mayor escala. El tercero marca un punto de comparación útil: ya existía el marco que impulsó esa expansión, pero buena parte de la generación posterior todavía no estaba en servicio. El cuarto muestra el resultado acumulado y, al mismo tiempo, los límites que quedaron a la vista. Esta secuencia evita que una fotografía de 2025 sea confundida con la historia que la produjo.

{{FIG:F01}}

La figura se lee de izquierda a derecha y cada columna conserva la frontera del balance anual de CAMMESA. El patrón principal es una diversificación gradual: las renovables del régimen legal pasan de una presencia marginal a un bloque relevante, mientras la gran hidráulica pierde peso y la generación térmica sigue siendo decisiva. El cambio importa porque reduce la dependencia horaria de una sola familia tecnológica, pero no elimina la necesidad de potencia controlable, red y coordinación. El límite de la comparación es temporal y contable: cuatro cortes no describen la secuencia dentro de cada año ni prueban qué medida causó cada movimiento (CAMMESA, 2026a).

Entre 2018 y 2025, la oferta total aumentó 9,271 TWh. Ese saldo pequeño esconde movimientos grandes y de signo opuesto. Las renovables del régimen legal sumaron 23,313 TWh y la generación nuclear 4,308 TWh; las importaciones agregaron 3,960 TWh. En sentido contrario, la generación térmica cayó 12,502 TWh y la gran hidráulica, 9,807 TWh. Hablar sólo del aumento neto borraría la transformación interna del abastecimiento.

{{TABLE:T01}}

{{FIG:F02}}

El puente comienza en la oferta de 2018, suma o resta cada componente y termina en 2025. Las barras no son estimaciones: forman una identidad contable. La lectura muestra que la expansión renovable fue mayor que el crecimiento total porque compensó simultáneamente menos generación térmica y menos gran hidráulica. Esa diferencia es estratégicamente relevante: el sistema incorporó energía baja en carbono, pero lo hizo en años en los que perdió parte de una fuente flexible y mantuvo una necesidad térmica sustancial. El puente no identifica causalidad, sustitución física hora por hora ni restricciones de transporte (CAMMESA, 2026a).

La demanda local anual llegó a 141,252 TWh en 2025. Frente a 2018 creció 6,2 %, mientras el máximo instantáneo aumentó 15,0 % hasta 30,257 GW. El factor de carga se redujo 4,425 puntos porcentuales. En lenguaje común, el sistema entregó algo más de energía a lo largo del año, pero tuvo que estar preparado para una punta que creció bastante más rápido. Esa divergencia desplaza el problema desde “cuánta energía anual” hacia “qué recursos están disponibles en las horas difíciles”.

Las renovables comprendidas por las leyes 26.190 y 27.191 aportaron 26,66 TWh, equivalentes a 18,7 % de la generación local. Si se agrega la gran hidráulica, el conjunto hidráulico y renovable representó 39,8 %. Con la generación nuclear, las fuentes no fósiles alcanzaron 47,3 %. Las tres cifras responden preguntas distintas. La primera sigue una definición legal; la segunda reúne recursos renovables en sentido físico; la tercera describe el conjunto no fósil. No deben intercambiarse.

La reducción de emisiones directas de la generación térmica fue otro cambio real: de 40,818 Mt de CO₂ en 2018 a 32,226 Mt en 2025. Sin embargo, una matriz anual más limpia no equivale a un sistema resuelto. En las cien horas de mayor demanda de 2023–2025, eólica y solar aportaron en promedio 11,55 % y la generación térmica, 58,53 %. La transición observada es, por eso, doble: cambia la energía anual y cambia la forma de cubrir potencia y flexibilidad.

> Clave de lectura. El hallazgo central no es que una tecnología haya reemplazado por completo a otra. Es que el sistema absorbió un bloque renovable grande mientras administraba menor generación hidráulica, una punta más exigente y una red cuya información pública no permite reconstruir todos los flujos.

Esta primera síntesis ordena el resto del informe. Los capítulos siguientes fijan las fronteras; separan energía, potencia y capacidad; examinan demanda, agua, térmica y emisiones; llevan la lectura al territorio; comparan la trayectoria regional; y convierten los hallazgos en preguntas de decisión. La conclusión no ofrece una receta única. Propone una secuencia de prioridades compatibles con lo que la evidencia permite sostener.

## 2. Alcance, fuentes y fronteras

El Mercado Eléctrico Mayorista es un arreglo institucional: coordina generadores, transportistas, distribuidores y grandes usuarios bajo reglas de despacho, medición y liquidación. El Sistema Argentino de Interconexión es la infraestructura física que vincula la mayor parte del país. CAMMESA administra el mercado y coordina la operación. En la conversación cotidiana, “sistema” suele abarcar las tres dimensiones. En este informe se las distingue porque una cifra de mercado no describe por sí sola una condición de red.

La generación local es la electricidad producida por centrales dentro de la frontera anual de CAMMESA. La oferta total agrega importaciones. La demanda local es el consumo publicado para las categorías territoriales de esa fuente. La demanda total del balance suma además exportaciones, bombeo y pérdidas. Tierra del Fuego permanece fuera del MEM y la generación distribuida no aparece con la misma frontera que en varias estadísticas internacionales. Estas diferencias no son notas al pie: determinan qué puede compararse.

{{TABLE:T02}}

La fuente científica canónica es el paquete v0.8.3 verificado por su huella SHA-256. De allí se heredan balances, transformaciones, estimaciones y controles ya auditados. La versión actual no recalcula una historia alternativa. Agrega una capa separada: cartografía oficial con vintage 2026, normalización regional, una matriz preliminar de capacidades nacionales y pruebas de sensibilidad acotadas. Cada extensión conserva su propia procedencia y no modifica los resultados heredados.

La jerarquía usada es explícita. Para el balance y la operación prevalece CAMMESA. Para líneas, estaciones y cartografía base se utilizan la Secretaría de Energía y el Instituto Geográfico Nacional. Los PDF de CAMMESA sirven como control visual de topología. La planilla AlmaMDI amplía la cobertura nodal, pero sus campos no documentados no se interpretan. Para la comparación regional se usa una serie armonizada común, controlada contra cierres nacionales. Para capacidades tecnológicas se consultan fuentes institucionales y técnicas primarias.

El año de operación principal es 2025. Las bases horarias cubren 2023–2025. La red y el inventario espacial recuperados tienen vintage 2026. Un mapa 2026 no debe ser leído como una explicación de un despacho 2025. Puede mostrar dónde existen activos o corredores publicados; no demuestra por sí solo qué flujo circuló, qué margen quedó disponible, si hubo congestión o qué refuerzo estaba energizado en una hora específica.

También se separan energía, potencia y capacidad. La energía expresa una cantidad acumulada durante un período y se informa aquí en GWh o TWh. La potencia es una tasa instantánea o media de un bloque horario y se expresa en MW o GW. La capacidad es una característica nominal o disponible de equipos. Una central puede tener mucha capacidad y producir poca energía por agua, combustible, mantenimiento, despacho o red. Una tecnología puede entregar mucha energía anual y aportar poco durante una punta particular.

La punta tiene dos mediciones válidas que no son equivalentes. CAMMESA informa un máximo instantáneo de 30,257 GW para 2025. La base horaria registra 28,094 GW como potencia media en el bloque de máxima demanda local. La diferencia no es un error: el primer dato capta un instante y el segundo resume una hora con otra resolución. El informe preserva ambos y evita mezclarlos.

Las afirmaciones se clasifican en tres planos. Una identidad contable responde cuánto cambió cada componente. Una asociación estadística describe cómo dos variables se movieron juntas después de aplicar una especificación. Una inferencia causal exige supuestos adicionales y controles explícitos. El puente de oferta y la descomposición LMDI pertenecen al primer plano. Las regresiones horarias, aun cuando usan variación meteorológica, se comunican como evidencia condicional y no como efecto universal de un parque o programa.

Las emisiones abarcan CO₂ directo de combustión de la generación térmica según el inventario publicado por CAMMESA. No incluyen ciclo de vida, metano aguas arriba, construcción, uso del suelo ni emisiones territoriales de otros sectores. La gran hidráulica se mantiene separada de las renovables legales para preservar la frontera de la fuente argentina. En la comparación regional, en cambio, se adopta una clasificación armonizada; por eso sus porcentajes no reemplazan el balance nacional.

El análisis económico-financiero ampliado no se desarrolla por decisión del autor.

## 3. Demanda, punta y flexibilidad

La energía anual suele dominar la conversación porque permite comparar años con una cifra. La operación se decide en una secuencia mucho más exigente: cada hora debe cerrar y algunos minutos concentran más estrés que meses enteros. Entre 2018 y 2025, la demanda anual creció menos que la punta. El dato no implica que el sistema sea necesariamente menos eficiente; indica que la relación entre carga media y máximo se volvió menos pareja.

{{FIG:F03}}

La figura combina tres escalas: energía anual, máximo instantáneo y factor de carga. No se comparan sus alturas como si tuvieran la misma unidad; se sigue la dirección de cada serie. La demanda crece de forma moderada, la punta avanza más y el factor de carga baja. El significado operativo es que atender el máximo requiere recursos que pueden utilizarse durante pocas horas. La relevancia estratégica está en coordinar demanda, generación, transformación y transporte, no sólo en sumar energía anual. El límite es que el máximo instantáneo no revela cuánto duró el evento ni qué contingencias coincidieron (CAMMESA, 2026a).

La composición de la demanda ayuda a entender de dónde proviene el total. El bloque publicado como `BUENOS AIRES` concentró 49,0 % de la demanda local de 2025; Santa Fe aportó 9,0 % y Córdoba, 7,7 %. El rótulo se conserva literalmente porque la fuente no documenta una equivalencia simple con CABA, AMBA o provincia. El dato muestra concentración estadística, no déficit provincial ni dirección de flujos.

{{FIG:F04}}

Las áreas apiladas muestran cómo las categorías publicadas contribuyen a la demanda local. El patrón dominante es la persistencia de `BUENOS AIRES` como mayor bloque, con un segundo nivel distribuido entre Santa Fe, Córdoba y otras jurisdicciones. Eso importa porque la punta y la infraestructura de transformación se enfrentan a una geografía concentrada. La figura no separa consumo residencial, industrial o comercial y tampoco permite asignar toda la categoría dominante a un límite administrativo específico. Su utilidad es describir dónde se registra la demanda, no explicar por qué crece (CAMMESA, 2026b).

{{FIG:F05}}

La curva ordena todas las horas desde la demanda más alta a la más baja y elimina el calendario. El extremo izquierdo muestra pocas horas excepcionales; la parte central, la carga habitual; el extremo derecho, los mínimos. La distancia entre las curvas anuales permite ver si cambia la forma completa o sólo la punta. La implicancia es práctica: una solución adecuada para veinte horas no necesariamente es la mejor para miles. El límite es deliberado: al perder el orden temporal, la figura no dice si dos horas altas fueron consecutivas, en qué estación ocurrieron ni qué recurso estaba disponible (CAMMESA, 2026b).

Las cien horas de mayor demanda forman una prueba descriptiva simple. En ese conjunto, la generación térmica promedió 58,53 % y la suma eólica–solar, 11,55 %. La cifra no descalifica el aporte anual renovable; muestra que la coincidencia temporal importa. Hidráulica, nuclear, otras renovables e intercambios completaron la cobertura con composiciones variables.

{{FIG:F06}}

Las barras representan el despacho medio, no la capacidad instalada, durante las cien horas de mayor demanda. La lectura correcta compara participaciones dentro de ese subconjunto. El patrón muestra un sostén térmico mayoritario y un aporte eólico–solar menor que su contribución anual combinada. La relevancia estratégica es la necesidad de tratar energía y potencia como problemas relacionados pero distintos. El límite es que un promedio de cien horas oculta dispersión, secuencia y disponibilidad: no determina capacidad firme ni identifica la tecnología marginal en cada hora (CAMMESA, 2026c).

La flexibilidad puede observarse mediante rampas, es decir, el cambio entre una hora y la siguiente. Para 2023–2025, el percentil 99 de la distribución firmada de la demanda fue 1,657 GW/h y el de los ascensos, 1,817 GW/h. En carga neta —demanda menos eólica y solar— los valores fueron 2,026 y 2,233 GW/h. Que la carga neta tenga rampas superiores es compatible con una operación que debe absorber simultáneamente cambios de consumo y de producción variable.

{{FIG:F07}}

La figura separa cambios firmados, ascensos y magnitud de descensos. No representa una reserva requerida ni una norma de seguridad; resume una distribución histórica. El patrón es que los extremos de carga neta superan a los de demanda sola, sobre todo en los ascensos. El significado es que la flexibilidad relevante no se reduce al récord anual: incluye velocidad de respuesta. Para decisiones, esto obliga a medir rampas, pronósticos y disponibilidad conjunta. El límite es que un percentil no modela contingencias, restricciones de red, tiempos de arranque ni reservas efectivamente contratadas (CAMMESA, 2026c).

La meteorología agrega otra dimensión. El máximo de verano de 2025 ocurrió el 10 de febrero a las 14:47, con 30,257 GW; el máximo de invierno fue 28,119 GW el 1 de julio a las 20:36. El calor y el frío pueden elevar la demanda por refrigeración y calefacción eléctrica. Para evitar que una sola coordenada represente toda la categoría `BUENOS AIRES`, la base científica canónica probó tres geografías: centroide bonaerense, CABA como extremo y una mezcla 80/20.

{{FIG:F10}}

Cada punto muestra cómo cambia una asociación estimada cuando se modifica el proxy territorial de temperatura. La lectura no busca elegir el punto “verdadero”, sino medir sensibilidad. El patrón es que la relación entre demanda y exceso térmico permanece positiva, aunque su magnitud se mueve con la geografía. El resultado es útil porque hace visible una incertidumbre normalmente escondida. Su límite es decisivo: el exceso térmico se mide por hora en °C sobre una grilla de reanálisis, no como grados-día ni como estación observada; la asociación no prueba causalidad meteorológica completa (NASA POWER, 2026; CAMMESA, 2026b).

La hora de mayor demanda local tuvo 28,094 GW de potencia media. En esa misma hora, la carga neta fue 23,676 GW. El máximo anual de carga neta ocurrió en otro momento y alcanzó 24,272 GW. Por lo tanto, el instante que maximiza consumo no necesariamente maximiza la exigencia residual. La planificación operativa necesita mirar ambas series y sus coincidencias con hidráulica, térmica, nuclear, intercambios y estado de red.

La respuesta no se limita a sumar generación. Gestión de demanda, eficiencia en equipos de uso final, pronóstico meteorológico, automatización, coordinación de mantenimiento y señales operativas pueden reducir o desplazar la punta. Este informe no cuantifica el potencial de cada medida. Sí establece qué datos se necesitan: cargas con mayor resolución, disponibilidad por unidad, estado de red, reservas y programas de respuesta medidos con una frontera común.

## 4. La incorporación de las renovables

La expansión renovable fue el cambio cuantitativo más grande de la oferta entre 2018 y 2025. Su lectura exige separar cuatro conceptos: capacidad instalada, generación efectiva, etiqueta contractual y efecto causal. La capacidad indica el tamaño nominal de los equipos; la generación registra energía entregada; la etiqueta ubica esa energía en una categoría administrativa; el efecto causal preguntaría qué habría ocurrido sin la medida. Las bases disponibles resuelven bien las dos primeras preguntas, parcialmente la tercera y no identifican por sí solas la cuarta.

{{FIG:F08}}

La figura presenta capacidad y generación por tecnología en paneles separados. La lectura evita dividir visualmente una serie por la otra sin controlar meses de habilitación y disponibilidad. El patrón muestra la expansión eólica como mayor componente, seguida por solar, con biogás, biomasa y pequeños aprovechamientos en escalas menores. El significado es que el crecimiento fue tecnológicamente concentrado, aunque no monolítico. Para la estrategia, la energía observada confirma operación real. El límite es que el stock de capacidad de una base con corte 2026 no equivale a capacidad firme ni explica por sí solo la generación de 2025 (CAMMESA, 2026d).

El marco institucional se acumuló por capas. La Ley 26.190 creó el régimen de fomento; la Ley 27.191 amplió metas y obligaciones; el Decreto 531/2016 reglamentó esa etapa. RenovAr organizó convocatorias y contratos de abastecimiento con CAMMESA. El MATER abrió una vía de contratos entre privados bajo la Resolución 281/2017. Otras resoluciones reencauzaron proyectos anteriores o crearon nuevos instrumentos. Esta cronología permite hablar de rutas de incorporación, no de una causa única (Argentina, 2006, 2015, 2016; Secretaría de Energía, 2017).

{{FIG:F09}}

Las áreas muestran generación etiquetada por programa en la base renovable. RenovAr alcanzó 11,344 TWh en 2025 y MATER con sus variantes, 10,741 TWh; RenMDI registró 0,151 TWh. Entre 2018 y 2025, RenovAr y MATER explican cantidades similares del aumento etiquetado. La relevancia es institucional: dos canales diferentes coexistieron y llegaron a operación. El límite es que una etiqueta no mide adicionalidad, cumplimiento contractual individual ni efecto de una norma aislada; además, adjudicación, habilitación y generación son estados distintos (CAMMESA, 2026d).

La expansión renovable no puede evaluarse sólo con su participación anual. Las horas de alta producción pueden reducir generación térmica, pero el efecto depende de demanda, hidráulica, nuclear, intercambios, estado de unidades y red. Cuando la producción variable cae o cambia rápido, otros recursos deben ajustar. Este problema no es una anomalía de la renovable; es una propiedad de la coordinación horaria que se vuelve más visible a medida que aumenta su peso.

La geografía también forma parte del recurso. El viento patagónico y bonaerense, y la radiación del noroeste y Cuyo, no coinciden plenamente con los mayores centros de demanda. La capacidad de transportar, transformar y controlar electricidad condiciona cuánto del potencial físico se convierte en energía útil. Por eso el capítulo territorial no presenta la red como una ilustración secundaria, sino como una dimensión constitutiva de la transición.

La siguiente etapa debería medirse con un tablero más completo: energía anual por tecnología, producción durante punta y rampas, vertimiento cuando exista una serie pública consistente, indisponibilidad, precisión de pronóstico, capacidad de transporte, tiempos de conexión y desempeño por cohorte. Sin ese conjunto, es fácil confundir más capacidad con integración efectiva.

## 5. Agua y generación hidráulica

La gran hidráulica perdió 9,807 TWh entre 2018 y 2025. Esa caída es casi tan grande como la reducción térmica y altera la lectura del cambio de matriz. Una narración que sólo contrapone renovables nuevas y térmica antigua omite que el agua fue el contrapeso principal del período. La hidráulica aporta energía, potencia, regulación y, en algunos complejos, almacenamiento; pero su disponibilidad depende de hidrología, usos múltiples, acuerdos binacionales, equipos, despacho y red.

{{FIG:F11}}

Las líneas separan complejos o agrupaciones en lugar de presentar una sola suma nacional. El patrón es heterogéneo: Yacyretá y Comahue explican la mayor parte del descenso, mientras otros grupos no se mueven igual. El significado es que “menos hidráulica” no nombra una causa única. La relevancia estratégica está en identificar qué información corresponde a cada cuenca y activo. El límite es que la generación anual no contiene caudales afluentes, reservas, restricciones ambientales, compromisos de riego ni consignas horarias de despacho (CAMMESA, 2026e).

Yacyretá requiere además separar producción total y asignación argentina. El aporte registrado para Argentina cayó 5,971 TWh entre 2018 y 2025. La descomposición atribuye 3,005 TWh a menor producción total del complejo y 2,966 TWh al cambio de asignación entre países. No es correcto adjudicar toda la diferencia a “falta de agua” ni a una decisión doméstica.

{{FIG:F12}}

Las dos barras suman exactamente la variación del aporte argentino mediante una descomposición simétrica. Una representa el efecto de producir menos en el complejo y la otra, el efecto de recibir una fracción diferente. El patrón es casi equilibrado. La implicancia es que una central binacional exige distinguir el activo físico del reparto. El límite es que la identidad no explica por qué cambió producción o asignación; para eso se necesitan datos hidrológicos, operativos y binacionales con la misma resolución (CAMMESA, 2026e).

En Comahue, la generación bajó 2,904 TWh entre 2018 y 2025. Sin embargo, la disponibilidad agregada subió 1,564 puntos porcentuales y la utilización cayó 7,704 puntos. Entre 2024 y 2025, el descenso fue 3,537 TWh. La coexistencia de más disponibilidad y menos uso muestra por qué no se debe atribuir automáticamente la caída a fallas de equipos.

{{FIG:F13}}

La figura pone en paralelo potencia, disponibilidad, utilización y generación. No se comparan sus niveles, sino sus trayectorias. El patrón clave es la divergencia entre disponibilidad y utilización: los equipos pueden estar técnicamente disponibles y aun así producir menos. El significado es compatible con restricciones de agua, despacho, red u otros usos, pero no elige entre ellas. Para la decisión, la brecha señala el dato faltante. El límite es que los promedios anuales esconden embalses, caudales, cotas y restricciones por central y hora (CAMMESA, 2026e).

El agua debe incorporarse a la política de transición como variable, no como fondo constante. Un año húmedo puede desplazar combustibles y suavizar rampas; un año seco puede elevar el requerimiento térmico o de intercambios. La expansión eólica y solar puede reservar agua para otras horas cuando la operación y los embalses lo permiten. Esa complementariedad es plausible, pero no se cuantifica aquí porque faltan series integradas de afluencias, restricciones y valor operativo del almacenamiento.

La agenda concreta es vincular, por complejo, generación horaria, caudales, niveles, disponibilidad, restricciones ambientales, requerimientos de otros usos y estado de transporte. En centrales binacionales debe sumarse la regla de asignación. Sólo entonces será posible separar con más confianza hidrología, mantenimiento, operación y red. Hasta ese punto, el informe conserva explicaciones múltiples y evita una conclusión prematura.

## 6. Generación térmica, emisiones y respuesta horaria

La generación térmica sigue siendo el mayor bloque individual de la matriz y el sostén principal en muchas horas exigentes. Entre 2018 y 2025 produjo menos energía y emitió menos CO₂ directo. La reducción es importante, pero no permite asumir que toda generación renovable adicional desplazó térmica en una relación uno a uno. La hidráulica cayó, la demanda cambió, la nuclear creció y los intercambios variaron.

{{FIG:F14}}

La figura superpone la trayectoria de generación térmica con las emisiones directas publicadas por CAMMESA. Ambas descienden, aunque no de forma idéntica, porque cambian la eficiencia media y la mezcla de combustibles. El patrón confirma una reducción de 8,593 Mt de CO₂ entre extremos. La relevancia es doble: hubo una mejora observable y la térmica continuó siendo central para la operación. El límite de frontera es estricto: se mide CO₂ de combustión térmica, no ciclo de vida ni otros gases o sectores (CAMMESA, 2026a).

Para ordenar los factores se aplica una descomposición LMDI. El método convierte el cambio total en cinco componentes que suman exactamente la diferencia observada: actividad, participación térmica, consumo específico medio, mezcla de combustibles y factor implícito de emisión. Es una lupa contable, no un modelo de comportamiento (Ang, 2005).

{{FIG:F15}}

Cada barra indica cuánto aportó un componente al cambio de emisiones. La menor participación térmica explica −6,963 Mt; la mejora del consumo específico medio, −1,583 Mt; y la mezcla de combustibles, −1,467 Mt. El crecimiento de la actividad agrega 1,369 Mt y el factor implícito, 0,052 Mt. Las barras cierran los −8,593 Mt observados. La implicancia es que el cambio de matriz domina, acompañado por mejoras técnicas. El límite es causal: LMDI distribuye una identidad y no asigna efectos a programas, empresas o centrales (CAMMESA, 2026a; Ang, 2005).

El análisis horario pregunta algo distinto: cuando aumentan eólica o solar, ¿cómo se mueve la generación térmica manteniendo constantes otras variables observadas? Las especificaciones usan datos 2023–2025, controles de calendario y meteorología, y errores que admiten correlación temporal. Una extensión instrumental aprovecha variación de viento o irradiancia como fuente de movimiento. Los supuestos son fuertes y la geografía meteorológica es aproximada; por eso los resultados se presentan como asociaciones condicionadas.

{{FIG:F16}}

Los coeficientes se leen como cambios medios de generación térmica asociados con una unidad adicional de eólica o solar dentro de cada especificación. La estimación principal es −0,442 para eólica y −0,278 para solar; en la variante dinámica, −0,377 y −0,140. El signo negativo es estable, pero la magnitud no equivale a sustitución física universal. La relevancia es que la respuesta horaria resulta parcial: otros recursos y restricciones también ajustan. El límite incluye instrumentos imperfectos, error meteorológico, agregación nacional y ausencia de una red explícita (CAMMESA, 2026c; NASA POWER, 2026; Newey y West, 1987).

En lenguaje común, un coeficiente de −0,442 no dice que cada MWh eólico “evita” exactamente 0,442 MWh térmico en cualquier momento. Dice que, en la muestra y bajo la especificación, horas con más producción eólica asociada a la variación utilizada tuvieron en promedio menos generación térmica, luego de controles. Hidráulica, nuclear, intercambios, demanda y restricciones absorben el resto. La cautela no invalida el resultado; delimita su uso.

Las cien horas de mayor demanda completan la imagen. Allí la térmica conserva una participación elevada, aun cuando las renovables reducen energía fósil en muchas otras horas. La política operativa debe cuidar dos objetivos simultáneos: sostener confiabilidad y reducir emisiones. Eso requiere información por unidad, arranques, mínimos técnicos, combustibles, reservas y restricciones. El inventario anual no alcanza para diseñar esa coordinación.

## 7. Territorio, red y capacidades tecnológicas

La transición ocurre en un territorio largo, con recursos y demanda distribuidos de manera desigual. El atlas combina cuatro capas con funciones diferentes. La Secretaría de Energía aporta geometría de líneas y estaciones; el IGN, límites, relieve y un inventario locacional de centrales sin escala de potencia; CAMMESA, el control visual de topología. Esa topología corresponde a 2026 y no se usa para reconstruir el despacho de 2025.

{{TABLE:T06}}

{{FIG:M01}}

El mapa se lee como inventario espacial. Los trazos más gruesos ubican niveles de 500/345/330 kV y los más finos, 220 kV; los símbolos diferencian tecnologías, pero su tamaño no representa MW. El patrón muestra una red troncal que conecta recursos alejados con el corredor central y una generación distribuida de forma desigual. La relevancia es territorial: distancia y relieve forman parte del desafío de integración. El límite está en el título: activos visibles, no flujos. No hay flechas, congestión, capacidad remanente, pérdidas ni estado horario (Secretaría de Energía, 2026a; IGN, 2026a; CAMMESA, 2026f).

El contraste entre consumo y generación renovable hace visible otro problema. La categoría agregada Buenos Aires y CABA concentra alrededor de la mitad de la demanda local, mientras provincias patagónicas, bonaerenses, cuyanas y del noroeste reúnen una parte relevante de la generación eólica o solar. No toda energía cruza necesariamente una línea larga; el mapa compara totales territoriales y no balances nodales.

{{FIG:M02}}

Los dos paneles usan escalas de color independientes: azul para demanda y verde para generación renovable legal. Un tono igual entre paneles no representa el mismo número. El patrón es un desajuste espacial entre el mayor centro de consumo registrado y varios polos de generación. La implicancia es que red, transformación y ubicación de nueva demanda importan tanto como el recurso. El límite es que Buenos Aires y CABA se conservan agregadas según la tabla de origen, Tierra del Fuego no se separa y los colores no describen flujos ni déficit provincial (CAMMESA, 2026b, 2026d; IGN, 2026a).

Los corredores seleccionados permiten distinguir infraestructura existente, prioridades administrativas y geometría faltante. Puerto Madryn–Choele Choel–Bahía Blanca aparece como trazado oficial de 500 kV; su refuerzo tuvo prioridad administrativa en 2025, pero el avance físico no se verifica con los insumos usados. La conexión Comahue–corredor central se observa como infraestructura; el mapa no contiene capacidad remanente. Para Río Diamante–Charlone–O’Higgins se registra un corredor planificado, pero no se dibuja una línea nueva sin geometría oficial reconciliada.

{{FIG:M03}}

La línea continua corresponde a geometría oficial publicada. Las tarjetas laterales declaran qué se sabe y qué falta. El patrón es una estructura radial y longitudinal con corredores que vinculan zonas de recurso y centros de carga. La relevancia está en separar una necesidad plausible de una obra demostrada. El límite es intencional: el gráfico no inventa trazados, flechas, MW, congestión ni fechas de energización. Una prioridad administrativa no equivale a avance físico y un activo existente no prueba margen disponible (Secretaría de Energía, 2026a; CAMMESA, 2026f).

La planilla AlmaMDI contiene 411 registros. Hay 408 con coordenadas y tres sin ubicación: AYSA BERNAL, SUR y LAS BREÑAS. Los nodos se distribuyen por regiones operativas; GBA reúne 143, Litoral 56, NOA 50, NEA 42, Centro 39, Buenos Aires 28, Comahue 25, Cuyo 16 y Misiones 9. Se cartografían nombre, coordenadas, tensión y región. No se interpretan `POTENCIA MAXIMA`, `LIMITACION`, `CATEGORIA` ni colores porque el adjunto no contiene un diccionario autorizado.

{{FIG:M04}}

Los puntos se colorean por región declarada y no por severidad. La lectura muestra cobertura espacial alta, con concentración en GBA y ejes regionales. El valor estratégico es metodológico: la planilla puede servir para enlazar nodos y organizar pedidos de información. El límite es sustantivo: 94 registros lograron coincidencia espacial y nominal con estaciones oficiales, seis sólo espacial y 308 no tuvieron una coincidencia suficientemente confiable; tres carecen de coordenadas. No se deduce saturación ni prioridad desde campos no documentados (AlmaMDI, 2024; Secretaría de Energía, 2026b).

El crosswalk conserva esa incertidumbre. Una coincidencia espacial y nominal alta no prueba identidad eléctrica completa; puede haber alias, niveles de tensión múltiples o instalaciones próximas. Una coincidencia sólo espacial necesita revisión humana. Los no coincidentes no se descartan: permanecen como observaciones del insumo, con estado explícito. Este diseño permite mejorar el enlace cuando exista un diccionario nodal o identificadores comunes.

La red plantea una agenda de datos concreta: modelos eléctricos con identificadores estables; parámetros por tramo; capacidad térmica y límites dinámicos; estados de servicio; flujos horarios; transformadores y compensación; indisponibilidades; restricciones y vertimiento; proyectos con geometría y estado verificables. Sin esos datos, el atlas puede guiar preguntas y auditorías, pero no simular contingencias ni recomendar un orden técnico definitivo de ampliaciones.

La dimensión tecnológica nacional se apoya en evidencia de capacidades, no en porcentajes inventados. Existen antecedentes institucionales en ingeniería hidroeléctrica, líneas de alta tensión, transformadores, conductores, ensayos de energías renovables, control operativo, investigación en electrónica de potencia y almacenamiento, industria nuclear y ciberseguridad. La presencia de un actor o producto no demuestra escala suficiente, integración local completa ni disponibilidad inmediata. La matriz del capítulo 9 separa evidencia, brecha y dato necesario.

## 8. Argentina frente a Brasil, Chile y Uruguay

Comparar sistemas eléctricos exige una frontera común. Argentina usa en el cuerpo nacional el balance CAMMESA; Brasil, Chile y Uruguay publican cierres con clasificaciones propias. Para observar trayectorias se adopta aquí la serie armonizada de Ember, distribuida por Our World in Data, para 2018–2025. La población 2025 proviene del Banco Mundial. Los cierres oficiales se usan como control, no se mezclan en una misma razón cuando sus denominadores difieren (Ember, 2026; Banco Mundial, 2026).

Los ceros nucleares de Chile y Uruguay son estructurales en la clasificación, no datos faltantes. La gran hidráulica se presenta como categoría separada. Eólica y solar se agrupan sólo en el índice de velocidad; las otras renovables permanecen identificadas. La comparación no clasifica “ganadores” y “perdedores”: pregunta qué problema enfrenta cada sistema después de su trayectoria.

{{FIG:F17}}

Las barras separan importaciones y exportaciones, y la línea muestra el saldo. En 2025, las importaciones fueron 4,304 TWh. El cociente bruto sobre demanda local fue 3,41 % y el saldo neto importador, 2,69 %. El patrón es que el comercio es pequeño frente al año completo, pero puede ser relevante en el margen horario. La implicancia es preservar interconexiones y datos de disponibilidad sin tratar al intercambio como sustituto automático de recursos internos. El límite es que totales anuales no revelan precio, congestión, dirección horaria ni condición simultánea de los países vecinos (CAMMESA, 2026g).

{{FIG:F22}}

Cada barra suma la generación de 2025 bajo la misma clasificación armonizada. Brasil y Uruguay muestran bases hidráulicas muy altas; Chile, una combinación con fuerte eólica y solar y presencia fósil; Argentina, una estructura más térmica con hidráulica, nuclear y renovables crecientes. La relevancia está en reconocer puntos de partida distintos: la misma participación eólica–solar puede tener implicancias diferentes según agua, interconexión y demanda. El límite es que la armonización sacrifica detalle nacional y no debe reemplazar los balances oficiales (Ember, 2026).

{{FIG:F23}}

La figura muestra cambios en puntos porcentuales entre 2018 y 2025. Las renovables aumentaron 10,585 puntos en Argentina, 4,243 en Brasil, 20,507 en Chile y 0,286 en Uruguay. El patrón no implica que Uruguay haya estado inmóvil: partía de una estructura renovable elevada y su variación marginal responde a otra etapa. Chile exhibe la expansión más rápida; Argentina, un cambio intermedio y material. La lectura estratégica compara fases, no méritos. El límite es que un cambio de participación combina movimientos del numerador y del total generado (Ember, 2026).

{{FIG:F24}}

El índice fija la generación eólica y solar de 2018 en 100 para cada país. Se compara velocidad relativa, no TWh. Las pendientes muestran una aceleración marcada en Chile y Argentina, una expansión sostenida en Brasil y una trayectoria más estable en Uruguay desde una base ya alta. La relevancia es distinguir “crecer rápido” de “tener gran volumen”. El límite es el efecto base: un país con pocos TWh iniciales puede registrar un índice alto con una adición absoluta menor (Ember, 2026).

{{FIG:F25}}

Las barras dividen generación renovable y fósil de 2025 por población. La normalización reduce el sesgo de tamaño, pero no corrige estructura productiva, clima, exportaciones, electrificación ni intensidad de uso. El patrón muestra perfiles per cápita distintos de los rankings por volumen absoluto. La implicancia es usar varias vistas antes de extraer lecciones. El límite es que la población anual no sustituye demanda, producto, superficie ni consumo industrial como denominadores alternativos (Ember, 2026; Banco Mundial, 2026).

{{TABLE:T05}}

Brasil enseña el valor y la exposición de una gran base hidráulica: escala, almacenamiento y variabilidad hidrológica conviven. Chile muestra la transición desde expansión eólica–solar hacia integración, flexibilidad y red. Uruguay ilustra complementariedad entre viento, agua, biomasa e intercambio en un sistema pequeño. Argentina combina escala intermedia, nuclear, gas, hidráulica y recursos renovables distantes. Las lecciones son preguntas transferibles, no soluciones copiables.

La cooperación regional tiene valor operativo cuando existen interconexiones disponibles, reglas claras y situaciones no perfectamente correlacionadas. También tiene límites: olas de calor, sequías o indisponibilidades pueden coincidir. El comercio de 2025 no justifica depender de una única dirección. La prioridad analítica es publicar capacidad disponible, flujos y restricciones con resolución compatible entre países.

## 9. Del diagnóstico a las decisiones

Una implicancia estratégica válida necesita una cadena completa: hallazgo, evidencia, mecanismo, actor, horizonte, incertidumbre y dato faltante. Saltar del mapa a una obra o de una asociación a una promesa rompe esa cadena. La matriz de esta versión utiliza horizontes de 0–2, 3–5 y más de 5 años. No estima presupuestos ni beneficios monetarios; ordena problemas que pueden medirse.

{{FIG:F26}}

Las tarjetas agrupan implicancias por horizonte, no por importancia. En el corto plazo predominan medición, coordinación operativa y publicación de datos; en el medio, integración de red, flexibilidad y cadenas tecnológicas; en el largo, arquitectura territorial y capacidades sostenidas. El patrón indica que varias acciones habilitantes preceden a decisiones irreversibles. La relevancia es secuenciar: primero reducir incertidumbre y mejorar operación, luego escalar. El límite es que los horizontes son categorías de gestión, no cronogramas garantizados ni evaluación de proyectos.

La primera prioridad es un tablero común de energía, punta, rampas, disponibilidad y red. Corresponde a CAMMESA, Secretaría de Energía, transportistas y reguladores en el corto plazo. La evidencia de origen es la divergencia entre demanda anual y punta, y entre disponibilidad y utilización hidráulica. La incertidumbre principal es la falta de series nodales y de restricciones publicadas con identificadores comunes.

La segunda es integrar pronóstico, respuesta de demanda y flexibilidad operativa. Corresponde a operadores, distribuidores, grandes usuarios y organismos técnicos. Las rampas de carga neta y la baja coincidencia eólica–solar en horas de mayor demanda justifican medir el problema. No prueban qué tecnología específica debe resolverlo. Antes de decidir, se necesitan requisitos de reserva, desempeño de pronósticos, arranques, tiempos de respuesta y cargas flexibles verificadas.

La tercera es tratar la red como parte del recurso. Secretaría de Energía, CAMMESA, transportistas, provincias y reguladores necesitan una capa común de activos, estados, proyectos y restricciones. El atlas muestra desajuste territorial y corredores visibles; no demuestra congestión. El paso habilitante es publicar geometrías y parámetros conciliados, y someter prioridades a estudios eléctricos de flujo, contingencia y estabilidad.

La cuarta es recuperar la dimensión hídrica. Organismos de cuenca, operadores, CAMMESA y autoridades binacionales deben vincular agua, disponibilidad, asignación y despacho. Las caídas de Yacyretá y Comahue muestran que la hidráulica puede modificar la lectura de toda la matriz. El dato crítico es una serie integrada por complejo y hora; sin ella, no corresponde atribuir causas únicas.

La quinta es orientar capacidades nacionales hacia cuellos de botella demostrados. La matriz preliminar no asigna porcentajes de contenido local. Clasifica evidencia en diseño, fabricación, ensayo, integración, operación o investigación y señala brechas. El objetivo es convertir demanda técnica verificable en agendas de homologación, prototipos, formación y escalamiento.

{{FIG:F27}}

Las filas son familias tecnológicas y las columnas distinguen evidencia visible de brechas. La lectura no suma casilleros como un índice. El patrón muestra fortalezas documentadas en hidroelectricidad, líneas, conductores, transformadores, nuclear, control y capacidades científico-técnicas, junto con vacíos en escala, electrónica de potencia avanzada, almacenamiento, interoperabilidad y ciberseguridad sectorial. La relevancia es elegir pruebas y estándares concretos. El límite es que una fuente institucional prueba existencia, no volumen, competitividad, integración nacional completa ni disponibilidad futura (INTI, 2026; IMPSA, 2026; CNEA, 2026; CAMMESA, 2026h).

{{TABLE:T07}}

Las pruebas de esfuerzo superaron un control de factibilidad acotado porque se dispone de una serie horaria nacional 2025 reconciliada y supuestos transparentes. No son escenarios de expansión ni simulaciones de despacho. Aplican factores simples a demanda, eólica y solar para observar cómo cambian dos métricas: máximo de carga neta y percentil 99 de rampas firmadas.

{{FIG:F28}}

El caso observado tiene una punta de carga neta de 24,272 GW y una rampa P99 de 2,026 GW/h. Con demanda 5 % mayor, la punta sube a 25,618 GW y la rampa a 2,095. Con eólica y solar 25 % mayores y el mismo perfil, la punta baja a 23,874 GW, pero la rampa sube a 2,184. El caso combinado alcanza 25,148 GW y 2,246 GW/h. La lectura muestra una tensión: más producción variable puede reducir el máximo residual y aumentar cambios horarios. El límite es severo: no hay respuesta de precios, red, almacenamiento, vertimiento, nuevas formas de perfil ni despacho endógeno.

{{TABLE:T09}}

El resultado no es una predicción. Sirve para probar si una decisión robusta bajo una sola métrica sigue siendolo bajo otra. Una estrategia que mire sólo la punta podría celebrar el caso renovable; una que mire sólo rampas podría sobrerreaccionar. La conclusión razonable es medir ambas, incorporar recursos de respuesta y avanzar hacia modelos operativos cuando existan datos suficientes.

La sexta prioridad, por lo tanto, es un programa escalonado de evidencia: publicación y conciliación de datos; ensayos operativos; estudios eléctricos; homologación tecnológica; y evaluación posterior. Cada etapa debe tener una pregunta falsable. Si un dato nuevo contradice la hipótesis, la prioridad debe poder cambiar sin que el sistema quede atado a una narrativa.

## 10. Conclusión integrada

Entre 2018 y 2025, Argentina incorporó un bloque renovable de 23,313 TWh, redujo 12,502 TWh de generación térmica y registró 8,593 Mt menos de CO₂ directo térmico. Esos resultados son sustantivos y están sostenidos por el balance CAMMESA. Al mismo tiempo, la gran hidráulica cayó 9,807 TWh, la punta creció más que la demanda anual y la térmica conservó un papel mayoritario en las horas de demanda más alta. La transición ocurrió, pero no adoptó la forma de un reemplazo lineal.

La energía anual muestra dirección; la operación horaria muestra dificultad. Las renovables legales llegaron a 18,7 % de la generación local y el conjunto no fósil a 47,3 %. Sin embargo, el aporte eólico–solar medio en las cien horas de mayor demanda fue 11,55 %. Esta diferencia no enfrenta una cifra con la otra. Explica que un sistema puede mejorar su matriz anual y, a la vez, requerir soluciones específicas para punta, rampas y contingencias.

El agua es la pieza que impide una narración binaria. La caída de Yacyretá combina menor producción total y cambio de asignación. La de Comahue convive con mayor disponibilidad y menor utilización. Sin caudales, restricciones y despacho integrados, cualquier explicación única sería más fuerte que la evidencia. Recuperar esa capa es una condición para entender cuánto respaldo y flexibilidad puede ofrecer la hidráulica en cada año.

El territorio convierte el potencial en sistema. Los mapas oficiales muestran activos de alta tensión y una geografía desigual de demanda y generación. No muestran flujos ni congestión. Esa limitación no vuelve inútil al atlas: lo vuelve honesto. Permite ubicar preguntas, distinguir trazado existente de corredor planificado y definir qué parámetros faltan antes de sostener una prioridad de obra.

La comparación regional refuerza la misma idea. Chile avanzó con mayor velocidad relativa de renovables; Uruguay partió de una estructura ya muy renovable; Brasil conserva una base hidráulica de otra escala; Argentina combina recursos diversos y un gran centro de demanda. Ningún porcentaje aislado define una secuencia óptima. La lección común es que, después de incorporar energía renovable, la agenda se desplaza hacia integración, flexibilidad, agua, red y calidad de datos.

Las capacidades nacionales deben insertarse en esa agenda sin triunfalismo ni resignación. Hay evidencia de ingeniería, fabricación, ensayos, operación e investigación en varias familias críticas. También hay brechas de escala, homologación, interoperabilidad y conocimiento público. La tarea no es declarar autosuficiencia. Es formular requerimientos técnicos, medir capacidades contra ellos y sostener ciclos de aprendizaje con actores identificados.

Las pruebas de sensibilidad ilustran por qué la secuencia importa. Elevar eólica y solar con el perfil observado reduce la punta de carga neta, pero aumenta la rampa extrema. Un aumento simultáneo de demanda vuelve a elevar ambas exigencias. Sin una simulación de despacho y red, no se debe convertir ese ejercicio en pronóstico. Sí puede usarse para evitar políticas de una sola métrica.

De los hallazgos emerge una orientación coherente: medir la operación completa; integrar pronóstico y flexibilidad; recuperar información hídrica; publicar una red eléctrica utilizable para estudios; y alinear capacidades tecnológicas con cuellos de botella demostrados. Son prioridades compatibles entre sí y escalonables. Ninguna exige fingir certeza donde faltan datos.

La soberanía de decisión, en este contexto, no consiste en aislarse ni en elegir una tecnología por identidad. Consiste en conocer las fronteras de los datos, poder reproducir los cálculos, formular alternativas y conservar capacidad para corregir el rumbo. El sistema eléctrico es una infraestructura física y también una infraestructura de conocimiento. Fortalecer ambas es el paso que conecta el cambio observado con una transformación duradera.

## 11. Límites y agenda de datos

Este informe se encuentra en revisión del autor. No fue publicado, validado institucionalmente ni revisado por pares. Su reproducibilidad permite examinar datos y cálculos; no reemplaza la revisión externa especializada. Las prioridades propuestas deben someterse a especialistas en operación y transmisión, hidrología, métodos cuantitativos, planificación tecnológica y edición general.

La primera limitación es de vintage. El balance describe 2025 con bases consolidadas o actualizadas hasta 2026; la cartografía de red recuperada corresponde a 2026. Una revisión posterior puede cambiar registros. El paquete conserva fechas de acceso y huellas de los insumos para que una actualización sea distinguible de un error.

La segunda es de resolución. Los balances anuales son adecuados para trayectorias y descomposiciones, pero no para reservas, rampas por unidad o congestión. Las series horarias nacionales permiten asociaciones y sensibilidad agregada, no contingencias eléctricas. La punta instantánea y el máximo horario no deben fusionarse.

La tercera es territorial. `BUENOS AIRES` es una categoría de publicación cuya composición no se redefine. La comparación provincial agrega Buenos Aires y CABA en una de las tablas disponibles. Tierra del Fuego queda fuera del MEM. Los puntos de centrales del IGN no incluyen MW en el recurso usado. Los mapas, por lo tanto, muestran ubicación y clase, no tamaño operativo completo.

La cuarta es hídrica. Falta una serie integrada de caudales, niveles, restricciones, otros usos, disponibilidad, asignación y despacho. La quinta es de red: no se dispone en este paquete de un modelo eléctrico con parámetros, límites, estados y flujos horarios. La sexta es inferencial: los instrumentos meteorológicos y controles reducen algunos sesgos, pero no resuelven todos; las estimaciones horarias permanecen condicionadas a su especificación.

La séptima es regional. La serie armonizada favorece comparabilidad a costa de detalle. La población mejora una vista, pero no controla estructura económica, clima o electrificación. La octava es tecnológica: las fuentes primarias prueban actividades y productos, no capacidad anual, origen de cada componente ni desempeño comparativo. La novena corresponde a las pruebas de esfuerzo: perfiles fijos y factores simples no representan conducta, despacho o red.

{{TABLE:T11}}

La agenda se ordena por valor de información. Primero, identificadores comunes para unidades, nodos, líneas y proyectos. Segundo, series horarias de disponibilidad, restricciones, reservas y vertimiento. Tercero, una capa hídrica por complejo. Cuarto, datos de capacidad tecnológica con criterios verificables. Quinto, fronteras regionales documentadas y series de intercambio compatibles. Cada publicación debería incluir metadatos, unidad, zona horaria, regla de revisión y licencia.

Una actualización responsable no consiste sólo en agregar el año 2026. Debe preguntar si cambiaron definiciones, si una revisión altera los puentes 2018–2025 y si los proyectos administrativos se convirtieron en activos energizados. También debe revalidar las coincidencias AlmaMDI, mantener separadas las capas 2025/2026 y volver a ejecutar todos los controles de figuras, citas y texto.

La revisión externa sugerida es dirigida. El especialista en transmisión debe evaluar los límites del atlas y la suficiencia de los datos pedidos. El especialista hídrico debe examinar la descomposición y la agenda por cuenca. El especialista cuantitativo debe revisar instrumentos, errores y sensibilidad. El especialista en planificación tecnológica debe revisar la matriz de capacidades. El revisor editorial debe leer la secuencia completa y detectar saltos que un lector no especializado todavía deba inferir.

El cierre permanece deliberadamente abierto a corrección. La evidencia disponible alcanza para afirmar que la matriz cambió, que las emisiones térmicas directas bajaron y que la integración futura depende de potencia, flexibilidad, agua, red y capacidades. No alcanza para fijar una cartera técnica definitiva. Esa frontera es el principal resultado metodológico del trabajo.

# Anexos metodológicos

## A. Contratos de magnitud y reconciliación

Las magnitudes se publican con unidades visibles. Energía anual: GWh o TWh. Potencia instantánea u horaria: MW o GW. Rampas: GW/h. Emisiones directas: Mt de CO₂. Participaciones y disponibilidades: porcentaje o puntos porcentuales según corresponda. Temperatura y exceso térmico horario: °C. Una diferencia de participaciones se informa en puntos porcentuales, no como porcentaje relativo.

El balance anual usa identidades. Oferta total = generación local + importaciones. Demanda total del balance = demanda local + exportaciones + bombeo + pérdidas. El puente de 2018–2025 suma cambios por fuente e importaciones. Las diferencias residuales sólo se aceptan dentro de la precisión de publicación y se registran; no se fuerza una serie mensual u horaria para igualar otra edición.

La conciliación horaria compara la suma de bloques con el total anual cuando las fronteras son compatibles. No se sustituye el máximo instantáneo por el horario. Para la curva de duración, las horas se ordenan de mayor a menor y pierden fecha. Para rampas, se calcula la diferencia entre horas consecutivas dentro de una secuencia regular; los cortes y faltantes se tratan antes de resumir percentiles.

## B. Descomposición de Yacyretá y LMDI

El aporte argentino de una central binacional puede escribirse como producción total multiplicada por participación asignada. El cambio entre dos años se reparte de manera simétrica entre ambos factores. La suma de los efectos reproduce exactamente la variación total, pero no explica las causas físicas o institucionales que movieron cada factor.

La descomposición LMDI parte de las emisiones térmicas observadas y las expresa como producto de actividad eléctrica, participación térmica, consumo específico, mezcla de combustibles y factor implícito. Se utiliza la media logarítmica para distribuir el cambio sin residuo. Los ceros se tratan conforme al contrato metodológico heredado. El inventario de CO₂ permanece anclado en CAMMESA; el método no reemplaza los valores publicados por un inventario alternativo (Ang, 2005).

## C. Asociación horaria y meteorología

Las regresiones horarias relacionan generación térmica con eólica y solar, controles de demanda, hidráulica, nuclear, intercambios, calendario y meteorología. Los errores se estiman de manera robusta a heterocedasticidad y correlación temporal (Newey y West, 1987). Las variantes instrumentales usan viento e irradiancia y reportan diagnósticos de fuerza y sensibilidad geográfica. La interpretación es local a la muestra y depende de exclusión, medición y especificación (Kleibergen y Paap, 2006; Sanderson y Windmeijer, 2016).

El exceso térmico horario es la distancia, en °C, por encima o por debajo de umbrales definidos en la base científica canónica. No es una suma diaria de grados-día. Las tres geografías de `BUENOS AIRES` son escenarios de medición; ninguna redefine la categoría CAMMESA. El análisis conserva esa incertidumbre en lugar de seleccionar el proxy que produce el resultado más fuerte.

## D. Atlas, crosswalk y evidencia espacial

Los límites provinciales y el relieve provienen del IGN. Las líneas y estaciones provienen de recursos abiertos de la Secretaría de Energía. Las centrales del IGN se muestran por tecnología sin escalar por potencia. La cartografía CAMMESA de agosto de 2026 se inspecciona como control de topología. Toda capa conserva fuente, fecha y huella en el registro de entradas.

El crosswalk nodal normaliza nombres, calcula proximidad geográfica y conserva el nivel de confianza. La coincidencia espacial y nominal exige coherencia en ambos planos; la coincidencia sólo espacial requiere revisión; el estado sin coincidencia confiable conserva el registro sin forzar enlace; y la falta de coordenadas identifica imposibilidad de cotejo espacial. No se usan los campos AlmaMDI sin diccionario.

Los mapas no contienen flechas de flujo, congestión, capacidad remanente, estabilidad ni pérdidas. Las ampliaciones sólo se dibujan cuando existe geometría oficial reconciliada. Cuando hay una referencia administrativa sin trazado, se usa texto y no una línea inventada.

## E. Comparación regional y sensibilidad

La comparación regional usa una clasificación armonizada para los cuatro países y años comunes 2018–2025. Los cambios se calculan en puntos porcentuales; el índice eólico–solar fija 2018 = 100; la vista per cápita divide generación 2025 por población 2025 del Banco Mundial. Los ceros nucleares de Chile y Uruguay se tratan como ceros estructurales. No se mezclan intensidades de emisiones con gases o denominadores distintos.

Las sensibilidades usan los perfiles horarios observados de 2025. El caso de demanda aplica un factor 1,05. El caso renovable aplica 1,25 a eólica y solar. El combinado aplica ambos. Carga neta = demanda − eólica − solar. Se recalculan máximo anual y P99 de rampas firmadas. No se representa despacho endógeno, respuesta de otros recursos, almacenamiento, vertimiento, red ni cambio de forma de los perfiles.

# Glosario

**Carga neta.** Demanda menos generación eólica y solar en la frontera horaria utilizada.

**Capacidad.** Potencia nominal o disponible de un equipo; no equivale a energía producida ni a capacidad firme.

**Causalidad.** Afirmación de que un cambio produce otro bajo supuestos identificadores; es más exigente que correlación o identidad.

**Curva de duración.** Horas ordenadas por nivel de demanda; muestra frecuencia, pero no secuencia temporal.

**Disponibilidad.** Proporción de tiempo o capacidad declarada disponible; no implica utilización.

**Energía.** Electricidad acumulada durante un período, expresada aquí en GWh o TWh.

**Exceso térmico horario.** Distancia en °C respecto de un umbral en una hora; no es grado-día.

**Factor de carga.** Relación entre demanda media y máxima en una frontera definida.

**Frontera.** Conjunto de activos, territorios, gases, períodos y reglas que una cifra incluye.

**Gran hidráulica.** Centrales hidráulicas fuera de la definición legal de renovables usada por CAMMESA en este informe.

**Identidad contable.** Descomposición que cierra exactamente un total sin atribuir causalidad.

**LMDI.** Método de media logarítmica que distribuye un cambio agregado entre factores sin residuo.

**Potencia.** Tasa instantánea o media horaria de producción o consumo, expresada en MW o GW.

**Rampa.** Cambio de potencia entre dos horas consecutivas, expresado en GW/h.

**Vintage.** Fecha o edición a la que corresponde un conjunto de datos.

# Abreviaturas

**CAMMESA:** Compañía Administradora del Mercado Mayorista Eléctrico.  
**CEM:** consumo específico medio.  
**CO₂:** dióxido de carbono.  
**GBA:** Gran Buenos Aires, según el uso del insumo correspondiente.  
**GW / GWh:** gigavatio / gigavatio-hora.  
**HAC:** covarianza robusta a heterocedasticidad y autocorrelación.  
**IGN:** Instituto Geográfico Nacional.  
**IV:** variables instrumentales.  
**LMDI:** índice de media logarítmica de Divisia.  
**MATER:** Mercado a Término de Energía Eléctrica de Fuente Renovable.  
**MEM:** Mercado Eléctrico Mayorista.  
**Mt:** millones de toneladas.  
**MW / MWh:** megavatio / megavatio-hora.  
**P99:** percentil 99.  
**SADI:** Sistema Argentino de Interconexión.  
**TWh:** teravatio-hora.

# Figuras y tablas

{{LISTS}}

# Bibliografía

{{BIBLIOGRAPHY}}

# Colofón

Versión v0.10.0, revisión del autor, 18 de agosto de 2026. Texto compuesto con Source Serif 4 y Source Sans 3 en formato A4. Figuras generadas desde datos y scripts incluidos en el paquete reproducible. Cartografía base y capas oficiales acreditadas en cada figura y en el registro de fuentes. La carta posterior a la portada se inserta literalmente desde el archivo ODT adjunto por el autor.

Estado: documento no publicado, no validado institucionalmente y no revisado por pares. Próximo paso recomendado: lectura integral del autor y revisión externa dirigida.
