import math
import turtle

tina = turtle.Turtle()
tina.shape("turtle")
tina.color("black")
tina.speed(0)

def drawSunflower(t, numseeds, numpetals, angle, cspread):
    t.fillcolor("orange")  #changed to orange for the center
    phi = angle * (math.pi / 180.0)

    for i in range(numseeds + numpetals):
        # figure out the next x, y position
        r = cspread * math.sqrt(i)
        theta = i * phi
        x = r * math.cos(theta)
        y = r * math.sin(theta)

        # move the turtle and orient it correctly
        t.penup()
        t.goto(x, y)
        t.setheading(i * angle)
        t.pendown()

        if i < numseeds:
            t.dot(3, "black") # Draw seeds as black dots
        else:
            drawPetal(t)

def drawPetal(t):
    t.fillcolor("yellow")
    t.begin_fill()
    t.right(20)
    t.forward(70)
    t.left(40)
    t.forward(70)
    t.left(140)
    t.forward(70)
    t.left(40)
    t.forward(70)
    t.end_fill()

# Draw the Sunflower
drawSunflower(tina, 250, 30, 137.508, 7)


# Draw leaves (example - adjust positions and shapes as needed)
tina.penup()
tina.goto(-100,-100)
tina.pendown()
tina.fillcolor("green")
tina.begin_fill()
for _ in range(3):
    tina.forward(50)
    tina.left(120)
tina.end_fill()

tina.penup()
tina.goto(100,-100)
tina.pendown()
tina.fillcolor("green")
tina.begin_fill()
for _ in range(3):
    tina.forward(50)
    tina.left(120)
tina.end_fill()



tina.hideturtle()

canvas = turtle.getcanvas()
canvas.postscript(file="output.eps")