#!/usr/bin/env python3
"""Generate the 28 publication figures and four official-source maps for v0.10.0."""

from __future__ import annotations

import json
import math
import os
import re
import time
from pathlib import Path

import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "figures/data"
PNG = ROOT / "figures/png"
VECTOR = ROOT / "figures/vector"
PROCESSED = ROOT / "network/processed"

NAVY = "#123B4A"
TEAL = "#188B86"
MINT = "#58B9AA"
GOLD = "#D9A441"
ORANGE = "#D8684A"
PURPLE = "#655777"
BLUE = "#3A6F8F"
SKY = "#79A9C2"
GREY = "#66757C"
LIGHT = "#EDF3F2"
DARK = "#203037"
RED = "#B84C45"

SOURCE_SHORT = "Fuente: elaboración propia sobre la base científica canónica v0.8.3, salvo indicación distinta."
REGISTER: list[dict] = []


for font in (ROOT / "editorial/fonts").glob("*.ttf"):
    fm.fontManager.addfont(font)

mpl.rcParams.update(
    {
        "font.family": "Source Sans 3",
        "font.size": 9.3,
        "axes.titlesize": 14,
        "axes.titleweight": "semibold",
        "axes.labelsize": 9.5,
        "axes.labelcolor": DARK,
        "axes.edgecolor": "#9FB0B5",
        "axes.linewidth": 0.7,
        "xtick.color": DARK,
        "ytick.color": DARK,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "legend.frameon": False,
        "svg.fonttype": "none",
    }
)


def es_num(value: float, decimals: int = 1) -> str:
    s = f"{value:,.{decimals}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def es_axis(decimals=0, suffix=""):
    return FuncFormatter(lambda x, _: f"{es_num(x, decimals)}{suffix}")


def clean_axes(ax, grid="y"):
    ax.spines[["top", "right"]].set_visible(False)
    if grid:
        ax.grid(axis=grid, color="#DCE5E7", lw=0.7, zorder=0)
    ax.set_axisbelow(True)


def title(ax, text: str, subtitle: str | None = None):
    ax.set_title(text, loc="left", color=NAVY, pad=10)
    if subtitle:
        ax.text(0, 1.01, subtitle, transform=ax.transAxes, ha="left", va="bottom", color=GREY, fontsize=8.5)


def footer(fig, text=SOURCE_SHORT):
    fig.text(0.01, 0.006, text, ha="left", va="bottom", fontsize=6.7, color=GREY)


def save(fig, fid: str, chart_title: str, chapter: int, purpose: str, source: str, *, map_flag=False, dpi=300):
    fig.tight_layout(rect=(0.01, 0.027, 0.99, 0.985))
    png_final = PNG / f"{fid}.png"
    png_tmp = PNG / f".{fid}.png.tmp"
    last_error = None
    for attempt in range(4):
        try:
            fig.savefig(png_tmp, format="png", dpi=dpi, bbox_inches="tight", facecolor="white")
            with Image.open(png_tmp) as check:
                check.load()
            os.replace(png_tmp, png_final)
            last_error = None
            break
        except Exception as exc:
            last_error = exc
            png_tmp.unlink(missing_ok=True)
            time.sleep(0.15 * (attempt + 1))
    if last_error is not None:
        raise RuntimeError(f"No se pudo escribir un PNG íntegro para {fid}") from last_error

    svg_final = VECTOR / f"{fid}.svg"
    svg_tmp = VECTOR / f".{fid}.svg.tmp"
    fig.savefig(svg_tmp, format="svg", bbox_inches="tight", facecolor="white")
    if "</svg>" not in svg_tmp.read_text(encoding="utf-8"):
        raise RuntimeError(f"SVG incompleto para {fid}")
    os.replace(svg_tmp, svg_final)
    plt.close(fig)
    REGISTER.append(
        {
            "figure_id": fid,
            "title_es": chart_title,
            "chapter": chapter,
            "purpose": purpose,
            "data_source": source,
            "png": f"figures/png/{fid}.png",
            "vector": f"figures/vector/{fid}.svg",
            "map_flag": "YES" if map_flag else "NO",
            "publication_status": "PASS",
        }
    )


def fig01_system_checkpoints():
    d = pd.read_csv(DATA / "annual_accounting_bridge_2005_2025.csv")
    d = d[d.year.isin([2005, 2012, 2018, 2025])].set_index("year") / 1000
    cols = ["thermal_gwh", "large_hydro_gwh", "nuclear_gwh", "law_renewables_gwh", "imports_gwh"]
    labels = ["Térmica", "Gran hidráulica", "Nuclear", "Renovables legales", "Importaciones"]
    colors = [ORANGE, BLUE, PURPLE, TEAL, GOLD]
    fig, ax = plt.subplots(figsize=(9.8, 5.8))
    bottom = np.zeros(len(d))
    x = np.arange(len(d))
    for c, lab, color in zip(cols, labels, colors):
        vals = d[c].to_numpy()
        ax.bar(x, vals, bottom=bottom, label=lab, color=color, width=0.64, edgecolor="white", lw=0.5)
        bottom += vals
    for i, total in enumerate(bottom):
        ax.text(i, total + 2.5, f"{es_num(total, 1)} TWh", ha="center", va="bottom", weight="semibold", color=NAVY)
    ax.set_xticks(x, ["2005\nexpansión de demanda", "2012\npunto de comparación", "2018\ndespegue renovable", "2025\nnuevo equilibrio"])
    ax.set_ylabel("Oferta total (TWh)")
    ax.set_ylim(0, max(bottom) * 1.17)
    ax.yaxis.set_major_formatter(es_axis(0))
    ax.legend(ncol=3, loc="upper left")
    clean_axes(ax)
    title(ax, "Cuatro cortes de un sistema que cambió de escala y composición", "Oferta total: generación local por fuente más importaciones")
    footer(fig)
    save(fig, "F01", "Cuatro cortes del sistema eléctrico", 1, "abrir la secuencia 2005–2025", "CAMMESA, Estadísticas anuales 2005–2025")


