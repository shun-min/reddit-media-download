from urllib.request import Request, urlopen

url = "https://www.reddit.com/r/malaysia/comments/vcnhkc/daylight_supermoon_near_the_tip_of_kl_twin_towers/"
user_agent = {'User-agent': 'Mozilla/5.0'}
req = Request(url, headers=user_agent)
page = urlopen(req)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
print(html)
