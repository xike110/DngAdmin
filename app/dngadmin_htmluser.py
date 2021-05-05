

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



def htmluser(request):
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

	zd_list = dngadmin_common.dng_ziduan("htmluser") #获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------



	#biaodan = dngadmin_common.dng_dnguser(uid=dnguser_uid)

	vis = zip(zd_list[0], zd_list[1])
	return render(request,"dngadmin/htmluser.html",{
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


def htmluser_json(request):
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

	zd_list = dngadmin_common.dng_ziduan("htmluser")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------



	page = request.GET.get('page', '')  # 第几页
	limit = request.GET.get('limit', '') #每页显示多少

	page = int(page)
	limit =int(limit)

	dngred = models.user.objects.filter().order_by('-id')
	paginator = Paginator(dngred, limit)

	list_count = paginator.count  # 总数据量
	num_pages = paginator.num_pages #有多少分页

	book_list = paginator.page(page)


	data = []
	for key in book_list:
		group  = dngadmin_common.html_usergroup(gid=dngadmin_common.html_user(key.uid_int).group_int)
		data.append({"id": str(key.id),
					 "uid_int": str(key.uid_int),
					 "username_str": str(key.username_str),
					 "password_str": str("******"),
					 "name_str": str(key.name_str),
					 "gender_str": str(key.gender_str),
					 "introduce_str": str(key.introduce_str),
					 "emall_str": str(key.emall_str),
					 "mobile_str": str(key.mobile_str),
					 "group_int": str(group.gname_str),
					 "rank_str": str(key.rank_str),
					 "gm_bool": str(key.gm_bool),
					 "money_int": str(key.money_int),
					 "totalmoney_int": str(key.totalmoney_int),
					 "totalspend_int": str(key.totalspend_int),
					 "integral_int": str(key.integral_int),
					 "spread_int": str(key.spread_int),
					 "ip_str": str(key.ip_str),
					 "shebei_str": str(key.shebei_str),
					 "cookie_str": str("******"),
					 "token_str": str("******"),
					 "days_int": str(key.days_int),
					 "pwderror_int": str(key.pwderror_int),
					 "frozen_bool": str(key.frozen_bool),
					 "frozentime_str": str(key.frozentime_str),
					 "vipime_time": str(key.vipime_time.strftime("%Y-%m-%d %H:%M:%S")),
					 "create_time": str(key.create_time.strftime("%Y-%m-%d %H:%M:%S")),
					 "update_time": str(key.update_time.strftime("%Y-%m-%d %H:%M:%S")),


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








def htmluser_added(request):  #新增
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

	zd_list = dngadmin_common.dng_ziduan("htmluser")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------

	post2 = request.POST.get(zd_list[0][2], '')
	post3 = request.POST.get(zd_list[0][3], '')
	posts = request.POST.get(zd_list[0][3]+'s', '')
	post9 = request.POST.get(zd_list[0][9], '')

	ok = '新增失败'
	off = False
	pws =models.user.objects.filter(username_str__contains=post2).only('username_str')
	if added:

		if not post2:
			off ='账号不能为空'


		elif post3!=posts:
			off = '两次的密码不一致'

		elif not post9:
			off = '会员组不能为空'
		elif pws:
			off = '已经有重复账号，请更换'

		else:
			post3_md5 = hashlib.md5(post3.encode(encoding='UTF-8')).hexdigest()  # 密码MD5加密
			user = models.user.objects.filter().order_by('-uid_int').first()

			uid = int(user.uid_int)+1 #会员ID递增
			models.user.objects.create(uid_int=uid,username_str=post2, password_str=post3_md5, group_int=post9,)


		if off:
			ok = off
		else:
			ok = 'yes'
	else:
		ok = '您没有新增权限'




	return HttpResponse(ok)



def htmluser_delete(request):  #删除
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

	zd_list = dngadmin_common.dng_ziduan("htmluser")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------

	delete_id = request.GET.get('delete_id') #接收单个删除

	id = request.POST.get('id', '') #接收批量删除

	ok = '删除失败'





	if delete: #判断删除权限

		if delete_id: #判断单个删除
			if not dngadmin_common.html_gmid(id=delete_id) == False:
				off = "前台超级管理员不能删除"
				return HttpResponse(off)

			ok = models.user.objects.filter(id=delete_id).delete()

			if ok:
				ok='yes'
			else:
				ok = 'no'

		elif id: #判断批量删除


			str(id)
			id = id.replace("[",'')  # 去两边
			id = id.replace("]",'')  # 去两边
			id = id.replace("\"",'')  # 去两边
			if "," in id :
				id =id.split(",")  # 分割
				for key in id:
					int(key)

					if not dngadmin_common.html_gmid(id=key) == False:
						off = "前台超级管理员不能删除"
						return HttpResponse(off)

					ok = models.user.objects.filter(id=key).delete()
					if ok:
						ok = 'yes'
					else:
						ok = 'no'


			else:
				int(id)

				if not dngadmin_common.html_gmid(id=id) == False:
					off = "前台超级管理员不能删除"
					return HttpResponse(off)

				ok = models.user.objects.filter(id=id).delete()
				if ok:
					ok = 'yes'
				else:
					ok = 'no'

	else:
		ok = parse.quote('您没有删除权限')




	return HttpResponse(ok)



def htmluser_update(request):  #更新修改
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

	zd_list = dngadmin_common.dng_ziduan("htmluser") #获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------
	post0 = request.POST.get(zd_list[0][0], '')
	post1 = request.POST.get(zd_list[0][1], '')  # 会员ID
	post2 = request.POST.get(zd_list[0][2], '')  # 会员账号
	post3 = request.POST.get(zd_list[0][3], '')  # 会员密码
	post4 = request.POST.get(zd_list[0][4], '')  # 昵称
	post5 = request.POST.get(zd_list[0][5], '')  # 性别
	post6 = request.POST.get(zd_list[0][6], '')  # 个人简介
	post7 = request.POST.get(zd_list[0][7], '')  # 邮箱
	post8 = request.POST.get(zd_list[0][8], '')  # 手机号
	post9 = request.POST.get(zd_list[0][9], '')  # 用户组
	post10 = request.POST.get(zd_list[0][10], '')  # 等级
	post12 = request.POST.get(zd_list[0][12], '')  # 余额
	post13 = request.POST.get(zd_list[0][13], '')  # 累计充值
	post14 = request.POST.get(zd_list[0][14], '')  # 累计消费
	post15 = request.POST.get(zd_list[0][15], '')  # 积分
	post16 = request.POST.get(zd_list[0][16], '')  # 推广注册
	post23 = request.POST.get(zd_list[0][23],'')#允许登录
	post25 = request.POST.get(zd_list[0][25],'')#登录时限

	ok ='修改失败'
	off=False
	if update:

		if not post0:

			off = "空ID"
			exit()  # 终止

		if post1:
			models.user.objects.filter(id=post0).update(uid_int=post1)

		if post2:
			models.user.objects.filter(id=post0).update(username_str=post2)

		if post3:
			models.user.objects.filter(id=post0).update(password_str=post3)

		if post4:
			models.user.objects.filter(id=post0).update(name_str=post4)

		if post5:

			models.user.objects.filter(id=post0).update(gender_str=post5)

		if post6:
			models.user.objects.filter(id=post0).update(introduce_str=post6)

		if post7:
			models.user.objects.filter(id=post0).update(emall_str=post7)

		if post8:
			models.user.objects.filter(id=post0).update(mobile_str=post8)

		if post9:

			if not dngadmin_common.html_gmid(id=post0) == False:
				off = "前台超级管理员不能操作"
				return HttpResponse(off)

			models.user.objects.filter(id=post0).update(group_int=post9)


		if post10:
			models.user.objects.filter(id=post0).update(rank_str=post10)

		if post12:
			models.user.objects.filter(id=post0).update(money_int=post12)

		if post13:
			models.user.objects.filter(id=post0).update(totalmoney_int=post13)

		if post14:
			models.user.objects.filter(id=post0).update(totalspend_int=post14)

		if post15:
			models.user.objects.filter(id=post0).update(integral_int=post15)

		if post16:
			models.user.objects.filter(id=post0).update(spread_int=post16)

		if post23:
			if post23 =='on':
				post23=True
			if post23 =='off':
				post23 = False
			if not dngadmin_common.html_gmid(id=post0) == False:
				off = "前台超级管理员不能操作"
				return HttpResponse(off)

			models.user.objects.filter(id=post0).update(frozen_bool=post23)


		if post25:
			models.user.objects.filter(id=post0).update(vipime_time=post25)


		if off:
			ok = off
		else:
			ok = 'yes'
			shijian = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			models.user.objects.filter(id=post0).update(update_time=shijian)

	else:
		ok =  '您没有修改权限'





	return HttpResponse(ok,off)

def htmluser_search(request):  #搜索

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

	zd_list = dngadmin_common.dng_ziduan("htmluser")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------


	post1 = request.GET.get(zd_list[0][1], '')  # 会员ID
	post2 = request.GET.get(zd_list[0][2], '')  # 会员账号
	post3 = request.GET.get(zd_list[0][3], '')  # 会员密码
	post4 = request.GET.get(zd_list[0][4], '')  # 昵称
	post5 = request.GET.get(zd_list[0][5], '')  # 性别
	post6 = request.GET.get(zd_list[0][6], '')  # 个人简介
	post7 = request.GET.get(zd_list[0][7], '')  # 邮箱
	post8 = request.GET.get(zd_list[0][8], '')  # 手机号
	post9 = request.GET.get(zd_list[0][9], '')  # 用户组
	post10 = request.GET.get(zd_list[0][10], '')  # 等级
	post11 = request.GET.get(zd_list[0][11], '')
	post12 = request.GET.get(zd_list[0][12], '')  # 余额
	post13 = request.GET.get(zd_list[0][13], '')  # 累计充值
	post14 = request.GET.get(zd_list[0][14], '')  # 累计消费
	post15 = request.GET.get(zd_list[0][15], '')  # 积分
	post16 = request.GET.get(zd_list[0][16], '')  # 推广注册
	post17 = request.GET.get(zd_list[0][17], '')
	post18 = request.GET.get(zd_list[0][18], '')
	post19 = request.GET.get(zd_list[0][19], '')
	post20 = request.GET.get(zd_list[0][20], '')
	post21 = request.GET.get(zd_list[0][21], '')
	post22 = request.GET.get(zd_list[0][22], '')
	post23 = request.GET.get(zd_list[0][23], '')  # 允许登录
	post24 = request.GET.get(zd_list[0][24], '')
	post25 = request.GET.get(zd_list[0][25], '')  # 登录时限
	post26 = request.GET.get(zd_list[0][26], '')  # 登录时限
	post27 = request.GET.get(zd_list[0][27], '')  # 登录时限

	page = request.GET.get('page', '')  # 第几页
	limit = request.GET.get('limit', '')  # 每页显示多少

	page = int(page)
	limit = int(limit)

	if   post1:

		dngred = models.user.objects.filter(uid_int__contains=post1).order_by('-id')

	elif post2:

		dngred = models.user.objects.filter(username_str__contains=post2).order_by('-id')

	elif post3:
		dngred = models.user.objects.filter(password_str__contains=post3).order_by('-id')

	elif post4:
		dngred = models.user.objects.filter(name_str__contains=str(post4)).order_by('-id')

	elif post5:
		dngred = models.user.objects.filter(gender_str__contains=post5).order_by('-id')

	elif post6:
		dngred = models.user.objects.filter(introduce_str__contains=post6).order_by('-id')

	elif post7:
		dngred = models.user.objects.filter(emall_str__contains=post7).order_by('-id')

	elif post8:
		dngred = models.user.objects.filter(mobile_str__contains=post8).order_by('-id')

	elif post9:
		gp = models.usergroup.objects.filter(gname_str__contains=post9).first()
		dngred = models.user.objects.filter(group_int__contains=gp.gid_int).order_by('-id')

	elif post10:
		dngred = models.user.objects.filter(rank_str__contains=post10).order_by('-id')

	elif post11:
		dngred = models.user.objects.filter(gm_bool__contains=post11).order_by('-id')

	elif post12:
		dngred = models.user.objects.filter(money_int__contains=post12).order_by('-id')

	elif post13:
		dngred = models.user.objects.filter(totalmoney_int__contains=post13).order_by('-id')

	elif post14:
		dngred = models.user.objects.filter(totalspend_int__contains=post14).order_by('-id')

	elif post15:
		dngred = models.user.objects.filter(integral_int__contains=post15).order_by('-id')

	elif post16:
		dngred = models.user.objects.filter(spread_int__contains=post16).order_by('-id')

	elif post17:
		dngred = models.user.objects.filter(ip_str__contains=post17).order_by('-id')

	elif post18:
		dngred = models.user.objects.filter(shebei_str__contains=post18).order_by('-id')

	elif post19:
		dngred = models.user.objects.filter(cookie_str__contains=post19).order_by('-id')

	elif post20:
		dngred = models.user.objects.filter(token_str__contains=post20).order_by('-id')

	elif post21:
		dngred = models.user.objects.filter(days_int__contains=post21).order_by('-id')

	elif post22:
		dngred = models.user.objects.filter(pwderror_int__contains=post22).order_by('-id')

	elif post23:
		dngred = models.user.objects.filter(frozen_bool__contains=post23).order_by('-id')

	elif post24:
		dngred = models.user.objects.filter(frozentime_str__contains=post24).order_by('-id')

	elif post25:
		dngred = models.user.objects.filter(vipime_time__contains=post25).order_by('-id')

	elif post26:
		dngred = models.user.objects.filter(create_time__contains=post26).order_by('-id')

	elif post27:
		dngred = models.user.objects.filter(update_time__contains=post27).order_by('-id')

	else:
		dngred = models.user.objects.filter().order_by('-id')

	paginator = Paginator(dngred, limit)

	list_count = paginator.count  # 总数据量
	num_pages = paginator.num_pages  # 有多少分页

	book_list = paginator.page(page)

	data = []
	for key in book_list:
		group = dngadmin_common.html_usergroup(gid=dngadmin_common.html_user(key.uid_int).group_int)
		data.append({"id": str(key.id),
					 "uid_int": str(key.uid_int),
					 "username_str": str(key.username_str),
					 "password_str": str("******"),
					 "name_str": str(key.name_str),
					 "gender_str": str(key.gender_str),
					 "introduce_str": str(key.introduce_str),
					 "emall_str": str(key.emall_str),
					 "mobile_str": str(key.mobile_str),
					 "group_int": str(group.gname_str),
					 "rank_str": str(key.rank_str),
					 "gm_bool": str(key.gm_bool),
					 "money_int": str(key.money_int),
					 "totalmoney_int": str(key.totalmoney_int),
					 "totalspend_int": str(key.totalspend_int),
					 "integral_int": str(key.integral_int),
					 "spread_int": str(key.spread_int),
					 "ip_str": str(key.ip_str),
					 "shebei_str": str(key.shebei_str),
					 "cookie_str": str("******"),
					 "token_str": str("******"),
					 "days_int": str(key.days_int),
					 "pwderror_int": str(key.pwderror_int),
					 "frozen_bool": str(key.frozen_bool),
					 "frozentime_str": str(key.frozentime_str),
					 "vipime_time": str(key.vipime_time.strftime("%Y-%m-%d %H:%M:%S")),
					 "create_time": str(key.create_time.strftime("%Y-%m-%d %H:%M:%S")),
					 "update_time": str(key.update_time.strftime("%Y-%m-%d %H:%M:%S")),

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