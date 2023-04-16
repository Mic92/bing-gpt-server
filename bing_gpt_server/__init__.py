from EdgeGPT import Chatbot, ConversationStyle
from quart import Quart, request, render_template
import os

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


def main():
    cookie_path = os.environ.get("COOKIE_PATH")
    if cookie_path is None:
        raise RuntimeError("COOKIES_PATH environment variable not set")
    app.config["bot"] = Chatbot(cookies={}, cookiePath=cookie_path)
    app.run()

if __name__ == "__main__":
    main()
