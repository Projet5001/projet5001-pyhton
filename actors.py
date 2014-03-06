import pygame
from pygame import rect as rect


class Actor(pygame.sprite.Sprite):
    def __init__(self, image, position, *groups):
        super(Actor, self).__init__(*groups)
        self.image = pygame.image.load(image)
        self.rect = rect.Rect(position, self.image.get_size())
        self.collision_rect = rect.Rect(position[0], position[1],25, 20)

        self.saveLastPos()

        self.tools = {}

        #spec of perso
        self.dommage = 1
        self.protection = 0
        self.life = 100
        self.speed = 8
        self.accel = 1
        self.isDoing = 'nothing'

    def save_x_pos(self):
        self.last_x = self.rect.x
        self.last_coll_x = self.collision_rect.x

    def save_y_pos(self):
        self.last_y = self.rect.y
        self.last_coll_y = self.collision_rect.y

    def saveLastPos(self):
        self.save_x_pos()
        self.save_y_pos()

    def resetX(self):
        self.rect.x = self.last_x
        self.collision_rect.x = self.last_coll_x
        self.save_x_pos()

    def resetY(self):
        self.rect.y = self.last_y
        self.collision_rect.y = self.last_coll_y
        self.save_y_pos()

    def resetPos(self):
        self.resetX()
        self.resetY()

    def definir_position(self, x, y):
        self.rect.x = x - 2
        self.rect.y = y - 30
        self.collision_rect.x = x
        self.collision_rect.y = y
        self.saveLastPos()

    def move(self, x, y):
        self.rect.move_ip(x, y)
        self.collision_rect.move_ip(x, y)
        for tool in self.tools.values():
            tool.definir_position(self.rect.x, self.rect.y)

    def attack(self):
        return self.dommage * self.luck()

    def take_dommage(self, dommage):
        self.life -= (dommage - self.protectionTotal())
        self.isBleeding()

    def block(self):
        pass

    def luck(self):
        return 1

    def protectionTotal(self):
        return self.protection

    def ajoute_outils(self, tool):
        self.tools[tool.name] = tool
        tool.definir_position(self.rect.x, self.rect.y)

    def make_tools_visible(self, visible):
        for tool in self.tools.values():
            print tool
            tool.visible = visible

    #fake death juste pour le moment en enleve le sprit de la map
    def isBleeding(self):
        if self.life == 0:
            self.kill()

    # this need the dt and game otherwise bug in tmx
    def update(self, dt, game):
        pass
