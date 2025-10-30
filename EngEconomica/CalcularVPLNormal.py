def calcular_vpl():
    print("=== Cálculo do VPL com PMT crescente ===")

    investimento_inicial = float(input("Investimento inicial (valor negativo se for saída de caixa): "))
    pmt_inicial = float(input("Valor do primeiro PMT (entrada mensal): "))
    taxa = float(input("Taxa de desconto mensal (em %): ")) / 100
    crescimento_pmt = float(input("Crescimento do PMT por mês (em %): ")) / 100
    meses = int(input("Número de meses: "))

    # Calcula o VPL
    vpl = -investimento_inicial  # começa com o valor investido (negativo)
    pmt_atual = pmt_inicial

    for mes in range(1, meses + 1):
        fluxo_descontado = pmt_atual / ((1 + taxa) ** mes)
        vpl += fluxo_descontado
        pmt_atual *= (1 + crescimento_pmt)  # aumenta o PMT conforme o crescimento

    print(f"\nO Valor Presente Líquido (VPL) é: R$ {vpl:.2f}")

# Executa o programa
if __name__ == "__main__":
    calcular_vpl()
