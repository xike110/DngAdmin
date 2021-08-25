

# Create your views here.
from django.shortcuts import render #视图渲染模块
from django.http import HttpResponse  #请求模块
from . import models #数据库操作模块
from django.db.models import Q #数据库逻辑模块
from django.db.models import Avg,Max,Min,Sum #数据库聚合计算模块
from datetime import datetime,timedelta #Cookie 模块
from django.http import HttpResponse, HttpResponseRedirect #重定向模块
from django.core.paginator import Paginator #分页器
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone #时间处理模块
from django.http import JsonResponse
from django.core import serializers
from urllib import parse#转码
import re #正则模块
import random#随机模块
import hashlib# 加密模块
import datetime#时间
import time# 日期模块
import os
import sys
import json
from . import dngadmin_common #公共函数
from . import html_common #公共函数
from . import dngadmin_formcommon #表单组件模块


def 映射的路径名替换(request):
	# ----------------------------------------------------------
	#   判断页面权限》》》 开始
	# ----------------------------------------------------------

	htmlsetup = html_common.dng_htmlsetup()  # 获取前台配置
	anquan = html_common.dng_protect()  # 获取前台安全
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	yuming_url = request.META.get('HTTP_HOST')  # 当前访问的域名
	route = html_common.html_ckurl(request)
	tishi = request.GET.get('tishi')  # 提示
	jinggao = request.GET.get('jinggao')  # 警告
	yes = request.GET.get('yes')  # 警告
	xitong = dngadmin_common.dng_setup()  # 系统设置
	shebei = dngadmin_common.shebei(liulanqi)  # 判断移动设备
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
				groupall = dngadmin_common.html_groupall()
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

	zd_list = dngadmin_common.dng_ziduan("映射的路径名替换") #获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------



	#biaodan = dngadmin_common.dng_dnguser(uid=dnguser_uid)

	vis = zip(zd_list[0], zd_list[1])
	return render(request,"html/映射的路径名替换.html",{
		"title": route.seotirle_str,  # 网站SEO标题
		"logotitle": htmlsetup.logotitle_str,  # 品牌名称
		"keywords": route.keywords_str,  # 关键词
		"description": route.description_str,  # 描述
		"route": route,  # 菜单信息
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
		"xitong": xitong,  # 系统配置
		"shebei": shebei,  # 设备
		"dnguser_uid": dnguser_uid,
		"groupall": groupall,
		"get_url": route.url_str.replace('/',''),#
		"zd_list": zd_list,  # 字段名称
		"vist": vis,
		"yuming_url": yuming_url,






	})


def 映射的路径名替换_json(request):
	# ----------------------------------------------------------
	#   判断页面权限》》》 开始
	# ----------------------------------------------------------

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

	zd_list = dngadmin_common.dng_ziduan("映射的路径名替换")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------



	page = request.GET.get('page', '')  # 第几页
	limit = request.GET.get('limit', '') #每页显示多少

	page = int(page)
	limit =int(limit)

	dngred = models.映射的路径名替换.objects.filter().order_by('-id')
	paginator = Paginator(dngred, limit)

	list_count = paginator.count  # 总数据量
	num_pages = paginator.num_pages #有多少分页

	book_list = paginator.page(page)


	data = []
	for key in book_list:

		#group  = dngadmin_common.html_usergroup(gid=dngadmin_common.html_user(key.uperior_int).group_int)

		data.append({
			# ⊙json查看替换⊙ #
		})


	#下面开始构造JSON格式
	datajson ="""{
		  "code": 0
		  ,"msg": ""
		  ,"count":"""+str(list_count)+"""
		  ,"data":"""+str(data)+"""}"""


	datajson = datajson.replace('\'', '\"') #替换成AJAX可以解析得格式
	datajson = datajson.replace('True', '启用')
	datajson = datajson.replace('False', '关闭')


	return HttpResponse(datajson)








