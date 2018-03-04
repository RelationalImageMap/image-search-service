#from sys import argv
import time
import json
import tweepy
#import requests
from api import getAPI
import os
from google.cloud import pubsub

def main():
    try:
        #URL = 'https://relational-image-map-dev.firebaseapp.com'
        #r = requests.get(URL)
        #data = r.json()
        query = data['properties']['query']['type']
        lat = data['properties']['options']['properties']['searchLoc']['properties']['lat']['type']
        long = data['properties']['options']['properties']['searchLoc']['properties']['long']['type']
        location = str(lat + ',' + long + ',' + radius + 'mi')
        api = getAPI()
        cricTweet = tweepy.Cursor(api.search, q=query, geocode=location)

        time.sleep(REQUEST_DELAY)
        for tweet in cricTweet:
            if 'media' in tweet.entities:
                for image in tweet.entities['media']:
                    img = image['media_url']
                return img
            time.sleep(REQUEST_DELAY)					
					
    except IndexError:
        print("Program Missign Arg. Twitter Handle")
    except Exception as e:
        print("Program Failure. Error: {}".format(e))
    #finally:
    #    with open('{}Tweets2017-50'.format(arg), 'w') as saveFile:
    #       json.dump(tweetResults, saveFile)
		   
publisher = pubsub.PublisherClient()
topic = 'projects/{project_id}/topics/{topic}'.format(project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),topic='MY_TOPIC_NAME',)  # Set this to something appropriate.
#publisher.create_topic(topic)  # raises conflict if topic exists
publisher.publish(topic, format(img, 'b'), spam='test')


if __name__ == '__main__':
    main()