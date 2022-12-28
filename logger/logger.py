import logging
from logging.handlers import RotatingFileHandler
import coloredlogs
from controller import gvar
import sys
import os

if not os.path.exists(gvar.get_value("path")+r'/logs/'):
    os.makedirs(gvar.get_value("path")+r'/logs/')

log_colors_config = {
    # 终端输出日志颜色配置
    'DEBUG': 'white',
    'INFO': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}
LOG_FORMAT = "[%(asctime)s] - %(levelname)s - %(message)s"
logger = logging.getLogger()
logger.setLevel('DEBUG')
WINDOWS = sys.platform.startswith('win')
NEED_COLORAMA = WINDOWS
CAN_USE_BOLD_FONT = (not NEED_COLORAMA)
coloredlogs.DEFAULT_FIELD_STYLES = dict(
    asctime=dict(color='green'),
    hostname=dict(color='magenta'),
    levelname=dict(color='white', bold=CAN_USE_BOLD_FONT),
    programname=dict(color='cyan'),
    name=dict(color='blue'),
    funcName=dict(color="blue"),
    lineno=dict(color="yellow")
)
coloredlogs.DEFAULT_LOG_FORMAT = '[%(asctime)s] [%(module)s] [%(funcName)s] @%(lineno)d %(levelname)s - %(message)s'
coloredlogs.install(level="INFO")

fhlr = logging.handlers.RotatingFileHandler(gvar.get_value("path") + r'/logs/log.log', maxBytes=5 * 1024 * 1024,
                                            backupCount=3, encoding="utf-8")

fhlr.setLevel("DEBUG")
fhlr.setFormatter(logging.Formatter(LOG_FORMAT))

logger.addHandler(fhlr)



def DisableConsole():
    logging.disable()
    # global logger
    # LOG_FORMAT = "[%(asctime)s] - %(levelname)s - %(message)s"
    # logger = logging.getLogger()
    # logger.setLevel('DEBUG')
    # fhlr = logging.handlers.RotatingFileHandler(gvar.get_value("path") + r'/logs/log.log', maxBytes=5 * 1024 * 1024,
    #                                             backupCount=3,
    #                                             encoding="utf-8")
    #
    # fhlr.setLevel("DEBUG")
    # fhlr.setFormatter(logging.Formatter(LOG_FORMAT))
    # logger.addHandler(fhlr)
