from src.pipeline import generate_event, detect_flood, event_summary
from src.risk import add_risk_score
from src.validation import classification_metrics
from src.uncertainty import threshold_ensemble


def test_event_pipeline():
    df = generate_event(size=32)
    out = add_risk_score(detect_flood(df))
    assert len(out) == 32 * 32
    assert out.flood_confidence.between(0, 1).all()
    assert out.risk_score.between(0, 100).all()
    m = classification_metrics(out.flood_truth, out.pred_flood)
    assert 0 <= m['f1'] <= 1
    assert event_summary(out)['flooded_area_km2'] >= 0


def test_uncertainty():
    u = threshold_ensemble(generate_event(size=24))
    assert u.ensemble_flood_probability.between(0, 1).all()
    assert u.uncertainty.between(0, 1).all()