def fig02_supply_bridge():
    d = pd.read_csv(DATA / "supply_change_bridge_2018_2025.csv")
    d = d[~d.component.eq("net_supply_change")]
    vals = d.change_twh.to_numpy()
    labels = d.label_es.tolist()
    starts = np.r_[0, np.cumsum(vals)[:-1]]
    ends = np.cumsum(vals)
    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    for i, (s, v, lab) in enumerate(zip(starts, vals, labels)):
        y = min(s, s + v)
        h = abs(v)
        patch = FancyBboxPatch((i - 0.33, y), 0.66, h, boxstyle="round,pad=0.015,rounding_size=0.12", facecolor=TEAL if v >= 0 else ORANGE, edgecolor="none", zorder=3)
        ax.add_patch(patch)
        ax.plot([i + 0.33, i + 0.67], [s + v, s + v], color="#9FB0B5", lw=0.9, zorder=2)
        ax.text(i, s + v + (0.8 if v >= 0 else -0.8), f"{v:+.1f}", ha="center", va="bottom" if v >= 0 else "top", weight="semibold", color=DARK)
    total = vals.sum()
    patch = FancyBboxPatch((len(vals) - 0.18, min(0, total)), 0.74, abs(total), boxstyle="round,pad=0.015,rounding_size=0.12", facecolor=NAVY, edgecolor="none", zorder=3)
    ax.add_patch(patch)
    ax.text(len(vals) + 0.19, total + 0.8, f"{total:+.1f}", ha="center", weight="bold", color=NAVY)
    ax.axhline(0, color=DARK, lw=0.8)
    ax.set_xlim(-0.7, len(vals) + 0.8)
    ax.set_ylim(min(ends.min(), 0) - 4, max(ends.max(), total) + 5)
    ax.set_xticks(list(range(len(vals))) + [len(vals) + 0.19], labels + ["Cambio neto"])
    ax.tick_params(axis="x", rotation=18)
    ax.set_ylabel("Contribución al cambio (TWh)")
    clean_axes(ax)
    title(ax, "El crecimiento renovable compensó dos retrocesos importantes", "Puente contable 2018–2025; las cajas muestran contribuciones, no causas")
    footer(fig)
    save(fig, "F02", "Puente contable de la oferta 2018–2025", 1, "separar contribuciones al cambio", "CAMMESA; base científica canónica v0.8.3")


def fig03_energy_peak_load_factor():
    d = pd.read_csv(DATA / "annual_demand_balance_2012_2025.csv")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.9), gridspec_kw={"width_ratios": [1.25, 1]})
    ax1.plot(d.year, d.local_demand_gwh / 1000, color=NAVY, lw=2.3, marker="o", ms=4)
    ax1.set_ylabel("Demanda local (TWh)")
    ax1b = ax1.twinx()
    ax1b.plot(d.year, d.peak_mw / 1000, color=ORANGE, lw=2.3, marker="s", ms=3.8)
    ax1b.set_ylabel("Punta instantánea (GW)", color=ORANGE)
    ax1b.tick_params(axis="y", colors=ORANGE)
    clean_axes(ax1)
    ax1.set_title("Energía y punta", loc="left", color=NAVY, weight="semibold")
    ax2.plot(d.year, d.calculated_load_factor * 100, color=TEAL, lw=2.4, marker="o", ms=4)
    ax2.axhline(d.loc[d.year.eq(2018), "calculated_load_factor"].iloc[0] * 100, color="#A9B6BA", ls="--", lw=1)
    ax2.set_ylabel("Factor de carga (%)")
    ax2.set_ylim(50, 68)
    clean_axes(ax2)
    ax2.set_title("Uso menos parejo de la punta", loc="left", color=NAVY, weight="semibold")
    fig.suptitle("La punta crece más rápido que la energía", x=0.02, ha="left", color=NAVY, fontsize=14, weight="semibold")
    fig.text(0.02, 0.93, "Entre 2018 y 2025: demanda +6,2 %; punta +15,0 %; factor de carga −4,43 pp", color=GREY, fontsize=8.7)
    footer(fig)
    save(fig, "F03", "Demanda, punta y factor de carga", 3, "mostrar divergencia entre energía y capacidad", "CAMMESA; base científica canónica v0.8.3")


def fig04_demand_composition():
    d = pd.read_csv(DATA / "demand_components_2012_2025.csv")
    fig, ax = plt.subplots(figsize=(9.8, 5.1))
    ax.stackplot(d.year, d.residential_gwh / 1000, d.commercial_gwh / 1000, d.large_demand_gwh / 1000, labels=["Residencial", "Comercial", "Grandes demandas"], colors=[SKY, MINT, PURPLE], alpha=0.95)
    ax.set_ylabel("Demanda local (TWh)")
    ax.legend(ncol=3, loc="upper left")
    clean_axes(ax)
    title(ax, "El volumen anual combina perfiles de consumo distintos", "La composición sirve para pensar instrumentos; no sustituye curvas horarias por usuario")
    footer(fig)
    save(fig, "F04", "Composición de la demanda local", 3, "diferenciar usos detrás del total anual", "CAMMESA; base científica canónica v0.8.3")


def fig05_duration_curve():
    d = pd.read_csv(DATA / "hourly_demand_duration_curve_2023_2025.csv.gz")
    fig, ax = plt.subplots(figsize=(9.8, 5.3))
    for year, color in zip([2023, 2024, 2025], [SKY, TEAL, NAVY]):
        g = d[d.year.eq(year)]
        ax.plot(g.exceedance_fraction * 100, g.load_mwh / 1000, color=color, lw=2, label=str(year))
    ax.set_xlabel("Porcentaje de horas con demanda igual o mayor")
    ax.set_ylabel("Demanda horaria (GW medios)")
    ax.set_xlim(0, 100)
    ax.legend(title="Año")
    clean_axes(ax)
    title(ax, "La curva de duración separa las pocas horas críticas del resto del año", "Ordena horas de mayor a menor; no conserva la secuencia temporal")
    footer(fig)
    save(fig, "F05", "Curva de duración de la demanda horaria", 3, "explicar duración y rareza de puntas", "CAMMESA, oferta horaria 2023–2025")


def fig06_top_hours_dispatch():
    d = pd.read_csv(DATA / "top_demand_hours_dispatch_summary_2023_2025.csv")
    d = d[d.top_n_demand_hours.eq(100)].copy()
    parts = ["mean_thermal_mwh", "mean_large_hydro_mwh", "mean_nuclear_mwh", "mean_wind_mwh", "mean_solar_mwh", "mean_other_renewables_mwh", "mean_net_imports_mwh"]
    labels = ["Térmica", "Gran hidro", "Nuclear", "Eólica", "Solar", "Otras renovables", "Importación neta"]
    colors = [ORANGE, BLUE, PURPLE, TEAL, GOLD, MINT, GREY]
    shares = np.array([d[p].to_numpy() / d.mean_load_mwh.to_numpy() * 100 for p in parts])
    fig, ax = plt.subplots(figsize=(9.6, 5.2))
    bottom = np.zeros(len(d))
    for s, lab, color in zip(shares, labels, colors):
        ax.bar(d.year.astype(str), s, bottom=bottom, label=lab, color=color, edgecolor="white", lw=0.4, width=0.58)
        bottom += s
    ax.set_ylabel("Participación media en las 100 horas de mayor demanda (%)")
    ax.set_ylim(0, max(105, bottom.max() + 3))
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.1))
    clean_axes(ax)
    title(ax, "En las horas de mayor demanda, la generación térmica sigue siendo central", "Promedios de las 100 horas de mayor demanda de cada año")
    footer(fig)
    save(fig, "F06", "Despacho medio en las 100 horas de mayor demanda", 3, "vincular punta con composición horaria", "CAMMESA; base científica canónica v0.8.3")


