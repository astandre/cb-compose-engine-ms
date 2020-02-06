from kbsbot.compose_engine.app import create_app
from kbsbot.compose_engine.database import db, init_database
import os


# def main(args=sys.argv[1:]):
# def main():
#     # parser = argparse.ArgumentParser(description='Compose engine service')
#
#     # parser.add_argument("-d", "--deploy", default=False, help="Pass to generate app wsgi object", dest="deploy",
#     #                     action='store_true')
#     # parser.add_argument("-cf", "--config-file", help="Config file for app",
#     #                     type=str, default="", dest="config_file")
#     # args = parser.parse_args(args=args)
#     # app = create_app(args.config_file)
#     app = create_app()
#
#     host = app.config.get('host', '0.0.0.0')
#     port = app.config.get('port', 5000)
#     debug = app.config.get('DEBUG', False)
#     # if args.deploy is False:
#     # app.run(debug=debug, host=host, port=port, use_reloader=debug)
#     return app
#     # else:
#     #     print("bon voyage!")

def main():
    app = create_app()
    host = app.config.get('host', '0.0.0.0')
    port = app.config.get('port', 5000)
    debug = app.config.get('DEBUG', False)
    db.init_app(app)
    db.app = app
    db.create_all(app=app)
    init_database()
    app.run(debug=debug, host=host, port=port, use_reloader=debug)


if __name__ == "__main__":
    main()
else:
    _HERE = os.path.dirname(__file__)
    _SETTINGS = os.path.join(_HERE, 'settings.ini')
    print("bon voyage!")
    app = create_app(settings=_SETTINGS)
    db.init_app(app)
    db.app = app
    db.create_all(app=app)
    init_database()
