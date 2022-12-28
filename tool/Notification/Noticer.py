import os
from controller import gvar
import pythonnet
import clr
import sys

sys.path.append(gvar.get_value("path") + "\\tool\\Notification")
clr.FindAssembly("Notification.dll")
dll = clr.AddReference("Notification")

from Notificationer import *


def Notice(title, content):
    i = Notices()
    i.Notice(title, content)
