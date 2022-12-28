import time
import json
import controller.control
from controller import pool
import bs4
from controller import gvar
from logger import logger
from qqzone import api
from config import config
from Handler import MsgHandler
import re
import sys
import os

FirstTime = int(time.time())


def Change(html_text):
    Change_list = [
        ["\\x3C", "<"],
        ["\\x22", '"'],
        [r"\/", "/"]
    ]
    tmp_html = html_text
    # print(Change_list)
    for i in Change_list:
        tmp_html = tmp_html.replace(i[0], i[1])
    return tmp_html


def Msg_Process_Handle(controler, extraparam="", BeginTime=""):
    if not controller.control.RunningFlag:
        return False
    Msg = api.Msg_Get(extraparam, BeginTime)
    global FirstTime
    if Msg == "":
        return False
    try:
        abstime = re.compile(r"(?<=abstime:').*?(?=')").findall(Msg)[0]
    except Exception as e:
        logger.logger.debug(Msg)
        logger.logger.error("解析出错" + repr(e))
        try:

            reson = json.loads(Msg.replace("_Callback(", "").replace(");", "").replace("\n", ""))
            if reson["code"] == -3000:
                logger.logger.error("登录过期:需要重新登录")
                controller.control.ExitRequests("", "")
            if reson["code"] == -10001:
                logger.logger.warning("网络繁忙，将重试")
                time.sleep(5)
                Msg_Process_Handle(controler, extraparam, BeginTime)
            logger.logger.debug("原因:" + reson)
        except:
            pass
            # logger.logger.error("原因查看日志文件")

        return True
    if controler == 1:
        FirstTime = int(abstime)
        gvar.set_value("ftime", FirstTime)

    extraparam = re.compile(r"(?<=,externparam:').*?(?=')").findall(Msg)[0]
    BeginTime = re.compile(r"(?<=,begintime:').*?(?=')").findall(Msg)[0]
    htmls = re.compile(r"(?<=,html:').*?(?=')").findall(Msg)
    uins = re.compile(r"(?<=,uin:').*?(?=')").findall(Msg)
    nicknames = re.compile(r"(?<=,nickname:').*?(?=')").findall(Msg)
    keys = re.compile(r"(?<=,key:').*?(?=')").findall(Msg)
    abstimes = re.compile(r"(?<=,abstime:').*?(?=')").findall(Msg)
    for index in range(len(keys)):
        # 屏蔽广告
        if "20050606" == uins[index]:
            continue
        if " advertisement" in nicknames[index]:
            continue
        if gvar.get_value("db").exists(keys[index]) and not config.getConfig("AutoRefresh"):
            continue
        self_html = Change(htmls[index])
        pool.pool_submit(MsgHandler.Handle(self_html, uins[index], nicknames[index], keys[index], abstimes[index]))

    if int(abstimes[0]) >= config.getConfig("timestamp"):
        # print(int(abstimes[len(abstimes) - 1]),int(abstimes[0]))
        time.sleep(1)
        Msg_Process_Handle(controler + 1, extraparam, BeginTime)
        return True
    else:
        config.setConfig("timestamp", gvar.get_value("ftime"))
        return True


def Loop_Start():
    config.show_config()
    while controller.control.RunningFlag:
        Msg_Process_Handle(1)
        for i in range(int(config.getConfig("timesleep")) // 1):
            if not controller.control.RunningFlag:
                break
            time.sleep(1)
