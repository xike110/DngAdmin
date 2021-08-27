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
#一键功能说明
一键列表和一键表单的功能，需要数据库表名的后缀作为判断标准，规划数据库名称，请参考下面对照表，表名_加上后缀

#表名后缀对照表
```
框体名称 | 后缀 | 数据类型 |说明
--------|-----|------|-----
静态框|_id|models.IntegerField_整形数字|生成静态框,不可修改，验证规则=是否为数字，不能重复，不能为空值 
文本框|_str|models.CharField_字符串|生成文本框,验证规则=填写不能为空
禁用文本框|_stop|models.CharField_字符串|禁止填写,禁止修改
密码框|_psd|models.CharField_字符串|禁用文本框,验证规则=密码必须6到12位，且不能出现空格，存时候会默认转MD5
手机框|_phone|models.CharField_字符串|生成文本框,验证规则=是否为手机号
邮箱框|_email|models.CharField_字符串|生成文本框,验证规则=是否为邮箱
身份证框|_email|models.CharField_字符串|生成文本框,验证规则=是否为邮箱
数字框|_int|models.IntegerField整形数字|生成数字框,验证规则=只能输入非负整数，做大输入1个亿
下拉框|_xiala|models.CharField_字符串|生成下拉框,验证规则=默认下拉值,default默认值必须写，添加好选择元组  choices=(('nan','男'),('nv','女')),default='男'
选择框|_xuanze|models.CharField_字符串|生成选择框,验证规则=默认选择值,default默认值必须写，添加好选择元组  choices=(('nan','男'),('nv','女')),default='男'
竖单选框|_shudanxuan|models.CharField_字符串|生成竖单选框,验证规则=默认选择值,default默认值必须写，添加好选择元组  choices=(('nan','男'),('nv','女')),default='男'
横单选框|_hengdanxuan|models.CharField_字符串|生成竖单选框,验证规则=默认选择值,default默认值必须写，添加好选择元组  choices=(('nan','男'),('nv','女')),default='男'
开关框|_bool|models.BooleanField_布尔|生成开关框
日期框|_years|DateTimeField 时间类型|生成日期框，验证规则=是否为时间格式=日期,(2099-12-28 00:00:00)
日期时间框|_datetime|DateTimeField 时间类型|生成时间框，格式=日期+时间,(2099-12-28 23:59:59)
富文本框|_text|models.TextField_富文本|生成超大文本框,验证规则=填写不能为空，字数限制1万以内
自动创建时间|create_time完整默认字段名称|DateTimeField 时间类型|请规范写，不然会前端要求填写创建时间，前端不会显示此值
自动更新时间|update_time完整默认字段名称|DateTimeField 时间类型|请规范写，不然会前端要求填写创建时间，前端不会显示此值
```