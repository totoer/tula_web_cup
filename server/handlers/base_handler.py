
import json
import pickle
import time
import datetime
import tornado.web
from models.base_model import BaseModel
from utils.json_encoder import ObjectEncoder


class BaseHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return BaseModel.db

    @property
    def cache(self):
        return self.application.cache

    @property
    def httpclient(self):
        return self.application.httpclient

    @property
    def request_data(self):
        if not hasattr(self, "_request_data"):
            self._request_data = json.loads(self.request.body.decode()) \
                if self.request.body else {}

            self._request_data = dict(filter(lambda i: i[1] != '', self._request_data.items()))

        return self._request_data

    def get_argument(self, field, default_value):
        v = super(BaseHandler, self).get_argument(field, default_value)
        return v or None

    def response(self, data):
        data = json.dumps(data, cls=ObjectEncoder)
        self.finish(data)
