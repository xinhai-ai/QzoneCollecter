from config import config
import datetime
try:
    config.load()
except:
    pass
if len(config.get_sections())==0:
    config.init()
if not config.has_key("timestamp"):
    config.setConfig("timestamp", int(datetime.datetime.now().timestamp()))
if not config.has_key("LikeUnIncluded"):
    config.setConfig("LikeUnIncluded", [])
if not config.has_key("AutoRefresh"):
    config.setConfig("AutoRefresh", True)
if not config.has_key("TimeSleep"):
    config.setConfig("TimeSleep", 150)
if not config.has_key("DisableNotification"):
    config.setConfig("DisableNotification", True)
if not config.has_key("cookies"):
    config.setConfig("cookies", {})
    config.load()
