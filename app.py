import streamlit as st
import pandas as pd
import plotly.express as px
from core import simulate

st.set_page_config(page_title='Flight Control Lab', layout='wide')
st.title('Flight Control Lab')
st.caption('A simplified vertical-motion PID experiment with bounded acceleration and anti-windup.')
kp = st.sidebar.slider('Kp', 0.0, 5.0, 1.0)
ki = st.sidebar.slider('Ki', 0.0, 1.0, 0.1)
kd = st.sidebar.slider('Kd', 0.0, 5.0, 1.5)
target = st.sidebar.slider('Target altitude (m)', 5, 100, 20)
gust = st.sidebar.slider('Disturbance at 10–12 s (m/s²)', -5.0, 5.0, 0.0)
data = pd.DataFrame(simulate(kp, ki, kd, target, gust=gust))
cols = st.columns(3)
cols[0].metric('Overshoot', f'{max(0, data.altitude_m.max()-target):.2f} m')
cols[1].metric('Final error', f'{data.error_m.iloc[-1]:.2f} m')
outside = data.index[data.error_m.abs() > target*0.02]
settling = data.time_s.iloc[outside[-1]+1] if len(outside) and outside[-1]+1 < len(data) else None
cols[2].metric('2% settling time', f'{settling:.2f} s' if settling is not None else 'Not settled')
fig = px.line(data, x='time_s', y='altitude_m'); fig.add_hline(y=target, line_dash='dash')
st.plotly_chart(fig, width='stretch')
st.plotly_chart(px.line(data, x='time_s', y='command_ms2'), width='stretch')
st.download_button('Export simulation', data.to_csv(index=False), 'simulation.csv', 'text/csv')
