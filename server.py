import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

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

if __name__ == '__main__':
    app.run_server(debug=True)