import google.generativeai as genai
from code_generator import code_generator
from parse import extract_code_from_output
from evaluator import eval
from corrector import read_file, get_corrected_code

import subprocess
from PIL import Image
from PIL import EpsImagePlugin
import turtle
import os

# --- Configure Ghostscript for Pillow EPS conversion ---
EpsImagePlugin.gs_windows_binary = r"C:\Program Files\gs\gs10.05.1\bin\gswin64c.exe"

# --- Configure Gemini API ---
genai.configure(api_key="YOUR_API_KEY")
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

MAX_REGEN_ITERS = 3
def exec_or_regen_code(eps_file, png_file, model, image_bytes, current_code_file, feedback, i, iteration=0):
    if iteration == MAX_REGEN_ITERS:
        subprocess.run([
            "python", "draw_and_save.py",
            current_code_file, eps_file, png_file
        ], check=True)
        
        return # this will cause subprocess to error out and program exits (or if success, continues on)
    
    try:
        subprocess.run([
            "python", "draw_and_save.py",
            current_code_file, eps_file, png_file
        ], check=True)
    except:
        print("Code failed to execute! Retrying generation...")
        print(f"Failed iteration {i}, rewriting {current_code_file}")
        if i == 0: # redo initial code generation
            response = code_generator(model, image_bytes)
            clean_code = extract_code_from_output(response)

            with open(current_code_file, "w") as f:
                f.write(clean_code)
        elif i >= 1: # feedback iteration
            code = read_file(current_code_file)  
            corrected_code = get_corrected_code(model, code, feedback)
            with open(current_code_file, "w", encoding="utf-8") as f:
                f.write(corrected_code)
        
        # recursively call again
        iteration += 1
        exec_or_regen_code(eps_file, png_file, model, image_bytes, current_code_file, feedback, i, iteration=iteration)
        

feedback = None
for i in range(3):  # Adjust as needed
    print(f"\n🔁 Iteration {i + 1}\n")
    eps_file = f"output/output{i}.eps"
    png_file = f"output/output{i}.png"

    exec_or_regen_code(eps_file, png_file, model, image_bytes, current_code_file, feedback, i, iteration=0)
    
    turtle_output = Image.open(png_file)
    print("🔍 Evaluating output...")
    feedback = eval(model, ref_image, turtle_output)

    code = read_file(current_code_file)  
    corrected_code = get_corrected_code(model, code, feedback)
    current_code_file = f"corrected_output{i + 1}.py"
    with open(current_code_file, "w", encoding="utf-8") as f:
        f.write(corrected_code)