# -*- coding: utf-8 -*-

"""
MYEVENT = pygame.USEREVENT+2
some_event = pygame.event.Event(MYEVENT, value=10.2)
pygame.event.post(some_event)
"""
import pygame


class EventEnum():
    JUMP = pygame.USEREVENT + 1
    ATTACK = pygame.USEREVENT + 2
    TRANSITION = pygame.USEREVENT + 3
    MOVE = pygame.USEREVENT + 4
    ACTION = pygame.USEREVENT + 5
    STORY = pygame.USEREVENT + 6
    LAST_EVENT = pygame.NUMEVENTS - 1


class EventManager():

    @staticmethod
    def envois_event(e, content):
        event = pygame.event.Event(e, m=content)
        pygame.event.post(event)

    @staticmethod
    def delay_event(e, temps):
        pygame.time.set_timer(e, temps)

    @staticmethod
    def update(game):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True

            if event.type == EventEnum.JUMP:
                game.perso.actors_actions.update_frame_jump(event)

            if event.type == EventEnum.ATTACK:
                game.perso.actors_actions.update_frame_attack(event)

            if event.type == EventEnum.TRANSITION:
                game.effectuer_transition(event.transition)

            if event.type == EventEnum.ACTION:
                pass
            if event.type == EventEnum.STORY:
                game.story_manager.story_event()

            if event.type == EventEnum.MOVE:
                game.perso.get_tool().receive_event(event)

