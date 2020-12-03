#!/bin/python3

try:
    from dugoutpull import DugoutPull
    from elasticsearchpush import ElasticsearchPush
except ImportError:
    from dugoutcrawler.dugoutpull import DugoutPull
    from dugoutcrawler.elasticsearchpush import ElasticsearchPush

import logging
import argparse
import json
from apscheduler.schedulers.blocking import BlockingScheduler


def main():
    parser = argparse.ArgumentParser(description="Start the Dugout Crawler")
    parser.add_argument(dest='config', type=str,
                help="The config file for server properties")
    parser.add_argument('-i', '--interval', dest='interval', type=int, default=5,
            help="The data crawl interval in minutes (default: 5).")
    parser.add_argument('-v', '--verbose', dest='verbosity', type=int, default=2,
                help="""Level of verbosity. Select between
                0 Nothing,
                1 Debug,
                2 Info (default),
                3 Warning,
                4 Error,
                5 Fatal""")
    args = parser.parse_args()

    logging.basicConfig(level=args.verbosity*10)
    logging.info("Starting Dugout Crawler with interval {}m".format(args.interval))

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

        dugout_address = config['dugoutserver']['address']
        dugout_port    = config['dugoutserver']['port']
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

    logging.debug("Initializing Dugout Puller")
    puller = None
    try:
        puller = DugoutPull(dugout_address, dugout_port)
    except Exception as msg:
        logging.error(msg)
        return

    def callback():
        logging.info('Performing crawl')
        data = puller.pull()
        pusher.bulk_push(index, data)

    scheduler = BlockingScheduler(timezone="Europe/Berlin")
    callback()
    try:
        logging.info("Dugout Crawler is ready")
        scheduler.add_job(callback, 'interval', minutes=args.interval, replace_existing=True)
        #scheduler.add_job(callback, 'interval', seconds=30, replace_existing=True)
        scheduler.start()
    except KeyboardInterrupt:
        pass
    except Exception as msg:
        logging.error(msg)


if __name__=="__main__":
    main()
