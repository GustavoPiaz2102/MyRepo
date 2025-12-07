import pandas as pd
import matplotlib.pyplot as plt

# Lendo CSV com vírgula como decimal
df = pd.read_csv('dados2.csv', decimal=',')

# Conferir os tipos (opcional)
print(df.dtypes)
print(df.head())

# Plotando
plt.figure(figsize=(10,6))
plt.plot(df['tempo'], df['deslocamento'], label='Deslocamento', color='blue', marker='o')
plt.plot(df['tempo'], df['força'], label='Força', color='red', marker='x')
plt.xlabel('Tempo')
plt.ylabel('Valores')
plt.title('Deslocamento e Força ao longo do Tempo')
plt.legend()
plt.grid(True)

# Salvar gráfico em PNG
plt.savefig('grafico.png', dpi=300)  # dpi=300 deixa o arquivo com boa qualidade

# Mostrar gráfico
plt.show()
