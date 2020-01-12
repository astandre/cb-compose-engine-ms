from kbsbot.compose_engine.app import create_app
import sys
import argparse


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Runnerly Dataservice')

    parser.add_argument("-d", "--deploy", default=False, help="Pass to generate app wsgi object", dest="deploy",
                        action='store_true')
    parser.add_argument("-cf", "--config-file", help="Config file for app",
                        type=str, default="", dest="config_file")
    args = parser.parse_args(args=args)
    app = create_app(args.config_file)

    host = app.config.get('host', '0.0.0.0')
    port = app.config.get('port', 5000)
    debug = app.config.get('DEBUG', False)
    if args.deploy is False:
        app.run(debug=debug, host=host, port=port, use_reloader=debug)
    else:
        print("bon voyage!")


if __name__ == "__main__":
    main()