def fig07_ramps():
    d = pd.read_csv(DATA / "hourly_ramp_summary_2023_2025.csv")
    d = d[d["sample"].eq("all_observed")].copy()
    fig, ax = plt.subplots(figsize=(9.8, 5.1))
    x = np.arange(3)
    width = 0.33
    load = d[d.metric.eq("load")].sort_values("year")
    net = d[d.metric.eq("net_load")].sort_values("year")
    ax.bar(x - width / 2, load.p99_ramp_mwh_per_h / 1000, width, color=SKY, label="Demanda")
    ax.bar(x + width / 2, net.p99_ramp_mwh_per_h / 1000, width, color=TEAL, label="Carga neta")
    for xx, vals in [(x - width / 2, load.p99_ramp_mwh_per_h / 1000), (x + width / 2, net.p99_ramp_mwh_per_h / 1000)]:
        for xi, v in zip(xx, vals): ax.text(xi, v + 0.035, es_num(v, 2), ha="center", fontsize=8, weight="semibold")
    ax.set_xticks(x, load.year.astype(str))
    ax.set_ylabel("Percentil 99 de la rampa ascendente (GW/h)")
    ax.legend()
    ax.set_ylim(0, 2.35)
    clean_axes(ax)
    title(ax, "La variabilidad relevante aparece en cuánto cambia la carga de una hora a la siguiente", "Carga neta = demanda − eólica − solar; percentil 99, no máximo excepcional")
    footer(fig)
    save(fig, "F07", "Rampas horarias de demanda y carga neta", 3, "mostrar necesidad de flexibilidad", "CAMMESA; base científica canónica v0.8.3")


def fig08_renewable_growth():
    cap = pd.read_csv(DATA / "renewable_capacity_by_technology_2012_2025.csv")
    gen = pd.read_csv(DATA / "renewable_generation_by_technology_2012_2025.csv")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.9))
    cap_cols = ["wind_mw_december", "solar_mw_december", "biomass_mw_december", "biogas_mw_december", "small_hydro_mw_december"]
    gen_cols = ["wind_gwh", "solar_gwh", "biomass_gwh", "biogas_gwh", "small_hydro_gwh"]
    labels = ["Eólica", "Solar", "Biomasa", "Biogás", "Pequeña hidro"]
    colors = [TEAL, GOLD, MINT, PURPLE, BLUE]
    ax1.stackplot(cap.year, *[cap[c] / 1000 for c in cap_cols], colors=colors, labels=labels)
    ax1.set_ylabel("Potencia a diciembre (GW)"); clean_axes(ax1); ax1.set_title("Potencia", loc="left", color=NAVY, weight="semibold")
    ax2.stackplot(gen.year, *[gen[c] / 1000 for c in gen_cols], colors=colors, labels=labels)
    ax2.set_ylabel("Generación anual (TWh)"); clean_axes(ax2); ax2.set_title("Generación", loc="left", color=NAVY, weight="semibold")
    ax2.legend(ncol=2, loc="upper left")
    fig.suptitle("La expansión renovable fue, sobre todo, eólica y luego solar", x=0.02, ha="left", color=NAVY, fontsize=14, weight="semibold")
    footer(fig)
    save(fig, "F08", "Potencia y generación renovable por tecnología", 4, "distinguir capacidad de energía", "CAMMESA, base renovable y estadísticas anuales")


def fig09_programs():
    d = pd.read_csv(DATA / "renewable_generation_by_program_2012_2025.csv")
    d = d[d.year.ge(2017)]
    groups = ["Resto/legado", "Renovar 202 (etiqueta CAMMESA)", "RenovAr", "MATER y variantes", "RenMDI", "Otra etiqueta CAMMESA"]
    colors = [GREY, SKY, TEAL, GOLD, PURPLE, MINT]
    fig, ax = plt.subplots(figsize=(9.8, 5.2))
    ax.stackplot(d.year, *[d[c] / 1000 for c in groups], labels=groups, colors=colors)
    ax.set_ylabel("Generación renovable (TWh)")
    ax.legend(ncol=3, loc="upper left", fontsize=8)
    clean_axes(ax)
    title(ax, "RenovAr y MATER terminaron aportando volúmenes parecidos por caminos distintos", "Etiquetas CAMMESA; la atribución es contable y depende del registro de proyecto")
    footer(fig)
    save(fig, "F09", "Generación renovable por programa", 4, "mostrar coexistencia de instrumentos", "CAMMESA, base de renovables 2026-06")


def fig10_peak_weather():
    d = pd.read_csv(DATA / "annual_peak_weather_sensitivity_v083.csv")
    fig, ax = plt.subplots(figsize=(9.5, 5.3))
    colors = {s: c for s, c in zip(d.scenario.unique(), [NAVY, ORANGE, TEAL])}
    scenario_labels = {
        "ba_province_centroid_proxy": "Centroide bonaerense",
        "caba_point_proxy_extreme": "Punto CABA (extremo)",
        "caba80_ba_interior20_proxy": "Mezcla CABA 80 / interior 20",
    }
    for s, g in d.groupby("scenario"):
        ax.scatter(g.load_weighted_cooling_excess_hourly_c, g.load_gwh, s=58, color=colors[s], label=scenario_labels[s], alpha=0.88)
    for year, g in d.groupby("year"):
        ax.text(g.load_weighted_cooling_excess_hourly_c.mean(), g.load_gwh.iloc[0] + 0.025, str(int(year)), fontsize=7.5, color=DARK, ha="center")
    ax.set_xlabel("Exceso térmico horario ponderado por demanda (°C)")
    ax.set_ylabel("Demanda en la hora pico (GW)")
    ax.legend(fontsize=7.5, loc="lower right")
    clean_axes(ax)
    title(ax, "Las horas pico coinciden con calor intenso, pero la geografía meteorológica importa", "Sensibilidad entre proxies; asociación descriptiva, no efecto causal del clima")
    footer(fig, "Fuente: CAMMESA y NASA POWER; escenarios geográficos heredados y auditados en v0.8.3.")
    save(fig, "F10", "Punta y exceso térmico horario", 3, "explicar sensibilidad meteorológica sin causalidad", "CAMMESA; NASA POWER; base científica canónica v0.8.3")


