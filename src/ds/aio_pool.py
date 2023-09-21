import logging

from aiomysql import Pool


class AIOPool:
    def __init__(self, pool: Pool, is_debug=False):
        self.pool = pool
        self.is_debug = is_debug

    async def execute(self, query, params=None):
        """Execute query in pool.

        Returns future yielding closed cursor.
        You can get rows, lastrowid, etc from the cursor.

        :return: Future of cursor
        :rtype: Future
        """
        async with self.pool.acquire() as conn:
            cur = await conn.cursor()
            await cur.execute(query, params)
            await cur.close()
            return cur

    async def execute_many(self, stmt, params=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                if self.is_debug:
                    sql = cur.mogrify(stmt, params)
                    logging.info("try execute_many sql=%s", sql)
                affected_count = await cur.executemany(stmt, params)
                return affected_count

    async def query(self, stmt, params=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                if self.is_debug:
                    sql = cur.mogrify(stmt, params)
                    logging.info("try query sql=%s", sql)
                await cur.execute(stmt, params)
                return await cur.fetchall()

    async def _get_conn(self):
        return await self.pool.acquire()

    async def _put_conn(self, conn):
        await self.pool.release(conn)

    def _close_conn(self, conn):
        conn.close()

    async def begin(self):
        """Start transaction

        Wait to get connection and returns `Transaction` object.

        :return: Future[Transaction]
        :rtype: Future
        """
        conn = await self._get_conn()
        try:
            await conn.begin()
        except:
            self._close_conn(conn)
            raise
        return Transaction(self, conn)


class Transaction(object):
    """Represents transaction in pool"""

    def __init__(self, pool, conn):
        self._pool = pool
        self._conn = conn
        self.is_debug = pool.is_debug

    def _ensure_conn(self):
        if self._conn is None:
            raise Exception("Transaction is closed already")

    async def _close(self):
        if hasattr(self, "_cur"):
            await self._cur.close()
        await self._pool._put_conn(self._conn)
        self._pool = self._conn = self._cur = None

    async def execute(self, query, args=None):
        """
        :return: Future[Cursor]
        :rtype: Future
        """
        self._ensure_conn()
        if not hasattr(self, "_cur"):
            self._cur = await self._conn.cursor()  # self.cur is _ContextManager(fut)
        if self.is_debug:
            sql = self._cur.mogrify(query, args)
            logging.info("trx going to execute sql=%s", sql)
        await self._cur.execute(query, args)
        return self._cur

    async def execute_many(self, query, args=None):
        """
        :return: Future[Cursor]
        :rtype: Future
        """
        self._ensure_conn()
        if not hasattr(self, "_cur"):
            self._cur = await self._conn.cursor()  # self.cur is _ContextManager(fut)
        if self.is_debug:
            sql = self._cur.mogrify(query, args)
            logging.info("trx going to execute_many sql=%s", sql)
        await self._cur.executemany(query, args)
        return self._cur

    async def commit(self):
        self._ensure_conn()
        await self._conn.commit()
        await self._close()

    async def rollback(self):
        self._ensure_conn()
        await self._conn.rollback()
        await self._close()

    def __del__(self):
        if self._pool is not None:
            logging.warn("Transaction has not committed or rollbacked.")
            self._pool._close_conn(self._conn)
