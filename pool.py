from OpenGL.GL import *
from OpenGL.GLUT import *
import math
import random

circle_radius = 20

ball_x = 300
ball_y = 100

animation_steps = 10
ball_moved_to_hole = False
animation_counter = 0

cue_angle = 0
cue_length = 500

holes = [(100, 550), (300, 550), (500, 550),
        (100, 50), (300, 50), (500, 50)]

def draw_circle(radius, center_x, center_y):
    glColor3f(1.0, 1.0, 1.0)
    for r in range(radius, 0, -1):
        x = r
        y = 0
        d = 1 - r
        glBegin(GL_POINTS)
        while x >= y:
            glVertex2i(x + center_x, y + center_y)
            glVertex2i(y + center_x, x + center_y)
            glVertex2i(-x + center_x, y + center_y)
            glVertex2i(-y + center_x, x + center_y)
            glVertex2i(-x + center_x, -y + center_y)
            glVertex2i(-y + center_x, -x + center_y)
            glVertex2i(x + center_x, -y + center_y)
            glVertex2i(y + center_x, -x + center_y)
            y += 1
            if d <= 0:
                d += 2 * y + 3
            else:
                x -= 1
                d += 2 * (y - x) + 5
        glEnd()

def init():
    global ball_x, ball_y
    ball_x = random.randint(100 + circle_radius, 500 - circle_radius)
    ball_y = random.randint(100 + circle_radius, 500 - circle_radius)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 600, 0, 600, -1, 1)
    glMatrixMode(GL_MODELVIEW)

def draw_board():
    glColor3f(0.2, 0.6, 0.2)
    glBegin(GL_POINTS)
    for x in range(50, 551):
        glVertex2i(x, 50)
        glVertex2i(x, 550)
    for y in range(50, 551):
        glVertex2i(50, y)
        glVertex2i(550, y)
    glEnd()

    def draw_midpoint_line(x1, y1, x2, y2):
        glColor3f(1.0, 1.0, 1.0)
        dx = x2 - x1
        dy = y2 - y1
        d = 2 * dy - dx
        y = y1
        glBegin(GL_POINTS)
        for x in range(x1, x2 + 1):
            glVertex2i(x, y)
            if d > 0:
                y += 1
                d -= 2 * dx
            d += 2 * dy
        glEnd()

    glBegin(GL_POINTS)
    glEnd()

    draw_midpoint_line(int(ball_x), int(ball_y),
                       int(ball_x + cue_length * math.cos(math.radians(cue_angle))),
                       int(ball_y + cue_length * math.sin(math.radians(cue_angle))))

    glColor3f(0.1, 0.4, 0.1)
    glBegin(GL_POINTS)
    for x in range(51, 550):
        for y in range(51, 550):
            glVertex2i(x, y)
    glEnd()

def draw_holes():
    glColor3f(0.25, 0.25, 0.25)
    hole_size = 30
    for hole in holes:
        x, y = hole
        glBegin(GL_POINTS)
        for i in range(-hole_size // 2, hole_size // 2):
            for j in range(-hole_size // 2, hole_size // 2):
                glVertex2i(x + i, y + j)
        glEnd()


def display():
    global ball_moved_to_hole

    glClear(GL_COLOR_BUFFER_BIT)
    draw_board()
    draw_holes()

    if not ball_moved_to_hole:
        # Draw the stick
        glColor3f(0.8, 0.8, 0.8)
        glBegin(GL_LINES)
        glVertex2f(ball_x, ball_y)
        glVertex2f(
            ball_x + cue_length * math.cos(math.radians(cue_angle)),
            ball_y + cue_length * math.sin(math.radians(cue_angle))
        )
        glEnd()

    glPushMatrix()
    glTranslatef(ball_x, ball_y, 0)
    glColor3f(1.0, 1.0, 1.0)
    draw_circle(circle_radius, 0, 0)
    glPopMatrix()

    glutSwapBuffers()


def keyboard_input(key, x, y):
    global ball_moved_to_hole, step_x, step_y
    if not ball_moved_to_hole:
        if key >= b'1' and key <= b'6':
            hole_number = int(key) - 1
            if 0 <= hole_number < len(holes):
                target_x, target_y = holes[hole_number]
                step_x = (target_x - ball_x) / animation_steps
                step_y = (target_y - ball_y) / animation_steps
                ball_moved_to_hole = True
                glutTimerFunc(5, animate_ball, 0)


def mouse_motion(x, y):
    global cue_angle, cue_length
    diff_x = x - ball_x
    diff_y = ball_y - y  # Invert the y-axis movement
    cue_angle = math.degrees(math.atan2(diff_y, diff_x))
    cue_length = math.sqrt(diff_x ** 2 + diff_y ** 2)
    glutPostRedisplay()

def animate_ball(value):
    global ball_x, ball_y, animation_counter, ball_moved_to_hole
    if animation_counter < animation_steps:
        ball_x += step_x
        ball_y += step_y
        animation_counter += 1
        glutPostRedisplay()
        glutTimerFunc(20, animate_ball, 0)
    else:
        ball_moved_to_hole = True
        animation_counter = 0
    glutPostRedisplay()

def main():
    glutInit()
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"OpenGL 8-Ball Pool Game")
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutDisplayFunc(display)
    glutPassiveMotionFunc(mouse_motion)
    glutKeyboardFunc(keyboard_input)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()



