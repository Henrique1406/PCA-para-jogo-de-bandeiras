Guess the Flag: PCA Edition
Um jogo interativo de "morte súbita" desenvolvido em Python que utiliza conceitos de Álgebra Linear e Processamento de Imagens para desafiar o conhecimento do jogador sobre bandeiras do mundo.

O projeto utiliza a Análise de Componentes Principais (PCA) para realizar a compressão e reconstrução de imagens. O diferencial deste projeto é a implementação manual do Método da Potência e da Técnica de Deflação para encontrar os autovetores e autovalores da matriz de covariância. Redução de Dimensionalidade: O PCA transforma as imagens originais em representações com menos colunas, preservando apenas as direções de maior variância (informação).Método da Potência: Um processo iterativo para encontrar o autovetor associado ao maior autovalor (a direção de maior "esticamento" dos dados).Deflação: Após encontrar o primeiro componente principal (PCA1), aplicamos a deflação para remover sua influência e extrair o próximo componente (PCA2), e assim sucessivamente.Reconstrução de Posto k: A imagem é reconstruída usando apenas k componentes. Quanto menor o valor de k, mais "borrada" e abstrata a bandeira se torna.

O objetivo é simples: adivinhar qual país a bandeira representa. O jogo começa com k = 6 (mais nítido). A cada duas rodadas, o valor de k diminui, tornando a imagem cada vez mais difícil de identificar.

Quanto menor o k (maior a dificuldade), mais pontos a rodada vale. Morte Súbita: Um erro encerra a partida.

Leaderboard: O jogo mantém um ranking dos 10 melhores jogadores em um arquivo scores.csv.
