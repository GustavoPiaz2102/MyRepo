"""
======================================================================

Sistemas Inteligentes - Projeto Final

Treino de modelo de regressão

======================================================================

Nome: Gustavo Piaz Da Silva
Matricula: 23200958

======================================================================

DATASET KEYS

======================================================================
ID
Débitos
Fabricante
Modelo
Ano
Categoria
Couro
Combustivel
Volume_motor
Km
Cilindros
Tipo_cambio
Tração
Portas
Rodas
Cor
Airbags
Preco
Numero_proprietarios
Data_ultima_lavagem
Adesivos_personalizados
Radio_AM_FM
Historico_troca_oleo
Codigo_concessionaria
Classificacao_Veiculo
Faixa_Preco

======================================================================


"""

# IMPORTS

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
from ReadDataSet import *


# READ AND CLEAR DATASET


# Lê e trata os dados
BruteData = read_csv_file('train.csv')
data = clearDataset(BruteData)
tratedData = trateData(data)

# Converte para DataFrame
df = pd.DataFrame(tratedData)

# Aplica encoding
df_encoded, encoders = encode_categorical_features(df)

# Separa treino e teste
X = df_encoded.drop('Preco', axis=1)
y = df_encoded['Preco']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Pronto para treinar! X_train shape: {X_train.shape}")

def trainModel(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

trained_model = trainModel(X_train, y_train)
y_pred = trained_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(f"Root Mean Squared Error (RMSE) on test set: {rmse}")