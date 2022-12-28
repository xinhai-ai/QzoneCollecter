import sys
import time

import controller.pool
import logger.logger

RunningFlag = True
Force = False


def ExitRequests(a,b):
    global Force
    if Force:
        logger.logger.logger.error("强制退出")
        sys.exit(0)

    if not Force:
        Force=True
    global RunningFlag
    RunningFlag = False
    logger.logger.logger.info(f"等待线程结束...")
    logger.logger.DisableConsole()
    while controller.pool.get_thread_num()>0:
        logger.logger.logger.info(f"还有{controller.pool.get_thread_num()}条线程在工作...")
        time.sleep(1)
    sys.exit(0)

