import google.generativeai as genai

import json


def code_generator(model, image_bytes):
    prompt = f"""
            User: we will create a flower with more intricate petals and leaves. The petals have different shapes and curves and we will add green leaves around the flower to enhance its appearance.
            Assistant: 
            # Draw a Sunflower in Python Using Turtle

            # import math and turtle
            import math
            import turtle

            tina = turtle.Turtle()
            tina.shape("turtle")
            tina.color("black")
            tina.speed(0)

            def drawSunflower(t, numseeds, numpetals, angle, cspread):
                t.fillcolor("orange")
                phi = angle * (math.pi / 180.0)
            
                for i in range (numseeds + numpetals):
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

                if i <  numseeds:
                    t.stamp()
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

            drawSunflower(tina, 160, 40, 137.508, 4)

            tina.hideturtle()

            User: Take the given image and generate the turtle code to generate the turtle graphics. 

            Make sure that the order of all the object are correct so none of them overlap. Generate only the code.  Add code to inject EPS saving into the code itself with file name as output.eps:
            canvas = turtle.getcanvas()
            canvas.postscript(file="output.eps") in the end. 
            
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