def fig11_hydro_trajectory():
    d = pd.read_csv(DATA / "large_hydro_annual_2018_2025.csv")
    fig, ax = plt.subplots(figsize=(9.8, 5.2))
    for col, lab, color in [("yacyreta", "Yacyretá (asignación argentina)", BLUE), ("comahue", "Comahue", TEAL), ("salto_grande", "Salto Grande (asignación argentina)", GOLD), ("rest", "Resto", GREY)]:
        ax.plot(d.year, d[col] / 1000, marker="o", ms=3.8, lw=2, color=color, label=lab)
    ax.set_ylabel("Generación (TWh)")
    ax.legend(ncol=2, loc="upper center")
    clean_axes(ax)
    title(ax, "La caída hidráulica no tiene una sola historia", "La asignación argentina de binacionales no equivale a producción física total")
    footer(fig)
    save(fig, "F11", "Trayectorias de la gran hidráulica", 5, "separar complejos y fronteras", "CAMMESA; base científica canónica v0.8.3")


def fig12_yacyreta_decomposition():
    d = pd.read_csv(DATA / "binational_allocation_decomposition_2018_2025.csv")
    r = d[d.plant.str.contains("Yacy")].iloc[0]
    vals = [r.production_effect_gwh / 1000, r.allocation_effect_gwh / 1000]
    labels = ["Menor producción\nfísica", "Menor fracción\nasignada a Argentina"]
    fig, ax = plt.subplots(figsize=(8.8, 4.9))
    bars = ax.bar(labels, vals, color=[BLUE, PURPLE], width=0.58)
    for b, v in zip(bars, vals): ax.text(b.get_x() + b.get_width() / 2, v - 0.12, f"{v:.2f} TWh".replace(".", ","), ha="center", va="top", color="white", weight="bold")
    ax.axhline(0, color=DARK, lw=0.8)
    ax.text(0.5, min(vals) - 0.35, f"Cambio observado: {r.observed_change_gwh/1000:.2f} TWh".replace(".", ","), ha="center", color=NAVY, weight="semibold")
    ax.set_ylabel("Contribución 2018–2025 (TWh)")
    clean_axes(ax)
    title(ax, "Yacyretá cayó por producción y por asignación", "Descomposición exacta de Shapley; identifica contribuciones contables, no causas hidrológicas finales")
    footer(fig)
    save(fig, "F12", "Descomposición de Yacyretá 2018–2025", 5, "separar producción de reparto binacional", "CAMMESA; método Shapley")


def fig13_comahue():
    d = pd.read_csv(DATA / "comahue_annual_indicators_2018_2025.csv")
    fig, ax = plt.subplots(figsize=(9.8, 5.2))
    ax.bar(d.year, d.generation_gwh / 1000, color=BLUE, alpha=0.85, label="Generación")
    ax.set_ylabel("Generación (TWh)")
    ax2 = ax.twinx()
    ax2.plot(d.year, d.availability_pct * 100, color=TEAL, marker="o", lw=2, label="Disponibilidad")
    ax2.plot(d.year, d.utilization_pct * 100, color=ORANGE, marker="s", lw=2, label="Utilización")
    ax2.set_ylabel("Indicador (%)")
    handles = [mpl.patches.Patch(color=BLUE, label="Generación")] + ax2.lines
    ax.legend(handles, [h.get_label() for h in handles], ncol=3, loc="upper center")
    clean_axes(ax)
    title(ax, "En Comahue, disponibilidad y utilización cuentan historias distintas", "Disponibilidad es aptitud de equipos; utilización combina agua, despacho y restricciones")
    footer(fig)
    save(fig, "F13", "Generación, disponibilidad y utilización en Comahue", 5, "evitar atribuir toda caída a equipos", "CAMMESA; base científica canónica v0.8.3")


def fig14_thermal_emissions():
    d = pd.read_csv(DATA / "annual_thermal_emissions_indicators_2018_2025.csv")
    fig, ax = plt.subplots(figsize=(9.8, 5.2))
    ax.plot(d.year, d.thermal_total_gwh / 1000, color=ORANGE, lw=2.5, marker="o", label="Generación térmica")
    ax.set_ylabel("Generación térmica (TWh)", color=ORANGE); ax.tick_params(axis="y", colors=ORANGE)
    ax2 = ax.twinx(); ax2.plot(d.year, d.emissions_mt, color=NAVY, lw=2.5, marker="s", label="Emisiones directas")
    ax2.set_ylabel("Emisiones directas (MtCO₂)", color=NAVY); ax2.tick_params(axis="y", colors=NAVY)
    clean_axes(ax)
    title(ax, "Menos generación térmica redujo las emisiones directas, con altibajos", "Inventario contable del parque térmico; no incluye ciclo de vida")
    footer(fig)
    save(fig, "F14", "Generación térmica y emisiones directas", 6, "vincular energía térmica con emisiones", "CAMMESA; base científica canónica v0.8.3")


def fig15_lmdi():
    d = pd.read_csv(DATA / "lmdi_direct_absolute_2018_2025.csv")
    order = ["activity", "thermal_share", "specific_fuel_consumption", "fuel_mix", "emission_factor"]
    labels = ["Actividad", "Participación\ntérmica", "Consumo específico", "Mezcla de\ncombustibles", "Factor de\nemisión"]
    vals = [float(d.loc[d.effect.eq(o), "value"].iloc[0]) for o in order]
    starts = np.r_[0, np.cumsum(vals)[:-1]]
    fig, ax = plt.subplots(figsize=(9.8, 5.2))
    for i, (s, v) in enumerate(zip(starts, vals)):
        ax.bar(i, v, bottom=s, color=ORANGE if v > 0 else TEAL, width=0.62)
        ax.plot([i + 0.31, i + 0.69], [s + v, s + v], color="#9FB0B5", lw=0.8)
        ax.text(i, s + v + (0.25 if v > 0 else -0.25), f"{v:+.2f}".replace(".", ","), ha="center", va="bottom" if v > 0 else "top", fontsize=8, weight="semibold")
    total = sum(vals); ax.bar(len(vals), total, color=NAVY, width=0.68); ax.text(len(vals), total - 0.3, f"{total:+.2f}".replace(".", ","), ha="center", va="top", color="white", weight="bold")
    ax.set_xticks(range(len(vals) + 1), labels + ["Cambio total"])
    ax.set_ylabel("Contribución al cambio (MtCO₂)")
    ax.axhline(0, color=DARK, lw=0.8); clean_axes(ax)
    title(ax, "La menor participación térmica fue el factor dominante de la caída de emisiones", "Descomposición LMDI 2018–2025; suma exacta de efectos contables")
    footer(fig)
    save(fig, "F15", "Descomposición LMDI de emisiones", 6, "explicar factores detrás del cambio", "CAMMESA; método Ang (2005)")


