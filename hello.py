import praw
import time
import datetime
import json


with open("logindata.json") as json_data_file:
    logindata = json.load(json_data_file)

reddit = praw.Reddit(client_id=logindata["client_id"],client_secret=logindata["client_secret"],user_agent=logindata["user_agent"])
tickersFile = open("tickers.txt", "r")
tickerSet = []
now = datetime.datetime.now()
for line in tickersFile:
    tickerSet.append(line.rstrip())
topDay = reddit.subreddit('WallStreetBets').search('flair:'"DD", limit=500, syntax='lucene',time_filter='day')

for posts in topDay:
    for words in posts.title.split():
        if words.startswith('$'):
            print(words)


    
    





