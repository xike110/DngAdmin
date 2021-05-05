

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



def protect(request):
	# ----------------------------------------------------------
	#    通过路径获得栏目ID 》》》开始
	# ----------------------------------------------------------
	get_url = request.path
	get_url = get_url.split("/")  # 分割
	get_url = get_url[1] + "/" + get_url[2]
	if "_" in get_url:
		url = get_url.split("_")  # 分割
		get_url = url[0]
	uid=models.dngroute.objects.filter(url_str__contains=get_url).first()
	dngroute_uid = uid.uid_int
	# ----------------------------------------------------------
	#    日记记录与COOKIE验证与权限 》》》开始
	# ----------------------------------------------------------
	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	yuming_url = request.META.get('HTTP_HOST')  # 当前访问的域名
	geturl = request.META.get('QUERY_STRING')  # 获取域名后缀的URL
	mulu_url = request.path  # 获取不包含？号之前的映射路径
	tishi = request.GET.get('tishi') #提示
	jinggao = request.GET.get('jinggao')  # 警告
	yes = request.GET.get('yes')  # 警告


	if "dnguser_uid" in request.COOKIES:  # 判断cookies有无，跳转
		dnguser_uid = request.get_signed_cookie(key="dnguser_uid", default=None,
												salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		dnguser_name = request.get_signed_cookie(key="dnguser_name", default=None,
												 salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		dnguser_cookie = request.get_signed_cookie(key="dnguser_cookie", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)

		if dngadmin_common.dng_anquan().tongshi_bool == False:  # 验证是否同时登录
			if dngadmin_common.dng_tongshi(uid=dnguser_uid, cookie=dnguser_cookie) == False:
				urlstr = parse.quote('不允许同时登录账号')
				response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
				return response
	else:
		urlstr = parse.quote('您需要重新登录')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response


	# ----------------------------------------------------------
	#    日记记录与COOKIE验证与权限《《《 结束
	# ----------------------------------------------------------
	# ----------------------------------------------------------
	#    判断页面权限开始》》》开始
	# ----------------------------------------------------------
	group = dngadmin_common.dng_usergroup(gid=dngadmin_common.dng_dnguser(dnguser_uid).group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()#查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url: #判断URL统一
		urlstr = parse.quote('您的访问与菜单映射不匹配')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	elif not '|'+str(dngroute_uid)+'|'in group.menu_text: #判断菜单权限
		urlstr = parse.quote('您没有访问这个菜单的权限')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	added =False #增
	delete = False #删
	update =False #改
	see =False #查

	if '|' + str(dngroute_uid) + '|' in group.added_text:  # 判断增加权限
		added  =True
	if '|' + str(dngroute_uid) + '|' in group.delete_text:  # 判断删除权限
		delete =True
	if '|' + str(dngroute_uid) + '|' in group.update_text:  # 判断修改权限
		update =True
	if '|' + str(dngroute_uid) + '|' in group.see_text:  # 判断查看权限
		see =True

	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------

	zd_list = dngadmin_common.dng_ziduan("protect") #获取对应表下所有字段值

	biaodan = dngadmin_common.dng_protect()


	return render(request,"dngadmin/protect.html",{
		"title":dngroute.name_str,
		"edition": dngadmin_common.dng_setup().edition_str,  # 版本号
		"file": dngadmin_common.dng_setup().file_str,  # 备案号
		"tongue": dngadmin_common.dng_setup().statistics_text,  # 统计
		"added": added,#增
		"delete": delete,#删
		"update": update, #改
		"see": see, #查
		"tishi": tishi,
		"jinggao": jinggao,
		"yes": yes,
		"zd_list": zd_list,
		"biaodan": biaodan,
		"yuming_url": yuming_url,








	})


def protect_post(request):
	# ----------------------------------------------------------
	#    通过路径获得栏目ID 》》》开始
	# ----------------------------------------------------------
	get_url = request.path
	get_url = get_url.split("/")  # 分割
	get_url = get_url[1] + "/" + get_url[2]
	if "_" in get_url:
		url = get_url.split("_")  # 分割
		get_url = url[0]
	uid=models.dngroute.objects.filter(url_str__contains=get_url).first()
	dngroute_uid = uid.uid_int
	# ----------------------------------------------------------
	#    日记记录与COOKIE验证与权限 》》》开始
	# ----------------------------------------------------------
	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	geturl = request.META.get('QUERY_STRING')  # 获取域名后缀的URL
	mulu_url = request.path  # 获取不包含？号之前的映射路径



	if "dnguser_uid" in request.COOKIES:  # 判断cookies有无，跳转
		dnguser_uid = request.get_signed_cookie(key="dnguser_uid", default=None,
												salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		dnguser_name = request.get_signed_cookie(key="dnguser_name", default=None,
												 salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		dnguser_cookie = request.get_signed_cookie(key="dnguser_cookie", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)

		if dngadmin_common.dng_anquan().tongshi_bool == False:  # 验证是否同时登录
			if dngadmin_common.dng_tongshi(uid=dnguser_uid, cookie=dnguser_cookie) == False:
				urlstr = parse.quote('不允许同时登录账号')
				response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
				return response
	else:
		urlstr = parse.quote('您需要重新登录')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response


	# ----------------------------------------------------------
	#    日记记录与COOKIE验证与权限《《《 结束
	# ----------------------------------------------------------
	# ----------------------------------------------------------
	#    判断页面权限开始》》》开始
	# ----------------------------------------------------------
	group = dngadmin_common.dng_usergroup(gid=dngadmin_common.dng_dnguser(dnguser_uid).group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()#查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url: #判断URL统一
		urlstr = parse.quote('您的访问与菜单映射不匹配')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	elif not '|'+str(dngroute_uid)+'|'in group.menu_text: #判断菜单权限
		urlstr = parse.quote('您没有访问这个菜单的权限')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	added =False #增
	delete = False #删
	update =False #改
	see =False #查

	if '|' + str(dngroute_uid) + '|' in group.added_text:  # 判断增加权限
		added  =True
	if '|' + str(dngroute_uid) + '|' in group.delete_text:  # 判断删除权限
		delete =True
	if '|' + str(dngroute_uid) + '|' in group.update_text:  # 判断修改权限
		update =True
	if '|' + str(dngroute_uid) + '|' in group.see_text:  # 判断查看权限
		see =True

	zd_list = dngadmin_common.dng_ziduan("protect")  # 获取对应表下所有字段值

	post2 = request.POST.get(zd_list[0][2], '')
	post3 = request.POST.get(zd_list[0][3], '')
	post4 = request.POST.get(zd_list[0][4], '')
	post5 = request.POST.get(zd_list[0][5], '')
	post6 = request.POST.get(zd_list[0][6], '')
	post7 = request.POST.get(zd_list[0][7], '')
	post8 = request.POST.get(zd_list[0][8], '')
	post9 = request.POST.get(zd_list[0][9], '')
	post10 = request.POST.get(zd_list[0][10], '')
	post11 = request.POST.get(zd_list[0][11], '')
	post12 = request.POST.get(zd_list[0][12], '')
	post13 = request.POST.get(zd_list[0][13], '')


	if update:
		if not post2:
			urlstr = parse.quote('安全入口不能为空')
			response = HttpResponseRedirect('/dngadmin/protect/?jinggao=' + urlstr)
			return response
		if not post3:
			urlstr = parse.quote('Cookie时效不能为空')
			response = HttpResponseRedirect('/dngadmin/protect/?jinggao=' + urlstr)
			return response
		if not post4:
			urlstr = parse.quote('加密盐不能为空')
			response = HttpResponseRedirect('/dngadmin/protect/?jinggao=' + urlstr)
			return response
		if not post5:
			urlstr = parse.quote('密错次数不能为空')
			response = HttpResponseRedirect('/dngadmin/protect/?jinggao=' + urlstr)
			return response
		if not post6:
			urlstr = parse.quote('冻结时间不能为空')
			response = HttpResponseRedirect('/dngadmin/protect/?jinggao=' + urlstr)
			return response
		if post7=='on':
			post7 =True
		else:
			post7 = False
		if post8=='on':
			post8 =True
		else:
			post8 = False
		if post11=='on':
			post11 =True
		else:
			post11 = False
		if post12=='on':
			post12 =True
		else:
			post12 = False

		models.protect.objects.filter(id=1).update(entrance_str=post2, prescription_int=post3, salt_str=post4,
													requests_int=post5, psdreq_int=post6, graphic_bool=post7,
													station_bool=post8, useragent_str=post9, area_str=post10,
													tongshi_bool=post11, sms_bool=post12, iptxt_text=post13,)  # 更新修改数据库
		urlstr = parse.quote('提交成功')
		response = HttpResponseRedirect('/dngadmin/protect/?yes=' + urlstr)
		return response

	else:
		urlstr = parse.quote('您没有修改权限')
		response = HttpResponseRedirect('/dngadmin/protect/?jinggao=' + urlstr)
		return response



