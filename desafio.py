menu = """"
  [d] depositar
  [s] sacar
  [e] extrato
  [q] sair

==>"""

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
  opcao = input(menu)
  if opcao == "d":
    valor = float(input("Informe o valor do depósito: "))
    if valor <= 0 :
      print("Operação falhou. O valor tem de ser maior que 0 (zero)")
      continue
    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
  elif opcao == "s":
    valor = float(input("Informe o valor do saque: "))
    
    excedeu_saldo = valor > saldo
    excedeu_limites = valor > limite
    excedeu_saques = numero_saques > LIMITE_SAQUES

    if excedeu_saldo:
      print("Operação falhou. Você não tem saldo suficiente.")

    elif excedeu_limites:
      print("Operação falhou. Você excedeu o limite.")
    elif excedeu_saques:
      print("Operação falhou. Você excedeu o limite de saques.")
    elif valor > 0:
      saldo -= valor
      extrato += f"Saque: R$ {valor:.2f}"
      numero_saques += 1
    else:
      print("Operação falhou. O valor é inválido.")

  elif opcao == "e":
    extrato_str = "Não foram realizadas operações" if not extrato else extrato
    extrato_msg = f""""
    \n======== EXTRATO ========
    {extrato_str}

    Saldo: R$ {saldo:.2f}
    ---------------------------
    """
    print(extrato_msg)
  elif opcao == "q":
    break
  else:
    print("Opção inválida.")
