from kazoo.client import KazooClient
import logging
import sys
import argparse
import json
import os

import platform
import getpass

from kazoo.recipe.barrier import DoubleBarrier
from version import __version__


def init_logger():
    logging.basicConfig()
    logger = logging.getLogger()

    h = logging.StreamHandler(sys.stdout)
    h.flush = sys.stdout.flush
    logger.addHandler(h)

    return logger


def user_input():
    parser = argparse.ArgumentParser(description='zkbarrier - Zookeeper Barrier '
                                                 'Client barrier')

    parser.add_argument('-r', '--replicas', type=int, help='Number of service replicas', default=3,
                        choices=xrange(2, 10))
    parser.add_argument('-z', '--zookeeper', help='Zookeeper server connection url zkhost:port', default='zk:2181')
    parser.add_argument('-d', '--debug', help='Enable debug logging', action='store_true')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    args = parser.parse_args()
    arguments = vars(args)
    records = [arguments]

    config = argparse.ArgumentParser()
    config.add_argument('-cf', '--config_file', help='config file name', default='', type=str, required=False)
    config_file_check = config.parse_known_args()
    object_check = vars(config_file_check[0])

    if object_check['config_file'] != '':
        records = []
        json_file = json.load(open(config_file_check[0].config_file))
        for record in range(0, len(json_file['Records'])):
            arguments = {}
            for key, value in json_file['Records'][record].items():
                arguments[key] = value
            records.append(arguments)

    return records


def main():
    records = user_input()

    for arguments in records:
        print arguments['replicas']
        print arguments['zookeeper']

        if arguments['debug']:
            logging.getLogger().setLevel(logging.DEBUG)

        logging.info('%scmd started with Python %s and User %s',
                     os.path.splitext(os.path.basename(sys.argv[0]))[0].upper(),
                     platform.python_version(), getpass.getuser())

        number_svc_replicas = arguments['replicas']
        group_name = "barrier_group"
        zk_path = "/" + group_name + "/barrier/g" + str(number_svc_replicas)
        logger = init_logger()

        print("Max elements in the group " + (str(number_svc_replicas)))

        zk = KazooClient(hosts=arguments['zookeeper'])
        zkb = DoubleBarrier(zk, zk_path, number_svc_replicas)

        print("Starting the client")
        zk.start()
        print("Entering in the barrier and waiting for the group")
        zkb.enter()

        # Note, if you disable the leaving code the clients will no longer
        # wait in the barrier after the first time the group leaves it.
        # This can be useful sometimes.
        print("leaving the barrier")
        zkb.leave()

        # finish
        zk.stop()
        print("bye")


if __name__ == "__main__":
    main()
