from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from metrics import flood_metrics

ROOT = Path(__file__).resolve().parents[1]
(ROOT / "data").mkdir(exist_ok=True)
(ROOT / "outputs").mkdir(exist_ok=True)
rng = np.random.default_rng(5)
n = 160
y, x = np.mgrid[-1:1:complex(n), -1:1:complex(n)]
reference = (((x+0.15)**2/0.55**2 + (y-0.05)**2/0.35**2) < 1).astype(int)
pre_db = -11 + rng.normal(0, 1.2, (n,n))
post_db = pre_db.copy()
post_db[reference==1] -= 7.0
change = post_db - pre_db
predicted = (change < -4.5).astype(int)
np.save(ROOT/"data"/"synthetic_reference_mask.npy", reference)
np.save(ROOT/"data"/"synthetic_sar_change_db.npy", change)
m = flood_metrics(reference, predicted)
(ROOT/"outputs"/"flood_metrics.json").write_text(json.dumps(m, indent=2))
plt.figure(figsize=(6,5)); plt.imshow(change); plt.colorbar(label="Post - pre backscatter (dB)")
plt.contour(reference, levels=[0.5], linewidths=1); plt.title("Synthetic Sentinel-1 Flood Change Signal")
plt.axis("off"); plt.tight_layout(); plt.savefig(ROOT/"outputs"/"sar_change_map.png", dpi=180); plt.close()
print(m)
