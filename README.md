# videoSpider
分布式视频信息爬虫,从豆瓣,bilibili等收集电视剧、电影、动漫、演员等信息,
使用requests, BeautifulSoup, gevent, SQLAlchemy, Alembic, celery

# Install
注意: 使用python3 <br />
首先因为选择使用使用lxml解析html,  安装lxml库前需要安装相关c库
```
sudo apt-get install libxml2-dev libxslt-dev python-dev
sudo apt-get build-dep python3-lxml
```
```
virtualenv videospider -p python3
. videospider/bin/activate
git clone https://github.com/billvsme/videoSpider
cd videoSpider
pip install -r requirements.txt
```
# Usage
首先,设置配置config.ini
```
cp config/config_dev.ini config/config.ini
vim config/config.ini
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
