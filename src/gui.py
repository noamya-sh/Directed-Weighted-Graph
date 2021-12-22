import math
import pygame as pg
from pygame import Color, display, gfxdraw, Rect
from pygame.constants import RESIZABLE
from pygame.examples.joystick import BLACK
from GraphAlgoInterface import *
from GraphAlgo import *
import numpy as np
# init pg
from src.GraphAlgo import GraphAlgo


class gui:
    def __init__(self, graphAlgo: GraphAlgoInterface):
        self.graphAlgo = graphAlgo
        WIDTH, HEIGHT = 1080, 720
        self.screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        while True:
            pg.init()
            clock = pg.time.Clock()
            pg.font.init()

            FONT = pg.font.SysFont('Arial', 20, bold=True)
            # check events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)

            # refresh screen
            self.screen.fill(Color(51, 25, 0))

            graph = self.graphAlgo.get_graph()
            # get data proportions
            self.min_x = min(list(graph.get_dicNodes().values()), key=lambda n: n.get_pos().x).get_pos().x
            self.min_y = min(list(graph.get_dicNodes().values()), key=lambda n: n.get_pos().y).get_pos().y
            self.max_x = max(list(graph.get_dicNodes().values()), key=lambda n: n.get_pos().x).get_pos().x
            self.max_y = max(list(graph.get_dicNodes().values()), key=lambda n: n.get_pos().y).get_pos().y

            # draw edges
            for e in graph.get_dicEdges().values():
                # find the edge nodes
                src = next(n for n in graph.get_dicNodes().values() if n.get_id() == e.get_src())
                dest = next(n for n in graph.get_dicNodes().values() if n.get_id() == e.get_dest())

                # scaled positions
                src_x = self.my_scale(src.get_pos().x, x=True)
                src_y = self.my_scale(src.get_pos().y, y=True)
                dest_x = self.my_scale(dest.get_pos().x, x=True)
                dest_y = self.my_scale(dest.get_pos().y, y=True)

                # draw the line
                p = np.subtract((dest_x, dest_y), yashar((src_x, src_y), (dest_x, dest_y)))
                line(self.screen, Color(153, 153, 0), (src_x, src_y), p)
                # pg.draw.line(screen, Color(153, 153, 0),
                #                  (src_x, src_y), (dest_x, dest_y), width=4)
            for e in graph.get_dicEdges().values():
                # find the edge nodes
                src = next(n for n in graph.get_dicNodes().values() if n.get_id() == e.get_src())
                dest = next(n for n in graph.get_dicNodes().values() if n.get_id() == e.get_dest())

                # scaled positions
                src_x = self.my_scale(src.get_pos().x, x=True)
                src_y = self.my_scale(src.get_pos().y, y=True)
                dest_x = self.my_scale(dest.get_pos().x, x=True)
                dest_y = self.my_scale(dest.get_pos().y, y=True)

                # draw the line
                p = np.subtract((dest_x, dest_y), yashar((src_x, src_y), (dest_x, dest_y)))
                arrow(self.screen, Color(0, 0, 0), (src_x, src_y), p, 10)
            # draw nodes
            for n in graph.get_dicNodes().values():
                x = self.my_scale(n.get_pos().x, x=True)
                y = self.my_scale(n.get_pos().y, y=True)

                # its just to get a nice antialiased circle
                gfxdraw.filled_circle(self.screen, int(x), int(y),
                                      radius, Color(176, 143, 35))
                gfxdraw.aacircle(self.screen, int(x), int(y),
                                 radius, Color(255, 255, 255))

                # draw the node id
                id_srf = FONT.render(str(n.get_id()), True, Color(0, 0, 0))
                rect = id_srf.get_rect(center=(x, y))
                self.screen.blit(id_srf, rect)
            # button(0, HEIGHT-50, 80, 50)
            # update screen changes
            display.update()

            # refresh rate
            clock.tick(60)

    def my_scale(self, data, x=False, y=False):
        if x:
            return scale(data, 50, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return scale(data, 50, self.screen.get_height() - 50, self.min_y, self.max_y)


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimensions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# # get the current directory path
# root_path = os.path.dirname(os.path.abspath(__file__))
#
# # load the json file into SimpleNamespace Object
# with open(root_path + '/graph_triangle.json', 'r') as file:
#     graph = json.load(
#         file, object_hook=lambda json_dict: SimpleNamespace(**json_dict))


# decorate scale with the correct values


radius = 15



def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def yashar(start, end):
    v = np.subtract(end, start)
    b = tuple(normalize(v) * 20)
    return b


def line(screen, lcolor, start, end, thickness=4):
    pg.draw.line(screen, lcolor, start, np.subtract(end, tuple(normalize(np.subtract(end, start)) * 10)), thickness)


def arrow(screen, tricolor, start, end, trirad):
    rad = math.pi / 180
    rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi / 2
    pg.draw.polygon(screen, tricolor, ((end[0] + trirad * math.sin(rotation),
                                        end[1] + trirad * math.cos(rotation)),
                                       (end[0] + trirad * math.sin(rotation - 120 * rad),
                                        end[1] + trirad * math.cos(rotation - 120 * rad)),
                                       (end[0] + trirad * math.sin(rotation + 120 * rad),
                                        end[1] + trirad * math.cos(rotation + 120 * rad))))


def button(screen, x, y, w, h, inactive=None, active=None, action=None):
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    pg.draw.rect(screen, Color(22, 225, 255), (x, y, x + w, y + h))
    # screen.blit()
    # if x + w > mouse[0] > x and y + h > mouse[1] > y:
    #     screen.blit(pg.Rect(x,y,w,h))
    #     if click[0] == 1 and action is not None:
    #         action()
    # else:
    #     screen.blit(inactive, (x, y))
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)
# YELLOW = (255, 255, 0)
# class menu():
#     def __init__(self):
#         pg.init()
#         screen = pg.display.set_mode((800, 600))
#         screen_rect = screen.get_rect()
#
#         # - objects -
#
#         stage = 'menu'
#
#         button_1 = self.button_create("GAME", (300, 100, 200, 75), RED, GREEN, self.on_click_button_1)
#         button_2 = self.button_create("OPTIONS", (300, 200, 200, 75), RED, GREEN, self.on_click_button_2)
#         button_3 = self.button_create("EXIT", (300, 300, 200, 75), RED, GREEN, self.on_click_button_3)
#
#         button_return = self.button_create("RETURN", (300, 400, 200, 75), RED, GREEN, self.on_click_button_return)
#         running = True
#jjjjj
#         while running:
#
#             # - events -
#
#             for event in pg.event.get():
#                 if event.type == pg.QUIT:
#                     running = False
#
#                 if stage == 'menu':
#                     self.button_check(button_1, event)
#                     self.button_check(button_2, event)
#                     self.button_check(button_3, event)
#                 elif stage == 'game':
#                     self.button_check(button_return, event)
#                 elif stage == 'options':
#                     self.button_check(button_return, event)
#                 # elif stage == 'exit':
#                 #    pass
#
#             # - draws -
#
#             screen.fill(BLACK)
#
#             if stage == 'menu':
#                 self.button_draw(screen, button_1)
#                 self.button_draw(screen, button_2)
#                 self.button_draw(screen, button_3)
#             elif stage == 'game':
#                 self.button_draw(screen, button_return)
#             elif stage == 'options':
#                 self.button_draw(screen, button_return)
#             elif stage == 'exit':
#                 running = False
#                 pg.display.E
#
#             pg.display.update()
#     WHITE = (255, 255, 255)
#     BLACK = (0, 0, 0)
#
#     RED = (255, 0, 0)
#     GREEN = (0, 255, 0)
#     BLUE = (0, 0, 255)
#
#     YELLOW = (255, 255, 0)
#
#     # --- classes --- (CamelCaseNanes)
#
#     # empty
#
#     # --- functions --- (lower_case_names_
#
#     def button_create(self,text, rect, inactive_color, active_color, action):
#
#         font = pg.font.Font(None, 40)
#
#         button_rect = pg.Rect(rect)
#
#         text = font.render(text, True, BLACK)
#         text_rect = text.get_rect(center=button_rect.center)
#
#         return [text, text_rect, button_rect, inactive_color, active_color, action, False]
#
#     def button_check(self,info, event):
#
#         text, text_rect, rect, inactive_color, active_color, action, hover = info
#
#         if event.type == pg.MOUSEMOTION:
#             # hover = True/False
#             info[-1] = rect.collidepoint(event.pos)
#
#         elif event.type == pg.MOUSEBUTTONDOWN:
#             if hover and action:
#                 action()
#
#     def button_draw(self,screen, info):
#
#         text, text_rect, rect, inactive_color, active_color, action, hover = info
#
#         if hover:
#             color = active_color
#         else:
#             color = inactive_color
#
#         pg.draw.rect(screen, color, rect)
#         screen.blit(text, text_rect)
#
#     # ---
#
#     def on_click_button_1(self):
#         global stage
#         stage = 'game'
#
#         print('You clicked Button 1')
#
#     def on_click_button_2(self):
#         global stage
#         stage = 'options'
#
#         print('You clicked Button 2')
#
#     def on_click_button_3(self):
#         global stage
#         global running
#
#         stage = 'exit'
#         running = False
#
#         pg.quit()
#         exit(0)
#         print('You clicked Button 3')
#
#     def on_click_button_return(self):
#         global stage
#         stage = 'menu'
#
#         print('You clicked Button Return')
#
#     # --- main ---  (lower_case_names)
#
#     # - init -
#
#
#
#     # - mainloop -
#
#
