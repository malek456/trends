import http.client
import json
from datetime import datetime

## Transformation :

def transform_twitter_trends_data(trends_data):
    """
    Transform Twitter trending topics data into a unified format.
    :param trends_data: Raw JSON data from the API.
    :return: List of dictionaries containing transformed data.
    """
    transformed_data = []
    if trends_data.get("status") == "SUCCESS":
        trends = trends_data.get("trending", {}).get("trends", [])
        for trend in trends:
            transformed_data.append({
                "name": trend.get("name"),
                "post_count": trend.get("postCount"),
                "domain": trend.get("domain"),
                "rank": trend.get("rank"),
                "mobile_url": trend.get("mobileIntent"),
                "web_url": trend.get("webUrl")
            })
    return transformed_data

def transform_twitter_locations_data(locations_data):
    """
    Transform Twitter locations data into a unified format.
    :param locations_data: Raw JSON data from the API.
    :return: List of dictionaries containing transformed data.
    """
    transformed_data = []
    if locations_data.get("status") == "SUCCESS":
        locations = locations_data.get("locations", [])
        for location in locations:
            transformed_data.append({
                "name": location.get("name"),
                "place_id": location.get("placeID"),
                "location_type": location.get("locationType")
            })
    return transformed_data

def transform_twitter_hashtags_data(hashtags_data):
    """
    Transform Twitter trending hashtags data into a unified format.
    :param hashtags_data: Raw JSON data from the API.
    :return: List of dictionaries containing transformed data.
    """
    transformed_data = []
    if hashtags_data.get("success"):
        hashtags = hashtags_data.get("data", [])
        for hashtag in hashtags:
            transformed_data.append({
                "name": hashtag.get("name"),
                "url": hashtag.get("url"),
                "tweet_volume": hashtag.get("tweet_volume"),
                "update_time": hashtag.get("agencyDataUpdateTime")
            })
    return transformed_data

def transform_tiktok_tags_data(tags_data):
    """
    Transform TikTok tags data into a unified format.
    :param tags_data: Raw JSON data from the API.
    :return: Dictionary containing transformed data for hashtags, trends, strategy, and metrics.
    """
    transformed_data = {
        "hashtags": {},
        "trends": {},
        "strategy": {},
        "metrics": {}
    }

    if tags_data.get("status") == "success":
        result = tags_data.get("result", {})

        # Extract hashtags
        hashtags = result.get("hashtags", {})
        transformed_data["hashtags"] = {
            "trending": hashtags.get("trending", []),
            "niche": hashtags.get("niche", []),
            "viral": hashtags.get("viral", []),
            "community": hashtags.get("community", []),
            "recommended": hashtags.get("recommended", [])
        }

        # Extract trends
        trends = result.get("trends", {})
        transformed_data["trends"] = {
            "current_trends": trends.get("currentTrends", []),
            "rising_trends": trends.get("risingTrends", []),
            "challenge_tags": trends.get("challengeTags", [])
        }

        # Extract strategy
        strategy = result.get("strategy", {})
        transformed_data["strategy"] = {
            "best_practices": strategy.get("bestPractices", []),
            "combinations": strategy.get("combinations", []),
            "timing": strategy.get("timing", "")
        }

        # Extract metrics
        metrics = result.get("metrics", {})
        transformed_data["metrics"] = {
            "trending_score": metrics.get("trendingScore", ""),
            "viral_potential": metrics.get("viralPotential", ""),
            "reach_estimate": metrics.get("reachEstimate", ""),
            "competition_level": metrics.get("competitionLevel", "")
        }

    return transformed_data

def transform_trending_keywords_data(keywords_data):
    """
    Transform trending keywords data into a unified format.
    :param keywords_data: Raw JSON data from the API.
    :return: List of dictionaries containing transformed data for each keyword.
    """
    transformed_data = []

    if keywords_data.get("code") == 0:  # Check if the API request was successful
        keyword_list = keywords_data.get("data", {}).get("keyword_list", [])

        for keyword_data in keyword_list:
            transformed_data.append({
                "keyword": keyword_data.get("keyword", ""),
                "comment": keyword_data.get("comment", 0),
                "cost": keyword_data.get("cost", 0),
                "cpa": keyword_data.get("cpa", 0),
                "ctr": keyword_data.get("ctr", 0),
                "cvr": keyword_data.get("cvr", 0),
                "impression": keyword_data.get("impression", 0),
                "like": keyword_data.get("like", 0),
                "play_six_rate": keyword_data.get("play_six_rate", 0),
                "post": keyword_data.get("post", 0),
                "post_change": keyword_data.get("post_change", 0),
                "share": keyword_data.get("share", 0),
                "video_list": "; ".join(keyword_data.get("video_list", []))  # Convert list to a string
            })

    return transformed_data

