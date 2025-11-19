# IMPORTS
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

anoAtual = 2025
ignoredKeys = ['ID', 'Data_ultima_lavagem', 'Codigo_concessionaria', 'Cor']

# ============================ READ CSV =============================

def read_csv_file(file_path):
    """
    Lê o CSV e retorna apenas as colunas desejadas como dicionário.
    """
    df = pd.read_csv(file_path)
    df = df.drop(columns=[col for col in ignoredKeys if col in df.columns])
    return df.to_dict(orient="list")


# ============================ TRATE DATA ===========================

def trateData(data_dict):
    """
    Corrige os valores do dataset que estão mal formatados ou estranhos
    """
    df = pd.DataFrame(data_dict)

    #remove as linhas sem preço
    df['Preco'] = df['Preco'].replace(['nan', 'NA', 'na', ''], np.nan)
    df = df[df['Preco'].notna()]

    # sinceramente n mudou nada pra np nan
    df['Débitos'] = df['Débitos'].replace(['-', 'na', 'nan', ''], np.nan)


    df['Km'] = df['Km'].astype(str).str.lower()
    df['Km'] = df['Km'].replace(['nan', 'na', '-', ''], np.nan)

    df['Combustivel'] = df['Combustivel'].astype(str).str.lower() # SEMPRE PADRONIZAR PRA MINUSCULOOOOOOO
    df['Combustivel'] = df['Combustivel'].replace({
        'dies.': 'diesel',
        'gasol.': 'gasolina'
    })


    df['Ano'] = df['Ano'].astype(str).replace(['nan', 'na', '-', ''], np.nan)
    df['Ano'] = df['Ano'].apply(lambda x: anoAtual - int(x) if str(x).isdigit() else np.nan) #n entendi pq mas se eu colocar a idade do veiculo ao inves da data de fabricação ele funciona melhor :/ 

    return df.reset_index(drop=True)


# ============================ SEPARATE TRAIN TEST ===========================

def SeparateTrainTest(data, target_col='Preco', test_size=0.2, random_state=42): #nem mexe no argumento q vai cagar o modelo
    """
    Separa o dataset em treino e teste.
    """
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    if target_col not in data.columns:
        print("Colunas disponíveis:", data.columns.tolist()) # só pra verificar se tem mesmo um preco (vai ser irrelevante se continuar com o mesmo dataset)
        raise KeyError(f"Coluna '{target_col}' não encontrada.") 

    X = data.drop(target_col, axis=1)
    y = data[target_col]

    return train_test_split(X, y, test_size=test_size, random_state=random_state)
