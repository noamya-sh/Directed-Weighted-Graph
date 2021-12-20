import math
import pygame as pg
from pygame import Color, display, gfxdraw, Rect
from pygame.constants import RESIZABLE

# init pg
from src.GraphAlgo import GraphAlgo

WIDTH, HEIGHT = 1080, 720

pg.init()
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pg.time.Clock()
pg.font.init()

FONT = pg.font.SysFont('Arial', 20, bold=True)


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimensions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


h = GraphAlgo()
h.load_from_json(".\data\A1.json")
graph = h.get_graph()

# # get the current directory path
# root_path = os.path.dirname(os.path.abspath(__file__))
#
# # load the json file into SimpleNamespace Object
# with open(root_path + '/graph_triangle.json', 'r') as file:
#     graph = json.load(
#         file, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

# get data proportions
min_x = min(list(graph.dicNodes.values()), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.dicNodes.values()), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.dicNodes.values()), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.dicNodes.values()), key=lambda n: n.pos.y).pos.y


# decorate scale with the correct values


def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


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


def line(lcolor, start, end, thickness=4):
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

def button(x, y, w, h, inactive=None, active=None, action=None):
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

while (True):
    # check events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)

    # refresh screen
    screen.fill(Color(51, 25, 0))

    # draw edges
    for e in graph.dicEdges.values():
        # find the edge nodes
        src = next(n for n in graph.dicNodes.values() if n.id == e.src)
        dest = next(n for n in graph.dicNodes.values() if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        p = np.subtract((dest_x, dest_y), yashar((src_x, src_y), (dest_x, dest_y)))
        line(Color(153, 153, 0), (src_x, src_y), p)
        # pg.draw.line(screen, Color(153, 153, 0),
        #                  (src_x, src_y), (dest_x, dest_y), width=4)
    for e in graph.dicEdges.values():
        # find the edge nodes
        src = next(n for n in graph.dicNodes.values() if n.id == e.src)
        dest = next(n for n in graph.dicNodes.values() if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        p = np.subtract((dest_x, dest_y), yashar((src_x, src_y), (dest_x, dest_y)))
        arrow(screen, Color(0, 0, 0), (src_x, src_y), p, 10)
    # draw nodes
    for n in graph.dicNodes.values():
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(176, 143, 35))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(0, 0, 0))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)
    # button(0, HEIGHT-50, 80, 50)
    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)
