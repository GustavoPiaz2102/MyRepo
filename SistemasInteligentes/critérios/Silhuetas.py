"""

s(i)=b(i)-a(i)/max(a(i),b(i))

"""

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.datasets import make_blobs
from sklearn.datasets import load_iris

maior_score = -1
Best_k = 0
BestLabels = None

#for para a melhor quantidade de clusters
for i in range(2, 150, 2):
    #  Gera exemplos de dados para a analise
    #X, y = make_blobs(n_samples=1000, centers=i, cluster_std=0.60, random_state=0)
    iris = load_iris()
    X = iris.data
    kmeans = KMeans(n_clusters=i, random_state=0)


#  Preve os resultados com base no valores gerados
    labels = kmeans.fit_predict(X)

    score = silhouette_score(X, labels)
    if score > maior_score:
        maior_score = score
        Best_k = i
        BestLabels = labels

print("Melhor número de clusters:", Best_k)
print("Melhor Silhouette Score:", maior_score)
