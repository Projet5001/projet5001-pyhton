

import pygame


class ActorActions(pygame.sprite.Sprite):
    def __init__(self,image, sprite_sheet, actor):

        self.quatreDirections = {}
        self.reinitValSiDetecter()

        self.image = image
        self.sprite_sheet = sprite_sheet
        self.actor = actor

        self.imageAngleBas = 0
        self.imageAngleHaut = 0
        self.lesImages = 0
        self.derniere_direction_perso = "none"
        self.aEteSauver = 0
        self.intervalImage = {"debut": 0, "fin": 0}

        self.event_jump = pygame.USEREVENT + 1
        self.event_attack = pygame.USEREVENT + 2
        self.nbrFrame = 0


    def mouvement(self,coord_to_move):

        laDirection = coord_to_move["side"]
        self.derniere_direction_perso = coord_to_move["side"]



        #diagonal
        if self.direction_angle_bas():

            self.intervalImage["debut"] = 0
            self.intervalImage["fin"] = 6
            self.sequenceImages(self.intervalImage,"angle_bas")

        #diagonal
        elif self.direction_angle_haut():

            self.intervalImage["debut"] =  7
            self.intervalImage["fin"] =  13
            self.sequenceImages(self.intervalImage,"angle_haut")


        else:
            if laDirection == "down":

                self.intervalImage["debut"] =  0
                self.intervalImage["fin"] =  6
                self.sequenceImages(self.intervalImage,"droit")

            if laDirection == "up":

                self.intervalImage["debut"] =  7
                self.intervalImage["fin"] =  13
                self.sequenceImages(self.intervalImage,"droit")

            if laDirection == "right":

                self.intervalImage["debut"] = 14
                self.intervalImage["fin"] = 20
                self.sequenceImages(self.intervalImage,"droit")

            if laDirection == "left":

                self.intervalImage["debut"] =  21
                self.intervalImage["fin"] =  27
                self.sequenceImages(self.intervalImage,"droit")

        if self.derniere_direction_perso != "none":
            self.quatreDirections[self.derniere_direction_perso] = 1

        self.aEteSauver  += 1
        return self.image



    def action(self, action_du_perso):
        self.actor.is_doing = action_du_perso

        if action_du_perso == "attack":
            self.le_set_image = 28
        else:
            self.le_set_image = 0




        if self.direction_angle_bas():
            self.derniere_direction_perso = "none"
            self.intervalImage["debut"] =  28 +  self.le_set_image
            self.intervalImage["fin"] =  34 +  self.le_set_image
            self.sequenceImages(self.intervalImage,"angle_bas")

        elif  self.direction_angle_haut():
            self.derniere_direction_perso = "none"
            self.intervalImage["debut"] =  35 +  self.le_set_image
            self.intervalImage["fin"] =  41 +  self.le_set_image
            self.sequenceImages(self.intervalImage,"angle_haut")

        else:
            if self.derniere_direction_perso == "down":
                self.intervalImage["debut"] =  28 +  self.le_set_image
                self.intervalImage["fin"] =  34 +  self.le_set_image
                self.sequenceImages(self.intervalImage,"droit")


            if self.derniere_direction_perso == "up":
                self.intervalImage["debut"] =  35 +  self.le_set_image
                self.intervalImage["fin"] =  41 +  self.le_set_image
                self.sequenceImages(self.intervalImage,"droit")


            if self.derniere_direction_perso == "right":
                self.intervalImage["debut"] =  42 +  self.le_set_image
                self.intervalImage["fin"] =  48 +  self.le_set_image
                self.sequenceImages(self.intervalImage,"droit")


            if self.derniere_direction_perso == "left":
                self.intervalImage["debut"] =  49 +  self.le_set_image
                self.intervalImage["fin"] =  55 +  self.le_set_image
                self.sequenceImages(self.intervalImage,"droit")


        self.reinitValSiDetecter()

        if self.derniere_direction_perso != "none":
            self.quatreDirections[self.derniere_direction_perso] = 1

        self.aEteSauver  += 1
        return self.image


    #iterateur d'image
    def sequenceImages(self, intervalle_img,type_image):

        if type_image == "droit":
            if self.lesImages < intervalle_img["debut"] or  self.lesImages > intervalle_img["fin"]:
                print "reset images"
                self.lesImages = intervalle_img["debut"]
                self.actor.is_doing = "nothing"
            self.image = self.sprite_sheet[self.lesImages]
            self.lesImages += 1

        elif type_image == "angle_bas":
            if self.imageAngleBas < intervalle_img["debut"] or self.imageAngleBas > intervalle_img["fin"]:
                 self.imageAngleBas = intervalle_img["debut"]
            self.image = self.sprite_sheet[self.imageAngleBas]
            self.imageAngleBas += 1

        elif type_image == "angle_haut":
            if self.imageAngleHaut < intervalle_img["debut"] or self.imageAngleHaut > intervalle_img["fin"]:
                 self.imageAngleHaut = intervalle_img["debut"]
            self.image = self.sprite_sheet[self.imageAngleHaut]
            self.imageAngleHaut += 1

    def direction_angle_bas(self):
        if  ((self.derniere_direction_perso == "down"  and self.quatreDirections["right"] > 0) or
             ( self.quatreDirections["right"] > 0 and self.derniere_direction_perso == "down"  )):
            return True

        if  ((self.derniere_direction_perso == "down"  and self.quatreDirections["left"] > 0) or
             ( self.quatreDirections["left"] > 0 and self.derniere_direction_perso == "down"  )):
            return False


    def direction_angle_haut(self):
        if  ((self.derniere_direction_perso == "up"  and self.quatreDirections["right"] > 0) or
             ( self.quatreDirections["right"] > 0 and self.derniere_direction_perso == "up"  )):
            return True

        if  ((self.derniere_direction_perso == "up"  and self.quatreDirections["left"] > 0) or
             ( self.quatreDirections["left"] > 0 and self.derniere_direction_perso == "up"  )):
            return False

    def reinitValSiDetecter(self):
        self.quatreDirections["down"] = 0
        self.quatreDirections["up"] = 0
        self.quatreDirections["right"] = 0
        self.quatreDirections["left"] = 0

    def update_frame_jump(self,event):

        if event.type == self.event_jump:
            self.actor.jump()
            self.nbrFrame += 1

            #reset frame
            if self.nbrFrame >= 6:
                pygame.time.set_timer(self.event_jump, 0)#1 second is 1000 milliseconds
                self.nbrFrame = 0
                self.actor.is_doing = "nothing"


    def update_frame_attack(self,event):

        if event.type == self.event_attack:
            self.actor.attack()
            self.nbrFrame += 1

            #reset frame
            print self.nbrFrame
            if self.nbrFrame >= 6:
                pygame.time.set_timer(self.event_attack, 0)#1 second is 1000 milliseconds
                self.nbrFrame = 0
                self.actor.is_doing = "nothing"


    def update(self,event):
        pass

