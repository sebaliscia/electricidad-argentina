# Método de sensibilidad horaria v0.10.0

## Alcance

El ejercicio transforma mecánicamente las series horarias nacionales reconciliadas de demanda, eólica y solar de 2025. Es una prueba de esfuerzo acotada, no un pronóstico ni un modelo de expansión, despacho o red.

## Definiciones

Para cada hora \(t\), la carga neta es \(N_t=D_t-W_t-S_t\). Cada caso aplica los factores declarados en `SCENARIO_ASSUMPTIONS_v0.10.0.csv`. La punta es \(\max_t N_t\). La rampa firmada es \(R_t=N_t-N_{t-1}\), calculada sólo entre horas consecutivas válidas, y se resume con su percentil 99.

## Reproducción

`scripts/prepare_release_data.py` lee la superficie horaria canónica, construye los cuatro casos y escribe `SCENARIO_SENSITIVITY_RESULTS_v0.10.0.csv`. `scripts/generate_figures.py` produce F28 sin recalcular resultados.

## Frontera

Se conserva la forma observada de los perfiles. No se representa almacenamiento, vertimiento, respuesta de precios, disponibilidad de unidades, intercambio endógeno, reservas, fallas, red ni cambio conductual. Por eso los resultados sólo permiten comparar dirección y magnitud de dos métricas bajo supuestos explícitos.
