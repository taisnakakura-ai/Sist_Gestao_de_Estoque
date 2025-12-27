# ==================================================================================
#                        SISTEMA DE CONTROLE DE ESTOQUE
# ==================================================================================
# Taís Nakakura

# Bibliotecas
import os
from colorama import Fore, init

init() #

# =========================================
# DICIONÁRIO PARA RECEBER DADOS DO ESTOQUE
# =========================================

estoque = {'produto a': {'quantidade': 10, 'preco': 25.5}, 'produto b': {'quantidade': 5, 'preco': 45.3}}
# Observação: Já deixei pré-preenchido com 2 itens para facilitar teste de todas as funcionalidades da ferramenta
#             sem precisar incluir produtos antes, mas podem ser apagados via menu ou substituídos por: estoque = {}

# =========================================
# FUNÇÕES
# =========================================

# 1. Auxiliares

# Limpa os dados do terminal
def limpar_tela(): 
    os.system('cls' if os.name == "nt" else "clear")

# Aguarda confirmação antes de seguir para o próximo comando
def pausa():
    input("Tecle ENTER para continuar ")

# 2. Funções modulares para manter mesmo estilo em diferentes telas

def cabecalho(texto):
    print(f"{texto.center(60)}")
    print('-' * 60)

def msg_sucesso(texto):
    print(f"{Fore.LIGHTBLACK_EX}\n{'-' * 60}")
    print(f"✅ {Fore.GREEN}{texto}")
    print(f"{Fore.LIGHTBLACK_EX}{'-' * 60}{Fore.RESET}")

def msg_erro(texto):
    print(f"{Fore.LIGHTBLACK_EX}\n{'-' * 60}")
    print(f"❌ {Fore.RED}{texto}{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}{'-' * 60}{Fore.RESET}")

# 3. Funções de tratamento de erros em input

def int_input(conteudo):
    while True:
        try:
            return int(input(conteudo))
        except ValueError:
            msg_erro("Este campo aceita apenas números")
    

def float_input(conteudo):
    while True:
        try:
            return float(input(conteudo))
        except ValueError:
            msg_erro("Este campo aceita apenas números. Ex.: 20.99")

# 4. Funções principais

def exibir_menu():
    print(f"{Fore.WHITE}\n{'='*8} MENU PRINCIPAL {'='*8}")
    print("      1. Adicionar produto")
    print("      2. Atualizar produto")
    print("      3. Excluir produto")
    print("      4. Visualizar estoque")
    print("      0. Sair do Sistema")
    print(f" {'='*33}\n{Fore.RESET}")
    

def escolher_opcao():
    while True:
        opcao = input("Selecione uma opção do menu acima: ")
                
        if opcao == "1":
            adicionar_produto()

        elif opcao == "2":
            atualizar_produto()

        elif opcao == "3":
            excluir_produto()
            
        elif opcao == "4":
            limpar_tela()
            cabecalho("VISUALIZAR ESTOQUE")
            ver_estoque()
            pausa()
            limpar_tela()
            exibir_menu()

        elif opcao == "0":
            limpar_tela()
            print(f"{Fore.GREEN}Você saiu do sistema.\n\n{Fore.RESET}")
            break
        else:
            msg_erro("Opção inválida")
            exibir_menu()


def submenu_continuar(funcao, mensagem):
    print(f"{Fore.YELLOW}\n{mensagem}")
    print(" s -> sim, continuar")
    print(f" n -> não, voltar ao menu principal {Fore.RESET}")
    
    escolha = input(f"\n Digite [s] ou [n] ")
    if escolha == "s":
        funcao()
    else:
        limpar_tela()
        exibir_menu()

# 5. Funções listadas no menu principal

def adicionar_produto():
    limpar_tela()
    cabecalho("ADICIONAR PRODUTO")
    produto = input("\nDigite o NOME do produto: ").lower()

    if produto in estoque:
        limpar_tela()
        msg_erro(f"Já existe um item {produto.upper()} no estoque")
        exibir_menu()
        return

    quantidade = int_input("Digite a QUANTIDADE em estoque: ")
    preco = float_input(f"Digite o PREÇO do produto: R$ ")

    estoque[produto] = {"quantidade": quantidade, "preco": preco}
    limpar_tela()
    msg_sucesso(f"Item {produto.upper()} cadastrado com sucesso")
    
    submenu_continuar(adicionar_produto, "Deseja adicionar outro produto? ")
        

