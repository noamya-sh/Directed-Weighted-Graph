import math
from tkinter import ttk, Button
from tkinter.filedialog import askopenfilename

import pygame as pg
from pygame import Color, display, gfxdraw, Rect, Surface, font, MOUSEBUTTONDOWN
from pygame.constants import RESIZABLE
from pygame.examples.joystick import BLACK
from GraphAlgoInterface import *
from GraphAlgo import *
import numpy as np
from menu import *
import tkinter as tk
# init pg
from src.GraphAlgo import GraphAlgo


class gui:
    def __init__(self, graphAlgo: GraphAlgoInterface):
        self.graphAlgo = graphAlgo
        WIDTH, HEIGHT = 1080, 720
        self.screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        self.GC = None
        self.SP = None
        self.TSP = None
        clock = pg.time.Clock()
        center = Button('Center', (70, 20))
        center.add_click_listener(lambda: self.setCenter(self.graphAlgo.centerPoint()[0]))
        load = Button('Load', (70, 20))
        load.add_click_listener(lambda: self.loadnewGraph())
        short = Button('ShortPath', (70, 20))
        short.add_click_listener(lambda: self.selectShortPath())
        tsp = Button('TSP', (70, 20))
        tsp.add_click_listener(lambda: self.selectTSP())
        algo = SubMenuItem('Show', (70, 20), [center, short, tsp], color=Color(152, 122, 19))
        menu = MenuItem('Menu', (70, 20), [algo, load], Color(98, 140, 30))
        m = MenuBar([menu])
        while True:
            pg.init()

            pg.font.init()
            # time_delta = clock.tick(60)
            FONT = pg.font.SysFont('Arial', 20, bold=True)

            # refresh screen
            self.screen.fill(Color("#513506"))

            graph = self.graphAlgo.get_graph()
            # get data proportions
            self.min_x = min(list(graph.get_dicNodes().values()), key=lambda n: n.get_pos()[0]).get_pos()[0]
            self.min_y = min(list(graph.get_dicNodes().values()), key=lambda n: n.get_pos()[1]).get_pos()[1]
            self.max_x = max(list(graph.get_dicNodes().values()), key=lambda n: n.get_pos()[0]).get_pos()[0]
            self.max_y = max(list(graph.get_dicNodes().values()), key=lambda n: n.get_pos()[1]).get_pos()[1]
            self.drawGraph()
            self.drawCenter()
            # self.drawShortPath()
            # draw edges

            # check events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    # check menubar clicks
                    m.check()
            # refresh rate
            m.render(self.screen, (0, 0))
            display.update()
            clock.tick(60)

    def my_scale(self, data, x=False, y=False):
        if x:
            return scale(data, 50, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return scale(data, 50, self.screen.get_height() - 50, self.min_y, self.max_y)

    def drawGraph(self):
        graph = self.graphAlgo.get_graph()
        for k in graph.get_dicEdges().keys():
            # find the edge nodes
            src = next(n for n in graph.get_dicNodes().values() if n.get_id() == k[0])
            dest = next(n for n in graph.get_dicNodes().values() if n.get_id() == k[1])

            # scaled positions
            src_x = self.my_scale(src.get_pos()[0], x=True)
            src_y = self.my_scale(src.get_pos()[1], y=True)
            dest_x = self.my_scale(dest.get_pos()[0], x=True)
            dest_y = self.my_scale(dest.get_pos()[1], y=True)

            # draw the line
            p = np.subtract((dest_x, dest_y), yashar((src_x, src_y), (dest_x, dest_y)))
            line(self.screen, Color("#2B1B01"), (src_x, src_y), p)
            # pg.draw.line(screen, Color(153, 153, 0),
            #                  (src_x, src_y), (dest_x, dest_y), width=4)
        for k in graph.get_dicEdges().keys():
            # find the edge nodes
            src = next(n for n in graph.get_dicNodes().values() if n.get_id() == k[0])
            dest = next(n for n in graph.get_dicNodes().values() if n.get_id() == k[1])

            # scaled positions
            src_x = self.my_scale(src.get_pos()[0], x=True)
            src_y = self.my_scale(src.get_pos()[1], y=True)
            dest_x = self.my_scale(dest.get_pos()[0], x=True)
            dest_y = self.my_scale(dest.get_pos()[1], y=True)

            # draw the line
            p = np.subtract((dest_x, dest_y), yashar((src_x, src_y), (dest_x, dest_y)))
            arrow(self.screen, Color("#003300"), (src_x, src_y), p, 10)
        FONT = pg.font.SysFont('Candara', 20, bold=True)
        self.drawPath(self.SP)
        self.drawPath(self.TSP)
        # draw nodes
        for n in graph.get_dicNodes().values():
            x = self.my_scale(n.get_pos()[0], x=True)
            y = self.my_scale(n.get_pos()[1], y=True)
            gfxdraw.filled_circle(self.screen, int(x), int(y), radius, Color(176, 143, 35))
            gfxdraw.aacircle(self.screen, int(x), int(y), radius, Color(255, 255, 255))

            # draw the node id
            id_srf = FONT.render(str(n.get_id()), True, Color(0, 0, 0))
            rect = id_srf.get_rect(center=(x, y))
            self.screen.blit(id_srf, rect)

    def setCenter(self, id=None):
        self.update()
        if id == -1 or id is None:
            return
        self.GC = id


    def drawCenter(self):
        if self.GC is not None:
            node = self.graphAlgo.get_graph().get_dicNodes()[self.GC]
            x = self.my_scale(node.get_pos()[0], x=True)
            y = self.my_scale(node.get_pos()[1], y=True)
            gfxdraw.filled_circle(self.screen, int(x), int(y),
                                  radius, Color(250, 143, 0))
            gfxdraw.aacircle(self.screen, int(x), int(y),
                             radius, Color(255, 255, 255))
            FONT = pg.font.SysFont('Candara', 20, bold=True)
            text = FONT.render('Center point', False, (0, 0, 0))
            rect = text.get_rect(center=(x, y - 50))
            self.screen.blit(text, rect)
            id_srf = FONT.render(str(self.GC), True, Color(0, 0, 0))
            rect = id_srf.get_rect(center=(x, y))
            self.screen.blit(id_srf, rect)

    def drawPath(self, path):
        if path is None:
            return
        graph = self.graphAlgo.get_graph()
        i = 0
        l = len(path)
        while i + 1 < l:
            p1 = path[i]
            p2 = path[i + 1]
            # find the edge nodes
            src = graph.get_dicNodes()[p1]
            dest = graph.get_dicNodes()[p2]

            # scaled positions
            src_x = self.my_scale(src.get_pos()[0], x=True)
            src_y = self.my_scale(src.get_pos()[1], y=True)
            dest_x = self.my_scale(dest.get_pos()[0], x=True)
            dest_y = self.my_scale(dest.get_pos()[1], y=True)
            # draw the line
            p = np.subtract((dest_x, dest_y), yashar((src_x, src_y), (dest_x, dest_y)))
            line(self.screen, Color("#1A8742"), (src_x, src_y), p)
            arrow(self.screen, Color("#2C037D"), (src_x, src_y), p, 10)
            i += 1

    def loadnewGraph(self):
        self.update()
        filrChooser = tk.Tk()
        filrChooser.withdraw()
        file = askopenfilename(filetypes=[("json", "*.json")])
        try:
            self.graphAlgo.load_from_json(file)
        except:
            return

    def selectTSP(self):
        self.update()
        window = tk.Tk()
        window.title('Select')
        window.geometry('350x150')
        # label
        ttk.Label(window, text="Add Node :", font=("Candara", 10)).grid(column=0, row=5, padx=10, pady=10)

        # Combobox creation
        n = tk.StringVar()
        src = ttk.Combobox(window, width=10, textvariable=n)
        start = [i for i in self.graphAlgo.get_graph().get_all_v().keys()]
        # Adding combobox drop down list
        src['values'] = start
        src['state'] = 'readonly'
        src.grid(column=2, row=5, pady=(10, 2), padx=(20, 0))

        def add():
            if src.get() == "":
                return
            if src.get() not in dest['values']:
                cur.append(int(src.get()))
                dest['values'] = cur
                start.remove(int(src.get()))
                src['values'] = start
            dest.current(0)

        add = tk.Button(window, text="Add", bg='yellow', command=add)
        add.grid(column=5, row=5, pady=(10, 2), padx=(20, 0))
        ttk.Label(window, text="Selected Node :", font=("Candara", 10)).grid(column=0, row=8, padx=10,
                                                                             pady=10)
        g = tk.StringVar()
        dest = ttk.Combobox(window, width=10, textvariable=g)
        src['state'] = 'readonly'
        cur = []
        dest['values'] = cur
        dest.grid(column=2, row=8, pady=(10, 2), padx=(20, 0))

        def remove():
            if len(cur) == 0 or dest.get() == "" or int(dest.get()) not in cur:
                return
            start.append(int(dest.get()))
            src['values'] = sorted(start)
            cur.remove(int(dest.get()))
            dest['values'] = cur
            if len(cur) > 0:
                dest.current(0)
            else:
                dest.set("")

        rem = tk.Button(window, text="Remove", bg='yellow', command=remove)
        rem.grid(column=5, row=8, pady=(10, 2), padx=(20, 0))

        def checkcmbo():

            path, dis = self.graphAlgo.TSP(cur)
            self.TSP = path
            window.destroy()

        find = tk.Button(window, text="Find", bg='yellow', command=checkcmbo)
        find.grid(column=2, row=10, pady=(10, 2), padx=(20, 0))
        window.mainloop()
        return

    def selectShortPath(self):
        # Creating tkinter window
        self.update()
        window = tk.Tk()
        window.title('Select')
        window.geometry('250x150')
        # label
        ttk.Label(window, text="Select src Node :", font=("Candara", 10)).grid(column=0, row=5, padx=10, pady=10)

        # Combobox creation
        n = tk.StringVar()
        src = ttk.Combobox(window, width=10, textvariable=n)

        # Adding combobox drop down list
        src['values'] = [i for i in self.graphAlgo.get_graph().get_all_v().keys()]
        src.grid(column=2, row=5, pady=(10, 2), padx=(20, 0))
        ttk.Label(window, text="Select dest Node :", font=("Candara", 10)).grid(column=0, row=8, padx=10,
                                                                                pady=10)

        def checkcmbo():
            if src.get() == "" or dest.get() == "":
                return
            dis, path = self.graphAlgo.shortest_path(int(src.get()), int(dest.get()))
            print(dis,path)
            self.SP = path
            window.destroy()

        g = tk.StringVar()
        dest = ttk.Combobox(window, width=10, textvariable=g)
        dest['values'] = [i for i in self.graphAlgo.get_graph().get_all_v().keys()]
        dest.grid(column=2, row=8, pady=(10, 2), padx=(20, 0))


        b = tk.Button(window, text="Find", bg='yellow', command=checkcmbo)
        b.grid(column=2, row=10, pady=(10, 2), padx=(20, 0))
        window.mainloop()

    def update(self):
        self.SP = None
        self.TSP = None
        self.GC = None


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
    pg.draw.line(screen, lcolor, start, np.subtract(end, tuple(normalize(np.subtract(end, start)) * 5)), thickness)


def arrow(screen, tricolor, start, end, trirad):
    rad = math.pi / 180
    rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi / 2
    pg.draw.polygon(screen, tricolor, ((end[0] + trirad * math.sin(rotation),
                                        end[1] + trirad * math.cos(rotation)),
                                       (end[0] + trirad * math.sin(rotation - 120 * rad),
                                        end[1] + trirad * math.cos(rotation - 120 * rad)),
                                       (end[0] + trirad * math.sin(rotation + 120 * rad),
                                        end[1] + trirad * math.cos(rotation + 120 * rad))))

#
# def button(screen, x, y, w, h, inactive=None, active=None, action=None):
#     mouse = pg.mouse.get_pos()
#     click = pg.mouse.get_pressed()
#
#     pg.draw.rect(screen, Color(22, 225, 255), (x, y, x + w, y + h))
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
# jjjjj
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
