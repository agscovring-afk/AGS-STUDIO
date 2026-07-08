import sqlite3
import os


DB_PATH = "ags_studio.db"


def get_connection():

    conn = sqlite3.connect(DB_PATH)

    return conn