def fig16_hourly_association():
    d = pd.read_csv(DATA / "iv_estimates_side_by_side.csv")
    d = d[d.outcome.eq("thermal_gwh")].copy()
    labels = []
    for _, r in d.iterrows():
        design = "Principal" if r.design == "inherited_hourly" else "Dinámico"
        labels.append(f"{design} · {'eólica' if r.variable == 'wind_gwh' else 'solar'}")
    y = np.arange(len(d))[::-1]
    fig, ax = plt.subplots(figsize=(9.5, 5.0))
    ax.errorbar(d.coefficient, y, xerr=[d.coefficient - d.ci_low, d.ci_high - d.coefficient], fmt="o", ms=7, color=NAVY, ecolor=TEAL, capsize=4, lw=1.8)
    ax.axvline(0, color=GREY, lw=0.9)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Asociación condicional: Δ térmica por MWh renovable (MWh/MWh)")
    clean_axes(ax, "x")
    title(ax, "Las asociaciones horarias son negativas, pero no equivalen a una ley física de desplazamiento", "Estimaciones IV con intervalos de confianza 95 %; diseños y diagnósticos completos en el anexo")
    footer(fig)
    save(fig, "F16", "Asociación horaria entre renovables y generación térmica", 6, "comunicar estimaciones con cautela causal", "CAMMESA; NASA POWER; base científica canónica v0.8.3")


def fig17_trade():
    d = pd.read_csv(DATA / "annual_exchange_metrics_2012_2025.csv")
    fig, ax = plt.subplots(figsize=(9.8, 5.1))
    ax.plot(d.year, d.gross_trade_gwh / 1000, color=GOLD, lw=2.3, marker="o", label="Comercio bruto")
    ax.plot(d.year, d.net_imports_gwh / 1000, color=NAVY, lw=2.3, marker="s", label="Saldo neto importador")
    ax.fill_between(d.year, 0, d.net_imports_gwh / 1000, color=SKY, alpha=0.25)
    ax.axhline(0, color=DARK, lw=0.8)
    ax.set_ylabel("Energía (TWh)"); ax.legend(); clean_axes(ax)
    title(ax, "Comercio bruto y saldo neto responden preguntas diferentes", "Bruto = importaciones + exportaciones; saldo = importaciones − exportaciones")
    footer(fig)
    save(fig, "F17", "Intercambios eléctricos internacionales", 8, "distinguir volumen de saldo", "CAMMESA; base científica canónica v0.8.3")


def merc(lon, lat):
    origin = 20037508.342789244
    x = np.asarray(lon, dtype=float) * origin / 180.0
    lat = np.clip(np.asarray(lat, dtype=float), -85.0511, 85.0511)
    y = np.log(np.tan((90 + lat) * math.pi / 360.0)) * origin / math.pi
    return x, y


def load_map_data():
    provinces = json.loads((PROCESSED / "provincias_IGN_simplificadas.geojson").read_text(encoding="utf-8"))
    lines = json.loads((PROCESSED / "lineas_AT_energia_2026.geojson").read_text(encoding="utf-8"))
    bounds = json.loads((PROCESSED / "argenmap_topo_z5_bounds.json").read_text(encoding="utf-8"))
    relief = Image.open(PROCESSED / "argenmap_topo_z5_mosaic.png").convert("RGB")
    return provinces, lines, bounds, relief


def map_setup(ax, provinces, bounds, relief, alpha=0.24):
    ax.imshow(relief, extent=[bounds["xmin"], bounds["xmax"], bounds["ymin"], bounds["ymax"]], origin="upper", alpha=alpha, zorder=0)
    for f in provinces["features"]:
        for poly in f["geometry"]["coordinates"]:
            for ring in poly:
                arr = np.asarray(ring)
                x, y = merc(arr[:, 0], arr[:, 1])
                ax.plot(x, y, color="#6D858B", lw=0.45, alpha=0.85, zorder=3)
    xmin, ymin = merc(-74.5, -55.4); xmax, ymax = merc(-52.3, -20.5)
    ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax); ax.set_aspect("equal"); ax.axis("off")


def line_coords(geometry):
    if geometry["type"] == "LineString": return [geometry["coordinates"]]
    if geometry["type"] == "MultiLineString": return geometry["coordinates"]
    return []


def draw_grid(ax, lines, levels=(500, 345, 330, 220), alpha=0.8, highlight=None):
    for f in lines["features"]:
        voltage = f["properties"].get("tension")
        try: voltage = int(float(voltage))
        except Exception: continue
        if voltage not in levels: continue
        name = str(f["properties"].get("nombre") or "")
        if highlight is not None and not highlight(name, voltage): continue
        color = PURPLE if voltage >= 330 else GOLD
        lw = 1.25 if voltage >= 330 else 0.75
        for coords in line_coords(f["geometry"]):
            arr = np.asarray(coords)
            x, y = merc(arr[:, 0], arr[:, 1])
            ax.plot(x, y, color=color, lw=lw, alpha=alpha, zorder=4)


def fill_provinces(ax, provinces, values, cmap, norm):
    for f in provinces["features"]:
        n = f["properties"]["name"]
        key = "Buenos Aires + CABA" if n in ("Buenos Aires", "Ciudad Autónoma de Buenos Aires") else n
        value = values.get(key)
        face = "#F3F5F4" if value is None or pd.isna(value) else cmap(norm(value))
        for poly in f["geometry"]["coordinates"]:
            for ring in poly:
                arr = np.asarray(ring); x, y = merc(arr[:, 0], arr[:, 1])
                ax.fill(x, y, facecolor=face, edgecolor="white", lw=0.35, zorder=1)


def fig18_map_infrastructure():
    provinces, lines, bounds, relief = load_map_data()
    plants = pd.read_csv(PROCESSED / "centrales_IGN.csv")
    fig, ax = plt.subplots(figsize=(7.5, 9.2))
    map_setup(ax, provinces, bounds, relief, 0.32); draw_grid(ax, lines)
    categories = [
        ("Eólica", plants.technology_label.fillna("").str.contains("Eólic|Eolic", case=False), TEAL, "^"),
        ("Solar", plants.technology_label.fillna("").str.contains("Solar", case=False), GOLD, "s"),
        ("Hidráulica", plants.technology_label.fillna("").str.contains("Hidro|Hidrá|Hidrol", case=False), BLUE, "o"),
        ("Térmica", plants.technology_label.fillna("").str.contains("Térm|Termo|Usina", case=False), ORANGE, "."),
        ("Nuclear", plants.technology_label.fillna("").str.contains("Nuclear", case=False), PURPLE, "D"),
    ]
    handles = []
    for lab, mask, color, marker in categories:
        g = plants[mask & plants.latitude.between(-55.5, -20) & plants.longitude.between(-75, -52)]
        x, y = merc(g.longitude, g.latitude)
        ax.scatter(x, y, s=18 if marker != "." else 12, marker=marker, color=color, edgecolors="white", linewidths=0.3, alpha=0.9, zorder=6)
        handles.append(Line2D([0], [0], marker=marker, color="none", markerfacecolor=color, markeredgecolor="white", markersize=7, label=lab))
    handles += [Line2D([0], [0], color=PURPLE, lw=2, label="500/345/330 kV"), Line2D([0], [0], color=GOLD, lw=1.5, label="220 kV")]
    ax.legend(handles=handles, ncol=2, loc="lower left", bbox_to_anchor=(0.01, 0.01), facecolor="white", frameon=True, framealpha=0.92, fontsize=8)
    title(ax, "Infraestructura y generación: activos visibles, no flujos", "Red 2026; centrales IGN sin escalado por potencia; relieve Argenmap Topo")
    footer(fig, "Fuentes: Secretaría de Energía (líneas AT); IGN (centrales, límites y Argenmap Topo); control visual CAMMESA agosto 2026.")
    save(fig, "M01", "Mapa nacional de infraestructura y generación", 7, "ubicar red y tecnologías sin inferir operación", "Secretaría de Energía; IGN; CAMMESA", map_flag=True, dpi=260)


