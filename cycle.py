import os
import sys
import pygame as pg


#These are the color cycles that will be used.
LOW = [(32,136,168), (48,144,168), (72,152,176), (96,160,184), (120,168,192),
       (136,176,200), (160,184,208), (184,192,216), (208,208,224)]

HIGH = [(80, 128,152), (96,136,160), (56,120,144)]

FOAM = [(184,192,216), (48,144,169)]


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
        cycles = [Cycle(self.image.subsurface(0,507,498,93),(0,507),LOW),
                  Cycle(self.image.subsurface(0,330,498,153), (0,330),
                        HIGH, fps=10),
                  Cycle(self.image.subsurface(0,483,498,12), (0,483), FOAM)]
        self.cycles = pg.sprite.Group(cycles)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def update(self):
        self.cycles.update(pg.time.get_ticks())

    def draw(self):
        self.cycles.draw(self.screen)

    def main_loop(self):
        self.screen.blit(self.image, (0,0))
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()
            self.clock.tick(self.fps)


class Cycle(pg.sprite.Sprite):
    def __init__(self, image, pos, color_cycle, fps=20, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.palette = list(self.image.get_palette())
        self.cycle = self.make_cycle(color_cycle)
        self.fps = fps
        self.timer = pg.time.get_ticks()

    def make_cycle(self, cycle):
        return {color:cycle[(i-1)%len(cycle)] for i,color in enumerate(cycle)}

    def advance_cycle(self):
        for i,color in enumerate(self.palette):
            self.palette[i] = pg.Color(*self.cycle.get(color[:3], color))
        self.image.set_palette(self.palette)

    def update(self, now):
        if now-self.timer > 1000.0/self.fps:
            self.advance_cycle()
            self.timer = now

    def draw(self, surface):
        surface.blit(self.image, self.rect)


if __name__ == "__main__":
    Control().main_loop()
    pg.quit()
    sys.exit()
