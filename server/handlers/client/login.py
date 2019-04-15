
from handlers.client.private_handler import PrivateHandler
from tornado.options import options


class Login(PrivateHandler):

    async def get(self):
        self.response(self.client)
