#!/usr/lib64/python3.6
import requests
import requests.auth

from utils import REDDIT

id = REDDIT.ID
secret = REDDIT.SECRET
username = REDDIT.USERNAME
password = REDDIT.PASSWORD


def get_media_links(url):
    # getting reddit authentication info
    client_auth = requests.auth.HTTPBasicAuth(id, secret)
    post_data = {"grant_type": "password", "username": username, "password": password}
    headers = {
        "User-Agent": "Reddit automation script"
    }

    # get token access ID
    TOKEN_ACCESS_ENDPOINT = "https://www.reddit.com/api/v1/access_token"
    response = requests.post(TOKEN_ACCESS_ENDPOINT, data=post_data, headers=headers, auth=client_auth)
    if response.status_code == 200:
        token_id = response.json()["access_token"]

    # use API to get json object of a subreddit page
    OAUTH_ENDPOINT = "https://oauth.reddit.com"
    params = {
        "limit": 100
    }
    header2 = {
        "User-Agent": "Reddit automation script",
        "Authorization": "Bearer" + token_id
    }

    # https://reddit.com/r/malaysia/comments/vcnhkc/daylight_supermoon_near_the_tip_of_kl_twin_towers/.json
    subreddit_url = url.split("reddit.com")[1] + ".json"
    response2 = requests.get(OAUTH_ENDPOINT + subreddit_url, headers=header2, params=params)
    if response2.status_code == 200:
        data = response2.json()

    parent_lists = list()
    for d in data:
        children = d["data"]["children"]
        for c in children:
            try:
                parent_list = c["data"]["crosspost_parent_list"]
                parent_lists.append(parent_list)
            except KeyError:
                continue

    video_links = list()
    for p in parent_lists:
        try:
            video_link = p["media"]["reddit_video"]["fallback_url"]
            video_links.append(video_link)
        except KeyError:
            continue

    return video_links
