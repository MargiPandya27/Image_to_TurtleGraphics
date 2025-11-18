# Image-to-Turtle Graphics Generator

A sophisticated multi-agent AI system that transforms input images into Python Turtle Graphics code through intelligent analysis, iterative rendering, evaluation, and correction. The system uses computer vision, AI-powered code generation, and ControlNet for enhanced image processing.

<div align="center">
  <img src="https://raw.githubusercontent.com/MargiPandya27/Image_to_TurtleGraphics/main/model_diagram.svg" alt="Model Architecture" style="width:30%;height:20%;"/>
</div>



## Features

- **AI-Powered Code Generation**: Uses Google Gemini to analyze images and generate initial Turtle Graphics code
- **Iterative Improvement**: Multi-step evaluation and correction process for better accuracy
- **Computer Vision Integration**: Advanced image analysis using edge detection and shape segmentation
- **ControlNet Enhancement**: Optional ControlNet integration for improved image-to-code conversion
- **Automatic EPS/PNG Export**: Built-in support for high-quality image export
- **Multi-Image Support**: Works with various image types (flowers, landscapes, objects)

## Architecture Overview

The system consists of several interconnected components:

### Core Components

1. **Code Generator** (`code_generator.py`): Analyzes input images using AI and generates initial Turtle Graphics code
2. **Evaluator** (`evaluator.py`): Compares generated Turtle drawings with original images using similarity metrics
3. **Corrector** (`corrector.py`): Iteratively improves code based on evaluator feedback
4. **Scene Renderer** (`draw_and_save.py`): Executes Turtle code and exports results
5. **Parser** (`parse.py`): Extracts clean code from AI model outputs

### Advanced Features

- **ControlNet Integration** (`controlnet_scribble.py`): Uses ControlNet for enhanced image processing
- **Multi-iteration Pipeline**: Up to 5 iterations for optimal results
- **GhostScript Integration**: High-quality EPS to PNG conversion

## Prerequisites

### Required Software
- **Python 3.8+**
- **GhostScript**: Download from [ghostscript.com](https://ghostscript.com/releases/gsdnld.html)
- **CUDA-compatible GPU** (optional, for ControlNet acceleration)

### API Keys
- **Google Gemini API Key**: Required for AI-powered code generation

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MargiPandya27/Image_to_TurtleGraphics.git
   cd Image_to_TurtleGraphics
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure GhostScript**
   - Install GhostScript on your system
   - Update the path in `main.py` and `draw_and_save.py`:
     ```python
     EpsImagePlugin.gs_windows_binary = r"C:\Program Files\gs\gs10.05.1\bin\gswin64c.exe"
     ```

4. **Set up API Key**
   - Replace `"Create Your API"` in `main.py` with your actual Gemini API key
   - Or set it as an environment variable

## Usage

### Basic Usage

Run the main pipeline with an input image:

```bash
python main.py path/to/your/image.jpg
```

### Advanced Usage with ControlNet

For enhanced results using ControlNet:

```bash
python main_controlnet.py
```

### Example Workflow

1. **Input**: Provide an image (e.g., `images/sunflower.jpg`)
2. **Analysis**: AI analyzes the image structure and generates initial Turtle code
3. **Rendering**: Turtle code is executed and rendered
4. **Evaluation**: Generated drawing is compared with original image
5. **Correction**: Code is iteratively improved based on feedback
6. **Output**: Final optimized Turtle Graphics code and rendered image

## Project Structure

```
Image_to_TurtleGraphics/
├── main.py                 # Main execution pipeline
├── main_controlnet.py      # ControlNet-enhanced pipeline
├── code_generator.py       # AI-powered code generation
├── evaluator.py           # Image comparison and evaluation
├── corrector.py           # Code correction based on feedback
├── draw_and_save.py       # Turtle code execution and export
├── parse.py               # Code extraction utilities
├── controlnet_scribble.py # ControlNet integration
├── images/                # Sample input images
│   ├── sunflower.jpg
│   ├── rose.jpg
│   ├── daisy.jpg
│   ├── tulip.jpg
│   └── beach.jpg
├── output/                # Generated outputs
└── ControlNet_/           # ControlNet framework files
```

## Configuration

### GhostScript Path
Update the GhostScript binary path in these files:
- `main.py` (line 19)
- `draw_and_save.py` (line 6)

### API Configuration
Set your Gemini API key in:
- `main.py` (line 22)
- `main_controlnet.py` (line 25)

### ControlNet Settings
Modify ControlNet parameters in `controlnet_scribble.py`:
- Model IDs
- Device selection (CPU/GPU)
- Inference parameters

## Output Files

The system generates several output files:

- `extracted_code.py`: Initial AI-generated Turtle code
- `corrected_output{i}.py`: Iteratively improved code versions
- `output/output{i}.eps`: EPS format drawings
- `output/output{i}.png`: PNG format drawings
- `generated_image.png`: Final ControlNet-enhanced result

## Supported Image Types

The system works best with:
- **Flowers**: Sunflowers, roses, daisies, tulips
- **Simple Objects**: Geometric shapes, basic drawings
- **Landscapes**: Simple scenes with clear structures

## How It Works

### 1. Image Analysis
The AI analyzes the input image using computer vision techniques to identify:
- Shapes and contours
- Color patterns
- Spatial relationships
- Geometric structures

### 2. Code Generation
Based on the analysis, the AI generates Python Turtle Graphics code that:
- Replicates the identified shapes
- Matches color schemes
- Maintains spatial relationships
- Uses appropriate drawing techniques

### 3. Iterative Improvement
The system runs multiple iterations:
- Execute generated code
- Compare output with original
- Generate feedback on differences
- Correct code based on feedback
- Repeat until satisfactory match

### 4. ControlNet Enhancement (Optional)
For advanced processing:
- Convert Turtle output to scribble format
- Apply ControlNet for enhanced generation
- Generate improved artistic versions

## Troubleshooting

### Common Issues

1. **GhostScript Error**
   - Ensure GhostScript is properly installed
   - Verify the binary path in configuration files

2. **API Key Issues**
   - Check your Gemini API key is valid
   - Ensure proper API quota and permissions

3. **CUDA/GPU Issues**
   - Install appropriate CUDA drivers
   - Use CPU fallback if GPU unavailable

4. **Memory Issues**
   - Reduce image resolution for large images
   - Close other applications to free memory

### Performance Tips

- Use smaller images for faster processing
- Enable GPU acceleration for ControlNet features
- Adjust iteration count based on complexity needs



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



**Note**: This system works best with simple, well-defined images of flowers only. Complex photographs of other objects may require multiple iterations or manual adjustments for optimal results.
