from __future__ import annotations
import numpy as np
import pandas as pd


def generate_event(seed: int = 42, size: int = 64) -> pd.DataFrame:
    """Generate a synthetic SAR flood-event raster table for portfolio demonstration."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:size, 0:size]
    xn = xx / (size - 1)
    yn = yy / (size - 1)
    dem = 5 + 18 * yn + 4 * np.sin(2 * np.pi * xn) + rng.normal(0, 0.6, (size, size))
    gy, gx = np.gradient(dem)
    slope = np.hypot(gx, gy)
    river_center = 0.48 + 0.10 * np.sin(3 * np.pi * yn)
    permanent_water = np.abs(xn - river_center) < 0.035
    distance_to_river = np.abs(xn - river_center)
    flood_truth = (distance_to_river < (0.12 + 0.05 * np.exp(-((yn - 0.55) ** 2) / 0.03))) & (dem < np.quantile(dem, 0.58))
    flood_truth &= ~permanent_water
    pre_vv = -8.5 - 5.0 * permanent_water + rng.normal(0, 1.1, (size, size))
    post_vv = pre_vv + rng.normal(0, 0.7, (size, size))
    post_vv[flood_truth] -= rng.normal(5.2, 0.9, flood_truth.sum())
    change_db = post_vv - pre_vv
    population = np.maximum(0, 45 + 95 * np.exp(-((xn - 0.75) ** 2 + (yn - 0.48) ** 2) / 0.025) + rng.normal(0, 8, (size, size)))
    road = (np.abs(yn - (0.27 + 0.10 * xn)) < 0.012) | (np.abs(xn - 0.72) < 0.012)
    critical = ((xx - int(size * 0.73)) ** 2 + (yy - int(size * 0.46)) ** 2) < (size * 0.025) ** 2
    return pd.DataFrame({
        'x': xx.ravel(), 'y': yy.ravel(), 'pre_vv_db': pre_vv.ravel(), 'post_vv_db': post_vv.ravel(),
        'change_db': change_db.ravel(), 'dem_m': dem.ravel(), 'slope_proxy': slope.ravel(),
        'permanent_water': permanent_water.ravel().astype(int), 'population': population.ravel().round(2),
        'road': road.ravel().astype(int), 'critical_facility': critical.ravel().astype(int),
        'flood_truth': flood_truth.ravel().astype(int),
    })


def detect_flood(df: pd.DataFrame, threshold_db: float = -3.0, max_slope: float = 1.6) -> pd.DataFrame:
    """Detect new flooding using SAR change plus terrain and permanent-water exclusions."""
    out = df.copy()
    candidate = (out['change_db'] <= threshold_db) & (out['permanent_water'] == 0) & (out['slope_proxy'] <= max_slope)
    out['pred_flood'] = candidate.astype(int)
    change_strength = np.clip((threshold_db - out['change_db']) / 4.0, 0, 1)
    terrain_factor = np.clip(1 - out['slope_proxy'] / max_slope, 0, 1)
    out['flood_confidence'] = np.clip(0.65 * change_strength + 0.35 * terrain_factor, 0, 1)
    return out


def event_summary(df: pd.DataFrame, pixel_area_m2: float = 100.0) -> dict:
    flooded = df['pred_flood'] == 1
    return {
        'flooded_pixels': int(flooded.sum()),
        'flooded_area_km2': float(flooded.sum() * pixel_area_m2 / 1e6),
        'population_exposure_index': round(float(df.loc[flooded, 'population'].sum()), 1),
        'road_pixels_exposed': int(df.loc[flooded, 'road'].sum()),
        'critical_facility_pixels_exposed': int(df.loc[flooded, 'critical_facility'].sum()),
        'mean_confidence': round(float(df.loc[flooded, 'flood_confidence'].mean()) if flooded.any() else 0.0, 3),
    }
