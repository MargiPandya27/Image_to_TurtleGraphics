import google.generativeai as genai

import os

def eval(model, ref_image, screenshot_image):
    

    # Send prompt + images
    response = model.generate_content([
        "You're comparing two images. The first is the reference (real image), and the second is a turtle graphics drawing. \
        Describe the main visual differences between them concisely, what has to be modified, deleted: focus on shape, position, size, color, or missing elements as compared to the original image.",
        ref_image,
        screenshot_image
    ])


    # Print response
    return response.text
