from pymongo import MongoClient
from api_requests import (
    get_trends_by_location,
    get_locations,
    get_trending_hashtags,
    generate_tiktok_tags,
    get_trending_keywords,
    get_top_ads,
    get_trending_videos,
    get_hashtag_info,
    get_google_trends,
    get_google_regions
)
from transform_data import (
    transform_twitter_trends_data,
    transform_twitter_locations_data,
    transform_twitter_hashtags_data,
    transform_tiktok_tags_data,
    transform_trending_keywords_data,
    transform_trending_ads_data,
    transform_trending_hashtags_data,
    transform_youtube_videos_data,
    transform_google_trends_data,
    transform_google_regions_data
)

# MongoDB connection
client = MongoClient('mongodb+srv://malekbouzidi:NYvZ913t7peJMuy8@cluster0.abswq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['trends_db']

# Collections
collections = {
    "tweeter": db['tweeter_trends'],
    "location": db['location_trends'],
    "hashtag": db['hashtag_trends'],
    "tiktok": db['tiktok_trends'],
    "trending_keywords": db['trending_keywords_trends'],
    "trending_ads": db['trending_ads_trends'],
    "trending_hashtags": db['trending_hashtags_trends'],
    "youtube": db['youtube_trends'],
    "google_trends": db['google_trends_trends'],
    "google_regions": db['google_regions']
}

# Function to insert data with upsert
def insert_data_with_upsert(collection, data, transform_function, unique):
    transformed_data = transform_function(data)
    
    if isinstance(transformed_data, list) and all(isinstance(item, dict) for item in transformed_data):
        for item in transformed_data:
            if unique in item:
                collection.update_one(
                    {unique: item[unique]},
                    {"$set": item},
                    upsert=True
                )
                print(f"Inserted or updated: {item}")
            else:
                print(f"Warning: Missing '{unique}' in item: {item}")
    else:
        print(f"Error: transformed_data is not a list of dictionaries. Data: {transformed_data}")

# ETL Process
def run_etl(api_key):
    print("Starting ETL process...")

    # Fetch data from APIs
    data = {
        "tweeter": get_trends_by_location("418f42bb932438869b297be8e9e8e492", api_key),
        "location": get_locations(api_key),
        "hashtag": get_trending_hashtags(api_key),
        "tiktok": generate_tiktok_tags(api_key),
        "trending_keywords": get_trending_keywords(api_key),
        "trending_ads": get_top_ads(api_key),
        "youtube": get_trending_videos(api_key),
        "trending_hashtags": get_hashtag_info(api_key),
        "google_trends": get_google_trends(api_key),
        "google_regions": get_google_regions(api_key),
    }

    # Insert Data into MongoDB
    insert_data_with_upsert(collections["tweeter"], data["tweeter"], transform_twitter_trends_data, "name")
    insert_data_with_upsert(collections["location"], data["location"], transform_twitter_locations_data, "name")
    insert_data_with_upsert(collections["hashtag"], data["hashtag"], transform_twitter_hashtags_data, "name")
    insert_data_with_upsert(collections["tiktok"], data["tiktok"], transform_tiktok_tags_data, "tag")
    insert_data_with_upsert(collections["trending_keywords"], data["trending_keywords"], transform_trending_keywords_data, "keyword")
    insert_data_with_upsert(collections["trending_ads"], data["trending_ads"], transform_trending_ads_data, "ad_title")
    insert_data_with_upsert(collections["trending_hashtags"], data["trending_hashtags"], transform_trending_hashtags_data, "hashtag")
    insert_data_with_upsert(collections["youtube"], data["youtube"], transform_youtube_videos_data, "video_id")
    insert_data_with_upsert(collections["google_trends"], data["google_trends"], transform_google_trends_data, "query")
    insert_data_with_upsert(collections["google_regions"], data["google_regions"], transform_google_regions_data, "code")

    print("ETL process completed.")
