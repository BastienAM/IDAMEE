import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from main import chronicle_recognition

global  reference
def transform_for_needlePlot(patients_recognised, c):
    cores_dic = {}
    index = 0

    # Transform for chronicle

    # Transform for each patient
    patients_new = {}
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
    return patients_new, opt_dropdown,opt_dropdown_date,opt_dropdown_location,opt_dropdown_gender
def query_data():
    patients_recognised, c = chronicle_recognition()
    data, opt_dropdown ,opt_dropdown_date,opt_dropdown_location,opt_dropdown_gender= transform_for_needlePlot(patients_recognised, c)
    return data, opt_dropdown,opt_dropdown_date,opt_dropdown_location,opt_dropdown_gender
data, opt_dropdown,opt_dropdown_date,opt_dropdown_location ,opt_dropdown_gender= query_data()
#print(opt_dropdown)
#df = px.data.gapminder()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
card_main = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5("Les patients pour cette chronique", className="card-title",style={"color": "#166fc7"}),

                dcc.Dropdown(id="patients",
                             options=opt_dropdown,
                             value=opt_dropdown[3]["value"],style={"color": "#166fc7"}
                             ),
                html.H6(id='dd-output-container',style={"color": "#166fc7"}),


                html.H4(""),
                #html.H4(id='dd-output-container', className="card-subtitle"),

                dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Sexe",style={"color": "#166fc7","font-style":"bold;italic"}),
                        dbc.Input(
                            id="H4_gender",
                            disabled=True,
                            style={"color": "000000)"}
                            #value=opt_dropdown_gender[0]["value"], style={"color": "#00000"}

                        ),
                            ]
                ),
                width = 4,

             ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Date de Naissance",style={"color": "#166fc7","font-style":"bold;italic"}),
                            dbc.Input(
                                id="id_date",
                                type="text",
                                disabled=True,
                                 style={"color": "000000)"}),
                        ]
                    ),
                    width=4,

                ),

                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Location Code",style={"color": "#166fc7","font-style":"bold;italic"}),
                            dbc.Input(
                                id='id_localisation',
                                disabled=True,
                                style={"color": "#000000"},



                            ),
                        ]
                    ),
                    width=4,

                ),
                html.P(
                    "",
                    className="card-text",
                ),

                # dbc.Button("Press me", color="primary"),
                # dbc.CardLink("GirlsWhoCode", href="https://girlswhocode.com/", target="_blank"),
            ]
        ),
    ],
    color="light",   # https://bootswatch.com/default/ for more card colors
    inverse=True,   # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)




card_graph = dbc.Card(
        dcc.Graph(id='my_bar', figure={}), body=True, color="secondary",
)


app.layout = html.Div([
    dbc.Row([dbc.Col(card_main, width=5),

             dbc.Col("", width=5)], justify="around"),  # justify="start", "center", "end", "between", "around"

    # dbc.CardGroup([card_main, card_question, card_graph])   # attaches cards with equal width and height columns
    # dbc.CardDeck([card_main, card_question, card_graph])    # same as CardGroup but with gutter in between cards

    # dbc.CardColumns([                        # Cards organised into Masonry-like columns
    #         card_main,
    #         card_question,
    #         card_graph,
    #         card_question,
    #         card_question,
    # ])

])



@app.callback(

Output(component_id='dd-output-container', component_property='children'),
    [Input(component_id='patients', component_property='value')]
)
def update_output(value):
    reference=value
    #print(reference,"-------------------------")
    return 'Les informations sur le patient sélectionné "{}"'.format(value)

@app.callback(
Output(component_id='H4_gender', component_property='value'),
    [Input(component_id='patients', component_property='value')]
)
def update_output(value):
    gender = ''
    reference = value
    for i in opt_dropdown_gender:
      if i["label"]==reference:
            gender=i["value"]

    if gender=='1':
        gender='homme'
    else:
        if gender=='2' :
            gender='femme'
    return gender

@app.callback(
Output(component_id='id_date', component_property='value'),
    [Input(component_id='patients', component_property='value')]
)
def update_output(value):
    date=''
    reference = value
    for i in opt_dropdown_date:
        if i["label"] == reference:
            date = i["value"]
    return date


@app.callback(

Output(component_id='id_localisation', component_property='value'),
    [Input(component_id='patients', component_property='value')]
)
def update_output(value):
    localisation=0
    reference = value
    for i in opt_dropdown_location:
        if i["label"] == reference:
            localisation = i["value"]

    return localisation






#def update_graph(valuea):
   # fig = px.scatter(df.query("year=={}".format(str(valuea))), x="gdpPercap", y="lifeExp",
                    # size="pop", color="continent", title=str(valuea),
                     #hover_name="country", log_x=True, size_max=60).update_layout(showlegend=True, title_x=0.5)



if __name__ == "__main__":
    app.run_server(debug=True)
