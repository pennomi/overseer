from pyglet import gl


class Camera:
    zoom = 1.0
    x = 0.0
    y = 0.0

    def pre_draw(self):
        gl.glPushMatrix()
        gl.glTranslatef(self.x, self.y, 0)
        gl.glScalef(self.zoom, self.zoom, self.zoom)

    def post_draw(self):
        gl.glPopMatrix()

    def untransform(self, x, y):
        return (x-self.x)//16, (y-self.y)//16