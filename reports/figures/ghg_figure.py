import pandas as pd
import plotly.graph_objects as go

colors = {"background": "#ffffff", "text": "#000000"}
fonts = {"font-family": ["Arial", "Helvetica", "sans-serif"]}

# ROOT_DIR = r"/Users/jamesmoro/Documents/Python/ClimateData/data/interim/"
# DF_NAMES = (
#     "CH4_df",
#     "CO2_df",
#     "HFC_df",
#     "NF3_df",
#     "PFC_df",
#     "SF6_df",
#     "N20_df",
# )

combined_df_dir = r"/Users/jamesmoro/Documents/Python/ClimateData/data/interim/Combined_ghg_dataframe.pkl"
combined_df = pd.read_pickle(combined_df_dir)

# CH4_df = pd.read_pickle(ROOT_DIR + DF_NAMES[0] + ".pkl")
# CO2_df = pd.read_pickle(ROOT_DIR + DF_NAMES[1] + ".pkl")
# HFC_df = pd.read_pickle(ROOT_DIR + DF_NAMES[2] + ".pkl")
# NF3_df = pd.read_pickle(ROOT_DIR + DF_NAMES[3] + ".pkl")
# PFC_df = pd.read_pickle(ROOT_DIR + DF_NAMES[4] + ".pkl")
# SF6_df = pd.read_pickle(ROOT_DIR + DF_NAMES[5] + ".pkl")
# N20_df = pd.read_pickle(ROOT_DIR + DF_NAMES[6] + ".pkl")


ghg_gas_name_dict = {
    "Methane": "CH4 Emissions",
    "Carbon Dioxide": "CO2 Emissions",
    "Hydrofluorocarbons": "HFC Emissions",
    "Nitrogen trifluoride": "NF3 Emissions",
    "Perfluorocarbon": "PFC Emissions",
    "Sulfur Hexafluoride": "SF6 Emissions",
    "Nitrous Oxide": "N20 Emissions",
    "Combined Total": "Combined Total",
}


ghg_fig_country = "Australia"
ghg_df_selection_name = "Methane"
ghg_selection = ghg_gas_name_dict.get(ghg_df_selection_name)

ghg_countries = combined_df["Country"].unique()
ghg_fig = go.Figure(
    data=go.Scatter(
        x=combined_df[combined_df["Country"] == ghg_fig_country]["Year"],
        y=combined_df[combined_df["Country"] == ghg_fig_country][ghg_selection],
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
