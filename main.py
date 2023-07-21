import pygame
import sys
from config import *
from enemy import Enemy
from player import Player
from key_listener import key_listener
from menu import Menu

font_path = "better-vcr_0.ttf"

def init_game():
    global display, clock, player, enemies

    pygame.init()

    display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(DISPLAY_CAPTION)
    clock = pygame.time.Clock()

    player = Player(400, 300, 52, 80)
    enemies = [Enemy(100, 200, 52, 80, player), Enemy(500, 500, 52, 80, player)]

    new_font = pygame.font.Font(font_path, 36)


def ui_render():
    f1 = pygame.font.Font(font_path, 30)
    text1 = f1.render(f"Health: {player.hp}", 1, (180, 0, 0))
    display.blit(text1, (100, 50))
    pass

def show_start_menu(screen):
    start_menu = Menu(["Start", "Difficulty", "Exit"])

    background_image = pygame.image.load("bg_img.jpg").convert()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                option = start_menu.handle_event(event)
                if option == "Start":
                    return
                elif option == "Exit":
                    pygame.quit()
                    sys.exit()

        screen.blit(background_image, (0, 0))

        start_menu.draw(screen, SCREEN_WIDTH - 50, 50, 30) 
        pygame.display.flip()


def game(screen):
    display.fill((0, 0, 0))
    paused = False
    pause_menu = Menu(["Continue", "Exit"])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Pause the game when the 'Escape' key is pressed
                    paused = not paused

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            btn = pygame.mouse.get_pressed()
            player.attack(enemies, pos, btn)

    ui_render()
    key_listener(pygame.key.get_pressed(), player)

    # ENTITY
    player.update(display)
    for enemy in enemies:
        enemy.update(display)
        if enemy.is_dead:
            enemies.remove(enemy)

    clock.tick(TICK_RATE)  # fps
    pygame.display.update()


if __name__ == '__main__':
    init_game()
    show_start_menu(display)

    while True: game(display)
