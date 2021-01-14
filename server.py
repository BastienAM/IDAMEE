import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(
    dbc.Row(
        [
            # Chronique ici
            dbc.Col(html.Div("One of two columns"), md=6),

            #Info patient + time line ici
            dbc.Col(html.Div("One of two columns"), md=6)
        ]
    )
)

df = pd.DataFrame([
    dict(Event="e1", Start='2021-01-01', Finish='2021-01-02'),
    dict(Event="e1", Start='2021-01-03', Finish='2021-01-04'),
    dict(Event="e1", Start='2021-01-05', Finish='2021-01-06'),
    dict(Event="e2", Start='2021-01-03', Finish='2021-01-04'),
    dict(Event="e2", Start='2021-01-04', Finish='2021-01-05'),
    dict(Event="e3", Start='2021-01-04', Finish='2021-01-05'),
])

fig = px.timeline(df, x_start="Start", x_end="Finish", y="Event", color = "Event")
fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
fig.update_xaxes(rangeslider_visible=True)

fig.add_shape(type="rect",
    yref='paper',
    x0='2021-01-01', y0=0, x1='2021-01-05', y1=0.99,
    line=dict(color="Blue"),
)

fig.add_shape(type="rect",
    yref='paper',
    x0='2021-01-04', y0=0.01, x1='2021-01-06', y1=1,
    line=dict(color="Purple"),
)

fig.show()

#if __name__ == '__main__':
#    app.run_server(debug=True)