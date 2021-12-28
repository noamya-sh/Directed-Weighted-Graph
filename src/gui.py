import math
from tkinter import ttk, Button
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox as mb

import pygame as pg
from pygame import Color, display, gfxdraw, Rect, Surface, font, MOUSEBUTTONDOWN
from pygame.constants import RESIZABLE
from pygame.examples.joystick import BLACK
from GraphAlgoInterface import *
from GraphAlgo import *
import numpy as np
from menu import *
import tkinter as tk

radius = 15
class gui:
    """
    This class implements gui for graph display.
    """

    def __init__(self, graphAlgo: GraphAlgoInterface) -> None:
        self.graphAlgo = graphAlgo
        WIDTH, HEIGHT = 1080, 720
        self.screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        self.GC = None
        self.SP = None
        self.TSP = None
        clock = pg.time.Clock()

        # Create buttons for menu
        center = Button('Center', (70, 20))
        center.add_click_listener(lambda: self._setCenter(self.graphAlgo.centerPoint()[0]))
        load = Button('Load', (70, 20))
        load.add_click_listener(self._loadnewGraph)
        save = Button('Save', (70, 20))
        save.add_click_listener(self._savegraph)
        short = Button('ShortPath', (70, 20))
        short.add_click_listener(self._selectShortPath)
        tsp = Button('TSP', (70, 20))
        tsp.add_click_listener(lambda: self._selectTSP())
        file = SubMenuItem('File', (70, 20), [load, save], color=Color(51, 0, 25))
        algo = SubMenuItem('Show', (70, 20), [center, short, tsp], color=Color(51, 0, 25))
        menu = MenuItem('Menu', (70, 20), [file, algo], Color(51, 0, 25))
        m = MenuBar([menu])

        pg.init()
        pg.font.init()

        while True:
            self.screen.fill(Color("#513506"))

            graph = self.graphAlgo.get_graph()
            # get data proportions
            self.min_x = min(list(graph.get_dicNodes().values()), key=lambda n: n.get_pos()[0]).get_pos()[0]
            self.min_y = min(list(graph.get_dicNodes().values()), key=lambda n: n.get_pos()[1]).get_pos()[1]
            self.max_x = max(list(graph.get_dicNodes().values()), key=lambda n: n.get_pos()[0]).get_pos()[0]
            self.max_y = max(list(graph.get_dicNodes().values()), key=lambda n: n.get_pos()[1]).get_pos()[1]
            self._drawGraph()
            self._drawCenter()

            # check events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    # check menubar clicks
                    m.check()
            # refresh screen and menu
            m.render(self.screen, (0, 0))
            display.update()
            clock.tick(60)

    def _my_scale(self, data, x=False, y=False) -> float:
        """scale point by this screen"""
        if x:
            return scale(data, 50, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return scale(data, 50, self.screen.get_height() - 50, self.min_y, self.max_y)

    def _getsrcDest(self, edge: tuple) -> tuple:
        """to get src and dest points for edge"""
        graph = self.graphAlgo.get_graph()
        src = next(n for n in graph.get_dicNodes().values() if n.get_id() == edge[0])
        dest = next(n for n in graph.get_dicNodes().values() if n.get_id() == edge[1])

        # scaled positions
        src_x = self._my_scale(src.get_pos()[0], x=True)
        src_y = self._my_scale(src.get_pos()[1], y=True)
        dest_x = self._my_scale(dest.get_pos()[0], x=True)
        dest_y = self._my_scale(dest.get_pos()[1], y=True)
        return src_x, src_y, dest_x, dest_y

    def _drawGraph(self) -> None:
        """draw all nodes and edges"""
        graph = self.graphAlgo.get_graph()
        for k in graph.get_dicEdges().keys():
            src_x, src_y, dest_x, dest_y = self._getsrcDest(k)
            # draw the line
            p = np.subtract((dest_x, dest_y), segment((src_x, src_y), (dest_x, dest_y)))
            line(self.screen, Color("#2B1B01"), (src_x, src_y), p)

        for k in graph.get_dicEdges().keys():
            # find the edge nodes
            src_x, src_y, dest_x, dest_y = self._getsrcDest(k)
            # draw the arrow triangle
            p = np.subtract((dest_x, dest_y), segment((src_x, src_y), (dest_x, dest_y)))
            arrow(self.screen, Color("#003300"), (src_x, src_y), p, 10)

        FONT = pg.font.SysFont('Candara', 20, bold=True)
        self._drawPath(self.SP)
        self._drawPath(self.TSP)
        # draw nodes
        for n in graph.get_dicNodes().values():
            x = self._my_scale(n.get_pos()[0], x=True)
            y = self._my_scale(n.get_pos()[1], y=True)
            gfxdraw.filled_circle(self.screen, int(x), int(y), radius, Color(176, 143, 35))
            gfxdraw.aacircle(self.screen, int(x), int(y), radius, Color(255, 255, 255))

            # draw the node id
            id_srf = FONT.render(str(n.get_id()), True, Color(0, 0, 0))
            rect = id_srf.get_rect(center=(x, y))
            self.screen.blit(id_srf, rect)

    def _setCenter(self, id=None) -> None:
        self._update()
        if id is None:
            mb.showerror("ERROR", "The Graph is not connected")
            return
        self.GC = id

    def _drawCenter(self) -> None:
        """to draw center point of graph"""
        if self.GC is not None:
            node = self.graphAlgo.get_graph().get_dicNodes()[self.GC]
            x = self._my_scale(node.get_pos()[0], x=True)
            y = self._my_scale(node.get_pos()[1], y=True)
            gfxdraw.filled_circle(self.screen, int(x), int(y),
                                  radius, Color('#A62360'))
            gfxdraw.aacircle(self.screen, int(x), int(y),
                             radius, Color(255, 255, 255))
            FONT = pg.font.SysFont('Candara', 20, bold=True)
            text = FONT.render('Center point', False, (0, 0, 0))
            rect = text.get_rect(center=(x, y - 50))
            self.screen.blit(text, rect)
            id_srf = FONT.render(str(self.GC), True, Color(0, 0, 0))
            rect = id_srf.get_rect(center=(x, y))
            self.screen.blit(id_srf, rect)

    def _drawPath(self, path) -> None:
        """to draw TSP path/shortestPath"""
        if path is None:
            return
        i = 0
        l = len(path)
        while i + 1 < l:
            p1 = path[i]
            p2 = path[i + 1]
            # find the edge nodes
            src_x, src_y, dest_x, dest_y = self._getsrcDest((p1, p2))
            # draw the line
            p = np.subtract((dest_x, dest_y), segment((src_x, src_y), (dest_x, dest_y)))
            line(self.screen, Color("#1A8742"), (src_x, src_y), p)
            arrow(self.screen, Color("#2C037D"), (src_x, src_y), p, 10)
            i += 1

    def _loadnewGraph(self)->None:
        """open window to load graph"""
        self._update()
        fileChooser = tk.Tk()
        fileChooser.withdraw()
        file = askopenfilename(filetypes=[("json", "*.json")])
        try:
            # self.graphAlgo = GraphAlgo()
            self.graphAlgo.load_from_json(file)
            fileChooser.destroy()
        except:
            return

    def _savegraph(self)->None:
        """open window to save this graph"""
        fileChooser = tk.Tk()
        fileChooser.withdraw()
        file = asksaveasfilename(filetypes=[("json", "*.json")])
        try:
            self.graphAlgo.save_to_json(file)
            fileChooser.destroy()
        except:
            return

    def _selectTSP(self)->None:
        """open dialog window to ask TSP"""
        self._update()
        window = tk.Tk()
        window.title('Select')
        window.geometry('350x120')
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
        dest['state'] = 'readonly'
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

        def find():
            path, dis = self.graphAlgo.TSP(cur)
            self.TSP = path
            window.destroy()
            self._drawPath(self.SP)

        find = tk.Button(window, text="Find", bg='yellow', command=find)
        find.grid(column=2, row=10, pady=(10, 2), padx=(20, 0))
        window.mainloop()
        return

    def _selectShortPath(self)->None:
        # Creating tkinter window
        self._update()
        window = tk.Tk()
        window.title('Find short path')
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

        def find():
            if src.get() == "" or dest.get() == "":
                return
            dis, path = self.graphAlgo.shortest_path(int(src.get()), int(dest.get()))
            window.destroy()
            if dis == math.inf:
                mb.showerror("ERROR", "No path from src to dest!")
                return
            self.SP = path

        g = tk.StringVar()
        dest = ttk.Combobox(window, width=10, textvariable=g)
        dest['values'] = [i for i in self.graphAlgo.get_graph().get_all_v().keys()]
        dest.grid(column=2, row=8, pady=(10, 2), padx=(20, 0))

        but = tk.Button(window, text="Find", bg='yellow', command=find)
        but.grid(column=2, row=10, pady=(10, 2), padx=(20, 0))
        window.mainloop()

    def _update(self)->None:
        """
        update for delete temp draw
        """
        self.SP = None
        self.TSP = None
        self.GC = None


def scale(data, min_screen, max_screen, min_data, max_data)->float:
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimensions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen




"""
Functions for a line segment to fit the arrow triangle
"""


def normalize(v:tuple)->tuple:
    """v/||v||"""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def segment(start:tuple, end:tuple)->tuple:
    """calculate segment line , use normalization"""
    v = np.subtract(end, start)
    b = tuple(normalize(v) * 20)
    return b


def line(screen, color, start, end, thickness=4)->None:
    """
    to draw line (in accordance with the arrow triangle)
    """
    pg.draw.line(screen, color, start, np.subtract(end, tuple(normalize(np.subtract(end, start)) * 5)), thickness)


def arrow(screen, color, start, end, trirad)->None:
    """

    :param screen: surface that draw about it
    :param color: color of triangle
    :param start: src vertical of line
    :param end: dest vertical of line
    :param trirad: size of triangle
    """
    rad = math.pi / 180
    rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi / 2
    pg.draw.polygon(screen, color, ((end[0] + trirad * math.sin(rotation),
                                     end[1] + trirad * math.cos(rotation)),
                                    (end[0] + trirad * math.sin(rotation - 120 * rad),
                                     end[1] + trirad * math.cos(rotation - 120 * rad)),
                                    (end[0] + trirad * math.sin(rotation + 120 * rad),
                                     end[1] + trirad * math.cos(rotation + 120 * rad))))
