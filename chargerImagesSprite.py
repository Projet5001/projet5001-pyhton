
import pygame

class Charger_Images_Sprite(pygame.sprite.Sprite):
    def __init__(self,imageDuSprite):

        self.image_set = pygame.image.load(imageDuSprite)
        self.personnage = [] # La liste des images de personnages en png ou jpg a voir ???
        self.charge_les_Images()

    def charge_les_Images(self):
        #Pour la marche du personnage
        posY = 15
        #Il y a 4 lignes
        for nbr in range(1,11,1):
            imgIndex = 0
            # Chaque lignes contients 7 images
            for nbr in range(1,8,1):
               #print "NBR VALUE =" + str(40+imgIndex)
               self.personnage.append(self.image_set.subsurface((40+imgIndex,posY,50,80)))
               imgIndex += 60
            posY += 95

        #Pour la saut du personnage
        posY = 965
        #Il y a 4 lignes
        for nbr in range(1,3,1):
            imgIndex = 0
            # Chaque lignes contients 7 images
            for nbr in range(1,8,1):
               #print "NBR VALUE =" + str(40+imgIndex)
               self.personnage.append(self.image_set.subsurface((40+imgIndex,posY,90,80)))
               imgIndex += 100
            posY += 95