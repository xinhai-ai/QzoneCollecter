import hashlib
import os
import re
import json
import time
import traceback
from Handler import extraHandler
import controller.pool
from qqzone import api
import bs4
from logger import logger
from controller import gvar
from controller import Structor
from controller import control


def Img_Download(url):
    try:
        if not os.path.exists(gvar.get_value("path") + r'\archives\image\\'):
            os.makedirs(gvar.get_value("path") + r'\archives\image\\')
        if "&" in url:
            single_key = hashlib.md5(url[:url.find("&")].encode(encoding='utf-8')).hexdigest()
        else:
            single_key = hashlib.md5(url.encode(encoding='utf-8')).hexdigest()

        if os.path.exists(gvar.get_value("path") + r'\archives\image\\' + single_key):
            return
        data = api.universal_get(url)
        if data == "":
            return
        logger.logger.debug("图片下载:" + url)
        w = open(gvar.get_value("path") + r'\archives\image\\' + single_key, "wb")
        w.write(data)
        w.close()
        return
    except:
        logger.logger.error(traceback.format_exc())
        return ""

def Video_Download(video_url,key):
    try:
        t = time.perf_counter() * 1000
        v = open(gvar.get_value("path") + r'\archives\video\\' + key + ".mp4", "wb")
        v.write(api.universal_get(video_url))
        v.close()
        logger.logger.info(
            "视频下载完成:" + video_url + " 处理时间:" + f"{time.perf_counter() * 1000 - t:.8f}ms")
    except:
        logger.logger.error(traceback.format_exc())
        return

def Video_process(bs_in):
    try:
        if not os.path.exists(gvar.get_value("path") + r'\archives\video\\'):
            os.makedirs(gvar.get_value("path") + r'\archives\video\\')
        bs = bs4.BeautifulSoup(bs_in, 'html.parser')
        div = bs.find("div", attrs={"class": "img-box f-video-wrap play"})

        video_url = div["url3"]
        key = hashlib.md5(video_url[:video_url.find("?")].encode(encoding="utf-8")).hexdigest()

        if not os.path.exists(gvar.get_value("path") + r'\archives\video\\' + key + ".mp4"):
            controller.pool.pool_submit(Video_Download,video_url,key)
        div.clear()
        video_tag = bs.new_tag("video")
        video_tag.attrs["width"] = "480"
        video_tag.attrs["height"] = "360"
        video_tag.attrs["src"] = "/videos/" + key + ".mp4"
        video_tag.attrs["controls"] = "controls"
        div.insert(0, video_tag)
        return str(bs)
    except:
        logger.logger.error(traceback.format_exc())
        return ""


def get_media_name(md_text):
    if md_text is None:
        return ""
    image_list = []
    bs = bs4.BeautifulSoup(md_text, 'html.parser')
    for i in bs.find_all("img"):
        key = str(i["src"])
        image_list.append(key[key.find("images/") + 7:])
    video_list = []
    for i in bs.find_all("video"):
        key = str(i["src"])
        video_list.append(key[key.find("videos/") + 7:])
    return image_list, video_list


def process_img(html_text):

    if html_text is None:
        return ""
    try:
        t = time.perf_counter() * 1000
        bs = bs4.BeautifulSoup(html_text, 'html.parser')
        for i in bs.find_all("img"):

            try:
                url = str(i["src"])
                if "&" in url:
                    url = url[:url.find("&")]
                if "&" in url:
                    single_key = hashlib.md5(url[:url.find("&")].encode(encoding='utf-8')).hexdigest()
                else:
                    single_key = hashlib.md5(url.encode(encoding='utf-8')).hexdigest()
                controller.pool.pool_submit(Img_Download, url)
                # data_base64 = base64.b64encode(data)
                # i["src"] = "data:image/jpg;base64," + str(data_base64)[2:len(str(data_base64)) - 1]
                i["src"] = "/images/" + single_key
            except:
                continue

        bss_thumbnails = bs.find_all("div", attrs={"class": "bss-thumbnails"})
        for i in range(len(bss_thumbnails)):
            url = re.compile(r"(?<=http:).*?(?=vuin=)").findall(bss_thumbnails[i].select_one('img')["onload"])[0]
            url = "http:" + url.replace(r"\\", "").replace("&amp;", "")
            url = url.replace("/m", "/b")
            bss_thumbnails[i].clear()
            img_tag = bs.new_tag("img")
            controller.pool.pool_submit(Img_Download,url)
            if "&" in url:
                single_key = hashlib.md5(url[:url.find("&")].encode(encoding='utf-8')).hexdigest()
            else:
                single_key = hashlib.md5(url.encode(encoding='utf-8')).hexdigest()
            # data_base64 = base64.b64encode(data)
            # img_tag.attrs = {"src": "data:image/jpg;base64," + str(data_base64)[2:len(str(data_base64)) - 1]}
            img_tag.attrs["src"] = "/images/" + single_key
            bss_thumbnails[i].append(img_tag)
        logger.logger.debug("图像处理完成:" + " 处理时间:" + f"{time.perf_counter() * 1000 - t:.8f}ms")
        div = bs.find_all("div", attrs={"class": "img-box f-video-wrap play"})
        if len(div) != 0:
            return Video_process(str(bs))
        return str(bs)
    except:
        logger.logger.error(traceback.format_exc())
        return ""


