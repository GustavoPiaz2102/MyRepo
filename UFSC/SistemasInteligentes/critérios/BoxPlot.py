import matplotlib.pyplot as plt
"""
calculando ordenando o vetor,calculando a mediana, primeiro e terceiro quartis
"""
vet = [35,38,29,33,36,25,42,27,48,37,15,3,96,98]
vet.sort()
n = len(vet)
print("Vetor Ordenado:",vet)
if n % 2 == 0:
    mediana = (vet[n//2 - 1] + vet[n//2]) / 2
else:
    mediana = vet[n//2]
print("Mediana:",mediana)
if n % 2 == 0:
    q1 = (vet[n//4 - 1] + vet[n//4]) / 2
    q3 = (vet[3*n//4 - 1] + vet[3*n//4]) / 2
else:
    q1 = vet[n//4]
    q3 = vet[3*n//4]
print("Primeiro Quartil (Q1):",q1)
print("Terceiro Quartil (Q3):",q3)


#limite superior e inferior


li = q1 - 1.5 * (q3 - q1)
ls = q3 + 1.5 * (q3 - q1)
print("Limite Inferior:",li)
print("Limite Superior:",ls)


#fazendo box plot


plt.boxplot(vet)
plt.title("Box Plot do Vetor")
plt.ylabel("Valores")
plt.show()
#formula do IQR
"""
IQR = Q3 - Q1
Limite Inferior = Q1 - 1.5 * IQR
Limite Superior = Q3 + 1.5 * IQR
"""