
import os
from PIL import Image
import numpy as np
import torch
from io import BytesIO
import requests

from . import IMAGE_URLS

class PinGridNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_images_from_urls"
    CATEGORY = "testing"

    def load_images_from_urls(self):
        image_list = []
        for url in IMAGE_URLS:
            try:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content)).convert('RGB')
                image_list.append(np.array(img))
            except Exception as e:
                print(f"Error loading image from {url}: {e}")

        if not image_list:
            return (torch.zeros(1, 256, 256, 3),)

        images_np = np.stack(image_list, axis=0)
        images_tensor = torch.from_numpy(images_np).float() / 255.0

        return (images_tensor,)

NODE_CLASS_MAPPINGS = {
    "PinGridNode": PinGridNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PinGridNode": "Pin Grid Node"
}
