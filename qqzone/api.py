import hashlib
import json
import os
import random
import re
import sys
import time
import traceback
import urllib3
import requests

import config.config
import controller.control
from controller import gvar
from selenium import webdriver
from logger import logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/76.0.3809.132 Safari/537.36'}
client = requests.session()
client.headers.update(headers)


def update_cookies():
    if gvar.get_value("cookies") == {}:
        return
    cookies = requests.utils.cookiejar_from_dict(gvar.get_value("cookies"))
    client.cookies = cookies
    pskey = cookies['p_skey']
    skey = cookies['skey']
    uin = cookies['uin'].replace('o', '')
    g_tk = getNewGTK(pskey, skey, None)
    gvar.set_value("g_tk", g_tk)
    gvar.set_value("uin", uin)


def LongToInt(value):  # 由于int+int超出范围后自动转为long型，通过这个转回来
    if isinstance(value, int):
        return int(value)


def LeftShiftInt(number, step):  # 由于左移可能自动转为long型，通过这个转回来
    if isinstance((number << step), int):
        return int((number << step) - 0x200000000)
    else:
        return int(number << step)


def getOldGTK(skey):
    a = 5381
    for i in range(0, len(skey)):
        a = a + LeftShiftInt(a, 5) + ord(skey[i])
        a = LongToInt(a)
    return a & 0x7fffffff


def getNewGTK(p_skey, skey, rv2):
    b = p_skey or skey or rv2
    a = 5381
    for i in range(0, len(b)):
        a = a + LeftShiftInt(a, 5) + ord(b[i])
        a = LongToInt(a)
    return a & 0x7fffffff


def GetDetails(uin, tid):
    global client
    try:
        url = "https://h5.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_ic_getcomments?g_tk=" + str(
            gvar.get_value("g_tk"))
        payload = {
            "uin": uin,
            "tid": tid
        }
        result = client.post(url, data=payload, ).text
        tmp = re.compile(r"(?<=callback\().*?(?=\); <)").findall(result)[0]
        tmp = json.loads(tmp)
        return tmp["newFeedXML"]
    except IndexError:
        return ""
    except:
        logger.logger.error(traceback.format_exc())
        return ""


def cookies_invalid():
    try:
        global client
        repose1 = client.get('https://user.qzone.qq.com/' + gvar.get_value("cookies")["uin"].replace("o", ""),
                             allow_redirects=False, verify=False)
        if repose1.status_code == 200:
            return True
        else:
            return False
    except:
        logger.logger.error(traceback.format_exc())
        return False


def universal_get(url):
    global client
    content = None
    try:
        content = client.get(url, verify=False).content
    except requests.exceptions.MissingSchema:
        return ""
    except:
        logger.logger.error(traceback.format_exc())
    return content


def Msg_Get(extraparam="", BeginTime=""):
    global client
    params = {
        'uin': gvar.get_value("uin"),
        'rd': str(random.uniform(0.1, 0.9)),
        'g_tk': gvar.get_value("g_tk"),
        "begintime": BeginTime,
        "externparam": extraparam
    }
    setnum = 1
    while 1:
        try:
            result = client.get(
                url='https://user.qzone.qq.com/proxy/domain/ic2.qzone.qq.com/cgi-bin/feeds/feeds3_html_more',
                params=params, verify=False, stream=True)

            if result.status_code == 403:
                return ""
            else:
                return result.text
        except:
            logger.logger.debug(str(sys.exc_info()[1]) + " 重连" + str(setnum) + "次")
            setnum += 1
            if setnum > 10:
                logger.logger.critical("重连过多，请求退出")
                controller.control.ExitRequests("", "")
            time.sleep(1)
            continue


def get_file(path):
    all_files = []
    for root, dirs, files in os.walk(path):
        for name in files:
            all_files.append(os.path.join(root, name))
        for name in dirs:
            os.path.join(root, name)
    return all_files


def get_one_zone(uin, start: int = 0, count: int = 10):
    global client
    params = {
        "uin": gvar.get_value("uin"),
        "hostuin": uin,
        "filter": "all",
        "start": start,
        "count": count,
        "r": str(random.uniform(0.1, 0.9)),
        "g_tk": gvar.get_value("g_tk")
    }
    setnum = 1
    while 1:
        try:
            resp = client.get(
                "https://user.qzone.qq.com/proxy/domain/ic2.qzone.qq.com/cgi-bin/feeds/feeds_html_act_all",
                params=params, verify=False)
            if resp.status_code == 403:
                logger.logger.error("登录失效")
                controller.control.ExitRequests("", "")
            return resp.text
        except:
            logger.logger.debug(str(sys.exc_info()[1]) + " 重连" + str(setnum) + "次")
            setnum += 1
            if setnum > 10:
                logger.logger.critical("重连过多，请求退出")
                controller.control.ExitRequests("", "")
            time.sleep(1)
            continue


