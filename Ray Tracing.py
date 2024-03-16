import pygame as pg
import pygame.math as math
from random import randint
from math import radians, sin, cos, dist
import sys

pg.init()

WIDTH, HEIGHT = 800, 800

# Setup
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Ray Tracing")
FPS = 60

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

numOfWalls = 5 # CHANGE THIS VALUE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Vector:
    def __init__(self, x, y, vec):
        self.x = x
        self.y = y
        self.vec = vec

class Wall:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.color = RED


# Create walls
walls = []
for n in range(numOfWalls):
    x1 = randint(0, WIDTH)
    y1 = randint(0, WIDTH)
    x2 = randint(0, WIDTH)
    y2 = randint(0, WIDTH)

    walls.append(Wall((x1, y1), (x2, y2)))


def draw(offset):
    WIN.fill(BLACK)
    lines = pg.Surface((WIDTH, HEIGHT))
    lines.set_alpha(100)

    # Create all rays
    rays = []
    angle = 5 # 0 < ANGLE < 360 CHANGE THIS VALUE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for angle in range(0, 360, angle):
        angle += offset
        rays.append(Vector(400, 400, math.Vector2(cos(radians(angle))*3000, sin(radians(angle))*3000)))
    for ray in rays:
        ray.x, ray.y = pg.mouse.get_pos()

    for ray in rays:
        x3 = ray.x
        y3 = ray.y
        x4 = ray.vec.x + ray.x
        y4 = ray.vec.y + ray.y

        intersections = []
        distance = lambda pos: dist((pos[0], pos[1]), (ray.x, ray.y))
        
        for wall in walls:
            x1 = wall.p1[0]
            y1 = wall.p1[1]
            x2 = wall.p2[0]
            y2 = wall.p2[1]


            den = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4) 
            if den == 0:
                continue

            t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / den
            u = -((x1 - x3)*(y1 - y2) - (y1 - y3)*(x1 - x2)) / den



            if 0 <= t <= 1 and u <= 0:
                x = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / den
                y = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / den

                intersections.append((x, y))
                

        
        if intersections:
            intersections.sort(key=distance, reverse=False)
            x, y = intersections[0][0], intersections[0][1]
            pg.draw.line(lines, WHITE, (ray.x, ray.y), (x, y), 2)

        else:
            pg.draw.line(lines, WHITE, (x3, y3), (x4, y4), 2)

    for wall in walls:
        pg.draw.line(WIN, wall.color, wall.p1, wall.p2, 5)



    WIN.blit(lines, (0, 0))

    pg.display.update()


def main():
    clock = pg.time.Clock()
    offset = 0

    # Main loop
    while True:
        clock.tick(FPS)

        # Events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()


        offset += 0.05
        
        draw(offset)       

main()