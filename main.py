import random
import time
import turtle
import pygame

window = turtle.Screen()
window.tracer(0)
window.bgpic("space.gif")
window.setup(0.5, 0.75)
window.title("Space Invaders")


# Create laser cannon
cannon = turtle.Turtle()
cannon.penup()
window.addshape("spaceship.gif")
spaceship_equip="spaceship.gif"
cannon.shape(spaceship_equip)
cannon.setposition(0, -200)  # Initial cannon position
cannon.cannon_movement = 0  # -1 for left, 1 for right, 0 for stationary

# Initialize Pygame
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("laser_effect.mp3")  # Load your sound file
shoot1_sound = pygame.mixer.Sound("superlaser.mp3")
pygame.mixer.music.load("background.mp3")  # Change to your music file

# Set the volume (0.0 to 1.0)
pygame.mixer.music.set_volume(0.2)  # Set volume to 20%

# Play the music
pygame.mixer.music.play(-1)

# Game state variables
GAME_RUNNING = 0
lasers = []
power_lasers = []
aliens = []
power_activated = 0
power_activated_time = None
FRAME_RATE = 30
TIME_FOR_1_FRAME = 1 / FRAME_RATE
CANNON_STEP = 10
LASER_LENGTH = 20
LASER_SPEED = 20
ALIEN_SPAWN_INTERVAL = 1.3
ALIEN_SPEED = 3.5
LIFE = 3
COINS= 0

LEFT = -window.window_width() / 2
RIGHT = window.window_width() / 2
TOP = window.window_height() / 2
BOTTOM = -window.window_height() / 2
FLOOR_LEVEL = 0.9 * BOTTOM
GUTTER = 0.025 * window.window_width()

window.addshape("alien.gif")
window.addshape("laser.gif")

highest_score = 0
saved_score_1=0
alien_equip="alien.gif"
laser_equip="laser.gif"
s=1
#shop list
shop_1 = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]


def draw_cannon():
    cannon.clear()
    cannon.turtlesize(1, 4)  # Base
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 10)
    cannon.turtlesize(1, 1.5)  # Next tier
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 20)
    cannon.turtlesize(0.8, 0.3)  # Tip of cannon
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL)

def move_left():
    cannon.cannon_movement = -1

def move_right():
    cannon.cannon_movement = 1

def stop_cannon_movement():
    cannon.cannon_movement = 0

def create_laser():
    if power_activated == 1:
        if power_activated_time is not None and (time.time() - power_activated_time <4)  :
            shoot1_sound.play()
            return power_laser()
    laser = turtle.Turtle()
    laser.penup()
    laser.shape(laser_equip)
    laser.hideturtle()
    laser.setposition(cannon.xcor(), cannon.ycor() + 10)
    laser.setheading(90)
    laser.pendown()
    laser.showturtle()
    shoot_sound.play()
    lasers.append(laser)

def activate_power1():
    global power_activated, power_activated_time,COINS
    power_activated_time = time.time()
    if COINS>10:
        if power_activated == 0:
            power_activated = 1
            COINS -=10
        elif power_activated == 1:
             power_activated = 0

def power_laser():
    laser = turtle.Turtle()
    laser.penup()
    window.addshape("powerlaser.gif")
    laser.shape("powerlaser.gif")  # Set the shape first
    laser.shapesize(stretch_wid=5, stretch_len=4)  # Adjust the size
    laser.hideturtle()
    laser.setposition(cannon.xcor(), cannon.ycor() + 10)
    laser.setheading(90)
    # laser.pendown()
    laser.showturtle()  # Show the laser after positioning
    power_lasers.append(laser)


def life_gain():
    global COINS,LIFE
    if COINS >30:
        COINS-=30
        LIFE+=1

def move_laser(laser):
    laser.clear()
    laser.forward(LASER_SPEED)
    if laser.ycor() > TOP:
        if laser in lasers:
            remove_sprite(laser, lasers)
        elif lasers in power_lasers:
            remove_sprite(laser, power_lasers)

