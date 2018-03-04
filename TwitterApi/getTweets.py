from sys import argv
import time
import json

from api import getAPI

REQUEST_DELAY = 5
MAX_REQUESTS = 10
def main():
    try:
        arg = argv[1]
        api = getAPI()
        tweetResults = []

        tweetIndex = api.user_timeline(screen_name=arg, count=1)[0].id
        #tweetIndex = 680949869961568255 (Dec 2015)

        time.sleep(REQUEST_DELAY)
        for request in range(MAX_REQUESTS):
            tweets = api.user_timeline(screen_name=arg, include_retweets=False, max_id=tweetIndex)
            #tweetIndex = tweets[-1].id - 1
            #print ("getting tweets before %s" % tweetIndex)
            for tweet in tweets:
                #print(tweet.text)
                tweetResults.append("\n" + str(tweet.created_at) +"  " + tweet.text)
            time.sleep(REQUEST_DELAY)
        print(tweetResults)
        print(len(tweetResults))

    except IndexError:
        print("Program Missign Arg. Twitter Handle")
    except Exception as e:
        print("Program Failure. Error: {}".format(e))
    finally:
        with open('{}Tweets2017-50'.format(arg), 'w') as saveFile:
           json.dump(tweetResults, saveFile)
if __name__ == '__main__':
    main()

