import pygame
import sys
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

RECORDS_FILE = 'records.txt'

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def generate_food(snake):
    while True:
        food_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food_pos not in snake:
            return food_pos

def draw_menu():
    screen.fill(BLACK)

    text_new_game = font.render('Novo Jogo', True, WHITE)
    text_records = font.render('Ver Records', True, WHITE)

    rect_new_game = pygame.Rect(200, 150, 200, 50)
    rect_records = pygame.Rect(200, 250, 200, 50)

    pygame.draw.rect(screen, GREEN, rect_new_game, 2)
    pygame.draw.rect(screen, GREEN, rect_records, 2)

    screen.blit(text_new_game, (250, 160))
    screen.blit(text_records, (250, 260))

    pygame.display.update()

def start_game():
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)  # Direção inicial da cobra (direita)
    food = generate_food(snake)
    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (-1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (1, 0):
                    direction = (1, 0)

        head = snake[-1]
        new_head = (head[0] + direction[0], head[1] + direction[1])

        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            game_over = True

        if new_head in snake:
            game_over = True

        if new_head == food:
            snake.append(food)
            food = generate_food(snake)
            score += 1
        else:
            snake.append(new_head)
            snake.pop(0)

        screen.fill(BLACK)


        pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        draw_snake(snake)

        pygame.display.update()

        clock.tick(10)

    if is_high_score(score):
        save_high_score(score)

    show_game_over(score)

def is_high_score(score):
    try:
        with open(RECORDS_FILE, 'r') as file:
            records = file.readlines()
            if not records:
                return True 
            lowest_score = int(records[-1].split(':')[1].strip())
            return score > lowest_score
    except FileNotFoundError:
        return True

def save_high_score(score):
    name = input_name()
    with open(RECORDS_FILE, 'a') as file:
        file.write(f'{name}:{score}\n')

def input_name():
    done = False
    name = ''

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.fill(BLACK)
        text = font.render('Digite seu nome:', True, WHITE)
        screen.blit(text, (200, 200))

        pygame.draw.rect(screen, GREEN, (200, 250, 200, 50), 2)
        text_name = font.render(name, True, WHITE)
        screen.blit(text_name, (210, 260))

        pygame.display.update()
        clock.tick(10)

    return name

def show_records():
    screen.fill(BLACK)
    text_title = font.render('Records:', True, WHITE)
    screen.blit(text_title, (10, 10))

    try:
        with open(RECORDS_FILE, 'r') as file:
            records = file.readlines()
            records.sort(key=lambda x: int(x.split(':')[1]), reverse=True)
            y_offset = 50
            for i, record in enumerate(records[:5]):
                record_info = record.strip().split(':')
                text_record = font.render(f'{record_info[0]} - {record_info[1]}', True, WHITE)
                screen.blit(text_record, (50, y_offset + i * 30))
    except FileNotFoundError:
        text_no_records = font.render('Nenhum registro encontrado.', True, WHITE)
        screen.blit(text_no_records, (50, 50))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                draw_menu()
                return

def show_game_over(score):
    screen.fill(BLACK)
    text = font.render(f'Game Over! Score: {score}', True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    pygame.display.update()

    pygame.time.wait(2000)

    draw_menu()

def main_menu():
    while True:
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                rect_new_game = pygame.Rect(200, 150, 200, 50)
                rect_records = pygame.Rect(200, 250, 200, 50)

                if rect_new_game.collidepoint(mouse_pos):
                    start_game()
                elif rect_records.collidepoint(mouse_pos):
                    show_records()

if __name__ == '__main__':
    main_menu()
