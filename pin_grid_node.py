import os
from PIL import Image
import numpy as np
import torch
from io import BytesIO
import requests
import server
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()
print(f"My module name is: {__name__}")


# @server.PromptServer.instance.routes.post("/pin_grid_select_image")
# async def select_pin_grid_image(request):
#     data = await request.json()
#     Logger.metaclass.selected_image_url = data.get("imageUrl")
#     print(f"Selected image URL: {Logger.metaclass.selected_image_url}")
#     return web.json_response({"status": "success", "imageUrl": Logger.metaclass.selected_image_url})

class PinGridNode:
    selected_image_url = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "griwdikowad": ("STRING",)
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_images_from_urls"
    CATEGORY = "testing"
    OUTPUT_NODE = True

    def load_images_from_urls(self, griwdikowad):
        print(f"Loading image from wawa: {griwdikowad}")
        image_list = []
        try:
            response = requests.get(griwdikowad)
            img = Image.open(BytesIO(response.content)).convert('RGB')
            image_list.append(np.array(img))
        except Exception as e:
                print(f"Error loading image from {griwdikowad}: {e}")

        if not image_list:
            return (torch.zeros(1, 256, 256, 3),)

        images_np = np.stack(image_list, axis=0)
        images_tensor = torch.from_numpy(images_np).float() / 255.0

        return (images_tensor,)

NODE_CLASS_MAPPINGS = {
    "PinGridNode": PinGridNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PinGridNode": "Pin Grid Node",
}