import tweepy
import time
import os

# =========================
# Load API keys securely
# =========================
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Authenticate
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# =========================
# Bot Functions
# =========================

# 1. Post a tweet
def post_tweet(message):
    api.update_status(message)
    print(f"✅ Tweeted: {message}")

# 2. Like and retweet tweets by hashtag
def like_and_retweet(hashtag, count=5):
    print(f"🔎 Searching tweets with #{hashtag}...")
    for tweet in tweepy.Cursor(api.search_tweets, q=f"#{hashtag}", lang="en").items(count):
        try:
            tweet.favorite()
            tweet.retweet()
            print(f"❤️ Liked and 🔁 Retweeted: {tweet.text[:50]}...")
            time.sleep(2)
        except tweepy.TweepyException as e:
            print(f"⚠️ Error: {e}")
            continue

# 3. Reply to mentions
def reply_to_mentions(message, since_id):
    print("💬 Checking mentions...")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if not tweet.favorited:
            try:
                tweet.favorite()
                api.update_status(
                    status=f"@{tweet.user.screen_name} {message}",
                    in_reply_to_status_id=tweet.id,
                )
                print(f"↩️ Replied to @{tweet.user.screen_name}")
            except tweepy.TweepyException as e:
                print(f"⚠️ Error: {e}")
    return new_since_id

# =========================
# Run Bot
# =========================
if __name__ == "__main__":
    # Example usage
    post_tweet("Hello Twitter! 🤖 This is my Python bot speaking.")
    like_and_retweet("Python", count=3)

    # Track mentions (run in loop)
    since_id = 1
    while True:
        since_id = reply_to_mentions("Thanks for reaching out! 🙌", since_id)
        time.sleep(60)  # check every 1 minute