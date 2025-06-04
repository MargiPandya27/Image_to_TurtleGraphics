# 🐢 Image-to-Turtle Graphics Generator

A multi-agent system that transforms input images into Python Turtle Graphics code by analyzing, rendering, evaluating, and iteratively correcting the output to closely match the original input.

---

## 🚀 Pipeline Overview

### 1. **Input and Analysis**
- User submits an image as input.
- A **Code Generator Agent** analyzes the image using computer vision techniques (e.g., edge detection, shape segmentation).
- Based on this analysis, the agent generates initial Turtle code to replicate the image.

### 2. **Scene Rendering**
- A **Scene Creator** runs the Turtle code.
- The generated Turtle scene is rendered and visualized.

### 3. **Evaluation and Correction**
- An **Evaluator Agent** compares the Turtle-rendered scene with the original image using similarity metrics like **SSIM** and feature comparison.
- If the result matches closely, the user is notified.
- Otherwise, feedback is sent to a **Corrector Agent**, which updates the Turtle code iteratively until an acceptable match is achieved.

---

## ⚙️ Installation & Setup

### 1. Install GhostScript
Download GhostScript from [here](https://ghostscript.com/releases/gsdnld.html) and provide the executable path when prompted or set it in your environment variables.

### 2. Get a Gemini API Key
Obtain an API key for Google Gemini (used for prompt engineering and code generation).

---

## 🛠️ How to Run

Clone the repository and run the main file:

```bash
git clone https://github.com/MargiPandya27/Image_to_TurtleGraphics.git
cd Image_to_TurtleGraphics
python main.py
```

---

## 📌 Model Architecture

<p align="center">
  <img src="https://github.com/MargiPandya27/Image_to_TurtleGraphics/blob/main/model_diagram.svg" width="400" alt="Model Diagram">
</p>
