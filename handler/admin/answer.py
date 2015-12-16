#!/usr/bin/env python
# coding:utf-8
import json
import uuid
import MySQLdb
from qiniu import Auth, put_data

from tornado import escape
from tornado.web import authenticated, os
from base import BaseHandler, pagination
import config
from optsql.db import db


class AnswerQueryHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        app_id = int(self.get_argument('app_id',  int(self.get_cookie('app_id', 1))))
        apps = db.query("SELECT * FROM app")

        if len(apps) == 0:
            self.write(u'你还未创建任何 APP')
            return

        finded = False
        for app in apps:
            if app.id == app_id:
                finded = True
                break

        if finded is False:
            app_id = apps[0].id

        self.set_cookie('app_id', str(app_id))
        rows = db.query("SELECT * FROM answer WHERE app_id=%d" % app_id)
        self.render('admin/answers.html', app_id=app_id, apps=apps, rows=rows)


class AnswerEditHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, action):
        if action == 'add':
            app_id = int(self.get_argument('app_id',  int(self.get_cookie('app_id', -1))))
            if app_id == -1:
                self.write(u'缺少 app_id 参数')
                return

            self.render('admin/answer_edit.html', action=action)

        elif action == 'edit':
            _id = int(self.get_argument('id', 1))
            answer = db.get('SELECT * FROM answer WHERE id=%d' % _id)

            if answer is None:
                self.write(u'找不到该答案')
                return

            self.render('admin/answer_edit.html', action=action, answer=answer)

        elif action == 'delete':
            _id = int(self.get_argument('id', 1))
            answer = db.get('SELECT * FROM answer WHERE id=%d' % _id)

            if answer is None:
                self.write(json.dumps(dict(flag=False, message='未找到该答案')))
                return

            sql = "DELETE FROM answer WHERE id=%d" % _id
            db.delete(sql)

            self.write("删除成功")

    def post(self, action):
        self.set_header('Content-Type', 'text/json')

        if action == 'add':
            app_id = int(self.get_argument('app_id', -1))
            if app_id == -1:
                self.write(u'缺少 app_id 参数')
                return

            logo_url = self.get_file_uploaded_url('logo_url')
            if logo_url is None:
                self.write(json.dumps(dict(flag=False, message='图片上传到七牛失败')))
                return

            sql = "INSERT INTO answer(app_id, logo_url, title, subtitle, content) " \
                  "VALUES(%d, '%s', '%s', '%s', '%s')" \
                  % (app_id,
                     MySQLdb.escape_string(logo_url),
                     MySQLdb.escape_string(self.get_body_argument('title')),
                     '',
                     MySQLdb.escape_string(self.get_body_argument('content')),)

            db.insert(sql)
            self.write(json.dumps(dict(flag=True, url='/test/admin/answer?app_id=%d' % app_id)))

        elif action == 'edit':
            _id = int(self.get_argument('id', 1))
            answer = db.get('SELECT * FROM answer WHERE id=%d' % _id)

            if answer is None:
                self.write(u'找不到该答案')
                return

            logo_url = self.get_file_uploaded_url('logo_url')
            if logo_url is None:
                self.write(json.dumps(dict(flag=False, message='图片上传到七牛失败')))
                return

            sql = "UPDATE answer SET logo_url='%s', title='%s', " \
                  "subtitle='%s', content='%s' WHERE id=%d" \
                  % (MySQLdb.escape_string(logo_url),
                     MySQLdb.escape_string(self.get_body_argument('title')),
                     "",
                     MySQLdb.escape_string(self.get_body_argument('content')),
                     _id)

            db.update(sql)
            self.write(json.dumps(dict(flag=True, url='/test/admin/answer')))

    def get_file_uploaded_url(self, name):
        if name in self.request.files:
            fileinfo = self.request.files[name][0]
            fname = fileinfo['filename']
            body = fileinfo['body']

            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn

            q = Auth(config.QINIU_AK, config.QINIU_SK)
            key = 'upload/' + cname
            token = q.upload_token(config.QINIU_BUCKET_NAME)
            ret, info = put_data(token, key, body)

            if info.status_code == 200:
                return 'http://7xon5f.com2.z0.glb.qiniucdn.com/' + key
            else:
                return None

        return ''
