import json
import os
from pathlib import Path
from typing import Any
from uuid import uuid4

from quart import Quart, render_template, request, send_from_directory, url_for

from BingImageCreator import ImageGenAsync
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

app = Quart(__name__)


@app.route("/api/chat")
async def chat():
    prompt = request.args.get("prompt")
    if prompt is None:
        return "No prompt provided", 400
    conversation_style = request.args.get("conversation_style", "creative")
    try:
        style = ConversationStyle[conversation_style]
    except KeyError:
        return (
            "Invalid conversation style, should be one of: "
            + ", ".join(ConversationStyle.__members__.keys()),
            400,
        )

    cookies = app.config["bot_cookies"]
    bot = Chatbot(cookies=cookies.raw)
    print("prompt: " + prompt, "style: " + conversation_style)
    resp = await bot.ask(
        prompt=prompt,
        conversation_style=style,
        wss_link="wss://sydney.bing.com/sydney/ChatHub",
    )
    await bot.close()
    print(resp)
    # return json
    return resp


@app.route("/images/<path:path>")
async def images(path):
    # serve ./images directory
    return await send_from_directory(app.config["images_dir"], path)


@app.route("/api/images")
async def async_image_gen():
    prompt = request.args.get("prompt")
    if prompt is None:
        return "No prompt provided", 400

    cookies = app.config["bot_cookies"]

    async with ImageGenAsync(cookies.u_cookie, False) as image_generator:
        images = await image_generator.get_images(prompt)
        uuid = uuid4()
        path = app.config["images_dir"] / f"{uuid}"

        await image_generator.save_images(images, output_dir=path)
        images = os.listdir(path)
        image_links = []

        for image in images:
            path = url_for("images", path=f"{uuid}/{image}")
            image_links.append(dict(url=f"{request.url_root}{path}"))
        return image_links


@app.route("/")
async def index():
    return await render_template("index.html")


class BotCookies:
    def __init__(self, data: Any) -> None:
        if isinstance(data, dict):
            if "Request Cookies" in data:
                data = data["Request Cookies"]
            self.raw = []
            try:
                self.u_cookie = data["_U"]
            except KeyError:
                raise RuntimeError("Cookie file does not contain _U cookie")

            for k, v in data.items():
                self.raw.append(dict(name=k, value=v))
        else:
            assert isinstance(data, list), "cookies file should be a list or dict"
            for pair in data:
                if pair["name"] == "_U":
                    self.u_cookie = pair["value"]
                    break
            else:
                raise RuntimeError("Cookie file does not contain _U cookie")
            self.raw = data


def load_cookies(cookie_path: Path) -> BotCookies:
    try:
        data = json.loads(Path(cookie_path).read_text())
    except FileNotFoundError as e:
        raise RuntimeError("Cookie file not found") from e
    return BotCookies(data)


def setup():
    cookie_path = os.environ.get("COOKIE_PATH")
    if cookie_path is None:
        raise RuntimeError("COOKIE_PATH environment variable not set")
    app.config["bot_cookies"] = load_cookies(Path(cookie_path))
    images_dir = Path(os.environ.get("IMAGES_DIR", "images"))
    images_dir.mkdir(exist_ok=True)
    app.config["images_dir"] = images_dir


setup()

if __name__ == "__main__":
    app.run()