def tag_clear(html):
    bs = bs4.BeautifulSoup(html, features="html.parser")
    a_s = bs.find_all("a")
    for index in range(len(a_s)):
        try:
            if "展开全文" in a_s[index].text:
                del a_s[index]
                continue
            for i in list(a_s[index].attrs.keys()):
                del a_s[index][i]
        except:
            continue
    a_s = bs.find_all("i")
    for index in range(len(a_s)):
        for i in list(a_s[index].attrs.keys()):
            del a_s[index][i]
    a_s = bs.find_all("div")
    for index in range(len(a_s)):

        for i in list(a_s[index].attrs.keys()):
            del a_s[index][i]
    a_s = bs.find_all("span", attrs={"class": "ui-mr10 state"})
    for index in range(len(a_s)):
        a_s[index].clear()
    return bs


def Handle(html, uin, nickname, key, abstime):
    try:
        aPost = Structor.Post()
        aPost.key = key
        aPost.creat_time = abstime
        aPost.modify_time = str(time.time())
        aPost.uin = uin
        bs = bs4.BeautifulSoup(html, features="html.parser")
        a_s = bs.find_all("a")

        for index in range(len(a_s)):
            if "data-cmd" in a_s[index].attrs.keys():
                if a_s[index]["data-cmd"] == "qz_toggle":
                    result = api.GetDetails(uin,key)
                    if not result == "":
                        bs = bs4.BeautifulSoup(result, features="html.parser")
        text = bs.find(class_="f-info")
        if text is None:
            return
        aPost.nickname = nickname
        if not gvar.get_value("db").exists(key):
            logger.logger.info(
                time.strftime("%Y-%m-%d %H:%M:%S  ", time.localtime(int(abstime))) + " " + aPost.nickname + " " + text.text)
        dt = bs.find("div", attrs={"class": "f-single-content f-wrap"})
        if dt.find("div", attrs={"class": "f-reprint"}) is not None:
            dt.find("div", attrs={"class": "f-reprint"}).clear()
        if dt.find("i", attrs={"class": "none"}) is not None:
            dt.find("i", attrs={"class": "none"}).clear()
        if dt.find("img", class_="load_img none") is not None:
            dt.find("img", class_="load_img none").clear()
        new_html = bs4.BeautifulSoup(process_img(str(dt)), features="html.parser")
        clear_ed = tag_clear(str(new_html))
        aPost.content = str(clear_ed)
        comments = bs.find("div", attrs={"class": "comments-list"})
        if comments is not None:
            reply_button = comments.find_all("a", attrs={"class": "act-reply none"})
            for a in range(len(reply_button)):
                reply_button[a].extract()
            new_html = bs4.BeautifulSoup(process_img(str(comments)), features="html.parser")
            clear_ed_comment = tag_clear(str(new_html))
            aPost.comments = str(clear_ed_comment)
        else:
            aPost.comments = ""
        medias = []
        tmp = get_media_name(aPost.content)
        medias.extend(tmp[0])
        medias.extend(tmp[1])
        medias.extend(get_media_name(aPost.comments)[0])
        aPost.medias = json.dumps(medias)
        gvar.get_value("db").insert(aPost)
        extraHandler.Main(aPost)
    except:
        logger.logger.error(traceback.format_exc())
        return
