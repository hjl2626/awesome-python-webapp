# -*- coding: UTF-8 -*-
"""
@version: ??
@site: 
@software: PyCharm
@file: db.py
@time: 2015/12/4 23:09
"""

# 数据库引擎对象:
import threading


class _Engine(object):
    def __init__(self, connect):
        self._connect = connect

    @property
    def connect(self):
        return self._connect()

    @connect.setter
    def connect(self, conn):
        self._connect = conn


engine = None


# 持有数据库连接的上下文对象:
class _DbCtx(threading.local):
    def __init__(self):
        self.connection = None
        self.transactions = 0

    def is_init(self):
        return not self.connection is None

    def init(self):
        self.connection = _LasyConnection()
        self.transactions = 0

    def cleanup(self):
        self.connection.cleanup()
        self.connection = None

    def cursor(self):
        return self.connection.cursor()


_db_ctx = _DbCtx()


# 定义了 __enter__() 和 __exit__() 的对象可以用于with语句，确保任何情况下 __exit__() 方法可以被调用.
# 把 _ConnectionCtx 的作用域作用到一个函数调用上，可以这么写：
#       with connection():
#           do_some_db_operation()
# 但是更简单的写法是写个@decorator：
#       @with_connection
#       def do_some_db_operation():
#           pass
class _ConnectionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()


def connection():
    return _ConnectionCtx()


class _TransactionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_close_conn = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_close_conn = True
            _db_ctx.transactions += 1
        return self

    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        _db_ctx.transactions -= 1
        try:
            if _db_ctx.transactions == 0:
                if exctype is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_close_conn:
                _db_ctx.cleanup()

    # noinspection PyBroadException
    @staticmethod
    def commit():
        global _db_ctx
        try:
            _db_ctx.connection.commit()
        except:
            _db_ctx.connection.rollback()
        raise

    @staticmethod
    def rollback():
        global _db_ctx
        _db_ctx.connection.rollback()


if __name__ == '__main__':
    pass