def create_alien(random_num):
    alien = turtle.Turtle()
    alien.penup()
    alien.turtlesize(6)
    alien.setposition(random.randint(int(LEFT + GUTTER), int(RIGHT - GUTTER)), TOP)
    alien.shape(alien_equip)
    alien.setheading(-90)
    alien.pensize(10)
    aliens.append(alien)

def remove_sprite(sprite, sprite_list):
    sprite.clear()
    sprite.hideturtle()
    window.update()
    sprite_list.remove(sprite)


def game_play(x,y):
    global LIFE, GAME_RUNNING, lasers, aliens,COINS,saved_score_1
    window.clear()
    window.tracer(0)
    window.bgpic("space.gif")
    LIFE = 3
    saved_score_1 =0
    score = 0
    lasers.clear()
    aliens.clear()
    GAME_RUNNING = 0
    cannon.shape(spaceship_equip)
    cannon.setposition(0, FLOOR_LEVEL)
    cannon.cannon_movement = 0

    # Create turtle for writing text
    text = turtle.Turtle()
    text.penup()
    text.hideturtle()
    text.setposition(LEFT * 0.8, TOP * 0.6)
    text.color(1, 1, 1)
    # Create instruction for superpowers
    life_icon = turtle.Turtle()
    life_icon.penup()
    life_icon.hideturtle()
    life_icon.goto(RIGHT*0.8,TOP *0.8)
    window.addshape('life+.gif')
    life_icon.shape("life+.gif")
    life_icon.showturtle()

    superpower_icon = turtle.Turtle()
    superpower_icon.penup()
    superpower_icon.hideturtle()
    superpower_icon.goto(RIGHT*0.5,TOP *0.8)
    window.addshape('superpower.gif')
    superpower_icon.shape("superpower.gif")
    superpower_icon.showturtle()

    # Key bindings
    window.onkeypress(move_left, "Left")
    window.onkeypress(move_right, "Right")
    window.onkeyrelease(stop_cannon_movement, "Left")
    window.onkeyrelease(stop_cannon_movement, "Right")
    window.onkeypress(create_laser, "space")
    window.onkeypress(activate_power1, "q")
    window.onkeypress(turtle.bye, "z")
    window.onkeypress(life_gain,'e')
    window.listen()

    draw_cannon()

    # Game loop
    alien_timer = 0
    game_timer = time.time()
    life_timer= 0

    while LIFE > 0:
        window.update()
        time_elapsed = time.time() - game_timer
        text.clear()
        text.write(f"Time: {time_elapsed:5.1f}s\nScore: {score:5}\nLife: {LIFE}\nCoins: {COINS}", font=("Courier", 20, "bold"))

        # Move cannon
        new_x = cannon.xcor() + CANNON_STEP * cannon.cannon_movement
        if LEFT + GUTTER <= new_x <= RIGHT - GUTTER:
            cannon.setx(new_x)
            draw_cannon()

        # Move all lasers
        for laser in lasers.copy():
            move_laser(laser)

        # Spawn new aliens
        if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
            random_num = random.randint(0,4)
            create_alien(random_num)
            alien_timer = time.time()

        # Move all aliens
        # Move all aliens
        for alien in aliens.copy():
            alien.forward(ALIEN_SPEED)

            # Prepare to remove lasers
            lasers_to_remove = []
            power_lasers_to_remove = []

            # Check for collision with normal lasers
            for laser in lasers.copy():
                if laser.distance(alien) < 20:
                    lasers_to_remove.append(laser)
                    remove_sprite(alien, aliens)
                    score += 1
                    saved_score_1+=1
                    COINS+=1

            # Check for collision with power lasers
            for laser in power_lasers.copy():
                move_laser(laser)
                if laser.ycor() > TOP:
                    power_lasers_to_remove.append(laser)
                    continue  # Skip to the next laser

                # Check if they are on the same y level
                if abs(laser.ycor() - alien.ycor()) < 20:
                    if abs(laser.xcor() - alien.xcor()) < 50:  # Define your threshold
                        power_lasers_to_remove.append(laser)
                        remove_sprite(alien, aliens)
                        score += 1
                        saved_score_1+=1

            # Remove lasers after the loop to avoid modifying the list during iteration
            for laser in lasers_to_remove:
                remove_sprite(laser, lasers)

            for laser in power_lasers_to_remove:
                remove_sprite(laser, power_lasers)

            if alien.ycor() < FLOOR_LEVEL and time.time()-life_timer>1:
                life_timer=time.time()
                LIFE -= 1
                remove_sprite(alien, aliens)

        time.sleep(TIME_FOR_1_FRAME)

    # Game Over
    GAME_RUNNING = 1
    game_over_screen(x,y)

