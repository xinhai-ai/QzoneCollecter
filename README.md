# QzoneCollecter

<p align="center"> 


一个收集、爬取、动态更新的QQ空间脚本
<p>


## Clone 

```
git clone https://github.com/xinhai-ai/QzoneCollecter.git
cd QzoneCollecter
```
## Start

### 安装依赖
```
pip -r requirements.txt
```

### 安装浏览器

由于登录时需要浏览器模拟登录，接下来需要安装浏览器

默认使用Chrome

#### 如果需要其他浏览器，可在qqzone/api.py中的Login()函数中更改

 在[Chrome浏览器](https://www.google.com/chrome/ "chrome浏览器")中下载并安装
 
### 浏览器驱动
 
 在[驱动页面](http://npm.taobao.org/mirrors/chromedriver/ "驱动") 中下载对应版本的webdriver
 并放在main.py同级目录即可

## Run
``` python main.py ```
浏览器会自动启动，登录即可

## 参数说明
``` python -s [QQ号] ```
可以爬取该用户的空间并保存在数据库中
<br>
请确保你有访问此空间的权限
<br>
``` python -c [Csv文件] ```
可以以html形式导出空间内容
<br>
如何获取Csv文件
<br>
点击view-database.bat打开数据库
<br>
在浏览数据中筛选数据，并点击文件->导出->导出表到csv文件，选择默认选项保存即可
## Other
空间数据保存在 archives中
<br>
Data/Posts.db为数据库，存放一条说说的key,内容,评论,发布时间,获取时间
<br>
以及说说主人的QQ号,昵称(账号登录者所设的昵称)
<br>
image 和 video 分别保存说说所属的图片及视频

## 扩展
脚本可以扩展
在 Handler/extraHandler.py 中 你可以自定义处理动态获取的说说
<br>
文件中已经给出点赞例子
<br>
传入的Post结构体可在 controller/Structor.py 中查看
<br>
注意：请将你的处理方法写为函数，并在Main()中插入
<br>
<br>
提供的接口:
<br>
logger.logger 提供日志接口，均写入文件,Debug以上的级别输出到控制台
api.client 提供处于登录状态的session
config 可写入配置，具体实现自己看代码
gvar 可配置全局变量

## 写到最后
这是一个高中生的作品，本来只是一个单文件的脚本，
经过多次灵光一闪最终形成了这个项目
<br>
时间能力有限，大佬轻喷，也欢迎 pr 和 issues



