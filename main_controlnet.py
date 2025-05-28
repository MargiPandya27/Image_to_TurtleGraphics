import google.generativeai as genai
from code_generator import code_generator
from parse import extract_code_from_output
from evaluator import eval
from corrector import read_file, get_corrected_code
import sys
sys.path.append('/content/drive/MyDrive/CSE_252D/Image_to_TurtleGraphics/ControlNet_')
from gradio_scribble2image import process

import subprocess
from PIL import Image
from PIL import EpsImagePlugin
import turtle
import os
import numpy as np
from corrector_controlnet import get_generated_code_from_images



# --- Configure Ghostscript for Pillow EPS conversion ---
EpsImagePlugin.gs_windows_binary = r"C:\Program Files\gs\gs10.05.1\bin\gswin64c.exe"

# --- Configure Gemini API ---
genai.configure(api_key="GOOGLE_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

# Extract image bytes
image_path = "images/sunflower.jpg"
with open(image_path, "rb") as f:
    image_bytes = f.read()
ref_image = Image.open(image_path)

# Initial code generation
response = code_generator(model, image_bytes)
clean_code = extract_code_from_output(response)

current_code_file = "extracted_code.py"
with open(current_code_file, "w") as f:
    f.write(clean_code)

input_path = '/content/drive/MyDrive/CSE_252D/Image_to_TurtleGraphics/images/beach.jpg'    # Update with your input path
output_dir = './output'       # Output directory
os.makedirs(output_dir, exist_ok=True)

# Load image
input_image = np.array(Image.open(input_path).convert("RGB"))

# Set parameters
prompt = "a distorted realistic sunflower, irregular petals, abstract shape, surreal style"
a_prompt = "realistic textures, natural colors, best quality, slightly surreal, painterly"
n_prompt = "symmetrical, perfect shape, sharp geometry, lowres, blurry, cropped"

num_samples = 1
image_resolution = 512
ddim_steps = 20
guess_mode = False
strength = 1.0
scale = 9.0
seed = 1234
eta = 0.0

# Run inference
outputs = process(
    input_image, prompt, a_prompt, n_prompt, num_samples, image_resolution,
    ddim_steps, guess_mode, strength, scale, seed, eta
)

# Save output images
Image.fromarray(outputs[0]).save(os.path.join(output_dir, "scribble_map.png"))
for idx, img in enumerate(outputs[1:]):
    Image.fromarray(img).save(os.path.join(output_dir, f"generated_{idx+1}.png"))

print("✅ Output saved in:", output_dir)


original_img_path = "/content/drive/MyDrive/CSE_252D/Image_to_TurtleGraphics/images/beach.jpg"
turtle_img_path = "/content/drive/MyDrive/CSE_252D/Image_to_TurtleGraphics/output/generated_1.png"

code = read_file("extracted_code.py")

generated_code = get_generated_code_from_images(model, code, original_img_path, turtle_img_path)

with open("corrected_output.py", "w", encoding="utf-8") as f:
    f.write(generated_code)
