import torch
from PIL import Image
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from diffusers import UniPCMultistepScheduler
import numpy as np

def get_pipeline():
  # 1. Configuration
  MODEL_ID = "runwayml/stable-diffusion-v1-5"
  CONTROLNET_ID = "lllyasviel/sd-controlnet-scribble"
  DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

  # 2. Load ControlNet model
  controlnet = ControlNetModel.from_pretrained(
      CONTROLNET_ID,
      torch_dtype=torch.float16,
  ).to(DEVICE)

  # 3. Load Stable Diffusion + ControlNet pipeline
  pipe = StableDiffusionControlNetPipeline.from_pretrained(
      MODEL_ID,
      controlnet=controlnet,
      safety_checker=None,
      torch_dtype=torch.float16,
  ).to(DEVICE)
  # 4. Use a multistep scheduler for faster, higher-quality results
  pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
  
  return pipe 

# 5. Load and preprocess your scribble image (e.g., a black stroke on white background)
def load_scribble(path, size=(512, 512)):
    image = Image.open(path).convert("RGB").resize(size)
    arr = np.array(image).astype(np.float32) / 255.0
    gray = np.mean(arr, axis=2)
    scribble = Image.fromarray((gray * 255).astype(np.uint8))
    return scribble
