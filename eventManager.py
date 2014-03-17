# -*- coding: utf-8 -*-

"""
MYEVENT = pygame.USEREVENT+2
some_event = pygame.event.Event(MYEVENT, value=10.2)
pygame.event.post(some_event)
"""
import pygame


class EventManager():
    #de 1 à 255
    event_jump = pygame.USEREVENT + 1
    event_attack = pygame.USEREVENT + 2
    effectuer_transition = pygame.USEREVENT+3
    move = pygame.USEREVENT+4
    action = pygame.USEREVENT+4

    def __init__(self):
        self.data = None

    def update(self, game):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True

            if event.type == self.event_jump:
                game.perso.actors_actions.update_frame_jump(event)

            if event.type == self.event_attack:
                game.perso.actors_actions.update_frame_attack(event)

            if event.type == self.effectuer_transition:
                game.effectuer_transition(event.transition)

            if event.type == self.action:
                pass
