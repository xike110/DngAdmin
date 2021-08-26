# DngAdmin后台系统

#### 项目官网
基于Python和Django的后台管理框架！
官网：https://www.dngadmin.com
视频教程：https://www.dngadmin.com/video.html
完整手册：https://www.dngadmin.com/docs/index

## 系统介绍
`- `编写DngAdmin源于2020年的春节后的流感疫情，被困家里3个月没事，打算写一个Python项目，由于没有趁手的后端系统，就打算自己从零造一个，由此写上了第一行代码，2021年8月20日完成1.0版本，经过了1年零7个月，其中因为工作停止开发了一年，1.0之前由本人独立开发，目前版本称不上完美，很多不足，先发布，后面在慢慢完善，有BUG及时反馈给我，个人开发者不容易，希望多多支持，希望本系统能在工作中帮助到你！
----作者：席克剑（网名：苟小云）
## 运行环境
```
系统版本：Centos8.0以上 

宝塔面板：7.5

web服务：nginx1.18

编程语言：Python3.7.0

web框架：Django2.2以上都支持

数据库：MySQL5.6版本以上

轻量级数据库：SQLite 3.8.3以上
```
## 目录结构
```
├── /seo/ #django配置目录
│   ├── __init__.py
│   ├── settings.py #django配置文件
│   ├── urls.py
│   └── wsgi.py
├── /app/ #应用目录
│   ├── /ssh/ #证书目录
│   ├── /migrations/ # 数据库ORM记录
│   └── /Templates/ #模板目录
│   │        ├── /dngadmin/ # 后台模板目录
│   │        ├── /html/  # 前台模板目录
│   │        └── /demo/ #INSPINIA演示模板
│   │
│   ├── html_urls.py  #前台URL映射文件
│   ├── dngadmin_urls.py  #后台URL映射文件
│   ├── models.py  #数据库文件
│   ├── dngadmin_common.py  #后台公共函数文件
│   └── html_common.py  #前台公共函数文件
│
├── /static/ #静态CSS和JS资源目录
├── /dng_cache/ #缓存目录
├── manage.py #manage命令文件
├── db.sqlite3 #本地SQLite数据库文件
└── requirements.txt #支持插件导入文本

```