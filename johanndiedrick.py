from __future__ import unicode_literals
from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
from bson import json_util
import json
import requests
import youtube_dl
from random import choice
from config import *
import os

app = Flask(__name__)
app.config['MONGO_DBNAME'] = MONGO_DBNAME
app.config['MONGO_USERNAME'] = MONGO_USERNAME
app.config['MONGO_PASSWORD'] = MONGO_PASSWORD
app.config['MONGO_URI'] = MONGO_URI
app.config['MONGO_PORT'] = MONGO_PORT
mongo = PyMongo(app)

@app.route("/")
def hello():
	return render_template('index.html')

@app.route("/api/1/bio")
def get_bio():
	bio = mongo.db.bio.find_one()
	response = { "response" : bio }
	return json.dumps(response, default=json_util.default)

@app.route("/api/1/works")
def get_all_works():
	all_works = []
	title = request.args.get('title')
	if title is None:
		works = mongo.db.works.find({})
	else:
		works = mongo.db.works.find({"title_slug" : title})
	for work in works:
		all_works.append(work)
	response = { "response" : all_works}
	return json.dumps(response, default=json_util.default)

@app.route("/api/1/videos/random")
def get_random_video():
	video_url = ""
	videos = os.listdir("static/vids")
	video = choice(videos)
	video_url = "static/vids/" + video
	response = { "response" : video_url}
	return json.dumps(response, default=json_util.default)

if __name__ == "__main__":
	app.debug = False
	app.run(host='0.0.0.0')
