import pandas as pd
import matplotlib.pyplot as plt

from .calculate_growth_rates import fit_population_model
from geci_plots import geci_plot


def get_number_of_nests(path):
    data = pd.read_csv(
        path, usecols=["Species_name", "Island", "Season", "Maximum_number_of_nests"]
    )
    return data


def plot_log_linear_tendency(to_plot: dict, png_path: str, dpi=300):
    fontsize = "x-large"
    species_island_label = (
        to_plot["resources"][0]["species"] + " in " + to_plot["resources"][0]["island"]
    )
    x = to_plot["resources"][0]["data"][to_plot["scales"][0]["domain"]["field"]]
    y = to_plot["resources"][0]["data"][to_plot["scales"][1]["domain"]["field"]]
    fig, ax = geci_plot()
    ax.plot(
        x,
        y,
        to_plot["style"][0]["point"],
        label=species_island_label,
    )

    x = to_plot["resources"][1]["data"]["x"]
    y = to_plot["resources"][1]["data"]["y"]
    lambdas = str(to_plot["resources"][1]["lambda"])
    ax.plot(x, y, to_plot["style"][1]["line"], label="Fit model $\lambda=$" + lambdas)

    ax.set_xlabel(to_plot["scales"][0]["name"], fontsize=fontsize)
    ax.set_ylabel(to_plot["scales"][1]["name"], fontsize=fontsize)
    ax.set_yscale(to_plot["scales"][1]["type"])
    ax.set_xscale(to_plot["scales"][0]["type"])
    ax.legend(fontsize=fontsize)
    plt.savefig(png_path, dpi=dpi)
    return fig, ax


def get_to_plot_from_island_and_specie(
    nest_data, island, specie, lambda_csv="data/processed/results_growth_rates.csv"
):
    filter_data_by_specie = nest_data[nest_data.Species_name == specie]
    filter_data_by_specie_and_island = filter_data_by_specie[filter_data_by_specie.Island == island]
    filter_data_by_specie_and_island = filter_data_by_specie_and_island.sort_values(by="Season")
    x = [
        filter_data_by_specie_and_island["Season"].iloc[0],
        filter_data_by_specie_and_island["Season"].iloc[-1],
    ]
    model = fit_population_model(
        filter_data_by_specie_and_island["Season"],
        filter_data_by_specie_and_island["Maximum_number_of_nests"],
    )
    lambdas = get_lambda_from_csv(specie, island, lambda_csv)
    y = [model.iloc[0], model.iloc[-1]]
    TO_PLOT = {
        "resources": [
            {
                "name": "table",
                "data": filter_data_by_specie_and_island,
                "island": island,
                "species": specie,
            },
            {"name": "fitted_model", "data": {"x": x, "y": y}, "lambda": lambdas},
        ],
        "scales": [
            {
                "name": "Season",
                "type": "linear",
                "range": "width",
                "domain": {"data": "table", "field": "Season"},
            },
            {
                "name": "Logarithmic number of breeding pairs",
                "type": "log",
                "range": "height",
                "domain": {"data": "table", "field": "Maximum_number_of_nests"},
            },
        ],
        "style": [{"point": "o"}, {"line": "-k"}],
    }
    return TO_PLOT


def get_lambda_from_csv(species, island, csv_path="data/processed/results_growth_rates.csv"):
    data = pd.read_csv(csv_path)
    is_species_and_island = (data["Species"] == species) & (data["Island"] == island)
    filtered_by_species_and_island = data[is_species_and_island]
    growth_rate = filtered_by_species_and_island["Tasa_de_crecimiento_boostrap"].values[0]
    return growth_rate
