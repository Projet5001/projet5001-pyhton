# -*- coding: utf-8 -*-
import pygame
import tmx

class UserInput:
    def __init__(self, perso):
        self.perso = perso

    def update(self):
        # -------- scroll the big map ----------
        pressedkeys = pygame.key.get_pressed()
        if pressedkeys[pygame.K_LEFT]:
             self.perso.position['x'] -= 1
        if pressedkeys[pygame.K_RIGHT]:
             self.perso.position['x'] += 1
        if pressedkeys[pygame.K_UP]:
             self.perso.position['y'] -= 1
        if pressedkeys[pygame.K_DOWN]:
             self.perso.position['y'] += 1

class Perso(pygame.sprite.Sprite):
    def __init__(self, screen, image):
        super(Perso, self).__init__()
        self.screen = screen
        self.image = pygame.image.load(image)
        self.position = {'x': 0, 'y': 0}

    def update(self):
        self.screen.blit(self.image, (self.position['x'], self.position['y']))


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    tilemap = tmx.load('example.tmx', screen.get_size())
    tilemap.set_focus(0, 0)
    clock = pygame.time.Clock()
    dt = clock.tick(30)
    perso = Perso(screen, "perso.png")
    userInput = UserInput(perso)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        tilemap.update(dt)
        black = (0,0,0)
        screen.fill(black)
        # Draw all layers of the tilemap to the screen.
        tilemap.draw(screen)
        userInput.update()
        perso.update()
        # Refresh the display window.
        pygame.display.flip()


if __name__ == '__main__':
    main()