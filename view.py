from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import numpy


class View:
    window = 0

    # TODO: Multiple camera angles (top down etc.)
    # TODO: image of heightmap

    def setNpGrid(self):
        pass

    def InitGL(self, Width, Height):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_FLAT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90.0, float(Width) / float(Height), 0.3, 10000.0)
        glRotatef(45.0, 1.0, 0.0, 0.0)
        glRotatef(150, 0.0, 1.0, 0.0)
        glRotatef(0, 0.0, 0.0, 1.0)
        glTranslatef(0.05, -0.2, 0.05)
        glMatrixMode(GL_MODELVIEW)

    def DrawGLScene1(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        gridSize = 250

        glBegin(GL_QUADS)

        for x in range(gridSize):
            for y in range(1):
                for z in range(gridSize):
                    self.drawCube(x, y, z, 0.75, 5)

        glEnd()

        glutSwapBuffers()

    def DrawGLScene2(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        gridSize = 10

        glBegin(GL_QUADS)

        for x in range(gridSize):
            for z in range(gridSize):
                for y in range(min(x, z)):
                    self.drawCube(x, y, z, 0.5, 1)

        glEnd()

        glutSwapBuffers()

    def DrawGLScene3(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        gridSize = 250

        glBegin(GL_QUADS)

        for x in range(gridSize):
            for y in range(1):
                for z in range(gridSize):
                    self.drawCube(x / 100.0, y / 100.0, z / 100.0, 0.01, 0.05 * (math.sin((x + z) / 5.0) + 1))

        glEnd()

        glutSwapBuffers()

    def drawCube(self, x, y, z, size, height):

        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(x + size, y + height, z)
        glVertex3f(x, y + height, z)
        glVertex3f(x, y + height, z + size)
        glVertex3f(x + size, y + height, z + size)

        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(x + size, y, z)
        glVertex3f(x, y, z)
        glVertex3f(x, y + height, z)
        glVertex3f(x + size, y + height, z)

        glColor3f(1.0, 0.0, 0.5)
        glVertex3f(x, y + height, z + size)
        glVertex3f(x, y + height, z)
        glVertex3f(x, y, z)
        glVertex3f(x, y, z + size)

    def test(self, key, x, y):
        print(key)

    def main(self):
        global window

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(1920, 1080)
        glutInitWindowPosition(0, 0)

        window = glutCreateWindow('OpenGL Python Cube')

        glutDisplayFunc(self.DrawGLScene3)
        glutIdleFunc(self.DrawGLScene3)
        self.InitGL(1920, 1080)
        glutKeyboardFunc(self.test)
        glutMainLoop()

view_obj = View()
view_obj.main()