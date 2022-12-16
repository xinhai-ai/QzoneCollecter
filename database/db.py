import os
import sqlite3
import traceback

from controller import gvar
from controller import Structor
from logger import logger

class DB:
    if not os.path.exists(gvar.get_value("path") + "\\database\\Data\\"):
        os.makedirs(gvar.get_value("path") + "\\database\\Data\\")
    db = sqlite3.connect(gvar.get_value("path") + "\\database\\Data\\Posts.db")
    c = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS Posts (key, nickname, uin, content,comments,medias,creat_time,modify_time)"""
    c.execute(sql)
    c.close()
    db.commit()
    def __int__(self):
        pass

    def insert(self, data: Structor):
        try:
            cursor = self.db.cursor()
            if self.exists(data.key):
                sql = f"""
                update Posts
                set nickname='{data.nickname}',content='{data.content}',comments='{data.comments}',medias='{data.medias}',modify_time={data.modify_time}
                where key='{data.key}'
"""
            else:
                sql = f"""
                    INSERT INTO Posts (key, nickname, uin, content,comments,medias,creat_time,modify_time)
                    VALUES ('{data.key}','{data.nickname}','{data.uin}','{data.content}','{data.comments}','{data.medias}',{data.creat_time},{data.modify_time})
                    
                    """
            cursor.execute(sql)
            cursor.close()
            self.db.commit()
        except:
            logger.logger.error(traceback.format_exc())
            self.db.rollback()
    def exists(self,key):
        try:
            cursor = self.db.cursor()
            sql =f"""
               SELECT * from Posts where key='{key}'
            """
            rep= cursor.execute(sql).fetchall()
            cursor.close()
            if len(rep) == 0:
                return False
            else:
                return True
        except:
            logger.logger.error(traceback.format_exc())
            return False

