import server
from aiohttp import web

IMAGE_URLS = [
    "https://plus.unsplash.com/premium_photo-1752155109947-539988d49e5d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxmZWF0dXJlZC1waG90b3MtZmVlZHwyfHx8ZW58MHx8fHx8"
]

@server.PromptServer.instance.routes.get("/pin_grid_images")
async def get_pin_grid_images(request):
    return web.json_response(IMAGE_URLS)

from .pin_grid_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
