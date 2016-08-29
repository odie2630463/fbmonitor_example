# -*- coding: utf-8 -*-
import logging
import urllib
import json
from google.appengine.api import urlfetch

Line_message_template = "HCCP輿情通報: \n" + "內容:{content} \n"+ "網址:{url}"

def push_msg(tgt_id,msg_data):
  url = "https://trialbot-api.line.me/v1/events"

  form_fields = {
      "to": [str(tgt_id)],
      "toChannel": 1383378250,
      "eventType": 138311608800106203,
      "content":{
        "contentType":1,
        "toType":1,
        "text": msg_data
        }
      }
  #logging.debug(form_fields)
  #form_data = urllib.urlencode(form_fields)
  result = urlfetch.fetch(
    url=url,
    payload=json.dumps(form_fields,ensure_ascii=False),
    method=urlfetch.POST,
    headers={
                'Content-type':'application/json; charset=UTF-8',
                'X-Line-ChannelID':'<line_ID>',
                'X-Line-ChannelSecret':'<Secret>',
                'X-Line-Trusted-User-With-ACL':'<MID>',
            }
    )
  if result.status_code == 200:
    logging.debug(result.content)
  else:
    logging.debug(result.content)
