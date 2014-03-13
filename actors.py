# -*-coding:utf-8-*-

import pygame
import  chargerImagesSprite
import actors_actions
from pygame import rect as rect


class Actor(pygame.sprite.Sprite):
    def __init__(self, image, position, *groups):
        super(Actor, self).__init__(*groups)
        # self.image = pygame.image.load(image)
        self.charger_Images_Sprite = chargerImagesSprite.Charger_Images_Sprite(image)

        self.personnage = self.charger_Images_Sprite.personnage
        self.image = self.personnage[4]

        self.rect = pygame.rect.Rect(position, self.image.get_size())
        self.collision_rect = pygame.rect.Rect(position[0] + 2,
                                               position[1] + 30,
                                               25,
                                               20)

        self.actors_actions = actors_actions.ActorActions(self.image, self.personnage, self)

        self.saveLastPos()

        self.coord_to_move = {"posX":0, "posY":0 ,"side":"none"}
        self.cycle_est_fini = False
        self.compteur_cycle = 0
        self.horloge = 0
        self.a_fini_cycle = 0
        self.compteur = 0

        self.tools = {}

        #spec of perso
        self.dommage = 1
        self.protection = 0
        self.life = 100
        self.speed = 8
        self.accel = 1
        self.isDoing = 'nothing'
        self.arme_equipe = 'epe'

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


    def move(self, x, y,laDirection):
        #print "dans la class Actor la direction recu ===  "+str(laDirection)
        self.coord_to_move["posX"] = x
        self.coord_to_move["posY"] = y
        self.coord_to_move["side"] = laDirection

        self.image =  self.actors_actions.actionMarche(self.coord_to_move,self.coord_to_move["side"])
        self.rect.move_ip(x, y)
        self.collision_rect.move_ip(x, y)
        for tool in self.tools.values():
            tool.definir_position(self.rect.x, self.rect.y)
        #self.saveLastPos()

    def jump(self):

        self.actors_actions.jumpAndAttack("jump")
        self.image = self.actors_actions.image

    def attack(self):
        self.actors_actions.jumpAndAttack("attack")
        self.image = self.actors_actions.image

    def calcul_dommage(self):
        return self.dommage * self.luck()

    def active_arme(self, active):
        self.tools[self.arme_equipe].visible = active

    def is_arme_active(self):
        return self.tools[self.arme_equipe].visible

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

    #fake death juste pour le moment en enleve le sprit de la map
    def isBleeding(self):
        if self.life == 0:
            self.kill()

    # this need the dt and game otherwise bug in tmx
    def update(self, dt, game):
        pass