def fig19_map_demand_generation():
    provinces, _, bounds, relief = load_map_data()
    demand = pd.read_csv(DATA / "provincial_demand_summary_2023_2025.csv")
    ren = pd.read_csv(DATA / "provincial_renewable_summary_2018_2025.csv")
    dv = demand.set_index("province").demand_2025_gwh.to_dict()
    rv = ren.set_index("province").renewable_2025_gwh.to_dict()
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 7.2))
    for ax in axes: map_setup(ax, provinces, bounds, relief, 0.11)
    cmap1, cmap2 = mpl.colormaps["Blues"], mpl.colormaps["YlGn"]
    n1, n2 = Normalize(0, max(dv.values())), Normalize(0, max(rv.values()))
    fill_provinces(axes[0], provinces, dv, cmap1, n1); fill_provinces(axes[1], provinces, rv, cmap2, n2)
    axes[0].set_title("Demanda local 2025", loc="left", color=NAVY, weight="semibold")
    axes[1].set_title("Generación renovable legal 2025", loc="left", color=NAVY, weight="semibold")
    sm1 = mpl.cm.ScalarMappable(norm=n1, cmap=cmap1); sm2 = mpl.cm.ScalarMappable(norm=n2, cmap=cmap2)
    c1 = fig.colorbar(sm1, ax=axes[0], orientation="horizontal", fraction=0.035, pad=0.02); c1.set_label("GWh")
    c2 = fig.colorbar(sm2, ax=axes[1], orientation="horizontal", fraction=0.035, pad=0.02); c2.set_label("GWh")
    fig.suptitle("Dónde se consume y dónde se genera no coincide", x=0.02, ha="left", color=NAVY, fontsize=14, weight="semibold")
    fig.text(0.02, 0.94, "Buenos Aires y CABA conservan una frontera agregada; Tierra del Fuego no está separada en la tabla provincial usada", color=GREY, fontsize=8.4)
    footer(fig, "Fuentes: CAMMESA (demanda provincial y renovables); IGN (límites y relieve). Valores territoriales no representan flujos.")
    save(fig, "M02", "Mapa de demanda y generación renovable", 7, "mostrar desajuste territorial", "CAMMESA; IGN", map_flag=True, dpi=260)


def fig20_map_corridors():
    provinces, lines, bounds, relief = load_map_data()
    fig, (ax, side) = plt.subplots(1, 2, figsize=(10.8, 7.5), gridspec_kw={"width_ratios": [1.65, 1]})
    map_setup(ax, provinces, bounds, relief, 0.24); draw_grid(ax, lines, alpha=0.34)
    wanted = lambda name, v: any(t in name.upper() for t in ["N.P.MADRYN", "PUERTO MADRYN", "CHOELE CHOEL", "B.BLANCA OLAVARRIA", "RIO DIAMANTE", "AGUA DEL CAJON", "PIEDRA DEL AGUILA"])
    draw_grid(ax, lines, alpha=0.98, highlight=wanted)
    ax.set_title("Corredores visibles y refuerzos", loc="left", color=NAVY, weight="semibold")
    side.axis("off")
    cards = [
        ("Patagonia–Buenos Aires", "El trazado oficial 500 kV Puerto Madryn–Choele Choel–Bahía Blanca se muestra como infraestructura existente. El refuerzo fue prioridad administrativa en 2025; avance físico no verificado.", TEAL),
        ("Comahue–centro de carga", "La red 500 kV conecta inyecciones hidroeléctricas con el corredor central. El mapa no contiene capacidad remanente ni dirección de flujo.", BLUE),
        ("Río Diamante–Charlone–O’Higgins", "Corredor planificado. Como los insumos no publican una geometría reconciliada de los nuevos tramos, no se dibuja una línea inventada.", ORANGE),
    ]
    y = 0.92
    for heading, body, color in cards:
        box = FancyBboxPatch((0.02, y - 0.24), 0.95, 0.21, transform=side.transAxes, boxstyle="round,pad=0.018,rounding_size=0.02", facecolor="#F5F8F7", edgecolor=color, lw=1.4)
        side.add_patch(box); side.text(0.06, y - 0.07, heading, transform=side.transAxes, color=color, weight="bold", fontsize=10)
        side.text(0.06, y - 0.115, body, transform=side.transAxes, color=DARK, fontsize=8.2, va="top", wrap=True)
        y -= 0.28
    side.text(0.03, 0.04, "Línea continua: infraestructura oficial.\nNo se dibujan flechas, congestión ni MW.", transform=side.transAxes, color=GREY, fontsize=8, style="italic")
    footer(fig, "Fuentes: Secretaría de Energía (geometría); CAMMESA (topología 2026); actos administrativos 2025 auditados en v0.8.3.")
    save(fig, "M03", "Corredores y ampliaciones regionales", 7, "separar activo existente, prioridad y dato faltante", "Secretaría de Energía; CAMMESA; normativa 2025", map_flag=True, dpi=260)


def fig21_map_almamdi():
    provinces, lines, bounds, relief = load_map_data()
    nodes = pd.read_csv(PROCESSED / "almamdi_nodes_safe.csv").dropna(subset=["latitude", "longitude"])
    fig, ax = plt.subplots(figsize=(7.5, 9.2))
    map_setup(ax, provinces, bounds, relief, 0.21); draw_grid(ax, lines, levels=(500, 345, 330, 220, 132), alpha=0.25)
    regions = sorted(nodes.region.dropna().unique())
    colors = mpl.colormaps["tab10"](np.linspace(0, 1, len(regions)))
    handles = []
    for reg, color in zip(regions, colors):
        g = nodes[nodes.region.eq(reg)]; x, y = merc(g.longitude, g.latitude)
        ax.scatter(x, y, s=13, color=color, edgecolors="white", linewidths=0.25, alpha=0.9, zorder=7)
        handles.append(Line2D([0], [0], marker="o", color="none", markerfacecolor=color, markersize=6, label=f"{reg} · {len(g)}"))
    ax.legend(handles=handles, ncol=2, loc="lower left", bbox_to_anchor=(0.01, 0.01), facecolor="white", frameon=True, framealpha=0.93, fontsize=7.7)
    title(ax, "AlmaMDI: 408 nodos con coordenadas, sin sobreinterpretar categorías", "Se muestran nombre, ubicación, tensión y región; no potencia máxima ni limitaciones sin diccionario oficial")
    footer(fig, "Fuentes: planilla AlmaMDI 30-01-2024 (adjunta); Secretaría de Energía; IGN. Tres registros sin coordenadas no se cartografían.")
    save(fig, "M04", "Cobertura espacial de nodos AlmaMDI", 7, "auditar alcance espacial del insumo nodal", "AlmaMDI; Secretaría de Energía; IGN", map_flag=True, dpi=260)


