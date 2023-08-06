import pandas as pd

burrows_data = "tables/alpha_parameters.csv"
beta_parameters = "tables/beta_parameters.csv"
nests_per_species = pd.read_csv(burrows_data)
parameters_per_species = pd.read_csv(beta_parameters)


def temporada():
    return nests_per_species["Temporada"][0]


def todos_nidos():
    return nests_per_species["Maxima_cantidad_nidos"][0]


def isla():
    return nests_per_species["Isla"][0]


def nidos_especie():
    return nests_per_species["Nidos_por_especie"][0]


def especie():
    return nests_per_species["Especie"][0]


def proporcion():
    nidos_especie = nests_per_species["Nidos_por_especie"][0]
    nidos_totales = nests_per_species["Maxima_cantidad_nidos"][0]
    proporcion = round(nidos_especie / nidos_totales, 2)
    return proporcion


def isla_de_interes():
    return parameters_per_species["Isla_de_interes"][0]


def isla_de_referencia():
    return parameters_per_species["Isla_de_referencia"][0]


def a():
    return parameters_per_species["a"][0]


def b():
    return parameters_per_species["b"][0]


def c():
    return parameters_per_species["c"][0]


def calculate_beta_index(a, b, c):
    beta = (b + c) / (2 * a + b + c)
    return beta


def beta_example():
    a = parameters_per_species["a"][0]
    b = parameters_per_species["b"][0]
    c = parameters_per_species["c"][0]
    beta_example = calculate_beta_index(a, b, c)
    rounded_beta = round(beta_example, 2)
    return rounded_beta
