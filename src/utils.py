import praw
import requests
import requests.auth

from enums import REDDIT

id = REDDIT.ID
secret = REDDIT.SECRET
username = REDDIT.USERNAME
password = REDDIT.PASSWORD
agent = "Reddit automation script"

# use API to get json object of a subreddit page
OAUTH_ENDPOINT = "https://oauth.reddit.com"
params = {
    "limit": 100
}


def get_auth():
    # getting reddit authentication info
    client_auth = requests.auth.HTTPBasicAuth(id, secret)
    post_data = {"grant_type": "password", "username": username, "password": password}
    headers = {"User-Agent": agent}

    # get token access ID
    TOKEN_ACCESS_ENDPOINT = "https://www.reddit.com/api/v1/access_token"
    response = requests.post(TOKEN_ACCESS_ENDPOINT, data=post_data, headers=headers, auth=client_auth)
    if response.status_code == 200:
        token_id = response.json()["access_token"]

    header2 = {
        "User-Agent": agent,
        "Authorization": "Bearer" + token_id
    }

    return header2

def get_reddit_instance():
    return praw.Reddit(
        client_id=id,
        client_secret=secret,
        password=password,
        user_agent=agent,
        username=username
    )


def get_url_response(header, url):
    subreddit_url = url.split("reddit.com")[1] + ".json"
    response2 = requests.get(OAUTH_ENDPOINT + subreddit_url, headers=header, params=params)
    if response2.status_code == 200:
        data = response2.json()
    return data