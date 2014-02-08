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


class Perso(pygame.sprite.Sprite):
    def __init__(self, screen, image, *groups):
        super(Perso, self).__init__(*groups)
        self.screen = screen
        self.image = pygame.image.load(image)
        self.position = (0, 0)
        self.px,self.py = self.position
        self.rect = pygame.rect.Rect((0,0), self.image.get_size())

    def update(self, dt, game):
        game.tilemap.set_focus(self.px, self.py)



class Game(object):

    def main(self,screen):
        self.tilemap = tmx.load('example.tmx', screen.get_size())
        self.config = Config(self.tilemap, screen)
        self.clock = pygame.time.Clock()
        self.players = tmx.SpriteLayer()
        self.perso = Perso(screen, "perso.png", self.players)
        self.userInput = UserInput(self.config, self.perso, self.tilemap)
        self.tilemap.layers.append(self.players)
        # add an enemy for each "enemy" trigger in the map



        while True:
            dt = self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.tilemap.update(dt, self)
            screen.fill((0,0,0))

            self.tilemap.draw(screen)
            pygame.display.flip()



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Game().main(screen)