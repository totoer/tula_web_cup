
from models.base_model import BaseModel
from pypika import Table, Query
from cerberus import Validator


image_like = Table('image_like', schema='twc')


CREATE_SCHEMA = {
    'image_id': {'type': 'integer', 'required': True},
    'client_id': {'type': 'integer', 'required': True},
    'value': {'type': 'boolean', 'required': True},
}


class ImageLikeModel(BaseModel):

    @classmethod
    async def create(cls, data):
        v = Validator(CREATE_SCHEMA)

        if v.validate(data):
            query = Query.into(image_like).columns(
                'image_id',
                'client_id',
                'value'
            ).insert(
                data.get('image_id'),
                data.get('client_id'),
                data.get('value')
            )

            cursor = await cls.db.execute(query.get_sql() + ' returning id');
            data['id'] = cursor.fetchone().get('id')

            return data, None

        else:
            return data, v.errors

    @classmethod
    async def delete(cls, image_like_id):
        query = Query.from_(image_like).delete().where(image_like.id==image_like_id)
        await cls.db.execute(query.get_sql())

    @classmethod
    async def get_by_image_id_client_id(cls, image_id, client_id):
        query = Query.from_(image_like).\
            where(
                (image_like.image_id==image_id) & \
                (image_like.client_id==client_id)
            ).select(
                image_like.id,
                image_like.image_id,
                image_like.client_id,
                image_like.value,
                image_like.create_at
            )

        cursor = await cls.db.execute(query.get_sql())
        return cursor.fetchone()
