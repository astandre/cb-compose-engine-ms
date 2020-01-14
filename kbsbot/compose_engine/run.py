from kbsbot.compose_engine.app import create_app
# import sys
# import argparse
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


if __name__ == "__main__":
    _HERE = os.path.dirname(__file__)
    _SETTINGS = os.path.join(_HERE, 'settings.ini')
    app = create_app(settings=_SETTINGS)
    # app = create_app()
    host = app.config.get('host', '0.0.0.0')
    port = app.config.get('port', 5000)
    debug = app.config.get('DEBUG', False)
    app.run()
else:
    _HERE = os.path.dirname(__file__)
    _SETTINGS = os.path.join(_HERE, 'settings.ini')
    print("bon voyage!")
    app = create_app(settings=_SETTINGS)
