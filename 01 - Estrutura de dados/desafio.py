import textwrap


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def depositar(contas, numero_conta, valor):
    conta = filtrar_conta(numero_conta, contas)

    if conta:
        if valor > 0:
            conta['saldo'] += valor
            conta['extrato'] += f"Depósito:\tR$ {valor:.2f}\n"
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    else:
        print("\n@@@ Conta não encontrada! @@@")


def sacar(contas, numero_conta, valor, limite, limite_saques):
    conta = filtrar_conta(numero_conta, contas)

    if conta:
        saldo = conta['saldo']
        extrato = conta['extrato']
        numero_saques = conta['numero_saques']

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= limite_saques

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif valor > 0:
            conta['saldo'] -= valor
            conta['extrato'] += f"Saque:\t\tR$ {valor:.2f}\n"
            conta['numero_saques'] += 1
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    else:
        print("\n@@@ Conta não encontrada! @@@")


def exibir_extrato(contas, numero_conta):
    conta = filtrar_conta(numero_conta, contas)

    if conta:
        saldo = conta['saldo']
        extrato = conta['extrato']

        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo:\t\tR$ {saldo:.2f}")
        print("==========================================")
    else:
        print("\n@@@ Conta não encontrada! @@@")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario, "saldo": 0, "extrato": "",
                "numero_saques": 0}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def filtrar_conta(numero_conta, contas):
    contas_filtradas = [conta for conta in contas if conta["numero_conta"] == numero_conta]
    return contas_filtradas[0] if contas_filtradas else None


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            numero_conta = int(input("Informe o número da conta: "))
            valor = float(input("Informe o valor do depósito: "))

            depositar(contas, numero_conta, valor)

        elif opcao == "s":
            numero_conta = int(input("Informe o número da conta: "))
            valor = float(input("Informe o valor do saque: "))

            sacar(contas, numero_conta, valor, limite=500, limite_saques=LIMITE_SAQUES)

        elif opcao == "e":
            numero_conta = int(input("Informe o número da conta: "))
            exibir_extrato(contas, numero_conta)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
