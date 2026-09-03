#!/usr/bin/env python3
"""Prepare the auditable v0.10.0 data surface from the verified v0.8.3 baseline.

The script never modifies the baseline. It copies only the canonical tables needed by
the new report, derives the explicitly bounded regional/scenario tables, and converts
official geographic inputs to light, documented formats used by the figure builder.
"""

from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import math
import re
import shutil
import struct
import unicodedata
import zipfile
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_BASELINE_SHA256 = "dc5f5348f5f82f78ec252cbc607703543f7186702bea790c6606c329e30749dc"
ACCESS_DATE = "2026-08-18"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_name(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"\b(ET|E T|ESTACION|TRANSFORMADORA|CENTRAL|PROVINCIA DE|PROVINCIA)\b", " ", value.upper())
    return re.sub(r"[^A-Z0-9]+", " ", value).strip()


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(a))


def read_dbf_bytes(blob: bytes) -> list[dict[str, str]]:
    n_records = struct.unpack("<I", blob[4:8])[0]
    header_len = struct.unpack("<H", blob[8:10])[0]
    record_len = struct.unpack("<H", blob[10:12])[0]
    fields: list[tuple[str, int]] = []
    pos = 32
    while pos + 32 <= header_len and blob[pos] != 13:
        desc = blob[pos : pos + 32]
        name = desc[:11].split(b"\0", 1)[0].decode("latin1")
        fields.append((name, desc[16]))
        pos += 32
    physical = max(0, (len(blob) - header_len) // record_len)
    n_records = min(n_records, physical)
    rows: list[dict[str, str]] = []
    for i in range(n_records):
        rec = blob[header_len + i * record_len : header_len + (i + 1) * record_len]
        if not rec or rec[0:1] == b"*":
            continue
        cursor = 1
        row: dict[str, str] = {}
        for name, length in fields:
            raw = rec[cursor : cursor + length].replace(b"\0", b"")
            row[name] = raw.decode("latin1", "ignore").strip()
            cursor += length
        rows.append(row)
    return rows


def iter_shp_records(blob: bytes):
    pos = 100
    while pos + 8 <= len(blob):
        _, content_words = struct.unpack(">ii", blob[pos : pos + 8])
        pos += 8
        content = blob[pos : pos + content_words * 2]
        pos += content_words * 2
        if len(content) < 4:
            continue
        yield struct.unpack("<i", content[:4])[0], content


def rdp(points: list[list[float]], epsilon: float) -> list[list[float]]:
    if len(points) <= 3:
        return points
    a, b = np.asarray(points[0]), np.asarray(points[-1])
    segment = b - a
    norm = float(np.dot(segment, segment))
    arr = np.asarray(points)
    if norm == 0:
        distances = np.linalg.norm(arr - a, axis=1)
    else:
        t = np.clip(((arr - a) @ segment) / norm, 0, 1)
        proj = a + t[:, None] * segment
        distances = np.linalg.norm(arr - proj, axis=1)
    idx = int(np.argmax(distances))
    if distances[idx] <= epsilon:
        return [points[0], points[-1]]
    return rdp(points[: idx + 1], epsilon)[:-1] + rdp(points[idx:], epsilon)


def polygon_features_from_zip(path: Path) -> dict:
    with zipfile.ZipFile(path) as zf:
        shp_name = next(n for n in zf.namelist() if n.lower().endswith(".shp"))
        dbf_name = next(n for n in zf.namelist() if n.lower().endswith(".dbf"))
        shp, dbf = zf.read(shp_name), read_dbf_bytes(zf.read(dbf_name))
    features = []
    for attrs, (shape_type, content) in zip(dbf, iter_shp_records(shp)):
        if shape_type not in (5, 15, 25):
            continue
        num_parts, num_points = struct.unpack("<ii", content[36:44])
        starts = list(struct.unpack(f"<{num_parts}i", content[44 : 44 + 4 * num_parts]))
        points_offset = 44 + 4 * num_parts
        pts = [list(struct.unpack("<dd", content[points_offset + 16 * i : points_offset + 16 * (i + 1)])) for i in range(num_points)]
        starts.append(num_points)
        polygons = []
        for a, b in zip(starts[:-1], starts[1:]):
            ring = pts[a:b]
            if len(ring) < 4:
                continue
            simp = rdp(ring, 0.018)
            if simp[0] != simp[-1]:
                simp.append(simp[0])
            polygons.append([simp])
        name = attrs.get("nam") or attrs.get("fna") or attrs.get("gid")
        features.append({"type": "Feature", "properties": {"gid": attrs.get("gid"), "name": name, "in1": attrs.get("in1"), "source": "IGN"}, "geometry": {"type": "MultiPolygon", "coordinates": polygons}})
    return {"type": "FeatureCollection", "name": "provincias_IGN_simplificadas", "features": features}


def point_rows_from_zip(path: Path) -> list[dict]:
    with zipfile.ZipFile(path) as zf:
        shp_name = next(n for n in zf.namelist() if n.lower().endswith(".shp"))
        dbf_name = next(n for n in zf.namelist() if n.lower().endswith(".dbf"))
        shp, dbf = zf.read(shp_name), read_dbf_bytes(zf.read(dbf_name))
    rows = []
    for attrs, (shape_type, content) in zip(dbf, iter_shp_records(shp)):
        if shape_type == 1:
            lon, lat = struct.unpack("<dd", content[4:20])
        elif shape_type == 8:
            n = struct.unpack("<i", content[36:40])[0]
            if not n:
                continue
            lon, lat = struct.unpack("<dd", content[40:56])
        else:
            continue
        rows.append({**attrs, "longitude": lon, "latitude": lat})
    return rows


def json_point(value: str) -> tuple[float, float] | None:
    try:
        geom = json.loads(value)
        coords = geom["coordinates"]
        while coords and isinstance(coords[0], list):
            coords = coords[0]
        return float(coords[0]), float(coords[1])
    except Exception:
        return None


def prepare_baseline_tables(baseline: Path) -> None:
    outputs = baseline / "outputs"
    mapping = {
        "data_scope_and_quality/annual_accounting_bridge_2005_2025.csv": "annual_accounting_bridge_2005_2025.csv",
        "power_mix_exploration/annual_power_mix_2012_2025.csv": "annual_power_mix_2012_2025.csv",
        "power_mix_exploration/supply_change_bridge_2018_2025.csv": "supply_change_bridge_2018_2025.csv",
        "power_mix_exploration/renewable_capacity_by_technology_2012_2025.csv": "renewable_capacity_by_technology_2012_2025.csv",
        "power_mix_exploration/renewable_generation_by_technology_2012_2025.csv": "renewable_generation_by_technology_2012_2025.csv",
        "demand_and_exchanges/annual_demand_balance_2012_2025.csv": "annual_demand_balance_2012_2025.csv",
        "demand_and_exchanges/demand_components_2012_2025.csv": "demand_components_2012_2025.csv",
        "demand_and_exchanges/annual_exchange_metrics_2012_2025.csv": "annual_exchange_metrics_2012_2025.csv",
        "v080_peak_flexibility/hourly_demand_duration_curve_2023_2025.csv.gz": "hourly_demand_duration_curve_2023_2025.csv.gz",
        "v080_peak_flexibility/hourly_ramp_summary_2023_2025.csv": "hourly_ramp_summary_2023_2025.csv",
        "v080_peak_flexibility/top_demand_hours_dispatch_summary_2023_2025.csv": "top_demand_hours_dispatch_summary_2023_2025.csv",
        "final_substantive_expansion/renewable_generation_by_program_2012_2025.csv": "renewable_generation_by_program_2012_2025.csv",
        "hydropower_case_study/large_hydro_annual_2018_2025.csv": "large_hydro_annual_2018_2025.csv",
        "hydropower_case_study/binational_allocation_decomposition_2018_2025.csv": "binational_allocation_decomposition_2018_2025.csv",
        "hydropower_case_study/comahue_annual_indicators_2018_2025.csv": "comahue_annual_indicators_2018_2025.csv",
        "v082_corrections/comahue_2024_2025_decomposition_v082.csv": "comahue_2024_2025_decomposition.csv",
        "thermal_generation_and_emissions/annual_thermal_emissions_indicators_2018_2025.csv": "annual_thermal_emissions_indicators_2018_2025.csv",
        "thermal_generation_and_emissions/lmdi_direct_absolute_2018_2025.csv": "lmdi_direct_absolute_2018_2025.csv",
        "hourly_dispatch_and_fossil_displacement/thermal_technology_response.csv": "thermal_technology_response.csv",
        "weather_iv_remediation_v070/iv_estimates_side_by_side.csv": "iv_estimates_side_by_side.csv",
        "hourly_dispatch_and_fossil_displacement/model_based_displacement_and_emissions_2023_2025.csv": "model_based_displacement_and_emissions_2023_2025.csv",
        "provincial_and_regional_transition/provincial_capacity_summary_june_2026.csv": "provincial_capacity_summary_june_2026.csv",
        "provincial_and_regional_transition/provincial_demand_summary_2023_2025.csv": "provincial_demand_summary_2023_2025.csv",
        "provincial_and_regional_transition/provincial_renewable_summary_2018_2025.csv": "provincial_renewable_summary_2018_2025.csv",
        "v083_corrections/annual_peak_weather_sensitivity_v083.csv": "annual_peak_weather_sensitivity_v083.csv",
        "v083_corrections/regional_harmonized_trajectory_v083.csv": "regional_harmonized_trajectory_v083.csv",
        "v083_corrections/regional_harmonized_changes_v083.csv": "regional_harmonized_changes_v083.csv",
        "v083_corrections/regional_official_endpoints_v083.csv": "regional_official_endpoints_v083.csv",
        "v082_corrections/network_projects_status_v082.csv": "network_projects_status_v082.csv",
        "v082_corrections/network_nodes_v082.csv": "network_nodes_v082.csv",
        "v082_corrections/network_edges_v082.csv": "network_edges_v082.csv",
    }
    for rel, name in mapping.items():
        src = outputs / rel
        if not src.exists():
            raise FileNotFoundError(src)
        shutil.copy2(src, ROOT / "figures" / "data" / name)
    shutil.copy2(baseline / "reports/source/canonical_metrics_v083.csv", ROOT / "science/CANONICAL_METRICS_v0.10.0.csv")
    shutil.copy2(baseline / "sources/source_registry_v083.csv", ROOT / "sources/SOURCE_REGISTRY_BASELINE_v0.8.3.csv")
    shutil.copy2(baseline / "reports/source/METODOLOGIA_TECNICA_ES_v0.8.3.md", ROOT / "science/METODOLOGIA_HEREDADA_v0.8.3.md")


def prepare_geography() -> None:
    raw = ROOT / "network/raw_official"
    processed = ROOT / "network/processed"
    provinces = polygon_features_from_zip(raw / "ign_provincia.zip")
    (processed / "provincias_IGN_simplificadas.geojson").write_text(json.dumps(provinces, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    plants = point_rows_from_zip(raw / "ign_centrales_energia.zip")
    plant_df = pd.DataFrame(plants).rename(columns={"nam": "name", "gna": "technology_label", "fna": "full_name", "fdc": "original_source"})
    keep = [c for c in ["gid", "name", "full_name", "technology_label", "fun", "ppc", "original_source", "longitude", "latitude"] if c in plant_df]
    plant_df[keep].to_csv(processed / "centrales_IGN.csv", index=False)

    stations = pd.read_csv(raw / "estaciones.csv")
    stations.columns = [c.lstrip("\ufeff") for c in stations.columns]
    coords = stations["geojson"].map(json_point)
    stations["longitude"] = coords.map(lambda x: x[0] if x else np.nan)
    stations["latitude"] = coords.map(lambda x: x[1] if x else np.nan)
    stations.to_csv(processed / "estaciones_transformadoras_energia_2026.csv", index=False)

    lines = pd.read_csv(raw / "transporte_lineas.csv")
    lines.columns = [c.lstrip("\ufeff") for c in lines.columns]
    features = []
    for _, row in lines.iterrows():
        try:
            geometry = json.loads(row["geojson"])
        except Exception:
            continue
        props = {k: (None if pd.isna(row[k]) else row[k]) for k in ["nombre", "id", "tension", "fecha_puesta_servicio", "propiedad", "concesion"]}
        features.append({"type": "Feature", "properties": props, "geometry": geometry})
    (processed / "lineas_AT_energia_2026.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # Mosaic of the official Argenmap Topo TMS tiles. TMS y grows from south to north.
    tile_dir = raw / "argenmap_z5"
    xs, ys = [9, 10, 11], [9, 10, 11, 12, 13, 14]
    mosaic = Image.new("RGBA", (256 * len(xs), 256 * len(ys)), (255, 255, 255, 0))
    for xi, x in enumerate(xs):
        for y in ys:
            img = Image.open(tile_dir / f"5_{x}_{y}.png").convert("RGBA")
            mosaic.paste(img, (xi * 256, (max(ys) - y) * 256))
    mosaic.save(processed / "argenmap_topo_z5_mosaic.png")
    origin = 20037508.342789244
    tile_span = 2 * origin / 32
    bounds = {"epsg": 3857, "xmin": -origin + min(xs) * tile_span, "xmax": -origin + (max(xs) + 1) * tile_span, "ymin": -origin + min(ys) * tile_span, "ymax": -origin + (max(ys) + 1) * tile_span, "zoom": 5, "x_tiles": xs, "tms_y_tiles": ys}
    (processed / "argenmap_topo_z5_bounds.json").write_text(json.dumps(bounds, indent=2), encoding="utf-8")

    alma = pd.read_excel(raw / "AlmaMDI_NODOS_2024-01-30.xlsx", sheet_name="Hoja2")
    safe = alma[["ET", "NOMBRE ET", "LAT", "LONG", "kV", "REGION"]].copy()
    safe.columns = ["alma_id", "alma_name", "latitude", "longitude", "voltage_kv", "region"]
    safe["coordinate_status"] = np.where(safe[["latitude", "longitude"]].notna().all(axis=1), "VALID", "MISSING")
    safe.to_csv(processed / "almamdi_nodes_safe.csv", index=False)

    station_points = stations.dropna(subset=["latitude", "longitude"]).copy()
    crosswalk = []
    for _, a in safe.iterrows():
        if pd.isna(a.latitude) or pd.isna(a.longitude):
            crosswalk.append({"alma_id": a.alma_id, "alma_name": a.alma_name, "alma_voltage_kv": a.voltage_kv, "official_station": "", "distance_km": "", "name_similarity": "", "match_status": "MISSING_COORDINATES", "interpretation_limit": "No se infiere saturación ni capacidad desde la planilla"})
            continue
        distances = station_points.apply(lambda s: haversine_km(a.latitude, a.longitude, s.latitude, s.longitude), axis=1)
        idx = distances.idxmin()
        s = station_points.loc[idx]
        similarity = difflib.SequenceMatcher(None, normalize_name(a.alma_name), normalize_name(s["nombre"])).ratio()
        dist = float(distances.loc[idx])
        status = "MATCHED_SPATIAL_AND_NAME" if dist <= 15 and similarity >= 0.45 else ("MATCHED_SPATIAL_ONLY" if dist <= 2.5 else "NO_CONFIDENT_MATCH")
        crosswalk.append({"alma_id": a.alma_id, "alma_name": a.alma_name, "alma_voltage_kv": a.voltage_kv, "official_station": s["nombre"], "official_station_id": s.get("id", ""), "distance_km": round(dist, 3), "name_similarity": round(similarity, 3), "match_status": status, "interpretation_limit": "Control de identidad; no valida potencia, limitaciones ni estado operativo"})
    pd.DataFrame(crosswalk).to_csv(ROOT / "network/NODE_CROSSWALK_v0.10.0.csv", index=False)

    edges = pd.read_csv(ROOT / "figures/data/network_edges_v082.csv")
    nodes = pd.read_csv(ROOT / "figures/data/network_nodes_v082.csv").set_index("node_id")
    official_names = lines["nombre"].fillna("").astype(str).tolist()
    edge_rows = []
    for _, e in edges.iterrows():
        a = str(nodes.loc[e.from_node_id, "node_name"])
        b = str(nodes.loc[e.to_node_id, "node_name"])
        ta = normalize_name(a).split()
        tb = normalize_name(b).split()
        candidates = []
        for name in official_names:
            nn = normalize_name(name)
            if any(t in nn for t in ta if len(t) >= 4) and any(t in nn for t in tb if len(t) >= 4):
                candidates.append(name)
        edge_rows.append({"analytic_edge_id": e.edge_id, "from_node": a, "to_node": b, "nominal_voltage_kv": e.nominal_voltage_kv, "analytic_status": e.edge_status, "official_line_candidates": " | ".join(candidates[:5]), "candidate_count": len(candidates), "crosswalk_status": "NAME_CANDIDATE_ONLY" if candidates else "NO_AUTOMATIC_MATCH", "flow_inference": "PROHIBITED", "note": "La geometría oficial se usa como infraestructura; el unifilar CAMMESA valida conectividad representativa"})
    pd.DataFrame(edge_rows).to_csv(ROOT / "network/EDGE_CROSSWALK_v0.10.0.csv", index=False)

    source_rows = [
        ["ENERGIA_LINES_2026", "Secretaría de Energía", "Transporte Eléctrico AT Líneas", "2026-06-05 (SHP); 2025-12-05 (CSV)", 1299, "geometría, tensión y nombre", "no prueba flujo, congestión ni estado horario", sha256(raw / "transporte_lineas.csv")],
        ["ENERGIA_STATIONS_2026", "Secretaría de Energía", "Estaciones Transformadoras AT", "2026-08-05", 323, "ubicación, tensiones declaradas y potencia nominal publicada", "no prueba disponibilidad ni saturación", sha256(raw / "estaciones.csv")],
        ["IGN_PROVINCES", "Instituto Geográfico Nacional", "Provincia WFS", f"snapshot {ACCESS_DATE}; vintage efectivo no publicado", 24, "límites oficiales", "simplificación sólo para representación", sha256(raw / "ign_provincia.zip")],
        ["IGN_PLANTS", "Instituto Geográfico Nacional", "Centrales eléctricas WFS", f"snapshot {ACCESS_DATE}; vintage efectivo no publicado", len(plants), "ubicación y etiqueta tecnológica", "no se usa para potencia instalada", sha256(raw / "ign_centrales_energia.zip")],
        ["IGN_ARGENMAP", "Instituto Geográfico Nacional", "Argenmap Topo TMS con relieve", f"snapshot {ACCESS_DATE}; composición vigente", 18, "relieve y contexto cartográfico", "mosaico a zoom 5; no es dato de elevación analítico", "MULTIPLE_TILE_HASHES_IN_INPUT_REGISTER"],
        ["CAMMESA_2026", "CAMMESA", "GEOSADI, red 500/330 kV y unifilares regionales", "2026-08", 7, "validación visual de topología visible", "sin inferencia de flujo, capacidad disponible o congestión", "SEE_INPUT_REGISTER"],
        ["ALMAMDI_2024", "Archivo adjunto del autor", "Nodos AlmaMDI", "2024-01-30", len(safe), "nombre, coordenadas, tensión y región", "categorías y limitaciones no interpretadas sin diccionario oficial", sha256(raw / "AlmaMDI_NODOS_2024-01-30.xlsx")],
    ]
    pd.DataFrame(source_rows, columns=["source_id", "authority", "resource", "vintage", "records", "supports", "does_not_support", "sha256"]).to_csv(ROOT / "network/NETWORK_SOURCE_CROSSWALK_v0.10.0.csv", index=False)


def prepare_regional() -> None:
    traj = pd.read_csv(ROOT / "figures/data/regional_harmonized_trajectory_v083.csv")
    pop_json = json.loads((ROOT / "sources/world_bank_population_2025.json").read_text(encoding="utf-8"))
    pop = {r["country"]["value"]: r["value"] for r in pop_json[1]}
    map_name = {"Argentina": "Argentina", "Brazil": "Brazil", "Chile": "Chile", "Uruguay": "Uruguay"}
    rows = []
    for country, group in traj.groupby("country"):
        group = group.sort_values("year")
        base = group.iloc[0]
        for _, r in group.iterrows():
            p = pop[map_name[country]]
            ws = r.wind_electricity_twh + r.solar_electricity_twh
            base_ws = base.wind_electricity_twh + base.solar_electricity_twh
            rows.append({"country": country, "country_es": r.country_es, "year": int(r.year), "generation_twh": r.electricity_generation, "hydro_twh": r.hydro_electricity_twh, "wind_twh": r.wind_electricity_twh, "solar_twh": r.solar_electricity_twh, "other_renewables_twh": r.other_renewables_electricity_twh, "nuclear_twh": r.nuclear_electricity_twh, "fossil_twh": r.fossil_electricity_twh, "renewables_share_pct": r.renewables_share_elec, "fossil_share_pct": r.fossil_share_elec, "wind_solar_index_2018_100": ws / base_ws * 100, "wind_solar_2018_twh": base_ws, "population_2025": p, "renewable_mwh_per_capita_2025": (r.renewables_electricity * 1e6 / p) if r.year == 2025 else np.nan, "fossil_mwh_per_capita_2025": (r.fossil_electricity_twh * 1e6 / p) if r.year == 2025 else np.nan, "harmonized_frontier": "OWID adaptation of Ember Yearly Electricity Data 2026", "population_source": "World Bank WDI SP.POP.TOTL; updated 2026-07-13"})
    metrics = pd.DataFrame(rows)
    metrics.to_csv(ROOT / "regional/REGIONAL_NORMALIZED_METRICS_v0.10.0.csv", index=False)
    metrics.to_csv(ROOT / "figures/data/regional_normalized_metrics_v010.csv", index=False)
    boundary = [
        ["generation_twh", "Generación eléctrica dentro de la frontera armonizada", "TWh", "incluye todas las fuentes registradas por Ember/OWID", "no equivale automáticamente a oferta interna nacional"],
        ["renewables", "Hidráulica + eólica + solar + otras renovables", "TWh y %", "misma taxonomía armonizada para cuatro países", "no equivale a la definición legal argentina"],
        ["fossil", "Generación fósil como cierre no negativo", "TWh y %", "misma frontera física", "no es consumo de combustibles"],
        ["per_capita", "Generación armonizada dividida por población 2025", "MWh/hab", "población WDI común", "no mide consumo final por habitante"],
        ["structural_zero", "Nuclear en Chile y Uruguay", "TWh", "cero estructural retenido", "no imputar desde redondeos"],
    ]
    pd.DataFrame(boundary, columns=["metric", "definition", "unit", "included", "excluded_or_limit"]).to_csv(ROOT / "regional/REGIONAL_BOUNDARY_DICTIONARY_v0.10.0.csv", index=False)
    reconciliation = []
    official = pd.read_csv(ROOT / "figures/data/regional_official_endpoints_v083.csv")
    for _, r in official.iterrows():
        h = traj[(traj.country == r.country) & (traj.year == r.year)]
        reconciliation.append({"country": r.country, "year": r.year, "official_electricity_twh": r.electricity_twh, "harmonized_generation_twh": None if h.empty else h.iloc[0].electricity_generation, "official_renewable_share_pct": r.renewable_share_pct, "harmonized_renewable_share_pct": None if h.empty else h.iloc[0].renewables_share_elec, "official_frontier": r.official_frontier, "reconciliation_status": "CONTROL_ONLY_NOT_SUBSTITUTED", "note": r.note})
    pd.DataFrame(reconciliation).to_csv(ROOT / "regional/REGIONAL_SOURCE_RECONCILIATION_v0.10.0.csv", index=False)


def prepare_scenario(baseline: Path) -> None:
    path = baseline / "outputs/hourly_dispatch_and_fossil_displacement/model_ready_hourly_2023_2025.csv.gz"
    df = pd.read_csv(path, parse_dates=["datetime"])
    df = df[df.year == 2025].copy()
    base_net = df.load - df.wind - df.solar
    threshold = base_net.quantile(0.99)
    designs = [("OBSERVED_2025", "Observado 2025", 1.00, 1.00), ("LOAD_PLUS_5", "Demanda +5 %", 1.05, 1.00), ("VRE_PLUS_25", "Eólica + solar +25 %", 1.00, 1.25), ("COMBINED", "Combinado", 1.05, 1.25)]
    rows = []
    for sid, label, load_scale, vre_scale in designs:
        load = df.load * load_scale
        vre = (df.wind + df.solar) * vre_scale
        net = load - vre
        ramp = net.diff()
        rows.append({"sensitivity_id": sid, "label_es": label, "load_scale": load_scale, "wind_solar_scale": vre_scale, "peak_load_gw": load.max() / 1000, "peak_net_load_gw": net.max() / 1000, "minimum_net_load_gw": net.min() / 1000, "p99_upward_net_ramp_gw_per_h": ramp.quantile(0.99) / 1000, "hours_above_observed_p99_net_load": int((net > threshold).sum()), "balance_definition": "net_load = scaled_load - scaled_wind - scaled_solar", "dispatch_feasibility": "NOT_TESTED", "storage_curtailment_network_commitment": "NOT_MODELED", "interpretation": "stress test algebraico acotado; no pronóstico ni expansión óptima"})
    out = pd.DataFrame(rows)
    out.to_csv(ROOT / "scenarios/SCENARIO_SENSITIVITY_RESULTS_v0.10.0.csv", index=False)
    out.to_csv(ROOT / "figures/data/scenario_sensitivity_results_v010.csv", index=False)


def prepare_strategy() -> None:
    implications = [
        ["IMP01", "La punta crece más rápido que la energía", "Demanda local +6,2 % y punta instantánea +15,0 % entre 2018 y 2025", "La exigencia de capacidad y flexibilidad crece aunque el volumen anual cambie menos", "rigidez operativa y oportunidad de gestión de punta", "forma y horario de la demanda", "gestión de demanda; medición subhoraria; recursos flexibles", "CAMMESA; distribuidores; grandes usuarios; reguladores", "corto/medio", "elasticidad horaria y respuesta de usuarios", "HIGH", "C03_PEAK"],
        ["IMP02", "Expansión renovable lejos de grandes centros de carga", "Chubut y otras provincias exportan un equivalente energético mientras Buenos Aires + CABA concentra 49,0 % de la demanda", "La geografía de generación y consumo no coincide", "oportunidad renovable condicionada por red", "capacidad de evacuación y localización", "planificación de transmisión; datos nodales; coordinación territorial", "Secretaría de Energía; CAMMESA; transportistas; provincias", "medio/largo", "capacidad y flujo por corredor", "MEDIUM", "C07_TERRITORY"],
        ["IMP03", "Caída hidráulica y exposición a años secos", "Gran hidráulica -9,807 TWh; Yacyretá y Comahue explican gran parte del cambio", "El agua no es una base constante y su asignación binacional importa", "riesgo hidrológico y oportunidad de modernización", "pronóstico hidrológico; disponibilidad; coordinación de embalses", "modernización; datos hidrológicos trazables; escenarios secos", "operadores; autoridades de cuenca; CAMMESA", "corto/largo", "aportes, restricciones y despacho horario", "HIGH", "C05_HYDRO"],
        ["IMP04", "Intercambios pequeños en el año, útiles en horas críticas", "Comercio bruto 3,41 % y saldo neto 2,69 % de la demanda local en 2025", "El peso anual no mide el valor operativo de una interconexión", "respaldo regional con dependencia acotada", "disponibilidad horaria de interconexiones", "coordinación operativa y transparencia de disponibilidad", "CAMMESA; operadores vecinos; Secretaría de Energía", "corto", "capacidad disponible y precios quedan fuera", "MEDIUM", "C08_TRADE"],
        ["IMP05", "RenovAr y MATER coexisten", "En 2025 aportan 11,344 y 10,741 TWh respectivamente", "La expansión surgió de instrumentos distintos y complementarios", "diversidad de canales de incorporación", "reglas de acceso y atribución por programa", "preservar trazabilidad de proyectos y generación", "Secretaría de Energía; CAMMESA; generadores; grandes usuarios", "corto/medio", "serie por proyecto y cambios de etiqueta", "HIGH", "C04_PROGRAMS"],
        ["IMP06", "Menor generación térmica, potencia y flexibilidad aún necesarias", "Térmica -12,502 TWh; 58,53 % de la carga en las 100 horas de mayor demanda", "Menos energía térmica no equivale a prescindir de respuesta gestionable", "reducción de emisiones con desafío de suficiencia", "disponibilidad, rampas y servicios complementarios", "medir atributos; coordinar renovables, demanda, hidro y almacenamiento", "CAMMESA; generadores; reguladores", "corto/medio", "servicios complementarios y indisponibilidades", "HIGH", "C06_THERMAL"],
        ["IMP07", "Concentración de demanda", "Buenos Aires + CABA representa 49,0 % de la demanda provincial publicada de 2025", "Un problema nacional tiene un centro de gravedad territorial", "concentración de riesgo y escala de intervención", "calidad y punta nodal en el área de carga", "medición y refuerzos con lectura federal", "distribuidores; CAMMESA; provincias; reguladores", "corto/medio", "separación CABA/provincia y nivel nodal", "HIGH", "C07_CONCENTRATION"],
        ["IMP08", "Separar infraestructura, operación y capacidad", "Los mapas 2026 muestran activos; no contienen flujos ni disponibilidad 2025", "Una línea dibujada no prueba margen de transporte", "evitar diagnósticos falsos", "vintage y clase de evidencia", "publicar capacidad, flujo y estado con identidad de activo", "CAMMESA; transportistas; Secretaría de Energía", "corto", "series horarias por activo", "HIGH", "C02_BOUNDARIES"],
        ["IMP09", "Datos nodales y subhorarios", "La evidencia pública permite balances horarios agregados, pero no congestión ni recorte por nodo", "Las decisiones finas requieren datos más finos", "aprendizaje institucional", "resolución espacial y temporal", "diccionario nodal; IDs persistentes; recortes; reservas; calidad", "CAMMESA; reguladores; distribuidores; academia", "corto", "datos de red y demanda con documentación", "HIGH", "C11_DATA"],
    ]
    columns = ["implication_id", "phenomenon", "evidence", "plain_meaning", "risk_or_opportunity", "decision_variable", "possible_action_family", "responsible_actors", "horizon", "missing_data", "confidence", "source_claim_id"]
    pd.DataFrame(implications, columns=columns).to_csv(ROOT / "strategy/STRATEGIC_IMPLICATION_MATRIX_v0.10.0.csv", index=False)

    capabilities = [
        ["Transformadores y equipamiento de alta tensión", "renovar y ampliar nodos 500/330/220 kV", "fabricación declarada de transformadores de potencia hasta 500 kV; capacidades nacionales de calibración y ensayo", "DEMONSTRATED", "materiales especiales, cambiadores, aislación y componentes no auditados", "falta censo de capacidad productiva y referencias verificadas activo por activo", "calificación, ensayos y mantenimiento avanzado", "industria; INTI; transportistas; universidades", "Faraday 2026; INTI 2025", "contenido local y cuellos de suministro", "BOUNDED_VERIFIED"],
        ["Conductores, torres, protecciones y servicios de ingeniería", "refuerzos y repotenciación de corredores", "fabricación declarada de conductores aéreos para transmisión hasta 500 kV; ingeniería y construcción AT documentada", "DEMONSTRATED_PARTIAL", "herrajes, aisladores, acero y protección digital no reconciliados", "torres y protecciones requieren evidencia adicional", "reconductoring, ensayos y diseño de corredor", "industria; transportistas; INTI; ingeniería", "IMSA 2022; IMPSA 2026", "censo por componente y norma", "PARTIAL"],
        ["Electrónica de potencia", "integrar renovables, calidad y control de tensión", "grupos CONICET-universidad declaran investigación en convertidores, control y redes inteligentes", "R_AND_D_DEMONSTRATED", "semiconductores de potencia y escala fabril no verificados", "brecha entre prototipo, certificación y producción", "pilotos de convertidores, protección y calidad", "CONICET; universidades; INTI; industria", "CONICET-UNSJ 2026; CONICET-UNaM 2026", "madurez tecnológica y transferencia", "PARTIAL"],
        ["Integración y control de almacenamiento", "suavizar rampas y desplazar demanda", "INTI documenta ensayos y asistencia en baterías; IEE CONICET-UNSJ declara líneas de almacenamiento y microrredes", "R_AND_D_AND_TESTING", "celdas, BMS de escala de red e integración EMS no verificados", "no hay inventario nacional de proyectos operativos comparable", "protocolos, seguridad, control y demostradores", "INTI; CONICET; universidades; CAMMESA; distribuidores", "INTI 2026; CONICET-UNSJ 2026", "datos de desempeño y seguridad", "PARTIAL"],
        ["Pronóstico, software, SCADA y ciberseguridad", "operar un sistema más variable y observable", "CAMMESA opera SCADA/EMS y protocolos SOTR; existe estrategia nacional de ciberseguridad", "OPERATING_CAPABILITY_WITH_GAP", "hardware, licencias y proveedores críticos no auditados", "no se verificó capacidad doméstica completa de producto ni postura OT sectorial", "pronóstico abierto, interoperabilidad, simuladores y seguridad OT", "CAMMESA; agentes; universidades; organismos de ciberseguridad", "CAMMESA 2026; JGM 2023", "inventario OT, incidentes y dependencia de proveedores", "PARTIAL"],
        ["Modernización hidráulica", "recuperar disponibilidad y flexibilidad sin confundir agua con capacidad", "IMPSA documenta modernizaciones, rehabilitaciones, repotenciaciones, automatización y O&M hidro", "DEMONSTRATED", "componentes especializados y cartera de referencias no auditados", "priorización requiere diagnóstico por unidad", "rehabilitación, control, protección y pronóstico", "operadores; industria; universidades; autoridades hídricas", "IMPSA Hydro 2026", "estado de unidades y restricciones hidráulicas", "BOUNDED_VERIFIED"],
        ["Operación y mantenimiento eólico/solar", "sostener disponibilidad de una flota creciente", "la operación de parques registrados y los laboratorios INTI prueban capacidad de ensayo y asistencia; no se infiere integración local", "OPERATING_AND_TESTING_PARTIAL", "repuestos de aerogeneradores, inversores y módulos", "faltan métricas públicas de disponibilidad y tiempos de reparación", "formación, inspección, diagnóstico y repuestos", "generadores; INTI; universidades; proveedores", "CAMMESA 2026; INTI 2026", "KPIs de O&M y origen de repuestos", "PARTIAL"],
        ["Componentes y servicios de cadenas eólica y solar", "capturar aprendizaje industrial sin bloquear despliegue", "INTI dispone de laboratorios solar y eólico y gestiona REPROER; hay servicios de ingeniería documentados", "TESTING_AND_SERVICES_DEMONSTRATED", "módulos, celdas, electrónica y grandes componentes no verificados como producción local", "registro no equivale a capacidad competitiva ni a contenido estable", "metrología, certificación, estructuras, cables y servicios", "INTI; industria; universidades; generadores", "INTI Renovables 2026", "capacidad, calidad y escala por componente", "PARTIAL"],
        ["Capacidades nucleares y de investigación", "preservar generación firme y conocimiento de ciclo largo", "operación de tres centrales, centros atómicos, combustible y componentes, más proyectos de investigación documentados", "DEMONSTRATED_SYSTEMIC", "equipos y servicios importados específicos no cuantificados", "necesidad de separar operación, combustible, ingeniería, fabricación e I+D", "extensión de vida, formación, combustibles, materiales y control", "CNEA; Nucleoeléctrica; CONUAR; INVAP; universidades", "CNEA/INAP 2023; Nucleoeléctrica 2026", "dependencias críticas y renovación de capacidades", "BOUNDED_VERIFIED"],
    ]
    cap_cols = ["technology_or_capability", "planning_need", "documented_domestic_evidence", "evidence_level", "critical_import_dependency", "bottleneck", "learning_opportunity", "relevant_actors", "source", "data_gap", "claim_status"]
    pd.DataFrame(capabilities, columns=cap_cols).to_csv(ROOT / "strategy/NATIONAL_TECH_CAPABILITY_MATRIX_v0.10.0.csv", index=False)


def write_editorial_tables() -> None:
    claims = [
        ["C01_SYSTEM", "Cambio de la oferta 2018–2025", "1", "supply_change_bridge_2018_2025.csv", "F02", "PRIMARY"],
        ["C02_BOUNDARIES", "Diferenciar generación, oferta, demanda, topología y operación", "2", "concept contracts + GIS registers", "T02", "PRIMARY"],
        ["C03_PEAK", "La punta creció más rápido que la energía", "3", "annual_demand_balance_2012_2025.csv", "F03", "PRIMARY"],
        ["C03_DURATION", "Curva de duración 2023–2025", "3", "hourly_demand_duration_curve_2023_2025.csv.gz", "F05", "PRIMARY"],
        ["C03_RAMP", "La carga neta exige rampas superiores", "3", "hourly_ramp_summary_2023_2025.csv", "F07", "PRIMARY"],
        ["C04_RENEW", "Expansión eólica y solar", "4", "renewable generation/capacity tables", "F08", "PRIMARY"],
        ["C04_PROGRAMS", "Coexistencia RenovAr y MATER", "4", "renewable_generation_by_program_2012_2025.csv", "F09", "PRIMARY"],
        ["C05_HYDRO", "Caída y composición hidráulica", "5", "large_hydro_annual_2018_2025.csv", "F11", "PRIMARY"],
        ["C05_YACY", "Yacyretá: producción y asignación", "5", "binational_allocation_decomposition_2018_2025.csv", "F12", "PRIMARY"],
        ["C06_THERMAL", "Generación térmica y emisiones", "6", "annual_thermal_emissions_indicators_2018_2025.csv", "F14", "PRIMARY"],
        ["C06_LMDI", "Descomposición de emisiones", "6", "lmdi_direct_absolute_2018_2025.csv", "F15", "PRIMARY"],
        ["C06_HOURLY", "Asociaciones horarias condicionales, no causales", "6", "thermal_technology_response.csv", "F16", "PRIMARY"],
        ["C07_TERRITORY", "Geografía de red, generación y consumo", "7", "official GIS + baseline provincial tables", "M01/M02", "PRIMARY"],
        ["C07_CONCENTRATION", "Buenos Aires + CABA concentra 49,0 % de demanda", "7", "provincial_demand_summary_2023_2025.csv", "M02", "PRIMARY"],
        ["C08_REGION", "Comparación regional normalizada", "8", "REGIONAL_NORMALIZED_METRICS", "F22-F25", "PRIMARY"],
        ["C08_TRADE", "Comercio bruto y saldo neto", "8", "annual_exchange_metrics_2012_2025.csv", "F17", "SECONDARY"],
        ["C09_DECISION", "Matriz de implicancias", "9", "STRATEGIC_IMPLICATION_MATRIX", "F26", "PRIMARY"],
        ["C09_CAP", "Capacidades tecnológicas preliminares", "9", "NATIONAL_TECH_CAPABILITY_MATRIX", "F27", "PRIMARY"],
        ["C09_STRESS", "Sensibilidad acotada, no pronóstico", "9", "SCENARIO_SENSITIVITY_RESULTS", "F28", "PRIMARY"],
        ["C10_SYNTHESIS", "La transición cambia energía, potencia, territorio e instituciones", "10", "integrated synthesis", "none", "PRIMARY"],
        ["C11_DATA", "Agenda de datos nodales y subhorarios", "11", "gap register", "T11", "PRIMARY"],
    ]
    pd.DataFrame(claims, columns=["claim_id", "claim", "home_chapter", "evidence", "visual", "role"]).to_csv(ROOT / "editorial/CLAIM_HOME_LEDGER_v0.10.0.csv", index=False)
    migration = [
        ["v0.8.3 opening/mix", "Ch. 1", "REWRITE_AND_CONDENSE", "2005/2012/2018/2025 opening retained"],
        ["scope and methods", "Ch. 2 + Annex A", "SPLIT", "reader-facing boundaries in body; formulas in annex"],
        ["demand and flexibility", "Ch. 3", "INTEGRATE", "annual, duration, peaks and ramps in one arc"],
        ["renewables and programs", "Ch. 4", "INTEGRATE", "technology and instrument evidence combined"],
        ["hydropower cases", "Ch. 5", "INTEGRATE", "Yacyretá and Comahue under water-risk question"],
        ["thermal, emissions, hourly models", "Ch. 6 + Annex B", "INTEGRATE_AND_MOVE_METHOD", "plain meaning in body; diagnostics in annex"],
        ["province and network policy", "Ch. 7 + Atlas annex", "EXPAND", "new official GIS and 2026 topology layer"],
        ["regional comparison", "Ch. 8", "NORMALIZE_AND_EXPAND", "four common-boundary views"],
        ["implications", "Ch. 9", "NEW_SYNTHESIS", "traceable actors, horizons and data gaps"],
        ["conclusions/limitations", "Ch. 10–11", "SEPARATE", "integrated conclusion followed by limits and data agenda"],
    ]
    pd.DataFrame(migration, columns=["legacy_surface", "new_home", "action", "reason"]).to_csv(ROOT / "editorial/CONTENT_MIGRATION_MATRIX_v0.10.0.csv", index=False)


def write_input_register(baseline_zip: Path | None) -> None:
    rows = [
        ["BASELINE_V083", "argentina_electricity_transition_v0.8.3(3).zip", "dc5f5348f5f82f78ec252cbc607703543f7186702bea790c6606c329e30749dc", 84190072, "baseline científico canónico", "VERIFIED_USED", "801 ZIP entries; internal manifest PASS"],
        ["AUTHOR_LETTER", "Carta a IA(2).odt", "829f571e4f50bd213354f756eff3aa99d1661c1c02e1a053bfd8d027bfa95d7f", 13458, "carta literal", "VERIFIED_USED", "ODT integrity PASS"],
        ["AUTHOR_LETTER_WRONG", "Carta a IA (1).odt", "cf261262d353a791d9b2f57edd48cd93e179a6be60f0457677a97d5579fd17f4", 13211, "copia no autorizada", "IGNORED_HASH_MISMATCH", "not used"],
        ["ALMAMDI", "1 - AlmaMDI NODOS 30-01-2024(1).zip", "0b83a7fa3a1916c550289ca0adb7af59d0257d8361a797bc0b3ffcc591e33f9a", 62156, "nodos y coordenadas", "VERIFIED_USED_WITH_LIMITS", "411 rows; 408 coordinates; categories not interpreted"],
        ["CAM_GEOSADI", "GEOSADI2026_08(1).pdf", "506f2392268044c2ada2c440fe9d3eee6f778757933d66f372e39c6c0b666c65", 1587266, "topología e infraestructura visible", "VERIFIED_USED", "2026-08"],
        ["CAM_500_330", "Red de 500 y 330 kV-A4(1).pdf", "970921536b9922ff731d74c973dd7fcd04f6c0e240caef2dc818602ba31ac678", 212905, "validación red troncal", "VERIFIED_USED", "2026-08"],
        ["CAM_GBA", "UNIFILAR-GBA (A3)(1).pdf", "533c7028330b37b9e7426d3b298dc56edd7cb9d94d204aa8ee317c21a4887ba1", 702641, "topología regional", "VERIFIED_USED", "2026-08"],
        ["CAM_BAS", "UNIFILAR-BAS (A3)(1).pdf", "093eadc5247c6579aed7647cdf93c83a4b37401c34b006280d8ac07c40f15d95", 321947, "topología regional", "VERIFIED_USED", "2026-08"],
        ["CAM_CUY", "UNIFILAR-CUY (A3)(1).pdf", "c87e111b701f26e71de50534d01359eae8bb4ca7a58eec4d67e629d139863c9c", 274447, "topología regional", "VERIFIED_USED", "2026-08"],
        ["CAM_COM", "UNIFILAR-COM (A3)(1).pdf", "0d3e05aacc05034612af00ba0fc97b3555e5309d34f5b01b8051dad9b6b1694f", 274591, "topología regional", "VERIFIED_USED", "2026-08"],
        ["CAM_PAT", "UNIFILAR-PAT (A3)(1).pdf", "70526a03a099ad9cdec571d83fa30e6dd5dd4be3ae557bf2e27fa5f82d661eba", 275626, "topología regional", "VERIFIED_USED", "2026-08"],
        ["V090_PDF", "PANORAMA_ELECTRICIDAD_ARGENTINA_2025_v0.9.0_REVISION_EDITORIAL.pdf", "16edca8f924a4102dbbaa624b739ab5493a000ab587c25f1a68d68ad749f053e", 2364679, "referencia visual opcional", "VISUAL_REFERENCE_ONLY", "no scientific authority"],
        ["V090_ZIP", "argentina_electricity_transition_v0.9.0.zip", "1a3ef5478f6f5554de4fffe197def693effdf1323c447760bf661e4f39cb9bee", 25281905, "fuentes visuales y tipografías", "FONTS_ONLY", "scientific contents not used"],
        ["MASTER_PROMPT", "PROMPT_MAESTRO_TGCP_v0.10.0_REESCRITURA_INTEGRAL_Y_EXPANSION_ESTRATEGICA(1).md", "13b53787cd2fdf82e78b7adbe4119635b68d231c3113c7c17fc10f3786bb2769", 67503, "contrato de ejecución", "VERIFIED_USED", "binding instruction"],
    ]
    pd.DataFrame(rows, columns=["input_id", "filename", "sha256", "bytes", "role", "status", "integrity_or_limit"]).to_csv(ROOT / "provenance/INPUT_REGISTER_v0.10.0.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-root", type=Path, required=True, help="Extracted verified v0.8.3 root")
    parser.add_argument("--baseline-zip", type=Path, help="Optional baseline ZIP for external hash verification")
    args = parser.parse_args()
    if args.baseline_zip and sha256(args.baseline_zip) != EXPECTED_BASELINE_SHA256:
        raise SystemExit("Baseline ZIP hash mismatch")
    baseline = args.baseline_root.resolve()
    if not (baseline / "MANIFEST.sha256").exists():
        raise SystemExit("Baseline root does not look like v0.8.3")
    prepare_baseline_tables(baseline)
    prepare_geography()
    prepare_regional()
    prepare_scenario(baseline)
    prepare_strategy()
    write_editorial_tables()
    write_input_register(args.baseline_zip)
    print("Prepared v0.10.0 data surface")


if __name__ == "__main__":
    main()
