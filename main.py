from routes.application import app
from routes.routes import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)