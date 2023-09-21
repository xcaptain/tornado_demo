import datetime

import jwt
from ds.aio_pool import AIOPool
from redis import Redis


class UserService:
    def __init__(self, db: AIOPool, redis: Redis, jwt_secret: str) -> None:
        self.db = db
        self.redis = redis
        self.jwt_secret = jwt_secret

    async def login_user(self, email: str, password: str) -> str:
        sql = "select id, password from users where email=%s"
        rows = await self.db.query(sql, (email,))
        if len(rows) != 1:
            raise Exception("no such user")
        user = rows[0]
        if user["password"] != password:
            raise Exception("wrong password")
        return self.create_token(user["id"])

    async def register_user(self, email: str, password: str) -> str:
        sql = "select id, password from users where email=%s"
        rows = await self.db.query(sql, (email,))
        if len(rows) != 0:
            raise Exception("user already exists")
        sql = "insert into users(email, password) values (%s, %s)"
        cur = await self.db.execute(sql, (email, password))
        user_id = cur.lastrowid
        return self.create_token(user_id)

    def create_token(self, user_id: int):
        now = datetime.datetime.utcnow()
        access_payload = {
            "iat": now,
            "sub": user_id,
            "type": "access",
            "exp": now + datetime.timedelta(days=30),
        }
        access_token = jwt.encode(access_payload, self.jwt_secret, algorithm="HS256")

        return access_token
