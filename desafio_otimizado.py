menu = """
  [u]\tcriar usuário
  [c]\tcriar conta
  [l]\tlistar contas
  [d]\tdepositar
  [s]\tsacar
  [e]\textrato
  [q]\tsair

==>\t"""
CRIAR_USUARIO = "u"
CRIAR_CONTA = "c"
LISTAR_CONTAS = "l"
DEPOSITO = "d"
SAQUE = "s"
EXTRATO = "e"
SAIR = "q"

AGENCIA_PADRAO = "0001"
SALDO_INICIAL_PADRAO = 0.0
LIMITE_PADRAO = 500
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

usuarios = {}
sequencial_conta_corrente = 0


def obter_informacoes_novo_usuario():
    print("===> CADASTRAR USUÁRIO")
    nome = input("Digite o nome do usuário: ")
    data_de_nascimento = input("Digite a data de nascimento: ")
    cpf = input("Digite os números do CPF: ")
    logradouro = input("Digite o logradouro: ")
    numero = input("Digite o número do endereço: ")
    bairro = input("Digite o bairro: ")
    cidade = input("Digite a cidade: ")
    sigla_estado = input("Digite a sigla do estado: ")
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{sigla_estado}"
    return nome, data_de_nascimento, cpf, endereco


def cadastrar_usuario(nome, data_nascimento, cpf, endereco):
    if cpf in usuarios:
        print("ERRO: Já existe um usuário com esse CPF")
    else:
        novo_usuario = {
            "cpf": cpf,
            "nome": nome,
            "data_nascimento": data_nascimento,
            "endereco": endereco,
            "contas": [],
        }
        usuarios[cpf] = novo_usuario
        print("Usuário Cadastrado com Sucesso")


def obter_dados_nova_conta_corrente():
    cpf = input("Digite os números do CPF: ")
    if cpf in usuarios:
        return usuarios[cpf]
    else:
        print("Erro: CPF inexistente")
    return None


def cadastrar_conta_corrente(usuario):
    print("===> CADASTRAR CONTA CORRENTE")
    global sequencial_conta_corrente
    sequencial_conta_corrente += 1
    nova_conta = {
        "agencia": AGENCIA_PADRAO,
        "numero_conta": sequencial_conta_corrente,
        "saldo": SALDO_INICIAL_PADRAO,
        "extrato": [],
        "limite": LIMITE_PADRAO,
        "numero_saques": 0,
    }
    usuario['contas'].append(nova_conta)
    print("Nova Conta cadastrada com Sucesso")


def listar_contas():
    print("===> LISTA DE CONTAS")
    if usuarios:
        for usuario in usuarios.values():
            print(f"{usuario['cpf']}\t{usuario['nome']}\t{usuario['data_nascimento']}")
            if usuario['contas']:
                for conta in usuario['contas']:
                    print(f"\tAG: {conta['agencia']} - CC: {conta['numero_conta']} - SALDO:{conta['saldo']} - LIMITE: {conta['limite']} - SAQUES: {conta['numero_saques']}")
                    extrato_str = '\n\t\t'.join(conta['extrato'])
                    print(f"\t\t{extrato_str}")
            else:
                print("\tNenhuma conta cadastrada para esse usuário")
    else:
        print("Não há contas cadastradas")


def obter_dados_conta():
    cpf = input("Digite o CPF: ")
    agencia = str(input("Digite a agência: "))
    numero_conta = str(input("Digite o número da conta: "))
    usuario = None
    conta_corrente = None
    if cpf in usuarios:
        usuario = usuarios[cpf]
        contas = usuario["contas"]
        contas_correntes = list(filter(
            lambda conta: str(conta["agencia"]) == agencia
            and str(conta["numero_conta"]) == numero_conta,
            contas,
        ))
        if contas_correntes:
            conta_corrente = contas_correntes[0]
    return usuario, conta_corrente