def Check_Details(uin, mood):
    param = {
        "uin": uin,
        "tid": mood,
        "g_tk": gvar.get_value("g_tk"),
        "format": "jsonp"
    }
    global client
    result_text = client.get("https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msgdetail_v6",
                             params=param, verify=False).text
    result_json = json.loads(result_text.replace("_Callback(", "").replace(");", ""))
    if "删除" in result_json["message"]:
        return False
    elif str(result_json["result"]["code"]) == "-10000":
        logger.logger.error("繁忙被系统检测，过会再试...")
        return None
    else:
        return True


def Check(Floder):
    if Floder == "":

        record_path = gvar.get_value("path") + r'/html_record'
        File_list = get_file(record_path)
    else:
        File_list = get_file(Floder)
    File_list.reverse()
    for i in File_list:
        if ".html" not in i:
            continue
        mood = str(os.path.split(i)[1]).split(" ")[1].replace(".html", "")
        try:
            uin = re.compile(r"(?<=user.qzone.qq.com/).*?(?=\")").findall(open(i, "r", encoding="utf-8").read())[0]
        except:
            continue
        result = Check_Details(uin, mood)
        print(i)
        if result:
            logger.logger.info(mood + " 存在")
        else:
            os.rename(str(i), str(i).replace(mood, mood + "_已删除"))
            logger.logger.info(mood + " 已被删除")


# 点赞
# uin 本人Q号 key 说说唯一标识 num 说说主人QQ号
def Like(key, num):
    try:
        payload = {
            "qzreferrer": f"https://user.qzone.qq.com/{gvar.get_value('uin')}/infocenter",
            "opuin": str(gvar.get_value('uin')),
            "unikey": f"http://user.qzone.qq.com/{num}/mood/{key}",
            "curkey": f"http://user.qzone.qq.com/{num}/mood/{key}",
            "fid": key,
            "active": "0",
            "fupdate": "1",
        }
        global client
        rep1 = client.post(
            "https://user.qzone.qq.com/proxy/domain/w.qzone.qq.com/cgi-bin/likes/internal_dolike_app?g_tk=" + str(
                gvar.get_value('g_tk')), data=payload, verify=False)
        if "succ" in rep1.text:
            return True
        else:
            logger.logger.debug(rep1.text)
            return False
    except:
        logger.logger.error(traceback.format_exc())
        return False


def get_info():
    try:
        url = "https://user.qzone.qq.com/2976024458/profile/qzbase"
        global client
        html = client.get(url).text
        first = html.find("ProfileSummary") + 15
        second = html.find("g_isOFP") - 3
        info = html[first:second]
        return json.loads(info)
    except:
        logger.logger.error(traceback.format_exc())
        return []


# 评论

def feeds(id, hostid, uin, content):
    try:
        url = "https://h5.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_re_feeds?&g_tk=" + str(
            gvar.get_value('g_tk'))
        payload = {
            "topicId": f"{hostid}_{id}__1",
            "hostUin": hostid,
            "uin": uin,
            "content": content,
            "qzreferrer": "https://user.qzone.qq.com/" + hostid,
            "format": "fs",
            "inCharset": "utf-8",
            "outCharset": "utf-8",
            "plat": "qzone",
            "feedsType": "100",
            "source": "ic",
            "platformid": "50",
            "ref": "feeds",
            "richtype": "",
            "richval": "",
            "isSignIn": "",
            "private": "0",
            "paramstr": "2"

        }
        global client
        rep = client.post(url, data=payload, verify=False)
        if rep.status_code == 200:
            return True
        else:
            return False
    except:
        logger.logger.error(traceback.format_exc())
        return False


def Login():
    update_cookies()
    if not cookies_invalid():
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=chrome_options)
        driver.delete_all_cookies()
        logger.logger.info("等待浏览器响应...")
        driver.get('https://qzone.qq.com')
        while "user.qzone.qq.com" not in driver.current_url:
            time.sleep(0.2)
        self_cookies = driver.get_cookies()
        driver.quit()
        re_cookies = {}
        for i in self_cookies:
            re_cookies[i['name']] = i['value']
        config.config.setConfig("cookies", re_cookies)
        config.config.load()
        update_cookies()
    info = get_info()
    if not len(info) == 0:
        logger.logger.info("欢迎:" + str(info[4]).replace("的空间", ""))
        return
