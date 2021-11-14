import pandas as pd
import plotly.graph_objects as go

colors = {"background": "#ffffff", "text": "#000000"}
fonts = {"font-family": ["Arial", "Helvetica", "sans-serif"]}

ROOT_DIR = r"/Users/jamesmoro/Documents/Python/ClimateData/data/interim/"
DF_NAMES = (
    "CH4_df",
    "CO2_df",
    "HFC_df",
    "NF3_df",
    "PFC_df",
    "SF6_df",
    "N20_df",
)

CH4_df = pd.read_pickle(ROOT_DIR + DF_NAMES[0] + ".pkl")
CO2_df = pd.read_pickle(ROOT_DIR + DF_NAMES[1] + ".pkl")
HFC_df = pd.read_pickle(ROOT_DIR + DF_NAMES[2] + ".pkl")
NF3_df = pd.read_pickle(ROOT_DIR + DF_NAMES[3] + ".pkl")
PFC_df = pd.read_pickle(ROOT_DIR + DF_NAMES[4] + ".pkl")
SF6_df = pd.read_pickle(ROOT_DIR + DF_NAMES[5] + ".pkl")
N20_df = pd.read_pickle(ROOT_DIR + DF_NAMES[6] + ".pkl")


ghg_gas_name_dict = {
    "Methane": CH4_df,
    "Carbon Dioxide": CO2_df,
    "Hydrofluorocarbons": HFC_df,
    "Nitrogen trifluoride": NF3_df,
    "Perfluorocarbon": PFC_df,
    "Sulfur Hexafluoride": SF6_df,
    "Nitrous Oxide": N20_df,
}


ghg_fig_country = "Germany"
ghg_df_selection_name = "Perfluorocarbon"
ghg_df_selection_df = ghg_gas_name_dict.get(ghg_df_selection_name)
# table_df = ghg_df_selection_df[
#     ghg_df_selection_df["Country or Area"] == ghg_fig_country
# ]

ghg_countries = ghg_df_selection_df["Country or Area"].unique()
ghg_fig = go.Figure(
    data=go.Scatter(
        x=ghg_df_selection_df[
            ghg_df_selection_df["Country or Area"] == ghg_fig_country
        ]["Year"],
        y=ghg_df_selection_df[
            ghg_df_selection_df["Country or Area"] == ghg_fig_country
        ]["Value"],
    )
)

ghg_fig.update_layout(
    font_color=colors["text"],
    title_text=f"{ghg_df_selection_name} Emissions - {ghg_fig_country}",
    xaxis_title="Year",
    yaxis_title="Emissions (Tonnes)",
    font_size=18,
    template="ggplot2",
)
