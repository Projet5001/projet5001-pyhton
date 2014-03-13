

import pygame


class ActorActions(pygame.sprite.Sprite):
    def __init__(self,image, sprite_sheet, actor):

        self.quatreDirections = {}
        self.reinitValSiDetecter()

        self.image = image
        self.sprite_sheet = sprite_sheet
        self.actor = actor
        self.lesImages = 0
        self.imageAngleBas = 0
        self.imageAngleHaut = 0
        self.derniere_direction_perso = "none"
        self.aEteSauver = 0
        self.last_side_before_action = ["none", "none"] # a nest pas utliser pour linstant

        self.intervalImage = {"debut": 0, "fin": 0}
        self.event_jump = pygame.USEREVENT + 1
        self.event_attack = pygame.USEREVENT + 2
        self.nbrFrame = 0
        self.desactiv_commande = 0

    def actionMarche(self,coord_to_move,laDirection):
       # print "ENTER____walkImage_____________________laDirection___" +str(laDirection)
        self.derniere_direction_perso = coord_to_move["side"]
        self.direction_angle_bas()
        self.direction_angle_haut()

        if self.vaEnAngleBas != 0: #vaEnAngleBas = -1 vers la gauche ou vaEnAngleBas = 1 vers la droite
            #print "IM going vaEnAngleBas >>>>>>>>>>vaEnAngleBas"
            if self.vaEnAngleBas == -1:
                self.last_side_before_action[0] = "left"
            else:
                self.last_side_before_action[0] = "right"
            self.last_side_before_action[1] = "down"
            self.intervalImage["debut"] = 0
            self.intervalImage["fin"] = 6
            self.sequenceImages(self.intervalImage,"none","angle_bas")

        elif self.vaEnAngleHaut != 0:
            #print "IM going vaEnAngleHaut >>>>>>>>>>vaEnAngleHaut"
            if self.vaEnAngleHaut == -1:
                self.last_side_before_action[0] = "left"
            else:
                self.last_side_before_action[0] = "right"
            self.last_side_before_action[1] = "up"
            self.intervalImage["debut"] =  7
            self.intervalImage["fin"] =  13
            self.sequenceImages(self.intervalImage,"none","angle_haut")


        else:
            if laDirection == "down":
               # print "IM going down >>>>>>>>>>down"
                self.last_side_before_action[0] = "none"
                self.last_side_before_action[1] = "down"
                self.intervalImage["debut"] =  0
                self.intervalImage["fin"] =  6
                self.sequenceImages(self.intervalImage,"up","droit")

            if laDirection == "up":
                #print "IM going up >>>>>>>>>>up"
                self.last_side_before_action[0] = "none"
                self.last_side_before_action[1] = "up"
                self.intervalImage["debut"] =  7
                self.intervalImage["fin"] =  13
                self.sequenceImages(self.intervalImage,"up","droit")

            if laDirection == "right":
                #print "IM going right >>>>>>>>>>right"
                self.last_side_before_action[0] = "none"
                self.last_side_before_action[1] = "right"
                self.intervalImage["debut"] = 14
                self.intervalImage["fin"] = 20
                self.sequenceImages(self.intervalImage,"right","droit")

            if laDirection == "left":
                #print "IM going left >>>>>>>>>>left"
                #print "     walk left ***"
                self.last_side_before_action[0] = "none"
                self.last_side_before_action[1] = "left"
                self.intervalImage["debut"] =  21
                self.intervalImage["fin"] =  27
                self.sequenceImages(self.intervalImage,"left","droit")

        return self.image



    def jumpAndAttack(self, action_du_perso):
        self.le_set_image = 0 # egal sequence d images de jump
        if action_du_perso == "attack":
            self.le_set_image = 28

        self.direction_angle_bas()
        self.direction_angle_haut()

        if self.vaEnAngleBas == 1:
            self.intervalImage["debut"] =  28 +  self.le_set_image
            self.intervalImage["fin"] =  34 +  self.le_set_image
            self.sequenceImages(self.intervalImage,"none","angle_bas")

        elif  self.vaEnAngleHaut == 1:
            self.intervalImage["debut"] =  35 +  self.le_set_image
            self.intervalImage["fin"] =  41 +  self.le_set_image
            self.sequenceImages(self.intervalImage,"none","angle_haut")

        else:
            if self.derniere_direction_perso == "down":
                self.intervalImage["debut"] =  28 +  self.le_set_image
                self.intervalImage["fin"] =  34 +  self.le_set_image
                self.sequenceImages(self.intervalImage,"down","droit")


            if self.derniere_direction_perso == "up":
                self.intervalImage["debut"] =  35 +  self.le_set_image
                self.intervalImage["fin"] =  41 +  self.le_set_image
                self.sequenceImages(self.intervalImage,"up","droit")


            if self.derniere_direction_perso == "right":
                self.intervalImage["debut"] =  42 +  self.le_set_image
                self.intervalImage["fin"] =  48 +  self.le_set_image
                self.sequenceImages(self.intervalImage,"right","droit")


            if self.derniere_direction_perso == "left":
                self.intervalImage["debut"] =  49 +  self.le_set_image
                self.intervalImage["fin"] =  55 +  self.le_set_image
                self.sequenceImages(self.intervalImage,"left","droit")

        return self.image


    #iterateur d'image
    def sequenceImages(self, intervalle_img,une_direction,type_image):

        if type_image == "droit":
            print self.lesImages
            #print " inside sequenceImages droit et self.lesImages === "+str(self.lesImages)
            if intervalle_img["debut"] > self.lesImages or  self.lesImages > intervalle_img["fin"]:
                 print "reset images"
                 self.lesImages = intervalle_img["debut"]

            self.image = self.sprite_sheet[self.lesImages]
            self.lesImages += 1

        elif type_image == "angle_bas":
            #print " inside angle_bas  self.imageAngleBas === "+str(self.imageAngleBas)
            if self.imageAngleBas < intervalle_img["debut"] or self.imageAngleBas > intervalle_img["fin"]:
                 self.imageAngleBas = intervalle_img["debut"]
            self.image = self.sprite_sheet[self.imageAngleBas]
            self.imageAngleBas += 1

        elif type_image == "angle_haut":
            #print " inside angle_haut  self.imageAngleHaut === "+str(self.imageAngleHaut)
            if self.imageAngleHaut < intervalle_img["debut"] or self.imageAngleHaut > intervalle_img["fin"]:
                 self.imageAngleHaut = intervalle_img["debut"]
            self.image = self.sprite_sheet[self.imageAngleHaut]
            self.imageAngleHaut += 1

        self.reinitValSiDetecter()

        if une_direction != "none":
            self.quatreDirections[une_direction] = 1

        self.aEteSauver  += 1



    def direction_angle_bas(self):
        self.vaEnAngleBas = 0
        if  self.aEteSauver > 0 and  \
             ((self.derniere_direction_perso == "down"  and self.quatreDirections["right"] > 0) or
             ( self.quatreDirections["right"] > 0 and self.derniere_direction_perso == "down"  )):
            self.vaEnAngleBas = 1

        if  self.aEteSauver > 0 and  \
             ((self.derniere_direction_perso == "down"  and self.quatreDirections["left"] > 0) or
             ( self.quatreDirections["left"] > 0 and self.derniere_direction_perso == "down"  )):
            self.vaEnAngleBas = -1


    def direction_angle_haut(self):

        self.vaEnAngleHaut = 0
        if  self.aEteSauver > 0 and  \
             ((self.derniere_direction_perso == "up"  and self.quatreDirections["right"] > 0) or
             ( self.quatreDirections["right"] > 0 and self.derniere_direction_perso == "up"  )):
            self.vaEnAngleHaut = 1

        if  self.aEteSauver > 0 and  \
             ((self.derniere_direction_perso == "up"  and self.quatreDirections["left"] > 0) or
             ( self.quatreDirections["left"] > 0 and self.derniere_direction_perso == "up"  )):
            self.vaEnAngleHaut = -1

    def reinitValSiDetecter(self):
        self.quatreDirections["down"] = 0
        self.quatreDirections["up"] = 0
        self.quatreDirections["right"] = 0
        self.quatreDirections["left"] = 0

    def update_frame_jump(self,event):

        if event.type == self.event_jump:
            #print "                    PERSO JUMP"

            self.actor.jump()
            self.nbrFrame += 1

            if self.nbrFrame == 7:
                pygame.time.set_timer(self.event_jump, 0)#1 second is 1000 milliseconds
                #self.desactiv_commande = 0
                self.nbrFrame = 0


    def update_frame_attack(self,event):

        if event.type == self.event_attack:
            #print "                     PERSO ATTACK"
            self.actor.attack()
            self.nbrFrame += 1


            if self.nbrFrame == 7:
                pygame.time.set_timer(self.event_attack, 0)#1 second is 1000 milliseconds
                #self.desactiv_commande =0
                self.nbrFrame = 0


    def update(self,event):
        pass

