import tornado.ioloop
import tornado.options
from tornado.options import define, options

from nbgraderapi import Application

define("host", default="", help="host address")
define("port", default=8080, help="port number", type=int)
define("debug", default=False, help="debug mode", type=bool)
define("db_url", default="sqlite:///:memory:", help="database url")
define("auth_token", default="", help="authorization token")


if __name__ == "__main__":
    try:
        tornado.options.parse_command_line()
        print("Server listening on port {}".format(options.port))

        app = Application(options.db_url,
                          debug=options.debug,
                          auth_token=options.auth_token)
        app.listen(options.port, options.host)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("\nStop server")
