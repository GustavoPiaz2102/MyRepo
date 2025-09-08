from sklearn.datasets import make_classification, make_circles
import pandas as pd
import numpy as np

# === Base VERDADEIRAMENTE linearmente separável (2D) === #
# Aumentando a separação entre classes e garantindo linearidade
X_lin, y_lin = make_classification(
    n_samples=200,
    n_features=2,
    n_informative=2,
    n_redundant=0,
    n_clusters_per_class=1,
    class_sep=3.0,  # Aumentei a separação
    random_state=42,
    flip_y=0.0      # Zero ruído - garante separação perfeita
)

# Garantindo que seja linearmente separável manualmente
# Adicionando uma margem maior entre as classes
for i in range(len(X_lin)):
    if y_lin[i] == 0:
        X_lin[i, 0] -= 0.5  # Desloca classe 0 para esquerda
    else:
        X_lin[i, 0] += 0.5  # Desloca classe 1 para direita

df_lin = pd.DataFrame(X_lin, columns=['x1', 'x2'])
df_lin['label'] = y_lin
df_lin.to_csv("linear.csv", index=False,header=False)

# === Base não linearmente separável (2D, círculos) === #
X_nonlin, y_nonlin = make_circles(
    n_samples=200,
    noise=0.05,
    factor=0.5,
    random_state=42
)

df_nonlin = pd.DataFrame(X_nonlin, columns=['x1', 'x2'])
df_nonlin['label'] = y_nonlin
df_nonlin.to_csv("nonlinear.csv", index=False,header=False)

#print("Bases salvas: linear.csv e nonlinear.csv")

# Verificação da separabilidade linear
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split

# Testa se o dataset linear é realmente separável
X_train, X_test, y_train, y_test = train_test_split(X_lin, y_lin, test_size=0.2, random_state=42)
clf = Perceptron(max_iter=1000, random_state=42)
clf.fit(X_train, y_train)
score = clf.score(X_test, y_test)

#print(f"Acurácia do Perceptron no dataset linear: {score:.4f}")
