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
genai.configure(api_key="AIzaSyDgXKQojjiZqdH468J6cP_ZZGedC49RGT4")
model = genai.GenerativeModel("gemini-1.5-flash")


# --- Load reference image once ---
image_path = "images/daisy.jpg"
with open(image_path, "rb") as f:
    image_bytes = f.read()
ref_image = Image.open(image_path)
os.makedirs("output", exist_ok=True)

query = "Similarly, Can you generate code to convert given flower in the image to turtle graphics?"

# --- Initial code generation from image ---
response = code_generator(model, image_bytes, query)
clean_code = extract_code_from_output(response)

with open("extracted_code.py", "w") as f:
    f.write(clean_code)

current_code_file = "extracted_code.py"

for i in range(5):  # Adjust as needed
    print(f"\n🔁 Iteration {i + 1}\n")
    eps_file = f"output/output{i}.eps"
    png_file = f"output/output{i}.png"

    # --- Run the drawing in a new subprocess ---
    subprocess.run([
        "python", "draw_and_save.py",
        current_code_file, eps_file, png_file
    ], check=True)

    # --- Evaluate against reference image ---
    turtle_output = Image.open(png_file)
    print("🔍 Evaluating output...")
    feedback = eval(model, ref_image, turtle_output)

    # --- Read current code again ---
    code = read_file(current_code_file)

    # --- Get corrected code ---
    corrected_code = get_corrected_code(model, code, feedback)

    # --- Save corrected code to new file ---
    current_code_file = f"corrected_output{i + 1}.py"
    with open(current_code_file, "w", encoding="utf-8") as f:
        f.write(corrected_code)
