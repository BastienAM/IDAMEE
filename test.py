import plotly.graph_objects as go
import pandas as pd

df = pd.DataFrame(dict(
    date=["2020-01-01", "2020-01-03", "2020-01-04", "2020-01-05", "2020-01-07", "2020-01-08"],
    value=[1,2,3,1,2,3]
))

fig = go.Figure()
fig.add_trace(go.Bar(
    name="Middle-aligned",
    x=df["date"], y=df["value"],
    xperiod=86400000.0,
    xperiodalignment="middle"
))
fig.update_xaxes(showgrid=False, ticklabelmode="period", dtick=86400000.0)

#print(fig)
#fig.show()