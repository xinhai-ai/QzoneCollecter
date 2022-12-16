import sys

import controller.pool
import logger.logger

RunningFlag = True
Force = False


def ExitRequests(signum, frame):
    global Force
    if Force:
        logger.logger.logger.error("强制退出")
        sys.exit(0)

    if not Force:
        Force=True
    global RunningFlag
    RunningFlag = False
    logger.logger.DisableConsole()
    logger.logger.logger.info(f"等待线程结束...")
