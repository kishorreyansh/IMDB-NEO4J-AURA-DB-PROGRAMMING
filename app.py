from flask import Flask, Response, jsonify, request
from neo4j import GraphDatabase

#For Mac use ssc and for Windows use +s
driver = GraphDatabase.driver(
    uri="neo4j+ssc://d9d1a978.databases.neo4j.io",
    auth=("neo4j", "1gOLsQxdm8hGKiX0NvRSJwM1ZMLONJvQ_KX_TIPgIy8"),
)

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    return "<h1 style='text-align: center'>Welcome to IMDB Programming Assignment<h1>"

# 1. Insert the new movie information and show using POST API 
@app.route("/imdb", methods=["POST"])
def insert_movie():
    session = driver.session()
    try:
        input_movie = request.json
        dynamic_generate_string = (
            "{" + ", ".join([f"{key} : ${key}" for key in input_movie.keys()]) + "}"
        )
        query = f"""CREATE (im:Movie {dynamic_generate_string}) RETURN im"""
        result = session.run(query, **input_movie)
        single_movie = result.single()
        if single_movie is None:
            return Response(
                "Unable to create movie ", status=500, mimetype="application/json"
            )
        return Response(
            "Movie inserted successfully !!", status=200, mimetype="application/json"
        )
    except Exception as ex:
        print("Exception")

# # 2. Update the movie information using title. (By update only title, description, and rating)
@app.route("/imdb/<string:title>", methods=["PATCH"])
def patch_movie(title):
    session = driver.session()
    try:
        request_params = request.json
        dynamic_update_movie = ", ".join(
            [f"um.{key} = ${key}" for key in request_params.keys()]
        )
        query = f"""MATCH (um:Movie {{title: $title}}) SET {dynamic_update_movie} RETURN um"""
        result = session.run(query,  **request_params)
        updated_movie = result.single()
        if updated_movie is None:
            return Response(
                "Movie '" + title + "' is not found", status=404, mimetype="application/json"
            )
        return jsonify(dict(updated_movie["um"]))
    except Exception as ex:
        print(ex)
        return Response("Unable to Update '" + title + "' Movie", status=500, mimetype="application/json")
    
# # 3. Delete the movie information using title using DELETE API
@app.route("/imdb/<string:title>", methods=["DELETE"])
def delete_movie(title):
    session = driver.session()
    try:
        query = """MATCH (dm:Movie{title:$title}) DETACH DELETE dm"""
        results = session.run(query, title=title)
        return Response(
            "Movie Deleted Successfully", status=200, mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response("Unable to delete '" + title + "' movie ", status=500, mimetype="application/json")

# 4. Retrieve all the movies in database. using GET API
@app.route("/imdb", methods=["GET"])
def imdb():
    session = driver.session() #setting up the neo4j Database Connection
    query = """MATCH (m:Movie) RETURN m"""
    try:
        #we are executing above cypher query to retrieve all films from neo4j database
        results = session.run(query)
        # Empty list to store records
        movies = []
        for record in results:
            node = record["m"]
            # we are converting node object to dictonary
            node_dict = dict(node)
            movies.append(node_dict)
        # we are converting dictonary into JSON format
        return jsonify(movies)
    except Exception as ex:
        print("Exception", ex)
        response = Response(
            "Unable to fetch Movies !!", status=500, mimetype="application/json"
        )
        return response

# # 5. Display the movie’s details includes actors, directors and genres using title using GET API
@app.route("/imdb/<string:title>", methods=["GET"])
def movie_by_title(title):
    session = driver.session()
    query = """MATCH (n:Movie{title:$title}) RETURN n"""
    try:
        #we are executing above cypher query to retrieve all characters from neo4j database
        results = session.run(query,title=title)
        movie = results.single()
        if movie:
            movie_details = dict(movie['n'])
            return jsonify(movie_details)
        else:
            return Response(
                f"Movie '{title}' not found", status=404, mimetype="application/json"
            )
    except Exception as ex:
        print("Exception", ex)
        response = Response(
            "Unable to Fetch '" + title + "' movie !!", status=500, mimetype="application/json"
        )
        return response

if __name__ == "__main__":
    app.run(port=5000, debug=True)