import shutil
import sys
import time

import bs4
import pandas
import numpy
from logger import logger
import json
import markdown
import os


def get_file(path):
    all_files = []
    for root, dirs, files in os.walk(path):
        for name in files:
            all_files.append(os.path.join(root, name))
        for name in dirs:
            os.path.join(root, name)
    return all_files


def export(csv_file):
    path = sys.path[0]
    logger.logger.info("正在分析文档")
    store_path = path + "\\ExportData\\" + (time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())) + "导出数据\\"
    if not os.path.exists(store_path):
        os.makedirs(store_path)
        os.makedirs(store_path+"\\medias")
    data = pandas.read_csv(csv_file)
    data = numpy.array(data)
    medias = []
    core_text = ""

    for i in data:
        main_text = ""
        nickname = i[1]
        main_text += "# "+nickname + "\n"
        content = i[3]
        bs = bs4.BeautifulSoup(content,features="html.parser")
        a_s = bs.findAll("img")
        for index in range(len(a_s)):
            for a in list(a_s[index].attrs.keys()):
                if a == "style":
                    del a_s[index]["style"]
        content = str(bs).replace('height="5%"',"")
        content = str(bs)
        main_text += content + "\n"
        main_text += "<br><br>"
        creat_time = int(i[6])
        main_text += f'<font size=1><i>最后发布于{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(creat_time))}</i></font>\n'
        modify_time = int(i[7])
        main_text += f'<font size=1><i>最后记录于{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(modify_time))}</i></font>\n<br>'
        comments = str(i[4])
        if not comments == "nan":
            main_text += str(comments)
        data_store = f'<div class="data_store" uin="{i[2]}" key="{i[0]}" style="display:none"></div>'
        main_text += data_store
        medias.extend(json.loads(i[5]))
        main_text += "<br>" * 5
        core_text += markdown.markdown(main_text)
    style = open(path + "\\exporter\\css.txt","r",encoding="utf-8").read()
    open(store_path + "main.html", "w", encoding="utf-8").write(style+"\n"+core_text)
    medias_own = []
    logger.logger.info("正在收集图片与视频")
    medias_own.extend(get_file(path+"\\archives\\image"))
    medias_own.extend(get_file(path+r"\archives\video"))
    for i in medias_own:
        name = os.path.split(i)[1]
        if name in medias:
            shutil.copyfile(i,store_path+"\\medias\\"+name)
    logger.logger.info("成功导出到:"+store_path + "main.html")
