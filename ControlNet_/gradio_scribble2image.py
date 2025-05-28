import os
import cv2
import einops
import numpy as np
import torch
import random
from PIL import Image

from pytorch_lightning import seed_everything
from annotator.util import resize_image, HWC3
from cldm.model import create_model, load_state_dict
from cldm.ddim_hacked import DDIMSampler

# Set up model and sampler
model = create_model('ControlNet_/models/cldm_v15.yaml').cpu()
model.load_state_dict(load_state_dict('ControlNet_/models/control_sd15_scribble.pth', location='cuda'), strict=False)
model = model.cuda()
ddim_sampler = DDIMSampler(model)

def process(input_image, prompt, a_prompt, n_prompt, num_samples, image_resolution,
            ddim_steps, guess_mode, strength, scale, seed, eta):
    with torch.no_grad():
        img = resize_image(HWC3(input_image), image_resolution)
        H, W, C = img.shape

        detected_map = np.zeros_like(img, dtype=np.uint8)
        detected_map[np.min(img, axis=2) < 127] = 255

        control = torch.from_numpy(detected_map.copy()).float().cuda() / 255.0
        control = torch.stack([control for _ in range(num_samples)], dim=0)
        control = einops.rearrange(control, 'b h w c -> b c h w').clone()

        if seed == -1:
            seed = random.randint(0, 65535)
        seed_everything(seed)

        cond = {"c_concat": [control], "c_crossattn": [model.get_learned_conditioning([prompt + ', ' + a_prompt] * num_samples)]}
        un_cond = {"c_concat": None if guess_mode else [control], "c_crossattn": [model.get_learned_conditioning([n_prompt] * num_samples)]}
        shape = (4, H // 8, W // 8)

        model.control_scales = [strength * (0.825 ** float(12 - i)) for i in range(13)] if guess_mode else ([strength] * 13)
        samples, _ = ddim_sampler.sample(ddim_steps, num_samples,
                                         shape, cond, verbose=False, eta=eta,
                                         unconditional_guidance_scale=scale,
                                         unconditional_conditioning=un_cond)

        x_samples = model.decode_first_stage(samples)
        x_samples = (einops.rearrange(x_samples, 'b c h w -> b h w c') * 127.5 + 127.5).cpu().numpy().clip(0, 255).astype(np.uint8)

        results = [x_samples[i] for i in range(num_samples)]
    return [255 - detected_map] + results


# ------------------
# MAIN EXECUTION
# ------------------

if __name__ == '__main__':
    # Input parameters
    input_path = '/content/drive/MyDrive/CSE_252D/Image_to_TurtleGraphics/images/beach.jpg'    # Update with your input path
    output_dir = './output'       # Output directory
    os.makedirs(output_dir, exist_ok=True)

    # Load image
    input_image = np.array(Image.open(input_path).convert("RGB"))

    # Set parameters
    prompt = "a cute cat"
    a_prompt = "best quality, extremely detailed"
    n_prompt = "lowres, bad anatomy, blurry, cropped"
    num_samples = 1
    image_resolution = 512
    ddim_steps = 20
    guess_mode = False
    strength = 1.0
    scale = 9.0
    seed = 1234
    eta = 0.0

    # Run inference
    outputs = process(
        input_image, prompt, a_prompt, n_prompt, num_samples, image_resolution,
        ddim_steps, guess_mode, strength, scale, seed, eta
    )

    # Save output images
    Image.fromarray(outputs[0]).save(os.path.join(output_dir, "scribble_map.png"))
    for idx, img in enumerate(outputs[1:]):
        Image.fromarray(img).save(os.path.join(output_dir, f"generated_{idx+1}.png"))

    print("✅ Output saved in:", output_dir)