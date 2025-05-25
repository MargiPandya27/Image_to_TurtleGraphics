# draw_and_save.py
import sys
import turtle
from PIL import Image, EpsImagePlugin

# Configure Ghostscript for EPS conversion
EpsImagePlugin.gs_windows_binary = r"C:\Program Files\gs\gs10.05.1\bin\gswin64c.exe"

code_file = sys.argv[1]
eps_file = sys.argv[2]
png_file = sys.argv[3]

with open(code_file, "r", encoding="utf-8") as f:
    code = f.read()
for end_call in ["turtle.done()", "turtle.exitonclick()", "turtle.bye()"]:
    code = code.replace(end_call, "")

exec(code)

canvas = turtle.getcanvas()
canvas.postscript(file=eps_file)
img = Image.open(eps_file)
img.save(png_file)
turtle.bye()
