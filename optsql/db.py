#!/usr/bin/env python
# coding:utf-8
import config
import torndb

db = torndb.Connection(config.DB_HOST, config.DB_NAME, config.DB_USER, config.DB_PWD)


def create_tables():
    if if_table_exist('app') == 0:
        db.execute("CREATE TABLE app(id INTEGER PRIMARY KEY AUTO_INCREMENT, "
                   "name VARCHAR(20) NOT NULL, qrcode_url VARCHAR(512) NOT NULL, "
                   "bg_url VARCHAR(512) NOT NULL, question VARCHAR(64) NOT NULL, intro VARCHAR(128) NOT NULL, "
                   "input_label VARCHAR(10) NOT NULL, answer_prefix VARCHAR(64) NOT NULL, "
                   "active BOOLEAN NOT NULL)")

    if if_table_exist( 'answer') == 0:
        db.execute("CREATE TABLE answer(id INTEGER PRIMARY KEY AUTO_INCREMENT, "
                   "app_id INTEGER NOT NULL, logo_url VARCHAR(512) NOT NULL, "
                   "title VARCHAR(64) NOT NULL, subtitle VARCHAR(128) NOT NULL, content VARCHAR(256) NOT NULL)")


def if_table_exist(table_name):
    count = db.get("select count(*) as count from information_schema.tables "
                   "where table_schema ='" + config.DB_NAME + "' and table_name ='" + table_name + "'")
    return count.count


if __name__ == '__main__':
    create_tables()

