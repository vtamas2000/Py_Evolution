import numpy as np
import agent
import pygame as pg
import sys
import random

Vector = pg.math.Vector2

FPS = 60
WIDTH = 1200
HEIGHT = 800
MAXCREATURES = 10
MAXFOOD = 60
FOODENERGY = 1000

creatures = [agent.Creature(random.randint(0,WIDTH),random.randint(0,HEIGHT)) for _ in range(MAXCREATURES)]
foods = [agent.Food(random.randint(0,WIDTH),random.randint(0,HEIGHT), FOODENERGY) for _ in range(MAXFOOD)]

boundary = pg.Rect(30,30,WIDTH-60,HEIGHT-60)


def mapColor(x):
    return [int(1 / (1 + np.exp(np.multiply(-1, i)))*255) for i in x]


# def coordinate(time):
#     for creature in creatures:
#         if not creature.alive:
#             if creature.energy > 0:
#                 f = agent.Food(creature.position.x, creature.position.y, creature.energy)
#                 # foods.append()
#             creatures.remove(creature)
#         index = creature.rect.collidelist(foods)
#         if index > -1:
#             creature.energy += foods[index].energy
#             foods.remove(foods[index])
#             # foods.append(agent.Food(random.randint(0,WIDTH),random.randint(0,HEIGHT)))
#     while len(creatures) < MAXCREATURES:
#         creatures.append(agent.Creature(random.randint(0,WIDTH),random.randint(0,HEIGHT)))
#     if time % 100 == 0:
#         foods.append(agent.Food(random.randint(0,WIDTH),random.randint(0,HEIGHT), FOODENERGY))


# def think(surf):
#     for creature in creatures:
#         output = creature.think(surf, foods, boundary)
#         creature.applyForce(Vector(output[0]/10, output[1]/10))
#         if output[2] > 0 and creature.justReproduced <= 0 and creature.energy > agent.CHILDENERGY * 2:
#             creatures.append(creature.reproduce())
#         creature.color = mapColor(output[3:6])
#         # creature.boundary(boundary)
#         creature.continuousBoundary(WIDTH, HEIGHT)
#         creature.update()


# def drawScreen(surf, debug):
#     if not debug:
#         surf.fill(0)
#     for creature in creatures:
#         creature.display(surf)
#     for food in foods:
#         food.display(surf)

def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    done = False
    debug = False
    paused = False
    Time = 0
    foodSpawnRate = 100

    trackedCreature = None
    font = pg.font.SysFont('arial', 30)

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    done = True
                if event.key == pg.K_d:
                    debug = not debug
                if event.key == pg.K_e:
                    trackedCreature = None
                if event.key == pg.K_SPACE:
                    paused = not paused
                if event.key == pg.K_UP:
                    if foodSpawnRate > 40:
                        foodSpawnRate -= 20
                if event.key == pg.K_DOWN:
                    foodSpawnRate += 20
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for creature in creatures:
                    if creature.rect.collidepoint(pg.mouse.get_pos()):
                        trackedCreature = creature

        # screen.fill(0)
        # player.seek(pg.mouse.get_pos())
        # player.update()
        # player.display(screen)
        # pellet.display(screen)
        # if pellet.rect.colliderect(player.rect):
        #     print('Collision')
        # # screen.blit(screen, player.display(screen))
        # pg.display.update()
        

        if not paused:
            screen.fill(0)

            # Coordinate
            for creature in creatures:
                if not creature.alive:
                    if creature.energy > 0:
                        foods.append(agent.Food(creature.position.x, creature.position.y, creature.energy))
                    creatures.remove(creature)
                    continue
                index = creature.rect.collidelist(foods)
                if index > -1:
                    creature.energy += foods[index].energy
                    foods.remove(foods[index])
                    # foods.append(agent.Food(random.randint(0,WIDTH),random.randint(0,HEIGHT)))
            while len(creatures) < MAXCREATURES:
                creatures.append(agent.Creature(random.randint(0,WIDTH),random.randint(0,HEIGHT)))
            if Time % foodSpawnRate == 0:
                foods.append(agent.Food(random.randint(0,WIDTH),random.randint(0,HEIGHT), FOODENERGY))


            # Think
            for creature in creatures:
                output = creature.think(screen, foods, boundary)
                creature.applyForce(Vector(output[0]/10, output[1]/10))
                if output[2] > 0 and creature.justReproduced <= 0 and creature.energy > agent.CHILDENERGY * 2:
                    creatures.append(creature.reproduce())
                creature.color = mapColor(output[3:6])
                # creature.boundary(boundary)
                creature.continuousBoundary(WIDTH, HEIGHT)
                creature.update()

            Time += 1

        # Draw Screen  
        if not debug:
            screen.fill(0)
        for creature in creatures:
            creature.display(screen)
        for food in foods:
            food.display(screen)


            # coordinate(Time)
            # think(screen)
            

        # drawScreen(screen, debug)

        if not trackedCreature is None:
            t = 'Energy ' + str(int(trackedCreature.energy)) + '    Age ' + str(trackedCreature.age) + '    Gen ' + str(trackedCreature.generation)
            text = font.render(t, True, [0,0,0], [255,255,255])
            textRect = text.get_rect()
            textRect.center = (300, HEIGHT - 100)
            screen.blit(text, textRect)
            pg.draw.circle(screen, pg.Color(255,255,255), trackedCreature.position, 30, width=3)
        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()
