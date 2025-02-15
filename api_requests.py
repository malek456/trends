import http.client
import json
from datetime import datetime

def get_hashtag_info(api_key, tag="viral"):
    """
    Fetch information about a specific hashtag.
    :param api_key: Your RapidAPI key.
    :param tag: Hashtag to search for (default: "viral").
    :return: JSON response containing hashtag information.
    """
    conn = http.client.HTTPSConnection("yt-api.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "yt-api.p.rapidapi.com"
    }
    conn.request("GET", f"/hashtag?tag={tag}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def get_trends_by_location(location_id, api_key):
    """
    Fetch trending topics for a specific location.
    """
    conn = http.client.HTTPSConnection("twitter-trends-by-location.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "twitter-trends-by-location.p.rapidapi.com"
    }
    conn.request("GET", f"/location/{location_id}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def get_locations(api_key):
    """
    Fetch available locations for trending topics.
    """
    conn = http.client.HTTPSConnection("twitter-trends-by-location.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "twitter-trends-by-location.p.rapidapi.com"
    }
    conn.request("GET", "/locations", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def get_trending_hashtags(api_key):
    """
    Fetch trending Twitter hashtags.
    """
    conn = http.client.HTTPSConnection("trending-twitter-hashtags.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "trending-twitter-hashtags.p.rapidapi.com",
        'Content-Type': "application/json"
    }
    payload = json.dumps({"key1": "value", "key2": "value"})
    conn.request("POST", "/getTrendingTwitterHashtags", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def generate_tiktok_tags(api_key, content="trends", trend="viral", language="en", noqueue=1, count=20):
    """
    Fetch TikTok tags based on trends.
    """
    conn = http.client.HTTPSConnection("youtube-tag-generator-api-viral-tiktok-tags-hashtags.p.rapidapi.com")
    payload = json.dumps({"content": content})

    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "youtube-tag-generator-api-viral-tiktok-tags-hashtags.p.rapidapi.com",
        'Content-Type': "application/json"
    }
    conn.request("POST", f"/generateTikTokTags?trend={trend}&language={language}&noqueue={noqueue}&count={count}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def get_trending_keywords(api_key, page=1, limit=20, period=7, country="US"):
    """
    Fetch trending keywords on TikTok.
    """
    conn = http.client.HTTPSConnection("tiktok-creative-center-api.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "tiktok-creative-center-api.p.rapidapi.com"
    }
    conn.request("GET", f"/api/trending/keyword?page={page}&limit={limit}&period={period}&country={country}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def get_top_ads(api_key, page=1, limit=20, period=7, country="US", order_by="ctr"):
    """
    Fetch top TikTok ads.
    """
    conn = http.client.HTTPSConnection("tiktok-creative-center-api.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "tiktok-creative-center-api.p.rapidapi.com"
    }
    conn.request("GET", f"/api/trending/ads?page={page}&limit={limit}&period={period}&country={country}&order_by={order_by}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def get_trending_videos(api_key, geo="US"):
    """
    Fetch trending YouTube videos for a specific region.
    """
    conn = http.client.HTTPSConnection("yt-api.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "yt-api.p.rapidapi.com"
    }
    conn.request("GET", f"/trending?geo={geo}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def get_google_trends(api_key):
    """
    Fetch Google's trending data.
    """
    conn = http.client.HTTPSConnection("google-trends8.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "google-trends8.p.rapidapi.com"
    }
    today_date = datetime.now().strftime("%Y-%m-%d")
    endpoint = f"/trendings?region_code=US&hl=en-US&date={today_date}"

    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def get_google_regions(api_key):
    """
    Fetch available regions for Google Trends.
    """
    conn = http.client.HTTPSConnection("google-trends8.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "google-trends8.p.rapidapi.com"
    }
    conn.request("GET", "/regions", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))
