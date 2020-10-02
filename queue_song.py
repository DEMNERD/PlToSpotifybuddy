import requests
from requests.structures import CaseInsensitiveDict
from get_pl import *

group_name = ""
headers = CaseInsensitiveDict()
headers["authority"] = "api.spotifybuddy.com"
headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                        "Chrome/85.0.4183.83 Safari/537.36 "
headers["content-type"] = "text/plain;charset=UTF-8"
headers["accept"] = "*/*"
headers["origin"] = "https://spotifybuddy.com"
headers["sec-fetch-site"] = "same-site"
headers["sec-fetch-mode"] = "cors"
headers["sec-fetch-dest"] = "empty"
headers["referer"] = f"https://spotifybuddy.com/group/{group_name}"
playlist_obj = PlaylistObject()  # Declaring instance
playlist_obj.from_id(playlist_id='4IifzqaU0gqSQ89yzZXu2K')
url = "https://api.spotifybuddy.com/user/guestSession"
session = requests.Session()
a = session.post(url)
tokens = a.json()['auth']
print(session.cookies['tokens'])
session.headers = headers

url = "https://api.spotifybuddy.com/user/getSession"
print(f'"{tokens}"')
a = session.get(url, params={"link": group_name, "workspace_userid": "guest",
                             "tokens": f'"{tokens}"'})
print(session.cookies)
print(a.cookies)
url = 'https://api.spotifybuddy.com/queueSong'
for i in playlist_obj.tracks_list:
    data = '{"workspace_userid":"guest","uri":"spotify:track:%s",' \
           '"uniqueid_type":"lynnelees-music_group","link":%s, "tokens":%s}' % (group_name, i.id, tokens)
    resp = requests.post(url, headers=headers, data=data, cookies={'tokens': tokens})
    print(resp.content)
