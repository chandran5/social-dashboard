import requests
import json

def clean_text(text):
    # Remove non-alphanumeric characters and leading/trailing whitespaces
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text).strip()
    return cleaned_text

def get_facebook_stats(access_token, user_id):
    # Facebook Graph API endpoint
    url = f"https://graph.facebook.com/v14.0/{user_id}"

    # Make the request to the Graph API
    params = {
        'fields': 'id,name,followers_count,friends_count,posts{message,created_time,likes.summary(true),comments.summary(true)}',
        'access_token': access_token
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return None  # Return None to indicate failure

    data = response.json()

    # Extract basic user info and stats
    facebook_stats = {
        "username": data.get("name", ""),
        "followers_count": data.get("followers_count", 0),
        "friends_count": data.get("friends_count", 0),
        "posts": [],
        "likes_vs_hashtags": {
            "likes": [],
            "hashtags": []
        }
    }

    # Check if the user has posts data and populate the dictionary with post information
    if 'posts' in data:
        for post in data['posts']['data']:
            post_message = post.get('message', "")
            post_likes = post['likes']['summary'].get('total_count', 0)
            post_comments = post['comments']['summary'].get('total_count', 0)

            post_info = {
                "message": clean_text(post_message),
                "likes_count": post_likes,
                "comments_count": post_comments,
                "created_time": post['created_time']
            }
            facebook_stats["posts"].append(post_info)

            # Update likes_vs_hashtags data
            facebook_stats["likes_vs_hashtags"]["likes"].append(post_likes)

    return facebook_stats

# Example usage
access_token = "YOUR_FACEBOOK_ACCESS_TOKEN"
user_id = "USER_ID_OR_PAGE_ID"
stats = get_facebook_stats(access_token, user_id)
print(json.dumps(stats, indent=4))
