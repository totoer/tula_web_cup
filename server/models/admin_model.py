
import hashlib

from models.base_model import BaseModel
from pypika import Table, Query, JoinType
from cerberus import Validator


admin = Table('admin', schema='twc')


CREATE_SCHEMA = {
    'login': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True},
    'access_token': {'type': 'string', 'required': True},
    'refresh_token': {'type': 'string', 'required': True},
    'expires_in': {'type': 'string', 'required': True}
}


class AdminModel(BaseModel):

    @classmethod
    async def create(cls, data):
        v = Validator(CREATE_SCHEMA)

        if v.calidate(data):
            password = hashlib.sha256(data.get('password').encode()).hexdigest()

            query = Query.into(admin).columns(
                'login',
                'password',
                'access_token',
                'refresh_token',
                'expires_in'
            ).insert(
                date.get('login'),
                password,
                date.get('access_token'),
                date.get('refresh_token'),
                date.get('expires_in')
            )

            cursor = await cls.db.execute(query.get_sql() + ' returning id');
            data['id'] = cursor.fetchone().get('id')

            return data, None

        else:
            return data, v.errors

    @classmethod
    async def get_by_id(cls, admin_id):
        query = Query.from_(admin).\
            where(admin.id==admin_id).
            select(
                admin.id,
                admin.login,
                admin.access_token,
                admin.refresh_token,
                admin.expires_in
            )

        cursor = await cls.db.execute(query.get_sql())
        return cursor.fetchone()

    @classmethod
    async def get_by_login_password(cls, login, password):
        password = hashlib.sha256(password.encode()).hexdigest()
        query = Query.from_(admin).where(
            (admin.login==login) & \
            (admin.password==password)
        ).select(
            admin.id,
            admin.login,
            admin.access_token,
            admin.refresh_token,
            admin.expires_in
        )

        cursor = await cls.db.execute(query.get_sql())
        return cursor.fetchone()