def game_over_screen(x,y):
    global window, highest_score
    window.clear()
    window.tracer(0)
    window.bgcolor(0.2, 0.2, 0.2)
    splash_text = turtle.Turtle()
    splash_text.penup()
    splash_text.hideturtle()
    splash_text.color(1, 1, 1)
    splash_text.setposition(LEFT * 0.38, TOP * 0.3)
    splash_text.write("GAME OVER", font=("Courier", 40, "bold"))

    shop_button=turtle.Turtle()
    shop_button.penup()
    shop_button.hideturtle()
    shop_button.goto( RIGHT*0.6,BOTTOM *0.3)
    shop_button.showturtle()
    window.addshape('shop.gif')
    shop_button.shape('shop.gif')
    shop_button.onclick(shop)

    play_again_button= turtle.Turtle()
    play_again_button.penup()
    play_again_button.goto(LEFT*0.6,BOTTOM * 0.3)
    window.addshape('playagain.gif')
    play_again_button.shape("playagain.gif")
    play_again_button.onclick(play_again)

    inventory_button = turtle.Turtle()
    inventory_button.penup()
    inventory_button.goto(RIGHT*0.01,BOTTOM*0.3)
    window.addshape("inventory.gif")
    inventory_button.shape("inventory.gif")
    inventory_button.onclick(inventory)

    score_text = turtle.Turtle()
    score_text.penup()
    score_text.goto(-50,50)
    score_text.hideturtle()
    score_text.write(f"Score : {saved_score_1}",font=("Courier", 20, "bold"))

    if highest_score<saved_score_1:
        highest_score = saved_score_1

    score_text.goto(-100,20)
    score_text.write(f"Highest Score : {highest_score}",font=("Courier", 20, "bold"))



    window.update()
def play_again(x, y):
    game_play(x,y)

def exit_game(x,y):
    turtle.bye()

def main_menu():
    play_button= turtle.Turtle()
    play_button.penup()
    play_button.goto(0,0)
    window.addshape("PLAY.gif")
    play_button.shape("PLAY.gif")
    play_button.showturtle()
    play_button.onclick(game_play)

    exit_button= turtle.Turtle()
    exit_button.penup()
    exit_button.goto(0,-100)
    window.addshape("EXIT.gif")
    exit_button.shape("EXIT.gif")
    exit_button.showturtle()
    exit_button.onclick(exit_game)

    logo= turtle.Turtle()
    logo.penup()
    logo.goto(0,150)
    window.addshape("spacewar.gif")
    logo.shape("spacewar.gif")
    logo.showturtle()


    window.update()

def equip1_0(x,y):
    global alien_equip
    alien_equip = "alien.gif"

def equip1_1(x,y):
    global alien_equip
    alien_equip = "alien1.gif"

def equip1_2(x,y):
    global alien_equip
    alien_equip = "alien2.gif"

def equip1_3(x,y):
    global alien_equip
    alien_equip = "alien3.gif"

def equip1_4(x,y):
    global alien_equip
    alien_equip = "alien4.gif"

def equip1_5(x,y):
    global alien_equip
    alien_equip = "alien5.gif"

def equip1_6(x,y):
    global alien_equip
    alien_equip = "alien6.gif"

def equip2_0(x,y):
    global spaceship_equip
    spaceship_equip = "spaceship.gif"

def equip2_1(x,y):
    global spaceship_equip
    spaceship_equip = "spaceship1.gif"

def equip2_2(x,y):
    global spaceship_equip
    spaceship_equip = "spaceship2.gif"

def equip2_3(x,y):
    global spaceship_equip
    spaceship_equip = "spaceship3.gif"

