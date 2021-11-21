import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, dash_table, State
import plotly.graph_objects as go
import pandas as pd
from figures.ghg_figure import (
    ghg_fig,
    ghg_countries,
    ghg_gas_name_dict,
    ghg_df_selection_df,
)

# TODO Country selection doesnt show initial state on ghg table
# TODO update ghg graph title from list format to string
# TODO Check units
# TODO update dfs in app.py to combined df
# TODO add "world" to ghg df

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
            clearable=False,
            placeholder="Select a greenhouse gas",
        ),
        html.P("Country", style={"textAlign": "center"}),  # Countries
        dcc.Dropdown(
            id="ghg_country_dropdown",
            options=[{"label": country, "value": country} for country in ghg_countries],
            value=["Australia"],
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

# ----------GHG FIGURE CALLBACK---------


@app.callback(
    Output(component_id="ghg-line-plot", component_property="figure"),
    [
        Input(component_id="ghg_dropdown", component_property="value"),
        Input(component_id="ghg_country_dropdown", component_property="value"),
    ],
)
def update_ghg_figure(gas_chosen, fig_country_chosen):
    _chosen_gas_df = ghg_gas_name_dict.get(gas_chosen)
    _chosen_gas_df = _chosen_gas_df.sort_values(by="Year")
    if not isinstance(fig_country_chosen, list):
        fig_country_chosen = list(fig_country_chosen)
    updated_df = _chosen_gas_df[
        _chosen_gas_df["Country or Area"].isin(fig_country_chosen)
    ]

    fig = go.Figure(
        go.Scatter(
            x=updated_df["Year"],
            y=updated_df["Value"],
            mode="lines",
        )
    )

    if len(fig_country_chosen) > 1:
        fig = go.Figure()
        for country in fig_country_chosen:
            year = _chosen_gas_df[_chosen_gas_df["Country or Area"] == country]["Year"]
            value = _chosen_gas_df[_chosen_gas_df["Country or Area"] == country][
                "Value"
            ]

            fig.add_trace(go.Scatter(x=year, y=value, name=country, mode="lines"))

    fig.update_layout(
        font_color=GRAPH_STYLE["text"],
        title_text=f"{gas_chosen} Emissions - {*fig_country_chosen,}",
        xaxis_title="Year",
        yaxis_title="Emissions (Tonnes)",
        font_size=18,
        template="ggplot2",
    )

    return fig


# ------GHG TABLE CALLBACK----------


@app.callback(
    Output(component_id="ghg_table", component_property="data"),
    [
        Input(component_id="ghg_dropdown", component_property="value"),
        Input(component_id="ghg_country_dropdown", component_property="value"),
    ],
)
def ghg_table_callback(gas_chosen, country_chosen):
    # selects the corresponding dataframe from dropdown ghg choices
    if not isinstance(country_chosen, list):
        country_chosen = list(country_chosen)
    _chosen_gas_df = ghg_gas_name_dict.get(gas_chosen)
    _chosen_gas_country_df = _chosen_gas_df[
        _chosen_gas_df["Country or Area"].isin(country_chosen)
    ]

    return _chosen_gas_country_df.to_dict("records")


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
