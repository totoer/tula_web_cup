
from models.base_model import BaseModel
from pypika import Tables, Query, JoinType
import pypika.functions as sql_fn
from cerberus import Validator


image, image_like, client = Tables('image', 'image_like', 'client', schema='twc')


CREATE_SCHEMA = {
    'filepath': {'type': 'string', 'required': True},
    'client_id': {'type': 'integer', 'required': True},
}


class ImageModel(BaseModel):

    @classmethod
    async def create(cls, data):
        v = Validator(CREATE_SCHEMA)

        if v.validate(data):
            query = Query.into(image).columns(
                'filepath',
                'client_id'
            ).insert(
                data.get('filepath'),
                data.get('client_id')
            )

            cursor = await cls.db.execute(query.get_sql() + ' returning id');
            data['id'] = cursor.fetchone().get('id')

            return data, None

        else:
            return data, v.errors

    @classmethod
    async def get_by_id(cls, image_id):
        query = Query.from_(image).where(image.id==image_id).select('*')
        cursor = await cls.db.execute(query.get_sql())
        return cursor.fetchone()

    @classmethod
    async def get_list(cls, client_id, limit, offset):
        query = Query.from_(image).\
            join(image_like, JoinType.left).on(
                (image_like.image_id==image.id) & \
                (image_like.client_id==client_id)
            ).\
            select(
                image.id,
                image.filepath,
                image.likecount,
                image.dislikecount,
                image_like.value,
                image.create_at
            ).orderby(image.create_at).limit(limit).offset(offset)
        
        cursor = await cls.db.execute(query.get_sql())
        return cursor.fetchall()
