

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

@cache_page(10 * 1)
def index(request): #前端首页


	htmlsetup = html_common.dng_htmlsetup()  # 获取前台配置
	anquan =html_common.dng_protect() #获取前台安全
	####系统安装####
	urlstr = None
	uid = models.dnguser.objects.filter().order_by('id').first()  # 最开始的第一条  # 查询管理员ID是否为空
	if uid:
		urlstr = False
	else:
		urlstr = True
	if not htmlsetup:
		# 创建管理员界面
		return HttpResponseRedirect('/dngadmin/install/?jinggao=' + parse.quote('创建管理员'))
	####系统安装结束####
	tishi = request.GET.get('tishi')  # 提示
	jinggao = request.GET.get('jinggao')  # 警告
	yes = request.GET.get('yes')  # 警告
	route= html_common.html_ckurl(request)


	true_daohang=None
	home_daohang=None
	group=None
	added = None
	delete =None
	update = None
	see = None
	if "cms_user_name" in request.COOKIES:  # 判断cookies有无，跳转
		cookie_user_uid = request.get_signed_cookie(key="cms_user_uid", default=None,salt=anquan.salt_str, max_age=None)
		cookie_user_name = request.get_signed_cookie(key="cms_user_name", default=None,salt=anquan.salt_str, max_age=None)
		cookie_user_cookie_echo = request.get_signed_cookie(key="cms_user_cookie_echo", default=None,salt=anquan.salt_str, max_age=None)
		cookie_user_cookie = request.get_signed_cookie(key="cms_user_cookie", default=None,salt=anquan.salt_str, max_age=None)
		cookie_pr = html_common.dng_yanzheng(cookie_user_uid, cookie_user_name, cookie_user_cookie, cookie_user_cookie_echo)
		if cookie_pr:
			# ----------------------------------------------------------
			#    cookie授权开始》》》开始
			# ----------------------------------------------------------
			dnguser_uid = cookie_pr.uid_int  # 赋值ID
			dnguser_name = cookie_pr.username_str  # 赋值用户名
			dnguser_cookie = cookie_pr.cookie_str  # 赋值COOKIE记录
			true_daohang = html_common.true_daohang(dnguser_uid, 0)# 登录后导航
			home_daohang = html_common.home_daohang(dnguser_uid, 0) #用户中心菜单
			# ----------------------------------------------------------
			#    判断页面权限开始》》》开始
			# ----------------------------------------------------------
			if route.prove_bool ==True:
				group = html_common.html_usergroup(gid=cookie_pr.group_int)  # 获取会员组名称
				added = html_common.dng_zsgc(cookie_pr.group_int, group.added_text)  # 增
				delete = html_common.dng_zsgc(cookie_pr.group_int, group.delete_text)  # 删
				update = html_common.dng_zsgc(cookie_pr.group_int, group.update_text)  # 改
				see = html_common.dng_zsgc(cookie_pr.group_int, group.see_text)  # 开发者

				if not '|' + str(route.uid_int) + '|' in group.menu_text:  # 判断菜单权限
					return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您没有访问这个栏目的权限</h1></center><div>""")

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











	return render(request,"html/index.html",{
	"title":route.seotirle_str,#网站SEO标题
	"logotitle": htmlsetup.logotitle_str, #品牌名称
	"keywords": route.keywords_str, # 关键词
	"description":route.description_str, #描述
	"file": htmlsetup.file_str, #备案号
	"htmlsetup": htmlsetup,#网站配置
	"statistics": htmlsetup.statistics_text, #统计代码
	"tishi": tishi,
	"jinggao": jinggao,
	"yes": yes,
	"added": added,  # 增
	"delete": delete,  # 删
	"update": update,  # 改
	"see": see,  # 开发者权限
	"caidan_1": html_common.false_daohang(0, 0), #无需登陆菜单
	"caidan_2": true_daohang, #登陆后菜单
	"caidan_3": home_daohang,  # 用户中心菜单





	})

@cache_page(10 * 1)
def mulu(request): #主目录页
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














	return render(request, "html/mulu.html", {
		"title":route.seotirle_str,#网站SEO标题
		"logotitle": htmlsetup.logotitle_str, #品牌名称
		"keywords": route.keywords_str, # 关键词
		"description":route.description_str, #描述
		"file": htmlsetup.file_str,  # 备案号
		"htmlsetup": htmlsetup,  # 网站配置
		"statistics": htmlsetup.statistics_text,  # 统计代码
		"added": added,  # 增
		"delete": delete,  # 删
		"update": update,  # 改
		"see": see,  # 开发者权限
		"caidan_1": html_common.false_daohang(0, 0),  # 无需登陆菜单
		"caidan_2": true_daohang,  # 登陆后菜单
		"caidan_3": home_daohang,  # 用户中心菜单



	})



@cache_page(10 * 1)
def zimulu(request): #子目录页
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


	



	return render(request,"html/zimulu.html",{
		"title":route.seotirle_str,#网站SEO标题
		"logotitle": htmlsetup.logotitle_str, #品牌名称
		"keywords": route.keywords_str, # 关键词
		"description":route.description_str, #描述
		"file": htmlsetup.file_str,  # 备案号
		"htmlsetup": htmlsetup,  # 网站配置
		"statistics": htmlsetup.statistics_text,  # 统计代码
		"added": added,  # 增
		"delete": delete,  # 删
		"update": update,  # 改
		"see": see,  # 开发者权限
		"caidan_1": html_common.false_daohang(0, 0),  # 无需登陆菜单
		"caidan_2": true_daohang,  # 登陆后菜单
		"caidan_3": home_daohang,  # 用户中心菜单
		})


@cache_page(10 * 1)
def sitemap(request): #网站地图
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










	return render(request,"html/sitemap.html",{
		"title":route.seotirle_str,#网站SEO标题
		"logotitle": htmlsetup.logotitle_str, #品牌名称
		"keywords": route.keywords_str, # 关键词
		"description":route.description_str, #描述
		"file": htmlsetup.file_str,  # 备案号
		"htmlsetup": htmlsetup,  # 网站配置
		"statistics": htmlsetup.statistics_text,  # 统计代码
		"added": added,  # 增
		"delete": delete,  # 删
		"update": update,  # 改
		"see": see,  # 开发者权限
		"caidan_1": html_common.false_daohang(0, 0),  # 无需登陆菜单
		"caidan_2": true_daohang,  # 登陆后菜单
		"caidan_3": home_daohang,  # 用户中心菜单
		})


@cache_page(10 * 1)
def list(request):  #列表页
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



	return render(request,"html/list.html",{
		"title":route.seotirle_str,#网站SEO标题
		"logotitle": htmlsetup.logotitle_str, #品牌名称
		"keywords": route.keywords_str, # 关键词
		"description":route.description_str, #描述
		"file": htmlsetup.file_str,  # 备案号
		"htmlsetup": htmlsetup,  # 网站配置
		"statistics": htmlsetup.statistics_text,  # 统计代码
		"added": added,  # 增
		"delete": delete,  # 删
		"update": update,  # 改
		"see": see,  # 开发者权限
		"caidan_1": html_common.false_daohang(0, 0),  # 无需登陆菜单
		"caidan_2": true_daohang,  # 登陆后菜单
		"caidan_3": home_daohang,  # 用户中心菜单

		})

@cache_page(10 * 1)
def new(request): #内容页
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


	return render(request,"html/new.html",{
		"title":route.seotirle_str,#网站SEO标题
		"logotitle": htmlsetup.logotitle_str, #品牌名称
		"keywords": route.keywords_str, # 关键词
		"description":route.description_str, #描述
		"file": htmlsetup.file_str,  # 备案号
		"htmlsetup": htmlsetup,  # 网站配置
		"statistics": htmlsetup.statistics_text,  # 统计代码
		"added": added,  # 增
		"delete": delete,  # 删
		"update": update,  # 改
		"see": see,  # 开发者权限
		"caidan_1": html_common.false_daohang(0, 0),  # 无需登陆菜单
		"caidan_2": true_daohang,  # 登陆后菜单
		"caidan_3": home_daohang,  # 用户中心菜单

		})

@cache_page(10 * 1)
def http404(request): #get地址
	htmlsetup = html_common.dng_htmlsetup()  # 获取前台配置




	return render(request, "html/404.html", {
		"title": "404页面",  # 网站SEO标题
		"logotitle": htmlsetup.logotitle_str,  # 品牌名称
		"keywords": "404页面",  # 关键词
		"description": "404页面",  # 描述
		"file": htmlsetup.file_str, #备案号
		"statistics": htmlsetup.statistics_text, #统计代码


	})
@cache_page(10 * 1)
def http505(request): #psot地址



	htmlsetup = html_common.dng_htmlsetup()  # 获取前台配置


	return render(request, "html/505.html", {
		"title": "505页面",  # 网站SEO标题
		"logotitle": htmlsetup.logotitle_str,  # 品牌名称
		"keywords": "505页面",  # 关键词
		"description": "505页面",  # 描述
		"file": htmlsetup.file_str,  # 备案号
		"statistics": htmlsetup.statistics_text,  # 统计代码


	})


def dug(request): #调试地址

	return HttpResponse("BUG调试页面")


	



