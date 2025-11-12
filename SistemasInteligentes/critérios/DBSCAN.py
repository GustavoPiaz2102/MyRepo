"""
Usa o DBscan para fazer os agrupamentos.
"""
from sklearn.cluster import DBSCAN
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import numpy as np

Ep = 0.9
MinS = 4

#carregando a irirs

iris = load_iris()
X = iris.data

#Aplicando o DBSCAN

dbscan = DBSCAN(eps=Ep, min_samples=MinS)

labels = dbscan.fit_predict(X)

print("Labels dos clusters:\n", labels)
print("Número de clusters encontrados:", len(set(labels)) - (1 if -1 in labels else 0))
print("Número de ruídos (outliers):", list(labels).count(-1))

#plotando o resultado

unique_labels = set(labels)
colors = plt.cm.get_cmap('Spectral', len(unique_labels))
for k in unique_labels:
    class_member_mask = (labels == k)
    xy = X[class_member_mask]
    plt.scatter(xy[:, 0], xy[:, 1], c=[colors(k)], label=f'Class {k}' if k != -1 else 'Noise', edgecolor='k', s=50)
plt.title('DBSCAN')
plt.xlabel('class 1')
plt.ylabel('class 2')
plt.legend()
plt.show()