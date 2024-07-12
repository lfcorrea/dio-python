from abc import ABC, abstractmethod
from datetime import datetime

class ContaIterador:
    def __init__(self, contas) -> None:
        self.contas = contas
        self.contador = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            conta = self.contas[self.contador]
            self.contador += 1
            return conta
        except IndexError:
            raise StopIteration


class Cliente:
    def __init__(self, endereco) -> None:
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("\nERRO: Número máximo de transações diárias alcançado!")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.conta.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco) -> None:
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente) -> None:
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def cliente(self):
        return self._cliente

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor) -> bool:
        valor = float(valor)
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nERROR: O valor do saque não pode ser maior que o valor do saldo")
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True
        else:
            print("\nERRO: O valor não pode ser negativo")
        return False

    def depositar(self, valor) -> bool:
        valor = float(valor)
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso")
            return True
        print("\nERRO: Valor inválido para depositar")
        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3) -> None:
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        valor = float(valor)
        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == Saque.__name__
            ]
        )

        excedeu_limite_saques = numero_saques >= self.limite_saques
        excedeu_limite = valor > self.limite
        if excedeu_limite_saques:
            print("\nERRO: O limite de saques foi excedido!")
        elif excedeu_limite:
            print("\nERRO: O limite do valor do saque foi excedido!")
        else:
            return super().sacar(valor)
        return False

    def __str__(self) -> str:
        return f"Cliente:{self.cliente.nome}\tAG:{self.agencia}\tCC: {self.numero}\tSaldo: {self.saldo}\tLimite: {self.limite}\tLimite Saques: {self.limite_saques}"


class Historico:
    def __init__(self) -> None:
        self._transacoes = []
        self._date_format = "%d-%m-%Y %H:%M"

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": float(transacao.valor),
                "data": datetime.now().strftime(self._date_format),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"] == tipo_transacao.lower():
                yield transacao

    def transacoes_do_dia(self):
        hoje = datetime.now().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao['data'], self._date_format).date()
            if data_transacao == hoje:
                transacoes.append(transacao)
        return transacoes



class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


def log_transacao(func, *args, **kwargs):
    def envelope(*args, **kwargs):
        ts = datetime.now().strftime("%d-%m-%Y %H:%M:%s")
        resultado = func(*args, **kwargs)
        print(f"{ts}\t{func.__name__}")
        return resultado
    return envelope

CRIAR_USUARIO = "u"
CRIAR_CONTA = "c"
LISTAR_CONTAS = "l"
DEPOSITO = "d"
SAQUE = "s"
EXTRATO = "e"
SAIR = "q"


def menu():
    menu = """
    [u]\tcriar usuário
    [c]\tcriar conta
    [l]\tlistar contas
    [d]\tdepositar
    [s]\tsacar
    [e]\textrato
    [q]\tsair

    ==>\t"""
    return input(menu)


@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("ERRO: Cliente não encontrado!")
        return None
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print("ERRO: Cliente não possui conta!")
        return None
    valor = input("Informe o valor do depósito: ")
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)


@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("ERRO: Cliente não encontrado!")
        return None
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print("ERRO: Cliente não possui conta!")
        return None
    valor = input("Informe o valor do saque: ")
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


def filtrar_cliente(cpf, clientes):
    clientes = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes[0] if clientes else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nERRO: Cliente não possui conta")
        return None
    return cliente.contas[0]


@log_transacao
def exibir_extrato(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("ERRO: Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("ERRO: O cliente não possui conta!")
        return

    print("=============EXTRATO===============")
    transacoes = conta.historico.transacoes
    extrato = "Não foram encontradas transações"
    if transacoes:
        extrato = ""
        for transacao in conta.historico.gerar_relatorio():
            extrato += f"\n{transacao['data']}\t{transacao['tipo']}:\t{transacao['valor']:.2f}"

    print(extrato)
    print(f"SALDO: R$ {float(conta.saldo):.2f}")
    print("=================================")


def criar_cliente(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("ERRO: Cliente já existe")
        return

    nome = input("Digite o nome do cliente: ")
    data_nascimento = input("Digite a data de nascimento: ")
    endereco = input("Digite o endereço do cliente: ")
    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco
    )
    clientes.append(cliente)

    print("Cliente criado")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("ERRO: Cliente não encontrado")
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso")


def listar_contas(contas):
    # TODO: usar o iterador
    for conta in ContaIterador(contas):
        print("=========================")
        print(str(conta))


def main():
    clientes = []
    contas = []
    while True:
        opcao = menu()
        if opcao == CRIAR_USUARIO:
            criar_cliente(clientes)
        elif opcao == CRIAR_CONTA:
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == LISTAR_CONTAS:
            listar_contas(contas)
        elif opcao == DEPOSITO:
            depositar(clientes)
        elif opcao == SAQUE:
            sacar(clientes)
        elif opcao == EXTRATO:
            exibir_extrato(clientes)
        elif opcao == "q":
            break
        else:
            print("ERRO: Opção inválida.")


main()
