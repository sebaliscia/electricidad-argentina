# Electricidad argentina: cambio, límites y decisiones — v0.10.0

Paquete reproducible en español para la versión de revisión del autor. El PDF principal es `reports/ELECTRICIDAD_ARGENTINA_v0.10.0_REVISION_AUTOR.pdf` y corresponde al título editorial elegido **Electricidad argentina: cambio, límites y decisiones**.

## Estado y alcance

- Estado: revisión del autor; no publicado, no validado institucionalmente y no revisado por pares.
- Cobertura principal: balances 2005–2025, contraste estructural 2018–2025 y operación horaria 2023–2025.
- Capa espacial: red, estaciones, centrales y relieve con vintage 2026, separada de la operación 2025.
- Extensiones: atlas oficial, comparación Argentina–Brasil–Chile–Uruguay, capacidades tecnológicas preliminares y sensibilidad horaria acotada.
- Exclusiones: producto web, versión inglesa, traducción, evaluación económico-financiera ampliada, trabajo final integrador y modelado de expansión o despacho óptimo.

## Base científica canónica

El único baseline científico autorizado es el ZIP v0.8.3 con SHA-256:

`dc5f5348f5f82f78ec252cbc607703543f7186702bea790c6606c329e30749dc`

El ZIP de 84.190.072 bytes no se duplica en este release. Sus tablas necesarias, métricas canónicas y método heredado están incluidos con trazabilidad. El registro completo de entradas se encuentra en `provenance/INPUT_REGISTER_v0.10.0.csv`.

## Construcción

Requisitos: Python 3.12, ReportLab 4.4.9, pandas 2.2.3, Matplotlib 3.10.8, NumPy, Pillow 12.3.0, openpyxl 3.1.5, pypdf 6.10.0 y Poppler 24.02 o compatible. Las versiones usadas están fijadas en `environment.lock`.

Desde la raíz:

```bash
python scripts/build_v010.py
python scripts/validate_v010.py --baseline-zip /ruta/al/argentina_electricity_transition_v0.8.3.zip
```

Para rehacer también la superficie de datos desde una copia externa verificada de v0.8.3:

```bash
python scripts/prepare_release_data.py \
  --baseline-root /ruta/a/argentina_electricity_transition_v0.8.3 \
  --baseline-zip /ruta/al/argentina_electricity_transition_v0.8.3.zip
python scripts/generate_figures.py
python scripts/generate_publication_sources.py
python scripts/build_v010.py
python scripts/validate_v010.py --baseline-zip /ruta/al/argentina_electricity_transition_v0.8.3.zip
python scripts/package_release.py --output ../argentina_electricity_transition_v0.10.0.zip
```

La fuente narrativa canónica es `editorial/source/INFORME_v0.10.0.md`. La carta se inserta directamente desde el ODT original y la extracción literal queda registrada como texto para QA. Tablas, bibliografía y tokens visuales están centralizados en archivos estructurados dentro de `editorial/source`, `sources` y `editorial/styles`.

## Organización

- `reports/`: PDF principal.
- `editorial/`: arquitectura, decisiones de título, fuente canónica, estilos, tipografías y prototipos de portada.
- `figures/`: 28 visuales, cuatro de ellos mapas; PNG de publicación, SVG y tablas fuente.
- `network/`: insumos oficiales, capas procesadas, crosswalks y límites del atlas.
- `regional/`: frontera común, métricas normalizadas y conciliación.
- `strategy/`: implicancias y capacidades tecnológicas con evidencia primaria.
- `scenarios/`: puerta de factibilidad y sensibilidad acotada.
- `science/`: métricas canónicas, método heredado y registro de extensiones.
- `qa/`: controles científicos, editoriales, cartográficos, estratégicos y visuales.
- `review/`: preguntas para revisión externa dirigida; no contiene dictámenes inventados.

## Regla de lectura

Los balances anuales explican trayectoria; las series horarias explican coincidencia y rampas; los mapas ubican activos, no flujos; las identidades contables no prueban causalidad; y las pruebas de sensibilidad no son pronósticos. Toda cifra decisiva preserva frontera, unidad, vintage y limitación.

`scripts/package_release.py` vuelve a generar `MANIFEST.sha256` y produce un ZIP determinista con fecha interna fija, orden estable y permisos normalizados. El conteo físico del release es siempre cantidad de líneas del manifiesto + 1.
