import pygame
import random

# Inicializa o Pygame
pygame.init()

# Define as cores
AZUL_CLARO = (135, 206, 250)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Define o tamanho da tela
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

# Título da janela
pygame.display.set_caption("Jogo de Educação Financeira")

# Define FPS (frames por segundo)
clock = pygame.time.Clock()

# Carrega as imagens da cesta, moeda, perda e renda variável, redimensionando para 30x30 pixels
imagem_cesta = pygame.image.load("Jogo_esquiva/cesta.png")
imagem_cesta = pygame.transform.scale(imagem_cesta, (150, 100))

imagem_moeda = pygame.image.load("Jogo_esquiva/moeda.png")
imagem_moeda = pygame.transform.scale(imagem_moeda, (30, 30))

imagem_perda = pygame.image.load("Jogo_esquiva/perda.png")
imagem_perda = pygame.transform.scale(imagem_perda, (30, 30))

imagem_variavel = pygame.image.load("Jogo_esquiva/variavel.png")
imagem_variavel = pygame.transform.scale(imagem_variavel, (30, 30))

largura_item = 30
altura_item = 30
velocidade_item = 5

# Define o jogador (posição da cesta)
largura_jogador = imagem_cesta.get_width()
altura_jogador = imagem_cesta.get_height()
x_jogador = LARGURA_TELA // 2 - largura_jogador // 2
y_jogador = ALTURA_TELA - altura_jogador - 10
velocidade_jogador = 7

# Listas para armazenar os itens
moedas = []
perdas = []
variaveis = []

for _ in range(5):
    x_moeda = random.randint(0, LARGURA_TELA - largura_item)
    y_moeda = random.randint(-100, -40)
    moedas.append([x_moeda, y_moeda])

for _ in range(3):
    x_perda = random.randint(0, LARGURA_TELA - largura_item)
    y_perda = random.randint(-100, -40)
    perdas.append([x_perda, y_perda])

for _ in range(2):
    x_variavel = random.randint(0, LARGURA_TELA - largura_item)
    y_variavel = random.randint(-100, -40)
    variaveis.append([x_variavel, y_variavel])

saldo = 0

# Funções para desenhar
def desenha_jogador(x, y):
    tela.blit(imagem_cesta, (x, y))

def desenha_moeda(moeda_x, moeda_y):
    tela.blit(imagem_moeda, (moeda_x, moeda_y))

def desenha_perda(perda_x, perda_y):
    tela.blit(imagem_perda, (perda_x, perda_y))

def desenha_variavel(variavel_x, variavel_y):
    tela.blit(imagem_variavel, (variavel_x, variavel_y))

