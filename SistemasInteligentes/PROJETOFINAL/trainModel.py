"""
======================================================================

Sistemas Inteligentes - Projeto Final

Treino de modelo de regressão com random forest

======================================================================

Nome: Gustavo Piaz Da Silva
Matricula: 23200958

Nome: Pedro Thomás Silveira de Alcântara
Matricula: 23200955


======================================================================
"""


# IMPORTS

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from ReadDataSet import *
from encoder import encode_categorical_features

# ============================
# READ , CLEAN AND ENCODE DATA
# ============================

data = read_csv_file('train.csv')
tratedData = trateData(data)

df = pd.DataFrame(tratedData)

df_encoded, encoders = encode_categorical_features(df)

# Separação treino/teste                                     LEMBRAR DE DEFINIR OS VALORES DE SIZE NO COMEÇO DO ARQUIVO
X = df_encoded.drop('Preco', axis=1)# dropa o preco pq é o target
y = df_encoded['Preco']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ============================
# TREINO DO MODELO 
# ============================

def trainModel(n_estimators=500, max_depth=None, min_samples_split=2, min_samples_leaf=2,random_state=42):
    """
    Pipeline com normalização e random forest (Eu achei melhor usar rf do que regressão linear e o scaler por hora vai ficar o standart)
   
    LEMBRAR DE TESTAR OUTRO SCALER SE O R² NÃO SUBIR DE 0.8
    
    """ 
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("regressor", RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf= min_samples_leaf,
            random_state=random_state,
            n_jobs=-1 # usa todos os nucleos para fazer o treinamento (vou fazer no notebook se for pra treinar em serie)
        ))
    ])

    model.fit(X_train, y_train)
    return model


trained_model = trainModel()

# ============================
# AVALIAÇÃO
# ============================

y_pred = trained_model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.2f}")
print(f"R²  : {r2:.4f}")



#IGNORA O ACC MAS EU QUERIA COLOCAR ELE AQUI
accuracy = 100 - (rmse / y_test.mean()) * 100
accuracy = max(0, accuracy)  
print(f"Acc aproximada: {accuracy:.2f}%") 
# sinceramente eu coloquei o acc por birra pq n serve d nada pra regressão mas enfim
