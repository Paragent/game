# menu.py

import pygame

font_path = "better-vcr_0.ttf"

class Menu:
    def __init__(self, items, font_size=50, font_color=(180, 190, 196), select_color=(255, 255, 255)):
        self.items = items
        self.font_size = font_size
        self.font_color = font_color
        self.select_color = select_color
        self.font = pygame.font.Font(font_path, font_size)
        self.selected_item_index = 0

    def draw(self, surface, x, y, padding):
        for index, item in enumerate(self.items):
            text_surface = self.font.render(item, True, self.font_color)
            text_rect = text_surface.get_rect(topright=(x, y + index * (self.font_size + padding)))
            if index == self.selected_item_index:
                text_surface = self.font.render('*' + item, True, self.font_color)
            surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.move_cursor(-1)
            elif event.key == pygame.K_s:
                self.move_cursor(1)
            elif event.key == pygame.K_RETURN:
                return self.items[self.selected_item_index]

    def move_cursor(self, direction):
        self.selected_item_index = (self.selected_item_index + direction) % len(self.items)
