# -*- coding: utf-8 -*-
import pygame
import tmx

class Config():
    def __init__(self, tilemap, screensize):
        self.isFullScreen = False
        self.bigWidth = tilemap.width * tilemap.tile_width
        self.bigHeight = tilemap.height * tilemap.tile_height
        self.screensize = screensize
        self.xtiles = tilemap.tile_width # how many grid tiles for x axis
        self.ytiles = tilemap.tile_height # how many grid tiles for y axis
        self.title = "prototype"
        self.scrollstepx = 1 # how many pixels to scroll when pressing cursor key
        self.scrollstepy = 1 # how many pixels to scroll when pressing cursor key
        self.cornerpoint = [0, 0] # left upper edge of visible screen rect inside bigmap

class UserInput:
    def __init__(self, config, perso, tilemap):
        self.config = config
        self.perso = perso
        self.tilemap = tilemap #TODO remove if not working
        self.backup = ""

    def update(self):
        # -------- scroll the big map ----------
        pressedkeys = pygame.key.get_pressed()
        if pressedkeys[pygame.K_LEFT]:
            self.perso.position['x'] -= self.config.scrollstepx
        if pressedkeys[pygame.K_RIGHT]:
            self.perso.position['x'] += self.config.scrollstepx
        if pressedkeys[pygame.K_UP]:
            self.perso.position['y'] -= self.config.scrollstepy
        if pressedkeys[pygame.K_DOWN]:
            self.perso.position['y'] += self.config.scrollstepy
        self.tilemap.set_focus(self.perso.position['x'], self.perso.position['y'])

class Perso(pygame.sprite.Sprite):
    def __init__(self, screen, image):
        super(Perso, self).__init__()
        self.screen = screen
        self.image = pygame.image.load(image)
        self.position = {'x': 320, 'y': 240}


    def update(self):
        self.screen.blit(self.image, (self.position['x'], self.position['y']))


def main():
    pygame.init()
    screensize = (640, 480)
    screen = pygame.display.set_mode(screensize)
    tilemap = tmx.load('example.tmx', screen.get_size())
    tilemap.set_focus(0, 0)
    config = Config(tilemap, screen)
    clock = pygame.time.Clock()
    dt = clock.tick(30)
    perso = Perso(screen, "perso.png")
    userInput = UserInput(config, perso, tilemap)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        tilemap.update(dt)
        black = (0,0,0)
        screen.fill(black)
        # Draw all layers of the tilemap to the screen.
        tilemap.draw(screen)
        userInput.update()
        perso.update()
        # Refresh the display window.
        pygame.display.flip()



if __name__ == '__main__':
    main()