from pyglet import gl


class Camera:
    x = 0.0
    y = 0.0

    def pre_draw(self):
        gl.glPushMatrix()
        gl.glTranslatef(int(self.x), int(self.y), 0)

    def post_draw(self):
        gl.glPopMatrix()

    def untransform_mouse(self, x, y):
        return (x-self.x)//16, (y-self.y)//16
