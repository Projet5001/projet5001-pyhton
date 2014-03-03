# -*- coding: utf-8 -*-
import pygame
from lib import tmx

class PlayerHud(tmx.Layer):
    def __init__(self, name, player, screen, tilemap):
        """

        :param name: Le nom du hub (permet la recherche dans layers[name]
        :param player: Le joueur auquelle nous voulons afficher l'information
        :param screen: Permet de récupérer (width, height) de l'écran dynamiquement
        """
        self.name = name
        self.visible = False
        self.player = player
        self.screen = screen
        self.tilemap = tilemap

    def move(self, offsetx, offsety):
        pass

    def setVisible(self, bool):
        self.visible = bool

    def __iter__(self):
        return tmx.LayerIterator(self)

    def update(self, dt, *args):
        pass

    def draw(self, surface):
        hub = self.__followPlayer() #Tous les autres objets seront placés en relation avec ce point
        pygame.draw.line(surface, (0, 0, 0), (hub["x"], hub["y"]), (hub["x"] + 1, hub["y"]), 1)
        hub["y"] -= self.tilemap.tile_height
        self.__showName(surface, (hub["x"], hub["y"]))
        self.__showHealth(surface, (hub["x"], hub["y"] + 5))

    def __showName(self, surface, hub):
        myfont = pygame.font.SysFont("monospace", 15, True)
        label = myfont.render(self.player.name, 1, (255,255,255))
        surface.blit(label, ((hub[0] - (label.get_width() / 2), hub[1] - (self.tilemap.tile_height))))

    def __showHealth(self, surface, hub):
        #line(Surface, color, start_pos, end_pos, width=1) -> Rect
        tileHalfWidth = self.tilemap.tile_width / 2
        originx = hub[0] - tileHalfWidth
        originy = hub[1] -  self.tilemap.tile_height / 2
        pygame.draw.line(surface, (0, 0, 0), (originx, originy), (originx + tileHalfWidth * 2, originy), 5)
        health = (tileHalfWidth * 2)  * (float(self.player.health["hp"]) / self.player.health["max"])
        pygame.draw.line(surface, (255, 0, 0), (originx, originy), (originx + health, originy), 3)

    def __followPlayer(self):
        #Centrer la position du HUD par rapport au personnage
        playerx, playery = self.player.collision_rect.x, self.player.collision_rect.y
        hubx = playerx - (playerx - (self.screen.get_width() / 2))
        huby = playery - (playery - (self.screen.get_height() / 2))
        #Gérer les bordures
        if(playerx  < hubx):
            hubx = playerx
        if(playery  < huby):
            huby = playery
        centerx = self.tilemap.px_width - self.screen.get_width() / 2
        centery = self.tilemap.px_height - self.screen.get_height() / 2
        if(playerx > centerx):
            hubx += playerx - centerx
        if(playery > centery):
            huby += playery - centery
        hubx += self.tilemap.tile_width / 2
        huby += self.tilemap.tile_height / 2
        return {"x": hubx, "y":huby}

