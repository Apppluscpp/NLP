from flask import Flask, render_template
from views import views
import os

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/views")

app.secret_key = "123"

if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
