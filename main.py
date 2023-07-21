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
    in_start_menu = False
    paused = False
    pause_menu = Menu(["Continue", "Exit"])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()

            if not paused and not in_start_menu:  # Only handle events when the game is not paused and not in the start menu
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    btn = pygame.mouse.get_pressed()
                    player.attack(enemies, pos, btn)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Pause the game when the 'Escape' key is pressed
                        paused = True
            elif in_start_menu:  # Handle events when in the start menu
                # Additional code to handle events in the start menu (if needed)
                pass
            else:  # Handle events for the pause menu when the game is paused
                option = pause_menu.handle_event(event)
                if option == "Continue":
                    paused = False
                elif option == "Exit":
                    in_start_menu = True  # Set the flag to return to the start menu
                    paused = False

        if not in_start_menu:
            if not paused:
                # Clear the screen before updating game entities
                display.fill((0, 0, 0))

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
            else:
                # If the game is paused, show the pause menu
                # Clear the screen before drawing the pause menu
                display.fill((0, 0, 0))

                # Draw the pause menu items on top of the background
                pause_menu.draw(display, SCREEN_WIDTH - 50, 50, 30)
                pygame.display.flip()
        else:
            # If in the start menu, show the start menu
            show_start_menu(display)
            in_start_menu = False


if __name__ == '__main__':
    init_game()
    show_start_menu(display)

    while True: game(display)
