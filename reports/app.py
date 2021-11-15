import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, dash_table, State
import pandas as pd
from figures.ghg_figure import (
    ghg_fig,
    ghg_countries,
    ghg_gas_name_dict,
    ghg_df_selection_df,
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# --------------------STYLES-----------------
GRAPH_STYLE = {"background": "#ffffff", "text": "#000000"}
FONT_STYLE = {"font-family": ["Arial", "Helvetica", "sans-serif"]}
TABLE_STYLE = {
    "background_color": "#ffffff",
    "font_color": "#000000",
    "header_color": "#EDEDED",
}

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

# --------------SIDEBAR-------------------------

controls = dbc.Card(
    [
        html.P("Greenhouse Gases", style={"textAlign": "center"}),  # Gases
        dcc.Dropdown(
            id="ghg_dropdown",
            options=[
                {"label": name, "value": name} for name in ghg_gas_name_dict.keys()
            ],
            value="Methane",
            multi=False,
            clearable=True,
            placeholder="Select a greenhouse gas",
        ),
        html.P("Country", style={"textAlign": "center"}),  # Countries
        dcc.Dropdown(
            id="ghg_country_dropdown",
            options=[{"label": country, "value": country} for country in ghg_countries],
            value="United Kingdom",  # default value
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
# -----------------------FIRST ROW---------------------------------
# ---------FIGURE-----
ghg_figure_div = html.Div(
    style={"backgroundColor": GRAPH_STYLE["background"]},
    children=[
        html.H1(
            children="Paris Agreement Update",
            style={
                "textAlign": "left",
                "color": GRAPH_STYLE["text"],
                "font-family": FONT_STYLE["font-family"],
            },
        ),
        html.Div(
            children="How far are we from the target?",
            style={
                "textAlign": "left",
                "color": GRAPH_STYLE["text"],
                "font-family": FONT_STYLE["font-family"],
            },
        ),
        dcc.Graph(id="ghg-line-plot", figure=ghg_fig),
    ],
)
# ---------TABLE-----

ghg_table = dash_table.DataTable(
    id="ghg_table",
    columns=[{"id": c, "name": c} for c in ghg_df_selection_df.columns],
    style_cell={"font_family": FONT_STYLE["font-family"], "textAlign": "left"},
    style_cell_conditional=[{"if": {"column_id": "Value"}, "textAlign": "right"}],
    style_table={"height": "500px", "overflowY": "auto"},
    style_header={
        "backgroundColor": TABLE_STYLE["header_color"],
        "color": TABLE_STYLE["font_color"],
    },
    style_data={
        "backgroundColor": TABLE_STYLE["background_color"],
        "color": TABLE_STYLE["font_color"],
    },
)

content_first_row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="ghg-line-plot", figure=ghg_fig)),
                dbc.Col(ghg_table, width=3),
            ]
        ),
    ]
)

# ------TABLE CALLBACK----------


@app.callback(
    Output(component_id="ghg_table", component_property="data"),
    Input(component_id="ghg_dropdown", component_property="value"),
)
def update_ghg_table(val_chosen):
    # selects the corresponding dataframe from dropdown ghg choices
    print("\n\n\n")
    print(f"user choice: {val_chosen}")
    print(f"original type: {type(val_chosen)}")
    if isinstance(val_chosen, list):
        val_chosen = val_chosen[0]
        print(f"updated type: {type(val_chosen)}")
    print(ghg_gas_name_dict.get(val_chosen))
    return ghg_gas_name_dict.get(val_chosen).to_dict("records")


# -------------------APP LAYOUT---------------------------

content = html.Div(
    [
        html.H2("Climate Change Dashboard", style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
    ],
    id="page-content",
    style=CONTENT_STYLE,
)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

if __name__ == "__main__":
    app.run_server(debug=True)
