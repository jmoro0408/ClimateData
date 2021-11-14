import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from figures.ghg_figure import ghg_fig

app = dash.Dash(__name__)

colors = {"background": "#ffffff", "text": "#000000"}
fonts = {"font-family": ["Arial", "Helvetica", "sans-serif"]}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


app.layout = html.Div(
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

if __name__ == "__main__":
    app.run_server(debug=True)