def equip2_4(x,y):
    global spaceship_equip
    spaceship_equip = "spaceship4.gif"

def equip2_5(x,y):
    global spaceship_equip
    spaceship_equip = "spaceship5.gif"

def equip2_6(x,y):
    global spaceship_equip
    spaceship_equip = "spaceship6.gif"

def equip3_0(x,y):
    global laser_equip
    laser_equip = "laser.gif"

def equip3_1(x,y):
    global laser_equip
    laser_equip = "laser1.gif"

def equip3_2(x,y):
    global laser_equip
    laser_equip = "laser2.gif"

def equip3_3(x,y):
    global laser_equip
    laser_equip = "laser3.gif"

def equip3_4(x,y):
    global laser_equip
    laser_equip = "laser4.gif"

def equip3_5(x,y):
    global laser_equip
    laser_equip = "laser5.gif"

def equip3_6(x,y):
    global laser_equip
    laser_equip = "laser6.gif"

def inventory(x,y):
    global shop_1
    window.clear()
    window.tracer(0)
    window.bgcolor(0.2, 0.2, 0.2)
    splash_text = turtle.Turtle()
    splash_text.penup()
    splash_text.hideturtle()
    splash_text.color(1, 1, 1)
    splash_text.setposition(LEFT*0.3, TOP * 0.8)
    splash_text.write("INVENTORY", font=("Courier", 40, "bold"))


    return_button = turtle.Turtle()
    return_button.penup()
    return_button.goto(-300,250)
    window.addshape("return.gif")
    return_button.shape("return.gif")
    return_button.onclick(game_over_screen)

    text = turtle.Turtle()
    text.penup()
    text.goto(-330,120)
    text.hideturtle()
    text.write("ENEMIES", font=("Courier", 20, "bold"))


    alien_1 = turtle.Turtle()
    alien_1.penup()
    alien_1.goto(-330,30)
    alien_1.shape("alien.gif")
    alien_1.onclick(equip1_0)

    alien1_1 = turtle.Turtle()
    alien1_1.penup()
    alien1_1.goto(-330, -70)
    window.addshape("alien1.gif")
    alien1_1.shape("alien1.gif")
    alien1_1.onclick(equip1_1)
    if shop_1 [0][0] != 1:
        alien1_1.hideturtle()



    alien2_1 = turtle.Turtle()
    alien2_1.penup()
    alien2_1.goto(-180, -70)
    window.addshape("alien2.gif")
    alien2_1.shape("alien2.gif")
    alien2_1.onclick(equip1_2)
    if shop_1 [0][1] != 1:
        alien2_1.hideturtle()


    alien3_1 = turtle.Turtle()
    alien3_1.penup()
    alien3_1.goto(-330, -170)
    window.addshape("alien3.gif")
    alien3_1.shape("alien3.gif")
    alien3_1.onclick(equip1_3)
    if shop_1 [0][2] != 1:
        alien3_1.hideturtle()


    alien4_1 = turtle.Turtle()
    alien4_1.penup()
    alien4_1.goto(-180, -170)
    window.addshape("alien4.gif")
    alien4_1.shape("alien4.gif")
    alien4_1.onclick(equip1_4)
    if shop_1 [0][3] != 1:
        alien4_1.hideturtle()


    alien5_1 = turtle.Turtle()
    alien5_1.penup()
    alien5_1.goto(-330, -270)
    window.addshape("alien5.gif")
    alien5_1.shape("alien5.gif")
    alien5_1.onclick(equip1_5)
    if shop_1 [0][4] != 1:
        alien5_1.hideturtle()


    alien6_1 = turtle.Turtle()
    alien6_1.penup()
    alien6_1.goto(-180, -270)
    window.addshape("alien6.gif")
    alien6_1.shape("alien6.gif")
    alien6_1.onclick(equip1_6)
    if shop_1 [0][5] != 1:
        alien6_1.hideturtle()


    text.goto(-130,70)
    text.setheading(270)
    text.pendown()
    text.forward(400)
    text.penup()


    text.goto(-40,120)
    text.write("PLAYER", font=("Courier", 20, "bold"))

    spaceship_1 = turtle.Turtle()
    spaceship_1.penup()
    spaceship_1.goto(-60,30)
    spaceship_1.shape("spaceship.gif")
    spaceship_1.onclick(equip2_0)

    spaceship1_1 = turtle.Turtle()
    spaceship1_1.penup()
    spaceship1_1.goto(-60, -70)
    window.addshape("spaceship1.gif")
    spaceship1_1.shape("spaceship1.gif")
    spaceship1_1.onclick(equip2_1)
    if shop_1 [1][0] != 1:
        spaceship1_1.hideturtle()


    spaceship2_1 = turtle.Turtle()
    spaceship2_1.penup()
    spaceship2_1.goto(50, -70)
    window.addshape("spaceship2.gif")
    spaceship2_1.shape("spaceship2.gif")
    spaceship2_1.onclick(equip2_2)
    if shop_1 [1][1] != 1:
        spaceship2_1.hideturtle()

    spaceship3_1 = turtle.Turtle()
    spaceship3_1.penup()
    spaceship3_1.goto(-60, -170)
    window.addshape("spaceship3.gif")
    spaceship3_1.shape("spaceship3.gif")
    spaceship3_1.onclick(equip2_3)
    if shop_1 [1][2] != 1:
        spaceship3_1.hideturtle()

    spaceship4_1 = turtle.Turtle()
    spaceship4_1.penup()
    spaceship4_1.goto(50, -170)
    window.addshape("spaceship4.gif")
    spaceship4_1.shape("spaceship4.gif")
    spaceship4_1.onclick(equip2_4)
    if shop_1 [1][3] != 1:
        spaceship4_1.hideturtle()

    spaceship5_1 = turtle.Turtle()
    spaceship5_1.penup()
    spaceship5_1.goto(-60, -270)
    window.addshape("spaceship5.gif")
    spaceship5_1.shape("spaceship5.gif")
    spaceship5_1.onclick(equip2_5)
    if shop_1 [1][4] != 1:
        spaceship5_1.hideturtle()

    spaceship6_1 = turtle.Turtle()
    spaceship6_1.penup()
    spaceship6_1.goto(50, -270)
    window.addshape("spaceship6.gif")
    spaceship6_1.shape("spaceship6.gif")
    spaceship6_1.onclick(equip2_6)
    if shop_1 [1][5] != 1:
        spaceship6_1.hideturtle()


    text.goto(130,70)
    text.setheading(270)
    text.pendown()
    text.forward(400)
    text.penup()


    text.goto(200,120)
    text.write("LASER", font=("Courier", 20, "bold"))

    laser_1= turtle.Turtle()
    laser_1.penup()
    laser_1.goto(180,30)
    laser_1.shape("laser.gif")
    laser_1.onclick(equip3_0)

    laser1_1 = turtle.Turtle()
    laser1_1.penup()
    laser1_1.goto(180, -70)
    window.addshape("laser1.gif")
    laser1_1.shape("laser1.gif")
    laser1_1.onclick(equip3_1)
    if shop_1 [2][0] != 1:
        laser1_1.hideturtle()

    laser2_1 = turtle.Turtle()
    laser2_1.penup()
    laser2_1.goto(300, -70)
    window.addshape("laser2.gif")
    laser2_1.shape("laser2.gif")
    laser2_1.hideturtle()
    laser2_1.onclick(equip3_2)
    if shop_1 [2][0] != 1:
        laser1_1.hideturtle()

    laser3_1 = turtle.Turtle()
    laser3_1.penup()
    laser3_1.goto(180, -170)
    window.addshape("laser3.gif")
    laser3_1.shape("laser3.gif")
    laser3_1.hideturtle()
    laser3_1.onclick(equip3_3)
    if shop_1 [2][0] != 1:
        laser1_1.hideturtle()

    laser4_1 = turtle.Turtle()
    laser4_1.penup()
    laser4_1.goto(300, -170)
    window.addshape("laser4.gif")
    laser4_1.shape("laser4.gif")
    laser4_1.hideturtle()
    laser4_1.onclick(equip3_4)
    if shop_1 [2][0] != 1:
        laser1_1.hideturtle()

    laser5_1 = turtle.Turtle()
    laser5_1.penup()
    laser5_1.goto(180, -270)
    window.addshape("laser5.gif")
    laser5_1.shape("laser5.gif")
    laser5_1.hideturtle()
    laser5_1.onclick(equip3_5)
    if shop_1 [2][0] != 1:
        laser1_1.hideturtle()

    laser6_1 = turtle.Turtle()
    laser6_1.penup()
    laser6_1.goto(300, -270)
    window.addshape("laser6.gif")
    laser6_1.shape("laser6.gif")
    laser6_1.hideturtle()
    laser6_1.onclick(equip3_6)
    if shop_1 [2][0] != 1:
        laser1_1.hideturtle()


    window.update()

