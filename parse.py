
import re

def extract_code_from_output(raw_output):
    lines = raw_output.splitlines()
    code_lines = []

    inside_code_block = False

    for line in lines:
        # Detect start or end of code block (markdown style)
        if line.strip().startswith("```python"):
            inside_code_block = True
            continue
        elif line.strip().startswith("```") and inside_code_block:
            inside_code_block = False
            continue

        # Skip shell prompts (e.g., PS C:\..., >>>)
        if re.match(r"^(>>>|\.\.\.|PS\s|Traceback)", line.strip()):
            continue

        # Add line if inside a code block or if it looks like valid code
        if inside_code_block or re.match(r"^\s*(import|def|class|#|from|\w+ ?=|for |while |if |else|elif|try|except|with|return|print|turtle\.)", line):
            code_lines.append(line)

    return "\n".join(code_lines)

