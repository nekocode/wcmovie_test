#!/usr/bin/env python
# coding:utf-8

import tornado.ioloop
import tornado.options
import tornado.httpserver
from application import application
from tornado.options import define, options, parse_command_line
from tokens import TokensRefreshTask

define("port", type=int, default=80, help="run on th given port")


def main():
    parse_command_line()

    TokensRefreshTask().start()

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print 'Server is running at http://127.0.0.1:%s/' % options.port
    print 'Quit the server with Control-C'
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
