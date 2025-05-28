import google.generativeai as genai

import json


def code_generator(model, image_bytes):
    prompt = f"""
            User: Using turtle graphics in python, draw an image of a black and yellow striped bumblebee that is floating through the sky.
            Generate only the code.
            Add code to inject EPS saving into the code itself with file name as output.eps:
            canvas = turtle.getcanvas()
            canvas.postscript(file="output.eps") in the end.
            
            Assistant: 
            # Necessary Imports
            import turtle

            # Setup screen
            screen = turtle.Screen()
            screen.setup(width=800, height=600)
            screen.bgcolor("skyblue")
            turtle.speed(0)
            turtle.hideturtle()

            # Draw body
            body = turtle.Turtle()
            body.hideturtle()
            body.penup()
            body.shape("circle")
            body.color("black", "yellow")
            body.shapesize(stretch_wid=3, stretch_len=5)
            body.goto(0, 0)
            body.stamp()

            # Draw black stripes
            stripe = turtle.Turtle()
            stripe.hideturtle()
            stripe.penup()
            stripe.shape("circle")
            stripe.color("black")
            stripe.shapesize(stretch_wid=3, stretch_len=1)
            for x in [-30, 0, 30]:
                stripe.goto(x, 0)
                stripe.stamp()

            # Draw head
            head = turtle.Turtle()
            head.hideturtle()
            head.penup()
            head.shape("circle")
            head.color("black")
            head.shapesize(stretch_wid=2, stretch_len=2)
            head.goto(-60, 0)
            head.stamp()

            # Draw eyes
            eye = turtle.Turtle()
            eye.hideturtle()
            eye.penup()
            for xpos in [-70, -50]:
                # white part
                eye.goto(xpos, 10)
                eye.color("white")
                eye.shapesize(stretch_wid=0.5, stretch_len=0.5)
                eye.stamp()
                # pupil
                eye.color("black")
                eye.shapesize(stretch_wid=0.2, stretch_len=0.2)
                eye.stamp()

            # Draw antennae
            ant = turtle.Turtle()
            ant.hideturtle()
            ant.penup()
            ant.color("black")
            ant.goto(-60, 20)
            ant.pendown()
            ant.setheading(120)
            ant.forward(40)
            ant.dot(8)
            ant.penup()
            ant.goto(-60, 20)
            ant.pendown()
            ant.setheading(60)
            ant.forward(40)
            ant.dot(8)

            # Draw wings
            wing = turtle.Turtle()
            wing.hideturtle()
            wing.penup()
            wing.shape("circle")
            wing.color("black", "lightblue")
            wing.shapesize(stretch_wid=3, stretch_len=2)
            for pos in [(-10, 60), (30, 60)]:
                wing.goto(pos)
                wing.stamp()

            # Save as EPS
            canvas = turtle.getcanvas()
            canvas.postscript(file="output.eps")

            turtle.done()


            User: Take the given image and generate the turtle code to generate the turtle graphics. 

            Try and match the generated image to the original image as closely as possible. 
            Generate only the code.  
            Add code to inject EPS saving into the code itself with file name as output.eps:
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