def 映射的路径名替换_added(request):  #新增
	# ----------------------------------------------------------
	#   判断页面权限》》》 开始
	# ----------------------------------------------------------

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

	zd_list = dngadmin_common.dng_ziduan("映射的路径名替换")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------

	# 1⊙added新增替换⊙1 #


	ok = 'no'
	if added:

		# 2⊙added新增替换⊙2 #
		if ok:
			ok = 'yes'
		else:
			ok = 'no'
	else:
		urlstr = '您没有新增权限'

		return urlstr

	return HttpResponse(ok)



def 映射的路径名替换_delete(request):  #删除
	# ----------------------------------------------------------
	#   判断页面权限》》》 开始
	# ----------------------------------------------------------

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

	zd_list = dngadmin_common.dng_ziduan("映射的路径名替换")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------

	delete_id = request.GET.get('delete_id')
	id = request.POST.get('id', '')

	ok = 'no'

	if delete:  # 判断删除权限

		if delete_id:  # 判断单个删除

			ok = models.映射的路径名替换.objects.filter(id=delete_id).delete()

			if ok:
				ok = 'yes'
			else:
				ok = 'no'

		elif id:  # 判断批量删除
			str(id)
			id = id.replace("[", '')  # 去两边
			id = id.replace("]", '')  # 去两边
			id = id.replace("\"", '')  # 去两边
			if "," in id:
				id = id.split(",")  # 分割
				for key in id:
					int(key)
					ok = models.映射的路径名替换.objects.filter(id=key).delete()
					if ok:
						ok = 'yes'
					else:
						ok = 'no'


			else:
				int(id)
				ok = models.映射的路径名替换.objects.filter(id=id).delete()
				if ok:
					ok = 'yes'
				else:
					ok = 'no'
	else:
		urlstr = parse.quote('您没有删除权限')

		return urlstr

	return HttpResponse(ok)



def 映射的路径名替换_update(request):  #更新修改
	# ----------------------------------------------------------
	#   判断页面权限》》》 开始
	# ----------------------------------------------------------

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

	zd_list = dngadmin_common.dng_ziduan("映射的路径名替换") #获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------
	post0 = request.POST.get(zd_list[0][0], '')
	# 1⊙update更改替换⊙1 #


	ok ='修改失败'
	off=False
	if update:

		if not post0:

			off = "空ID"
			exit()  # 终止
		# 2⊙update更改替换⊙2 #


		ok = 'yes'
	else:
		ok =  '您没有修改权限'





	return HttpResponse(ok,off)





def 映射的路径名替换_search(request):  #搜索

	# ----------------------------------------------------------
	#   判断页面权限》》》 开始
	# ----------------------------------------------------------

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

	zd_list = dngadmin_common.dng_ziduan("映射的路径名替换")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------


	# 1⊙search搜索替换⊙1 #


	page = request.GET.get('page', '')  # 第几页
	limit = request.GET.get('limit', '')  # 每页显示多少

	page = int(page)
	limit = int(limit)


	# 2⊙search搜索替换⊙2 #
	else:
		dngred = models.映射的路径名替换.objects.filter().order_by('-id')

	paginator = Paginator(dngred, limit)

	list_count = paginator.count  # 总数据量
	num_pages = paginator.num_pages  # 有多少分页

	book_list = paginator.page(page)

	data = []
	for key in book_list:
		#group = dngadmin_common.html_usergroup(gid=dngadmin_common.html_user(key.uid_int).group_int)
		data.append({"id": str(key.id),
					 # 3⊙search搜索替换⊙3 #
					 })

	# 下面开始构造JSON格式
	datajson = """{
			  "code": 0
			  ,"msg": ""
			  ,"count":""" + str(list_count) + """
			  ,"data":""" + str(data) + """}"""

	datajson = datajson.replace('\'', '\"')  # 替换成AJAX可以解析得格式
	datajson = datajson.replace('True', '启用')
	datajson = datajson.replace('False', '关闭')

	return HttpResponse(datajson)


# noinspection PyUnreachableCode
@csrf_exempt
def 映射的路径名替换_api_json(request):  #api查询
	return HttpResponse("待开发")
@csrf_exempt
def 映射的路径名替换_api_post(request):
	return HttpResponse("待开发")