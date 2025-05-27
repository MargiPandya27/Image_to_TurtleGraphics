import os
import google.generativeai as genai
from parse import extract_code_from_output


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_corrected_code(model, code: str, feedback: str) -> str:
    prompt = f"""
        You're a Python Turtle Graphics expert helping debug and improve turtle-based drawing code. Firstly, understand the feedback provided below given by the evaluator \
        and identify what parts of the original code need to be modified. If no changes are necessary, simply rewrite the original code.
        
        Feedback:
        {feedback}
        ---

        The original code:
        ```python
        {code}

        Import all the necessary libraries and ensure the code is bug free. Please return the corrected code ONLY, inside triple backticks. Add code to inject EPS saving into the code itself with file name as output1.eps:
        canvas = turtle.getcanvas()
        canvas.postscript(file="output1.eps") in the end. \
        Note: you can generate new code if the output is not good at all.
        """
    
    response = model.generate_content(prompt)
    return extract_code_from_output(response.text)