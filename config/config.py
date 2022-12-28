import configparser
import os
import json
import time

from controller import gvar
from logger import logger

path = os.path.split(os.path.realpath(__file__))[0] + '/db.conf'


def getConfig(key):
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")
    return json.loads(config.get("config", key))


def setConfig(key, value):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/db.conf'
    config.read(path, encoding="utf-8")
    config.set("config", key, json.dumps(value))
    config.write(open(path, "w", encoding="utf-8"))


def has_key(key):
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")
    return config.has_option("config", key)


def get_sections():
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")
    return config.sections()


def init():
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")
    config.add_section("config")
    config.write(open(path, "w", encoding="utf-8"))


def load():
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")
    for i in config["config"].keys():
        gvar.set_value(i, json.loads(config["config"][i]))

def show_config():
    time.sleep(0.2)
    logger.logger.info("排除点赞个数: "+str(len(getConfig("likeunincluded"))))
    time.sleep(0.2)
    logger.logger.info("禁用系统消息: "+str(getConfig("disablenotification")))
    time.sleep(0.2)
    logger.logger.info("自动刷新已有动态: "+str(getConfig("autorefresh")))
    time.sleep(0.2)
    logger.logger.info("刷新间隔: "+str(getConfig("timesleep"))+"秒")
    