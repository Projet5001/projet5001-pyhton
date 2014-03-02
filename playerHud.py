# -*- coding: utf-8 -*-
import pygame

from lib import tmx

class PlayerHud(tmx.Layer):
    def __init__(self, name, player, game):
        """

        :param name: Le nom du hub (permet la recherche dans layers.__get_name__())
        :param player: Le joueur auquelle nous voulons afficher l'information
        :param screen: Permet de récupérer (width, height) de l'écran dynamiquement
        """
        self.name = name
        self.visible = True
        self.player = player
        self.game = game

    def __iter__(self):
        return tmx.LayerIterator(self)

    def update(self, dt, *args):
        pass

    def draw(self, surface):
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render(self.player.name, 1, (255,255,255))
        #Centrer la position du HUD par rapport au personnage
        playerx, playery = self.player.collision_rect.x, self.player.collision_rect.y
        hubx = playerx - (playerx - (self.game.screen.get_width() / 2))
        huby = playery - (playery - (self.game.screen.get_height() / 2))
        #Gérer les bordures
        if(playerx  < hubx):
            hubx = playerx
        if(playery  < huby):
            huby = playery
        centerx = self.game.tilemap.px_width - self.game.screen.get_width() / 2
        centery = self.game.tilemap.px_height - self.game.screen.get_height() / 2
        if(playerx > centerx):
            hubx += playerx - centerx
        if(playery > centery):
            huby += playery - centery
        print "hubx" + str(hubx) + " <=> playerx " + str(playerx)
        print "huby" + str(huby) + " <=> playery " + str(playery)
        surface.blit(label, (hubx, huby))


