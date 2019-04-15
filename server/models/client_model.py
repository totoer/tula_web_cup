
from models.base_model import BaseModel
from pypika import Table, Query
from cerberus import Validator


client = Table('client', schema='twc')


CREATE_SCHEMA = {
    'login': {'type': 'string', 'required': True},
    'access_token': {'type': 'string', 'required': True},
    'refresh_token': {'type': 'string', 'required': True},
    'expires_in': {'type': 'integer', 'required': True},
}


class ClientModel(BaseModel):

    @classmethod
    async def create(cls, data):
        v = Validator(CREATE_SCHEMA)

        if v.validate(data):
            query = Query.into(client).columns(
                'login',
                'access_token',
                'refresh_token',
                'expires_in'
            ).insert(
                data.get('login'),
                data.get('access_token'),
                data.get('refresh_token'),
                data.get('expires_in')
            )

            cursor = await cls.db.execute(query.get_sql() + ' returning id');
            data['id'] = cursor.fetchone().get('id')

            return data, None

        else:
            return data, v.errors

    @classmethod
    async def get_by_id(cls, client_id):
        query = Query.from_(client).where(
            (client.id==client_id) & \
            (client.is_remove==False)
        ).select('*')
        cursor = await cls.db.execute(query.get_sql())
        return cursor.fetchone()

    @classmethod
    async def delete(cls, client_id):
        query = Query.from_(client).delete().where(client.id==client_id)
        await cls.db.execute(query.get_sql())
