import requests, json, api_key

def url_gen(kwd, maxCount):
	return "https://www.googleapis.com/youtube/v3/search?type=playlist&part=snippet&q={key}&maxResults={count}&order=viewCount&key={API_KEY}".format(key = kwd, count = str(maxCount), API_KEY = api_key.api_key)

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

def validate(videoID, playlistId):
	ls = getVideoIDs(playlistId)
	if videoID in ls:
		return True
	else:
		return False

def getVideoTitle(videoID):
	url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={VID_ID}&key={API_KEY}".format(VID_ID = videoID, API_KEY = api_key.api_key)
	r = requests.get(url)
	data = json.loads(r.text)
	return data["items"][0]["snippet"]["title"]

def extractPlaylistIDs(data):
	ls = []
	for item in data["items"]:
		ls.append(item["id"]["playlistId"])
	return ls

if __name__ == '__main__':
	IDs_toProcess = ["SC4xMk98Pdc"]
	searchTerms = []
	diction = dict()

	for each in IDs_toProcess:
		diction[each] = []


	for item in IDs_toProcess:
		searchTerms.append(getVideoTitle(item))

	for i in range(len(searchTerms)):
		
		url = url_gen(searchTerms[i], 50)
		r = requests.get(url)
		data = json.loads(r.text)
		playlistIDs = extractPlaylistIDs(data)
		print(playlistIDs)
		# print(getVideoIDs("PLegvV8yC11ja5xmIvaRTj6hZ7lMeP4f6N"))
		for each in playlistIDs:
			if validate(IDs_toProcess[i], each):
				diction[IDs_toProcess[i]].append(each)
	print(diction)
			

