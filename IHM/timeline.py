import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from dash.dependencies import Input, Output, State

fig = None

def createTimeline(app):
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
        name='rect1',
        yref='paper',
        x0='2021-01-01', y0=0, x1='2021-01-05', y1=0.99,
        line=dict(color="Blue"),
    )

    fig.add_shape(type="rect",
        name='rect2',
        yref='paper',
        x0='2021-01-04', y0=0.01, x1='2021-01-06', y1=1,
        line=dict(color="Purple"),
    )

    #fig.show()

    inline_switches = dbc.FormGroup(
    [
        dbc.Label("Chroniques"),
        dbc.Checklist(
            options=[
                {"label": "Chronique 1", "value": 1},
                {"label": "Chronique 2", "value": 2},
            ],
            value=[1,2],
            id="switches-inline-input",
            inline=True,
            switch=True,
        ),
    ]
    )

    dropdown = dcc.Dropdown(
        options=[
            {"label": "Chronique 1", "value": 1},
            {"label": "Chronique 2", "value": 2}
        ],
        value=[1, 2],
        multi=True,
        id="dropdown-input"
    )

    @app.callback(
        Output("timeline", "figure"),
        Input("dropdown-input", "value"),
        State('dropdown-input', 'options'), prevent_initial_call=True)
    def updateTimeline(switches_value, children):
        
        visible = None

        for elem in children:
            if(elem['value'] in switches_value):
                visible = True
            else:
                visible = False

            fig.update_shapes(visible=visible, selector = dict(name='rect'+str(elem['value'])))

        print(switches_value, children)

        print("figure trace :")
        fig.for_each_trace(
            lambda trace: print(trace),
        )

        return fig

    card = dbc.Card(
        [
            dbc.CardHeader("Timeline"),
            dbc.CardBody(dcc.Graph(id='timeline', figure=fig)),
            dbc.CardFooter(dropdown)
        ]
    )

    return card