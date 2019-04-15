
import os
import json
import urllib

from handlers.client.private_handler import PrivateHandler
from models.client_model import ClientModel
from tornado.httpclient import HTTPRequest
from tornado.options import options


class OAuth(PrivateHandler):

    async def get(self):
        code = self.get_argument('code', None)

        if code is not None:
            headers = {
                'Host': 'oauth.yandex.ru',
                'Content-type': 'application/x-www-form-urlencoded',
            }

            body = {
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': options.yandex_client_id,
                'client_secret': options.yandex_password,
            }

            body = urllib.parse.urlencode(body)

            oauth_request = HTTPRequest(
                'https://oauth.yandex.ru/token',
                method='POST',
                headers=headers,
                body=body)

            oauth_response = await self.httpclient.fetch(oauth_request)

            if oauth_response.code == 200:
                oauth_response_data = json.loads(oauth_response.body.decode("utf-8"))

                access_token = oauth_response_data.get('access_token')

                info_request = HTTPRequest(
                    'https://login.yandex.ru/info',
                    method='GET',
                    headers={'Authorization': 'OAuth %s' % (access_token,)})

                info_response = await self.httpclient.fetch(info_request)

                if info_response.code == 200:
                    info_response_data = json.loads(info_response.body.decode("utf-8"))

                    data, errors = await ClientModel.create({
                        'login': info_response_data.get('login'),
                        'access_token': access_token,
                        'refresh_token': oauth_response_data.get('refresh_token'),
                        'expires_in': oauth_response_data.get('expires_in'),
                    })

                    print(errors)

                    session_key = os.urandom(8).hex()
                    self.cache.set("twc:session_pool:{}".format(session_key), data.get("id"))
                    self.set_cookie("X-Session-Token", session_key)

                    state = self.get_argument('state', '/')

                    self.redirect(state)

                else:
                    self.send_error(500)

            else:
                self.send_error(500)
                
        else:
            self.send_error(500)
