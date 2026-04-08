import os
import random
import csv
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def potencia(C):
    n = C.shape[0]
    v = np.random.randn(n, 1) #vetor aleatorio
    if np.linalg.norm(v) == 0: #vetor nulo
        v = np.ones((n, 1))

    for _ in range(100):
        Cv = C @ v #multiplica a matriz C pelo vetor v
        norm_Cv = np.linalg.norm(Cv)
        if norm_Cv == 0: #divisão por zero
            return v, 0
        v = Cv / norm_Cv  #normaliza o vetor, a fim de evitar
                          #explosões nas contas
    λ = (v.T @ C @ v).item()
    return v, λ  #retorna o maior autovalor e o autovetor associado

def reconstruir_com_k(A, k):
    if np.all(A == 0):
        return A

    C = A @ A.T  #Acha a matriz C de Covariancia
    componentes = []    #guardará os autovetores(PCAs)
    lambdas = []        #guardará os autovalores(λ)

    for _ in range(k):
        v, λ = potencia(C) #acha v e λ via metodo da potencia
        componentes.append(v)
        lambdas.append(λ)
        C -= λ * (v @ v.T)  #aplica a tecnica da deflação

    A_rec = np.zeros_like(A)
    for i in range(len(componentes)):
        p = A.T @ componentes[i]  #calcula as projeçoes dos dados de A na direção de v
        A_rec += componentes[i] @ p.T  #Acha a melhor matriz de posto k

    return A_rec
#parte da pontuaçao
ARQUIVO_PONTUACOES = "scores.csv"

def exibir_pontuacoes():
    print("\n PLACAR DE LÍDERES ")
    try:
        with open(ARQUIVO_PONTUACOES, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)

            scores_validos = [row for row in reader if len(row) == 2 and row[1].isdigit()]

            scores = sorted(scores_validos, key=lambda x: int(x[1]), reverse=True)

            if not scores:
                print("Ainda não há pontuações válidas registradas!")
                return

            print(f"{'Pos.':<5} {'Nome':<20} {'Pontos':<10}")
            print("-" * 40)
            for i, (nome, pontos) in enumerate(scores[:10], 1):
                print(f"{i:<5} {nome:<20} {pontos:<10}")
        print("-" * 40)
    except (IOError, csv.Error) as e:
        print(f"Erro ao ler o arquivo de pontuações: {e}")


def salvar_pontuacao(nome, pontos):
    scores = {}

    try:
        if os.path.exists(ARQUIVO_PONTUACOES):
            with open(ARQUIVO_PONTUACOES, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)

                for row in reader:
                    if len(row) == 2 and row[1].isdigit():
                        player_name = row[0]
                        player_score = int(row[1])
                        if player_name not in scores or player_score > scores[player_name]:
                            scores[player_name] = player_score
    except (IOError, StopIteration):
        # Ignora erros de leitura ou arquivo vazio, começando com um placar limpo
        pass

    pontuacao_antiga = scores.get(nome, -1)

    if pontos > pontuacao_antiga:
        if pontuacao_antiga == -1:
            print(f"Ótima primeira pontuação, {nome}! Salva: {pontos} pontos.")
        else:
            print(f"🏆 Novo recorde pessoal para {nome}! De {pontuacao_antiga} para {pontos} pontos!")
        scores[nome] = pontos
    else:
        print(f"Sua pontuação de {pontos} não superou seu recorde de {pontuacao_antiga}. Tente de novo!")
        return # Não precisa reescrever o arquivo se nada mudou

    # Reescreve o arquivo inteiro
    try:
        with open(ARQUIVO_PONTUACOES, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Nome", "Pontos"]) # Escreve o cabeçalho
            for player_name, player_score in scores.items():
                writer.writerow([player_name, player_score])
    except IOError as e:
        print(f"Não foi possível salvar a pontuação: {e}")


def main():
    bandeiras = "flags"
    TOTAL_RODADAS = 100

    extensoes_validas = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
    if not os.path.exists(bandeiras):
        print(f"Erro: A pasta '{bandeiras}' não foi encontrada.")
        return
    todos_os_itens = os.listdir(bandeiras)
    arquivos = [f for f in todos_os_itens if f.lower().endswith(extensoes_validas)]
    if not arquivos:
        print(f"Erro: Nenhuma imagem válida foi encontrada na pasta '{bandeiras}'.")
        return

    random.shuffle(arquivos)

    print("=" * 50)
    print(" Bem-vindo ao Guess the Flag com PCA! ")
    print("=" * 50)

    exibir_pontuacoes()

    nome_jogador = ""
    while not nome_jogador:
        nome_jogador = input("\nDigite seu nome para começar: ").strip()

    print(f"\nOlá, {nome_jogador}! O jogo começará em breve! Morte súbita! Boa sorte!")
    print("-" * 50)

    pontos = 0
    rodadas_a_jogar = min(TOTAL_RODADAS, len(arquivos))

    for i in range(rodadas_a_jogar):
        k = max(1, 6 - (i // 2))  #A cada duas rodadas o k diminui, aumentando a dificuldade
        pontos_por_rodada = 6 - k + 1 # k=6 -> 1 pt, k=5 -> 2 pts, aumentando consecutivamente

        print(f"Rodada {i+1} de {rodadas_a_jogar} (Dificuldade k={k}, Vale {pontos_por_rodada} ponto(s))")

        nome_arquivo = arquivos[i]
        caminho = os.path.join(bandeiras, nome_arquivo)

        with Image.open(caminho) as img_original:
            largura_base = 200
            percentual_largura = (largura_base / float(img_original.size[0]))
            altura_calculada = int((float(img_original.size[1]) * float(percentual_largura)))
            img_pequena = img_original.resize((largura_base, altura_calculada), Image.Resampling.LANCZOS)
            img = Image.new("RGB", img_pequena.size, (255, 255, 255))
            img.paste(img_pequena, mask=img_pequena.convert('RGBA').split()[-1])

        img_array = np.array(img, dtype=np.float64) / 255.0
        R, G, B = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
        R_rec = reconstruir_com_k(R, k)
        G_rec = reconstruir_com_k(G, k)
        B_rec = reconstruir_com_k(B, k)
        img_rec = np.clip(np.stack([R_rec, G_rec, B_rec], axis=2), 0, 1)

        plt.figure(figsize=(8, 5))
        plt.imshow(img_rec)
        plt.title(f"Adivinhe a bandeira! (k={k})")
        plt.axis('off')
        plt.show(block=False)
        plt.pause(0.1)

        resposta = input("Qual é essa bandeira? ").strip().lower()
        nome_pais = os.path.splitext(nome_arquivo)[0].strip().lower()

        plt.close()

        if resposta == nome_pais:
            # 3. Adiciona os pontos da rodada
            print(f"✅ Correto! +{pontos_por_rodada} ponto(s)!\n")
            pontos += pontos_por_rodada
        else:
            print(f"❌ Errado! A resposta era: {nome_pais.capitalize()}.")
            print("Fim de jogo para você!")
            break

    print("=" * 50)
    print("🏁 Fim de Jogo! 🏁")
    print(f"{nome_jogador}, sua pontuação final foi: {pontos}")

    salvar_pontuacao(nome_jogador, pontos)
    exibir_pontuacoes()

if __name__ == "__main__":
    main()