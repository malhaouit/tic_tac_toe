#!/usr/bin/env python3
"""
Database moudule for handling MongoDB connections within a Flask application.
"""
from pymongo import MongoClient
from flask import current_app, g


def initialize_db():
    """
    Initializes the MongoDB conncetion for the current request and stores the
    connected database in Flask's `g` context object, ensuring the connection
    is available throughout the request lifecycle.
    """
    # Connect to MongoDB using the URI in the Flask app configuration
    client = MongoClient(current_app.config['MONGO_URI'])
    # Store the connected database in Falsk's `g` object
    g.db = client.get_database()


def get_db():
    """
    Retrieves the MongoDB connection for the current request.
    """
    # Check if the database connection is already initialized in `g`
    if 'db' not in g:
        # If not, initialize the database connection
        initialize_db()

    # Return the MongoDB connection from `g`
    return g.db
