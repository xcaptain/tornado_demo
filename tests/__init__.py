import aiomysql
from redis import asyncio as aioredis
from tornado.testing import AsyncHTTPTestCase

from ds.aio_pool import AIOPool
from routes import Application
from services.user_service import UserService


class BaseTestCase(AsyncHTTPTestCase):
    access_token = ""

    def get_app(self):
        self.db_pool = self.io_loop.run_sync(
            lambda: aiomysql.create_pool(
                host="127.0.0.1",
                port=3306,
                user="root",
                password="",
                db="demo_db",
                pool_recycle=30,
                autocommit=True,
                cursorclass=aiomysql.DictCursor,
            )
        )
        self.redis_client = aioredis.Redis(host="127.0.0.1", port=6379, db=0)
        db = AIOPool(self.db_pool, is_debug=True)
        user_service = UserService(
            db=db,
            redis=self.redis_client,
            jwt_secret="123456",
        )
        app = Application(
            db=db,
            redis_client=self.redis_client,
            user_service=user_service,
        )
        return app

    def tearDown(self) -> None:
        self.db_pool.close()
        self.io_loop.run_sync(self.db_pool.wait_closed)
        self.io_loop.run_sync(self.redis_client.close)
        return super().tearDown()
