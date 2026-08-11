#!/usr/bin/env python3
"""
Mapa de calor de sismicidad histórica — Sudamérica
===================================================

Descarga el catálogo del USGS (FDSN event API), lo limpia y corrige por
completitud, y produce dos mapas de calor de densidad de epicentros:

    1. Interactivo  -> output/heatmap_sudamerica.html   (folium, opcional)
    2. Estático     -> output/densidad_sudamerica.png   (matplotlib + hexbin)

Diseñado para ejecutarse LOCALMENTE (necesita salida a earthquake.usgs.gov).

Parte del proyecto "Observatorio Sísmico · Sudamérica" · Licencia MIT.

Dependencias mínimas: requests, numpy, pandas, matplotlib, scipy
Opcionales (mejoran el resultado): folium, pyarrow, cartopy

    pip install requests numpy pandas matplotlib scipy folium pyarrow cartopy

Uso:
    python seismic_heatmap.py                    # usa la config de abajo
    python seismic_heatmap.py --no-cache         # ignora el cache local
"""
from __future__ import annotations

import argparse
import sys
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
import requests

# --------------------------------------------------------------------------- #
# CONFIGURACIÓN
# --------------------------------------------------------------------------- #
BBOX = dict(minlat=-56.0, maxlat=13.0, minlon=-82.0, maxlon=-34.0)  # Sudamérica
START_YEAR = 1990
END_YEAR = 2026
MIN_MAG = 4.0            # magnitud descargada del catálogo
MC = 4.5                # magnitud de completitud usada para el análisis (>= MC)
WEIGHT_BY_MAGNITUDE = True   # ponderar el heatmap por tamaño del sismo

USGS_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
USGS_MAX_EVENTS = 20_000     # tope duro por consulta de la API
CACHE_DIR = Path("cache")
OUT_DIR = Path("output")
TIMEOUT = 120


# --------------------------------------------------------------------------- #
# DESCARGA (con chunking anual para respetar el tope de 20k eventos)
# --------------------------------------------------------------------------- #
def _fetch_window(start: str, end: str) -> pd.DataFrame:
    """Una sola ventana temporal del catálogo USGS en formato CSV."""
    params = {
        "format": "csv",
        "starttime": start,
        "endtime": end,
        "minmagnitude": MIN_MAG,
        "minlatitude": BBOX["minlat"],
        "maxlatitude": BBOX["maxlat"],
        "minlongitude": BBOX["minlon"],
        "maxlongitude": BBOX["maxlon"],
        "orderby": "time-asc",
    }
    r = requests.get(USGS_URL, params=params, timeout=TIMEOUT)
    r.raise_for_status()
    df = pd.read_csv(StringIO(r.text))
    if len(df) >= USGS_MAX_EVENTS:
        # La ventana llegó al tope: los datos están truncados. Con chunks
        # anuales y M>=4 en Sudamérica esto no debería pasar, pero avisamos.
        print(f"  [!] {start[:10]} devolvió {len(df)} eventos (posible "
              f"truncamiento). Reduce el tamaño de la ventana.", file=sys.stderr)
    return df


def fetch_catalog() -> pd.DataFrame:
    """Descarga el catálogo completo, año por año."""
    frames = []
    for year in range(START_YEAR, END_YEAR + 1):
        start = f"{year}-01-01T00:00:00"
        end = f"{year + 1}-01-01T00:00:00"
        print(f"  Descargando {year} ...", end=" ", flush=True)
        df = _fetch_window(start, end)
        print(f"{len(df)} eventos")
        frames.append(df)
    cat = pd.concat(frames, ignore_index=True)
    # Solo eventos de tipo 'earthquake' (excluye explosiones, colapsos, etc.)
    if "type" in cat.columns:
        cat = cat[cat["type"] == "earthquake"].copy()
    return cat


def load_or_fetch(use_cache: bool = True) -> pd.DataFrame:
    """Carga desde cache si existe; si no, descarga y cachea."""
    CACHE_DIR.mkdir(exist_ok=True)
    key = f"usgs_sa_{START_YEAR}_{END_YEAR}_m{MIN_MAG}"
    pq = CACHE_DIR / f"{key}.parquet"
    csv = CACHE_DIR / f"{key}.csv"

    if use_cache:
        if pq.exists():
            print(f"Cache: {pq}")
            return pd.read_parquet(pq)
        if csv.exists():
            print(f"Cache: {csv}")
            return pd.read_csv(csv, parse_dates=["time"])

    print("Descargando catálogo USGS...")
    cat = fetch_catalog()
    cat["time"] = pd.to_datetime(cat["time"], utc=True, errors="coerce")

    # Persistir: Parquet si hay pyarrow/fastparquet, si no CSV.
    try:
        cat.to_parquet(pq, index=False)
        print(f"Guardado en cache: {pq}")
    except Exception:
        cat.to_csv(csv, index=False)
        print(f"Guardado en cache: {csv} (instala pyarrow para Parquet)")
    return cat


