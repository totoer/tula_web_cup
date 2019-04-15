
from handlers.base_handler import BaseHandler
from models.client_model import ClientModel


class PrivateHandler(BaseHandler):

    @property
    def client(self):
        return self._client

    async def prepare(self):
        session_key = self.get_cookie("X-Session-Token")
        client_id = self.cache.get("twc:session_pool:{}".format(session_key))
        if client_id:
            self._client = await ClientModel.get_by_id(str(client_id, 'utf8'))

        else:
            self._client = None
