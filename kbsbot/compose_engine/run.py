from kbsbot.compose_engine.app import create_app
import sys
import os
import argparse


def _quit(signal, frame):
    print("Bye!")
    # add any cleanup code here
    sys.exit(0)


def main(args=sys.argv[1:]):
    print(args)
    parser = argparse.ArgumentParser(description='Runnerly Dataservice')

    parser.add_argument('--fd', type=int, default=None)
    parser.add_argument('--config-file', help='Config file',
                        type=str, default=None)
    args = parser.parse_args(args=args)

    app = create_app(args.config_file)
    # app = create_app()
    host = app.config.get('host', '0.0.0.0')
    port = app.config.get('port', 5000)
    debug = app.config.get('DEBUG', False)
    # app.run(debug=debug, host=host, port=port, use_reloader=debug)

    if args.fd is not None:
        # use chaussette
        app = create_app(args.config_file)
    else:
        app.run(debug=debug, host=host, port=port, use_reloader=debug)


if __name__ == "__main__":
    main()
# else:
#     _HERE = os.path.dirname(__file__)
#     _SETTINGS = os.path.join(_HERE, 'settings.ini')
#     print(_SETTINGS)
#     app = create_app(settings=_SETTINGS)
