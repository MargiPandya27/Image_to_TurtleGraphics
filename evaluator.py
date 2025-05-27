import google.generativeai as genai

import os

def eval(model, ref_image, screenshot_image):
    

    # Send prompt + images
    response = model.generate_content([
        "You're comparing two images. The first is the reference (real image), and the second is a turtle graphics drawing done in Python. \
        Concisely describe any major discrepancies between the original image and the generated graphic, focusing on what should be added, \
        deleted, or modified to try and make the graphic representation closer to the actual image. Keep in mind the limitations of drawing \
        with such a software (DO NOT ASK for minute details like texture, shading, variation in size and color, complicated patterns etc). \
        Keep the output as simple as possible while making sure it captures the overall theme of the original image.",
        ref_image,
        screenshot_image
    ])


    # Print response
    return response.text
