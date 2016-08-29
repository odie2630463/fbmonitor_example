# -*- coding: utf-8 -*-

import logging
from datetime import datetime , timedelta

from linebot import *
from fbcrawler import *
import models
# Import the Flask Framework
from flask import Flask
from flask import request

#from requests_toolbelt.adapters import appengine
#appengine.monkeypatch()
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    return 'Hello Odie!'

@app.route('/test')
def test():
    my_id = '<Your Line id>' # for testing
    push_msg( my_id,'to Odie')
    return 'Hello Odie!'

@app.route('/fbtest')
def fbtest():
    target_ids = ['622543414529008','1507207486163325'] #example targets
    target_names = ['新竹大小事粉絲頁','新竹大小事社團']
    targets = zip(target_ids,target_names)
    Line_message_template = "HCCP輿情通報: \n"+ "來源:{target_name} \n" + "內容:{content} \n"+ "網址:{url}"

    until = datetime.now()
    #until = datetime(2016,8,28,15,0,0)
    since = until - timedelta(minutes=12)

    for target in targets:
        raw = query(target[0],since,until)
        data = raw["data"]
        logging.debug(data)
        for i in data:
            post_id_str = i['id'].encode('utf-8')
            post_id = post_id_str.split('_')
            post_url = 'https://www.facebook.com/groups/%s/permalink/%s' % (post_id[0] , post_id[1])
            post_content = i.get('message','').encode('utf-8')

            q_res = models.FbPost.query_by_post_id(post_id_str)
            if q_res == []:
                logging.debug("q_res is None")
                models.FbPost(post_id_str,post_id=post_id_str).put()
                #my_id = 'uf200cdcce2dc900ef701b65fd5131d2d'
                for line_id in models.LineID.query_all_id():
                    logging.debug(line_id)
                    push_msg(line_id.id,Line_message_template.format(target_name=target[1],content=post_content,url=post_url))

    return 'Done'

@app.route('/callback', methods=["POST"])
def linebot():
  args = json.loads(request.get_data().decode('utf-8'))
  logging.debug('kick from line server,\n %s'%(args['result']))
  for msg in args['result']:
        id = msg["content"]["from"]
        content = msg["content"]["text"].strip()
        if content == '<keyword>': #Set keyword to join
            models.LineID.get_or_insert(id,id=id).put()
            push_msg(id,"成功加入")
        else:
            push_msg(id,"無法加入")
    #push_msg( msg["content"]["from"], msg["content"]["text"] )
  return '{}'

@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404
