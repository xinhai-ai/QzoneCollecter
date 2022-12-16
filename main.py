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
gvar._init()
gvar.set_value("db",db.DB())


signal.signal(signal.SIGINT,controller.control.ExitRequests)
api.Login()


MsgLoop.Loop_Start()
