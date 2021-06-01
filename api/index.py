from PIL import Image as pil_image, ImageFont as pil_font, ImageDraw as pil_draw
from http.server import BaseHTTPRequestHandler
from base64 import encodebytes
import requests
import io
import os

sh = "500"
sw = "500"
userId = os.environ['userId']
img_name = "im_quote.png"
sh = int(sh) * 2
sw = int(sw) * 2
userId = userId

bewise_url = "https://us-central1-bewise-forgr.cloudfunctions.net/quote"
bewise_url_query = f"{bewise_url}?userId={userId}&width={sw}&heigth={sh}"
color = "rgb(255, 255, 255)"
color_auth = "rgb(223, 153, 216)"


def draw_image(quote, author):
    shape = [(20, 20), (sw - 20, sh - 20)]

    img = pil_image.new("RGB", (sw, sh), color=(255, 255, 255, 1))

    img1 = pil_draw.Draw(img)
    img1.rectangle(shape, fill="#4b279b")
    fnt = pil_font.truetype("AvenirLTPro-Roman.ttf", 44)
    draw = pil_draw.Draw(img)
    textwidth, textheight = draw.textsize(quote, font=fnt)

    lines = text_wrap(quote, fnt, sw * 0.6)
    line_height = textheight + 5
    y = (sh / 2) - ((line_height * len(lines)) / 2)
    for line in lines:
        twidth, theight = draw.textsize(line, font=fnt)
        tmp_x = (sw - twidth) / 2
        draw.text((tmp_x, y), line, fill=color, font=fnt)

        y = y + line_height

    y += 15
    twidth, theight = draw.textsize(author, font=fnt)
    tmp_x = (sw - twidth) / 2
    draw.text((tmp_x, y), author, fill=color_auth, font=fnt)


def text_wrap(text, font, max_width):
    lines = []
    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        words = text.split(" ")
        i = 0
        while i < len(words):
            line = ""
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines


def getBewise():
    r = requests.get(bewise_url_query)
    data = r.json()
    tags = data.get("tags", [])
    tags.append("full hd")
    quote = f"“{data.get('text')}.”"
    author = f"{data.get('author')} "
    pil_img = draw_image(quote, author)
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format="PNG")
    encoded_img = encodebytes(byte_arr.getvalue()).decode("ascii")
    return encoded_img


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "image/png")
        self.end_headers()
        self.wfile.write(getBewise())
        return
