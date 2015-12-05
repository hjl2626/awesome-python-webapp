# -*- coding: UTF-8 -*-
"""
@version: ??
@site: 
@software: PyCharm
@file: test.py
@time: 2015/12/5 12:35
"""
import logging, time
import db

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    db.create_engine('root', '123456', 'test')
    db.update('drop table if exists user')
    db.update('create table user (id VARCHAR(50) primary key, name text, email text, passwd text, last_modified real)')
    u1 = dict(id=db.next_id(), name='Michael', email='michael@test.org', passwd='123456', last_modified=time.time())
    db.insert('user', **u1)