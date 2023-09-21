import logging

import tornado
from redis import Redis

from ds.aio_pool import AIOPool
from handlers.user_handler import UserRegisterHandler, UserSigninHandler
from services.user_service import UserService


class HealthCheckHandler(tornado.web.RequestHandler):
    async def get(self):
        sql = "select count(*) as cnt from users"
        a = await self.application.db.query(sql)
        await self.application.redis_client.set("ping", "pong", ex=60)
        pong = await self.application.redis_client.get("ping")
        msg = f"ok, {a[0]['cnt']}, {pong}"
        logging.info(msg)
        self.write(msg)


class Application(tornado.web.Application):
    def __init__(
        self,
        db: AIOPool | None = None,
        redis_client: Redis | None = None,
        user_service: UserService | None = None,
    ):
        self.db = db
        self.redis_client = redis_client
        self.user_service = user_service
        handlers = [
            ("/health_check", HealthCheckHandler),
            ("/user/signin", UserSigninHandler),
            ("/user/register", UserRegisterHandler),
        ]
        super().__init__(handlers)
