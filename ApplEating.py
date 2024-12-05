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

width, height = 500, 400

game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption("ApplEating")

clock = pygame.time.Clock()

snake_size = 10
snake_speed = 10

message_font = pygame.font.SysFont('ubuntu', 30)
score_font = pygame.font.SysFont('ubuntu', 25)

###########################

#funções

# mostra os pontos na tela
def print_score(score):    
    text = score_font.render("Score: "+ str(score), True, laranja)
    game_display.blit(text, [0,0])

# desenha a cobra
def draw_snake(snake_size, snake_pixels):
    for pixel in snake_pixels:
        pygame.draw.rect(game_display, branco, [pixel[0], pixel[1], snake_size, snake_size])


def run_game():

    game_over = False
    game_close = False

    x = width / 2
    y = height / 2

    x_speed = 0
    y_speed = 0

    snake_pixels = []
    snake_length = 1

    target_x = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
    target_y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0   

    while not game_over:

        while game_close:
            game_display.fill(preto)
            game_over_message = message_font.render("Game Over!", True, vermelho)
            game_display.blit(game_over_message, [width / 3, height / 3])
            print_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_2:
                        run_game()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Impede que a cobra se mova na direção oposta
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

        # Verificando se a cobra saiu das bordas
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        x += x_speed
        y += y_speed

        # Atualizando o fundo e o alvo
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
        if x == target_x and y == target_y:
            target_x = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
            target_y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0            

            snake_length += 1
            

        clock.tick(snake_speed)

    pygame.quit()
    quit()

run_game()
