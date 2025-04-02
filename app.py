{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "d6165812-ca24-4cb7-bed8-a066525081f0",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "        <iframe\n",
       "            width=\"100%\"\n",
       "            height=\"650\"\n",
       "            src=\"http://127.0.0.1:8050/\"\n",
       "            frameborder=\"0\"\n",
       "            allowfullscreen\n",
       "            \n",
       "        ></iframe>\n",
       "        "
      ],
      "text/plain": [
       "<IPython.lib.display.IFrame at 0x18c7acdaab0>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# app.py\n",
    "# Deployment link: [PASTE LINK HERE]\n",
    "# Password (if any): [PASTE HERE]\n",
    "\n",
    "import dash\n",
    "from dash import dcc, html, Input, Output\n",
    "import pandas as pd\n",
    "import plotly.express as px\n",
    "\n",
    "# === Load World Cup data ===\n",
    "df = pd.read_csv(\"world_cup_finals.csv\")\n",
    "\n",
    "# Treat West Germany as Germany (if present)\n",
    "df[\"Winner\"] = df[\"Winner\"].replace({\"West Germany\": \"Germany\"})\n",
    "df[\"RunnerUp\"] = df[\"RunnerUp\"].replace({\"West Germany\": \"Germany\"})\n",
    "\n",
    "# Count wins per country\n",
    "win_counts = df[\"Winner\"].value_counts().reset_index()\n",
    "win_counts.columns = [\"Country\", \"Wins\"]\n",
    "\n",
    "# === Start Dash App ===\n",
    "app = dash.Dash(__name__)\n",
    "\n",
    "app.layout = html.Div([\n",
    "    html.H1(\"FIFA World Cup Dashboard\"),\n",
    "\n",
    "    # Step 2a: Choropleth map\n",
    "    html.H2(\"World Cup-Winning Countries\"),\n",
    "    dcc.Graph(id=\"choropleth-map\"),\n",
    "\n",
    "    # Step 2b: Select country for win count\n",
    "    html.H2(\"Country Win Count\"),\n",
    "    html.Label(\"Select a country:\"),\n",
    "    dcc.Dropdown(\n",
    "        id=\"country-dropdown\",\n",
    "        options=[{\"label\": c, \"value\": c} for c in sorted(win_counts[\"Country\"].unique())],\n",
    "        placeholder=\"Choose a country\"\n",
    "    ),\n",
    "    html.Div(id=\"country-wins\"),\n",
    "\n",
    "    # Step 2c: Select year for final result\n",
    "    html.H2(\"Final Match Result by Year\"),\n",
    "    html.Label(\"Select a year:\"),\n",
    "    dcc.Dropdown(\n",
    "        id=\"year-dropdown\",\n",
    "        options=[{\"label\": str(y), \"value\": y} for y in sorted(df[\"Year\"].unique())],\n",
    "        placeholder=\"Choose a year\"\n",
    "    ),\n",
    "    html.Div(id=\"year-result\")\n",
    "])\n",
    "\n",
    "# === Callbacks ===\n",
    "\n",
    "# Step 2a: Choropleth map of winning countries\n",
    "@app.callback(\n",
    "    Output(\"choropleth-map\", \"figure\"),\n",
    "    Input(\"country-dropdown\", \"value\")  # triggers map redraw (optional interactivity)\n",
    ")\n",
    "def update_map(selected_country):\n",
    "    fig = px.choropleth(\n",
    "        win_counts,\n",
    "        locations=\"Country\",\n",
    "        locationmode=\"country names\",\n",
    "        color=\"Wins\",\n",
    "        color_continuous_scale=\"Blues\",\n",
    "        title=\"World Cup Wins by Country\"\n",
    "    )\n",
    "    return fig\n",
    "\n",
    "# Step 2b: Show number of wins for selected country\n",
    "@app.callback(\n",
    "    Output(\"country-wins\", \"children\"),\n",
    "    Input(\"country-dropdown\", \"value\")\n",
    ")\n",
    "def show_country_wins(country):\n",
    "    if not country:\n",
    "        return \"\"\n",
    "    wins = win_counts.loc[win_counts[\"Country\"] == country, \"Wins\"].values[0]\n",
    "    return html.P(f\"{country} has won the FIFA World Cup {wins} time(s).\")\n",
    "\n",
    "# Step 2c: Show final result for selected year\n",
    "@app.callback(\n",
    "    Output(\"year-result\", \"children\"),\n",
    "    Input(\"year-dropdown\", \"value\")\n",
    ")\n",
    "def show_year_result(year):\n",
    "    if not year:\n",
    "        return \"\"\n",
    "    row = df[df[\"Year\"] == year].iloc[0]\n",
    "    return html.P(f\"In {year}, {row['Winner']} won against {row['RunnerUp']}.\")\n",
    "\n",
    "# Run app\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=True)  \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c3bbae69-4c9f-4258-99a8-8533235d9a80",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3f155d67-1ad9-456c-9945-d6beda64280c",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
