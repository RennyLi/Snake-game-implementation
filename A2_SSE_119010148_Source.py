import turtle
import random

g_food = []  # The food items
g_eaten_food = []  # The food items that have been consumed by the snake
g_body_id = []  # The stamp ID of the snake body
g_decelerate_time = 4  # The times that the snake needs to decelerate
g_track = [(0,0)]  # Save all the locations of the snake head passes
g_snake_body = None  # The last block of the snake body. Equally the snake "tail" block.
g_game_screen = None  # Set the game area
g_snake_head = None  # Set the snake head
g_monster = None  # Set the monster component
g_pen = None  # Set the pen to write texts
g_elapsed_time = 0  # The elapsed time of the game
g_contact_monster = 0  # The times that the monster collides the snake body part
g_time_rate = 500  # The motion time rate (velocity)
g_end = False  # Whether the game is over

def configureScreen(w = 500, h = 500):
    # Set the game area
    # Define the game area as 500 × 500 in dimension
    global g_game_screen
    g_game_screen = turtle.Screen()
    g_game_screen.setup(w,h)
    g_game_screen.bgcolor("white")
    g_game_screen.tracer(0)  # Disable auto screen fresh

    # Use the four arrow keys to maneuver the snake
    # Use space bar to pause the snake motion
    g_game_screen.onkeypress(go_up,"Up")
    g_game_screen.onkeypress(go_down,"Down")
    g_game_screen.onkeypress(go_left,"Left")
    g_game_screen.onkeypress(go_right,"Right")
    g_game_screen.onkeypress(pause,"space")

def configureTurtle(instance = None, shape = "square", fill_color = "", border_color = "", x = 0, y = 0):
    # Define a turtle module to make other turtle objects
    instance.speed(0)
    instance.shape(shape)
    instance.color(border_color,fill_color)
    instance.penup()
    instance.goto(x,y)

def configureSnake():
    # Set the initial snake component
    global g_snake_head
    global g_snake_body
    global g_body_id
    global g_game_screen
    g_snake_body = turtle.Turtle()
    configureTurtle(instance = g_snake_body, fill_color = "black", border_color = "blue")

    # Set the initial length of the tail to be 5
    # The tail of length 5 contains the snake tail block. So we just set it to be 4.
    # Later when the snake consumes food, the extended length will exclude snake tail.
    i = 0
    while i < 4:
        m = g_snake_body.stamp()
        g_body_id.insert(0,m)
        i += 1

    # Set the snake head
    g_snake_head = turtle.Turtle()
    configureTurtle(instance = g_snake_head, fill_color = "red")
    g_snake_head.direction = "stop"
    
    # Manually refresh the game area
    g_game_screen.update()

def configureMonster():
    # Set the monster component
    global g_monster
    global g_game_screen
    g_monster = turtle.Turtle()

    # On startup, place the monster on a random position with a fair distance from the snake
    monster_x = random.choice([random.randint(-220,-60),random.randint(60,220)])
    monster_y = random.choice([random.randint(-220,-60),random.randint(60,220)])
    configureTurtle(instance = g_monster, fill_color = "purple", x = monster_x, y = monster_y)
    g_monster.direction = "stop"

    # Manually refresh the game area
    g_game_screen.update()

def configurePen():
    # Define a pen to write the introduction texts
    global g_pen
    g_pen = turtle.Turtle()
    g_pen.speed(0)
    g_pen.color("black")
    g_pen.penup()
    g_pen.hideturtle()

def snake_food():
    # Set the food items
    global g_food
    for food in range(1,10):
    # Represented as numbers from 1 to 9
        while True:
            number = turtle.Turtle()
            number.speed(0)

            # Displayed within the game area in random
            x = random.randint(-220,220)
            y = random.randint(-220,220)
            number.penup()
            number.hideturtle()
            number.goto(x,y)

            # Ensure the food items will not overlap with each other
            check = True
            if len(g_food) != 0:
                for i in g_food:
                    if number.distance(i) < 40:
                        check = False
            if check == False:
                continue 
            number.write(food)
            g_food.append(number)
            break
    
    # Manually refresh the game area
    g_game_screen.update()

