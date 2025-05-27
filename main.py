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


MAX_ATTEMPTS = 3

def run_with_retries(model, image_bytes, initial_code_file):
    current_code_file = initial_code_file

    for attempt in range(1, MAX_ATTEMPTS + 1):
        eps_file = f"output/output{attempt - 1}.eps"
        png_file = f"output/output{attempt - 1}.png"

        try:
            # Try running the generated code
            subprocess.run([
                "python", "draw_and_save.py",
                current_code_file, eps_file, png_file
            ], check=True)
            return current_code_file, png_file  # success!

        except subprocess.CalledProcessError:
            # On failure, if this was the last attempt, propagate the error
            if attempt == MAX_ATTEMPTS:
                raise

            print(f"Iteration {attempt} failed — regenerating code and retrying...")

            # Generate a fresh batch of code
            response = code_generator(model, image_bytes)
            clean_code = extract_code_from_output(response)
            with open("extracted_code.py", "w", encoding="utf-8") as f:
                f.write(clean_code)

            # Update for the next iteration
            current_code_file = "extracted_code.py"

    # Should never get here
    raise RuntimeError("Exceeded maximum retry attempts")

# --- Usage in your loop ---
image_path = "images/sunflower.jpg"
with open(image_path, "rb") as f:
    image_bytes = f.read()
ref_image = Image.open(image_path)

# first code generation
initial_response = code_generator(model, image_bytes)
initial_code = extract_code_from_output(initial_response)
with open("extracted_code.py", "w", encoding="utf-8") as f:
    f.write(initial_code)

current_code_file = "extracted_code.py"
for i in range(3):
    print(f"\n🔁 Iteration {i + 1}\n")

    # run and possibly retry
    current_code_file, png_file = run_with_retries(model, image_bytes, current_code_file)

    # evaluate the output
    turtle_output = Image.open(png_file)
    print("🔍 Evaluating output...")
    feedback = eval(model, ref_image, turtle_output)

    # apply corrections
    code = read_file(current_code_file)
    corrected_code = get_corrected_code(model, code, feedback)
    current_code_file = f"corrected_output{i + 1}.py"
    with open(current_code_file, "w", encoding="utf-8") as f:
        f.write(corrected_code)