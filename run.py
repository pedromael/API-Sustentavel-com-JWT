from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from app.config import Config
from app.database import get_db, close_connection, init_db
from app.routes.auth import auth_bp
from app.routes.actions import actions_bp

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa extensões
JWTManager(app)
CORS(app, supports_credentials=True)

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Registra os Blueprints das rotas
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(actions_bp, url_prefix="/actions")

@app.route("/")
def home():
    return {"message": "API de Ações Sustentáveis está no ar!"}

@app.teardown_appcontext
def teardown_db(exception):
    close_connection(exception)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=8000)
