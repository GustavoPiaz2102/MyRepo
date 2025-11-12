"""
Isolation Forest para detecção de anomalias em dados.
"""
#====================================================
#Imports
#====================================================
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
#====================================================

# Gerando os dados e normais e anomalos e mesclando eles
np.random.seed(400)
X_normal = 0.3 * np.random.randn(100, 2) 
X_anomalous = np.random.uniform(low=-4, high=4, size=(20, 2)) 
X = np.r_[X_normal + 2, X_normal - 2, X_anomalous]
print("Dados Gerados:\n", X)
#====================================================

#Treinando o modelo Isolation Forest
clf = IsolationForest(contamination=0.1) 
clf.fit(X)
y_pred = clf.predict(X)
#comprimento n da arvore 
n_tree_length = [estimator.tree_.node_count for estimator in clf.estimators_]
#print("Comprimento n da árvore:", n_tree_length)
#====================================================

#plotando os valores
plt.scatter(X[:, 0], X[:, 1], c=y_pred, cmap='coolwarm', edgecolor='k')
plt.title("Plot isolation forest para a aula de sistemas inteligentes")
plt.xlabel("x")
plt.ylabel("y")
plt.show()