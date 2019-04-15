
from handlers.client.private_handler import PrivateHandler
from models.client_model import ClientModel

class Logout(PrivateHandler):

    async def get(self):
        if self.client is not None:
            session_key = self.get_cookie("X-Session-Token")

            self.cache.set("twc:session_pool:{}".format(session_key), "")
            self.clear_cookie("X-Session-Token", session_key)

            await ClientModel.delete(self.client.get('id'))

        else:
            self.send_error(500)
