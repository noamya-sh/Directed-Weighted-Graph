import pygame as pg
from pygame import Rect, font, Surface, Color

font.init()
arial_font = font.SysFont('Candara', 15, bold=True)

"""This file contain classes for draw menu. Inspired by the code of Achia zigler: 
https://github.com/benmoshe/OOP_2021/tree/main/Class_Material/Week_11/T11-AchiyaZigi/pygame_ui """


class Button:
    """
    simple button, base for everything
    """

    def __init__(self, title: str, size: tuple[int, int], color=Color(51, 0, 25)) -> None:
        self.title = title
        self.size = size
        self.color = color
        self.rect = Rect((0, 0), size)
        self.on_click = []
        self.show = True
        self.disabled = False

    def add_click_listener(self, func) -> None:
        self.on_click.append(func)

    def render(self, surface: Surface, pos) -> None:
        if (not self.show):
            return
        self.rect.topleft = pos

        title_srf = arial_font.render(self.title, True, Color(255, 255, 255))
        title_rect = title_srf.get_rect(center=self.rect.center)
        pg.draw.rect(surface, Color(51, 0, 25), self.rect)
        pg.draw.rect(surface, Color(255, 255, 255), self.rect, width=1)
        surface.blit(title_srf, title_rect)

    def check(self) -> None:
        if self.on_click != [] and not self.disabled:
            mouse_pos = pg.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                clicked, _, _ = pg.mouse.get_pressed()
                if clicked:
                    for func in self.on_click:
                        func()


class MenuItem(Button):
    """
    drop down to bottom side
    """

    def __init__(self, title: str, size, buttons: list[Button], color=Color(51, 0, 25)) -> None:
        super().__init__(title, size, color=color)
        max_w = max(buttons, key=lambda b: b.rect.width).rect.width
        sum_h = sum(b.rect.height for b in buttons)
        self.menu_rect = Rect((0, 0), (max_w, sum_h))
        self.show_menu = False
        self.buttons = buttons

        def toggle_menu():
            self.show_menu = not self.show_menu

        self.add_click_listener(toggle_menu)

    def check(self) -> None:
        super().check()
        if self.show_menu:
            for b in self.buttons:
                b.check()

    def render(self, surface: Surface, pos) -> None:
        super().render(surface, pos)
        if self.show_menu:
            self.menu_rect.topleft = self.rect.bottomleft
            last_button_rect = self.rect
            for b in self.buttons:
                b.render(surface, (self.menu_rect.left, last_button_rect.bottom))
                last_button_rect = b.rect
                b.disabled = False
            pg.draw.rect(surface, self.color, self.menu_rect, width=1)
        else:
            for b in self.buttons:
                b.disabled = True


class SubMenuItem(MenuItem):
    """
    dropdown to the right
    """

    def render(self, surface: Surface, pos) -> None:
        Button.render(self, surface, pos)
        if self.show_menu:
            self.menu_rect.topleft = self.rect.topright
            last_button_bottom = self.menu_rect.top
            for b in self.buttons:
                b.render(surface, (self.menu_rect.left, last_button_bottom))
                last_button_bottom = b.rect.bottom
                b.disabled = False
            pg.draw.rect(surface, self.color, self.menu_rect, width=1)
        else:
            for b in self.buttons:
                b.disabled = True


class MenuBar:
    """
    container for menu items
    """

    def __init__(self, menu_items: list[MenuItem]) -> None:
        self.menu_items = menu_items
        max_h = max(m.rect.height for m in menu_items)
        sum_w = sum(m.rect.width for m in menu_items)
        self.rect = Rect((0, 0), (sum_w, max_h))

    def check(self) -> None:
        for m in self.menu_items:
            m.check()

    def render(self, surface, pos) -> None:
        self.rect.topleft = pos
        last_menu_pos = pos
        for m in self.menu_items:
            m.render(surface, last_menu_pos)
            last_menu_pos = m.rect.topright
