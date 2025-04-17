import tweepy
import time

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAH8VzwEAAAAAQeOvVokJlROaVhH4Wn%2BgUCBviqE%3Dmb85Ll3yPoiHyk27IRIbb8GJzPQ50OIGlrHdV7L9MrY1SiFewU"

client = tweepy.Client(bearer_token=BEARER_TOKEN)

query = "TSMC"
max_results = 10
next_token = None

# Loop to handle pagination and rate limiting
while True:
    # Fetch recent tweets
    response = client.search_recent_tweets(
        query=query,
        max_results=max_results,
        tweet_fields=["created_at", "text"],
        next_token=next_token,
    )

    # Print tweets
    for tweet in response.data:
        print(tweet.created_at, tweet.text)
