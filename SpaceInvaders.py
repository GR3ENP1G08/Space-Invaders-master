import turtle
import math
import cv2
from Tracker import *

#Ecrã
window = turtle.Screen()
window.title("Space Invaders")

#Imagens usadas
turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")
window.bgpic("space_invaders_background.gif")

#Pontuação
score = 0
score_pen = turtle.Turtle()
score_pen.penup()
score_pen.speed(0)
score_pen.color("white")
score_pen.setposition(-290, 280)
score_string = "Score: %s" % score
score_pen.write(score_string, False, align = "left", font=("Arial", 14, "normal"))
score_pen.hideturtle()


#Player
player = turtle.Turtle()
player.shape("player.gif")
player.speed(0)
player.penup()
player.setposition(0, -250)
player.setheading(90)
player_speed = 30

#Inimigos
number_of_enemies = 5
enemy_y_decrement_offset = 35
enemy_x_offset = 40
enemies = []

for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

index_of_current_enemy = 0
for enemy in enemies:
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    enemy_x_position = -200 + (index_of_current_enemy * enemy_x_offset)
    enemy_y_position = 250
    enemy.setposition(enemy_x_position, enemy_y_position)
    index_of_current_enemy += 1

enemy_speed = 5

#Bala
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.penup()
bullet.shapesize(0.5, 0.5)
bullet.setheading(90)
bullet.hideturtle()
bullet.speed(0)
bullet_speed = 30

# Incializar a Camara
cap = cv2.VideoCapture()
image = None

# Inicialização do tracker
tracker = None
direction, isPlayerFiring = 0, 0

# Rectangulo do Rato
refPt = []
cropping = False

def click_and_crop(event, x, y, flags, param):
    # Referências globais para as variáveis usadas no evento do mouse
    global refPt, cropping

    # Se o botão esquerdo do mouse foi pressionado, registra o ponto inicial
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # Se o botão esquerdo do mouse foi solto, registra o ponto final
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False

        # Desenha o retângulo na janela
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("Camera", image)

cv2.namedWindow("Camera")
cv2.setMouseCallback("Camera", click_and_crop)


#Movimentação do player
def move_left():
    player_x_position = player.xcor()
    player_x_position -= player_speed
    if player_x_position < -280:
        player_x_position = -280
    player.setx(player_x_position)

def move_right():
    player_x_position = player.xcor()
    player_x_position += player_speed
    if player_x_position > 280:
        player_x_position = 280
    player.setx(player_x_position)

#Disparar bala
def fire_bullet():
    if not bullet.isvisible():
        x_pos = player.xcor()
        y_pos = player.ycor() + 10
        bullet.setposition(x_pos, y_pos)
        bullet.showturtle()

#Ver se existe colição
def isCollission(turtle1, turtle2):
    distance = math.sqrt(math.pow(turtle1.xcor() - turtle2.xcor(), 2) + math.pow(turtle1.ycor() - turtle2.ycor(), 2))

    if distance < 20:
        return True
    else:
        return False

#Main game loop
game_over = False
while not game_over:
    if not cap.isOpened():
        cap.open(0)
    _, image_camera = cap.read()
    image_camera = image_camera[:, ::-1, :]

    image = image_camera.copy()

    # Se o retângulo foi selecionado, exibe a imagem com o retângulo
    if len(refPt) == 2 and tracker is None:
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        # Iniciar o Tracker
        tracker = Tracker(image, (refPt[0][0], refPt[0][1],
                                        refPt[1][0] - refPt[0][0],
                                        refPt[1][1] - refPt[0][1]))

    if tracker is not None:
        direction, isPlayerFiring = tracker.track(image)

    cv2.imshow("Camera", image)

    #Movimentação inimigos
    for enemy in enemies:
        enemy_x_position = enemy.xcor()
        enemy_x_position += enemy_speed
        enemy.setx(enemy_x_position)

        #Ver se o inimigo tocou na borda esquerda
        if enemy_x_position < -280:
            #Mover inimigos para baixo
            for enemy in enemies:
                enemy_y_position = enemy.ycor()
                enemy_y_position -= enemy_y_decrement_offset;
                enemy.sety(enemy_y_position)
            enemy_speed *= -1

        # Ver se o inimigo tocou na borda direita
        elif enemy_x_position > 280:
            #Mover inimigos para baixo
            for enemy in enemies:
                enemy_y_position = enemy.ycor()
                enemy_y_position -= enemy_y_decrement_offset;
                enemy.sety(enemy_y_position)
            enemy_speed *= -1

        #Ver se existe colição entre bala e inimigo
        if isCollission(bullet, enemy):
            #Resetar bala
            bullet.hideturtle()
            bullet.setposition(0, -400)
            #Resetar inimigo
            enemy.setposition(-200, 250)
            score += 10
            score_string = "Score: %s" % score
            score_pen.clear()
            score_pen.write(score_string, False, align = "left", font = ("Arial", 14, "normal"))

        #Ver se o inimigo passa da linha do player
        if enemy_y_position < -250 and not game_over:
            enemy.hideturtle()
            player.hideturtle()
            print("Game over")
            game_over = True

    #Ver se é possivel disparar a bala
    if bullet.isvisible():
        bullet_y_position = bullet.ycor()
        bullet_y_position += bullet_speed
        bullet.sety(bullet_y_position)

    #Ver se a bala chegou a borda em cima
    if bullet.ycor() > 275:
        bullet.hideturtle()

    #Controlos
    # turtle.listen()

    if isPlayerFiring:
        fire_bullet()
    if direction == -1:
        move_left()
    elif direction == 1:
        move_right()

    # turtle.onkeypress(move_left, "Left")
    # turtle.onkeypress(move_right, "Right")
    # turtle.onkeypress(fire_bullet, "space")

turtle.done()
cv2.destroyAllWindows()
cap.release()