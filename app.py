# Deployment link: [PASTE YOUR RENDER LINK HERE]
# Password: None

import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load your CSV
df = pd.read_csv("world_cup_finals.csv")

df["Winner"] = df["Winner"].replace({"West Germany": "Germany"})
df["RunnerUp"] = df["RunnerUp"].replace({"West Germany": "Germany"})

# Count wins
win_counts = df["Winner"].value_counts().reset_index()
win_counts.columns = ["Country", "Wins"]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard"),

    dcc.Graph(id="choropleth-map"),

    html.H2("Country Win Count"),
    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": c, "value": c} for c in sorted(win_counts["Country"].unique())],
        placeholder="Choose a country"
    ),
    html.Div(id="country-wins"),

    html.H2("Final Match Result by Year"),
    dcc.Dropdown(
        id="year-dropdown",
        options=[{"label": str(y), "value": y} for y in sorted(df["Year"].unique())],
        placeholder="Choose a year"
    ),
    html.Div(id="year-result")
])

@app.callback(
    Output("choropleth-map", "figure"),
    Input("country-dropdown", "value")
)
def update_map(selected_country):
    fig = px.choropleth(
        win_counts,
        locations="Country",
        locationmode="country names",
        color="Wins",
        color_continuous_scale="Blues",
        title="World Cup Wins by Country"
    )
    return fig

@app.callback(
    Output("country-wins", "children"),
    Input("country-dropdown", "value")
)
def show_country_wins(country):
    if not country:
        return ""
    wins = win_counts.loc[win_counts["Country"] == country, "Wins"].values[0]
    return html.P(f"{country} has won the FIFA World Cup {wins} time(s).")

@app.callback(
    Output("year-result", "children"),
    Input("year-dropdown", "value")
)
def show_year_result(year):
    if not year:
        return ""
    match = df[df["Year"] == year]
    if match.empty:
        return f"No data for {year}."
    winner = match["Winner"].values[0]
    runner_up = match["RunnerUp"].values[0]
    return html.P(f"In {year}, {winner} won against {runner_up}.")


import os

port = int(os.environ.get("PORT", 8050))
app.run(host="0.0.0.0", port=port, debug=True)