def purchase1_1(x,y):
    global shop_1,COINS
    if COINS>=1 and shop_1 [0][0]==0:
        shop_1 [0][0] += 1
        COINS -=1

def purchase1_2(x,y):
    global shop_1,COINS
    if COINS>=100 and shop_1 [0][1]==0:
        shop_1 [0][1] += 1
        COINS -=100

def purchase1_3(x,y):
    global shop_1,COINS
    if COINS>=100 and shop_1 [0][2]==0:
        shop_1 [0][2] += 1
        COINS -=100

def purchase1_4(x,y):
    global shop_1,COINS
    if COINS>=100 and shop_1 [0][3]==0:
        shop_1 [0][3] += 1
        COINS -=100

def purchase1_5(x,y):
    global shop_1,COINS
    if COINS>=100 and shop_1 [0][4]==0:
        shop_1 [0][4] += 1
        COINS -=100

def purchase1_6(x,y):
    global shop_1,COINS
    if COINS>=100 and shop_1 [0][5]==0:
        shop_1 [0][5] += 1
        COINS -=100

def purchase2_1(x,y):
    global shop_1,COINS
    if COINS>=1 and shop_1 [1][0]==0:
        shop_1 [1][0] += 1
        COINS -=1

def purchase2_2(x,y):
    global shop_1,COINS
    if COINS>=100 and shop_1 [1][1]==0:
        shop_1 [1][1] += 1
        COINS -=100

