import json
import tornado.ioloop
from tornado_json.routes import get_routes
from tornado_json.application import Application


def main():
    import slink
    routes = get_routes(slink)
    print("Routes\n======\n\n" + json.dumps(
        [(url, repr(rh)) for url, rh in routes],
        indent=2)
          )
    application = Application(routes=routes, settings={})

    application.listen(7777)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
