# -*- coding: utf-8 -*-
#
# Projet5001: un jeu de survie post-apocalyptique
# Copyright (C) 2014  Équipe Projet5001
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import pygame


class Charger_Images_Sprite(pygame.sprite.Sprite):
    def __init__(self,imageDuSprite,nombre_ligne):

        self.image_set = pygame.image.load(imageDuSprite)
        self.personnage = [] # La liste des images de personnages en png ou jpg a voir ???
        self.charge_les_Images(nombre_ligne)

    def charge_les_Images(self,nombre_ligne):
        #Pour la marche du personnage
        posY = 15
        #Il y a 4 lignes
        for nbr in range(1,nombre_ligne+1,1):
            imgIndex = 0
            # Chaque lignes contients 7 images
            for nbr in range(1,8,1):
               #print "NBR VALUE =" + str(40+imgIndex)
               self.personnage.append(self.image_set.subsurface((40+imgIndex,posY,120,100)))
               imgIndex += 130
            posY += 110

        # #Pour la saut du personnage
        # posY = 965
        # #Il y a 4 lignes
        # for nbr in range(1,3,1):
        #     imgIndex = 0
        #     # Chaque lignes contients 7 images
        #     for nbr in range(1,8,1):
        #        #print "NBR VALUE =" + str(40+imgIndex)
        #        self.personnage.append(self.image_set.subsurface((40+imgIndex,posY,90,80)))
        #        imgIndex += 100
        #     posY += 95