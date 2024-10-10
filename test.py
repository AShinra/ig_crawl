import http.client
import json

_user = 'annecurtissmith'

# check country
conn = http.client.HTTPSConnection("instagram-scraper-api3.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "e1a0925e61msh1d52c10d6fe3576p17c9eejsnec6db565d7ff",
    'x-rapidapi-host': "instagram-scraper-api3.p.rapidapi.com"
}

conn.request("GET", f"/user_about?username_or_id={_user}", headers=headers)

res = conn.getresponse()
data = res.read()

# print(data.decode("utf-8"))
user_data = json.loads(data)
country = user_data['data']['about_this_account_country']

if country == 'Philippines':
    
    conn.request("GET", f"/user_posts?username_or_id={_user}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    # print(data.decode("utf-8"))
    _post_data = json.loads(data)
    post_data = _post_data['data']

    # for k, v in post_data.items():
    #     print(k)

    print(post_data['items'][0]['caption']['text'])
    