def purchase2_3(x,y):
    global shop_1,COINS
    if COINS>=100 and shop_1 [1][2]==0:
        shop_1 [1][2] += 1
        COINS -=100

def purchase2_4(x,y):
    global shop_1,COINS
    if COINS>=100 and shop_1 [1][3]==0:
        shop_1 [1][3] += 1
        COINS -=100

def purchase2_5(x,y):
    global shop_1,COINS
    if COINS>=100 and shop_1 [1][4]==0:
        shop_1 [1][4] += 1
        COINS -=100

def purchase2_6(x,y):
    global shop_1,COINS
    if COINS>=100 and shop_1 [1][5]==0:
        shop_1 [1][5] += 1
        COINS -=100

def purchase3_1(x,y):
    global shop_1,COINS
    if COINS>=1 and shop_1 [2][0]==0:
        shop_1 [2][0] += 1
        COINS -=1

def purchase3_2(x,y):
    global shop_1,COINS
    if COINS>=100 and shop_1 [2][1]==0:
        shop_1 [2][1] += 1
        COINS -=100

def purchase3_3(x,y):
    global shop_1,COINS
    if COINS>=100 and shop_1 [2][2]==0:
        shop_1 [2][2] += 1
        COINS -=100

def purchase3_4(x,y):
    global shop_1,COINS
    if COINS>=100 and shop_1 [2][3]==0:
        shop_1 [2][3] += 1
        COINS -=100

def purchase3_5(x,y):
    global shop_1,COINS
    if COINS>=100 and shop_1 [2][4]==0:
        shop_1 [2][4] += 1
        COINS -=100

def purchase3_6(x,y):
    global shop_1,COINS
    if COINS>=100 and shop_1 [2][5]==0:
        shop_1 [2][5] += 1
        COINS -=100

