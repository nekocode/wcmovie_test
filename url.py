#!/usr/bin/env python
# coding:utf-8

import sys
from handler.test import TestHandler, ResultHandler
from handler.admin.log import *
from handler.admin.app import *
from handler.admin.answer import *

reload(sys)
sys.setdefaultencoding('utf-8')


url = [
    (r'/test/admin/login', LoginHandler),
    (r'/test/admin/logout', LogoutHandler),

    (r'/test/admin/app', AppQueryHandler),
    (r'/test/admin/app/(.*)', AppEditHandler),

    (r'/test/admin/answer', AnswerQueryHandler),
    (r'/test/admin/answer/(.*)', AnswerEditHandler),

    (r'/test/(.*)/result', ResultHandler),
    (r'/test/(.*)', TestHandler),
]
