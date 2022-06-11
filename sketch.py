import numpy as np
import agent
import pygame as pg
import sys


FPS = 60




def main():
    screen = pg.display.set_mode((1200, 800))
    clock = pg.time.Clock()

    player = agent.Vehicle(300,300)
    pellet = agent.Food(300,400)

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    done = True

        screen.fill(0)
        player.seek(pg.mouse.get_pos())
        player.update()
        player.display(screen)
        pellet.display(screen)
        if pellet.rect.colliderect(player.rect):
            print('Collision')
        # screen.blit(screen, player.display(screen))
        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()
