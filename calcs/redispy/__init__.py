from collections import defaultdict
import time
import random

from redis import Redis
from redis.exceptions import ConnectionError


class MaxRetriesExceeded(Exception):
    pass


pool = dict()


def get_connection(db, host='redis', port=6379, max_retries=3, time_sleep=2):
    try:
        pool[db].ping()
        return pool[db]
    except (ConnectionError, KeyError):
        for attempt in range(max_retries):
            pool[db] = Redis(host=host, port=port, db=db)
            try:
                pool[db].ping()
                return pool[db]
            except ConnectionError as err:
                time.sleep(time_sleep + abs(random.random()))
                time_sleep *= 2
                continue

    raise MaxRetriesExceeded