def monster_direction():
    # Set the monster direction
    global g_monster

    # Divide the screen area into 4 parts. Compute the angle snake towards the monster.
    # Check which part the angle is in. Then determine the monster motion direction.
    if g_monster.towards(g_snake_head) <= 45 or g_monster.towards(g_snake_head) > 315:
        g_monster.direction = "right"
    elif g_monster.towards(g_snake_head) > 45 and g_monster.towards(g_snake_head) <= 135:
        g_monster.direction = "up"
    elif g_monster.towards(g_snake_head) > 135 and g_monster.towards(g_snake_head) <= 225:
        g_monster.direction = "left"
    elif g_monster.towards(g_snake_head) > 225 and g_monster.towards(g_snake_head) <= 315:
        g_monster.direction = "down"

def screen_title():
    # Set the title of the screen. Keep track of the total elapsed time and monster-snake collisions
    global g_elapsed_time
    global g_contact_monster
    global g_end
    if g_end == False:
        g_elapsed_time += 1
    g_game_screen.title("Snake:   Contacted:{}, Time:{} second(s)".format(g_contact_monster, g_elapsed_time))

    # Call the function every 1000 milliseconds(1 second)
    # That is to keep track of the total elapsed game time in seconds
    g_game_screen.ontimer(screen_title, 1000)

def introduction():
    # Set the introduction content
    global g_pen
    g_pen.goto(-220,220)
    g_pen.write("Welcome to Renny's version of snake.",font = ("Comic Sans MS",12,"normal"))
    g_pen.goto(-220,180)
    g_pen.write("You are going to use the 4 arrow keys to move the snake",font = ("Comic Sans MS",12,"normal"))
    g_pen.goto(-220,160)
    g_pen.write("around the screen, trying to consume all the food items", font = ("Comic Sans MS",12,"normal"))
    g_pen.goto(-220,140)
    g_pen.write("before the monster catches you.",font = ("Comic Sans MS",12,"normal"))
    g_pen.goto(-220,100)
    g_pen.write("Click anywhere on the screen to start the game. Have fun!", font = ("Comic Sans MS",12,"normal"))

def touch_screen_boundary(part):
    # Check whether the monster or snake reach the boundary
    # If they reach the boundary, then stop motion
    if part.ycor() >= 240 and part.direction == "up":
        part.direction = "stop"
    if part.ycor() <= -240 and part.direction == "down":
        part.direction = "stop"
    if part.xcor() <= -240 and part.direction == "left":
        part.direction = "stop"
    if part.xcor() >= 240 and part.direction == "right":
        part.direction = "stop"

def determine_win():
    # Check whether the user wins the game
    global g_eaten_food
    global g_game_screen
    global g_end
    global g_decelerate_time
    if len(g_eaten_food) == 9 and g_decelerate_time == 0:
        show_win()
        g_game_screen.onkeypress(pause,"Up")
        g_game_screen.onkeypress(pause,"Down")
        g_game_screen.onkeypress(pause,"Left")
        g_game_screen.onkeypress(pause,"Right")
        g_game_screen.onkeypress(pause,"space")
        g_end = True

def determine_lose():
    # Check whether the user loses the game
    global g_monster
    global g_snake_head
    global g_game_screen
    global g_end

    # If the monster touches the snake head, then the user loses the game
    if g_monster.distance(g_snake_head) <= 20:
        show_lose()
        g_game_screen.onkeypress(pause,"Up")
        g_game_screen.onkeypress(pause,"Down")
        g_game_screen.onkeypress(pause,"Left")
        g_game_screen.onkeypress(pause,"Right")
        g_game_screen.onkeypress(pause,"space")
        g_end = True

def show_win():
    # Show on the screen to inform the user of the success
    global g_snake_head
    global g_monster
    global g_pen
    g_snake_head.direction = "stop"
    g_monster.direction = "stop"
    g_pen.color("red")
    g_pen.goto(0,0)
    g_pen.hideturtle()
    g_pen.write("You win!!", align = "Center", font = ("Comic Sans MS",18,"normal"))

