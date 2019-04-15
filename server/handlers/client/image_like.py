
from handlers.client.private_handler import PrivateHandler
from models.image_model import ImageModel
from models.image_like_model import ImageLikeModel


class ImageLike(PrivateHandler):

    async def post(self):
        if self.client is not None:
            image_id = self.request_data.get('image_id', None)
            image = await ImageModel.get_by_id(image_id)

            if image is not None:
                image_like = await ImageLikeModel.get_by_image_id_client_id(
                    image.get('id'), self.client.get('id'))

                if image_like is None:
                    data, errors = await ImageLikeModel.create({
                        'image_id': image.get('id'),
                        'client_id': self.client.get('id'),
                        'value': self.request_data.get('value'),
                    })

                    if errors is None:
                        self.response({'ok': True})

                    else:
                        self.response({'ok': False})

                else:
                    await ImageLikeModel.delete(image_like.get('id'))
                    self.response({'ok': True})

            else:
                self.send_error(404)

        else:
            self.send_error(401)
