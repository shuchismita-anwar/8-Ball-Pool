from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL import glRotatef
import math
import random
import tkinter as tk
from tkinter import messagebox



circle_radius = 10
animation_steps = 10
ball_moved_to_hole = False
animation_counter = 0
start_game = False
cue_angle = 0
cue_length = 0
ball_rotation_angle = 0.0


holes = [(100, 550), (300, 550), (500, 550), (100, 50), (300, 50), (500, 50)]


def draw_circle(radius, center_x, center_y):
    glColor3f(1.0, 1.0, 1.0)
    for r in range(radius, 0, -1):  
        x = 0
        y = r
        d = 1 - r
        glBegin(GL_POINTS)
        while x <= y:
            glVertex2i(x + center_x, y + center_y)
            glVertex2i(y + center_x, x + center_y)
            glVertex2i(x + center_x, -y + center_y)
            glVertex2i(y + center_x, -x + center_y)
            glVertex2i(-x + center_x, -y + center_y)
            glVertex2i(-y + center_x, -x + center_y)
            glVertex2i(-x + center_x, y + center_y)
            glVertex2i(-y + center_x, x + center_y)
            x += 1
            if d <= 0:
                d += 2 * x + 3
            else:
                y -= 1
                d += 2 * (x - y) + 5
        glEnd()


def init():
    global ball_x, ball_y
    ball_x = random.randint(50 + circle_radius, 550 - circle_radius)
    ball_y = random.randint(50 + circle_radius, 550 - circle_radius)
    print(ball_x, ball_y)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 600, 0, 600, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPointSize(5)


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
    glColor3f(0.1, 0.4, 0.1)
    glBegin(GL_POINTS)
    for x in range(51, 550):
        for y in range(51, 550):
            glVertex2i(x, y)
    glEnd()

    glColor3f(0.35, 0.15, 0.0) 
    draw_midpoint_line(50, 50, 550, 50)
    draw_midpoint_line(50, 50, 50, 550)
    draw_midpoint_line(50, 550, 550, 550)
    draw_midpoint_line(550, 50, 550, 550)


def draw_midpoint_line(x1, y1, x2, y2):
        
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    if dx == 0:  
        glBegin(GL_POINTS)
        for y in range(y1, y2 + 1):
            glVertex2i(x1, y)
        glEnd()
        return

    slope = dy / dx

    if slope <= 1:
        y = y1
        if y2 > y1:
            y_step = 1
        else:
            y_step = -1

        d = 2 * dy - dx

        glBegin(GL_POINTS)
        for x in range(x1, x2 + 1):
            glVertex2i(x, y)
            if d >= 0:
                y += y_step
                d -= 2 * dx
            d += 2 * dy
        glEnd()

    else:
        x = x1
        if y2 > y1:
            x_step = 1
        else:
            x_step = -1

        d = 2 * dx - dy

        glBegin(GL_POINTS)
        for y in range(y1, y2 + 1):
            glVertex2i(x, y)
            if d >= 0:
                x += x_step
                d -= 2 * dy
            d += 2 * dx
        glEnd()


def draw_circle2(radius, center_x, center_y):
    glColor3f(0.25, 0.25, 0.25)
    for r in range(radius, 0, -1):  
        x = 0
        y = r
        d = 1 - r
        glBegin(GL_POINTS)
        while x <= y:
            glVertex2i(x + center_x, y + center_y)
            glVertex2i(y + center_x, x + center_y)
            glVertex2i(x + center_x, -y + center_y)
            glVertex2i(y + center_x, -x + center_y)
            glVertex2i(-x + center_x, -y + center_y)
            glVertex2i(-y + center_x, -x + center_y)
            glVertex2i(-x + center_x, y + center_y)
            glVertex2i(-y + center_x, x + center_y)    
            x += 1
            if d <= 0:
                d += 2 * x + 3
            else:
                y -= 1
                d += 2 * (x - y) + 5
        glEnd()


def draw_holes():
    glColor3f(0.25, 0.25, 0.25)
    hole_radius = 20
    for hole in holes:
        x, y = hole
        draw_circle2(hole_radius, x, y)


def display():
    global ball_moved_to_hole, ball_rotation_angle
    glClear(GL_COLOR_BUFFER_BIT)
    draw_board()
    draw_holes()


    if not ball_moved_to_hole:     
        glColor3f(0.8, 0.8, 0.8)
        glBegin(GL_LINES)
        glVertex2f(ball_x, ball_y)
        glVertex2f(ball_x + cue_length * math.cos(math.radians(cue_angle)),
                    ball_y + cue_length * math.sin(math.radians(cue_angle)))
        
        glEnd()
    # print(cue_angle)

    glPushMatrix()
    glTranslatef(ball_x, ball_y, 0)
    glRotatef(ball_rotation_angle, 0, 0, 1)
    glColor3f(1.0, 1.0, 1.0)
    draw_circle(circle_radius, 0, 0)
    glPopMatrix()

    characters = [('8', (0.0, 0.0, 0.0), 0.0)]

    for char, color, pos in characters:
        glColor3f(*color)  
        text_x = ball_x + pos - 3
        text_y = ball_y - circle_radius +3  
        glRasterPos2f(text_x, text_y)
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

    glutSwapBuffers()


def keyboard_input(key, x, y):
    global ball_moved_to_hole, step_x, step_y
    if not ball_moved_to_hole:
        if key >= b'1' and key <= b'6':
            hole_number = int(key) - 1
            if 0 <= hole_number < len(holes):
                target_x, target_y = holes[hole_number]
                # print(target_x, target_y)
                step_x = (target_x - ball_x) / animation_steps
                step_y = (target_y - ball_y) / animation_steps
                ball_moved_to_hole = True
                glutTimerFunc(16, animate_ball, 0)


def mouse_motion(x, y):
    global cue_angle, cue_length
    diff_x = x - ball_x
    diff_y = ball_y - y  
    cue_angle = math.degrees(math.atan2(diff_y, diff_x))
    cue_length = math.sqrt(diff_x ** 2 + diff_y ** 2)
    # print("cue",cue_length)
    glutPostRedisplay()

def animate_ball(value):
    global ball_x, ball_y, animation_counter, ball_moved_to_hole, ball_rotation_angle
    if animation_counter < animation_steps:
        ball_x += step_x
        ball_y += step_y
        ball_rotation_angle += 5.0
        animation_counter += 1
        glutPostRedisplay()
        glutTimerFunc(16, animate_ball, 0)
    else:
        ball_moved_to_hole = True
        animation_counter = 0
    glutPostRedisplay()


def start_game_command(root):
    global start_game
    start_game = True
    root.destroy()


def exit_game_command(root):
    root.destroy()


def main():
    global start_game
    root = tk.Tk()
    root.geometry("300x200")
    root.title("8-Ball Pool Game")
    label = tk.Label(root, text="Do you want to play 8-Ball Pool?")
    label.pack()
    yes_button = tk.Button(root, text="Yes! 😃", command=lambda: start_game_command(root), height= 2, width=10)
    yes_button.pack(side=tk.LEFT)
    no_button = tk.Button(root, text="No 🙁", command=lambda: exit_game_command(root), height= 2, width=10)
    no_button.pack(side=tk.RIGHT)
    root.mainloop()
    if start_game:
        start_opengl_game()


def start_opengl_game():
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
