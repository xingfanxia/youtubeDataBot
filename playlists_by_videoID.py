#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-13 14:32:01
# @Author  : Xingfan Xia (xiax@carleton.edu)
# @Link    : http://xiax.tech
# @Version : $V1$
# run this with python3
import requests, json, api_key, tqdm

# Generate API call to search top 50 playlists by keyword
def url_gen(kwd, maxCount):
	return "https://www.googleapis.com/youtube/v3/search?type=playlist&part=snippet&q={key}&maxResults={count}&order=viewCount&key={API_KEY}".format(key = kwd, count = str(maxCount), API_KEY = api_key.api_key)

# Given a playlistId find the videoIDs of top 50 songs sorted by popularity; ideally should get all videoIDs. But it's kinda complicated and top 50 should be enough and more efficient
def getVideoIDs(playlistId):
	videoIDs = []
	url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2C+id&playlistId={PL_ID}&maxResults=50&order=viewCount&key={API_KEY}".format(PL_ID = playlistId, API_KEY = api_key.api_key)
	r = requests.get(url)
	data = json.loads(r.text)
	try:
		for item in data["items"]:
			videoIDs.append(item["snippet"]["resourceId"]["videoId"])
	except:
		print("Unknow Error")
	return videoIDs

# Validate if the interested video is in that playlist
def validate(videoID, playlistId):
	ls = getVideoIDs(playlistId)
	if videoID in ls:
		return True
	else:
		return False

# Get the video title by videoID
def getVideoTitle(videoID):
	url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={VID_ID}&key={API_KEY}".format(VID_ID = videoID, API_KEY = api_key.api_key)
	r = requests.get(url)
	data = json.loads(r.text)
	return data["items"][0]["snippet"]["title"]

# Extract all the playlistID from json repsonse
def extractPlaylistIDs(data):
	ls = []
	for item in data["items"]:
		ls.append((item["id"]["playlistId"], item["snippet"]["title"]))
	return ls

if __name__ == '__main__':
	IDs_toProcess = ["SC4xMk98Pdc", "e-ORhEE9VVg", "IdneKLhsWOQ"]
	searchTerms = []
	diction = dict()

	for each in IDs_toProcess:
		vid_title = getVideoTitle(each)
		diction[each] = [vid_title, []]
		searchTerms.append(vid_title)

	for i in range(len(searchTerms)):
		url = url_gen(searchTerms[i], 50)
		r = requests.get(url)
		data = json.loads(r.text)
		playlistIDs = extractPlaylistIDs(data)

		# for each releveant playlist check if the video is in it; if it is, append to the list asscociated with the dictionary entry with videoID as a key
		with tqdm.tqdm(unit='playlists', total=len(playlistIDs)) as pbar:
			for each in playlistIDs:
				if validate(IDs_toProcess[i], each[0]):
					diction[IDs_toProcess[i]][1].append(each)
				pbar.update(1)
			# improve readability by dumping to json
			# Structured as 
			# {"videoID": [
		 #        "videoTitle",
		 #        [ //Array of playlists that include it
		 #            "PLegvV8yC11jb-HHZQN2kbQSdZK47F2Wi4",
		 #            "PLegvV8yC11ja5xmIvaRTj6hZ7lMeP4f6N",
		 #            "PLqZhJtFQSRt44EPKSlVkACy8dEl7vI8-g",
		 #            "PLJ3eEnBTDlWmLkI-vW-KMWbz21yyojMJ4",
		 #            "PL6NCFegKoCEzcIGGt7pD7-n4dYG0737xi",
		 #            "PLWoba7uuii59_Yu0_g-FpV610ZMG0-Lb5",
		 #            "PLK8tajmX0uLjT8LTzxyUBpkaJQiShDJxf",
		 #            "PLir_zeQq_1GofyNDQx7JZ4H0EA2BGEap7",
		 #            "PLzb4x-Jqqbb7htzqfq0MWN692RT9p0oyH",
		 #            "PLqZhJtFQSRt4C47pq01bBjBETG4Kbzlv_",
		 #            "PLUz5ZYKGi2yrxRmOsO_zeCuTq89e2hVWl",
		 #            "PLghrFgkzVHiTlF7xFhNqIsYkwzDRKjEuj",
		 #            "PLSV39S4qft4oIbcpkjEai-c0Q5T3zD4uG",
		 #            "PLlQezi7ZjIBf5q50bYoYx8Vsfy0mVmctT",
		 #            "PLSRPVvtqCQBAIRsMfFFkcFI3sIkTW84Xv",
		 #            "PLZE1UAUgE_q9ob4iwR_2cVoj1R9CJFawJ",
		 #            "PL2ndDRBqT3wn3yzcXrehDRFcPtwiSmssn",
		 #            "PL9QuDds9qoqg5_U6_kRQX0azyNOWSYatq",
		 #            "PLWkg4t_m90-qGHt-JJPBKod6OWiNR1rf1",
		 #            "PLXTBy-UCFrsnlL0aZRG3RoBvAMNdRLyGv",
		 #            "PLhGOZYXl77uyWJAWuDaYu0loE51Sa4Wgh"
		 #        ]
		 #    ]}
	print(json.dumps(diction, indent=4))