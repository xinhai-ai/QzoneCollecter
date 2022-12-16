from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import time

import logger.logger

pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() + 1)
running = []


def deleteFromRunning(future):
    global running
    running.remove(future)


def pool_submit(*kwg):
    global running
    if len(running) >= 100:
        logger.logger.logger.warning("触发线程池上限...")
    while len(running) >= 100:
        time.sleep(0.1)
    future = pool.submit(*kwg)
    running.append(future)
    future.add_done_callback(deleteFromRunning)


def get_thread_num():
    global running
    return len(running)