def atualizar_produto():
    limpar_tela()
    cabecalho("ATUALIZAR PRODUTO")

    if not ver_estoque():
        pausa()
        limpar_tela()
        exibir_menu()
        return

    chaves = list(estoque.keys())
    while True:
        try:
            indice = int(input(f"\nDigite o número do item que deseja atualizar: "))
            if indice < 0 or indice >= len(estoque):
                msg_erro(f"Índice inexistente. Escolha um número da lista acima.")
                continue
            break
        except ValueError:
            msg_erro("Digite um número válido para o índice.")

    nome_produto = chaves[indice]
    produto = estoque[nome_produto]
    limpar_tela()
    print(f"{Fore.YELLOW}ITEM SELECIONADO: {nome_produto.title()}")
    print(f"\nQuantidade: {produto['quantidade']} | Preço: R$ {produto['preco']:.2f}\n{Fore.LIGHTBLACK_EX}")
    print(f"\nDigite os novos valores abaixo ou pressione ENTER para manter valor atual. {Fore.RESET}\n")

    while True:
        novo_nome = input("Nome do produto: ").lower().strip()
        if novo_nome == "":
            break

        if novo_nome in estoque:
            msg_erro(f"Já existe um produto com o nome '{novo_nome.upper()}'")
            continue

        estoque[novo_nome] = estoque.pop(nome_produto)
        nome_produto = novo_nome
        produto = estoque[nome_produto]
        break

    nova_qtd = input("Quantidade em estoque: ")
    if nova_qtd != "":
        produto["quantidade"] = int(nova_qtd)

    novo_preco = input("Preço unitário: ")
    if novo_preco != "":
        produto["preco"] = float(novo_preco)

    msg_sucesso(f"Item {nome_produto.upper()} atualizado.")

    submenu_continuar(atualizar_produto, "Deseja atualizar outro produto? ")


def ver_estoque(): 
    if not estoque:
        msg_erro("Não há itens no estoque. Por favor, escolha outra opção do menu")
        return False
  
    print(f"{Fore.LIGHTBLACK_EX}{'NOME DO PRODUTO'}{" "*24}{'QUANT.'}{" "*5}{'PREÇO'}")

    for indice, item in enumerate(estoque):
            print(f"{indice}. {item.title():37}{estoque[item]['quantidade']:4}{" "*6}R$ {estoque[item]['preco']:.2f}")

    print(f"{'-' * 60}{Fore.RESET}")
    return True


def excluir_produto():
    limpar_tela()
    cabecalho("EXCLUIR PRODUTO")

    if not ver_estoque():
        pausa()
        limpar_tela()
        exibir_menu()
        return

    chaves = list(estoque.keys())
    
    while True:
        try:
            indice = int(input(f"\nDigite o número do item que deseja excluir: "))
            if indice < 0 or indice >= len(estoque):
                msg_erro(f"Índice inexistente. Escolha um número da lista acima.")
                continue
            break
        except ValueError:
            msg_erro("Digite um número válido para o índice.")
    
    nome_produto = chaves[indice]
    del estoque[nome_produto]

    msg_sucesso(f"{nome_produto.upper()} excluído do estoque.")

    submenu_continuar(excluir_produto, "Deseja excluir outro produto do estoque? ")


# =========================================
# EXECUÇÃO DO SISTEMA
# =========================================

# Página inicial
print(f"{'='*60}\n{'LOJA DE ELETRÔNICOS UNIFECAF'.center(60)}\n{'='*60}")
print(f"\n\n\n\n\n{Fore.LIGHTBLACK_EX}Bem-vindo ao Sistema de Controle de Estoque.\n")
pausa()

# Menu Principal e seleção de opções
limpar_tela()
exibir_menu()
escolher_opcao()