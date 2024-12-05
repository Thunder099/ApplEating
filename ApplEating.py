# Base do jogo
import pygame
import random

# init Pygame
pygame.init()

# Definindo cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
laranja = (255, 165, 0)
verde = (0, 255, 0)

# tamanho do mapa
width, height = 500, 400

# aqui é basicamente a janela do jogo
game_display = pygame.display.set_mode((width, height))

# aqui é o nome que a janela do jogo vai ter
pygame.display.set_caption("ApplEating")

# aqui eu acho que ele ta definindo uma variavel que vai ser o "tick rate" do jogo, ou seja, quão rápido ele "atualiza"
clock = pygame.time.Clock()

# snake size é o tamanho dos quadradinhos "deixar o snake_size no 20 quebra o jogo", a velocidade é usada la embaixo junto com o clock
snake_size = 10
snake_speed = 10

# aqui eu estou definindo fontes de texto e o tamanho em uma variavel, a fonte é "ubuntu" e tem uma variação no tamanho das letras, que são os numeros
message_font = pygame.font.SysFont('ubuntu', 40)
message_font2 = pygame.font.SysFont('ubuntu', 20)
score_font = pygame.font.SysFont('ubuntu', 25)


#funções

# mostra os pontos na tela
def print_score(score):    
    text = score_font.render("Pontos: "+ str(score), True, laranja)

    # aqui ele está falando para mostrar os pontos na tela do jogo com a variavel "text" e depois a coordenada [x,y], adicionar o X faz a coordenada ir mais para a direita, adicionar o Y faz a coordenada ir mais para baixo
    game_display.blit(text, [0,0])

# aqui é onde desenha a cobra; rect significa rectangle -> retangulo, basicamente ta falando pra fazer a cobra renderizar usando quadrados
def draw_snake(snake_size, snake_pixels):
    for pixel in snake_pixels:

        # snake_size, define o tamanho de cada segmento da cobra (largura e altura dos quadrados), snake_pixels é uma lista de posições (X, Y) que reprentam os segmentos da cobra. Cada posição na lista é um segmento da cobra, o loop 'for' percorre cada segmento da cobra, pixel é uma lista que tem coordenadas (X, Y) de cada segmento

        # pygame.draw.rect desenha um retângulo(ou quadrado) na tela, game_display é a janela do jogo, branco é a cor, [pixel[0], pixel[1], snake_size, snake_size]: Essa lista define o retângulo a ser desenhado; pixel[0] é a posição X pixel[1] é a posição Y depois disso vem a largura e a altura do retangulo
        pygame.draw.rect(game_display, branco, [pixel[0], pixel[1], snake_size, snake_size])


