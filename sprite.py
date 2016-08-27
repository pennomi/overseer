import pyglet


class BetterSprite(pyglet.sprite.Sprite):

    def __init__(self, image, x, y, batch):
        super().__init__(image, x * 16, y * 16, batch=batch)

    @property
    def location(self):
        return self.x // 16, self.y // 16