def fig22_regional_structure():
    d = pd.read_csv(DATA / "regional_normalized_metrics_v010.csv"); d = d[d.year.eq(2025)]
    parts = ["hydro_twh", "wind_twh", "solar_twh", "other_renewables_twh", "nuclear_twh", "fossil_twh"]
    labels = ["Hidro", "Eólica", "Solar", "Otras renovables", "Nuclear", "Fósil"]
    colors = [BLUE, TEAL, GOLD, MINT, PURPLE, ORANGE]
    shares = d[parts].div(d.generation_twh, axis=0) * 100
    fig, ax = plt.subplots(figsize=(9.8, 5.2)); left = np.zeros(len(d))
    for p, lab, color in zip(parts, labels, colors):
        ax.barh(d.country_es, shares[p], left=left, color=color, label=lab, edgecolor="white", lw=0.4); left += shares[p].to_numpy()
    ax.set_xlim(0, 100); ax.set_xlabel("Composición de la generación 2025 (%)"); ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.13)); clean_axes(ax, "x")
    title(ax, "Cuatro estructuras eléctricas distintas en una frontera común", "Generación armonizada Ember/OWID; no confundir con definiciones legales nacionales")
    footer(fig, "Fuente: adaptación OWID de Ember Yearly Electricity Data 2026; controles nacionales preservados por separado.")
    save(fig, "F22", "Estructura regional de generación 2025", 8, "comparar composición con frontera común", "Ember/OWID 2026")


def fig23_regional_change():
    d = pd.read_csv(DATA / "regional_normalized_metrics_v010.csv")
    rows = []
    for c, g in d.groupby("country_es"):
        a, b = g.set_index("year").loc[2018], g.set_index("year").loc[2025]
        rows.append([c, (b.hydro_twh / b.generation_twh - a.hydro_twh / a.generation_twh) * 100, ((b.wind_twh + b.solar_twh) / b.generation_twh - (a.wind_twh + a.solar_twh) / a.generation_twh) * 100, (b.fossil_share_pct - a.fossil_share_pct)])
    q = pd.DataFrame(rows, columns=["country", "Hidráulica", "Eólica + solar", "Fósil"])
    fig, ax = plt.subplots(figsize=(9.8, 5.2)); x = np.arange(len(q)); w = 0.24
    for i, (col, color) in enumerate([("Hidráulica", BLUE), ("Eólica + solar", TEAL), ("Fósil", ORANGE)]): ax.bar(x + (i - 1) * w, q[col], w, label=col, color=color)
    ax.axhline(0, color=DARK, lw=0.8); ax.set_xticks(x, q.country); ax.set_ylabel("Cambio 2018–2025 (puntos porcentuales)"); ax.legend(); clean_axes(ax)
    title(ax, "La dirección del cambio importa tanto como el nivel de partida", "Cambios sobre la misma frontera de generación; no es un ranking de desempeño")
    footer(fig, "Fuente: adaptación OWID de Ember Yearly Electricity Data 2026.")
    save(fig, "F23", "Movimiento regional 2018–2025", 8, "comparar cambios por fuente", "Ember/OWID 2026")


def fig24_regional_speed():
    d = pd.read_csv(DATA / "regional_normalized_metrics_v010.csv")
    fig, ax = plt.subplots(figsize=(9.8, 5.3))
    for (c, g), color in zip(d.groupby("country_es"), [NAVY, TEAL, ORANGE, PURPLE]):
        ax.plot(g.year, g.wind_solar_index_2018_100, lw=2.2, marker="o", ms=3.5, label=f"{c} · base {g.wind_solar_2018_twh.iloc[0]:.1f} TWh".replace(".", ","), color=color)
    ax.axhline(100, color=GREY, lw=0.8, ls="--"); ax.set_ylabel("Índice eólica + solar (2018 = 100)"); ax.legend(fontsize=8); clean_axes(ax)
    title(ax, "La velocidad depende del punto de partida", "El nivel inicial se muestra en la leyenda para evitar que un índice alto oculte una base pequeña")
    footer(fig, "Fuente: adaptación OWID de Ember Yearly Electricity Data 2026.")
    save(fig, "F24", "Velocidad regional de eólica y solar", 8, "comparar crecimiento sin ocultar base", "Ember/OWID 2026")


def fig25_regional_percapita():
    d = pd.read_csv(DATA / "regional_normalized_metrics_v010.csv"); d = d[d.year.eq(2025)]
    x = np.arange(len(d)); w = 0.36
    fig, ax = plt.subplots(figsize=(9.6, 5.1))
    ax.bar(x - w / 2, d.renewable_mwh_per_capita_2025, w, color=TEAL, label="Renovable")
    ax.bar(x + w / 2, d.fossil_mwh_per_capita_2025, w, color=ORANGE, label="Fósil")
    ax.set_xticks(x, d.country_es); ax.set_ylabel("Generación 2025 (MWh por habitante)"); ax.legend(); clean_axes(ax)
    title(ax, "La escala por habitante cambia la lectura de los porcentajes", "Generación armonizada dividida por población 2025; no es consumo final por habitante")
    footer(fig, "Fuentes: Ember/OWID 2026; Banco Mundial, WDI SP.POP.TOTL, actualización 13-07-2026.")
    save(fig, "F25", "Generación renovable y fósil por habitante", 8, "normalizar por población", "Ember/OWID; World Bank WDI")


