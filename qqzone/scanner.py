import json
import re
import sys
import time

import controller.control
from Handler import MsgLoop
from Handler import MsgHandler
from qqzone import api
from controller import pool
from logger import logger


def scan(uin):
    counter = 0
    error = 0
    while 1:
        time.sleep(0.3)
        Msg = api.get_one_zone(uin, counter, 10)
        try:
            code = re.compile(r"""(?<="code":).*?(?=,)""").findall(Msg)[0]
            message = re.compile(r"""(?<="message":).*?(?=,)""").findall(Msg)[0]
            try:
                tips = re.compile(r"""(?<="tips":).*?(?=,)""").findall(Msg)[0]
                if tips == "0103-247":
                    logger.logger.error("无法访问")
            except:
                pass
        except:
            code = ""
            tips = ""
            error+=1
            if error> 10:
                logger.logger.critical("错误次数过多")
                controller.control.ExitRequests("","")
            logger.logger.error(sys.exc_info()[1])
            continue

        htmls = re.compile(r"(?<=,html:').*?(?=')").findall(Msg)
        uins = re.compile(r"(?<=,uin:').*?(?=')").findall(Msg)
        nicknames = re.compile(r"(?<=,nickname:').*?(?=')").findall(Msg)
        keys = re.compile(r"(?<=,key:').*?(?=')").findall(Msg)
        abstimes = re.compile(r"(?<=,abstime:').*?(?=')").findall(Msg)
        has_more_data = ""
        try:
            has_more_data = re.compile(r"(?<=hasMoreFeeds_0:).*?(?=,)").findall(Msg)[0]
        except:

            logger.logger.error(str(sys.exc_info()[1]) + " 重试")
            logger.logger.error(code + " " + message)
            logger.logger.debug(Msg)
            error += 1
            if error > 10:
                logger.logger.error("错误次数过多")
                controller.control.ExitRequests("", "")
            continue
        for i in range(len(htmls)):
            nickname = nicknames[i]
            html = MsgLoop.Change(htmls[i])
            key = keys[i]
            abstime = abstimes[i]
            uin_i = uins[i]
            pool.pool_submit(MsgHandler.Handle(html, uin_i, nickname, key, abstime, False))
        if has_more_data == "true":
            error = 0
            counter += 10
            continue
        elif has_more_data == "false":
            logger.logger.info(str(uin) + "爬取完成...")
            controller.control.ExitRequests("", "")
        else:
            logger.logger.error("未知错误")
            continue
