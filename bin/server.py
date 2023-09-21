import asyncio

import _paths  # noqa: F401
import aiomysql
from redis import asyncio as aioredis

from config.env_config import (
    APP_PORT,
    IS_DEBUG,
    MYSQL_HOST,
    MYSQL_PASSWD,
    MYSQL_PORT,
    MYSQL_USER,
    REDIS_DB,
    REDIS_HOST,
    REDIS_PORT,
)
from ds.aio_pool import AIOPool
from routes import Application
from services.user_service import UserService


async def main():
    async with aiomysql.create_pool(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWD,
        db="demo_db",
        pool_recycle=30,
        autocommit=True,
        cursorclass=aiomysql.DictCursor,
    ) as db_pool:
        db = AIOPool(db_pool, is_debug=IS_DEBUG)
        redis_client = aioredis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        user_service = UserService(
            db,
            redis_client,
        )
        app = Application(db, redis_client, user_service)
        app.listen(APP_PORT)

        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
