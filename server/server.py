#!./.venv/bin/python

import sys
import os

sys.path.append(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), '.'))

import asyncio
import logging
import tornado.ioloop
import tornado.platform.asyncio
import tornado.log
from tornado.options import define, options, parse_config_file

import momoko
import psycopg2.extras
import redis
import tornado.web
import tornado.httpclient

from models.base_model import BaseModel

import urls


class Application(tornado.web.Application):

    @property
    def cache(self):
        return self._cache

    @property
    def httpclient(self):
        return self._httpclient

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

        dsn = "dbname={} user={} password={} host={} port={}".format(
            options.db_name,
            options.db_user,
            options.db_password,
            options.db_host,
            options.db_port)

        BaseModel.db = momoko.Pool(
            dsn=dsn,
            size=options.size_db_connection_pool,
            ioloop=tornado.ioloop.IOLoop.current(),
            cursor_factory=psycopg2.extras.RealDictCursor)

        BaseModel.db.connect()

        self._redis_pool = redis.ConnectionPool(
            host=options.cache_host,
            port=options.cache_port,
            db=options.cache_db)

        self._cache = redis.StrictRedis(connection_pool=self._redis_pool)

        self._httpclient = tornado.httpclient.AsyncHTTPClient()


if __name__ == '__main__':
    define("port", type=int)
    define("db_name", type=str)
    define("db_user", type=str)
    define("db_password", type=str)
    define("db_host", type=str)
    define("db_port", type=str)
    define("size_db_connection_pool", type=int)
    define("cache_host", type=str)
    define("cache_port", type=int)
    define("cache_db", type=int)
    define("debug", type=str)
    define("yandex_client_id", type=str)
    define("yandex_password", type=str)

    parse_config_file("application.conf")
    tornado.options.parse_command_line()

    tornado.log.enable_pretty_logging()

    if options.debug == "yes":
        tornado.log.app_log.setLevel(logging.DEBUG)
    elif options.debug == "no":
        tornado.log.app_log.setLevel(logging.INFO)

    tornado.platform.asyncio.AsyncIOMainLoop().install()

    application = Application(
        urls.urls,
        debug=(True if options.debug == "yes" else False))

    application.listen(options.port)

    asyncio.get_event_loop().run_forever()
