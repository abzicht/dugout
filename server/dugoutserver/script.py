#!/bin/python3

try:
    from server import DugoutServer
    from sensors import DugoutSensors
except ImportError:
    from dugout.server import DugoutServer
    from dugout.sensors import DugoutSensors

import logging
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Start the Dugout server")
    parser.add_argument(dest='config', type=str,
                help="The config file for Sensor stuff")
    parser.add_argument('-a', '--address', dest='address', type=str,
                default= "127.0.0.1", help="The address or hostname to bind to")
    parser.add_argument('-p', '--port', dest='port', type=int, default=4321,
                help="The port to bind to")
    parser.add_argument('-v', '--verbose', dest='verbosity', type=int, default=20,
                help="""Level of verbosity. Select between
                0 Nothing,
                1 Debug,
                2 Info (default),
                3 Warning,
                4 Error,
                5 Fatal""")
    args = parser.parse_args()

    logging.basicConfig(level=args.verbosity*10)
    logging.info("Starting Dugout Server at {}:{}".format(args.address,args.port))

    config = None
    with open(args.config, 'r') as config_file:
        config = json.load(config_file)

    logging.debug("Initializing Dugout Sensors")
    sensors = DugoutSensors(config=config)

    logging.debug("Initializing Dugout Web Server")
    server = DugoutServer(args.address, args.port, sensors, config)

    def stop():
        logging.info("Stopping Dugout Server")
        server.stop()
        sensors.stop()
        logging.debug("Stopped Dugout Server")
    try:
        # so blocking:
        logging.info("Dugout Server is ready")
        server.serve()
    except KeyboardInterrupt:
        stop()


if __name__=="__main__":
    main()
