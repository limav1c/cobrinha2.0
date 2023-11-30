import pygame
import random
from pygame.locals import *

pygame.init()

# tela do Jogo
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Cobrinha')
clock = pygame.time.Clock()  # tempo de movimentação

# função de gerar um número aleatório nas coordenadas
def posicao_aleatoria():
    x = random.randint(1, 590)
    y = random.randint(1, 590)
    return (x // 10 * 10, y // 10 * 10)

# função de colisão
def colisao(c1, c2):
    return c1[0] == c2[0] and c1[1] == c2[1]

# criando direcoes
cima = 0
direita = 1
baixo = 2
esquerda = 3

direcao = esquerda

# criando a cobrinha
cobrinha = [(200, 200), (210, 200), (220, 200)]  # segmentos da cobrinha nas posições
cobrinha_skin = pygame.Surface((10, 10))  # altura e largura
cobrinha_skin.fill((255, 255, 255))  # cor

# criando a maçã
maca_posicao = posicao_aleatoria()  # posição aleatória inicial
maca = pygame.Surface((10, 10))  # tamanho e largura da maçã
maca.fill((255, 0, 0))  # cor

while True:

    # velocidade de movimentação
    clock.tick(20)

    # eventos do jogo
    for event in pygame.event.get():
        # quando aperta o botão de fechar, o jogo sai
        if event.type == QUIT:
            pygame.quit()

        # direção da cobrinha com o teclado
        if event.type == KEYDOWN:
            if event.key == K_UP and direcao != baixo:
                direcao = cima
            if event.key == K_DOWN and direcao != cima:
                direcao = baixo
            if event.key == K_LEFT and direcao != direita:
                direcao = esquerda
            if event.key == K_RIGHT and direcao != esquerda:
                direcao = direita

    # ação de colidir com a maçã
    if colisao(cobrinha[0], maca_posicao):
        maca_posicao = posicao_aleatoria()  # caso haja colisão, ela aparece em um lugar aleatório da tela
        cobrinha.append((0, 0))  # nova posição da cobra, ela aumenta

    for i in range(len(cobrinha) - 1, 0, -1):
        cobrinha[i] = (cobrinha[i - 1][0], cobrinha[i - 1][1])  # toma posição da cauda anterior

    # posicoes da cobrinha
    if direcao == cima:
        cobrinha[0] = (cobrinha[0][0], cobrinha[0][1] - 10)
    if direcao == baixo:
        cobrinha[0] = (cobrinha[0][0], cobrinha[0][1] + 10)
    if direcao == direita:
        cobrinha[0] = (cobrinha[0][0] + 10, cobrinha[0][1])
    if direcao == esquerda:
        cobrinha[0] = (cobrinha[0][0] - 10, cobrinha[0][1])

    # verificação de colisão com a própria cobra
    for segmento in cobrinha[1:]:
        if colisao(cobrinha[0], segmento):
            pygame.quit()

    # verificação de colisão com a borda
    if cobrinha[0][0] < 0 or cobrinha[0][0] >= 800 or cobrinha[0][1] < 0 or cobrinha[0][1] >= 600:
        pygame.quit()

    screen.fill((0, 0, 0))  # limpa a tela
    screen.blit(maca, maca_posicao)  # desenha a maçã na tela

    for posicao in cobrinha:
        screen.blit(cobrinha_skin, posicao)  # desenha a cobrinha em cada posição

    pygame.display.update()