def obter_informacoes_saque():
    print("===> SAQUE")
    usuario, conta_corrente = obter_dados_conta()
    if usuario is None:
        print("Erro: Usuário inexistente")
    elif conta_corrente is None:
        print("Erro: Conta inexistente")
    else:
        valor_saque = input("Digite o valor do saque: ")
    return usuario, conta_corrente, valor_saque


def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    valor = float(valor)
    excedeu_saldo = valor > saldo
    excedeu_limites = valor > limite
    excedeu_saques = numero_saques > limite_saques

    saldo_inicial = saldo
    if excedeu_saldo:
        print("Operação falhou. Você não tem saldo suficiente.")
    elif excedeu_limites:
        print("Operação falhou. Você excedeu o limite.")
    elif excedeu_saques:
        print("Operação falhou. Você excedeu o limite de saques.")
    elif valor > 0:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        numero_saques += 1
        print("Saque realizado com sucesso")
    else:
        print("Operação falhou. O valor é inválido.")

    if saldo == saldo_inicial:
        # Quando retornar o saldo -1 quer dizer que a operação falhou
        saldo = -1
    return saldo, extrato


def obter_dados_deposito():
    print("===> DEPÓSITO")
    usuario, conta_corrente = obter_dados_conta()
    valor_deposito = input("Digite o valor do depósito: ")
    return usuario, conta_corrente, valor_deposito


def deposito(saldo, valor, extrato, /):
    valor = float(valor)
    if valor <= 0:
        print("Operação falhou. O valor tem de ser maior que 0 (zero)")
        # Saldo será -1 para indicar que deu erro
        saldo = -1
    else:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print("Depósito realizado com sucesso")
    return saldo, extrato


def obter_dados_extrato():
    print("===> EXTRATO")
    _, conta_corrente = obter_dados_conta()
    return conta_corrente["saldo"], conta_corrente["extrato"]


def exibir_extrato(saldo, /, *, extrato):
    extrato_str = (
        "Não foram realizadas operações" if not extrato else "\n".join(extrato)
    )
    extrato_msg = f""""
  \n======== EXTRATO ========
  \t{extrato_str}

  Saldo: R$ {saldo:.2f}
  ---------------------------
  """
    print(extrato_msg)


def mostrar_menu():
    while True:
        opcao = input(menu)
        if opcao == CRIAR_USUARIO:
            nome, data_de_nascimento, cpf, endereco = obter_informacoes_novo_usuario()
            cadastrar_usuario(nome, data_de_nascimento, cpf, endereco)
        elif opcao == CRIAR_CONTA:
            usuario_conta = obter_dados_nova_conta_corrente()
            if usuario_conta:
                cadastrar_conta_corrente(usuario_conta)
        elif opcao == LISTAR_CONTAS:
            listar_contas()
        elif opcao == DEPOSITO:
            usuario, conta_corrente, valor_deposito = obter_dados_deposito()
            if usuario and conta_corrente:
                saldo, extrato = deposito(
                    conta_corrente["saldo"],
                    valor_deposito,
                    conta_corrente["extrato"].copy(),
                )
                if saldo != -1:
                    # Foi possível fazer o depósito
                    conta_corrente["saldo"] = saldo
                    conta_corrente["extrato"] = extrato
        elif opcao == SAQUE:
            usuario, conta_corrente, valor_saque = obter_informacoes_saque()
            if usuario and conta_corrente:
                saldo, extrato = saque(
                    saldo=conta_corrente["saldo"],
                    valor=valor_saque,
                    extrato=conta_corrente["extrato"].copy(),
                    limite=conta_corrente["limite"],
                    numero_saques=conta_corrente["numero_saques"],
                    limite_saques=LIMITE_SAQUES,
                )
                if saldo != -1:
                    # Foi possível fazer o saque
                    conta_corrente["saldo"] = saldo
                    conta_corrente["extrato"] = extrato
                    conta_corrente["numero_saques"] += 1

        elif opcao == EXTRATO:
            saldo, extrato_usuario = obter_dados_extrato()
            exibir_extrato(saldo, extrato=extrato_usuario)
        elif opcao == "q":
            break
        else:
            print("Opção inválida.")


mostrar_menu()
