from flask import Flask
from flask_cors import CORS

from routes.predict_routes import predict_bp
from routes.indicator_routes import indicator_bp
from routes.utility_routes import utility_bp
from routes.sentiment_routes import sentiment_bp



app = Flask(__name__)
CORS(app)


app.config["PROPAGATE_EXCEPTIONS"] = True

# Register routes
app.register_blueprint(predict_bp)
app.register_blueprint(indicator_bp)
app.register_blueprint(utility_bp)
app.register_blueprint(sentiment_bp)





@app.route("/")
def home():
    return {"status": "Backend Running"}

if __name__ == "__main__":
    app.run(debug=True, port=8000)