def transform_trending_ads_data(ads_data):
    """
    Transform trending ads data into a unified format.
    :param ads_data: Raw JSON data from the API.
    :return: List of dictionaries containing transformed data for each ad.
    """
    transformed_data = []

    if ads_data.get("code") == 0:  # Check if the API request was successful
        materials = ads_data.get("data", {}).get("materials", [])

        for ad in materials:
            video_info = ad.get("video_info", {})
            transformed_data.append({
                "ad_title": ad.get("ad_title", ""),
                "brand_name": ad.get("brand_name", ""),
                "cost": ad.get("cost", 0),
                "ctr": ad.get("ctr", 0),
                "favorite": ad.get("favorite", False),
                "id": ad.get("id", ""),
                "industry_key": ad.get("industry_key", ""),
                "is_search": ad.get("is_search", False),
                "like": ad.get("like", 0),
                "objective_key": ad.get("objective_key", ""),
                "video_id": video_info.get("vid", ""),
                "video_duration": video_info.get("duration", 0),
                "video_cover": video_info.get("cover", ""),
                "video_url_720p": video_info.get("video_url", {}).get("720p", ""),
                "video_width": video_info.get("width", 0),
                "video_height": video_info.get("height", 0)
            })

    return transformed_data

def transform_trending_hashtags_data(hashtags_data):
    """
    Transform trending hashtags data into a unified format.
    :param hashtags_data: Raw JSON data from the API.
    :return: List of dictionaries containing transformed data for each hashtag.
    """
    transformed_data = []

    if hashtags_data.get("code") == 0:  # Check if the API request was successful
        hashtag_list = hashtags_data.get("data", {}).get("list", [])

        for hashtag in hashtag_list:
            # Extract trend data
            trend_data = []
            for trend_point in hashtag.get("trend", []):
                trend_data.append({
                    "time": trend_point.get("time", 0),
                    "value": trend_point.get("value", 0)
                })

            # Extract creators data
            creators_data = []
            for creator in hashtag.get("creators", []):
                creators_data.append({
                    "nick_name": creator.get("nick_name", ""),
                    "avatar_url": creator.get("avatar_url", "")
                })

            transformed_data.append({
                "hashtag_id": hashtag.get("hashtag_id", ""),
                "hashtag_name": hashtag.get("hashtag_name", ""),
                "country_id": hashtag.get("country_info", {}).get("id", ""),
                "country_name": hashtag.get("country_info", {}).get("value", ""),
                "is_promoted": hashtag.get("is_promoted", False),
                "trend": trend_data,
                "creators": creators_data,
                "publish_cnt": hashtag.get("publish_cnt", 0),
                "video_views": hashtag.get("video_views", 0),
                "rank": hashtag.get("rank", 0),
                "rank_diff": hashtag.get("rank_diff", 0),
                "rank_diff_type": hashtag.get("rank_diff_type", 0)
            })

    return transformed_data

def transform_youtube_videos_data(videos_data):
    """
    Transform YouTube trending videos data into a unified format.
    :param videos_data: Raw JSON data from the API.
    :return: List of dictionaries containing transformed data for each video.
    """
    transformed_data = []

    if videos_data.get("data"):  # Check if the API request was successful
        for video in videos_data.get("data", []):
            # Extract channel thumbnail
            channel_thumbnail = video.get("channelThumbnail", [{}])[0].get("url", "")

            # Extract video thumbnails
            thumbnails = []
            for thumbnail in video.get("thumbnail", []):
                thumbnails.append({
                    "url": thumbnail.get("url", ""),
                    "width": thumbnail.get("width", 0),
                    "height": thumbnail.get("height", 0)
                })

            transformed_data.append({
                "video_id": video.get("videoId", ""),
                "title": video.get("title", ""),
                "channel_title": video.get("channelTitle", ""),
                "channel_id": video.get("channelId", ""),
                "channel_handle": video.get("channelHandle", ""),
                "channel_thumbnail": channel_thumbnail,
                "description": video.get("description", ""),
                "view_count": video.get("viewCount", ""),
                "published_time_text": video.get("publishedTimeText", ""),
                "publish_date": video.get("publishDate", ""),
                "length_text": video.get("lengthText", ""),
                "thumbnails": thumbnails
            })

    return transformed_data

def transform_google_trends_data(trends_data):
    """
    Transform Google Trends data into a unified format.
    :param trends_data: Raw JSON data from the API.
    :return: List of dictionaries containing transformed data for each trending query.
    """
    transformed_data = []

    if trends_data.get("status") == "success":  # Check if the API request was successful
        for item in trends_data.get("items", []):
            # Extract image details
            image_data = item.get("image", {})
            image_info = {
                "news_url": image_data.get("newsUrl", ""),
                "source": image_data.get("source", ""),
                "image_url": image_data.get("imageUrl", "")
            }

            # Extract articles
            articles_data = []
            for article in item.get("articles", []):
                article_image = article.get("image", {})
                articles_data.append({
                    "title": article.get("title", ""),
                    "time_ago": article.get("timeAgo", ""),
                    "source": article.get("source", ""),
                    "news_url": article_image.get("newsUrl", ""),
                    "image_url": article_image.get("imageUrl", ""),
                    "url": article.get("url", ""),
                    "snippet": article.get("snippet", "")
                })

            transformed_data.append({
                "query": item.get("query", ""),
                "formatted_traffic": item.get("formattedTraffic", ""),
                "related_queries": item.get("relatedQueries", []),
                "image": image_info,
                "articles": articles_data
            })

    return transformed_data

def transform_google_regions_data(regions_data):
    """
    Transform Google Trends regions data into a unified format.
    :param regions_data: Raw JSON data from the API.
    :return: List of dictionaries containing transformed data for each region.
    """
    transformed_data = []

    if regions_data.get("status") == "success":  # Check if the API request was successful
        for region in regions_data.get("regions", []):
            transformed_data.append({
                "code": region.get("code", ""),
                "name": region.get("name", "")
            })

    return transformed_data