

# Create your views here.
from django.shortcuts import render #视图渲染模块
from django.http import HttpResponse  #请求模块
from . import models #数据库操作模块
from django.db.models import Q #数据库逻辑模块
from django.db.models import Avg,Max,Min,Sum #数据库聚合计算模块
from datetime import datetime,timedelta #Cookie 模块
from django.http import HttpResponse, HttpResponseRedirect #重定向模块
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import os
import sys
import rsa
import base64
import sqlite3
from urllib import parse#转码
import re #正则模块
import random#随机模块
import hashlib# 加密模块
from django.utils import timezone #时间处理模块
import datetime#时间
import time# 日期模块
from . import html_common #公共函数




def 映射的路径名替换(request):  #空白页面
	htmlsetup = html_common.dng_htmlsetup()  # 获取前台配置
	anquan = html_common.dng_protect()  # 获取前台安全
	route = html_common.html_ckurl(request)
	tishi = request.GET.get('tishi')  # 提示
	jinggao = request.GET.get('jinggao')  # 警告
	yes = request.GET.get('yes')  # 警告
	true_daohang = None
	home_daohang = None
	group = None
	added = None
	delete = None
	update = None
	see = None
	if "cms_user_name" in request.COOKIES:  # 判断cookies有无，跳转
		cookie_user_uid = request.get_signed_cookie(key="cms_user_uid", default=None, salt=anquan.salt_str,
													max_age=None)
		cookie_user_name = request.get_signed_cookie(key="cms_user_name", default=None, salt=anquan.salt_str,
													 max_age=None)
		cookie_user_cookie_echo = request.get_signed_cookie(key="cms_user_cookie_echo", default=None,
															salt=anquan.salt_str, max_age=None)
		cookie_user_cookie = request.get_signed_cookie(key="cms_user_cookie", default=None, salt=anquan.salt_str,
													   max_age=None)
		cookie_pr = html_common.dng_yanzheng(cookie_user_uid, cookie_user_name, cookie_user_cookie,
											 cookie_user_cookie_echo)
		if cookie_pr:
			# ----------------------------------------------------------
			#    cookie授权开始》》》开始
			# ----------------------------------------------------------
			dnguser_uid = cookie_pr.uid_int  # 赋值ID
			dnguser_name = cookie_pr.username_str  # 赋值用户名
			dnguser_cookie = cookie_pr.cookie_str  # 赋值COOKIE记录
			true_daohang = html_common.true_daohang(dnguser_uid, 0)  # 登录后导航
			home_daohang = html_common.home_daohang(dnguser_uid, 0)  # 用户中心菜单
			# ----------------------------------------------------------
			#    判断页面权限开始》》》开始
			# ----------------------------------------------------------
			if route.prove_bool == True:
				group = html_common.html_usergroup(gid=cookie_pr.group_int)  # 获取会员组名称
				added = html_common.dng_zsgc(cookie_pr.group_int, group.added_text)  # 增
				delete = html_common.dng_zsgc(cookie_pr.group_int, group.delete_text)  # 删
				update = html_common.dng_zsgc(cookie_pr.group_int, group.update_text)  # 改
				see = html_common.dng_zsgc(cookie_pr.group_int, group.see_text)  # 开发者

				user = html_common.html_user(dnguser_uid)
				qx_if = html_common.html_qx_if(route.uid_int, group.menu_text, user.integral_int, route.integral_int,
											   user.money_int, route.money_int, user.totalmoney_int,
											   route.totalmoney_int, user.totalspend_int, route.totalspend_int,
											   user.spread_int, route.spread_int)
				if qx_if:
					if "您" in qx_if:  # 目录权限判断
						return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote(qx_if))
		else:
			return HttpResponseRedirect('/signout/?jinggao=' + parse.quote('检测到非法登录'))

		if anquan.tongshi_bool == False:  # 验证是否同时登录
			if html_common.html_tongshi(uid=dnguser_uid, cookie=dnguser_cookie) == False:
				return HttpResponseRedirect('/signout/?tishi' + parse.quote('不允许同时登录账号'))

	#zd_list = html_common.dng_ziduan("映射的路径名替换")  # 获取对应表下所有字段值



	return render(request,"html/映射的路径名替换.html",{
		"title":route.seotirle_str,#网站SEO标题
		"logotitle": htmlsetup.logotitle_str, #品牌名称
		"keywords": route.keywords_str, # 关键词
		"description":route.description_str, #描述
		"route":route, #菜单信息
		"file": htmlsetup.file_str,  # 备案号
		"htmlsetup": htmlsetup,  # 网站配置
		"statistics": htmlsetup.statistics_text,  # 统计代码
		"tishi": tishi,
		"jinggao": jinggao,
		"yes": yes,
		"added": added,  # 增
		"delete": delete,  # 删
		"update": update,  # 改
		"see": see,  # 开发者权限
		"caidan_1": html_common.false_daohang(0, 0),  # 无需登陆菜单
		"caidan_2": true_daohang,  # 登陆后菜单
		"caidan_3": home_daohang,  # 用户中心菜单
		})



	
