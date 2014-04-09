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


class EventEnum():
    JUMP = pygame.USEREVENT + 1
    ATTACK = pygame.USEREVENT + 2
    TRANSITION = pygame.USEREVENT + 3
    MOVE = pygame.USEREVENT + 4
    ACTION = pygame.USEREVENT + 5
    STORY = pygame.USEREVENT + 6
    TRIGGER = pygame.USEREVENT + 7
    COLLISION = pygame.USEREVENT + 8
    LAST_EVENT = pygame.NUMEVENTS - 1


class EventManager():

    @staticmethod
    def envois_event(e, *args):
        if len(args) > 1:
            event = pygame.event.Event(e, m=args[0], o=args[1], u=args[2])
            pygame.event.post(event)
        else:
            event = pygame.event.Event(e, m=args[0])
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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game.story_manager.next_speech()

            if event.type == EventEnum.JUMP:
                game.perso.actors_actions.update_frame_jump(event)

            if event.type == EventEnum.ATTACK:
                event_copy = event
                game.perso.actors_actions.update_frame_attack(event)
                game.perso.get_tool().receive_event(event_copy)

            if event.type == EventEnum.TRANSITION:
                game.effectuer_transition(event.transition)

            if event.type == EventEnum.TRIGGER:
                game.do_trigger(event.trigger)

            if event.type == EventEnum.STORY:
                game.story_manager.story_event()

            if event.type == EventEnum.MOVE:
                game.perso.get_tool().receive_event(event)