def desenha_menu():
    tela.fill(AZUL_CLARO)
    fonte_menu = pygame.font.SysFont(None, 48)
    texto_titulo = fonte_menu.render("Jogo de Educação Financeira", True, PRETO)
    tela.blit(texto_titulo, (LARGURA_TELA // 2 - texto_titulo.get_width() // 2, 150))

    botao_iniciar = pygame.Rect(LARGURA_TELA // 2 - 100, 250, 200, 50)
    pygame.draw.rect(tela, PRETO, botao_iniciar)
    texto_iniciar = fonte_menu.render("Iniciar", True, AZUL_CLARO)
    tela.blit(texto_iniciar, (botao_iniciar.x + 50, botao_iniciar.y + 5))

    botao_parar = pygame.Rect(LARGURA_TELA // 2 - 100, 350, 200, 50)
    pygame.draw.rect(tela, PRETO, botao_parar)
    texto_parar = fonte_menu.render("Sair", True, AZUL_CLARO)
    tela.blit(texto_parar, (botao_parar.x + 60, botao_parar.y + 5))

    pygame.display.flip()
    return botao_iniciar, botao_parar

# Função para desenhar o botão de voltar ao menu
def desenha_botao_voltar():
    largura_botao = 150
    altura_botao = 40
    x_botao = LARGURA_TELA - largura_botao - 10  # Posiciona 10 pixels à esquerda da borda direita
    y_botao = 10  # Margem superior de 10 pixels
    botao_voltar = pygame.Rect(x_botao, y_botao, largura_botao, altura_botao)
    pygame.draw.rect(tela, PRETO, botao_voltar)
    fonte = pygame.font.SysFont(None, 36)
    texto_voltar = fonte.render("Sair", True, BRANCO)
    tela.blit(texto_voltar, (botao_voltar.x + 10, botao_voltar.y + 5))
    return botao_voltar

def jogo():
    global saldo, x_jogador, y_jogador, moedas, perdas, variaveis

    jogando = True
    while jogando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogando = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.collidepoint(event.pos):
                    jogando = False  # Volta ao menu

        # Movimento do jogador (setas esquerda e direita)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and x_jogador > 0:
            x_jogador -= velocidade_jogador
        if teclas[pygame.K_RIGHT] and x_jogador < LARGURA_TELA - largura_jogador:
            x_jogador += velocidade_jogador

        # Movimento das moedas
        for moeda in moedas:
            moeda[1] += velocidade_item
            if moeda[1] > ALTURA_TELA:
                moeda[0] = random.randint(0, LARGURA_TELA - largura_item)
                moeda[1] = random.randint(-100, -40)

            # Detectar colisão entre o jogador e a moeda
            if (x_jogador < moeda[0] + largura_item and x_jogador + largura_jogador > moeda[0] and
                    y_jogador < moeda[1] + altura_item and y_jogador + altura_jogador > moeda[1]):
                saldo += 1
                moeda[0] = random.randint(0, LARGURA_TELA - largura_item)
                moeda[1] = random.randint(-100, -40)

        # Movimento das perdas
        for perda in perdas:
            perda[1] += velocidade_item
            if perda[1] > ALTURA_TELA:
                perda[0] = random.randint(0, LARGURA_TELA - largura_item)
                perda[1] = random.randint(-100, -40)

            # Detectar colisão entre o jogador e a perda
            if (x_jogador < perda[0] + largura_item and x_jogador + largura_jogador > perda[0] and
                    y_jogador < perda[1] + altura_item and y_jogador + altura_jogador > perda[1]):
                saldo -= 1
                perda[0] = random.randint(0, LARGURA_TELA - largura_item)
                perda[1] = random.randint(-100, -40)

        # Movimento das rendas variáveis
        for variavel in variaveis:
            variavel[1] += velocidade_item
            if variavel[1] > ALTURA_TELA:
                variavel[0] = random.randint(0, LARGURA_TELA - largura_item)
                variavel[1] = random.randint(-100, -40)

            # Detectar colisão entre o jogador e a renda variável
            if (x_jogador < variavel[0] + largura_item and x_jogador + largura_jogador > variavel[0] and
                    y_jogador < variavel[1] + altura_item and y_jogador + altura_jogador > variavel[1]):
                operacao = random.choice(["multiplica", "divide", "soma", "subtrai"])
                valor = random.uniform(0.5, 5.0)

                if operacao == "multiplica":
                    saldo = int(saldo * valor)
                elif operacao == "divide":
                    saldo = int(saldo / valor) if valor != 0 else saldo
                elif operacao == "soma":
                    saldo += int(valor * 10)
                elif operacao == "subtrai":
                    saldo -= int(valor * 10)
                variavel[0] = random.randint(0, LARGURA_TELA - largura_item)
                variavel[1] = random.randint(-100, -40)

        # Desenho da tela
        tela.fill(AZUL_CLARO)
        desenha_jogador(x_jogador, y_jogador)
        for moeda in moedas:
            desenha_moeda(moeda[0], moeda[1])
        for perda in perdas:
            desenha_perda(perda[0], perda[1])
        for variavel in variaveis:
            desenha_variavel(variavel[0], variavel[1])

        # Exibe o saldo
        texto_saldo = pygame.font.SysFont(None, 36).render(f"Saldo: {saldo}", True, PRETO)
        tela.blit(texto_saldo, (10, 10))

        # Desenha o botão de voltar
        botao_voltar = desenha_botao_voltar()

        pygame.display.flip()
        clock.tick(60)

# Menu
no_menu = True
while no_menu:
    botao_iniciar, botao_parar = desenha_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            no_menu = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if botao_iniciar.collidepoint(event.pos):
                no_menu = False
                jogo()
            if botao_parar.collidepoint(event.pos):
                no_menu = False

pygame.quit()
