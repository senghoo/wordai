from mongoengine import connect

from config import mongo_config

connect(**mongo_config())

from .models import *
