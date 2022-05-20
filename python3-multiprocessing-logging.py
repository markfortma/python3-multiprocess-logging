#!/usr/bin/env python3

import logging
import logging.handlers
import multiprocessing
import time

def count_it(digit, q):
    logger = logging.getLogger(count_it.__name__)
    logger.addHandler(logging.handlers.QueueHandler(q))
    for n in range(digit):
        logger.info('count is at %d' % (n))
        time.sleep(1)


if __name__ == '__main__':
    q = multiprocessing.Queue()
    daemon_pool = []
    root_format = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s,%(lineno)d %(process)d %(thread)d %(message)s')
    root_handler = logging.handlers.RotatingFileHandler(__file__.replace('.py', '.log'), maxBytes=10240, backupCount=3)
    root_handler.setFormatter(root_format)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_listener = logging.handlers.QueueListener(q, root_handler)
    root_listener.start()

    for n in range(4):
        p = multiprocessing.Process(target=count_it, args=(100, q,))
        daemon_pool.append(p)
        p.start()

    for p in daemon_pool:
        p.join()

