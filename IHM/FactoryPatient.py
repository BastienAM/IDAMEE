import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from dash.dependencies import Input, Output

class FactoryPatient:

    def __init__(self, app, data):
        self.app = app
        self.data = data
        self.opt_dropdown, self.opt_dropdown_date, self.opt_dropdown_location, self.opt_dropdown_gender = self.__transformData(data)

    def __transformData(self, patients_recognised):
        # Transform for each patient
        index_patient = 0
        opt_dropdown = []
        opt_dropdown_gender = []
        opt_dropdown_date = []
        opt_dropdown_location = []
        for patient, dates_evts in patients_recognised.items():
            opt_dropdown.append({'label': patient,'value':patient})
            opt_dropdown_date.append({'label': patient,'value':patients_recognised[patient]["date_of_birth"]})
            opt_dropdown_gender.append({'label': patient,'value':patients_recognised[patient]["gender"]})
            opt_dropdown_location.append({'label': patient,'value':patients_recognised[patient]["location_code"]})
            index_patient += 1
        return opt_dropdown,opt_dropdown_date,opt_dropdown_location,opt_dropdown_gender

    def createIHM(self):
        card_main = dbc.Card(
            [
                dbc.CardHeader("Les patients pour cette chronique"),
                dbc.CardBody(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Label("Patient sélectionné",style={"color": "#166fc7","font-style":"bold;italic"}, width=3),
                                dbc.Col(
                                    dcc.Dropdown(id="patients",
                                        options = self.opt_dropdown,
                                        value = self.opt_dropdown[0]["value"], style={"color": "#166fc7"}
                                    ),
                                    width = 4
                                )
                            ],
                            row = True
                        ),

                        dbc.FormGroup(
                            [
                                dbc.Label("Sexe",style={"color": "#166fc7","font-style":"bold;italic"}, width=3),
                                dbc.Col(
                                    dbc.Input(
                                        id="H4_gender",
                                        disabled=True,
                                        style={"color": "000000)"}
                                    ),
                                    width = 4
                                )
                            ],
                            row = True
                        ),
                           
                        dbc.FormGroup(
                            [
                                dbc.Label("Date de Naissance",style={"color": "#166fc7","font-style":"bold;italic"}, width=3),
                                dbc.Col(
                                    dbc.Input(
                                        id="id_date",
                                        type="text",
                                        disabled=True,
                                        style={"color": "000000)"}
                                    ),
                                    width = 4
                                )
                            ],
                            row = True
                        ),

                        dbc.FormGroup(
                            [
                                dbc.Label("Location Code",style={"color": "#166fc7","font-style":"bold;italic"}, width = 3),
                                dbc.Col(
                                    dbc.Input(
                                        id='id_localisation',
                                        disabled=True,
                                        style={"color": "#000000"}
                                    ),
                                    width = 4
                                )
                            ],
                            row = True
                        ),
                    ]
                ),
            ],
            color="light",   # https://bootswatch.com/default/ for more card colors
            inverse=True,   # change color of text (black or white)
            outline=False,  # True = remove the block colors from the background and header
        )

        @self.app.callback(
            Output(component_id='H4_gender', component_property='value'),
            Input(component_id='patients', component_property='value')
        )
        def update_output(value):
            gender = ''
            reference = value
            for i in self.opt_dropdown_gender:
                if i["label"]==reference:
                        gender=i["value"]

            if gender=='1':
                gender='homme'
            elif gender=='2':
                gender='femme'
            return gender

        @self.app.callback(
            Output(component_id='id_date', component_property='value'),
            Input(component_id='patients', component_property='value')
        )
        def update_output(value):
            date=''
            reference = value
            for i in self.opt_dropdown_date:
                if i["label"] == reference:
                    date = i["value"]
            return date

        @self.app.callback(
            Output(component_id='id_localisation', component_property='value'),
            Input(component_id='patients', component_property='value')
        )
        def update_output(value):
            localisation = 0
            reference = value
            for i in self.opt_dropdown_location:
                if i["label"] == reference:
                    localisation = i["value"]

            return localisation

        return card_main