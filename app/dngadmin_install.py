

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

from . import dngadmin_common #公共函数
from . import dngadmin_models #公共数据库操作






def install(request):#安装创建页面

	uid = models.dnguser.objects.filter(uid_int=1).first()  # 查询管理员ID是否为空
	if uid:
		urlstr = parse.quote('已经创建账号，禁止再次创建')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao='+urlstr)  # 不是安全入口进去跳转提示
		return response

	else:
		return render(request, "dngadmin/install.html", {

			"title": "DngAdmin框架-创建管理员",

		})





def install_post(request):#创建管理员
	"""
	创建管理员POST

	"""
	username = request.POST.get('username', '')  # POST
	password = request.POST.get('password', '')  # POST
	repassword = request.POST.get('repassword', '')  # POST
	yuming_url = request.META.get('HTTP_HOST')  # 当前访问的域名
	anquan_url = models.security.objects.filter(uid_int=1).first()  # 查询安全后缀是否为空
	shibai=False
	uid=False

	if not username:

		shibai = '错误：账号为空'
	elif not password:
		shibai = '错误：密码为空'
	elif(password != repassword):
		shibai = '错误：两次密码输入不相同'
	elif(password == repassword):
		uid = models.dnguser.objects.filter(uid_int=1).first()# 查询管理员ID是否为空

		if not uid:
			password_md5 = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()#密码MD5加密
			models.dnguser.objects.create(uid_int=1, username_str =username,password_str=password_md5,group_int=1,gm_bool=True)  # 创建后台管理员
			models.user.objects.create(uid_int=1, username_str=username, password_str=password_md5, group_int=1,gm_bool=True)  # 创建前台管理员
			models.dngusergroup.objects.create(gid_int=1,gname_str='后台管理员')  # 创建后台管理员组
			models.dngusergroup.objects.create(gid_int=2,gname_str='新手用户')  # 创建后台默认新手组
			models.usergroup.objects.create(gid_int=1,gname_str='前台管理员')  # 创建前台管理员组
			models.usergroup.objects.create(gid_int=2,gname_str='新手会员')  # 创建前台默认新手组
			dngadmin_models.dng_install()#创建安装表
			dngadmin_models.html_install()  # 创建安装表

			uid = models.dnguser.objects.filter(uid_int=1).first()  # 查询管理员ID

			if not anquan_url:
				models.security.objects.create(uid_int=1, entrance_str=dngadmin_common.v_code(),salt_str=dngadmin_common.v_code())  # 创建后台安全设置
				models.protect.objects.create(uid_int=1, entrance_str=dngadmin_common.v_code(),salt_str=dngadmin_common.v_code())  # 创建前台安全设置
				models.setup.objects.create(setupname_str ='DngAdmin开发框架',domain_str=yuming_url)
				models.htmlsetup.objects.create(id=1)
				anquan_url = models.security.objects.filter(uid_int=1).first()  # 查询安全后缀
			else:
				urlstr = parse.quote('无法再次创建安全入口')
				response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)  # 不是安全入口进去跳转提示
				return response
		else:
			urlstr = parse.quote('无法再次创建账号')
			response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)  # 不是安全入口进去跳转提示
			return response



	else:
		urlstr = parse.quote('无法再次创建账号')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao='+urlstr)  # 不是安全入口进去跳转提示
		return response


	return render(request,"dngadmin/install_post.html",{

			"title":"创建管理员提示",
			"uid": uid,
			"shibai": shibai,
			"anquan_url": anquan_url,
			"yuming_url": yuming_url,



		})




