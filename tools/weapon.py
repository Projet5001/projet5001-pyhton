from pygame.locals import *
from basetool import BaseTool
import pygame


class Weapon(BaseTool):
    def __init__(self, game, player, name, obj=None):
        super(Weapon, self).__init__(game, player, name, obj)
        self.hub = self.__followPlayer__()
        self.rect = Rect((self.hub[0], self.hub[1]+8), (5, 100))

    @classmethod
    def is_type_for(cls, object_type):
        return object_type == "weapon"

    def is_equippable(self):
        return True

    def draw(self, screen):
        self.hub = self.__followPlayer__()
        pygame.draw.rect(screen, (140,240,130), ((self.hub[0], self.hub[1]+8), (5, 100)))

    def definir_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, dt, *args):
        self.hub = self.__followPlayer__()
        self.rect = Rect((self.player.collision_rect[0], self.player.collision_rect[1]+8), (5, 100))

    def handle_collision(self):
        pass

    def __followPlayer__(self):
        #Centrer la position du HUD par rapport au personnage
        playerx, playery = self.player.collision_rect.x, self.player.collision_rect.y
        hubx = playerx - (playerx - (self.game.screen.get_width() / 2))
        huby = playery - (playery - (self.game.screen.get_height() / 2))

        if playerx < hubx:
            hubx = playerx

        if playery < huby:
            huby = playery

        centerx = self.game.tilemap.px_width - self.game.screen.get_width() / 2
        centery = self.game.tilemap.px_height - self.game.screen.get_height() / 2

        if playerx > centerx:
            hubx += playerx - centerx

        if playery > centery:
            huby += playery - centery
            hubx += self.game.tilemap.tile_width / 2
            huby += self.game.tilemap.tile_height / 2

        return hubx, huby
