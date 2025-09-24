from sklearn.datasets import make_classification, make_circles
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split






# ==========================
# Dataset Linear
# ==========================
X_lin, y_lin = make_classification(
    n_samples=200,
    n_features=2,
    n_informative=2,
    n_redundant=0,
    n_clusters_per_class=1,
    class_sep=3.0,
    random_state=42,
    flip_y=0.0
)

# desloca levemente pra abrir mais espaço
for i in range(len(X_lin)):
    if y_lin[i] == 0:
        X_lin[i, 0] -= 0.5
    else:
        X_lin[i, 0] += 0.5

df_lin = pd.DataFrame(X_lin, columns=['x1', 'x2'])
df_lin['label'] = y_lin
df_lin.to_csv("linear.csv", index=False, header=False)







# ==========================
# Dataset "Não Linear" (mas quase linear)
# ==========================
X_nonlin, y_nonlin = make_classification(
    n_samples=200,
    n_features=2,
    n_informative=2,
    n_redundant=0,
    n_clusters_per_class=1,
    class_sep=1.2,  
    random_state=42,
    flip_y=0.01     
)

# Adicionaa uma leve Curvatura
X_nonlin[y_nonlin == 1, 1] += np.sin(X_nonlin[y_nonlin == 1, 0]) * 0.3


df_nonlin = pd.DataFrame(X_nonlin, columns=['x1', 'x2'])
df_nonlin['label'] = y_nonlin
df_nonlin.to_csv("nonlinear.csv", index=False, header=False)





#Local das Bases  (Dentro da pasta)
print("Bases salvas: linear.csv e nonlinear.csv")
