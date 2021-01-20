import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from IHM.FactoryTimeline import FactoryTimeline

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

timeline = FactoryTimeline(app, FactoryTimeline.df)

app.layout = html.Div(
    dbc.Container(
        dbc.Row(
            [
                # Chronique ici
                dbc.Col(html.Div("One of two columns"), md=6),

                #Info patient + time line ici
                dbc.Col(timeline.createIHM(), md=6, id='div-timeline')
            ]
        ),
        fluid = True
    )
)

if __name__ == '__main__':
    app.run_server(debug=True)