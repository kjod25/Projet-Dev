import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import datetime
import plotly.express as px
import pandas as pd


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(__name__, server=server,
                         routes_pathname_prefix='/Image/',
                         external_stylesheets=[dbc.themes.BOOTSTRAP, "https://fonts.googleapis.com/css?family=Nunito+Sans&display=swap"]
                         )

    # Create Dash Layout

    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#FFC000",
        "font-family": "Nunito Sans"

    }

    CONTENT_STYLE = {
        "margin-left": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#0A3754",
        "color": "white"
    }

    sidebar = html.Div(
        [
            html.Img(src=dash_app.get_asset_url('logo2.png'), style={'height':'10.5%', 'width':'14'}),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Ajouter une image", href="/Image/", style={"color":"black", "font-size":"20px"}),
                    html.Br(),
                    dbc.NavLink("Carte", href="/Map/", style={"color":"black", "font-size":"20px"}),
                    html.Br(),
                    dbc.NavLink("Statistiques", href="/Stats/", style={"color":"black", "font-size":"20px"}),
                    html.Br(),
                    dbc.NavLink("Contact", href="/Contact/", style={"color":"black", "font-size":"20px"}),
                    html.Br(),
                ],
                vertical=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    content = html.Div(id="page-content", style=CONTENT_STYLE)


    mapbox_access_token = open("sources/plotlydash/token").read()

    trash_loc = pd.read_excel("sources/plotlydash/assets/Carte_vendée.xlsx")

    fig = px.scatter_mapbox(trash_loc, lat="lat", lon="lon", hover_name="Zone", hover_data=["Plastique","Biodégra","Verre","Total",],
                            color_discrete_sequence=["#FFC000"], zoom=4, height=800)
    fig.update_layout(mapbox_style="streets", mapbox_accesstoken=mapbox_access_token)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    map_layout = html.Div([
        html.Div([
            html.H1("Trash location map", id="map_title", style={"text-align": "center", "font-family":"Nunito Sans"})]
        ),
        html.Hr(),

        html.Div([dcc.Graph(figure=fig)]),
        ], id="map-content"),

    addImage_layout = html.Div([
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-image-upload'),
        dcc.Dropdown(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Montreal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            placeholder="Select a city",
        )
    ])

    def parse_contents(contents, filename, date):
        return html.Div([
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),

            # HTML images accept base64 encoded strings in the same format
            # that is supplied by the upload
            html.Img(src=contents, style={"height": "50%", "weight": "50%"}),
            html.Hr(),
            html.Div('Raw Content'),
            html.Pre(contents[0:200] + '...', style={
                'whiteSpace': 'pre-wrap',
                'wordBreak': 'break-all'
            })
        ])

    @dash_app.callback(Output('output-image-upload', 'children'),
                       Input('upload-image', 'contents'),
                       State('upload-image', 'filename'),
                       State('upload-image', 'last_modified'))
    def update_output(list_of_contents, list_of_names, list_of_dates):
        if list_of_contents is not None:
            children = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
            return children

    dash_app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

    @dash_app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/Map/":
            return map_layout
        elif pathname == "/Stats/":
            return html.P("Page pour les statistiques")
        elif pathname == "/Contact/":
            return html.P("Page contact")
        elif pathname == "/Image/":
            return addImage_layout
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )

    return dash_app.server
