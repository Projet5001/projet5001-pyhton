
import os
import json

import pygame
from pygame import Rect

from lib import tmx
from eventManager import EventEnum


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

    def read_story(self, source):
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
                self.events.append(StoryEvent(self.stories[story], self.game,
                                              self.stories[story]['delay']))

    def set_unblockable(self, unblockable):
        self.unblockable = unblockable

    def story_event(self):
        print "story event!!"
        pygame.time.set_timer(EventEnum.STORY, 0)
        event = self.events.pop(0)
        event.handle_event()
        if self.events:
            pygame.time.set_timer(EventEnum.STORY, self.events[0].delay)

    def display_speech(self, text, pos):
        self.speechlayer = SpeechLayer(self.layer_manager, text, pos)
        self.layer_manager.add_layer('speech', self.speechlayer)
        self.blocking = True

    def remove_speech(self):
        if self.unblockable:
            if 'speech' in self.layer_manager:
                self.layer_manager.remove('speech')
            self.blocking = False


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

    def __init__(self, story, game, delay):
        self.story = story
        self.game = game
        self.delay = delay

    def handle_event(self):
        if self.story["action"] == "death":
            if self.story["sprite"] == "player":
                print "GAME OVER>"
                self.game.story_manager.display_speech("GAME OVER", "bottom")
                self.game.story_manager.set_unblockable(False)
                self.game.perso.kill()

