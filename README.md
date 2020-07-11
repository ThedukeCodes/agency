### Capstone project - The Casting Agency

### Motivation

Final project for Full stack developer course.
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.
You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

### Installing Dependencies

# Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

# PIP Dependencies

Install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

# Key Dependencies

- [Flask] is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy] is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database.

- [Jose] JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

- [Gunicorn] is a stand-alone WSGI web application server. We'll use this to deploy the app on heroku server.

### Running the server

To run the server, execute:

```bash
source setup.sh
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Running setup.sh will set key environment variables which are AUTH0_DOMAIN, API_AUDIENCE, ALGORITHMS, DATABASE_URL.
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.
Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application. 

### Roles

Casting Assistant : Can view actors and movies
Casting Director : All permissions a Casting Assistant has and Add or delete an actor from the database, Modify actors or movies
Executive Producer : All permissions a Casting Director has and Add or delete a movie from the database

We use Auth0 service to assign roles to users.
To perform above tasks http request should consist of proper Authorization token.
It will help you understand how it works to read the codes of `test_api.py` 

### End points

It will also help you understand how end points work to read the codes of `test_api.py` 

GET '/actors'
- Fetches a dictionary of actors in which the keys are the id, name, age, gender and the values are the corresponding string or integer.

GET '/movies'
- Fetches a dictionary of actors in which the keys are the id, title, release_date and the values are the corresponding string or integer.

POST '/actors'
- POST a new actor which will require the name(string) and age(integer), gendr(string).
- This will add new row in the database and it will show the id of the created actor.

POST '/movies'
- POST a new move which will require the title(string) and release_date(integer).
- This will add new row in the database and it will show the id of the created movie.

DELETE '/actors/<int:actor_id>'
- Delete actor using a actor ID on the endpoint.
- This removal will persist in the database and it will show the id of the deleted actor.

DELETE '/movies/<int:movie_id>'
- Delete movie using a movie ID on the endpoint.
- This removal will persist in the database and it will show the id of the deleted movie.

PATCH '/actors/<int:actor_id>'
- Update actor using a actor ID on the endpoint.
- This require new name(string) and new age(integer), new gender(string).
- This will update existing row in the database and it will show the id of the updated actor.

PATCH '/movies/<int:movie_id>'
- Update movie using a movie ID on the endpoint.
- This require new title(string) and new release_date(integer).
- This will update existing row in the database and it will show the id of the updated movie.

### Testing
To run the tests, run
```
source setup.sh
python test_api.py
```

### Running the server on Heroku

API is hosted live at Heroku on `https://capstone-agency1.herokuapp.com/`

You can test endpoints described above with [Postman](https://getpostman.com). 
- Import the postman collection `capstone.postman_collection.json`
- Right-click the collection folder for assistant, director, and producer.
- Run the collection and test endpoints.
