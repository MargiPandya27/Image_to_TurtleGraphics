import os
import google.generativeai as genai
from parse import extract_code_from_output


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_corrected_code(model, code: str, feedback: str) -> str:
    prompt = f"""
        You are a Python Turtle Graphics expert. Your task is to review and improve the following turtle drawing code based on evaluator feedback. 

        ## Feedback:
        {feedback}

        ## Original Code:
        ```python
        {code}


       Instructions:
        Carefully read the feedback and understand what visual changes are needed.

        Modify the original code only to reflect those changes.

        Import all necessary libraries.

        Ensure the code is syntactically correct and runs without errors.

        At the very end of the code, inject this EPS export step:canvas = turtle.Screen.getcanvas()
            canvas.postscript(file="output1.eps"). 
        3. Don't use 'darkbrown' use brown color and not the shades. Try making the petals around the center. so the center should come first and then the petals around it. Also the center should be visible.

        """
    
    response = model.generate_content(prompt)
    return extract_code_from_output(response.text)