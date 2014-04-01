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

import os
import json

import pygame
from pygame import Rect

from lib import tmx

from eventManager import EventEnum
from npc import Npc


class StoryManager(object):

    def __init__(self, game, layer_manager):
        self.game = game
        self.layer_manager = layer_manager
        self.source = ""
        self.story_file = ""

        self.stories = None

        self.blocking = False
        self.unblockable = True

        self.speechlayer = None

        self.events = []
        self.blocked_events = []

    def read_story(self, source):
        try:
            self.source = "%s.json" % source.split('.')[0]
            self.story_file = open(os.path.join(os.path.dirname(__file__),
                                                self.source),
                                   "r")
            self.stories = json.load(self.story_file)

            for story in self.stories['ordre']:
                if self.stories[story]['type'] == "speech":
                    self.display_speech(self.stories[story]['text'],
                                        self.stories[story]['position'])
                elif self.stories[story]['type'] == "timer":
                    if not self.events:
                        pygame.time.set_timer(EventEnum.STORY,
                                              self.stories[story]['delay'])
                    delay = self.stories[story]['delay']
                    self.events.append(StoryEvent(story,
                                                  self.stories[story],
                                                  self.game,
                                                  delay))
        except IOError:
            print "attention: impossible de charger le fichier d'histoire"
            pass
        except KeyError as e:
            # On peut ici avoir passé à travers beaucoup de création d'objets
            # il vaut mieux tout vider.

            print "attention: erreur de syntaxe dans le fichier d'histoire"
            print e

            self.stories.clear()

            # vider les events...
            self.events[:] = []

            # désactiver les timers déjà créés
            pygame.time.set_timer(EventEnum.STORY, 0)
            self.unblockable = True
            self.remove_speech()
            pass

    def set_unblockable(self, unblockable):
        self.unblockable = unblockable

    def story_event(self):
        pygame.time.set_timer(EventEnum.STORY, 0)
        if self.events:
            event = self.events.pop(0)
            #print "story event: %s" % event
            event.handle_event()
            #print "events left: %s" % self.events
            if self.events:
                pygame.time.set_timer(EventEnum.STORY, self.events[0].delay)

    def display_speech(self, text, pos):
        self.speechlayer = SpeechLayer(self.layer_manager, text, pos)
        self.layer_manager.add_layer('speech', self.speechlayer)
        self.blocking = True

        # on bloque tous les events en attendant.
        pygame.time.set_timer(EventEnum.STORY, 0)
        self.blocked_events[:] = self.events[:]
        self.events[:] = []

    def remove_speech(self):
        if not self.speechlayer:
            return

        if self.unblockable:
            if 'speech' in self.layer_manager:
                self.layer_manager.remove('speech')
            self.blocking = False
        self.speechlayer = None

        # remettre les events bloques en place
        self.events[:] = self.blocked_events[:]
        self.blocked_events[:] = []
        if self.events:
            pygame.time.set_timer(EventEnum.STORY, self.events[0].delay)


class SpeechLayer(tmx.Layer):

    def __init__(self, layer_manager, text, pos="bottom"):
        super(SpeechLayer, self).__init__('speech', True, layer_manager)
        self.text = text
        self.width = 300
        self.height = 100
        if pos == "top":
            self.px = self.width / 2
            self.py = self.height / 2
        else:
            self.px = (layer_manager.screen_width - self.width) / 2
            self.py = layer_manager.screen_height - self.height * 1.5
        self.rect = Rect(self.px,
                         self.py,
                         self.width,
                         self.height)

    def draw(self, surface):
        surface.fill((0, 0, 0),
                     rect=self.rect,
                     special_flags=0)
        myfont = pygame.font.SysFont("monospace", 15, True)
        label = myfont.render(self.text, 1, (255, 255, 255))
        surface.blit(label, (self.px + 20,
                             self.py + 20))

class StoryEvent(object):

    def __init__(self, story_name, story, game, delay):
        self.name = story_name
        self.story = story
        self.game = game
        self.delay = delay

    def __repr__(self):
        return self.name

    def handle_event(self):
        if self.story["action"] == "death":
            if self.story["sprite"] == "player":
                self.game.story_manager.display_speech("GAME OVER", "bottom")
                self.game.story_manager.set_unblockable(False)
                self.game.perso.kill()
            elif self.story["sprite"]:
                sprite_name = self.story["sprite"]
                sprite = self.game.layer_manager.get_sprite(sprite_name)
                sprite.kill()
        elif self.story["action"] == "spawn":
            if self.story["spawn_type"] == "npc":
                npc = Npc(self.story["name"],
                          os.path.join(self.game.config.get_sprite_dir(),
                                       self.story["sprite_img"]),
                          self.story["destination"],
                          self.game.layer_manager["npcs"])
                npc.definir_position(self.story["destination"][0],
                                     self.story["destination"][1])
            else:
                sprite = self.game.layer_manager.get_sprite(self.story["sprite"])
                sprite.kill()
                sprite.add(self.game.layer_manager['monster'])
        elif self.story["action"] == "speech":
            self.game.story_manager.display_speech(self.story['text'],
                                                   self.story['position'])
        elif self.story["action"] == "move":
            self.game.story_manager.blocking = True
            self.game.story_manager.set_unblockable(False)
            sprite = self.game.layer_manager.get_sprite(self.story["sprite"])
            dest = self.story["destination"]
            print dest
            print sprite.collision_rect
            if sprite.collision_rect.x != dest[0]:
                if sprite.collision_rect.x < dest[0]:
                    sprite.move(sprite.speed * sprite.accel, 0, "right")
                else:
                    sprite.move(-(sprite.speed * sprite.accel), 0, "left")
                self.game.story_manager.events.insert(0, self)
                return
            if sprite.collision_rect.y != dest[1]:
                if sprite.collision_rect.y < dest[1]:
                    sprite.move(0, sprite.speed * sprite.accel, "down")
                else:
                    sprite.move(0, -(sprite.speed * sprite.accel), "up")
                self.game.story_manager.events.insert(0, self)
                return

            if self.game.story_manager.blocking:
                self.game.story_manager.set_unblockable(True)
                self.game.story_manager.blocking = False

