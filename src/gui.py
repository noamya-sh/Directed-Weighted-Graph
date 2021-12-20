import math
import pygame as pg
from pygame import Color, display, gfxdraw, Rect
from pygame.constants import RESIZABLE
from GraphAlgo import *
# init pg
from src.GraphAlgo import GraphAlgo

class gui:
    def __init__(self,graphAlgo:GraphAlgoInterface):
        self.graphAlgo = graphAlgo
        WIDTH, HEIGHT = 1080, 720
        self.screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        while (True):
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

            # h = GraphAlgo()
            # h.load_from_json(".\data\A2.json")
            graph = self.graphAlgo.get_graph()

            # get data proportions
            self.min_x = min(list(graph.dicNodes.values()), key=lambda n: n.pos.x).pos.x
            self.min_y = min(list(graph.dicNodes.values()), key=lambda n: n.pos.y).pos.y
            self.max_x = max(list(graph.dicNodes.values()), key=lambda n: n.pos.x).pos.x
            self.max_y = max(list(graph.dicNodes.values()), key=lambda n: n.pos.y).pos.y

            # draw edges
            for e in graph.dicEdges.values():
                # find the edge nodes
                src = next(n for n in graph.dicNodes.values() if n.id == e.src)
                dest = next(n for n in graph.dicNodes.values() if n.id == e.dest)

                # scaled positions
                src_x = self.my_scale(src.pos.x, x=True)
                src_y = self.my_scale(src.pos.y, y=True)
                dest_x = self.my_scale(dest.pos.x, x=True)
                dest_y = self.my_scale(dest.pos.y, y=True)

                # draw the line
                p = np.subtract((dest_x, dest_y), yashar((src_x, src_y), (dest_x, dest_y)))
                line(self.screen,Color(153, 153, 0), (src_x, src_y), p)
                # pg.draw.line(screen, Color(153, 153, 0),
                #                  (src_x, src_y), (dest_x, dest_y), width=4)
            for e in graph.dicEdges.values():
                # find the edge nodes
                src = next(n for n in graph.dicNodes.values() if n.id == e.src)
                dest = next(n for n in graph.dicNodes.values() if n.id == e.dest)

                # scaled positions
                src_x = self.my_scale(src.pos.x, x=True)
                src_y = self.my_scale(src.pos.y, y=True)
                dest_x = self.my_scale(dest.pos.x, x=True)
                dest_y = self.my_scale(dest.pos.y, y=True)

                # draw the line
                p = np.subtract((dest_x, dest_y), yashar((src_x, src_y), (dest_x, dest_y)))
                arrow(self.screen, Color(0, 0, 0), (src_x, src_y), p, 10)
            # draw nodes
            for n in graph.dicNodes.values():
                x = self.my_scale(n.pos.x, x=True)
                y = self.my_scale(n.pos.y, y=True)

                # its just to get a nice antialiased circle
                gfxdraw.filled_circle(self.screen, int(x), int(y),
                                      radius, Color(176, 143, 35))
                gfxdraw.aacircle(self.screen, int(x), int(y),
                                 radius, Color(255, 255, 255))

                # draw the node id
                id_srf = FONT.render(str(n.id), True, Color(0, 0, 0))
                rect = id_srf.get_rect(center=(x, y))
                self.screen.blit(id_srf, rect)
            # button(0, HEIGHT-50, 80, 50)
            # update screen changes
            display.update()

            # refresh rate
            clock.tick(60)
    def my_scale(self,data, x=False, y=False):
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
import numpy as np


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def yashar(start, end):
    v = np.subtract(end, start)
    b = tuple(normalize(v) * 20)
    return b


def line(screen,lcolor, start, end, thickness=4):
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

def button(screen,x, y, w, h, inactive=None, active=None, action=None):
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


