from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline import generate_event, detect_flood, event_summary
from src.risk import add_risk_score

app = FastAPI(title='Flood Intelligence Event Service', version='1.0.0')

class EventRequest(BaseModel):
    seed: int = 42
    threshold_db: float = -3.0

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/event-summary')
def score_event(req: EventRequest):
    df = add_risk_score(detect_flood(generate_event(seed=req.seed), threshold_db=req.threshold_db))
    summary = event_summary(df)
    summary['critical_priority_pixels'] = int((df['response_priority'] == 'Critical').sum())
    return summary
