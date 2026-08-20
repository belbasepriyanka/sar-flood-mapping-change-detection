import numpy as np
import pandas as pd


def add_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    """Combine flood confidence and exposure into a demonstration response-priority score."""
    out = df.copy()
    pop_norm = out['population'] / max(out['population'].quantile(0.99), 1)
    exposure = 0.55 * np.clip(pop_norm, 0, 1) + 0.25 * out['road'] + 0.20 * out['critical_facility']
    out['risk_score'] = np.clip(100 * out['pred_flood'] * (0.55 * out['flood_confidence'] + 0.45 * exposure), 0, 100)
    out['response_priority'] = pd.cut(out['risk_score'], [-1, 25, 50, 75, 100], labels=['Low', 'Moderate', 'High', 'Critical']).astype(str)
    return out
