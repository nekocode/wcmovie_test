#!/usr/bin/env python
# coding:utf-8

from tornado.web import RequestHandler
import hashlib
from optsql.db import db


class BaseHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, application, request, **kwargs):
        RequestHandler.__init__(self, application, request, **kwargs)

    def get_app(self, app_id):
        try:
            app_id = int(app_id)
            app = db.get("SELECT * FROM app WHERE id=%d" % app_id)

            if app is None:
                raise Exception("does not have this id")
            return app_id, app

        except Exception, e:
            self.write(u"Err：APP not found, " + e.message if e.message is not '' else str(e.args))
            return None, None

    @staticmethod
    def update_pv(app_id, pv, fake_pv):
        sql = "UPDATE app SET pv=%d, fake_pv=%d WHERE id=%d" % (pv, fake_pv, app_id)
        db.update(sql)


class TestHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, app_id):
        app_id, app = self.get_app(app_id)
        if app is None:
            return

        BaseHandler.update_pv(app_id, app.pv+1, app.fake_pv+1)
        self.render('index.html', app=app)

    def post(self, app_id):
        app_id, app = self.get_app(app_id)
        if app is None:
            return

        input_str = self.get_argument("name")
        self.redirect('/test/%d/result?input=%s' % (app_id, input_str), permanent=True)


class ResultHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, app_id):
        input_str = self.get_argument("input", None)
        if input_str is None:
            self.write("Input is none")
            return

        app_id, app = self.get_app(app_id)
        if app is None:
            return

        count = db.get("SELECT COUNT(*) AS COUNT FROM answer WHERE app_id=%d" % app_id).COUNT
        if count == 0:
            self.write("This APP has no answers")
            return

        md5impl = hashlib.md5()
        md5impl.update(input_str)
        answer_row = int(md5impl.hexdigest(), 16) % count

        answer = db.get("SELECT * FROM answer WHERE app_id=%d LIMIT %d,1;" % (app_id, answer_row))

        BaseHandler.update_pv(app_id, app.pv+1, app.fake_pv+1)
        self.render('result.html', input_str=input_str, app=app, answer=answer, retest_url="/test/%d" % app_id)


