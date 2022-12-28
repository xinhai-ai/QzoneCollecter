import traceback
from config import config
from controller import gvar
from logger import logger
from qqzone import api
from controller import Structor


def Main(Post: Structor):
    ForLike(Post)
    Notice(Post)
    pass
    # 此处写额外功能


def Notice(Post: Structor):
    if not gvar.get_value("db").exists(Post.key) and not config.getConfig("DisableNotification"):
        from tool.Notification import Noticer
        Noticer.Notice(Post.nickname, Post.content)


def ForLike(Post: Structor):
    if not gvar.get_value("db").exists(Post.key) and Post.key not in config.getConfig("likeunincluded"):
        try:
            if api.Like(Post.key, Post.uin):
                logger.logger.info(Post.key + " 点赞成功")
            else:
                logger.logger.error(Post.key + " 点赞失败")
        except:
            logger.logger.error(traceback.format_exc())
            return
