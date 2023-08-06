import numpy as np
import pandas as pd
import itertools


def get_bootstraped_lambda_from_group(
    group, seed=2, N=2000, csv_path="data/processed/results_growth_rates_taxon.csv"
):
    return [get_average_lambda_from_group(group, seed=i, csv_path=csv_path) for i in range(N)]


def get_average_lambda_from_group(
    group, seed=1, csv_path="data/processed/results_growth_rates_taxon.csv"
):
    resampled_lambdas = get_resampled_lambda_from_group(group, seed=seed, csv_path=csv_path)
    return np.mean(resampled_lambdas)


def get_resampled_lambda_from_group(
    group, seed=2, csv_path="data/processed/results_growth_rates_taxon.csv"
):
    np.random.seed(seed)
    resampled_species = get_resampled_species_from_group(group, seed, csv_path)
    resampled_lambdas = [
        resample_lambdas_by_species(species, np.random.randint(1, 100), csv_path).tolist()
        for species in resampled_species
    ]
    return list(itertools.chain.from_iterable(resampled_lambdas))


def get_group_list(csv_path="data/processed/results_growth_rates_taxon.csv"):
    growth_rates_data = pd.read_csv(csv_path)
    return growth_rates_data["Ordenes"].unique()


def get_species_list_from_group(group, csv_path="data/processed/results_growth_rates_taxon.csv"):
    growth_rates_data = pd.read_csv(csv_path)
    is_group = growth_rates_data["Ordenes"] == group
    filtered_growth_rates_data_by_group = growth_rates_data[is_group]
    return filtered_growth_rates_data_by_group["Nombre_ingles"].unique()


def get_island_count_from_species(
    species, csv_path="data/processed/results_growth_rates_taxon.csv"
):
    growth_rates_data = pd.read_csv(csv_path)
    is_species = growth_rates_data["Nombre_ingles"] == species
    filtered_growth_rates_data_by_species = growth_rates_data[is_species]
    return len(filtered_growth_rates_data_by_species)


def resample_lambdas_by_species(
    species, seed=2, csv_path="data/processed/results_growth_rates_taxon.csv"
):
    growth_rates_data = pd.read_csv(csv_path)
    island_count = get_island_count_from_species(species, csv_path)
    is_species = growth_rates_data["Nombre_ingles"] == species
    original_lambdas = growth_rates_data[is_species]["Tasa_de_crecimiento"]
    resampled_lambdas = original_lambdas.sample(n=island_count, replace=True, random_state=seed)
    return resampled_lambdas


def get_resampled_species_from_group(
    group, seed=1, csv_path="data/processed/results_growth_rates_taxon.csv"
):
    np.random.seed(seed)
    species_list = get_species_list_from_group(group, csv_path)
    resampled_species = np.random.choice(species_list, len(species_list))
    return resampled_species


def get_species_count_from_group(group, csv_path="data/processed/results_growth_rates_taxon.csv"):
    species_list = get_species_list_from_group(group, csv_path)
    return len(species_list)
