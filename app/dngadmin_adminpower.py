

# Create your views here.
from django.shortcuts import render #视图渲染模块
from django.http import HttpResponse  #请求模块
from . import models #数据库操作模块
from django.db.models import Q #数据库逻辑模块
from django.db.models import Avg,Max,Min,Sum #数据库聚合计算模块
from datetime import datetime,timedelta #Cookie 模块
from django.http import HttpResponse, HttpResponseRedirect #重定向模块
from django.core.paginator import Paginator #分页器
from django.shortcuts import render
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



def adminpower(request):
	# ----------------------------------------------------------
	#   判断页面权限》》》 开始
	# ----------------------------------------------------------

	dngroute_uid = dngadmin_common.dng_ckurl(request)[0]
	get_url=dngadmin_common.dng_ckurl(request)[1]

	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	yuming_url = request.META.get('HTTP_HOST')  # 当前访问的域名
	geturl = request.META.get('QUERY_STRING')  # 获取域名后缀的URL
	mulu_url = request.path  # 获取不包含？号之前的映射路径
	tishi = request.GET.get('tishi') #提示信息
	jinggao = request.GET.get('jinggao')  # 警告信息
	yes = request.GET.get('yes')  # 成功信息
	xitong = dngadmin_common.dng_setup()# 系统设置


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


	group = dngadmin_common.dng_usergroup(gid=dngadmin_common.dng_dnguser(dnguser_uid).group_int)  # 获取会员组名称
	groupall =	dngadmin_common.html_groupall()
	#groupall=zip(groupall[0], groupall[1])
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

	added =dngadmin_common.dng_zsgc(dngroute_uid,group.added_text) #增
	delete = dngadmin_common.dng_zsgc(dngroute_uid,group.delete_text) #删
	update = dngadmin_common.dng_zsgc(dngroute_uid,group.update_text)#改
	see = dngadmin_common.dng_zsgc(dngroute_uid,group.see_text) #查

	zd_list = dngadmin_common.dng_ziduan("adminpower") #获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------



	#biaodan = dngadmin_common.dng_dnguser(uid=dnguser_uid)

	vis = zip(zd_list[0], zd_list[1])
	return render(request,"dngadmin/adminpower.html",{
		"title":dngroute.name_str,
		"xitong": xitong,  # 系统配置
		"dnguser_uid": dnguser_uid,
		"groupall": groupall,


		"get_url": get_url,#
		"added": added,#增
		"delete": delete,#删
		"update": update, #改
		"see": see, #查
		"zd_list": zd_list,  # 字段名称
		"vist": vis,

		"tishi": tishi,
		"jinggao": jinggao,
		"yes": yes,
		"yuming_url": yuming_url,






	})


