

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



def mail(request):
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

	zd_list = dngadmin_common.dng_ziduan("mail") #获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------



	#biaodan = dngadmin_common.dng_dnguser(uid=dnguser_uid)

	vis = zip(zd_list[0], zd_list[1])
	return render(request,"dngadmin/mail.html",{
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


def mail_json(request):
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

	zd_list = dngadmin_common.dng_ziduan("mail")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------



	page = request.GET.get('page', '')  # 第几页
	limit = request.GET.get('limit', '') #每页显示多少

	page = int(page)
	limit =int(limit)

	dngred = models.mail.objects.filter().order_by('-id')
	paginator = Paginator(dngred, limit)

	list_count = paginator.count  # 总数据量
	num_pages = paginator.num_pages #有多少分页

	book_list = paginator.page(page)


	data = []
	for key in book_list:

		#group  = dngadmin_common.html_usergroup(gid=dngadmin_common.html_user(key.uperior_int).group_int)

		data.append({
			
			"id" : str(key.id), # ID
			
			"type_str" : str(key.type_str), # 邮件发送方式
			
			"host_str" : str(key.host_str), # SMTP服务器
			
			"port_str" : str(key.port_str), # SMTP端口
			
			"user_str" : str(key.user_str), # SMTP用户名
			
			"pass_str" : str(key.pass_str), # SMTP密码
			
			"verify_str" : str(key.verify_str), # SMTP验证方式
			
			"from_str" : str(key.from_str), # 发件人邮箱
			
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








def mail_added(request):  #新增
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

	zd_list = dngadmin_common.dng_ziduan("mail")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------

	
	post1 = request.POST.get(zd_list[0][1], '') #邮件发送方式
	
	post2 = request.POST.get(zd_list[0][2], '') #SMTP服务器
	
	post3 = request.POST.get(zd_list[0][3], '') #SMTP端口
	
	post4 = request.POST.get(zd_list[0][4], '') #SMTP用户名
	
	post5 = request.POST.get(zd_list[0][5], '') #SMTP密码
	
	post6 = request.POST.get(zd_list[0][6], '') #SMTP验证方式
	
	post7 = request.POST.get(zd_list[0][7], '') #发件人邮箱
	


	ok = 'no'
	if added:

		ok = models.mail.objects.create(type_str=post1, host_str=post2, port_str=post3, user_str=post4, pass_str=post5, verify_str=post6, from_str=post7, )  # 更新修改数据库
		if ok:
			ok = 'yes'
		else:
			ok = 'no'
	else:
		urlstr = '您没有新增权限'

		return urlstr

	return HttpResponse(ok)



def mail_delete(request):  #删除
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

	zd_list = dngadmin_common.dng_ziduan("mail")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------

	delete_id = request.GET.get('delete_id')
	id = request.POST.get('id', '')

	ok = 'no'

	if delete:  # 判断删除权限

		if delete_id:  # 判断单个删除

			ok = models.mail.objects.filter(id=delete_id).delete()

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
					ok = models.mail.objects.filter(id=key).delete()
					if ok:
						ok = 'yes'
					else:
						ok = 'no'


			else:
				int(id)
				ok = models.mail.objects.filter(id=id).delete()
				if ok:
					ok = 'yes'
				else:
					ok = 'no'
	else:
		urlstr = parse.quote('您没有删除权限')

		return urlstr

	return HttpResponse(ok)



def mail_update(request):  #更新修改
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

	zd_list = dngadmin_common.dng_ziduan("mail") #获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------
	post0 = request.POST.get(zd_list[0][0], '')
	
	post1 = request.POST.get(zd_list[0][1], '') #邮件发送方式
	
	post2 = request.POST.get(zd_list[0][2], '') #SMTP服务器
	
	post3 = request.POST.get(zd_list[0][3], '') #SMTP端口
	
	post4 = request.POST.get(zd_list[0][4], '') #SMTP用户名
	
	post5 = request.POST.get(zd_list[0][5], '') #SMTP密码
	
	post6 = request.POST.get(zd_list[0][6], '') #SMTP验证方式
	
	post7 = request.POST.get(zd_list[0][7], '') #发件人邮箱
	


	ok ='修改失败'
	off=False
	if update:

		if not post0:

			off = "空ID"
			exit()  # 终止
		
		if post1:
			models.mail.objects.filter(id=post0).update(type_str=post1)	
			
		if post2:
			models.mail.objects.filter(id=post0).update(host_str=post2)	
			
		if post3:
			models.mail.objects.filter(id=post0).update(port_str=post3)	
			
		if post4:
			models.mail.objects.filter(id=post0).update(user_str=post4)	
			
		if post5:
			models.mail.objects.filter(id=post0).update(pass_str=post5)	
			
		if post6:
			models.mail.objects.filter(id=post0).update(verify_str=post6)	
			
		if post7:
			models.mail.objects.filter(id=post0).update(from_str=post7)	
			


		ok = 'yes'
	else:
		ok =  '您没有修改权限'





	return HttpResponse(ok,off)

def mail_search(request):  #搜索

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

	zd_list = dngadmin_common.dng_ziduan("mail")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------


	
	post1 = request.POST.get(zd_list[0][1], '') #邮件发送方式
	
	post2 = request.POST.get(zd_list[0][2], '') #SMTP服务器
	
	post3 = request.POST.get(zd_list[0][3], '') #SMTP端口
	
	post4 = request.POST.get(zd_list[0][4], '') #SMTP用户名
	
	post5 = request.POST.get(zd_list[0][5], '') #SMTP密码
	
	post6 = request.POST.get(zd_list[0][6], '') #SMTP验证方式
	
	post7 = request.POST.get(zd_list[0][7], '') #发件人邮箱
	


	page = request.GET.get('page', '')  # 第几页
	limit = request.GET.get('limit', '')  # 每页显示多少

	page = int(page)
	limit = int(limit)


	
	if post1: 
		dngred = models.mail.objects.filter(type_str__contains=post1).order_by('-id') #邮件发送方式
	
	elif post2: 
		dngred = models.mail.objects.filter(host_str__contains=post2).order_by('-id') #SMTP服务器
	
	elif post3: 
		dngred = models.mail.objects.filter(port_str__contains=post3).order_by('-id') #SMTP端口
	
	elif post4: 
		dngred = models.mail.objects.filter(user_str__contains=post4).order_by('-id') #SMTP用户名
	
	elif post5: 
		dngred = models.mail.objects.filter(pass_str__contains=post5).order_by('-id') #SMTP密码
	
	elif post6: 
		dngred = models.mail.objects.filter(verify_str__contains=post6).order_by('-id') #SMTP验证方式
	
	elif post7: 
		dngred = models.mail.objects.filter(from_str__contains=post7).order_by('-id') #发件人邮箱
	
	else:
		dngred = models.mail.objects.filter().order_by('-id')

	paginator = Paginator(dngred, limit)

	list_count = paginator.count  # 总数据量
	num_pages = paginator.num_pages  # 有多少分页

	book_list = paginator.page(page)

	data = []
	for key in book_list:
		#group = dngadmin_common.html_usergroup(gid=dngadmin_common.html_user(key.uid_int).group_int)
		data.append({"id": str(key.id),
					 
					 "type_str": str(key.type_str),  # 邮件发送方式
					 "host_str": str(key.host_str),  # SMTP服务器
					 "port_str": str(key.port_str),  # SMTP端口
					 "user_str": str(key.user_str),  # SMTP用户名
					 "pass_str": str(key.pass_str),  # SMTP密码
					 "verify_str": str(key.verify_str),  # SMTP验证方式
					 "from_str": str(key.from_str),  # 发件人邮箱
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

