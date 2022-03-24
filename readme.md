#### setup virtual environment

> pip install --user pipenv

#### install flask

> pipenv install flask

#### To run flask enter pip env shell first

> pipenv shell
> python app.py

---

#### Working with json files and mock data

```python
from flask import Flask, jsonify, request
app = Flask(__name__)

# @app.route is called a decorator


@app.route('/', methods=['GET'])
def home_page():
    return {"hello": "world"}


movies = [
    {
        "name": "The Shawshank Redemption",
        "casts": ["Tim Robbins", "Morgan Freeman", "Bob Gunton", "William Sadler"],
        "genres": ["Drama"]
    },
    {
        "name": "The Godfather ",
        "casts": ["Marlon Brando", "Al Pacino", "James Caan", "Diane Keaton"],
        "genres": ["Crime", "Drama"]
    }
]


@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(movies)

# ADD MOVIES


@app.route('/movies', methods=['POST'])
def add_movie():
    movie = request.get_json()
    movies.append(movie)
    return {"id": len(movies)}, 201

# UPDATE MOVIE


@app.route('/movies/<int:index>', methods=['PUT'])
def update_movie(index):
    movie = request.get_json()
    movies[index] = movie
    return jsonify(movies[index]), 200

# DELETE MOVIE


@app.route('/movies/<int:index>', methods=['DELETE'])
def delete_movie(index):
    movies.pop(index)
    return "None", 200


app.run(debug=True)


```

---

#### Using MongoDb

> pipenv install flask-mongoengine

The jsonify is no longer needed, we Response instead

```python
from flask import Flask, request, Response
from database.db import initialize_db
from database.models import Movie

app = Flask(__name__)


# connect database
app.config['MONGO_SETTINGS'] ={
    'host':'mongodb://localhost/movie-api'
}

# initialize_db
initialize_db(app)

# @app.route is called a decorator


@app.route('/', methods=['GET'])
def home_page():
    return {"hello": "world"}



@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.objects().to_json()
    return Response(movies, mimetype='application/json' , status=200)

# ADD MOVIES


@app.route('/movies', methods=['POST'])
def add_movie():
    body = request.get_json()
    movie = Movie(**body).save()
    id = movie.id
    return {"id": str(id)}, 201

# UPDATE MOVIE


@app.route('/movies/<id>', methods=['PUT'])
def update_movie(id):
    body = request.get_json()
    Movie.objects().get(id=id).update(**body)
    return "", 200


# DELETE MOVIE


@app.route('/movies/<int:index>', methods=['DELETE'])
def delete_movie(id):
    Movie.objects.get(id=id).delete()
    return "", 200


app.run(debug=True)


```

---

#### Structuring Flask project

- Using Blueprint or Flask-restful

###### Using Blue Print

```python

from flask import Blueprint, Response, request
from database.models import Movie

movies = Blueprint('movies', __name__)

# @app.route is called a decorator

@movies.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.objects().to_json()
    return Response(movies, mimetype='application/json' , status=200)

# ADD MOVIES


@movies.route('/movies', methods=['POST'])
def add_movie():
    body = request.get_json()
    movie = Movie(**body).save()
    id = movie.id
    return {"id": str(id)}, 201

# UPDATE MOVIE


@movies.route('/movies/<id>', methods=['PUT'])
def update_movie(id):
    body = request.get_json()
    Movie.objects().get(id=id).update(**body) # ** is the spread operator
    return "", 200


# DELETE MOVIE


@movies.route('/movies/<int:index>', methods=['DELETE'])
def delete_movie(id):
    Movie.objects.get(id=id).delete()
    return "", 200

# GET SINGLE MOVIE
@movies.route('/movies/<id>', methods=['GET'])
def get_movie(id):
    movies = Movie.objects.get(id=id).to_json()
    return Response(movies, mimetype="application/json", status=200)
```

---

#### Set env location in windows

> set ENV_FILE_LOCATION=./.env ====> window
> export ENV_FILE_LOCATION=./.env ====> bash
> use cmd for this
