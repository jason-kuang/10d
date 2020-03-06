import praw
import time
import datetime
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def setup(): 
    with open("logindata.json") as json_data_file:
        logindata = json.load(json_data_file)

        reddit = praw.Reddit(client_id=logindata["client_id"],
                     client_secret=logindata["client_secret"],
                     user_agent=logindata["user_agent"])
    
    return reddit 


def main():
    bull = 0
    bear = 0
    neutral = 0
    commentArray = []
    reddit = setup()
    for comment in reddit.subreddit('wallstreetbets').comments(limit=None):
        commentArray.append(comment.body)
    analyzer = SentimentIntensityAnalyzer()
    for sentence in commentArray:
        sentiment = analyzer.polarity_scores(sentence)
        if (sentiment["compound"] > .005) or (sentiment["pos"] > abs(sentiment["neg"])):
            bull += 1
        elif (sentiment["compound"] < -.005) or (abs(sentiment["neg"]) > sentiment["pos"]):
            bear += 1
        else:
            neutral += 1
    print("Bearish Sentiment: " + str(bear))
    print("Bullish Sentiment: " + str(bull))
    print("Neutral Sentiment: " + str(neutral))


if __name__ == "__main__":
    main()
    





