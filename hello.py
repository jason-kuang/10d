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


def analyzeSentiments(commentArray):
    largestBear = 0
    largestBull = 0
    notableBullandBear = ["Bear", "Bull"]
    overall = [0, 0, 0, notableBullandBear]  # 1st number is Bull sentiment, 2nd is Bear, 3rd is Neutral.
    analyzer = SentimentIntensityAnalyzer()
    for sentence in commentArray:
        sentiment = analyzer.polarity_scores(sentence)
        if (sentiment["compound"] > .005) or (sentiment["pos"] > abs(sentiment["neg"])):
            overall[0] += 1 #positive sentiment
            if (sentiment["pos"] > largestBull and len(sentence) > 30):
                largestBull = sentiment["pos"]
                notableBullandBear[0] = sentence
        elif (sentiment["compound"] < -.005) or (abs(sentiment["neg"]) > sentiment["pos"]):
            overall[1] += 1 #negative sentiment
            if (sentiment["neg"] > largestBear and len(sentence) > 30):
                largestBear = sentiment["neg"]
                notableBullandBear[1] = sentence
        else:
            overall[2] += 1 #neutral
    return overall


def extractComments(redditInstance):
    commentArray = []
    for comment in redditInstance.subreddit('wallstreetbets').comments(limit=None):
        commentArray.append(comment.body)

    return commentArray

def resultPrinter(sentiment,total):
    print("Bullish Sentiment: " + str(sentiment[0]))
    print("Bearish Sentiment: " + str(sentiment[1]))
    print("Neutral Sentiment: " + str(sentiment[2]))
    print("Notable Bullish Comment: " + str(sentiment[3][0]))
    print("Notable Bearish Comment: " + str(sentiment[3][1]))
    print("Overall: " + '%.2f' % ((sentiment[0] / total) * 100) + "%" + " of the " + str(total) + " comments are bullish")

def main():
    redditInstance = setup()
    commentArray = extractComments(redditInstance)
    sentiment = analyzeSentiments(commentArray)
    total = sentiment[0] + sentiment[1]
    resultPrinter(sentiment,total)




if __name__ == "__main__":
    main()
    





