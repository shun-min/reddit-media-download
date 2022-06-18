#!/usr/lib64/python3.6

import re
from urllib.request import Request, urlopen

def scrape_url =
url = "https://www.reddit.com/r/malaysia/comments/vcnhkc/daylight_supermoon_near_the_tip_of_kl_twin_towers/"
user_agent = {'User-agent': 'Mozilla/5.0'}
req = Request(url, headers=user_agent)
page = urlopen(req)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
print(html)

# TODO: handle multiple urls from whole page
# pattern = r""".+(?P<src_tag>source src=)(?P<link>.+)(?P<format>m3u8).+"""
compiled_pattern = re.compile(r""".+(?P<src_tag>source src=")(?P<link>.+)(?P<format>m3u8).+""")
result = compiled_pattern.match(html)
m3u8_url = result.groupdict().get("link") + "m3u8"
