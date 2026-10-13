import json
import pandas as pd
import plotly.express as px
import streamlit as st
from core import simulate, metrics

st.set_page_config(page_title='Flight Control Lab', page_icon='🎛️', layout='wide')
st.title('Flight Control Lab')
st.caption('Vertical motion · gravity-compensated acceleration · PID with anti-windup')
presets = {'Balanced PID': (1.0, 0.1, 1.5), 'Proportional only': (1.0, 0.0, 0.0), 'Damped PD': (1.0, 0.0, 2.0), 'Custom': (1.0, 0.1, 1.5)}
preset = st.sidebar.selectbox('Controller preset', list(presets))
gains = presets[preset]
if preset == 'Custom':
    gains = tuple(st.sidebar.slider(label, 0.0, maximum, value) for label,maximum,value in zip(['Kp','Ki','Kd'],[5.0,1.0,5.0],gains))
target = st.sidebar.slider('Target altitude (m)', 5, 100, 20)
duration = st.sidebar.slider('Duration (s)', 20, 120, 40)
gust = st.sidebar.slider('Disturbance at 10–12 s (m/s²)', -5.0, 5.0, 0.0)
compare = st.sidebar.checkbox('Compare proportional-only controller', value=True)
rows = simulate(*gains, target=target, duration=duration, gust=gust)
data = pd.DataFrame(rows)
stats = metrics(rows, target)
cols = st.columns(4)
for col,label,value in zip(cols,['Overshoot','Final error','2% settling time','Actuator saturation'],
                          [f'{stats["overshoot_m"]:.2f} m',f'{stats["final_error_m"]:.2f} m', f'{stats["settling_time_s"]:.2f} s' if stats['settling_time_s'] is not None else 'Not settled', f'{stats["saturation_pct"]:.1f}%']):
    col.metric(label,value)
data['controller'] = preset
if compare:
    baseline = pd.DataFrame(simulate(gains[0], 0, 0, target, duration=duration, gust=gust)); baseline['controller'] = 'P baseline'
    plotted = pd.concat([data,baseline], ignore_index=True)
else: plotted = data
for field in ['altitude_m','velocity_ms','command_ms2','error_m']:
    fig = px.line(plotted,x='time_s',y=field,color='controller',template='plotly_dark')
    if field == 'altitude_m': fig.add_hline(y=target,line_dash='dash')
    st.plotly_chart(fig,width='stretch')
with st.expander('Model and performance definitions'):
    st.markdown('`dh/dt = v`, `dv/dt = u − 0.3v + disturbance`. Command is limited to ±10 m/s². Semi-implicit Euler uses a 0.02 s step. The initial altitude and velocity are zero. There is no ground-contact model. Settling time is the first time after the last excursion outside the 2% band within this finite observation window. The disturbance is an acceleration, not a wind-speed measurement.')
st.download_button('Simulation CSV', data.to_csv(index=False), 'simulation.csv', 'text/csv')
st.download_button('Parameters and metrics JSON', json.dumps(dict(gains=gains,target_m=target,duration_s=duration,disturbance_ms2=gust,metrics=stats),indent=2), 'experiment.json','application/json')
