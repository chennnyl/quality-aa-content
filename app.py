import json
import base64
from io import BytesIO
from flask import Flask, request

import characters as char
import meme_templates as templates
import image_macros as images

def load_config() -> dict:
    with open("conf/config.json") as config:
        return json.load(config)

def create_app():
    config = load_config()

    characters = char.generate_character_list(
        config.get("use_stored_characters", False)
    )

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
        <hr/>
        <footer>
            <p><i>Written and maintained by <a href="https://lynnux.org">Lynnux</a>. View the <a href="https://github.com/Spirati/quality-aa-content">source code</a> or talk to me on <a href="https://twitter.com/_lynnux">Twitter</a>!<i></p>
        </footer>
        """

    @app.route("/<category>")
    def quote_template(category: str):

        HOME_LINK = ["<a href=\"/\">Go home</a>"]

        if category.lower() in ("image",):
            image = images.generate_image_macro(characters)
            with BytesIO() as output:
                image.save(output, format="PNG")
                image_bytes = output.getvalue()
            
            encoded = base64.b64encode(image_bytes).decode()
            data_uri = 'data:image/png;base64,{}'.format(encoded)

            return "<hr/>".join(HOME_LINK + [f"<img src=\"{data_uri}\"/>"])

            
        num_quotes = int(request.args.get('num', 1))
        return "<hr/>".join(HOME_LINK + [templates.random_template(category, characters) for _ in range(num_quotes)])

    return app