def show_lose():
    # Show on the screen to inform the user of the failure
    global g_snake_head
    global g_monster
    g_snake_head.direction = "stop"
    g_monster.direction = "stop"
    g_pen.color("red")
    g_pen.goto(0,0)
    g_pen.hideturtle()
    g_pen.write("Game over!!", align = "Center", font = ("Comic Sans MS",18,"normal"))

def go_up():
    global g_snake_head
    g_snake_head.direction = "up"

def go_down():
    global g_snake_head
    g_snake_head.direction = "down"

def go_left():
    global g_snake_head
    g_snake_head.direction = "left"

def go_right():
    global g_snake_head
    g_snake_head.direction = "right"

def pause():
    global g_snake_head
    g_snake_head.direction = "stop"

def move(part):
    if part.direction == "up":
        y = part.ycor()
        part.sety(y + 20)
    
    if part.direction == "down":
        y = part.ycor()
        part.sety(y - 20)

    if part.direction == "left":
        x = part.xcor()
        part.setx(x - 20)

    if part.direction == "right":
        x = part.xcor()
        part.setx(x + 20)
    g_game_screen.update()

def snake_body_move():
    global g_snake_body
    global g_body_id
    global g_track
    head_x = g_snake_head.xcor()
    head_y = g_snake_head.ycor()
    g_snake_body.goto(head_x,head_y)
    g_snake_body.clearstamp(g_body_id[-1])
    n = g_snake_body.stamp()
    g_body_id.insert(0,n)
    g_body_id.pop()
    g_snake_body.goto(g_track[-1])

def snake_head_move():
    global g_snake_head
    global g_track
    global g_decelerate_time
    global g_time_rate
    global g_game_screen
    touch_screen_boundary(g_snake_head)
    if g_snake_head.direction != "stop":
        snake_body_move()
        move(g_snake_head)
        determine_win()

        g_track.insert(0,g_snake_head.pos())
        eat_food()

        # Check how many times the snake still needs to decelerate
        if g_decelerate_time != 0:
            g_decelerate_time -= 1
        else:
            # No need to decelerate again, then back to fast velocity
            g_time_rate = 300
            g_track.pop()
            # Previously the tail sticks. Now pop it then it can move forward.
    g_game_screen.ontimer(snake_head_move,g_time_rate)

def eat_food():
    global g_food
    global g_snake_head
    global g_eaten_food
    global g_body_id
    global g_snake_body
    global g_time_rate
    global g_decelerate_time
    for i in range(9):
        food = g_food[i]
        if g_snake_head.distance(food) <= 20:
            food.clear()
            food.goto(2000,2000)
            # After clear the food, there still exists a turtle. 
            # When snake passes the location, it will still lengthen the body
            # So after clearing it, we should also move it far far away
            g_eaten_food.append(i + 1)

            # Extends as the value of the food item number
            t = 0
            while t < i+1:
                s = g_snake_body.stamp()
                g_body_id.append(s)
                t += 1
            g_time_rate = 500

            # As the tail is being extended, the movement of the snake will slow down
            g_decelerate_time += i + 1
            
def monster_move():
    global g_end
    global g_monster
    global g_track
    global g_contact_monster
    global g_game_screen
    if g_end == False:
        monster_direction()
        touch_screen_boundary(g_monster)
        if g_monster.direction != "stop":
            move(g_monster)
        
        # Calculate the monster snake_body collisions
        for item in g_track:
            if g_monster.distance(item) <= 20:
                g_contact_monster += 1
        
        # Set the monster velocity to be a suitable value
        monster_rate = random.randint(700,1100)
        determine_lose()
        g_game_screen.ontimer(monster_move,monster_rate)

def start_game(x,y):
    # The function onclick calls should have 2 parameters x,y
    # x, y represents the locations where the mouse clicks
    g_game_screen.onclick(None)
    # Use None to unbind the onclick and start_game function
    g_pen.clear()
    snake_food()
    monster_move()
    snake_head_move()
    screen_title()

def main():
    configureScreen()
    configurePen()
    introduction()
    configureSnake()
    configureMonster()
    g_game_screen.listen()
    g_game_screen.onclick(start_game)
    g_game_screen.mainloop()

main()