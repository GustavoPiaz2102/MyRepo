import re
import matplotlib.pyplot as plt
import csv
import math
import time
import os

def parse_file(filename):
    """Lê o arquivo data.txt com pesos e bias por epoch."""
    epochs = []
    with open(filename, "r") as f:
        for line in f:
            match = re.match(
                r"Epoch (\d+): Weights: \[([\d\.\-+eEinf]+), ([\d\.\-+eEinf]+)\], Bias: ([\d\.\-+eEinf]+)",
                line.strip()
            )
            if match:
                epoch = int(match.group(1))
                try:
                    w1 = float(match.group(2))
                    w2 = float(match.group(3))
                    b = float(match.group(4))
                    if math.isfinite(w1) and math.isfinite(w2) and math.isfinite(b):
                        epochs.append((epoch, w1, w2, b))
                except ValueError:
                    continue
    return epochs

def read_points(filename):
    """Lê o CSV e retorna os pontos (x, y) e labels (0 ou 1)."""
    points = []
    labels = []
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 3:
                    x = float(row[0])
                    y = float(row[1])
                    label = int(float(row[2]))
                    points.append((x, y))
                    labels.append(label)
    except FileNotFoundError:
        return [], []
    return points, labels

def parse_test_results(filename):
    """Lê o arquivo TestResults.txt e retorna os dados de teste."""
    test_data = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                match = re.match(
                    r"Input: \[([\d\.\-+]+), ([\d\.\-+]+)\], Expected: ([\d\.\-+]+), Predicted: (\d+)",
                    line.strip()
                )
                if match:
                    x = float(match.group(1))
                    y = float(match.group(2))
                    expected = float(match.group(3))
                    predicted = int(match.group(4))
                    test_data.append((x, y, expected, predicted))
    except FileNotFoundError:
        print(f"Arquivo {filename} não encontrado!")
    return test_data

def plot_animation(epochs, points, labels):
    if not epochs:
        return
    
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 8))

    # Limites do gráfico
    if points:
        x_min, x_max = min(p[0] for p in points) - 1, max(p[0] for p in points) + 1
        y_min, y_max = min(p[1] for p in points) - 1, max(p[1] for p in points) + 1
    else:
        x_min, x_max = -2, 2
        y_min, y_max = -2, 2
        
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True, linestyle='--', alpha=0.7)

    # Plotar os pontos de treino
    for (x, y), label in zip(points, labels):
        ax.scatter(x, y, c="blue" if label == 1 else "red", s=100, 
                  edgecolors="k", alpha=0.7)

    # Linha de decisão
    line, = ax.plot([], [], 'g-', linewidth=3)
    
    # Animação das epochs
    for i, (epoch, w1, w2, b) in enumerate(epochs):
        if abs(w2) > 1e-6:
            x_vals = [x_min, x_max]
            y_vals = [-(w1*x + b)/w2 for x in x_vals]
            line.set_data(x_vals, y_vals)
        elif abs(w1) > 1e-6:
            x_val = -b / w1
            line.set_data([x_val, x_val], [y_min, y_max])
        else:
            line.set_data([], [])

        ax.set_title(f"Epoch {epoch}\nw1={w1:.6f}, w2={w2:.6f}, bias={b:.6f}")
        plt.draw()
        plt.pause(0.000000000000001)
    
    plt.ioff()
    
    # Limpa os pontos de treino e mantém apenas a reta final
    ax.clear()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Plota apenas a linha de decisão final
    w1_final, w2_final, b_final = epochs[-1][1], epochs[-1][2], epochs[-1][3]
    if abs(w2_final) > 1e-6:
        x_vals = [x_min, x_max]
        y_vals = [-(w1_final*x + b_final)/w2_final for x in x_vals]
        ax.plot(x_vals, y_vals, 'g-', linewidth=3, label='Linha de Decisão Final')
    elif abs(w1_final) > 1e-6:
        x_val = -b_final / w1_final
        ax.axvline(x=x_val, color='g', linewidth=3, label='Linha de Decisão Final')
    
    ax.set_title("Linha de Decisão Final (Após Treinamento)")
    ax.legend()
    plt.draw()
    plt.pause(1.0)  # Pausa para mostrar a linha limpa
    
    return fig, ax

def plot_test_results(ax, test_data):
    """Plota os resultados do teste sobre o gráfico existente."""
    if not test_data:
        print("Nenhum dado de teste encontrado!")
        return
    
    # Plota pontos de teste
    correct_x = []
    correct_y = []
    incorrect_x = []
    incorrect_y = []
    
    for x, y, expected, predicted in test_data:
        if expected == predicted:
            correct_x.append(x)
            correct_y.append(y)
        else:
            incorrect_x.append(x)
            incorrect_y.append(y)
    
    # Pontos corretos em verde
    if correct_x:
        ax.scatter(correct_x, correct_y, c='green', s=150, marker='o', 
                  edgecolors='black', linewidth=2, label='Teste: Correto', alpha=0.8)
    
    # Pontos incorretos em laranja
    if incorrect_x:
        ax.scatter(incorrect_x, incorrect_y, c='blue', s=150, marker='x', 
                  linewidth=3, label='Teste: Incorreto', alpha=0.8)
    
    # Adiciona anotações para pontos incorretos
    for x, y, expected, predicted in test_data:
        if expected != predicted:
            ax.annotate(f'E:{expected} P:{predicted}', (x, y), 
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=8, color='red')
    
    # Calcula acurácia
    accuracy = len(correct_x) / len(test_data) * 100
    ax.set_title(f"Resultados do Teste - Acurácia: {accuracy:.1f}%\n"
                f"Verde: Correto ({len(correct_x)}), Laranja: Incorreto ({len(incorrect_x)})")
    
    ax.legend()
    plt.draw()

def RunCPPLinear():
    "LINEAR"    
    os.system("cd datasets && python3 GenData.py && cd ..")  
    os.system("./PerceptronLinear")

def RunCPPNonLinear():
    "LINEAR"    
    os.system("cd datasets && python3 GenData.py && cd ..")  
    os.system("./PerceptronNonLinear")

if __name__ == "__main__":
    RunCPPLinear()
    epochs = parse_file("data.txt")
    points, labels = read_points("datasets/linear.csv")
    
    # Animação do treinamento
    if epochs and points:
        fig, ax = plot_animation(epochs, points, labels)
        
        # Lê e plota resultados do teste
        test_data = parse_test_results("TestResults.txt")
        if test_data:
            plot_test_results(ax, test_data)
        plt.show()

    RunCPPNonLinear()
    epochs = parse_file("data.txt")
    points, labels = read_points("datasets/nonlinear.csv")
    
    # Animação do treinamento
    if epochs and points:
        fig, ax = plot_animation(epochs, points, labels)
        
        # Lê e plota resultados do teste
        test_data = parse_test_results("TestResults.txt")
        if test_data:
            plot_test_results(ax, test_data)
        plt.show()
