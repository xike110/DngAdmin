

# Create your views here.
from django.shortcuts import render #视图渲染模块
from django.http import HttpResponse  #请求模块
from . import models #数据库操作模块
from django.db.models import Q #数据库逻辑模块
from django.db.models import Avg,Max,Min,Sum #数据库聚合计算模块
from datetime import datetime,timedelta #Cookie 模块
from django.http import HttpResponse, HttpResponseRedirect #重定向模块
from django.shortcuts import render
import os
import sys
from urllib import parse#转码
import re #正则模块
import random#随机模块
import hashlib# 加密模块
from django.utils import timezone #时间处理模块
import datetime#时间
import time# 日期模块



def index(request): #前端首页


		return render(request,"html/demo_index.html",{
		"title":"感谢您使用DngAdmin框架-首页演示",
		"keywords":"DngAdmin框架",
		"description":"DngAdmin框架3.0-基于python和Django的极速后台开发框架,为极速开发而生！",


		})

def mulu(request): #主目录页

	return render(request,"html/demo_mulu.html",{
		"title":"主目录地址",
		"keywords":"主目录",
		"description":"DngAdmin框架3.0-基于python和Django的极速后台开发框架,为极速开发而生！",

		})

def zimulu(request): #子目录页

	return render(request,"html/demo_zimulu.html",{
		"title":"子目录地址",
		"keywords":"子目录",
		"description":"DngAdmin框架3.0-基于python和Django的极速后台开发框架,为极速开发而生！",

		})
def list(request):  #列表页

	return render(request,"html/demo_list.html",{
		"title":"列表页地址",
		"keywords":"列表页",
		"description":"DngAdmin框架3.0-基于python和Django的极速后台开发框架,为极速开发而生！",

		})

def new(request): #内容页

	return render(request,"html/demo_new.html",{
		"title":"内容页地址",
		"keywords":"内容页",
		"description":"DngAdmin框架3.0-基于python和Django的极速后台开发框架,为极速开发而生！",

		})

def get(request): #get地址
	
	return HttpResponse("DngAdmin框架GET预留地址") #retorn是返回声明

def post(request): #psot地址
	
	return HttpResponse("DngAdmin框架POST预留地址") #retorn是返回声明







def app_index(request):#工具首页
	
	

	return render(request,"app/app_index.html",{
		"title":"DngAdmin在线开发工具",
		"keywords":"在线开发工具",
		"description":"基于Django的极速后台开发框架",
	

		})

def app_http(request): #请求获取类
	#打印头部所以信息
	# print(request.META)
	ip = request.META.get('HTTP_X_FORWARDED_FOR')# 获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')# 获取浏览器信息
	get_url = request.META.get('QUERY_STRING')# 获取域名后缀的URL
	sessionid_cookie_url = request.META.get('HTTP_COOKIE')# 您的请求的token和sessionid
	cookie_url = request.META.get('CSRF_COOKIE')# 获取请求的token
	lailu_url = request.META.get('HTTP_REFERER')# 获取请求的上级来路
	yuming_url = request.META.get('HTTP_HOST')# 当前访问的域名
	duankou_url = request.META.get('SERVER_PORT')# 当前访问的端口
	qingqiu_url = request.META.get('REQUEST_METHOD')# 当前的请求方式是get还是POST
	http_ceho = request.META #所有请求参数


	
	
	return render(request,"app/app_http.html",{
		"title":"DngAdmin框架-请求获取类工具",
		"keywords":"请求获取类",
		"description":"基于Django的极速后台开发框架",
		"ip":ip,
		"liulanqi":liulanqi,
		"get_url":get_url,
		"sessionid_cookie_url":sessionid_cookie_url,
		"cookie_url":cookie_url,
		"lailu_url":lailu_url,
		"yuming_url":yuming_url,
		"duankou_url":duankou_url,
		"qingqiu_url":qingqiu_url,
		"http_ceho":http_ceho,

		})

def app_models(request): #数据库类


	root = os.getcwd()#获取项目运行根目录
	root_py = os.path.abspath('app/common.py') # 跟目录+py文件所在路径
	root_py = os.path.abspath('app/common1.py') # 跟目录+py文件所在路径

	seo = open (root_py,"rb")  #读取
	key = str(seo.read(),'utf-8') #read是读取命令 str 转换字符串和编码


	strinfo = re.compile('值') #正则替换前
	keyseo = strinfo.sub('数据',key)#正则替换后

	keyseo ='''
from django.db import models

# Create your models here.
# 
# # ORM模型
# 类 -> 数据库表
# 对象 -> 表中的每一行数据
# 对象.id，对象.value -> 每行中的数据
#这个类是用来生成数据库表的，这个类必须继承models.Model类
#注：对于ORM框架，可以简单的认为自定义类UserInfo表示数据库的表；根据UserInfo创建的对象表示数据库表
#里的一行数据；而对象.username和对象.password表示每一行数据里具体的字段(username/password)的数据。

class dnguser(models.Model): #后台会员表

	#id            = models.AutoField(max_length=11,db_column='id',primary_key=True) #id主键
	user_uid           = models.CharField(max_length=255,null=False) #会员ID,设置不能为空
	user_username      = models.CharField(max_length=255,null= True) #会员账号
	user_password      = models.CharField(max_length=255,null= True) #会员密码MD5加密
	user_name          = models.CharField(max_length=255,null= True) #后台会员昵称
	user_emall         = models.CharField(max_length=255,null= True) #后台会员邮箱
	user_mobile        = models.CharField(max_length=255,null= True) #手机号接收短信等
	user_portrait      = models.CharField(max_length=255,null= True) #上传头像后的地址
	user_grade         = models.CharField(max_length=255,null= True) #后台会员组
	user_integral      = models.CharField(max_length=255,null= True) #积分
	user_ip            = models.CharField(max_length=255,null= True) #最后一次登录ip地址
	user_shebei        = models.CharField(max_length=255,null= True) #登录后台设备
	user_zctime        = models.CharField(max_length=255,null= True) #后台注册时间
	user_token         = models.CharField(max_length=255,null= True) #后台客户token密钥，预留加密授权登录用
	user_onine         = models.CharField(max_length=255,null= True) #后台是否允许账号在多设备同时在线，考虑大家都是做授权系统卖VIP账号，默认为空不允许同时在线，0=等于不允许 1=允许同时在线
	user_dltime        = models.CharField(max_length=255,null= True) #最后一次登录时间'''


	kaobei2 = open(root_py,"w") #写入
	kaobei2.write(keyseo)  #write是写入命令
	kaobei2.close()   #close()是关闭命令


	return HttpResponse(keyseo) #retorn是返回声明



	



