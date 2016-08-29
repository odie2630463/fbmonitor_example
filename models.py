from google.appengine.ext import ndb

class LineID(ndb.Model):
    id = ndb.StringProperty()

    @classmethod
    def query_all_id(cls):
        return cls.query().fetch()

class FbPost(ndb.Model):
    post_id = ndb.StringProperty()
    created_time = ndb.StringProperty()
    updated_time = ndb.StringProperty()
    content = ndb.TextProperty()

    @classmethod
    def query_by_post_id(cls,id):
        return cls.query().filter(FbPost.post_id == id).fetch()