from EdgeGPT import Chatbot, ConversationStyle
from quart import Quart, request, render_template, Response
import os
import json
from pathlib import Path


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
        return "Invalid conversation style, should be one of: " + ", ".join(ConversationStyle.__members__.keys()), 400

    bot = app.config["bot"]
    print("prompt: " + prompt, "style: " + conversation_style)
    resp = await bot.ask(prompt=prompt, conversation_style=style, wss_link="wss://sydney.bing.com/sydney/ChatHub")
    await bot.close()
    print(resp)
    # return json
    return resp


@app.route("/")
async def index():
    return await render_template("index.html")


def load_cookies(cookie_path: Path) -> list[dict[str, str]]:
    try:
        data = json.loads(Path(cookie_path).read_text())
    except FileNotFoundError as e:
        raise RuntimeError("Cookie file not found") from e

    new_format = []
    if isinstance(data, dict):
        if "Request Cookies" in data:
            data = data["Request Cookies"]
        new_format = []
        for k,v in data.items():
            new_format.append(dict(name=k, value=v))
    else:
        new_format = data
    return new_format


def setup():
    cookie_path = os.environ.get("COOKIE_PATH")
    if cookie_path is None:
        raise RuntimeError("COOKIES_PATH environment variable not set")
    cookies = load_cookies(Path(cookie_path))

    app.config["bot"] = Chatbot(cookies=cookies) # type: ignore

setup()

if __name__ == "__main__":
    app.run()
