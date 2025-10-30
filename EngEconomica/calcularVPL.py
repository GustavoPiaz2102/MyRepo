def CalcularVPL(i, n, pmt, pv):
    value = -pv
    for t in range(1, n+1):
        value += pmt / ((1 + i) ** t)
    return value

i = float(input("Digite a taxa (ex: 0.1 para 10%): "))
n = int(input("Período: "))
pmt = float(input("PMT: "))
pv = float(input("PV (investimento inicial): "))

VPL = CalcularVPL(i, n, pmt, pv)
print(f"Valor do VPL: {VPL:.2f}")