# --------------------------------------------------------------------------- #
# LIMPIEZA / COMPLETITUD
# --------------------------------------------------------------------------- #
def clean(cat: pd.DataFrame) -> pd.DataFrame:
    """Filtra nulos, duplicados y aplica el corte de completitud (>= MC)."""
    df = cat.dropna(subset=["latitude", "longitude", "mag"]).copy()
    df = df.drop_duplicates(subset=["id"]) if "id" in df.columns else df

    before = len(df)
    df = df[df["mag"] >= MC].copy()
    print(f"Completitud: {before} -> {len(df)} eventos con M >= {MC}")

    # Chequeo Gutenberg-Richter rápido: la Mc elegida debería quedar cerca
    # del pico del histograma de magnitudes. Si no, ajústala.
    peak_mag = df["mag"].round(1).mode()
    if len(peak_mag):
        print(f"Magnitud más frecuente (~Mc real): {peak_mag.iloc[0]:.1f}")
    return df


# --------------------------------------------------------------------------- #
# MAPA INTERACTIVO (folium)
# --------------------------------------------------------------------------- #
def make_folium_heatmap(df: pd.DataFrame) -> None:
    try:
        import folium
        from folium.plugins import HeatMap
    except ImportError:
        print("[skip] folium no instalado -> se omite el heatmap interactivo")
        return

    center = [df["latitude"].mean(), df["longitude"].mean()]
    m = folium.Map(location=center, zoom_start=4, tiles="CartoDB dark_matter")

    if WEIGHT_BY_MAGNITUDE:
        # Peso creciente pero acotado: exp de la magnitud sobre la Mc.
        w = 10 ** (0.5 * (df["mag"] - MC))
        data = [[la, lo, float(wi)]
                for la, lo, wi in zip(df["latitude"], df["longitude"], w)]
    else:
        data = df[["latitude", "longitude"]].values.tolist()

    HeatMap(data, radius=9, blur=7, min_opacity=0.25,
            max_zoom=6).add_to(m)

    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / "heatmap_sudamerica.html"
    m.save(str(out))
    print(f"OK  {out}")


# --------------------------------------------------------------------------- #
# MAPA ESTÁTICO (densidad hexbin, con costas si hay cartopy)
# --------------------------------------------------------------------------- #
def make_static_density(df: pd.DataFrame) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm

    OUT_DIR.mkdir(exist_ok=True)
    lon, lat = df["longitude"].values, df["latitude"].values
    weights = 10 ** (0.5 * (df["mag"].values - MC)) if WEIGHT_BY_MAGNITUDE else None

    # Intento con cartopy (costas + límite de placas Nazca); si no, plano.
    try:
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
        proj = ccrs.PlateCarree()
        fig = plt.figure(figsize=(9, 11))
        ax = plt.axes(projection=proj)
        ax.set_extent([BBOX["minlon"], BBOX["maxlon"],
                       BBOX["minlat"], BBOX["maxlat"]], crs=proj)
        ax.add_feature(cfeature.LAND, facecolor="#1a1a1a")
        ax.add_feature(cfeature.OCEAN, facecolor="#0a0a12")
        ax.add_feature(cfeature.COASTLINE, edgecolor="#888", linewidth=0.6)
        ax.add_feature(cfeature.BORDERS, edgecolor="#555", linewidth=0.4)
        transform = dict(transform=proj)
    except Exception:
        print("[info] cartopy no disponible -> mapa sin costas")
        fig, ax = plt.subplots(figsize=(9, 11))
        ax.set_xlim(BBOX["minlon"], BBOX["maxlon"])
        ax.set_ylim(BBOX["minlat"], BBOX["maxlat"])
        ax.set_facecolor("#0a0a12")
        transform = {}

    hb = ax.hexbin(lon, lat, C=weights, reduce_C_function=np.sum,
                   gridsize=90, cmap="inferno", norm=LogNorm(),
                   mincnt=1, linewidths=0.0, **transform)
    cb = fig.colorbar(hb, ax=ax, shrink=0.6, pad=0.02)
    cb.set_label("Densidad de sismicidad (ponderada)" if WEIGHT_BY_MAGNITUDE
                 else "Nº de epicentros")

    ax.set_title(f"Sismicidad Sudamérica  {START_YEAR}–{END_YEAR}  "
                 f"(M ≥ {MC}, n={len(df):,})", fontsize=12)
    fig.tight_layout()
    out = OUT_DIR / "densidad_sudamerica.png"
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"OK  {out}")


# --------------------------------------------------------------------------- #
def summary(df: pd.DataFrame) -> None:
    print("\n--- Resumen del catálogo ---")
    print(f"Eventos analizados : {len(df):,}")
    print(f"Rango temporal     : {df['time'].min()}  ->  {df['time'].max()}")
    print(f"Magnitud           : min {df['mag'].min():.1f}  "
          f"máx {df['mag'].max():.1f}  media {df['mag'].mean():.2f}")
    if "depth" in df.columns:
        print(f"Profundidad (km)   : mediana {df['depth'].median():.0f}  "
              f"máx {df['depth'].max():.0f}")
    # b-value de Gutenberg-Richter (estimador de Aki, máxima verosimilitud)
    m = df["mag"].values
    b = np.log10(np.e) / (m.mean() - (MC - 0.05))
    print(f"b-value (G-R, Aki) : {b:.2f}   (típico ~1.0)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-cache", action="store_true",
                    help="ignora el cache local y vuelve a descargar")
    args = ap.parse_args()

    cat = load_or_fetch(use_cache=not args.no_cache)
    df = clean(cat)
    if df.empty:
        print("Sin datos tras el filtrado. Revisa MC / rango temporal.")
        return
    summary(df)
    print()
    make_folium_heatmap(df)
    make_static_density(df)
    print("\nListo.")


if __name__ == "__main__":
    main()
