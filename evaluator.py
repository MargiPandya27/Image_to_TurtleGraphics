import google.generativeai as genai

import os

def eval(model, ref_image, screenshot_image):
    

    # Send prompt + images
    response = model.generate_content([
    "You're comparing two images. The first is a real reference image, and the second is a turtle graphics drawing done in Python. \
    Your task is to describe only the key visual differences between the two images, such as missing shapes, incorrect positions, colors, or orientations. \
    Do not mention complex visual elements like shading, textures, lighting, or fine-grained patterns that are hard to replicate with turtle graphics. \
    Keep the feedback concise, practical, and directly usable to help correct the turtle drawing to better match the reference image. \
    Avoid vague statements and only mention corrections that could realistically be implemented using Python turtle (e.g., 'add more petals', 'change flower center color to yellow'). check the position and size of the circle at the center. ",
        ref_image,
        screenshot_image
    ])


    # Print response
    return response.text
