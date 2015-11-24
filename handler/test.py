#!/usr/bin/env python
# coding:utf-8

from tornado.web import RequestHandler
import hashlib
from optsql.db import db


class TestHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, app_id):
        try:
            app_id = int(app_id)
            app = db.get("SELECT * FROM app WHERE app_id=%d" % app_id)

            if app is None:
                raise Exception("does not have this id")

        except Exception, e:
            self.write(u"Err：APP not found, " + e.message)
            return

        count = db.get("SELECT COUNT(*) AS COUNT FROM answer WHERE app_id=%d" % app_id).COUNT
        if count == 0:
            self.write("This APP has no answers")
            return

        input_str = self.get_argument("input", None)
        if input_str is None:
            self.write("Input is none")
            return

        md5impl = hashlib.md5()
        md5impl.update(input_str)
        answer_row = int(md5impl.hexdigest(), 16) % count

        answer = db.get("SELECT * FROM answer WHERE app_id=%d LIMIT %d,1;" % (app_id, answer_row))

        self.write(str(answer))


