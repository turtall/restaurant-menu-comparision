from flask import Flask
from flask import request
from flask import jsonify, make_response, render_template
import numpy as np

from datetime import datetime, timezone
from db_table import db_table

app = Flask(__name__)

# function to get db connection of BAGAAN table


def get_bagaan_db_conn():
    db_schema = {
        "sn": "INT PRIMARY KEY",
        "name": "string",
        "price": "float",
    }
    return db_table("BAGAAN", db_schema)

# function to get db connection of JIMBU table


def get_jimbu_db_conn():
    db_schema = {
        "sn": "INT PRIMARY KEY",
        "name": "string",
        "price": "float",
    }
    return db_table("JIMBU", db_schema)

# create a route to get all the data from BAGAAN table
# this route will accept GET request and return all the data from BAGAAN table
# there will be a search parameter with key "name" which will be used to search the "name" column in the table
# if the search parameter is not provided, all the data will be returned
# if the search parameter is provided, then search the name column with the provided value and return the result
# search for partial match of the name column


@app.route('/bagaan', methods=['GET'])
def get_bagaan_data():
    bagaan_db = get_bagaan_db_conn()
    search_name = request.args.get('name')
    if search_name:
        data = bagaan_db.select(["name", "price", "image"], like={
                                "name": search_name})
    else:
        data = bagaan_db.select(["name", "price", "image"])
    return jsonify(data)

# do the same for /jimbu route


@app.route('/jimbu', methods=['GET'])
def get_jimbu_data():
    jimbu_db = get_jimbu_db_conn()
    search_name = request.args.get('name')
    if search_name:
        data = jimbu_db.select(["name", "price", "image"], like={
                               "name": search_name})
    else:
        data = jimbu_db.select(["name", "price", "image"])
    return jsonify(data)


@app.route('/')
def index():
    return render_template('index.html')


app.run(port=8080)
