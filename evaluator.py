import google.generativeai as genai

import os

def eval(model, ref_image, screenshot_image):
    

    # Send prompt + images
    response = model.generate_content([
        "You are comparing two images. The first is the reference (real image), and the second is a turtle graphics drawing done in Python.\
        Point out one or two major errors that might exist between the two images, ignoring finer details that would be difficult to \
        execute in a program (like texture, small details, etc.). Make sure you structure your output in such a way that someone reading \
        it could easily modify the program they wrote to generate the graphic. Keep your descriptions and advice short and concise ",
        ref_image,
        screenshot_image
    ])


    # Print response
    return response.text
