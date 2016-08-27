import pyglet


_TEXTURE = pyglet.image.load('overseer.png')
_IMAGES = pyglet.image.ImageGrid(_TEXTURE, 8, 16)


def get_tile(x, y):
    """Return the image tile extracted from the spritesheet. The origin (0, 0)
    is the bottom-left corner of the image.
    """
    return _IMAGES[y * 16 + x]
