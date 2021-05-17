import json
from flask import Flask, request

import characters as char
import meme_templates as templates

def load_config() -> dict:
    with open("conf/config.json") as config:
        return json.load(config)

config = load_config()

characters = char.generate_character_list(
    config.get("use_stored_characters", False)
)

print(characters["Phoenix Wright"])

app = Flask(__name__)

@app.route("/")
def home_page():
    return """
    <h1>Welcome to the Randomly Generated Ace Attorney Shitpost Hellhole!</h1>
    <h2><i>Home to only the highest quality of wildly overdone memes!</i></h2>

    <p>Try it out!</p>
    <ul>
        <li><a href="/quotes?num=5">"Incorrect" quotes</a></li>
        <li><a href="/mulaney?num=5">AA characters as John Mulaney quotes</a></li>
    </ul>
    """

@app.route("/<category>")
def quote_template(category: str):
    num_quotes = int(request.args.get('num', 1))
    return "<hr/>".join([templates.random_template(category, characters) for _ in range(num_quotes)])