def 映射的路径名替换_post(request): #空白页面
	htmlsetup = html_common.dng_htmlsetup()  # 获取前台配置
	anquan = html_common.dng_protect()  # 获取前台安全
	route = html_common.html_ckurl(request)
	true_daohang = None
	home_daohang = None
	group = None
	added = None
	delete = None
	update = None
	see = None


	if "cms_user_name" in request.COOKIES:  # 判断cookies有无，跳转
		cookie_user_uid = request.get_signed_cookie(key="cms_user_uid", default=None, salt=anquan.salt_str,
													max_age=None)
		cookie_user_name = request.get_signed_cookie(key="cms_user_name", default=None, salt=anquan.salt_str,
													 max_age=None)
		cookie_user_cookie_echo = request.get_signed_cookie(key="cms_user_cookie_echo", default=None,
															salt=anquan.salt_str, max_age=None)
		cookie_user_cookie = request.get_signed_cookie(key="cms_user_cookie", default=None, salt=anquan.salt_str,
													   max_age=None)
		cookie_pr = html_common.dng_yanzheng(cookie_user_uid, cookie_user_name, cookie_user_cookie,
											 cookie_user_cookie_echo)
		if cookie_pr:
			# ----------------------------------------------------------
			#    cookie授权开始》》》开始
			# ----------------------------------------------------------
			dnguser_uid = cookie_pr.uid_int  # 赋值ID
			dnguser_name = cookie_pr.username_str  # 赋值用户名
			dnguser_cookie = cookie_pr.cookie_str  # 赋值COOKIE记录
			true_daohang = html_common.true_daohang(dnguser_uid, 0)  # 登录后导航
			home_daohang = html_common.home_daohang(dnguser_uid, 0)  # 用户中心菜单
			# ----------------------------------------------------------
			#    判断页面权限开始》》》开始
			# ----------------------------------------------------------
			if route.prove_bool == True:
				group = html_common.html_usergroup(gid=cookie_pr.group_int)  # 获取会员组名称
				added = html_common.dng_zsgc(cookie_pr.group_int, group.added_text)  # 增
				delete = html_common.dng_zsgc(cookie_pr.group_int, group.delete_text)  # 删
				update = html_common.dng_zsgc(cookie_pr.group_int, group.update_text)  # 改
				see = html_common.dng_zsgc(cookie_pr.group_int, group.see_text)  # 开发者

				user = html_common.html_user(dnguser_uid)
				qx_if = html_common.html_qx_if(route.uid_int, group.menu_text, user.integral_int, route.integral_int,
											   user.money_int, route.money_int, user.totalmoney_int,
											   route.totalmoney_int, user.totalspend_int, route.totalspend_int,
											   user.spread_int, route.spread_int)
				if qx_if:
					if "您" in qx_if:  # 目录权限判断
						return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote(qx_if))
		else:
			return HttpResponseRedirect('/signout/?jinggao=' + parse.quote('检测到非法登录'))

		if anquan.tongshi_bool == False:  # 验证是否同时登录
			if html_common.html_tongshi(uid=dnguser_uid, cookie=dnguser_cookie) == False:
				return HttpResponseRedirect('/signout/?tishi' + parse.quote('不允许同时登录账号'))




	post1 = request.POST.get('参数1', '')
	# ----------------------------------------------------------
	#    这里写接收参数
	# ----------------------------------------------------------

	if update:
		if not post1:
			urlstr = parse.quote('参数不能为空')
			response = HttpResponseRedirect('/映射的路径名替换/?jinggao=' + urlstr)
			return response
	# ----------------------------------------------------------
	#   这里写入库规则
	# ----------------------------------------------------------


	else:
		urlstr = parse.quote('您没有修改权限')
		response = HttpResponseRedirect('/映射的路径名替换/?jinggao=' + urlstr)
		return response