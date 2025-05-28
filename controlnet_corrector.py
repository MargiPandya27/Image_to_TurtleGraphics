import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import base64

# === SETUP GOOGLE GENERATIVE AI ===
os.environ["GOOGLE_API_KEY"] = "AIzaSyB8IeHPkLNjRnrmIi6Js-EjWddQsMx_7gY"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# === Create Model Instance ===
model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # or "gemini-1.5-flash"

# === Helper: Load and encode image for Gemini ===
def load_image_for_gemini(image_path):
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()
    return Image.open(BytesIO(image_bytes))

# === Function to Extract Python Code Block from Response ===
def extract_code_from_output(response_text):
    import re
    code_blocks = re.findall(r"```(?:python)?(.*?)```", response_text, re.DOTALL)
    return code_blocks[0].strip() if code_blocks else response_text.strip()

# === Main Function: Generate Turtle Code from Image Pair ===
def get_generated_code_from_images(model, original_code, original_image_path, turtle_output_path):
    # Load both images
    original_image = load_image_for_gemini(original_image_path)
    turtle_image = load_image_for_gemini(turtle_output_path)

    prompt = (
        "Compare the two images: the first one is the real image, the second one is the turtle-rendered image. "
        "Below is the original code that generated the second image. "
        "Fix the code to include the missing parts from the real image or correct mistakes. "
        "Don't explain anything, just return the full corrected Python turtle code inside triple backticks. "
        "Add `turtle.done()` at the end of the script.\n\n"
        "Original code:\n"
        "```python\n"
        f"{original_code}\n"
        "```"
    )


    response = model.generate_content(
        [prompt, original_image, turtle_image],
        generation_config={"temperature": 0.3, "max_output_tokens": 2048}
    )

    return extract_code_from_output(response.text)


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# === USAGE EXAMPLE ===
original_img_path = "/content/drive/MyDrive/CSE_252D/Image_to_TurtleGraphics/images/beach.jpg"
turtle_img_path = "/content/drive/MyDrive/CSE_252D/Image_to_TurtleGraphics/ControlNet_/output/generated_1.png"

code = read_file("extracted_code.py")

generated_code = get_generated_code_from_images(model, code, original_img_path, turtle_img_path)

with open("corrected_output.py", "w", encoding="utf-8") as f:
    f.write(generated_code)