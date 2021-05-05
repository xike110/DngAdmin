

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



def adminmenu(request):
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

	zd_list = dngadmin_common.dng_ziduan("adminmenu") #获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------



	#biaodan = dngadmin_common.dng_dnguser(uid=dnguser_uid)

	vis = zip(zd_list[0], zd_list[1])
	return render(request,"dngadmin/adminmenu.html",{
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


def adminmenu_json(request):
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

	zd_list = dngadmin_common.dng_ziduan("adminmenu")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------



	page = request.GET.get('page', '')  # 第几页
	limit = request.GET.get('limit', '') #每页显示多少

	page = int(page)
	limit =int(limit)

	dngred = models.dngroute.objects.filter().order_by('-id')
	paginator = Paginator(dngred, limit)

	list_count = paginator.count  # 总数据量
	num_pages = paginator.num_pages #有多少分页

	book_list = paginator.page(page)


	data = []
	for key in book_list:

		#group  = dngadmin_common.html_usergroup(gid=dngadmin_common.html_user(key.uperior_int).group_int)

		data.append({"id": str(key.id),
					 	"uid_int": str(key.uid_int),#菜单id
						"name_str": str(key.name_str),#菜单名称
						"url_str": str(key.url_str),#菜单URL
						"icon_str": str(key.icon_str),#菜单图标
						"model_str": str(key.model_str),#菜单模型
						"superior_int": str(key.superior_int),#上级菜单
						"sort_int": str(key.sort_int),#菜单排序
						"integral_int": str(key.integral_int),#积分阈值
						"money_int": str(key.money_int),#余额阈值
						"totalmoney_int": str(key.totalmoney_int),#充值阈值
						"totalspend_int": str(key.totalspend_int),#消费阈值
						"spread_int": str(key.spread_int),#推广阈值
						"display_bool": str(key.display_bool),#菜单显示
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








def adminmenu_added(request):  #新增
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

	zd_list = dngadmin_common.dng_ziduan("adminmenu")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------

	post2 = request.POST.get(zd_list[0][2], '')#名称
	post3 = request.POST.get(zd_list[0][3], '')#URL
	post5 = request.POST.get(zd_list[0][5], '')#菜单模型
	post6 = request.POST.get(zd_list[0][6], '')#上级菜单

	ok = '新增失败'
	off = False
	pwname =models.dngroute.objects.filter(name_str=post2).only('name_str')
	pwurl = models.dngroute.objects.filter(url_str=post3).only('url_str')

	if added:

		if not post2:
			off ='菜单名称不能为空'

		elif pwname:
			off = '菜单名称不能重复'
		elif pwurl:

			off = '已经有重复菜单URL路径'

		else:

			users = models.dngusergroup.objects.filter(gid_int=1).first()  # 读用户组权限
			ider = models.dngroute.objects.filter().order_by('-uid_int').first()  # 读ID
			sortdb = models.dngroute.objects.filter().order_by('-sort_int').first()  # 读排序

			uid = int(ider.uid_int) + 1  # 会员ID递增
			sort = int(sortdb.sort_int) + 10  # 排序递增
			qx_menu = users.menu_text + "|" + str(uid) + "|"
			qx_added = users.added_text + "|" + str(uid) + "|"
			qx_delete = users.delete_text + "|" + str(uid) + "|"
			qx_update = users.update_text + "|" + str(uid) + "|"
			qx_see = users.see_text + "|" + str(uid) + "|"

			models.dngroute.objects.create(uid_int=uid, name_str=post2, url_str=post3, model_str=post5,
										   superior_int=post6, sort_int=sort)  # 增加菜单表
			models.dngusergroup.objects.filter(gid_int=1).update(menu_text=qx_menu, added_text=qx_added,
																 delete_text=qx_delete, update_text=qx_update,
																 see_text=qx_see)  # 更新管理员用户组权限

		if off:
			ok = off
		else:
			ok = 'yes'
	else:
		ok = '您没有新增权限'




	return HttpResponse(ok)



def adminmenu_delete(request):  #删除
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

	zd_list = dngadmin_common.dng_ziduan("adminmenu")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------

	delete_id = request.GET.get('delete_id') #接收单个删除

	id = request.POST.get('id', '') #接收批量删除

	ok = '删除失败'





	if delete: #判断删除权限

		if delete_id: #判断单个删除
			uxxg = models.dngroute.objects.filter(id=delete_id).first()
			udhg = models.dngroute.objects.filter(superior_int=uxxg.uid_int).first()
			if udhg:
				off = "下面还有二级菜单,不能删除"
				return HttpResponse(off)

			ok = models.dngroute.objects.filter(id=delete_id).delete()

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
					uxxg = models.dngroute.objects.filter(id=key).first()
					udhg = models.dngroute.objects.filter(superior_int=uxxg.uid_int).first()
					if udhg:
						off = "下面还有二级菜单,不能删除"
						return HttpResponse(off)

					ok = models.dngroute.objects.filter(id=key).delete()
					if ok:
						ok = 'yes'
					else:
						ok = 'no'


			else:
				int(id)

				uxxg = models.dngroute.objects.filter(id=id).first()
				udhg = models.dngroute.objects.filter(superior_int=uxxg.uid_int).first()
				if udhg:
					off = "下面还有二级菜单,不能删除"
					return HttpResponse(off)

				ok = models.dngroute.objects.filter(id=id).delete()
				if ok:
					ok = 'yes'
				else:
					ok = 'no'

	else:
		ok = parse.quote('您没有删除权限')




	return HttpResponse(ok)



def adminmenu_update(request):  #更新修改
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

	zd_list = dngadmin_common.dng_ziduan("adminmenu") #获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------
	post0 = request.POST.get(zd_list[0][0], '')
	post1 = request.POST.get(zd_list[0][1], '')
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


	ok ='修改失败'
	off=False
	if update:

		if not post0:

			off = "空ID"
			exit()  # 终止

		if post1:
			models.dngroute.objects.filter(id=post0).update(uid_int=post1)  # 菜单id
		if post2:
			models.dngroute.objects.filter(id=post0).update(name_str=post2)  # 菜单名称
		if post3:
			models.dngroute.objects.filter(id=post0).update(url_str=post3)  # 菜单URL
		if post4:
			models.dngroute.objects.filter(id=post0).update(icon_str=post4)  # 菜单图标
		if post5:
			models.dngroute.objects.filter(id=post0).update(model_str=post5)  # 菜单模型
		if post6:
			models.dngroute.objects.filter(id=post0).update(superior_int=post6)  # 上级菜单
		if post7:
			models.dngroute.objects.filter(id=post0).update(sort_int=post7)  # 菜单排序
		if post8:
			models.dngroute.objects.filter(id=post0).update(integral_int=post8)  # 积分阈值
		if post9:
			models.dngroute.objects.filter(id=post0).update(money_int=post9)  # 余额阈值
		if post10:
			models.dngroute.objects.filter(id=post0).update(totalmoney_int=post10)  # 充值阈值
		if post11:
			models.dngroute.objects.filter(id=post0).update(totalspend_int=post11)  # 消费阈值
		if post12:
			models.dngroute.objects.filter(id=post0).update(spread_int=post12)  # 推广阈值

		if post13:
			if post13=='on':
				post13=True
				models.dngroute.objects.filter(id=post0).update(display_bool=post13)  # 菜单显示
			elif post13=='off':
				post13 = False
				models.dngroute.objects.filter(id=post0).update(display_bool=post13)  # 菜单显示



		ok = 'yes'
	else:
		ok =  '您没有修改权限'





	return HttpResponse(ok,off)

def adminmenu_search(request):  #搜索

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

	zd_list = dngadmin_common.dng_ziduan("adminmenu")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------


	post1 = request.GET.get(zd_list[0][1], '')
	post2 = request.GET.get(zd_list[0][2], '')
	post3 = request.GET.get(zd_list[0][3], '')
	post4 = request.GET.get(zd_list[0][4], '')
	post5 = request.GET.get(zd_list[0][5], '')
	post6 = request.GET.get(zd_list[0][6], '')
	post7 = request.GET.get(zd_list[0][7], '')
	post8 = request.GET.get(zd_list[0][8], '')
	post9 = request.GET.get(zd_list[0][9], '')
	post10 = request.GET.get(zd_list[0][10], '')
	post11 = request.GET.get(zd_list[0][11], '')
	post12 = request.GET.get(zd_list[0][12], '')
	post13 = request.GET.get(zd_list[0][13], '')



	page = request.GET.get('page', '')  # 第几页
	limit = request.GET.get('limit', '')  # 每页显示多少

	page = int(page)
	limit = int(limit)

	if post1:
		dngred = models.dngroute.objects.filter(uid_int__contains=post1).order_by('-id')
	elif post1:
		dngred = models.dngroute.objects.filter(uid_int__contains=post1).order_by('-id')
	elif post2:
		dngred = models.dngroute.objects.filter(name_str__contains=post2).order_by('-id')
	elif post3:
		dngred = models.dngroute.objects.filter(url_str__contains=post3).order_by('-id')
	elif post4:
		dngred = models.dngroute.objects.filter(icon_str__contains=post4).order_by('-id')
	elif post5:
		dngred = models.dngroute.objects.filter(model_str__contains=post5).order_by('-id')
	elif post6:
		dngred = models.dngroute.objects.filter(superior_int__contains=post6).order_by('-id')
	elif post7:
		dngred = models.dngroute.objects.filter(sort_int__contains=post7).order_by('-id')
	elif post8:
		dngred = models.dngroute.objects.filter(integral_int__contains=post8).order_by('-id')
	elif post9:
		dngred = models.dngroute.objects.filter(money_int__contains=post9).order_by('-id')
	elif post10:
		dngred = models.dngroute.objects.filter(totalmoney_int__contains=post10).order_by('-id')
	elif post11:
		dngred = models.dngroute.objects.filter(totalspend_int__contains=post11).order_by('-id')
	elif post12:
		dngred = models.dngroute.objects.filter(spread_int__contains=post12).order_by('-id')
	elif post13:
		dngred = models.dngroute.objects.filter(display_bool__contains=post13).order_by('-id')

	else:
		dngred = models.dngroute.objects.filter().order_by('-id')

	paginator = Paginator(dngred, limit)

	list_count = paginator.count  # 总数据量
	num_pages = paginator.num_pages  # 有多少分页

	book_list = paginator.page(page)

	data = []
	for key in book_list:
		#group = dngadmin_common.html_usergroup(gid=dngadmin_common.html_user(key.uid_int).group_int)
		data.append({"id": str(key.id),
					 "uid_int": str(key.uid_int),  # 菜单id
					 "name_str": str(key.name_str),  # 菜单名称
					 "url_str": str(key.url_str),  # 菜单URL
					 "icon_str": str(key.icon_str),  # 菜单图标
					 "model_str": str(key.model_str),  # 菜单模型
					 "superior_int": str(key.superior_int),  # 上级菜单
					 "sort_int": str(key.sort_int),  # 菜单排序
					 "integral_int": str(key.integral_int),  # 积分阈值
					 "money_int": str(key.money_int),  # 余额阈值
					 "totalmoney_int": str(key.totalmoney_int),  # 充值阈值
					 "totalspend_int": str(key.totalspend_int),  # 消费阈值
					 "spread_int": str(key.spread_int),  # 推广阈值
					 "display_bool": str(key.display_bool),  # 菜单显示
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