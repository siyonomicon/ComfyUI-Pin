import server
from aiohttp import web
import requests
import os
import urllib3
import re
from dotenv import load_dotenv

load_dotenv()
print(f"My module name is: {__name__}")

@server.PromptServer.instance.routes.get("/pinterest_data")
async def get_pinterest_data(request):
    pinterest_cookie = os.getenv("PINTEREST_COOKIE")
    headers = {
        "Host": "id.pinterest.com",
        "Cookie": pinterest_cookie,
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "referer": "https://id.pinterest.com/",
    }
    url = "https://id.pinterest.com/"
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        html_content = response.text
        
        # Regex to find img tags with elementtiming="grid-non-story-pin-image-homefeed" and extract src
        # This regex looks for:
        # <img
        #   .*? (any characters non-greedy)
        #   elementtiming="grid-non-story-pin-image-homefeed" (the exact attribute)
        #   .*? (any characters non-greedy)
        #   src="(.*?)" (captures the content of the src attribute)
        #   .*? (any characters non-greedy)
        # > (closing tag)
        pattern = r'<img(?=[^>]*elementtiming="grid-non-story-pin-image-homefeed")[^>]*src="([^"]+)"[^>]*>'
        image_srcs = re.findall(pattern, html_content)
        
        return web.json_response(image_srcs)
    except requests.exceptions.RequestException as e:
        return web.Response(text=f"Error fetching data: {e}", status=500)


from .pin_grid_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS',  'WEB_DIRECTORY']
