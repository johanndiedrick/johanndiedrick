from __future__ import unicode_literals
from flask import Flask, render_template, jsonify, request
from flask.ext.pymongo import PyMongo
from bson import json_util
import json
import requests
import youtube_dl
from random import choice
from config import *

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

	#get videos playlist via youtube api
	r = requests.get(YOUTUBE_PLAYLIST)

	items = r.json()['items']

	#collect video ids
	video_ids = []
	for item in items:
		video_ids.append(item['snippet']['resourceId']['videoId'])
	
	#pick a random video
	yt_vid = choice(video_ids)

	#get our mp4 url :) lol
	youtube_vid_url = "http://www.youtube.com/watch?v=" + yt_vid
	ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'}) 
	yt_extract = ydl.extract_info(youtube_vid_url, download=False)
	yt_url = yt_extract['formats'][3]['url']

	response = { "response" : yt_url}
	return json.dumps(response, default=json_util.default)

if __name__ == "__main__":
	app.debug = True
	app.run()
