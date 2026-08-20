from pathlib import Path
import sys
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.pipeline import generate_event, detect_flood, event_summary
from src.risk import add_risk_score
from src.validation import classification_metrics
from src.uncertainty import threshold_ensemble

for p in [ROOT/'data', ROOT/'results']:
    p.mkdir(exist_ok=True)
raw = generate_event()
scored = add_risk_score(detect_flood(raw))
uncert = threshold_ensemble(raw)
merged = scored.merge(uncert, on=['x','y'])
metrics = classification_metrics(merged.flood_truth, merged.pred_flood)
summary = event_summary(merged)
summary['critical_priority_pixels'] = int((merged.response_priority == 'Critical').sum())
merged.head(500).to_csv(ROOT/'data'/'sample_event_pixels.csv', index=False)
pd.DataFrame([metrics]).to_csv(ROOT/'results'/'validation_metrics.csv', index=False)
pd.DataFrame([summary]).to_csv(ROOT/'results'/'event_summary.csv', index=False)
merged.sort_values('risk_score', ascending=False).head(100).to_csv(ROOT/'results'/'top_priority_pixels.csv', index=False)
print('Validation metrics:', metrics)
print('Event summary:', summary)