def fig26_implications():
    d = pd.read_csv(ROOT / "strategy/STRATEGIC_IMPLICATION_MATRIX_v0.10.0.csv")
    horizon_cols = ["corto", "medio", "largo"]
    fig, ax = plt.subplots(figsize=(10.4, 6.5))
    y = np.arange(len(d))[::-1]
    for yi, (_, r) in zip(y, d.iterrows()):
        hz = str(r.horizon).split("/")
        for h in hz:
            if h in horizon_cols:
                x = horizon_cols.index(h)
                color = NAVY if r.confidence == "HIGH" else GOLD
                ax.scatter(x, yi, s=150 if r.confidence == "HIGH" else 105, color=color, edgecolor="white", lw=0.8, zorder=3)
    labels = [re.sub(r"^La |^Expansión |^Caída |^Intercambios |^Menor |^Datos ", "", s) for s in d.phenomenon]
    ax.set_yticks(y, labels); ax.set_xticks(range(3), ["Corto", "Medio", "Largo"]); ax.set_xlim(-0.5, 2.5); ax.grid(axis="x", color="#DCE5E7")
    ax.spines[:].set_visible(False); ax.tick_params(length=0)
    ax.legend(handles=[Line2D([0], [0], marker="o", color="none", markerfacecolor=NAVY, markersize=10, label="Confianza alta"), Line2D([0], [0], marker="o", color="none", markerfacecolor=GOLD, markersize=8, label="Confianza media")], loc="lower right")
    title(ax, "Las prioridades no viven todas en el mismo horizonte", "Cada punto enlaza un hallazgo, una variable de decisión, actores y un dato faltante")
    footer(fig, "Fuente: matriz de implicancias v0.10.0; trazabilidad completa en las matrices estratégicas y los controles de calidad.")
    save(fig, "F26", "Horizontes de las implicancias estratégicas", 9, "ordenar prioridades por horizonte", "Síntesis trazable v0.10.0")


def fig27_capabilities():
    d = pd.read_csv(ROOT / "strategy/NATIONAL_TECH_CAPABILITY_MATRIX_v0.10.0.csv")
    score_map = {"DEMONSTRATED_SYSTEMIC": 4, "DEMONSTRATED": 4, "OPERATING_CAPABILITY_WITH_GAP": 3, "DEMONSTRATED_PARTIAL": 3, "TESTING_AND_SERVICES_DEMONSTRATED": 3, "OPERATING_AND_TESTING_PARTIAL": 2, "R_AND_D_AND_TESTING": 2, "R_AND_D_DEMONSTRATED": 2}
    scores = d.evidence_level.map(score_map).fillna(1).to_numpy()
    labels = [s.replace(" y ", " / ") for s in d.technology_or_capability]
    y = np.arange(len(d))[::-1]
    fig, ax = plt.subplots(figsize=(10.4, 6.3))
    ax.barh(y, scores, color=[mpl.colormaps["YlGnBu"]((s - 1) / 3) for s in scores], height=0.62)
    ax.set_yticks(y, labels); ax.set_xticks([1, 2, 3, 4], ["No verificada", "I+D / ensayo", "Parcial", "Demostrada"]); ax.set_xlim(0.6, 4.35)
    status_labels = {
        "VERIFIED": "VERIFICADA",
        "PARTIAL": "PARCIAL",
        "BOUNDED_VERIFIED": "VERIFICADA",
        "BOUNDED_PARTIAL": "PARCIAL",
        "WITH_LIMITATION": "CON LÍMITE",
    }
    for yi, s, status in zip(y, scores, d.claim_status):
        ax.text(s + 0.08, yi, status_labels.get(str(status), "EVIDENCIA ACOTADA"), va="center", fontsize=7.5, color=GREY)
    clean_axes(ax, "x")
    title(ax, "Hay capacidades demostradas, pero ninguna etiqueta reemplaza un censo industrial", "Evaluación preliminar: separa operación, ingeniería, fabricación, ensayo e I+D")
    footer(fig, "Fuentes primarias e institucionales: INTI, CONICET-universidades, CAMMESA, CNEA/Nucleoeléctrica y páginas técnicas empresariales.")
    save(fig, "F27", "Matriz preliminar de capacidades tecnológicas nacionales", 9, "mostrar evidencia y brechas sin porcentajes inventados", "Fuentes primarias institucionales y técnicas")


def fig28_sensitivity():
    d = pd.read_csv(DATA / "scenario_sensitivity_results_v010.csv")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 5.0))
    colors = [GREY, ORANGE, TEAL, NAVY]
    ax1.bar(d.label_es, d.peak_net_load_gw, color=colors); ax1.set_ylabel("Pico de carga neta (GW)"); ax1.tick_params(axis="x", rotation=24); clean_axes(ax1); ax1.set_title("Pico neto", loc="left", color=NAVY, weight="semibold")
    ax2.bar(d.label_es, d.p99_upward_net_ramp_gw_per_h, color=colors); ax2.set_ylabel("Rampa ascendente p99 (GW/h)"); ax2.tick_params(axis="x", rotation=24); clean_axes(ax2); ax2.set_title("Rampa neta", loc="left", color=NAVY, weight="semibold")
    for ax, vals in [(ax1, d.peak_net_load_gw), (ax2, d.p99_upward_net_ramp_gw_per_h)]:
        for patch, v in zip(ax.patches, vals): ax.text(patch.get_x() + patch.get_width() / 2, v + (0.18 if ax is ax1 else 0.025), es_num(v, 2), ha="center", fontsize=8, weight="semibold")
    fig.suptitle("Más eólica y solar puede reducir el pico neto y aumentar la exigencia de rampa", x=0.02, ha="left", color=NAVY, fontsize=14, weight="semibold")
    fig.text(0.02, 0.93, "Sensibilidad algebraica 2025: no modela despacho, almacenamiento, recortes, red ni compromiso de unidades", color=GREY, fontsize=8.6)
    footer(fig, "Fuente: perfil horario CAMMESA 2025; escalas transparentes. Sensibilidad acotada, no pronóstico.")
    save(fig, "F28", "Sensibilidad acotada de carga neta y rampas", 9, "probar tensiones sin falsa precisión", "CAMMESA horario 2025; supuestos v0.10.0")


def main():
    PNG.mkdir(parents=True, exist_ok=True); VECTOR.mkdir(parents=True, exist_ok=True)
    for func in [
        fig01_system_checkpoints, fig02_supply_bridge, fig03_energy_peak_load_factor, fig04_demand_composition,
        fig05_duration_curve, fig06_top_hours_dispatch, fig07_ramps, fig08_renewable_growth, fig09_programs,
        fig10_peak_weather, fig11_hydro_trajectory, fig12_yacyreta_decomposition, fig13_comahue,
        fig14_thermal_emissions, fig15_lmdi, fig16_hourly_association, fig17_trade,
        fig18_map_infrastructure, fig19_map_demand_generation, fig20_map_corridors, fig21_map_almamdi,
        fig22_regional_structure, fig23_regional_change, fig24_regional_speed, fig25_regional_percapita,
        fig26_implications, fig27_capabilities, fig28_sensitivity,
    ]:
        func()
    reg = pd.DataFrame(REGISTER)
    reg.to_csv(ROOT / "figures/FIGURE_PUBLICATION_REGISTER_v0.10.0.csv", index=False)
    reg.rename(columns={"publication_status": "planned_status"}).to_csv(ROOT / "editorial/FIGURE_PLAN_v0.10.0.csv", index=False)
    print(f"Generated {len(reg)} figures ({int((reg.map_flag == 'YES').sum())} maps)")


if __name__ == "__main__":
    main()
