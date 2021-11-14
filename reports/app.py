import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
from figures.ghg_figure import ghg_fig, ghg_countries, ghg_gas_name_dict

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {"background": "#ffffff", "text": "#000000"}
fonts = {"font-family": ["Arial", "Helvetica", "sans-serif"]}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20%",
    "padding": "20px 10px",
    "background-color": "#f8f9fa",
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    "margin-left": "25%",
    "margin-right": "5%",
    "top": 0,
    "padding": "20px 10px",
}

TEXT_STYLE = {"textAlign": "center", "color": "#191970"}

CARD_TEXT_STYLE = {"textAlign": "center", "color": "#0074D9"}

controls = dbc.Card(
    [
        html.P("Greenhouse Gases", style={"textAlign": "center"}),
        dcc.Dropdown(
            id="ghg_dropdown",
            options=[
                {"label": name, "value": str(df)}
                for name, df in ghg_gas_name_dict.items()
            ],
            value=["Carbon Dioxide"],  # default value
            multi=False,
            clearable=False,
            placeholder="Select a greenhouse gas",
        ),
        html.P("Country", style={"textAlign": "center"}),
        dcc.Dropdown(
            id="ghg_country_dropdown",
            options=[{"label": country, "value": country} for country in ghg_countries],
            value=["United Kingdom"],  # default value
            multi=True,
            clearable=False,
            placeholder="Select a country",
        ),
    ]
)


sidebar = html.Div(
    [html.H2("Parameters", style=TEXT_STYLE), html.Hr(), controls],
    style=SIDEBAR_STYLE,
)

ghg_figure_div = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.H1(
            children="Paris Agreement Update",
            style={
                "textAlign": "left",
                "color": colors["text"],
                "font-family": fonts["font-family"],
            },
        ),
        html.Div(
            children="How far are we from the target?",
            style={
                "textAlign": "left",
                "color": colors["text"],
                "font-family": fonts["font-family"],
            },
        ),
        dcc.Graph(id="ghg-line-plot", figure=ghg_fig),
    ],
)

content_ghg_fig = dbc.Row([dcc.Graph(id="ghg-line-plot", figure=ghg_fig)])


content = html.Div(
    [html.H2("Climate Change Dashboard", style=TEXT_STYLE), html.Hr(), content_ghg_fig],
    id="page-content",
    style=CONTENT_STYLE,
)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

if __name__ == "__main__":
    app.run_server(debug=True)
