#!/bin/python3

try:
    from dugoutowm import DugoutOWM
    from elasticsearchpush import ElasticsearchPush
except ImportError:
    from dugoutweathercrawler.dugoutowm import DugoutOWM
    from dugoutweathercrawler.elasticsearchpush import ElasticsearchPush

import logging
import argparse
import json
from apscheduler.schedulers.blocking import BlockingScheduler


def main():
    parser = argparse.ArgumentParser(description="Start the Dugout Weather Crawler")
    parser.add_argument(dest='config', type=str,
                help="The config file for server properties")
    parser.add_argument('-i', '--interval', dest='interval', type=int,
            default=15,
            help="The data crawl interval in minutes (default: 15).")
    parser.add_argument('-v', '--verbose', dest='verbosity', type=int,
            default=2,
                help="""Level of verbosity. Select between
                0 Nothing,
                1 Debug,
                2 Info (default),
                3 Warning,
                4 Error,
                5 Fatal""")
    args = parser.parse_args()

    logging.basicConfig(level=args.verbosity*10)
    logging.info("Starting Dugout Weather Crawler with interval {}m".format(args.interval))

    config = None
    with open(args.config, 'r') as config_file:
        config = json.load(config_file)

    try:
        es_address = config['elasticsearch']['address']
        es_port    = config['elasticsearch']['port']
        username   = config['elasticsearch']['username']
        password   = config['elasticsearch']['password']
        index      = config['elasticsearch']['index']
        mapping    = config['elasticsearch']['mapping']

        owm_api_key = config['owm']['api_key']
        owm_location = config['owm']['location']
    except Exception as msg:
        raise Exception('Unable to initialize config file at {}: {}'.format(args.config,msg))

    logging.debug("Initializing Elasticsearch Pusher")
    pusher = None
    try:
        pusher = ElasticsearchPush(es_address, es_port, username, password)
        pusher.create_index(index, mapping)
    except Exception as msg:
        logging.error(msg)
        return

    logging.debug("Initializing OWM Crawler")
    owmshell = None
    try:
        owmshell = DugoutOWM(owm_api_key, owm_location)
    except Exception as msg:
        logging.error(msg)
        return

    def callback():
        logging.info('Performing crawl')
        data = owmshell.pull()
        logging.debug(data)
        id_ = data['timestamp']
        pusher.push(index, id_, data)

    scheduler = BlockingScheduler(timezone="Europe/Berlin")
    callback()
    try:
        logging.info("Dugout Weather Crawler is ready")
        scheduler.add_job(callback, 'interval', minutes=args.interval, replace_existing=True)
        #scheduler.add_job(callback, 'interval', seconds=30, replace_existing=True)
        scheduler.start()
    except KeyboardInterrupt:
        pass
    except Exception as msg:
        logging.error(msg)


if __name__=="__main__":
    main()
