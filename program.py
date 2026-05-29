import os
import time

import json
PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_QUIZES = os.path.join(PASTA, "quizes.json")
ARQUIVO_RANKING = os.path.join(PASTA, "ranking.json")

# -----------------------------------------------------------
# FUNÇÕES AUXILIARES
# -----------------------------------------------------------

def limpar_terminal():
    os.system('cls')

# -----------------------------------------------------------
# SISTEMA DE RANKING 
# -----------------------------------------------------------

def salvar_ranking(ranking):
    with open(ARQUIVO_RANKING, "w", encoding="utf-8") as arquivo:
        json.dump(ranking, arquivo, indent=4, ensure_ascii=False)

def adicionar_ranking_usuario(dados, pontos, nome):
    novo_ranking ={"id": len(dados) + 1, "nome": nome, "pontuacao": pontos}
    dados.append(novo_ranking)
    salvar_ranking(dados)

def mostrar_ranking():
    dados = carregar_quizzes(False)
    for i in range(0, len(dados)):
        print(f"{dados[i]['id']}°: {dados[i]['pontuacao']}, {dados[i]['nome']}")
    input("\nAperte enter para voltar.\n\n")
    time.sleep(1)


# -----------------------------------------------------------
# SISTEMA DE RESPOSTA 
# -----------------------------------------------------------

pontosUsuario = 0

def processa_resposta(resposta, pergunta_atual):
    if resposta == pergunta_atual:
         return 1
    return 0

# -----------------------------------------------------------
# SISTEMA DE PERGUNTAS 
# -----------------------------------------------------------

import random

def carregar_quizzes(is_quiz):
    if os.path.exists(ARQUIVO_QUIZES and ARQUIVO_RANKING):
        with open(ARQUIVO_QUIZES if is_quiz else ARQUIVO_RANKING, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        if is_quiz:
            return dados["quizzes"]
        return dados
    return []

def start_quiz():
    global pontosUsuario
    dados_quiz = carregar_quizzes(True)
    perguntas_lista = quiz_aleatorio(dados_quiz)

    print(f"Você irá fazer um quiz de {perguntas_lista['tema']}.")

    time.sleep(3)

    # -----------------------------------------------------------
    # LOOP PERGUNTAS 
    # -----------------------------------------------------------
    
    for i in range(0, len(perguntas_lista['perguntas'])):
        limpar_terminal()

        pergunta_atual = perguntas_lista['perguntas'][i]

        print("\n")
        print(pergunta_atual["pergunta"])
        print(f"\na){pergunta_atual['opcoes']['a']}\n"
            f"b){pergunta_atual['opcoes']['b']}\n"
            f"c){pergunta_atual['opcoes']['c']}\n"
            f"d){pergunta_atual['opcoes']['d']}\n")
        resposta = input("\nDigite sua resposta: ").upper()

        # VERIFICAÇÃO DA RESPOSTA + ADIÇÃO DOS PONTOS
        pontosUsuario += processa_resposta(resposta, pergunta_atual['resposta_correta'].upper()) 

        input("\nAperte enter para ir para a próxima pergunta.\n\n")
        time.sleep(1)

    print(f"Você fez {pontosUsuario * 20}% do quiz")

    dados_ranking = carregar_quizzes(False)
    adicionar_ranking_usuario(dados_ranking, str(pontosUsuario * 20), nomeUsuario)

    print("\nSua pontuação foi salva no ranking!")

    input("\nAperte enter para voltar.\n\n")
    time.sleep(1)

def quiz_aleatorio(dados):
    quiz = random.choice(dados) # ESCOLHE UM DOS QUIZZES
    random.shuffle(quiz["perguntas"]) # EMBARALHA AS PERGUNTAS
    return quiz


# -----------------------------------------------------------
# INTERAÇÃO COM O USUÁRIO 
# -----------------------------------------------------------

def processa_informacao(info):
    match info:
        case '1' | "INICIAR" | "INICIAR O QUIZ":
            start_quiz()
        case '2' | "VER" | "VER RANKING":
            mostrar_ranking()
        case '3' | "SAIR":
            return False

limpar_terminal()

nomeUsuario = input("Digite seu nome para começar o quiz: ")


while True:
    limpar_terminal()

    escolha = input(
        "╔══════════════════════════╗\n"
        "║        Quiz Geral        ║\n"
        "╠══════════════════════════╣\n"
        "║  1. Iniciar              ║\n"
        "║  2. Ver ranking          ║\n"
        "║  3. Sair                 ║\n"
        "╚══════════════════════════╝\n"
        "\nEscolha uma opção: "
    ).upper()

    if processa_informacao(escolha) == False:
        break