# My original own game "Pong extremo"
#     Copyright (C) <2022>  <José Manuel Naveiro Gómez>

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Defining an initial value
import pygame
from random import randint
import os
from math import sqrt

pygame.font.init()

WIDTH, HEIGHT = 1200,700
WIND = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Xtremo!")

#COLORES
WHIC = (255,255,255)
BLAC = (  0,  0,  0)
GREC = (100,100,100)
REDC = (255,  0,  0)
BLUC = (  0,  0,255)
YELC = (255, 255 ,0)

#VELOCIDADES Y FPS
FPS = 120
JUGA_VEL = 10
CIRC_VEL = 4
MAXI_VEL = 7

#ANCHOS Y ALTOS
ANCOLU, ALCOLU = 4,HEIGHT//7
ANCIRC, ALCIRC = 25,25
ANJUGA, ALJUGA = 50,50
ANPORT, ALPORT = 8,HEIGHT//7+4

#POSICIONES COLUMNAS
POSX1,POSY1 = 60, (HEIGHT//7)
POSX2,POSY2 = WIDTH - 60, (HEIGHT//7)
POSX3,POSY3 = 100, 3*(HEIGHT//7)
POSX4,POSY4 = WIDTH - 100, 3*(HEIGHT//7)
POSX5,POSY5 = 60, 5*(HEIGHT//7)
POSX6,POSY6 = WIDTH - 60, 5*(HEIGHT//7)

#EVENTOS DE GOLPEO DE COLUMNAS
COL1_HIT = pygame.USEREVENT + 1
COL2_HIT = pygame.USEREVENT + 2
COL3_HIT = pygame.USEREVENT + 3
COL4_HIT = pygame.USEREVENT + 4
COL5_HIT = pygame.USEREVENT + 5
COL6_HIT = pygame.USEREVENT + 6

#FUENTES PARA DISTINTOS CASOS
PUNTOS_FONT = pygame.font.SysFont('comicsans',20)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

#CARGA DE IMAGENES
# blue_spaceship_image = pygame.image.load(
#     os.path.join('Assets','spaceship_blue.png'))
# blue_spaceship = pygame.transform.rotate(
#     pygame.transform.scale(
#         blue_spaceship_image,(anchonave,altonave)),90)
#SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))

#MOVIMIENTO DE LOS LIBEROS
def blue_handle_movement(keys_pressed,blue):
    if keys_pressed[pygame.K_a] and (blue.x - JUGA_VEL) > 0: #LEFT
        blue.x -= JUGA_VEL
    if keys_pressed[pygame.K_d] and (blue.x + JUGA_VEL + blue.width) < WIDTH : #RIGHT
        blue.x += JUGA_VEL
    if keys_pressed[pygame.K_w] and (blue.y - JUGA_VEL) > 0: #UP
        blue.y -= JUGA_VEL
    if keys_pressed[pygame.K_s] and (blue.y + JUGA_VEL + blue.height) < HEIGHT: #DOWN
        blue.y += JUGA_VEL

def blue_barrier_control(keys_pressed,bluecol):
    if keys_pressed[pygame.K_1]: #COL1
        bluecol.x = POSX1-2
        bluecol.y = POSY1-2
    if keys_pressed[pygame.K_2]: #COL2
        bluecol.x = POSX3-2
        bluecol.y = POSY3-2
    if keys_pressed[pygame.K_3]: #COL3
        bluecol.x = POSX5-2
        bluecol.y = POSY5-2

def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT]  and (red.x - JUGA_VEL) > 0: #LEFT
        red.x -= JUGA_VEL
    if keys_pressed[pygame.K_RIGHT] and (red.x + JUGA_VEL + red.width) < WIDTH: #RIGHT
        red.x += JUGA_VEL
    if keys_pressed[pygame.K_UP]    and (red.y - JUGA_VEL) > 0: #UP
        red.y -= JUGA_VEL
    if keys_pressed[pygame.K_DOWN]  and (red.y + JUGA_VEL + red.height) < HEIGHT: #DOWN
        red.y += JUGA_VEL

def red_barrier_control(keys_pressed,redcol):
    if keys_pressed[pygame.K_KP1]: #COL1
        redcol.x = POSX2-2
        redcol.y = POSY2-2
    if keys_pressed[pygame.K_KP2]: #COL2
        redcol.x = POSX4-2
        redcol.y = POSY4-2
    if keys_pressed[pygame.K_KP3]: #COL3
        redcol.x = POSX6-2
        redcol.y = POSY6-2

#CATCHER
def catcher(ball, blue, red, blu_ball,red_ball,ballvelx,ballvely,ball_with):
    if red.colliderect(ball) and not red_ball:
        #Codigo redirige bola
        red_ball=True
        ball_with = "red"
    elif red.colliderect(ball):
        #Codigo redirige bola
        ballvelx *=-1
        ballvely *=-1
    elif blue.colliderect(ball) and not blu_ball:
        #Codigo redirige bola
        blu_ball=True
        ball_with = "blue"
    elif blue.colliderect(ball):
        #Codigo redirige bola
        ballvelx *=-1
        ballvely *=-1

    return ball,blu_ball,red_ball,ballvelx,ballvely,ball_with

#GESTION DE LAS BOLAS
def handle_ball(ball, ballvelx, ballvely, blue, red, blu_ball, red_ball, bluecol,
redcol, colu1, colu2, colu3, colu4, colu5, colu6, ball_with):
    if ball_with == "":
        ball.x += ballvelx
        ball.y += ballvely

        ball,blu_ball,red_ball,ballvelx,ballvely,ball_with = catcher(ball,blue,red,blu_ball,red_ball,ballvelx,ballvely,ball_with)

        #CHOQUE CON LAS COLUMNAS 
        if bluecol.colliderect(ball):
            ballvelx *=-1
            # ball.x = bluecol.x + ANPORT +1
        elif redcol.colliderect(ball):
            ballvelx *=-1
            # ball.x = redcol.x - ANCIRC -1
        elif colu1.colliderect(ball):
            ball.x = POSX1 + ANCOLU + 1
            ballvelx = CIRC_VEL
            ballvely = 0
            pygame.event.post(pygame.event.Event(COL1_HIT))
        elif colu2.colliderect(ball):
            ball.x = POSX2 - ANCIRC - 1
            ballvelx = -1*CIRC_VEL
            ballvely = 0
            pygame.event.post(pygame.event.Event(COL2_HIT))
        elif colu3.colliderect(ball):
            ball.x = POSX3 + ANCOLU + 1
            ballvelx = CIRC_VEL
            ballvely = 0
            pygame.event.post(pygame.event.Event(COL3_HIT))
        elif colu4.colliderect(ball):
            ball.x = POSX4 - ANCOLU - ANCIRC - 1
            ballvelx = -1*CIRC_VEL
            ballvely = 0
            pygame.event.post(pygame.event.Event(COL4_HIT))
        elif colu5.colliderect(ball):
            ball.x = POSX5 + ANCOLU + 1
            ballvelx = CIRC_VEL
            ballvely = 0
            pygame.event.post(pygame.event.Event(COL5_HIT))
        elif colu6.colliderect(ball):
            ball.x = POSX6 - ANCOLU - ANCIRC -1
            ballvelx = -1*CIRC_VEL
            ballvely = 0
            pygame.event.post(pygame.event.Event(COL6_HIT))
        elif ball.x <=0 or ball.x>=(WIDTH - ANCIRC):
            ballvelx *= -1
            ballvely = ballvely
        elif ball.y <=0 or ball.y>=(HEIGHT - ALCIRC):
            ballvelx = ballvelx
            ballvely *= -1
    elif ball_with == "blue":
        ball.x = blue.x + ANJUGA//2 - ANCIRC//2
        ball.y = blue.y + ALJUGA//2 - ALCIRC//2
    elif ball_with == "red":
        ball.x = red.x + ANJUGA//2 - ANCIRC//2
        ball.y = red.y + ALJUGA//2 - ALCIRC//2
    return ball, ballvelx, ballvely, blu_ball, red_ball, ball_with

def calculavel(ball,ballvelx,ballvely,COLU):
    dix = (COLU.x-ball.x)
    tiempo = abs(dix/ballvelx)
    diy = (COLU.y - ball.y + ALCOLU//2)
    ballvelx = int(dix/(0.5*tiempo))
    ballvely = int(diy/(0.5*tiempo))
    if ballvelx > MAXI_VEL:
        ballvelx = MAXI_VEL
    if ballvely > MAXI_VEL:
        ballvely = MAXI_VEL

    return ballvelx,ballvely

def eleccionposi(word,ball,juga):
    if word == "blue":
        ball.x = juga.x + ANJUGA + 10
        ball.y = juga.y + ALJUGA//2 - ALCIRC//2
    elif word == "red":
        ball.x = juga.x - ALCIRC -10
        ball.y = juga.y + ALJUGA//2 - ALCIRC//2


def lanzador(ball1,ball2,blue,COLU2,COLU4,COLU6,ballvelx1,ballvely1,ballvelx2,ballvely2,ball,ball1_with,ball2_with,word):
    
    porteria = randint(1,3)

    if porteria == 1:
        if ball1_with == word:
            eleccionposi(word,ball1,blue)
            ballvelx1,ballvely1 = calculavel(ball1,ballvelx1,ballvely1,COLU2)
            ball1_with = ""
        elif ball2_with == word:
            eleccionposi(word,ball2,blue)
            ballvelx2,ballvely2 = calculavel(ball2,ballvelx2,ballvely2,COLU2)
            ball2_with = ""
    elif porteria == 2:
        if ball1_with == word:
            eleccionposi(word,ball1,blue)
            ballvelx1,ballvely1 = calculavel(ball1,ballvelx1,ballvely1,COLU4)
            ball1_with = ""
        elif ball2_with == word:
            eleccionposi(word,ball2,blue)
            ballvelx2,ballvely2 = calculavel(ball2,ballvelx2,ballvely2,COLU4)
            ball2_with = ""
    elif porteria == 3:
        if ball1_with == word:
            eleccionposi(word,ball1,blue)
            ballvelx1,ballvely1 = calculavel(ball1,ballvelx1,ballvely1,COLU6)
            ball1_with = ""
        elif ball2_with == word:
            eleccionposi(word,ball2,blue)
            ballvelx2,ballvely2 = calculavel(ball2,ballvelx2,ballvely2,COLU6)
            ball2_with = ""

    ball = False

    return ballvelx1,ballvely1,ballvelx2,ballvely2,ball,ball1_with,ball2_with

#DIBUJO DE LA VENTANA
def draw_window(red,blue,ball1,ball2,blu_points,red_points,bluecol,redcol,COLU1, COLU2, COLU3, COLU4, COLU5, COLU6):
    WIND.fill(GREC)
    # WIND.blit(SPACE,(0,0))
    
    # WIND.blit(blue,(blue.x,blue.y))
    # WIND.blit(red,(red.x,red.y))

    red_health_text = PUNTOS_FONT.render("POINTS: " + str(red_points),1,WHIC)
    blu_health_text = PUNTOS_FONT.render("POINTS: " + str(blu_points),1,WHIC)

    WIND.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
    WIND.blit(blu_health_text,(10,10))

    pygame.draw.rect(WIND,BLUC,blue)
    pygame.draw.rect(WIND,REDC,red)

    pygame.draw.rect(WIND,YELC,ball1)
    pygame.draw.rect(WIND,YELC,ball2)
    
    pygame.draw.rect(WIND,BLAC,COLU1)
    pygame.draw.rect(WIND,BLAC,COLU2)
    
    pygame.draw.rect(WIND,BLAC,COLU3)
    pygame.draw.rect(WIND,BLAC,COLU4)
    
    pygame.draw.rect(WIND,BLAC,COLU5)
    pygame.draw.rect(WIND,BLAC,COLU6)

    pygame.draw.rect(WIND,BLUC,bluecol)
    pygame.draw.rect(WIND,REDC,redcol)

    pygame.display.update()

#MENSAJE DE VICTORIA
def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHIC)
    WIND.blit(draw_text,(WIDTH//2-draw_text.get_width()//2,HEIGHT//2-draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

#JUEGO PRINCIPAL
def main():
    
    #VELOCIDADES DE LAS BOLAS
    ballvelx1 = 2
    ballvely1 = 0
    ballvelx2 = -2
    ballvely2 = 0

    #BOLAS DENTRO DE
    ball1_with = ""
    ball2_with = ""

    pygame.init()

    red = pygame.Rect(WIDTH//2 + 100,(HEIGHT//2)-(ALJUGA//2),ANJUGA, ALJUGA)
    blue = pygame.Rect(WIDTH//2 - 100,(HEIGHT//2)-(ALJUGA//2),ANJUGA, ALJUGA)

    ball1 = pygame.Rect(WIDTH//2,HEIGHT//2-(ALCIRC//2),ANCIRC, ALCIRC)
    ball2 = pygame.Rect(WIDTH//2,HEIGHT//2-(ALCIRC//2),ANCIRC, ALCIRC)

    red_points = 0
    blu_points = 0

    red_ball = False
    blu_ball = False

    bluecol = pygame.Rect(POSX3-2,POSY3-2,ANPORT,ALPORT)
    redcol = pygame.Rect(POSX4-2,POSY4-2,ANPORT,ALPORT)

    COLU1 = pygame.Rect(POSX1,POSY1,ANCOLU,ALCOLU)
    COLU2 = pygame.Rect(POSX2,POSY2,ANCOLU,ALCOLU)
    COLU3 = pygame.Rect(POSX3,POSY3,ANCOLU,ALCOLU)
    COLU4 = pygame.Rect(POSX4,POSY4,ANCOLU,ALCOLU)
    COLU5 = pygame.Rect(POSX5,POSY5,ANCOLU,ALCOLU)
    COLU6 = pygame.Rect(POSX6,POSY6,ANCOLU,ALCOLU)

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            #Evento para cerrar el juego
            if event.type == pygame.QUIT:
                run = False
                break
            #Eventos cuando se pulsan ciertas teclas
            if event.type == pygame.KEYDOWN:
                #ADONDE DIRIGEN Y QUIEN DIRIGE LA BOLA
                if event.key == pygame.K_LCTRL and blu_ball:
                    ballvelx1,ballvely1,ballvelx2,ballvely2,blu_ball,ball1_with,ball2_with = lanzador(ball1,ball2,blue,COLU2,COLU4,COLU6,ballvelx1,ballvely1,ballvelx2,ballvely2,blu_ball,ball1_with,ball2_with,"blue")
                if event.key == pygame.K_RCTRL and red_ball:
                    ballvelx1,ballvely1,ballvelx2,ballvely2,red_ball,ball1_with,ball2_with = lanzador(ball1,ball2,red,COLU1,COLU3,COLU5,ballvelx1,ballvely1,ballvelx2,ballvely2,red_ball,ball1_with,ball2_with,"red")
                    
            #EVENTOS DE TIPO PUNTUACION, SOLO UNA BOLA DE MOMENTO
            if event.type == COL1_HIT:
                red_points += 1
                # BULLET_HIT_SOUND.play()
            elif event.type == COL3_HIT:
                red_points += 1
                # BULLET_HIT_SOUND.play()
            elif event.type == COL5_HIT:
                red_points += 1
                # BULLET_HIT_SOUND.play()
            elif event.type == COL2_HIT:
                blu_points += 1
                # BULLET_HIT_SOUND.play()
            elif event.type == COL4_HIT:
                blu_points += 1
                # BULLET_HIT_SOUND.play()
            elif event.type == COL6_HIT:
                blu_points += 1
                # BULLET_HIT_SOUND.play()


        winner_text = ""

        if red_points >= 15:
            winner_text = "Red WINS"
            
        elif blu_points >= 15:
            winner_text = "Blue WINS"

        if winner_text != "":
            draw_winner(winner_text)
            break

        # print(red_bullets,yel_bullets)
        keys_pressed = pygame.key.get_pressed()
        blue_handle_movement(keys_pressed,blue)
        red_handle_movement(keys_pressed,red)

        blue_barrier_control(keys_pressed,bluecol)
        red_barrier_control(keys_pressed,redcol)

        ball1, ballvelx1, ballvely1, blu_ball, red_ball, ball1_with = handle_ball(ball1, 
        ballvelx1, ballvely1, blue, red, blu_ball, red_ball, bluecol,redcol, COLU1, COLU2, COLU3, COLU4, COLU5, COLU6, ball1_with)
        ball2, ballvelx2, ballvely2, blu_ball, red_ball, ball2_with = handle_ball(ball2, 
        ballvelx2, ballvely2, blue, red, blu_ball, red_ball, bluecol,redcol, COLU1, COLU2, COLU3, COLU4, COLU5, COLU6, ball2_with)
        
        draw_window(red,blue,ball1,ball2,blu_points,red_points,bluecol,redcol,COLU1, COLU2, COLU3, COLU4, COLU5, COLU6)

    if not run:
        pygame.quit()
    else:
        main()

if __name__ == "__main__":
    main()