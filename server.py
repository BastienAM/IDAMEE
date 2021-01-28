import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from IHM.FactoryTimeline import FactoryTimeline, convertToDataFrame
from IHM.FactoryPatient import FactoryPatient
from chronicleRequest import chronicle_recognition
from dash.dependencies import Input, Output

# Configuration du serveur avec son template 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


data, c = chronicle_recognition()

patient = list(data.items())[0][1]

timeline = FactoryTimeline(app, convertToDataFrame(patient))
patient = FactoryPatient(app, data)


# Création Timeline
@app.callback(
    Output(component_id='div-timeline', component_property='children'),
    Input(component_id='patients', component_property='value'),
    prevent_initial_call = True
)
def update_output(value):
    timeline = FactoryTimeline(app, convertToDataFrame(data[value]))
    return timeline.createIHM()


app.layout = html.Div(
    dbc.Container(
        dbc.Row(
            [
                # Chronique ici
                dbc.Col(html.Div("One of two columns"), md=6),

                # Info patient + timeline ici
                dbc.Col(
                    [
                        html.Div(patient.createIHM(), id='div-patient'),
                        html.Div(timeline.createIHM(), id='div-timeline', style={"margin-top": "15px"})
                    ],
                    md=6
                )
            ]
        ),
        fluid = True
    )
)

# Lancement du serveur
if __name__ == '__main__':
    app.run_server(debug=True)