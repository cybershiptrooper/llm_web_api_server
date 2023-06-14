from flask_ngrok import run_with_ngrok
from flask import Flask

app = Flask(__name__, static_folder="public")
# run_with_ngrok(app)

def run_application():
    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)
    # app.run()