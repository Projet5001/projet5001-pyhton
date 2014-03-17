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

    @staticmethod
    def envois_event(e, content):
        event = pygame.event.Event(e, e=content)
        pygame.event.post(event)

    @staticmethod
    def update(game):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True

            if event.type == EventManager.event_jump:
                game.perso.actors_actions.update_frame_jump(event)

            if event.type == EventManager.event_attack:
                game.perso.actors_actions.update_frame_attack(event)

            if event.type == EventManager.effectuer_transition:
                game.effectuer_transition(event.transition)

            if event.type == EventManager.action:
                pass
