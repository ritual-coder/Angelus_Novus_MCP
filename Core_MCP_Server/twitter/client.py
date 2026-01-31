import tweepy
import logging
import requests
import os
from config import TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_BEARER_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_client():
    """Returns an initialized Tweepy Call V2 Client."""
    try:
        client = tweepy.Client(
            bearer_token=TWITTER_BEARER_TOKEN,
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
        )
        return client
    except Exception as e:
        logger.error(f"Error initializing Twitter client: {e}")
        return None

def get_api_v1():
    """Returns an initialized Tweepy V1.1 API object (useful for trends if V2 doesn't support it easily yet or for media upload)."""
    try:
        auth = tweepy.OAuth1UserHandler(
            TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
        )
        api = tweepy.API(auth)
        return api
    except Exception as e:
        logger.error(f"Error initializing Twitter API v1.1: {e}")
        return None

def post_tweet(text, in_reply_to_tweet_id=None):
    """Posts a tweet to the account. Optionally replies to a tweet ID."""
    client = get_client()
    if client:
        try:
            response = client.create_tweet(text=text, in_reply_to_tweet_id=in_reply_to_tweet_id)
            logger.info(f"Tweet posted successfully! ID: {response.data['id']}")
            return response.data['id']
        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            return None
    return None

def search_trend_images(query, max_results=10):
    """
    Searches for recent tweets containing images related to the query.
    Returns a list of dictionaries with text and image URLs.
    """
    client = get_client()
    if not client:
        return []

    # Construct query: ensure we look for images and exclude retweets for quality
    # Note: 'has:images' is a standard operator.
    full_query = f"{query} has:images -is:retweet"

    try:
        # We need to explicitly ask for media fields and expansions
        response = client.search_recent_tweets(
            query=full_query,
            max_results=max_results,
            expansions=['attachments.media_keys', 'author_id'],
            media_fields=['url', 'preview_image_url', 'type'],
            user_fields=['name', 'username']
        )
        
        if not response.data:
            logger.info(f"No tweets found with images for query: {query}")
            return []

        # Map media keys to media objects for easy lookup
        media_map = {m.media_key: m for m in response.includes.get('media', [])}
        
        results = []
        for tweet in response.data:
            # Check availability of attachments
            if not tweet.attachments or 'media_keys' not in tweet.attachments:
                continue
                
            # Get the first image found in the tweet
            image_url = None
            for media_key in tweet.attachments['media_keys']:
                media = media_map.get(media_key)
                if media and media.type == 'photo':
                    image_url = media.url
                    break
            
            if image_url:
                results.append({
                    "id": tweet.id,
                    "text": tweet.text,
                    "image_url": image_url,
                    "author_id": tweet.author_id
                })
        
        return results

    except Exception as e:
        logger.error(f"Error searching for images: {e}")
        return []

def download_image(image_url, temp_filename="temp_image.jpg"):
    """Downloads an image from a URL to a local file."""
    try:
        # Twitter/X images often require a User-Agent to avoid 403 Forbidden
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        response = requests.get(image_url, headers=headers, stream=True)
        if response.status_code == 200:
            with open(temp_filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return temp_filename
        else:
            logger.error(f"Failed to download image. Status: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error downloading image: {e}")
        return None

def post_tweet_with_media(text, image_path):
    """
    Posts a tweet with an image attached.
    Uses API v1.1 for media upload and Call v2 for posting.
    """
    api = get_api_v1()
    client = get_client()
    
    if not api or not client:
        return None

    try:
        # 1. Upload Media (V1.1)
        logger.info(f"Uploading media: {image_path}")
        media = api.media_upload(image_path)
        media_id = media.media_id
        
        # 2. Create Tweet (V2)
        logger.info(f"Posting tweet with media_id: {media_id}")
        response = client.create_tweet(text=text, media_ids=[media_id])
        
        logger.info(f"Tweet with media posted! ID: {response.data['id']}")
        return response.data['id']
        
    except Exception as e:
        logger.error(f"Failed to upload media/post tweet: {e}")
        return None
