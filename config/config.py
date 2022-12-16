import configparser
import os
import json
from controller import gvar

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
