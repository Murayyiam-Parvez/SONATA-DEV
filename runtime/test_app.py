#!/usr/bin/python
# Initialize coloredlogs.
import logging
import sys

print sys.path
logging.getLogger("testApp")

import coloredlogs

coloredlogs.install(level='ERROR',)

from runtime import *
import sys
print sys.path

from query_engine.sonata_queries import *

batch_interval = 1
window_length = 10
sliding_interval = 10
T = 1000*window_length

featuresPath = ''
redKeysPath = ''

if __name__ == "__main__":

    spark_conf = {'batch_interval': batch_interval, 'window_length': window_length, 'sliding_interval': sliding_interval, 'featuresPath': featuresPath, 'redKeysPath': redKeysPath, 'sm_socket':('localhost',5555),
                  'op_handler_socket': ('localhost', 4949)}

    emitter_conf = {'spark_stream_address': 'localhost',
                    'spark_stream_port': 8989,
                    'sniff_interface': "out-veth-2"}

    conf = {'dp': 'p4', 'sp': 'spark',
            'sm_conf': spark_conf, 'emitter_conf': emitter_conf,
            'fm_socket': ('localhost', 6666)}

    query = (PacketStream()
                    .filter(keys=("proto",), values=('6',), comp = "eq")
                    .map(keys=("dIP", "sIP"))
                    .distinct()
                    .map(keys=("dIP",), values = ("1",))
                    .reduce(func='sum', values=('count',))
                    #.filter(expr='count > 2')
                    .map(keys=('dIP',)))

    queries = []
    queries.append(query)
    runtime = Runtime(conf, queries)
    #runtime.send_to_sm()
