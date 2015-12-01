#!/usr/bin/env python
# coding:utf-8
__author__ = 'nekocode'


class Pagination:
    def __init__(self, db):
        self.db = db

    def get_page_rows(self, p, table_name, per_page_count=10, where=''):
        # 获取分页
        rows = self.db.query("SELECT * FROM %s %s ORDER BY id DESC LIMIT %d,%d"
                             % (table_name, where, per_page_count*(p-1), per_page_count))

        return rows

    def get_last_page(self, table_name, per_page_count=10, where=''):
        # 获取分页数量
        row_count = self.db.get("SELECT COUNT(*) FROM %s %s" % (table_name, where))['COUNT(*)']
        page_count = row_count/per_page_count + 1
        if row_count % per_page_count == 0:
            page_count -= 1

        return page_count


