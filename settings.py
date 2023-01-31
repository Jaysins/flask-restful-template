# coding=utf-8

import os

# settings.py
"""
settings.py

The base settings file for the project. This file will be imported by any modules that require settings functionality.
All variables and paths are loaded up from the environmental variables setup by in the .env file in use.
"""

import os
from dotenv import load_dotenv

# import the necessary
# .env file based on what environment you are in
# The base folder will be the env folder at the root of the project

ENV = os.getenv("ENV", "")  # get environment

# Implementing staging and production bypass. Useful for kubernetes environment.
if ENV not in ["staging", "production"]:
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__name__)), "configs",
                               "{env}.env".format(env=ENV))  # determine .env path
    # Load settings variables using dotenv
    load_dotenv(verbose=True, dotenv_path=dotenv_path)

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")
ENV = os.getenv("ENV")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRES_IN_HOURS = int(os.getenv("JWT_EXPIRES_IN_HOURS", "200"))
