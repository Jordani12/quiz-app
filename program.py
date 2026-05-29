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

def mostrar_ranking(dados):
    ranking_ordenado = sorted(dados, key=lambda x: int(x['pontuacao']), reverse=True)
    for i, entrada in enumerate(ranking_ordenado, start=1):
        print(f"{i}°: {entrada['nome']} - {entrada['pontuacao']}%")

# -----------------------------------------------------------
# SISTEMA DE RESPOSTA 
# -----------------------------------------------------------

def processa_resposta(resposta, pergunta_atual):
    if resposta == pergunta_atual:
         return 1
    return 0

# -----------------------------------------------------------
# SISTEMA DE PERGUNTAS 
# -----------------------------------------------------------

import random

def carregar_quizzes():
    if os.path.exists(ARQUIVO_QUIZES):
        with open(ARQUIVO_QUIZES, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados["quizzes"]
    return []

def carregar_ranking():
    if os.path.exists(ARQUIVO_RANKING):
        with open(ARQUIVO_RANKING, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados
    return []

def start_quiz():
    pontos = 0

    dados_quiz = carregar_quizzes()
    perguntas_lista = quiz_aleatorio(dados_quiz)

    print(f"Você irá fazer um quiz de {perguntas_lista['tema']}.")

    time.sleep(3)

    # -----------------------------------------------------------
    # LOOP PERGUNTAS 
    # -----------------------------------------------------------
    
    for pergunta_atual in perguntas_lista['perguntas']:
        limpar_terminal()

        print("\n")
        print(pergunta_atual['pergunta'])
        print(f"\na){pergunta_atual['opcoes']['a']}\n"
            f"b){pergunta_atual['opcoes']['b']}\n"
            f"c){pergunta_atual['opcoes']['c']}\n"
            f"d){pergunta_atual['opcoes']['d']}\n")
        
        resposta = input("\nDigite sua resposta: ").upper()
        pontos += processa_resposta(resposta, pergunta_atual['resposta_correta'].upper()) 

        input("\nAperte enter para ir para a próxima pergunta.\n\n")
        time.sleep(0.5)

    total_perguntas = len(perguntas_lista['perguntas'])
    porcentagem = round((pontos / total_perguntas) * 100)

    print(f"Você fez {porcentagem}% do quiz")

    dados_ranking = carregar_ranking()
    adicionar_ranking_usuario(dados_ranking, porcentagem, nomeUsuario)

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
            return True
        case '2' | "VER" | "VER RANKING":
            dados_ranking = carregar_ranking()
            mostrar_ranking(dados_ranking)
            return True
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

    if not processa_informacao(escolha):
        break
    input("\nVoltar - pressione ENTER\n\n")