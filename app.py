from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from database.db import initialize_db
from flask_restful import Api

from resources.errors import errors

app = Flask(__name__)
CORS(app)
app.config.from_envvar('ENV_FILE_LOCATION')
mail = Mail(app)

@app.route('/', methods=['GET'])
def index():
    return {"msg":"home page"}
    
    
from resources.routes import initialize_routes

api = Api(app, errors=errors)


bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/movie-api'
}

initialize_db(app)
initialize_routes(api)






