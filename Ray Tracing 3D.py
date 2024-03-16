from contextlib import suppress
import pygame as pg
import pygame.math as math
from random import randint, choice
from math import radians, sin, cos, dist
import sys

pg.init()

WIDTH, HEIGHT = 1600, 800
MAPW, MAPH = 400, 200
# Setup
FOV = 140
WIN = pg.display.set_mode((WIDTH, HEIGHT))
MAP = pg.Surface((MAPW, MAPH))

pg.display.set_caption("Ray Tracing")
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SPEED = 5
SPEEDMOS = 2
pX, pY = 500, 500



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
        self.color = choice(colors)
        colors.remove(self.color)

def generate_walls():
    global colors
    colors = [
        (255, 0, 0),
        (0, 0, 255),
        (0, 255, 0), 
        (255, 255, 0), 
        (200, 100, 0), 
        (255, 0, 255), 
        (255, 128, 215), 
        (79, 136, 227),
        (140, 22, 79),
        (75, 79, 22),
        (0, 255, 255)
    ]


    walls = []    

    walls.append(Wall((250, 350), (400, 350)))
    walls.append(Wall((400, 350), (400, 375)))
    walls.append(Wall((400, 375), (250, 375)))
    walls.append(Wall((250, 350), (250, 375)))


    for n in range(numOfWalls):
        x1 = randint(0, WIDTH)
        y1 = randint(0, HEIGHT)
        x2 = randint(0, WIDTH)
        y2 = randint(0, HEIGHT)

        walls.append(Wall((x1, y1), (x2, y2)))
    return walls


def draw(offset, useMap):
    global centerAngle

    WIN.fill(BLACK)

    lines = pg.Surface((WIDTH, HEIGHT))
    lines.set_alpha(100)

    # Create all rays
    hits = []
    distances = []
    rays = []
    criticals = []

    for angle in range(0, FOV*2):
        if angle == FOV:
            centerAngle = angle/2+offset

        angle /= 2
        angle += offset
        rays.append(Vector(400, 400, math.Vector2(cos(radians(angle))*3000, sin(radians(angle))*3000)))
    for ray in rays:
        ray.x, ray.y = pX, pY

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

                intersections.append((x, y, wall.color))
                

        
        if intersections:
            intersections.sort(key=distance, reverse=False)
            x, y, color = intersections[0][0], intersections[0][1], intersections[0][2]
            criticals.append((x, y))
            hits.append(color)
            distances.append(dist((ray.x, ray.y), (x, y)))

        else:
            criticals.append((x4, y4))
            hits.append(WHITE)
            distances.append(dist((ray.x, ray.y), (x4, y4)))

    # 3d view
    draw_3d(hits, distances)

    MAP.fill(BLACK)

    # Rays
    criticals.append((pX, pY))
    for i, p in enumerate(criticals):
        criticals[i] = (p[0]/4, p[1]/4)
    criticals = tuple(criticals)

    pg.draw.polygon(MAP, (200, 200, 200), criticals)

    # Walls
    for wall in walls:
        pg.draw.line(MAP, wall.color, (wall.p1[0]/4, wall.p1[1]/4), (wall.p2[0]/4, wall.p2[1]/4), 3)
    
    # Player
    pg.draw.circle(MAP, (255, 0, 0), (pX/4, pY/4), 4)

    # Border
    pg.draw.rect(MAP, BLACK, (0, 0, MAPW, MAPH), 2)

    if useMap:
        WIN.blit(MAP, (20, 20))


    pg.display.update()

def draw_3d(hits, distances):
    pg.draw.rect(WIN, (50, 50, 50), (0, HEIGHT/2, WIDTH, HEIGHT))
    pg.draw.rect(WIN, WHITE, (0, 0, WIDTH, HEIGHT/2))

    increment = WIDTH/len(hits)

    for i, hit in enumerate(hits):
        if i == 0:
            previousColor = hit
            previousDist = distances[i]
            previousX = 0

        if i+1 == len(hits) or previousColor != hits[i+1]:
            h1 = (HEIGHT*60)/previousDist
            h2 = (HEIGHT*60)/distances[i]
            top1 = (HEIGHT-h1)/2
            top2 = (HEIGHT-h2)/2

            topLeft = (previousX, top1)
            bottomLeft = (previousX, top1+h1)

            if i+1 == len(hits):
                topRight = ((i+1)*increment, top2)
                bottomRight = ((i+1)*increment, top2+h2)
            else:
                topRight = (i*increment, top2)
                bottomRight = (i*increment, top2+h2)

            if hit != WHITE:
                pg.draw.polygon(WIN, hit, (topLeft, topRight, bottomRight, bottomLeft))
                pg.draw.polygon(WIN, BLACK, (topLeft, topRight, bottomRight, bottomLeft), 2)

            with suppress(IndexError):
                previousColor = hits[i+1]
                previousDist = distances[i+1]
                previousX = (i)*increment


def main():
    global walls, pX, pY
    clock = pg.time.Clock()
    offset = 0
    useMap = True
    walls = generate_walls()
    # Main loop
    while True:
        clock.tick(FPS)

        # Events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    walls = generate_walls()
                if event.key == pg.K_m:
                    useMap = not useMap

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    offset += 5
                if event.button == 5:
                    offset -= 5

        # Movement
        if pg.key.get_pressed()[pg.K_LCTRL]:
            SPEED = 9
            SPEEDMOS = 3.5
        elif pg.key.get_pressed()[pg.K_LSHIFT]:
            SPEED = 1
            SPEEDMOS = 1
        else:
            SPEED = 5
            SPEEDMOS = 2


        # Looking
        if pg.key.get_pressed()[pg.K_LEFT]:
            offset -= SPEEDMOS
        if pg.key.get_pressed()[pg.K_RIGHT]:
            offset += SPEEDMOS

        draw(offset, useMap)       

        if pg.key.get_pressed()[pg.K_w]:
            pX += SPEED*cos(radians(centerAngle))
            pY += SPEED*sin(radians(centerAngle))
        if pg.key.get_pressed()[pg.K_s]:
            pX -= SPEED*cos(radians(centerAngle))
            pY -= SPEED*sin(radians(centerAngle))
        if pg.key.get_pressed()[pg.K_a]:
            pX -= SPEED*cos(radians(centerAngle+90))
            pY -= SPEED*sin(radians(centerAngle+90))
        if pg.key.get_pressed()[pg.K_d]:
            pX += SPEED*cos(radians(centerAngle+90))
            pY += SPEED*sin(radians(centerAngle+90))

main()