# tudo acontece aqui aparentemente, isso aqui é a programação do jogo inteiro, define algumas variaveis, interações, etc.
def run_game():

    # definindo algumas variavéis
    game_over = False
    game_close = False

    x = width / 2
    y = height / 2

    x_speed = 0
    y_speed = 0

    # oia a lista sendo usada ai hihihi
    snake_pixels = []
    snake_length = 1

    # isso aqui ele ta falando pra spawnar a comida em um lugar aleatório
    target_x = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
    target_y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0   

    while not game_over:

        while game_close:
            
            # mostra a tela de game over, aqui embaixo é o fundo
            game_display.fill(preto)
            # renderiza as mensagens na tela, ("texto", basicamente ativa o 'antialiasing' que deixa as bordas do texto mais suavizadas ao invés de serrilhadas, cor)
            game_over_message = message_font.render("Game Over!", True, branco)
            game_over_message2 = message_font2.render("[1]Reiniciar", True, verde)
            game_over_message3 = message_font2.render("[2]Fechar", True, vermelho)

            # aqui muda a posição das palavras na tela 'eu juro que nao ta desalinhado'
            game_display.blit(game_over_message, [width / 3.5, height / 3])
            game_display.blit(game_over_message2, [width / 3.5, height / 2])
            game_display.blit(game_over_message3, [width / 2, height / 2])

            # aqui ele pega o score e diminui -1, porque se nao tivesse isso logo no começo do jogo voce ja vai ter um ponto, que seria a cabeça do seu personagem '-'
            print_score(snake_length - 1)
            # isso aqui ele só atualiza as mudanças feitas
            pygame.display.update()

            # isso aqui são os botões 1 e 2, que são os que reiniciam ou fecham o jogo
            # enquanto game_over nao for verdade tudo continua rodando, a partir do momento que é verdade, o código inteiro para imediatamente, o quit é basicamente se voce fechar pelo X
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_2:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_1:
                        run_game()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False


        # (foi usado IA como ajuda)

        # esse trecho do código aparentemente pega todos os eventos usando o comando "for" como teclas apertadas, quando o tipo for pygame.QUIT(quando fecha a janela), o jogo é encerrado atribuindo True a variavel "game_over"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            # pygame.KEYDOWN significa que a tecla foi pressionada.
            if event.type == pygame.KEYDOWN:

                # Impede que a cobra se mova na direção oposta (explicação mais detalhada mais abaixo)
                if event.key == pygame.K_LEFT and x_speed == 0:
                    x_speed = -snake_size
                    y_speed = 0
                if event.key == pygame.K_RIGHT and x_speed == 0:
                    x_speed = snake_size
                    y_speed = 0
                if event.key == pygame.K_UP and y_speed == 0:
                    x_speed = 0
                    y_speed = -snake_size
                if event.key == pygame.K_DOWN and y_speed == 0:
                    x_speed = 0
                    y_speed = snake_size

                # Bloquear movimento 180 graus

                 # exemplo: se a cobra está indo para a direita (x_speed = snake_size), e o jogador tenta apertar a tecla esquerda(pygame.K_LEFT), o código não permite, porque (x_speed != snake_size). Ou seja, não podemos mudar a direção para a esquerda, pois a cobra já está indo para a direita; pelo oque entendi: está indo para a direita (x_speed = snake_size), ele verifica se isso é verdade o tempo todo, (direita = snake_size) (esquerda = -snake_size) se for igual a 'snake_size' ele nao deixa voce virar para a esquerda que é snake_size só que negativo, usando o termo "and" ('e' em ingles) onde é preciso que ambas as afirmações sejam verdadeiras para funcionar

                if event.key == pygame.K_LEFT and x_speed != snake_size:  # Não pode ir para a esquerda se já estiver indo para a direita
                    x_speed = -snake_size
                    y_speed = 0
                if event.key == pygame.K_RIGHT and x_speed != -snake_size:  # Não pode ir para a direita se já estiver indo para a esquerda
                    x_speed = snake_size
                    y_speed = 0
                if event.key == pygame.K_UP and y_speed != snake_size:  # Não pode ir para cima se já estiver indo para baixo
                    x_speed = 0
                    y_speed = -snake_size
                if event.key == pygame.K_DOWN and y_speed != -snake_size:  # Não pode ir para baixo se já estiver indo para cima
                    x_speed = 0
                    y_speed = snake_size

        # Verificando se a cobra saiu das bordas; basicamente falando pro código que se estiver mais que essa coordenada quer dizer que voce perdeu, ai ele faz a variavel "game_close" verdadeira
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        x += x_speed
        y += y_speed

        # Atualizando o fundo e a comida
        game_display.fill(preto)
        pygame.draw.rect(game_display, laranja, [target_x, target_y, snake_size, snake_size])

        # Adicionando a nova posição da cabeça da cobra
        snake_pixels.append([x, y])

        if len(snake_pixels) > snake_length:
            del snake_pixels[0]

        # Verificando se a cobra colidiu com ela mesma
        for pixel in snake_pixels[:-1]:
            if pixel == [x, y]:
                game_close = True

        draw_snake(snake_size, snake_pixels)
        print_score(snake_length - 1)

        pygame.display.update()

        # Verificando se a cobra comeu a comida

        # aqui ele verifica se a coordenada da cabeça da cobra é EXATAMENTE a coordenada da comida
        if x == target_x and y == target_y:

            # caso ele atinja exatamente a coordenada da comida, ele vai spawnar outra comida num lugar aleatório
            target_x = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
            target_y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0            

            # depois que ele faz isso tudo, o tamanho da cobrinha aumenta em 1
            snake_length += 1
            
        # acho que aqui é o 'tick rate' do jogo, ou seja, quão rapido o jogo atualiza
        clock.tick(snake_speed)

    # acho que aqui é quando estora tudo, só finaliza o loop, ou fecha, talvez
    pygame.quit()
    quit()

# aqui ele chama a função, para começar o jogo
run_game()