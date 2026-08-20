import numpy as np
import pandas as pd
from .pipeline import detect_flood


def threshold_ensemble(df: pd.DataFrame, thresholds=(-2.6, -3.0, -3.4, -3.8), max_slope=1.6):
    """Estimate detection stability across plausible SAR-change thresholds."""
    votes = [detect_flood(df, threshold_db=t, max_slope=max_slope)['pred_flood'].to_numpy() for t in thresholds]
    probability = np.vstack(votes).mean(axis=0)
    out = df[['x', 'y']].copy()
    out['ensemble_flood_probability'] = probability
    out['uncertainty'] = 1 - np.abs(probability - 0.5) * 2
    return out
