from flask import Flask, render_template
from modules import modules


def test_index():
    app = Flask(__name__, template_folder="../templates")

    @app.route("/")
    def index():
        hello = modules.hello()
        content = modules.content()
        return render_template("index.html", hello=hello, content=content)

    app.testing = True
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
