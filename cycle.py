import os
import sys

import pygame as pg


FALL_1 = [(32,136,168), (48,144,168), (72,152,176), (96,160,184), (120,168,192),
          (136,176,200), (160,184,208), (184,192,216), (208,208,224)]
CYCLE = {color:FALL_1[(i-1)%len(FALL_1)] for i,color in enumerate(FALL_1)}


class Control(object):
    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pg.init()
        self.screen = pg.display.set_mode((498,600))
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.cycle_fps = 20
        self.timer = 0.0
        self.done = False
        self.image = pg.image.load("mega.png").convert(8)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def cycle(self):
        palette = list(self.image.get_palette())
        for i,color in enumerate(palette):
            palette[i] = pg.Color(*CYCLE.get(color[:3], color))
        self.image.set_palette(palette)

    def update(self):
        now = pg.time.get_ticks()
        if now-self.timer > 1000.0/self.cycle_fps:
            self.cycle()
            self.timer = now

    def draw(self):
        self.screen.blit(self.image, (0,0))

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    Control().main_loop()
    pg.quit()
    sys.exit()