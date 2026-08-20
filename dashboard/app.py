import streamlit as st
from src.pipeline import generate_event, detect_flood, event_summary
from src.risk import add_risk_score
from src.validation import classification_metrics

st.set_page_config(page_title='AI Flood Intelligence', layout='wide')
st.title('AI Flood Intelligence & Event Mapping')
st.caption('Synthetic portfolio demonstration — not an operational emergency product.')
threshold = st.slider('SAR change threshold (dB)', -5.0, -1.5, -3.0, 0.1)
df = add_risk_score(detect_flood(generate_event(), threshold_db=threshold))
summary = event_summary(df)
metrics = classification_metrics(df.flood_truth, df.pred_flood)
c1,c2,c3,c4 = st.columns(4)
c1.metric('Mapped flood area', f"{summary['flooded_area_km2']:.3f} km²")
c2.metric('F1', f"{metrics['f1']:.3f}")
c3.metric('IoU', f"{metrics['iou']:.3f}")
c4.metric('Mean confidence', f"{summary['mean_confidence']:.2f}")
st.subheader('Highest-priority flood pixels')
st.dataframe(df[df.pred_flood == 1][['x','y','change_db','population','road','critical_facility','flood_confidence','risk_score','response_priority']].sort_values('risk_score', ascending=False).head(100), use_container_width=True)
st.scatter_chart(df[df.pred_flood == 1], x='x', y='y', color='risk_score')
