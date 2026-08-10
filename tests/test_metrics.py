import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from metrics import flood_metrics

def test_perfect_prediction():
    y = [0,1,1,0]
    m = flood_metrics(y,y)
    assert m["f1"] == 1.0
    assert m["iou"] == 1.0
