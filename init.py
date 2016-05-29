import pymongo
from pymongo import MongoClient

connection = MongoClient()
db = connection.database

users = db["users"]
sessions = db["sessions"]
