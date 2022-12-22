#!/usr/lib64/python3.6
import requests
import requests.auth
from urllib.request import Request, urlopen

from utils import REDDIT

id = REDDIT.ID
secret = REDDIT.SECRET

requests.auth.HTTPBasicAuth(id, secret)
post_data = 


url = "https://www.reddit.com/r/malaysia/comments/vcnhkc/daylight_supermoon_near_the_tip_of_kl_twin_towers/"
user_agent = {'User-agent': 'Mozilla/5.0'}
req = Request(url, headers=user_agent)
page = urlopen(req)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

# TODO: Test string for UI dev
# html = '123https://v.redd.it/0sljhvn5sm5a1/HLSPlaylist.m3u8123'
ext = "m3u8"
raw_pattern = r".+(?P<link>https.+.{}).+".format(ext)
pattern = re.compile(raw_pattern)
results = re.findall(pattern, html)
return results

# for full_url in results:
    print(full_url)


from bs4 import BeautifulSoup

url = "https://www.reddit.com/r/malaysia/comments/vcnhkc/daylight_supermoon_near_the_tip_of_kl_twin_towers/"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
