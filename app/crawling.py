import re
import GetOldTweets3     as     got
from   app.models        import Model

class Crawling():

    def __init__(self):
        pass

    def check_isnews(self, tweet):
        data = re.findall("http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+", tweet)

        if data:
            result = 1
        else:
            result =  0

        return result

    def crawling(self, keyword, startdate, enddate, maxtweet):
        model_crawling = Model()

        if startdate and enddate and maxtweet > 0:

            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword).setSince(startdate).setUntil(enddate).setMaxTweets(maxtweet)

        elif startdate and enddate and maxtweet < 1:

            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword).setSince(startdate).setUntil(enddate)

        elif startdate and not enddate and maxtweet > 0:

            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword).setSince(startdate).setMaxTweets(maxtweet)

        elif enddate and not startdate and maxtweet > 0:

            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword).setUntil(startdate).setMaxTweets(maxtweet)

        elif startdate and not enddate and maxtweet < 1:

            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword).setUntil(startdate)

        elif enddate and not startdate and maxtweet < 1:

            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword).setUntil(startdate)

        else:
            print( keyword, startdate, enddate, maxtweet)
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword)

        tweets              = got.manager.TweetManager.getTweets(tweetCriteria)

        for tweet in tweets:
            content     =   tweet.text
            content     =   content.strip()
            tweetdate   =   tweet.date
            isnews      =   self.check_isnews(content)

            if not isnews:
                model_crawling.save_tweet(content, keyword, tweetdate)
