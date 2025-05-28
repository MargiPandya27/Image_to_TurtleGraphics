import google.generativeai as genai

import json


def code_generator(model, image_bytes, query):
    prompt = f"""
            User: we will create a flower with more intricate petals and leaves. The petals have different shapes and curves and we will add green leaves around the flower to enhance its appearance.
            Assistant: # Draw a Sunflower in Python Using Turtle
            # Draw a Sunflower in Python Using Turtle
            import math
            import turtle


            def drawPhyllotacticPattern(turtle, t, petalstart, angle=120, size=2, cspread=4):
                # initialize position
                # turtle.pen(outline=1,pencolor="black",fillcolor="orange")
                turtle.color('black')
                turtle.fillcolor("orange")
                phi = angle * (math.pi / 180.0)
                xcenter = 0.0
                ycenter = 0.0

                # for loops iterate in this case from the first value until < 4, so
                for n in range(0, t):
                    r = cspread * math.sqrt(n)
                    theta = n * phi

                    x = r * math.cos(theta) + xcenter
                    y = r * math.sin(theta) + ycenter

                    # move the turtle to that position and draw
                    turtle.up()
                    turtle.setpos(x, y)
                    turtle.down()
                    # orient the turtle correctly
                    turtle.setheading(n * angle)
                    if n > petalstart - 1:
                        turtle.color("yellow")
                        drawPetal(turtle, x, y)
                    else:
                        turtle.stamp()


            def drawPetal(turtle, x, y):
                turtle.penup()
                turtle.goto(x, y)
                turtle.pendown()
                turtle.color('black')
                turtle.fillcolor('yellow')
                turtle.begin_fill()
                turtle.right(20)
                turtle.forward(70)
                turtle.left(40)
                turtle.forward(70)
                turtle.left(140)
                turtle.forward(70)
                turtle.left(40)
                turtle.forward(70)
                turtle.penup()
                turtle.end_fill()  # this is needed to complete the last petal

            tina = turtle.Turtle()
            tina.shape("turtle")
            tina.speed(0)  # make the turtle go as fast as possible
            drawPhyllotacticPattern(tina, 300, 120, 137.508)
            tina.penup()
            tina.forward(1000)
            tina._position = (150, -250)
            print(tina._position)
            tina._write('Danh Tran', align='left', font=("Arial", 20, "normal"))
            turtle.mainloop(). 

            User: {query}

            Make sure that the order of all the object are correct so none of them overlap. Generate only the code.  Add code to inject EPS saving into the code itself with file name as output.eps:
            1. canvas = turtle.Screen.getcanvas()
            2. canvas.postscript(file="output.eps") in the end. 
            3. Don't use 'darkbrown' use basic color and not the shades. Try making the petals around the center. so the center should come first and then the petals around it. Also the center should be visible.

            Assistant:

            """ 


    # Generate content using the model
    response = model.generate_content([
        prompt,
        {
            "mime_type": "image/jpeg",
            "data": image_bytes,
        }
    ])

    return response.text


