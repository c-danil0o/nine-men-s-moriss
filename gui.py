import time

import pygame
from game import Game
pygame.init()

screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Nine Men's Morris")
icon = pygame.image.load('assets/white.png')
pygame.display.set_icon(icon)
board = pygame.image.load('assets/board.png')
boardx = 210
boardy = 60
white = pygame.image.load('assets/white.png')
black = pygame.image.load('assets/black.png')
transparent = pygame.image.load('assets/transparent.png')

positions = [pygame.Rect(215, 65, 40, 40), pygame.Rect(433, 65, 40, 40), pygame.Rect(650, 65, 40, 40),
             pygame.Rect(285, 135, 40, 40), pygame.Rect(433, 135, 40, 40), pygame.Rect(580, 135, 40, 40),
             pygame.Rect(355, 205, 40, 40), pygame.Rect(430, 205, 40, 40), pygame.Rect(505, 205, 40, 40),
             pygame.Rect(215, 280, 40, 40), pygame.Rect(285, 280, 40, 40), pygame.Rect(355, 280, 40, 40),
             pygame.Rect(505, 280, 40, 40), pygame.Rect(580, 280, 40, 40), pygame.Rect(650, 280, 40, 40),
             pygame.Rect(355, 355, 40, 40), pygame.Rect(433, 355, 40, 40), pygame.Rect(505, 355, 40, 40),
             pygame.Rect(285, 425, 40, 40), pygame.Rect(433, 425, 40, 40), pygame.Rect(580, 425, 40, 40),
             pygame.Rect(215, 500, 40, 40), pygame.Rect(433, 500, 40, 40), pygame.Rect(650, 500, 40, 40)
             ]

new_game = Game()


def draw_board():
    screen.blit(board, (boardx, boardy))


def draw_pieces(white_left, black_left):
    white_start_coordx = 40
    white_start_coordy = 40
    black_start_coordx = 828
    black_start_coordy = 40
    for i in range(white_left):
        screen.blit(white, (white_start_coordx, white_start_coordy))
        white_start_coordy += 40
    for i in range(black_left):
        screen.blit(black, (black_start_coordx, black_start_coordy))
        black_start_coordy += 40


def set_positions(placed, highlighted):
    j = 0
    while j < 24:
        # pygame.draw.rect(screen, (255, 0, 0), positions[j])
        if placed[j] == 1:
            screen.blit(white, positions[j])
        elif placed[j] == 2:
            screen.blit(black, positions[j])
        if highlighted[j]:
            pygame.draw.rect(screen, (255, 0, 0), positions[j], 2)
        else:
            pass
        j = j + 1


def start_game():
    game = True

    while game:
        screen.fill((224, 224, 224))
        draw_board()
        draw_pieces(new_game.white_left, new_game.black_left)
        for event in pygame.event.get():
            nextmove = False
            if event.type == pygame.QUIT:
                game = False
            if new_game.player_turn == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(24):
                        if pygame.mouse.get_pressed()[0]:
                            if positions[i].collidepoint(pygame.mouse.get_pos()):
                                print("Mouse pressed!")
                                new_game.check_move(i)
                                nextmove = True

                                break
                    if nextmove:
                        break
            else:
                new_game.ai_next_move()
        set_positions(new_game.placed, new_game.highlighted)
        pygame.display.update()
        if new_game.check_if_end():
            time.sleep(3)
            game = False