def shop(x,y):
    global window,COINS
    window.clear()
    window.tracer(0)
    window.bgcolor(0.2, 0.2, 0.2)
    splash_text = turtle.Turtle()
    splash_text.penup()
    splash_text.hideturtle()
    splash_text.color(1, 1, 1)
    splash_text.setposition(LEFT*0.15, TOP * 0.3)
    splash_text.write("SHOP", font=("Courier", 40, "bold"))

    line1=turtle.Turtle()
    line1.penup()
    line1.hideturtle()
    line1.goto(-130,20)
    line1.setheading(270)
    line1.pendown()
    line1.forward(350)
    line1.penup()
    line1.goto(120,20)
    line1.pendown()
    line1.forward(350)
    line1.penup()
    line1.goto(-390,-20)
    line1.setheading(0)
    line1.pendown()
    line1.forward(770)
    line1.penup()
    line1.goto(-390, 20)
    line1.setheading(0)
    line1.pendown()
    line1.forward(770)
    line1.penup()
    line1.goto(-390, 20)
    line1.setheading(270)
    line1.pendown()
    line1.forward(350)
    line1.penup()
    line1.goto(380, 20)
    line1.setheading(270)
    line1.pendown()
    line1.forward(350)
    line1.penup()
    line1.goto(-390, -330)
    line1.setheading(0)
    line1.pendown()
    line1.forward(770)
    line1.penup()
    line1.goto(-330, -20)
    line1.setheading(0)
    line1.write("Enemies",font=("Courier", 20, "bold"))
    line1.goto(-40,-20)
    line1.write("Player",font=("Courier", 20, "bold"))
    line1.goto(200,-20)
    line1.write("Laser", font=("Courier", 20, "bold"))

    return_button = turtle.Turtle()
    return_button.penup()
    return_button.goto(-300,250)
    window.addshape("return.gif")
    return_button.shape("return.gif")
    return_button.onclick(game_over_screen)

    coins=turtle.Turtle()
    coins.penup()
    coins.hideturtle()
    coins.goto(-350,100)
    coins.write(f"COINS : {COINS}",font=("Courier", 20, "bold"))

    price = turtle.Turtle()
    price.penup()
    price.hideturtle()

    alien1=turtle.Turtle()
    alien1.penup()
    alien1.goto(-330,-70)
    window.addshape("alien1.gif")
    alien1.shape("alien1.gif")
    alien1.onclick(purchase1_1)

    coins.goto(-360,-130)
    coins.write("100 COINS", font=("Courier", 10, "bold"))

    alien2 = turtle.Turtle()
    alien2.penup()
    alien2.goto(-180, -70)
    window.addshape("alien2.gif")
    alien2.shape("alien2.gif")
    alien2.onclick(purchase1_2)

    coins.goto(-220,-130)
    coins.write("100 COINS", font=("Courier", 10, "bold"))

    alien3 = turtle.Turtle()
    alien3.penup()
    alien3.goto(-330, -170)
    window.addshape("alien3.gif")
    alien3.shape("alien3.gif")
    alien3.onclick(purchase1_3)
    coins.goto(-360, -230)
    coins.write("100 COINS", font=("Courier", 10, "bold"))

    alien4 = turtle.Turtle()
    alien4.penup()
    alien4.goto(-180, -170)
    window.addshape("alien4.gif")
    alien4.shape("alien4.gif")
    alien4.onclick(purchase1_4)
    coins.goto(-220,-230)
    coins.write("100 COINS", font=("Courier", 10, "bold"))

    alien5 = turtle.Turtle()
    alien5.penup()
    alien5.goto(-330, -270)
    window.addshape("alien5.gif")
    alien5.shape("alien5.gif")
    alien5.onclick(purchase1_5)
    coins.goto(-360,-320)
    coins.write("100 COINS", font=("Courier", 10, "bold"))

    alien6 = turtle.Turtle()
    alien6.penup()
    alien6.goto(-180, -270)
    window.addshape("alien6.gif")
    alien6.shape("alien6.gif")
    alien6.onclick(purchase1_6)
    coins.goto(-220,-320)
    coins.write("100 COINS", font=("Courier", 10, "bold"))

    spaceship1 = turtle.Turtle()
    spaceship1.penup()
    spaceship1.goto(-60,-70)
    window.addshape("spaceship1.gif")
    spaceship1.shape("spaceship1.gif")
    spaceship1.onclick(purchase2_1)
    coins.goto(-100,-130)
    coins.write("100 COINS", font=("Courier", 10, "bold"))

    spaceship2 = turtle.Turtle()
    spaceship2.penup()
    spaceship2.goto(50, -70)
    window.addshape("spaceship2.gif")
    spaceship2.shape("spaceship2.gif")
    spaceship2.onclick(purchase2_2)
    coins.goto(20, -130)
    coins.write("100 COINS", font=("Courier", 10, "bold"))

    spaceship3 = turtle.Turtle()
    spaceship3.penup()
    spaceship3.goto(-60, -170)
    window.addshape("spaceship3.gif")
    spaceship3.shape("spaceship3.gif")
    spaceship3.onclick(purchase2_3)
    coins.goto(-100, -230)
    coins.write("100 COINS", font=("Courier", 10, "bold"))

    spaceship4 = turtle.Turtle()
    spaceship4.penup()
    spaceship4.goto(50, -170)
    window.addshape("spaceship4.gif")
    spaceship4.shape("spaceship4.gif")
    spaceship4.onclick(purchase2_4)
    coins.goto(20, -230)
    coins.write("100 COINS", font=("Courier", 10, "bold"))

    spaceship5 = turtle.Turtle()
    spaceship5.penup()
    spaceship5.goto(-60, -270)
    window.addshape("spaceship5.gif")
    spaceship5.shape("spaceship5.gif")
    spaceship5.onclick(purchase2_5)
    coins.goto(-100, -330)
    coins.write("100 COINS", font=("Courier", 10, "bold"))

    spaceship6 = turtle.Turtle()
    spaceship6.penup()
    spaceship6.goto(50, -270)
    window.addshape("spaceship6.gif")
    spaceship6.shape("spaceship6.gif")
    spaceship6.onclick(purchase2_6)
    coins.goto(20, -330)
    coins.write("100 COINS", font=("Courier", 10, "bold"))


    laser1= turtle.Turtle()
    laser1.penup()
    laser1.goto(180,-70)
    window.addshape("laser1.gif")
    laser1.shape("laser1.gif")
    laser1.onclick(purchase3_1)
    coins.goto(150,-130)
    coins.write("100 COINS", font=("Courier", 10, "bold"))


    laser2= turtle.Turtle()
    laser2.penup()
    laser2.goto(300,-70)
    window.addshape("laser2.gif")
    laser2.shape("laser2.gif")
    laser2.onclick(purchase3_2)
    coins.goto(270,-130)
    coins.write("100 COINS", font=("Courier", 10, "bold"))


    laser3= turtle.Turtle()
    laser3.penup()
    laser3.goto(180,-170)
    window.addshape("laser3.gif")
    laser3.shape("laser3.gif")
    laser3.onclick(purchase3_3)
    coins.goto(150,-230)
    coins.write("100 COINS", font=("Courier", 10, "bold"))


    laser4= turtle.Turtle()
    laser4.penup()
    laser4.goto(300,-170)
    window.addshape("laser4.gif")
    laser4.shape("laser4.gif")
    laser4.onclick(purchase3_4)
    coins.goto(270,-230)
    coins.write("100 COINS", font=("Courier", 10, "bold"))


    laser5= turtle.Turtle()
    laser5.penup()
    laser5.goto(180,-270)
    window.addshape("laser5.gif")
    laser5.shape("laser5.gif")
    laser5.onclick(purchase3_5)
    coins.goto(150,-330)
    coins.write("100 COINS", font=("Courier", 10, "bold"))


    laser6= turtle.Turtle()
    laser6.penup()
    laser6.goto(300,-270)
    window.addshape("laser6.gif")
    laser6.shape("laser6.gif")
    laser6.onclick(purchase3_6)
    coins.goto(270,-330)
    coins.write("100 COINS", font=("Courier", 10, "bold"))


    window.update()
# Start the game
main_menu()



turtle.done()
