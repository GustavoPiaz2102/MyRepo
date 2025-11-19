
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd

"""
ta batendo um 0.75 d r2 com esse encoder
da mais uma lida no ds e ve se tem algo que não ta tratado
ignora os comentarios no código , provavel q eu vou tirar dps
outra prd , eu to com future warning do pandas, c for usar outra versão talvez o interpretador reclame
"""

def encode_categorical_features(df): # vai retornar outro df só q codificado, era bom melhorar isso aq


    df = df.copy()
    label_encoders = {}



    # ======================== COLUNAS NUMÉRICAS ==========================



    """
    Basicamente pra tirar os caracteres e converter pra numerico
    """




    numeric_cols = [
        'Débitos', 'Ano', 'Cilindros', 'Portas', 'Rodas',
        'Airbags', 'Preco', 'Numero_proprietarios',
        'Historico_troca_oleo'
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].replace(['-', 'na', 'nan', ''], np.nan)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # ============================= KM  ===============================
    if 'Km' in df.columns:
        df['Km'] = (
            df['Km'].astype(str)
            .str.replace('km', '')
            .str.replace('.', '')
            .str.strip()
            .replace(['', '-', 'nan', 'na'], np.nan)
        )
        df['Km'] = pd.to_numeric(df['Km'], errors='coerce').fillna(0)

    # ======================== VOLUME MOTOR ============================
    if 'Volume_motor' in df.columns:
        df['Volume_motor'] = (
            df['Volume_motor'].astype(str)
            .str.lower()
            .str.replace('l', '')
            .str.replace('turbo', '') # c pah q eu deveria fazer uma ft extra pra turbo
            .str.replace(',', '.')
            .str.strip()
        )
        df['Volume_motor'] = df['Volume_motor'].replace(['', '-', 'na', 'nan'], np.nan)
        df['Volume_motor'] = pd.to_numeric(df['Volume_motor'], errors='coerce').fillna(0)

    # ========================= PORTAS =================================
    if 'Portas' in df.columns:
        df['Portas'] = df['Portas'].astype(str).str.split('-').str[0]
        df['Portas'] = pd.to_numeric(df['Portas'], errors='coerce').fillna(4)




    #======================== COLUNAS BINÁRIAS ==========================



    binary_cols = ['Couro', 'Adesivos_personalizados'] 

    for col in binary_cols:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                .str.lower()
                .str.strip()
                .map({'sim': 1, 'não': 0, 'nao': 0})
                .fillna(0)
            )

    # ---------------------- RADIO AM/FM ---------------------------
    if 'Radio_AM_FM' in df.columns:
        df['Radio_AM_FM'] = (
            df['Radio_AM_FM'].astype(str)
            .str.lower()
            .str.strip()
            .replace({
                'am': 0,
                'fm': 1,
                'am/fm': 2
            }) # eu acho que o tratamento pra nan só foi feito em binario, dps eu olho, qqr coisa eu ajeito aq dps
        )
        df['Radio_AM_FM'] = pd.to_numeric(df['Radio_AM_FM'], errors='coerce').fillna(1)

    # -------------------- LABEL ENCODING --------------------------
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    for col in categorical_cols:
        df[col] = df[col].astype(str).str.lower().str.strip()
        df[col] = df[col].replace(['', 'na', 'nan'], 'desconhecido')

        le = LabelEncoder()
        df[col] = le.fit_transform(df[col]) # aqui ta transformando a coluna inteira direto (Sim dava pra ter feito isso desde o começo :) <- isso era pra ser um pipe mas o teclado nao tem 
        label_encoders[col] = le 

    # ------------------ GARANTE DATAFRAME NUMÉRICO ----------------
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)


    return df, label_encoders 
