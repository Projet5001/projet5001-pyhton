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
import time

import pygame
from pygame import Rect

from lib import tmx

from eventManager import EventEnum
from npc import Npc
from monster import Monster


class StoryManager(object):

    def __init__(self, game, layer_manager):
        self.game = game
        self.layer_manager = layer_manager
        self.source = ""
        self.story_file = ""

        self.stories = None
        self.stories_done = []

        self.blocking = False
        self.unblockable = True

        self.speechlayer = None

        self.events = []
        self.blocked_events = []

    def read_story(self, story):
        if not self.stories:
            return

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

    def read_stories(self, source):
        try:
            self.source = "%s.json" % source.split('.')[0]
            self.story_file = open(os.path.join(os.path.dirname(__file__),
                                                self.source),
                                   "r")
            self.stories = json.load(self.story_file)

            if self.source in self.stories_done:
                return

            for story in self.stories['ordre']:
                self.read_story(story)

            self.stories_done.append(self.source)
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

    def trigger_event(self, event_name):
        self.read_story(event_name)

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

    def next_speech(self):
        if not self.speechlayer:
            return

        if self.speechlayer.has_text_left():
            self.speechlayer.next_speech()
        else:
            self.remove_speech()

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
        self.text = []
        self.text.extend(text[2:])
        self.visible_text = []
        self.visible_text[:] = text[0:2]
        self.width = 0.8 * layer_manager.screen_width
        self.height = 100
        self.px = (layer_manager.screen_width - self.width) / 2
        if pos == "top":
            self.py = self.height / 2
        else:
            self.py = layer_manager.screen_height - self.height * 1.5
        self.rect = Rect(self.px,
                         self.py,
                         self.width,
                         self.height)

        self._black = (0, 0, 0)
        self._white = (255, 255, 255)
        self.dot_color = self._white
        self.last_dot_color = self._white
        self.color_counter = 0

    def next_speech(self):
        self.visible_text[:] = self.text[0:2]
        self.text[:] = self.text[2:]

    def has_text_left(self):
        return len(self.text) > 0

    def draw(self, surface):
        if self.color_counter >= 25:
            if self.last_dot_color is self._white:
                self.dot_color = self._black
            else:
                self.dot_color = self._white
            self.color_counter = 0

        # Build dialog box shadow
        for x in range(1, 5, 1):
            surface.fill((0, 0, 0),
                         rect=self.rect,
                         special_flags=0)
            self.rect.x = self.rect.x - 1
            self.rect.y = self.rect.y - 1

        # Build dialog box contour.
        for x in range(1, 3, 1):
            surface.fill((255, 255, 255),
                         rect=self.rect,
                         special_flags=0)
            self.rect.x = self.rect.x - 1
            self.rect.y = self.rect.y - 1

        self.rect.x = self.rect.x + 3
        self.rect.y = self.rect.y + 3
        self.rect.width = self.rect.width - 3
        self.rect.height = self.rect.height - 3

        # black box for text
        surface.fill((0, 0, 0),
                     rect=self.rect,
                     special_flags=0)
        myfont = pygame.font.SysFont("monospace", 20, True)
        line_x = self.px + 20
        line_y = self.py + 20
        for line in self.visible_text:
            label = myfont.render(line, 1, (255, 255, 255))
            surface.blit(label, (line_x, line_y))
            line_y = line_y + myfont.get_linesize()
        pygame.draw.circle(surface,
                           self.dot_color,
                           (int(line_x) + label.get_width() + 6 + 3,
                            int(line_y) - myfont.get_linesize() + 6 + 3),
                           6, 0)
        self.last_dot_color = self.dot_color
        self.color_counter = self.color_counter + 1

        # reset for next call to draw.
        self.rect.x = self.px
        self.rect.y = self.py
        self.rect.width = self.width
        self.rect.height = self.height

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
                self.game.story_manager.display_speech(["GAME OVER"], "bottom")
                self.game.story_manager.set_unblockable(False)
                self.game.perso.kill()
            elif self.story["sprite"]:
                sprite_name = self.story["sprite"]
                sprite = self.game.layer_manager.get_sprite(sprite_name)
                time.sleep(2)
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
                monster = Monster(self.story["name"],
                                  os.path.join(self.game.config.get_sprite_dir(),
                                               self.story["sprite_img"]),
                                  self.story["destination"],
                                  self.game.layer_manager["monster"])
                monster.definir_position(self.story["destination"][0],
                                         self.story["destination"][1])
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
            sprite.saveLastPos()
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

