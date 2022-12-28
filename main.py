import time
import sys
import controller.control
from controller import gvar
from controller import pool
from config import config
from logger import logger
import signal
from database import db
from qqzone import api
from Handler import MsgLoop
import argparse
gvar._init()
gvar.set_value("db",db.DB())

parser = argparse.ArgumentParser()
parser.add_argument("-csv","-c",required=False)
parser.add_argument("-scan","-s",required=False)

args = parser.parse_args()
if args.xml is not None:
    from exporter import export
    export.export(str(args.xml))
    controller.control.ExitRequests("","")


signal.signal(signal.SIGINT,controller.control.ExitRequests)
api.Login()
if args.scan is not None:
    from qqzone import scanner
    scanner.scan(str(args.scan))

time.sleep(0.5)

MsgLoop.Loop_Start()
