
import pygame

class Charger_Images_Sprite(pygame.sprite.Sprite):
    def __init__(self,imageDuSprite):
        #super(ChargeurImages, self).__init__(*groups)e
        #print "Charger_Images_Sprite _____________________________________"
        self.image_set = pygame.image.load(imageDuSprite)

        self.personnage = [] # La liste des images de personnages en png ou jpg a voir ???
        self.charge_les_Images()
        #self.image = self.personnage[0] # ou [self.lesImages]

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





       # self.charger_Images_Sprite = chargerImagesSprite.Charger_Images_Sprite(imageDuSprite)
       #  self.rect = pygame.rect.Rect(position, self.charger_Images_Sprite.image.get_size())
       #  self.collision_rect = pygame.rect.Rect(position[0], position[1],25, 20)
       #
       #
       #  self.image = self.charger_Images_Sprite.image
       #  self.personnage = self.charger_Images_Sprite.personnage
       #  self.actor_action = actors_actions.ActorActions(self.image, self.personnage)
       #  self.actor_action.reinitValSiDetecter()
       #  self.image = self.actor_action.image