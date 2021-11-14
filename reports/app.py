import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash(__name__)

colors = {"background": "#ffffff", "text": "#000000"}
fonts = {"font-family": ["Arial", "Helvetica", "sans-serif"]}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
CH4_df = pd.read_pickle(
    "/Users/jamesmoro/Documents/Python/ClimateData/data/interim/CH4_df.pkl"
)
CO2_df = pd.read_pickle(
    "/Users/jamesmoro/Documents/Python/ClimateData/data/interim/CO2_df.pkl"
)
HFC_df = pd.read_pickle(
    "/Users/jamesmoro/Documents/Python/ClimateData/data/interim/HFC_df.pkl"
)
N2O_df = pd.read_pickle(
    "/Users/jamesmoro/Documents/Python/ClimateData/data/interim/N2O_df.pkl"
)
NF3_df = pd.read_pickle(
    "/Users/jamesmoro/Documents/Python/ClimateData/data/interim/NF3_df.pkl"
)
PFC_df = pd.read_pickle(
    "/Users/jamesmoro/Documents/Python/ClimateData/data/interim/PFC_df.pkl"
)
SF6_df = pd.read_pickle(
    "/Users/jamesmoro/Documents/Python/ClimateData/data/interim/SF6_df.pkl"
)





ghg_fig_country = "United Kingdom"

ghg_fig = go.Figure(
    data=go.Scatter(
        x=CH4_df[CH4_df["Country or Area"] == ghg_fig_country]["Year"],
        y=CH4_df[CH4_df["Country or Area"] == ghg_fig_country]["Value"],
    )
)


ghg_fig.update_layout(
    plot_bgcolor=colors["background"],
    paper_bgcolor=colors["background"],
    font_color=colors["text"],
    title_text=f"Methane Emissions - {ghg_fig_country}",
    xaxis_title='Year',
    yaxis_title='Temperature (degrees F)')
    font_size=18,
)


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
