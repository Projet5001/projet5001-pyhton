import actors


class Monster(actors.Actor):
    def __init__(self, image, position, *groups):
        super(Monster, self).__init__(image, position, *groups)

    def update(self, dt, game):
        print 'rect-monstre', self.rect.x, self.rect.y