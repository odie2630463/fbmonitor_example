# -*- coding: utf-8 -*-

from google.appengine.api import urlfetch
import json

app_id = '<fb_app_id>'
app_secret = '<fb_app_secret>'

access_token = '<token>'

base_url = 'https://graph.facebook.com/v2.7/{target_id}/feed?icon_size=16&access_token={access_token}&limit=100&since={since}&until={until}&fields=id,created_time,updated_time,message'

def query(target_id,since,until):
    url = base_url.format(access_token=access_token,target_id = target_id ,since=since , until=until)
    print url
    data = urlfetch.fetch(url).content
    data=json.loads(data)
    return data