def adminpower_json(request):
	# ----------------------------------------------------------
	#   判断页面权限》》》 开始
	# ----------------------------------------------------------

	dngroute_uid = dngadmin_common.dng_ckurl(request)[0]
	get_url = dngadmin_common.dng_ckurl(request)[1]

	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	yuming_url = request.META.get('HTTP_HOST')  # 当前访问的域名
	geturl = request.META.get('QUERY_STRING')  # 获取域名后缀的URL
	mulu_url = request.path  # 获取不包含？号之前的映射路径
	tishi = request.GET.get('tishi') #提示信息
	jinggao = request.GET.get('jinggao')  # 警告信息
	yes = request.GET.get('yes')  # 成功信息
	xitong = dngadmin_common.dng_setup()# 系统设置

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

	group = dngadmin_common.dng_usergroup(gid=dngadmin_common.dng_dnguser(dnguser_uid).group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()  # 查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url:  # 判断URL统一
		urlstr = parse.quote('您的访问与菜单映射不匹配')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	elif not '|' + str(dngroute_uid) + '|' in group.menu_text:  # 判断菜单权限
		urlstr = parse.quote('您没有访问这个菜单的权限')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 查

	zd_list = dngadmin_common.dng_ziduan("adminpower")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------



	page = request.GET.get('page', '')  # 第几页
	limit = request.GET.get('limit', '') #每页显示多少

	page = int(page)
	limit =int(limit)

	dngred = models.dngusergroup.objects.filter().order_by('-id')
	paginator = Paginator(dngred, limit)

	list_count = paginator.count  # 总数据量
	num_pages = paginator.num_pages #有多少分页

	book_list = paginator.page(page)


	data = []
	for key in book_list:

		#group  = dngadmin_common.html_usergroup(gid=dngadmin_common.html_user(key.uperior_int).group_int)

		data.append({"id": str(key.id),
					 "gid_int": str(key.gid_int),  # 用户组id
					 "gname_str": str(key.gname_str),  # 用户组名称
					 "uperior_int": str(key.uperior_int),  # 上级用户组
					 "integral_int": str(key.integral_int),  # 积分阈值
					 "money_int": str(key.money_int),  # 余额阈值
					 "totalmoney_int": str(key.totalmoney_int),  # 充值阈值
					 "totalspend_int": str(key.totalspend_int),  # 消费阈值
					 "spread_int": str(key.spread_int),  # 推广阈值
					 "added_int": str(key.added_int),  # 每日新增
					 "look_int": str(key.look_int),  # 每日查看
					 "space_int": str(key.space_int),  # 每日上传
					 "download_int": str(key.download_int),  # 每日下载
					 "trial_bool": str(key.trial_bool),  # 自动过审
					 "upload_bool": str(key.upload_bool),  # 上传权限
					 "download_bool": str(key.download_bool),  # 下载权限
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




def adminpower_menu(request): #访问权限
	# ----------------------------------------------------------
	#   判断页面权限》》》 开始
	# ----------------------------------------------------------

	dngroute_uid = dngadmin_common.dng_ckurl(request)[0]
	get_url = dngadmin_common.dng_ckurl(request)[1]

	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	yuming_url = request.META.get('HTTP_HOST')  # 当前访问的域名
	geturl = request.META.get('QUERY_STRING')  # 获取域名后缀的URL
	mulu_url = request.path  # 获取不包含？号之前的映射路径
	tishi = request.GET.get('tishi') #提示信息
	jinggao = request.GET.get('jinggao')  # 警告信息
	yes = request.GET.get('yes')  # 成功信息
	xitong = dngadmin_common.dng_setup()# 系统设置

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

	group = dngadmin_common.dng_usergroup(gid=dngadmin_common.dng_dnguser(dnguser_uid).group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()  # 查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url:  # 判断URL统一
		urlstr = parse.quote('您的访问与菜单映射不匹配')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	elif not '|' + str(dngroute_uid) + '|' in group.menu_text:  # 判断菜单权限
		urlstr = parse.quote('您没有访问这个菜单的权限')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 查


	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------
	posturl = request.GET.get('posturl', '')
	qxid = request.GET.get('qxid', '')

	caidan1_list = []  # 声明为数组的变量
	caidan2_list = []  # 声明为数组的变量
	caidan = models.dngroute.objects.filter(superior_int=0) #查询主菜单
	for caidan1 in caidan:

		if caidan1:
			caidan1_list.append(caidan1)

			candan2 = models.dngroute.objects.filter(superior_int=caidan1.uid_int)
			if candan2:
				caidan2_list.append(candan2)





	cdid = models.dngroute.objects.filter() #查询所有菜单ID
	cdidss = models.dngroute.objects.filter(~Q(superior_int=0))   # 查询所有菜单ID
	looo =[]
	for sk in cdidss:
		looo.append('|'+str(sk.superior_int)+'|')

	zuqxx = models.dngusergroup.objects.filter(gid_int=qxid).first() #查询对应组的权限
	stre = ""
	keys = stre.join(zuqxx.menu_text)
	for skk in looo:

		keys = keys.replace(skk, '')

	keys = keys.replace('||', ',')
	zuqx = keys.replace('|', '')


	return render(request, "dngadmin/quanxian.html", {"posturl": posturl,
													  "cdid": cdid,
													  "qxid": qxid,
													  "zuqx": zuqx,
													  "fenlei": "menu_text",
													  "caidan1_list": caidan1_list,
													  "caidan2_list": caidan2_list,
													  })


def adminpower_added(request):  #新增
	# ----------------------------------------------------------
	#   判断页面权限》》》 开始
	# ----------------------------------------------------------

	dngroute_uid = dngadmin_common.dng_ckurl(request)[0]
	get_url = dngadmin_common.dng_ckurl(request)[1]

	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	yuming_url = request.META.get('HTTP_HOST')  # 当前访问的域名
	geturl = request.META.get('QUERY_STRING')  # 获取域名后缀的URL
	mulu_url = request.path  # 获取不包含？号之前的映射路径
	tishi = request.GET.get('tishi') #提示信息
	jinggao = request.GET.get('jinggao')  # 警告信息
	yes = request.GET.get('yes')  # 成功信息
	xitong = dngadmin_common.dng_setup()# 系统设置

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

	group = dngadmin_common.dng_usergroup(gid=dngadmin_common.dng_dnguser(dnguser_uid).group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()  # 查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url:  # 判断URL统一
		urlstr = parse.quote('您的访问与菜单映射不匹配')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	elif not '|' + str(dngroute_uid) + '|' in group.menu_text:  # 判断菜单权限
		urlstr = parse.quote('您没有访问这个菜单的权限')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 查


	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------
	posturl = request.GET.get('posturl', '')
	qxid = request.GET.get('qxid', '')

	caidan1_list = []  # 声明为数组的变量
	caidan2_list = []  # 声明为数组的变量
	caidan = models.dngroute.objects.filter(superior_int=0) #查询主菜单
	for caidan1 in caidan:

		if caidan1:
			caidan1_list.append(caidan1)

			candan2 = models.dngroute.objects.filter(superior_int=caidan1.uid_int)
			if candan2:
				caidan2_list.append(candan2)



	cdid = models.dngroute.objects.filter() #查询所有菜单ID
	cdidss = models.dngroute.objects.filter(~Q(superior_int=0))   # 查询所有菜单ID
	looo =[]
	for sk in cdidss:
		looo.append('|'+str(sk.superior_int)+'|')

	zuqxx = models.dngusergroup.objects.filter(gid_int=qxid).first() #查询对应组的权限
	stre = ""
	keys = stre.join(zuqxx.added_text)
	for skk in looo:

		keys = keys.replace(skk, '')

	keys = keys.replace('||', ',')
	zuqx = keys.replace('|', '')

	return render(request, "dngadmin/quanxian.html", {"posturl": posturl,
													  "cdid": cdid,
													  "qxid": qxid,
													  "zuqx": zuqx,
													  "fenlei": "added_text",
													  "caidan1_list": caidan1_list,
													  "caidan2_list": caidan2_list,
													  })



def adminpower_delete(request):  #删除
	# ----------------------------------------------------------
	#   判断页面权限》》》 开始
	# ----------------------------------------------------------

	dngroute_uid = dngadmin_common.dng_ckurl(request)[0]
	get_url = dngadmin_common.dng_ckurl(request)[1]

	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	yuming_url = request.META.get('HTTP_HOST')  # 当前访问的域名
	geturl = request.META.get('QUERY_STRING')  # 获取域名后缀的URL
	mulu_url = request.path  # 获取不包含？号之前的映射路径
	tishi = request.GET.get('tishi')  # 提示信息
	jinggao = request.GET.get('jinggao')  # 警告信息
	yes = request.GET.get('yes')  # 成功信息
	xitong = dngadmin_common.dng_setup()  # 系统设置

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

	group = dngadmin_common.dng_usergroup(gid=dngadmin_common.dng_dnguser(dnguser_uid).group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()  # 查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url:  # 判断URL统一
		urlstr = parse.quote('您的访问与菜单映射不匹配')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	elif not '|' + str(dngroute_uid) + '|' in group.menu_text:  # 判断菜单权限
		urlstr = parse.quote('您没有访问这个菜单的权限')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 查

	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------
	posturl = request.GET.get('posturl', '')
	qxid = request.GET.get('qxid', '')

	caidan1_list = []  # 声明为数组的变量
	caidan2_list = []  # 声明为数组的变量
	caidan = models.dngroute.objects.filter(superior_int=0)  # 查询主菜单
	for caidan1 in caidan:

		if caidan1:
			caidan1_list.append(caidan1)

			candan2 = models.dngroute.objects.filter(superior_int=caidan1.uid_int)
			if candan2:
				caidan2_list.append(candan2)




	cdid = models.dngroute.objects.filter() #查询所有菜单ID
	cdidss = models.dngroute.objects.filter(~Q(superior_int=0))   # 查询所有菜单ID
	looo =[]
	for sk in cdidss:
		looo.append('|'+str(sk.superior_int)+'|')

	zuqxx = models.dngusergroup.objects.filter(gid_int=qxid).first() #查询对应组的权限
	stre = ""
	keys = stre.join(zuqxx.delete_text)
	for skk in looo:

		keys = keys.replace(skk, '')

	keys = keys.replace('||', ',')
	zuqx = keys.replace('|', '')


	return render(request, "dngadmin/quanxian.html", {"posturl": posturl,
													  "cdid": cdid,
													  "qxid": qxid,
													  "zuqx": zuqx,
													  "fenlei": "delete_text",
													  "caidan1_list": caidan1_list,
													  "caidan2_list": caidan2_list,
													  })



def adminpower_update(request):  #更新修改
	# ----------------------------------------------------------
	#   判断页面权限》》》 开始
	# ----------------------------------------------------------

	dngroute_uid = dngadmin_common.dng_ckurl(request)[0]
	get_url = dngadmin_common.dng_ckurl(request)[1]

	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	yuming_url = request.META.get('HTTP_HOST')  # 当前访问的域名
	geturl = request.META.get('QUERY_STRING')  # 获取域名后缀的URL
	mulu_url = request.path  # 获取不包含？号之前的映射路径
	tishi = request.GET.get('tishi')  # 提示信息
	jinggao = request.GET.get('jinggao')  # 警告信息
	yes = request.GET.get('yes')  # 成功信息
	xitong = dngadmin_common.dng_setup()  # 系统设置

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

	group = dngadmin_common.dng_usergroup(gid=dngadmin_common.dng_dnguser(dnguser_uid).group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()  # 查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url:  # 判断URL统一
		urlstr = parse.quote('您的访问与菜单映射不匹配')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	elif not '|' + str(dngroute_uid) + '|' in group.menu_text:  # 判断菜单权限
		urlstr = parse.quote('您没有访问这个菜单的权限')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 查

	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------
	posturl = request.GET.get('posturl', '')
	qxid = request.GET.get('qxid', '')

	caidan1_list = []  # 声明为数组的变量
	caidan2_list = []  # 声明为数组的变量
	caidan = models.dngroute.objects.filter(superior_int=0)  # 查询主菜单
	for caidan1 in caidan:

		if caidan1:
			caidan1_list.append(caidan1)

			candan2 = models.dngroute.objects.filter(superior_int=caidan1.uid_int)
			if candan2:
				caidan2_list.append(candan2)


	cdid = models.dngroute.objects.filter() #查询所有菜单ID
	cdidss = models.dngroute.objects.filter(~Q(superior_int=0))   # 查询所有菜单ID
	looo =[]
	for sk in cdidss:
		looo.append('|'+str(sk.superior_int)+'|')

	zuqxx = models.dngusergroup.objects.filter(gid_int=qxid).first() #查询对应组的权限
	stre = ""
	keys = stre.join(zuqxx.update_text)
	for skk in looo:

		keys = keys.replace(skk, '')

	keys = keys.replace('||', ',')
	zuqx = keys.replace('|', '')



	return render(request, "dngadmin/quanxian.html", {"posturl": posturl,
													  "cdid": cdid,
													  "qxid": qxid,
													  "zuqx": zuqx,
													  "fenlei": "update_text",
													  "caidan1_list": caidan1_list,
													  "caidan2_list": caidan2_list,
													  })


def adminpower_see(request): #开发者权限
	# ----------------------------------------------------------
	#   判断页面权限》》》 开始
	# ----------------------------------------------------------

	dngroute_uid = dngadmin_common.dng_ckurl(request)[0]
	get_url = dngadmin_common.dng_ckurl(request)[1]

	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	yuming_url = request.META.get('HTTP_HOST')  # 当前访问的域名
	geturl = request.META.get('QUERY_STRING')  # 获取域名后缀的URL
	mulu_url = request.path  # 获取不包含？号之前的映射路径
	tishi = request.GET.get('tishi')  # 提示信息
	jinggao = request.GET.get('jinggao')  # 警告信息
	yes = request.GET.get('yes')  # 成功信息
	xitong = dngadmin_common.dng_setup()  # 系统设置

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

	group = dngadmin_common.dng_usergroup(gid=dngadmin_common.dng_dnguser(dnguser_uid).group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()  # 查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url:  # 判断URL统一
		urlstr = parse.quote('您的访问与菜单映射不匹配')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	elif not '|' + str(dngroute_uid) + '|' in group.menu_text:  # 判断菜单权限
		urlstr = parse.quote('您没有访问这个菜单的权限')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 查

	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------
	posturl = request.GET.get('posturl', '')
	qxid = request.GET.get('qxid', '')

	caidan1_list = []  # 声明为数组的变量
	caidan2_list = []  # 声明为数组的变量
	caidan = models.dngroute.objects.filter(superior_int=0)  # 查询主菜单
	for caidan1 in caidan:

		if caidan1:
			caidan1_list.append(caidan1)

			candan2 = models.dngroute.objects.filter(superior_int=caidan1.uid_int)
			if candan2:
				caidan2_list.append(candan2)



	cdid = models.dngroute.objects.filter()  # 查询所有菜单ID
	cdidss = models.dngroute.objects.filter(~Q(superior_int=0))  # 查询所有菜单ID
	looo = []
	for sk in cdidss:
		looo.append('|' + str(sk.superior_int) + '|')

	zuqxx = models.dngusergroup.objects.filter(gid_int=qxid).first()  # 查询对应组的权限
	stre = ""
	keys = stre.join(zuqxx.see_text)
	for skk in looo:
		keys = keys.replace(skk, '')

	keys = keys.replace('||', ',')
	zuqx = keys.replace('|', '')

	return render(request, "dngadmin/quanxian.html", {"posturl": posturl,
													  "cdid": cdid,
													  "qxid": qxid,
													  "zuqx": zuqx,
													  "fenlei": "see_text",
													  "caidan1_list": caidan1_list,
													  "caidan2_list": caidan2_list,
													  })


def adminpower_post(request):
	# ----------------------------------------------------------
	#   判断页面权限》》》 开始
	# ----------------------------------------------------------

	dngroute_uid = dngadmin_common.dng_ckurl(request)[0]
	get_url = dngadmin_common.dng_ckurl(request)[1]

	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	yuming_url = request.META.get('HTTP_HOST')  # 当前访问的域名
	geturl = request.META.get('QUERY_STRING')  # 获取域名后缀的URL
	mulu_url = request.path  # 获取不包含？号之前的映射路径
	tishi = request.GET.get('tishi')  # 提示信息
	jinggao = request.GET.get('jinggao')  # 警告信息
	yes = request.GET.get('yes')  # 成功信息
	xitong = dngadmin_common.dng_setup()  # 系统设置

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

	group = dngadmin_common.dng_usergroup(gid=dngadmin_common.dng_dnguser(dnguser_uid).group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()  # 查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url:  # 判断URL统一
		urlstr = parse.quote('您的访问与菜单映射不匹配')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	elif not '|' + str(dngroute_uid) + '|' in group.menu_text:  # 判断菜单权限
		urlstr = parse.quote('您没有访问这个菜单的权限')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
		return response

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 查

	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------
	if update:
		qxid = request.POST.get('qxid', '')
		post_id1 = request.POST.get('id1', '')
		post_id2 = request.POST.get('id2', '')
		fenlei = request.POST.get('fenlei', '')
		post_id1 = post_id1.replace(']', '')
		post_id1 = post_id1.replace('[', '')
		post_id1 = post_id1.split(',')

		if "id" in post_id2: #判断是否代码齐全

			fhf = post_id2.replace('[[', '[')
			dhd = fhf.replace('}],[{', '},{')
			tht = dhd.replace(']]', ']')

			shs = dhd.replace(',[]', '')
			shs2 = shs.replace('[{', '')
			shs3 = shs2.replace('}]', '')
			shs4 = shs3.replace(']', '')
			ghg = shs4.replace(']]', ']')
			str(ghg)
			zuqx = ghg.split('},{')

			seoss = []  # 声明为数组的变量
			for sks in zuqx:  # 遍历字符串，遍历输出

				reart = re.findall(r"\"title\":\"(.*)\",\"id\":(.*)", sks)

				seoss.append(reart[0][1])

			qxzz = (post_id1 + seoss)#合并数组
			qxzz = sorted(qxzz)
		else:

			qxzz =  post_id1
			qxzz = sorted(qxzz)


		stre = "||"
		keys = "|"+stre.join(qxzz)+"|"

		if  keys =="||": #空去掉两边
			keys =""

		if fenlei=="menu_text":
			models.dngusergroup.objects.filter(gid_int=qxid).update(menu_text= keys)
			ok = "yes"
		elif fenlei=="added_text":
			models.dngusergroup.objects.filter(gid_int=qxid).update(added_text= keys)
			ok = "yes"
		elif fenlei == "delete_text":
			models.dngusergroup.objects.filter(gid_int=qxid).update(delete_text= keys)
			ok = "yes"
		elif fenlei == "update_text":
			models.dngusergroup.objects.filter(gid_int=qxid).update(update_text= keys)
			ok = "yes"
		elif fenlei == "see_text":
			models.dngusergroup.objects.filter(gid_int=qxid).update(see_text= keys)
			ok = "yes"
		else:
			ok ="权限规则错误"

	return HttpResponse(ok)

