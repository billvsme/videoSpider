# videoSpider
[![ENV](https://img.shields.io/badge/python-3.4-blue.svg)](https://github.com/billvsme/videoSpider)
[![LICENSE](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/billvsme/videoSpider/blob/master/LICENSE)
[![Travis](https://img.shields.io/travis/billvsme/videoSpider.svg)](https://travis-ci.org/billvsme/videoSpider)  
分布式视频信息爬虫,从豆瓣,bilibili等收集电视剧、电影、动漫、演员等信息,
使用requests, BeautifulSoup, gevent, SQLAlchemy, Alembic, celery

# Install
首先因为选择使用使用lxml解析html,  安装lxml库前需要安装相关c库
```
sudo apt-get install libxml2-dev libxslt-dev python-dev
sudo apt-get build-dep python3-lxml
```
注意用python3
```
virtualenv tv -p python3
. tv/bin/activate
git clone https://github.com/billvsme/videoSpider
cd videoSpider
pip install -r requirements.txt
```
# Usage
注意使用python3 
首先,设置配置config.ini
```
cp config/config_dev.ini config/config.ini
vim config/config.ini
```
config_dev.ini 默认配置，可以运行，最好自己修改一下（比如celery的backend）。
```
[database]
database_url = sqlite:///tv.db  #数据库
test = false                    #是否输出SQLAlchemy 信息
[photo]
path = ./photo                  ＃下载图片存放等位置
[qiniu]                         #七牛的配置
access_key = xxxx              
secret_key = xxxx
bucket_name = xxxx
[celery]                        ＃celery 配置
backend = db+sqlite:///celery_backend.sqlite     
broker = sqla+sqlite:///celery_borker.sqlite
```
然后生成数据库
```
alembic upgrade head
```
然后运行Celery
```
celery -A tasks worker  --loglevel=info
```
抓取电影、电视剧、动漫 信息(video)
```
python start.py video
```
抓取演员信息
```
python start.py celebrity
```
下载电影、电视剧、动漫、演员的图片到本地(大概需要10个小时, 40G)
```
python start.py down-image
```
上传图片到七牛
```
python start.py upload-image
```
创建Whoosh索引
```
python start.py whoosh
```
# Doc

### 代码的文件结构
```
.
├── README.md
├── alembic
├── alembic.ini         # alembic.ini 配置文件，注意无需修改其中的'sqlalchemy.url'
├── config              # 存放配置信息
├── helpers             # 存放一些公共的函数 
├── models              # model层
├── start.py            # cmdline
├── tasks.py            # 定义Celery任务
└── webs                # 存放各个网站的代码
    ├── bilibili
    │   ├── parsers     # 定义html解析函数
    │   └── tasks       # 调用parsers, 把解析出来的数据保存到数据库
    └── douban
        ├── parsers
        └── tasks

```

### model
![model](http://7xqumk.com1.z0.glb.clouddn.com/%40%2Freadme%2Ftv-s_model.png)

### 流程
![流程](http://7xqumk.com1.z0.glb.clouddn.com/%40%2Freadme%2Ftv-s.png)

### 遇到的坑
1. SQLAlchemy 多进程问题: http://docs.sqlalchemy.org/en/rel_1_0/core/pooling.html, 而且要注意更新session, 这就是为什么config中使用一个名叫sqla的字典来保存session和engine
2. sqlite 对 alter 支持有问题。所以alembic 如果使用sqlite 注意: https://alembic.readthedocs.org/en/latest/batch.html
3. alembic.ini 中的配置信息，可以在alembic/env.py 中使用config.set_main_option 定义
4. lxml 安装: http://lxml.de/installation.html
