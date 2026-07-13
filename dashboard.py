import streamlit as st
import time
import plotly.graph_objects as go
from data_generator import generate_data
from detector import OnlineZScoreDetector
from storage import InMemoryStorage
from config import UPDATE_INTERVAL

st.set_page_config(page_title="Anomaly Dashboard", layout="wide")
st.title("📈 Real-Time Anomaly Detection Dashboard")
st.markdown("Red dots are detected anomalies in the stream.")

detector = OnlineZScoreDetector()
storage = InMemoryStorage(maxlen=300)
data_gen = generate_data()

chart_placeholder = st.empty()
info_placeholder = st.empty()

while True:
    t, val = next(data_gen)
    is_anom = detector.detect(val)
    storage.add(t, val, is_anom)

    df = storage.get_dataframe()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['value'],
                             mode='lines', name='Data', line=dict(color='blue')))

    anomalies_df = df[df['anomaly'] == 1]
    if not anomalies_df.empty:
        fig.add_trace(go.Scatter(x=anomalies_df['timestamp'], y=anomalies_df['value'],
                                 mode='markers', name='Anomaly',
                                 marker=dict(color='red', size=10)))

    fig.update_layout(title="Live Data Stream", xaxis_title="Time", yaxis_title="Value", height=500)
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    if not anomalies_df.empty:
        info_placeholder.markdown(f"### 🔴 Anomalies! Total in window: {len(anomalies_df)}")
        info_placeholder.dataframe(anomalies_df[['timestamp', 'value']].tail(5))
    else:
        info_placeholder.markdown("✅ No anomalies in the current window.")

    time.sleep(UPDATE_INTERVAL)
