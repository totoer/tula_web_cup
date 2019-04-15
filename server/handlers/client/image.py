
import os
import json
import urllib

from handlers.client.private_handler import PrivateHandler
from models.image_model import ImageModel
from tornado.httpclient import HTTPRequest


class Image(PrivateHandler):

    async def get(self):
        limit = self.get_argument('limit', 10)
        offset = self.get_argument('offset', 0)

        client_id = self.client.get('id') if self.client is not None else None
        images = await ImageModel.get_list(client_id, limit, offset)

        for image in images:
            href = self.cache.get('image:%s' % (image.get('filepath'),))

            if href is not None:
                image['href'] = str(href, 'utf8')

            else:
                query = urllib.parse.urlencode({'path': image.get('filepath')})

                download_request = HTTPRequest(
                    'https://cloud-api.yandex.net/v1/disk/resources/download?'+query,
                    method='GET',
                    headers={'Authorization': 'OAuth %s' % (self.client.get('access_token'),)})

                download_response = await self.httpclient.fetch(download_request)

                if download_response.code == 200:
                    download_response_data = json.loads(download_response.body.decode("utf-8"))

                    href = download_response_data.get('href')
                    self.cache.set('image:%s' % (image.get('filepath'),), href, ex=(60*60))
                    image['href'] = href
        
        self.response(images)

    async def post(self):
        if self.client is not None:
            file_info = self.request.files.get('image')[0]
            ext = file_info.get('filename').split('.')[-1]
            file_body = file_info.get("body")

            filepath = '/twc/%s.%s' % (os.urandom(8).hex(), ext,)

            query = urllib.parse.urlencode({'path': filepath})

            upload_request = HTTPRequest(
                'https://cloud-api.yandex.net/v1/disk/resources/upload?'+query,
                method='GET',
                headers={'Authorization': 'OAuth %s' % (self.client.get('access_token'),)})

            upload_response = await self.httpclient.fetch(upload_request)

            if upload_response.code == 200:
                response_data = json.loads(upload_response.body.decode("utf-8"))
                upload_href = response_data.get('href')

                request = HTTPRequest(upload_href, method='PUT', body=file_body)
                response = await self.httpclient.fetch(request)

                if response.code in (201, 202,):
                    await ImageModel.create({
                        'filepath': filepath,
                        'client_id': self.client.get('id'),
                    })

                    self.response({'ok': True})

                else:
                    self.send_error(500)

            else:
                self.send_error(500)

        else:
            self.send_error(500)
