import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from dash.dependencies import Input, Output

class FactoryTimeline:

    df = pd.DataFrame([
        dict(Event="e1", Start='2021-01-01 00:00', Finish='2021-01-01 23:59', Group=1),
        dict(Event="e1", Start='2021-01-03', Finish='2021-01-03 23:59', Group=1),
        dict(Event="e1", Start='2021-01-05', Finish='2021-01-05 23:59', Group=2),
        dict(Event="e2", Start='2021-01-03', Finish='2021-01-03 23:59', Group=2),
        dict(Event="e2", Start='2021-01-04', Finish='2021-01-04 23:59', Group=1),
        dict(Event="e3", Start='2021-01-04', Finish='2021-01-04 23:59', Group=1),
        dict(Event="e3", Start='2021-01-04', Finish='2021-01-04 23:59', Group=2),
    ])


    def __init__(self, app, dataFrame):
        self.app = app
        self.dataFrame = dataFrame
    

    def createIHM(self):

        chroniqueIdx = self.dataFrame.Group.unique()

        dropdown = self.__createDropdowm(chroniqueIdx)

        fig = self.__createTimeline(self.dataFrame)

        card = dbc.Card(
            [
                dbc.CardHeader("Timeline"),
                dbc.CardBody(dcc.Graph(id='timeline', figure=fig)),
                dbc.CardFooter(dropdown)
            ]
        )

        return card


    def __createDropdowm(self, chroniqueIdx):

        options = []
        for elem in chroniqueIdx:
            options.append({"label": "Chronique "+str(elem), "value": elem})


        dropdown = dcc.Dropdown(
            options = options,
            value = chroniqueIdx,
            multi = True,
            id = "dropdown-input"
        )

        @self.app.callback(
            Output("timeline", "figure"),
            Input("dropdown-input", "value"),
            prevent_initial_call = True
        )
        def updateTimeline( switches_value):
            if(len(switches_value) > 0):
                dfFilter = self.dataFrame[self.dataFrame['Group'].isin(switches_value)]
                return self.__createTimeline(dfFilter)
            else:
                return {}

        return dropdown

    def __createTimeline(self, dataFrame):

        fig = px.timeline(dataFrame, x_start="Start", x_end="Finish", y="Event", color = "Event", hover_data=dict(Event=False, Start=False, Finish=False, Group=False))
        fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
        fig.update_traces(xperiodalignment="middle", xperiod=86400000.0)
        fig.update_xaxes(rangeslider_visible=True, ticklabelmode="period", showgrid=True, dtick=86400000.0, type="date")

        chroniqueIdxToDisplay = dataFrame.Group.unique()

        shift = 0
        for val in chroniqueIdxToDisplay:
            dataframeChronique = dataFrame[dataFrame['Group'] == val]
            minDate = min(dataframeChronique['Start'])
            maxDate = max(dataframeChronique['Finish'])

            fig.add_shape(
                type = "rect",
                yref = "paper",
                x0 = minDate, 
                y0 = 0 + shift, 
                x1 = maxDate, 
                y1 = 0.99 + shift,
                line = dict(color = px.colors.qualitative.Set3[val-1 % 10]),
            )

            shift += 0.01

        return fig

def convertToDataFrame(array):
    values = []
    chroniqueIdx = 1
    for row in array:
        eventIdx = 1
        for chronique in row:
            values.append(dict(Event="e"+str(eventIdx), Start= chronique[1]+'00:00', Finish=chronique[1]+'23:59', Group=chroniqueIdx))
            eventIdx += 1
        chroniqueIdx += 1

    return pd.DataFrame(values)
