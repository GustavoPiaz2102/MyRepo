#Read a CSV
import pandas as pd
from sklearn.model_selection import train_test_split




ignoredKeys = ['ID', 'Data_ultima_lavagem', 'Codigo_concessionaria','Cor']




def clearDataset(data_dict):
    """
    Change all values to lowercase
    """
    for key in data_dict:
        data_dict[key] = [str(value).lower() for value in data_dict[key]]
    return data_dict

def read_csv_file(file_path):
    """
    Read a csv and return a dictionary with column names as keys and column data as values.
    """
    df = pd.read_csv(file_path)
    data_dict = {col: df[col].tolist() for col in df.columns if col not in ignoredKeys}
    return data_dict

def trateData(data_dict):

    #se preco for 'nan' remove toda a linha
    for i, price in enumerate(data_dict['Preco']):
        if price == 'nan':
            for key in data_dict:
                data_dict[key].pop(i)

    #se debito for - troca por 0
    for debits in data_dict['Débitos']:
        if debits == '-':
            data_dict['Débitos'][data_dict['Débitos'].index(debits)] = 0

    #se km for 'nan' troca por 0
    for kms in data_dict['Km']:
        if kms == 'nan':
            data_dict['Km'][data_dict['Km'].index(kms)] = "0 km"


    #converte dies. para diesel e gasol. para gasolina
    for fuels in data_dict['Combustivel']:
        if fuels == 'dies.':
            data_dict['Combustivel'][data_dict['Combustivel'].index(fuels)] = 'diesel'
        if fuels == 'gasol.':
            data_dict['Combustivel'][data_dict['Combustivel'].index(fuels)] = 'gasolina'
    
    return pd.DataFrame(data_dict)

def SeparateTrainTest(data, target_col='Preco', test_size=0.2, random_state=42):
    """
    Separate the dataset into training and testing sets.
    
    """
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    
    if target_col not in data.columns:
        print("Colunas disponíveis:", data.columns.tolist())
        raise KeyError(f"Coluna '{target_col}' não encontrada.")
    
    X = data.drop(target_col, axis=1)
    y = data[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    return X_train, X_test, y_train, y_test

    import pandas as pd


import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def encode_categorical_features(df):
    """
    Codifica todas as features categóricas para valores numéricos
    """
    df = df.copy()  # Evita modificar o DataFrame original
    
    # Define colunas que devem ser numéricas
    numeric_cols = ['Débitos', 'Ano', 'Cilindros', 'Portas', 'Rodas', 
                    'Airbags', 'Preco', 'Numero_proprietarios', 'Historico_troca_oleo']
    
    # 1. PROCESSA COLUNAS NUMÉRICAS
    for col in numeric_cols:
        if col in df.columns:
            # Substitui 'NA', '-', strings vazias por NaN
            df[col] = df[col].replace(['-', 'na', 'NA', ''], np.nan)
            # Converte para numérico
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Preenche NaN com 0 (ou use a mediana: df[col].median())
            df[col] = df[col].fillna(0)
    
    # 2. PROCESSA COLUNA KM (remove 'km' e converte)
    if 'Km' in df.columns:
        df['Km'] = df['Km'].astype(str).str.lower()
        df['Km'] = df['Km'].str.replace('km', '').str.strip()
        df['Km'] = df['Km'].replace(['na', '-', ''], '0')
        df['Km'] = pd.to_numeric(df['Km'], errors='coerce').fillna(0)
    
    # 3. PROCESSA VOLUME_MOTOR (remove 'l' e converte)
    if 'Volume_motor' in df.columns:
        df['Volume_motor'] = df['Volume_motor'].astype(str).str.lower()
        df['Volume_motor'] = df['Volume_motor'].str.replace('l', '').str.replace('turbo', '').str.strip()
        df['Volume_motor'] = df['Volume_motor'].replace(['na', '-', ''], '0')
        df['Volume_motor'] = pd.to_numeric(df['Volume_motor'], errors='coerce').fillna(0)
    
    # 4. PROCESSA PORTAS (converte "4-5" em 4)
    if 'Portas' in df.columns:
        df['Portas'] = df['Portas'].astype(str).str.split('-').str[0]
        df['Portas'] = pd.to_numeric(df['Portas'], errors='coerce').fillna(4)
    
    # 5. CODIFICA COLUNAS BINÁRIAS (Sim/Não)
    binary_cols = ['Couro', 'Adesivos_personalizados']
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip()
            df[col] = df[col].map({'sim': 1, 'não': 0, 'nao': 0}).fillna(0)
    
    # 6. CODIFICA RADIO_AM_FM
    if 'Radio_AM_FM' in df.columns:
        df['Radio_AM_FM'] = df['Radio_AM_FM'].astype(str).str.lower().str.strip()
        # Cria encoding: AM=0, FM=1, AM/FM=2
        radio_map = {'am': 0, 'fm': 1, 'am/fm': 2}
        df['Radio_AM_FM'] = df['Radio_AM_FM'].map(radio_map).fillna(1)
    
    # 7. IDENTIFICA E CODIFICA COLUNAS CATEGÓRICAS RESTANTES
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Remove a coluna target se estiver presente
    if 'Preco' in categorical_cols:
        categorical_cols.remove('Preco')
    
    # Aplica LabelEncoder
    label_encoders = {}
    for col in categorical_cols:
        try:
            le = LabelEncoder()
            # Converte para string e remove espaços
            df[col] = df[col].astype(str).str.strip().str.lower()
            # Substitui valores vazios ou NA
            df[col] = df[col].replace(['', 'na', 'nan'], 'desconhecido')
            # Aplica encoding
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le
        except Exception as e:
            print(f"Erro ao codificar coluna {col}: {e}")
            df[col] = 0
    
    # 8. GARANTE QUE TODAS AS COLUNAS SÃO NUMÉRICAS
    for col in df.columns:
        if df[col].dtype == 'object':
            print(f"Aviso: Coluna {col} ainda é object, convertendo para numérico...")
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    print(f"\n{'='*50}")
    print(f"RESUMO DO ENCODING:")
    print(f"{'='*50}")
    print(f"Shape final: {df.shape}")
    print(f"Colunas numéricas: {len(df.select_dtypes(include=[np.number]).columns)}")
    print(f"Colunas categóricas codificadas: {len(label_encoders)}")
    print(f"Tipos de dados:\n{df.dtypes.value_counts()}")
    print(f"{'='*50}\n")
    
    return df, label_encoders