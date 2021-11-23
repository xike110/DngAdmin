

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
from . import dngadmin_formcommon #表单组件模块


def 映射的路径名替换(request):
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
	shebei = dngadmin_common.shebei(liulanqi)  # 判断移动设备


	if "dnguser_uid" in request.COOKIES:  # 判断cookies有无，跳转
		cookie_user_uid = request.get_signed_cookie(key="dnguser_uid", default=None,
												salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_name = request.get_signed_cookie(key="dnguser_name", default=None,
												 salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie_echo = request.get_signed_cookie(key="dnguser_cookie_echo", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie = request.get_signed_cookie(key="dnguser_cookie", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)

		cookie_pr = dngadmin_common.dng_yanzheng(cookie_user_uid, cookie_user_name, cookie_user_cookie,
												 cookie_user_cookie_echo)
		if cookie_pr:
			dnguser_uid =cookie_pr.uid_int #赋值ID
			dnguser_name = cookie_pr.username_str#赋值用户名
			dnguser_cookie=cookie_pr.cookie_str#赋值COOKIE记录
		else:
			return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('检测到非法登录'))

		if dngadmin_common.dng_anquan().tongshi_bool == False:  # 验证是否同时登录
			if dngadmin_common.dng_tongshi(uid=dnguser_uid, cookie=dnguser_cookie) == False:
				return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('不允许同时登录账号'))
	else:
		return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('您需要重新登录'))


	dnguser =dngadmin_common.dng_dnguser(dnguser_uid)
	group = dngadmin_common.dng_usergroup(gid=dnguser.group_int)  # 获取会员组名称
	groupall =	dngadmin_common.html_groupall()
	#groupall=zip(groupall[0], groupall[1])
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()#查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url: #判断URL统一
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您的访问与菜单映射不匹配</h1></center><div>""")

	elif not '|'+str(dngroute_uid)+'|'in group.menu_text: #判断菜单权限

		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您没有访问这个栏目的权限</h1></center><div>""")

	elif not dnguser.integral_int >= dngroute.integral_int:
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您积分"""+str(dnguser.integral_int)+""",访问需要达到"""+str(dngroute.integral_int)+"""积分！</h1></center><div>""")

	elif not dnguser.money_int >= dngroute.money_int:
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您余额"""+str(dnguser.money_int)+""",访问需要达到"""+str(dngroute.money_int)+"""余额！</h1></center><div>""")

	elif not dnguser.totalmoney_int >= dngroute.totalmoney_int:
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您累计充值""" + str(dnguser.totalmoney_int) + """,访问需要累计充值达到""" + str(dngroute.totalmoney_int) + """！</h1></center><div>""")

	elif not dnguser.totalspend_int >= dngroute.totalspend_int:
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您累计消费""" + str(dnguser.totalspend_int) + """,访问需要累计消费达到""" + str(dngroute.totalspend_int) + """！</h1></center><div>""")
	elif not dnguser.spread_int >= dngroute.spread_int:
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您推广""" + str(dnguser.spread_int) + """人,访问需要推广""" + str(dngroute.spread_int) + """人！</h1></center><div>""")

	added =dngadmin_common.dng_zsgc(dngroute_uid,group.added_text) #增
	delete = dngadmin_common.dng_zsgc(dngroute_uid,group.delete_text) #删
	update = dngadmin_common.dng_zsgc(dngroute_uid,group.update_text)#改
	see = dngadmin_common.dng_zsgc(dngroute_uid,group.see_text) #查

	zd_list = dngadmin_common.dng_ziduan("映射的路径名替换") #获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------



	#biaodan = dngadmin_common.dng_dnguser(uid=dnguser_uid)


	vist = zip(zd_list[0], zd_list[1])
	vis1 = zip(zd_list[0], zd_list[1])
	vis2 = zip(zd_list[0], zd_list[1])
	vis3 = zip(zd_list[0], zd_list[1])
	vis4 = zip(zd_list[0], zd_list[1])
	vis5 = zip(zd_list[0], zd_list[1])
	return render(request,"dngadmin/映射的路径名替换.html",{
		"title":dngroute.name_str,
		"xitong": xitong,  # 系统配置
		"shebei": shebei,  # 设备
		"dnguser_uid": dnguser_uid,
		"groupall": groupall,


		"get_url": get_url,#
		"added": added,#增
		"delete": delete,#删
		"update": update, #改
		"see": see, #开发者权限
		"zd_list": zd_list,  # 字段名称
		"vist": vist,
		"vis1": vis1,
		"vis2": vis2,
		"vis3": vis3,
		"vis4": vis4,
		"vis5": vis5,

		"tishi": tishi,
		"jinggao": jinggao,
		"yes": yes,
		"yuming_url": yuming_url,






	})


def 映射的路径名替换_json(request):
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
		cookie_user_uid = request.get_signed_cookie(key="dnguser_uid", default=None,
												salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_name = request.get_signed_cookie(key="dnguser_name", default=None,
												 salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie_echo = request.get_signed_cookie(key="dnguser_cookie_echo", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie = request.get_signed_cookie(key="dnguser_cookie", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)

		cookie_pr = dngadmin_common.dng_yanzheng(cookie_user_uid, cookie_user_name, cookie_user_cookie,
												 cookie_user_cookie_echo)
		if cookie_pr:
			dnguser_uid =cookie_pr.uid_int #赋值ID
			dnguser_name = cookie_pr.username_str#赋值用户名
			dnguser_cookie=cookie_pr.cookie_str#赋值COOKIE记录
		else:
			return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('检测到非法登录'))

		if dngadmin_common.dng_anquan().tongshi_bool == False:  # 验证是否同时登录
			if dngadmin_common.dng_tongshi(uid=dnguser_uid, cookie=dnguser_cookie) == False:
				return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('不允许同时登录账号'))
	else:
		return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('您需要重新登录'))

	dnguser =dngadmin_common.dng_dnguser(dnguser_uid)
	group = dngadmin_common.dng_usergroup(gid=dnguser.group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()  # 查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url:  # 判断URL统一
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您的访问与菜单映射不匹配</h1></center><div>""")

	elif not '|' + str(dngroute_uid) + '|' in group.menu_text:  # 判断菜单权限
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您没有访问这个栏目的权限</h1></center><div>""")

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 开发者

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
	def deal_json_invaild(data):
		#过滤字符，防止JSON解释报错
		datas = str(data).replace('\'', ' ').replace('\"', ' ')
		return datas
	for key in book_list:

		#group  = dngadmin_common.html_usergroup(gid=dngadmin_common.html_user(key.uperior_int).group_int)

		data.append({
			# ⊙json查看替换⊙ #
		})


	#下面开始构造JSON格式
	datajson = """{"code": 0,"msg": "","count":""" + str(list_count) + ""","data":""" + str(data) + """}"""

	datajson = datajson.replace('\'', '\"')  # 替换成AJAX可以解析得格式


	return HttpResponse(datajson)








def 映射的路径名替换_added(request):  #新增
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
		cookie_user_uid = request.get_signed_cookie(key="dnguser_uid", default=None,
												salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_name = request.get_signed_cookie(key="dnguser_name", default=None,
												 salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie_echo = request.get_signed_cookie(key="dnguser_cookie_echo", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie = request.get_signed_cookie(key="dnguser_cookie", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)

		cookie_pr = dngadmin_common.dng_yanzheng(cookie_user_uid, cookie_user_name, cookie_user_cookie,
												 cookie_user_cookie_echo)
		if cookie_pr:
			dnguser_uid =cookie_pr.uid_int #赋值ID
			dnguser_name = cookie_pr.username_str#赋值用户名
			dnguser_cookie=cookie_pr.cookie_str#赋值COOKIE记录
		else:
			return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('检测到非法登录'))

		if dngadmin_common.dng_anquan().tongshi_bool == False:  # 验证是否同时登录
			if dngadmin_common.dng_tongshi(uid=dnguser_uid, cookie=dnguser_cookie) == False:
				return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('不允许同时登录账号'))
	else:
		return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('您需要重新登录'))

	dnguser =dngadmin_common.dng_dnguser(dnguser_uid)
	group = dngadmin_common.dng_usergroup(gid=dnguser.group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()  # 查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url:  # 判断URL统一
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您的访问与菜单映射不匹配</h1></center><div>""")

	elif not '|' + str(dngroute_uid) + '|' in group.menu_text:  # 判断菜单权限
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您没有访问这个栏目的权限</h1></center><div>""")

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 开发者

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
		cookie_user_uid = request.get_signed_cookie(key="dnguser_uid", default=None,
												salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_name = request.get_signed_cookie(key="dnguser_name", default=None,
												 salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie_echo = request.get_signed_cookie(key="dnguser_cookie_echo", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie = request.get_signed_cookie(key="dnguser_cookie", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)

		cookie_pr = dngadmin_common.dng_yanzheng(cookie_user_uid, cookie_user_name, cookie_user_cookie,
												 cookie_user_cookie_echo)
		if cookie_pr:
			dnguser_uid =cookie_pr.uid_int #赋值ID
			dnguser_name = cookie_pr.username_str#赋值用户名
			dnguser_cookie=cookie_pr.cookie_str#赋值COOKIE记录
		else:
			return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('检测到非法登录'))

		if dngadmin_common.dng_anquan().tongshi_bool == False:  # 验证是否同时登录
			if dngadmin_common.dng_tongshi(uid=dnguser_uid, cookie=dnguser_cookie) == False:
				return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('不允许同时登录账号'))
	else:
		return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('您需要重新登录'))

	dnguser =dngadmin_common.dng_dnguser(dnguser_uid)
	group = dngadmin_common.dng_usergroup(gid=dnguser.group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()  # 查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url:  # 判断URL统一
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您的访问与菜单映射不匹配</h1></center><div>""")

	elif not '|' + str(dngroute_uid) + '|' in group.menu_text:  # 判断菜单权限
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您没有访问这个栏目的权限</h1></center><div>""")

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 开发者

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
		cookie_user_uid = request.get_signed_cookie(key="dnguser_uid", default=None,
												salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_name = request.get_signed_cookie(key="dnguser_name", default=None,
												 salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie_echo = request.get_signed_cookie(key="dnguser_cookie_echo", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie = request.get_signed_cookie(key="dnguser_cookie", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)

		cookie_pr = dngadmin_common.dng_yanzheng(cookie_user_uid, cookie_user_name, cookie_user_cookie,
												 cookie_user_cookie_echo)
		if cookie_pr:
			dnguser_uid =cookie_pr.uid_int #赋值ID
			dnguser_name = cookie_pr.username_str#赋值用户名
			dnguser_cookie=cookie_pr.cookie_str#赋值COOKIE记录
		else:
			return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('检测到非法登录'))

		if dngadmin_common.dng_anquan().tongshi_bool == False:  # 验证是否同时登录
			if dngadmin_common.dng_tongshi(uid=dnguser_uid, cookie=dnguser_cookie) == False:
				return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('不允许同时登录账号'))
	else:
		return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('您需要重新登录'))


	dnguser =dngadmin_common.dng_dnguser(dnguser_uid)
	group = dngadmin_common.dng_usergroup(gid=dnguser.group_int)  # 获取会员组名称

	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()#查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url: #判断URL统一
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您的访问与菜单映射不匹配</h1></center><div>""")

	elif not '|'+str(dngroute_uid)+'|'in group.menu_text: #判断菜单权限

		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您没有访问这个栏目的权限</h1></center><div>""")

	elif not dnguser.integral_int >= dngroute.integral_int:
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您积分"""+str(dnguser.integral_int)+""",访问需要达到"""+str(dngroute.integral_int)+"""积分！</h1></center><div>""")

	elif not dnguser.money_int >= dngroute.money_int:
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您余额"""+str(dnguser.money_int)+""",访问需要达到"""+str(dngroute.money_int)+"""余额！</h1></center><div>""")

	elif not dnguser.totalmoney_int >= dngroute.totalmoney_int:
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您累计充值""" + str(dnguser.totalmoney_int) + """,访问需要累计充值达到""" + str(dngroute.totalmoney_int) + """！</h1></center><div>""")

	elif not dnguser.totalspend_int >= dngroute.totalspend_int:
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您累计消费""" + str(dnguser.totalspend_int) + """,访问需要累计消费达到""" + str(dngroute.totalspend_int) + """！</h1></center><div>""")
	elif not dnguser.spread_int >= dngroute.spread_int:
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您推广""" + str(dnguser.spread_int) + """人,访问需要推广""" + str(dngroute.spread_int) + """人！</h1></center><div>""")

	added =dngadmin_common.dng_zsgc(dngroute_uid,group.added_text) #增
	delete = dngadmin_common.dng_zsgc(dngroute_uid,group.delete_text) #删
	update = dngadmin_common.dng_zsgc(dngroute_uid,group.update_text)#改
	see = dngadmin_common.dng_zsgc(dngroute_uid,group.see_text) #查

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
		cookie_user_uid = request.get_signed_cookie(key="dnguser_uid", default=None,
												salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_name = request.get_signed_cookie(key="dnguser_name", default=None,
												 salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie_echo = request.get_signed_cookie(key="dnguser_cookie_echo", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie = request.get_signed_cookie(key="dnguser_cookie", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)

		cookie_pr = dngadmin_common.dng_yanzheng(cookie_user_uid, cookie_user_name, cookie_user_cookie,
												 cookie_user_cookie_echo)
		if cookie_pr:
			dnguser_uid =cookie_pr.uid_int #赋值ID
			dnguser_name = cookie_pr.username_str#赋值用户名
			dnguser_cookie=cookie_pr.cookie_str#赋值COOKIE记录
		else:
			return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('检测到非法登录'))

		if dngadmin_common.dng_anquan().tongshi_bool == False:  # 验证是否同时登录
			if dngadmin_common.dng_tongshi(uid=dnguser_uid, cookie=dnguser_cookie) == False:
				return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('不允许同时登录账号'))
	else:
		return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('您需要重新登录'))

	dnguser =dngadmin_common.dng_dnguser(dnguser_uid)
	group = dngadmin_common.dng_usergroup(gid=dnguser.group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()  # 查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url:  # 判断URL统一
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您的访问与菜单映射不匹配</h1></center><div>""")

	elif not '|' + str(dngroute_uid) + '|' in group.menu_text:  # 判断菜单权限
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您没有访问这个栏目的权限</h1></center><div>""")

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 开发者

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


	def deal_json_invaild(data):
		# 过滤字符，防止JSON解释报错
		datas = str(data).replace('\'', ' ').replace('\"', ' ')
		return datas
	for key in book_list:
		#group = dngadmin_common.html_usergroup(gid=dngadmin_common.html_user(key.uid_int).group_int)
		data.append({"id": str(key.id),
					 # 3⊙search搜索替换⊙3 #
					 })

	# 下面开始构造JSON格式
	#下面开始构造JSON格式
	datajson = """{"code": 0,"msg": "","count":""" + str(list_count) + ""","data":""" + str(data) + """}"""

	datajson = datajson.replace('\'', '\"')  # 替换成AJAX可以解析得格式


	return HttpResponse(datajson)



@csrf_exempt
def 映射的路径名替换_api_json(request):  #api查询

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
	# # # # # 获取api授权# # # # #
	UID = request.META.get('HTTP_UID')
	USERNAME = request.META.get('HTTP_USERNAME')
	COOKIE = request.META.get('HTTP_COOKIE')
	TOKEN = request.META.get('HTTP_TOKEN')

	if "dnguser_uid" in request.COOKIES and not TOKEN:  # 判断cookies有无，跳转
		cookie_user_uid = request.get_signed_cookie(key="dnguser_uid", default=None,
												salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_name = request.get_signed_cookie(key="dnguser_name", default=None,
												 salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie_echo = request.get_signed_cookie(key="dnguser_cookie_echo", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie = request.get_signed_cookie(key="dnguser_cookie", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)

		cookie_pr = dngadmin_common.dng_yanzheng(cookie_user_uid, cookie_user_name, cookie_user_cookie,
												 cookie_user_cookie_echo)
		if cookie_pr:
			dnguser_uid =cookie_pr.uid_int #赋值ID
			dnguser_name = cookie_pr.username_str#赋值用户名
			dnguser_cookie=cookie_pr.cookie_str#赋值COOKIE记录
		else:
			return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('检测到非法登录'))

		if dngadmin_common.dng_anquan().tongshi_bool == False:  # 验证是否同时登录
			if dngadmin_common.dng_tongshi(uid=dnguser_uid, cookie=dnguser_cookie) == False:
				return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('不允许同时登录账号'))

	elif UID and USERNAME and COOKIE and TOKEN:  ####判断API用户

		cookie_pr = dngadmin_common.api_yanzheng(UID, USERNAME, TOKEN,COOKIE)
		if cookie_pr:
			dnguser_uid = cookie_pr.uid_int  # 赋值ID
			dnguser_name = cookie_pr.username_str  # 赋值用户名
			dnguser_cookie = cookie_pr.cookie_str  # 赋值COOKIE记录
		else:
			data = {
				'code': '1',
				'msg': '检测到非法登录',
			}
			return HttpResponse(json.dumps(data))

	else:



		data = {
			'code': '1',
			'msg': '您需要重新登录',
		}
		return HttpResponse(json.dumps(data))

	dnguser =dngadmin_common.dng_dnguser(dnguser_uid)
	group = dngadmin_common.dng_usergroup(gid=dnguser.group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()  # 查询路径取回本页面菜单信息


	if not dngroute.url_str in mulu_url:  # 判断URL统一
		data = {
			'code': '1',
			'msg': '您的访问与菜单映射不匹配',
		}
		return HttpResponse(json.dumps(data))

	elif not '|' + str(dngroute_uid) + '|' in group.menu_text:  # 判断菜单权限
		data = {
			'code': '1',
			'msg': '您没有访问这个菜单的权限',
		}
		return HttpResponse(json.dumps(data))
	elif not dnguser.integral_int >= dngroute.integral_int:
		data = {
			'code': '1',
			'msg': '您的积分不满足访问条件',
		}
		return HttpResponse(json.dumps(data))
	elif not dnguser.money_int >= dngroute.money_int:
		data = {
			'code': '1',

			'msg': '您的余额不满足访问条件',
		}
		return HttpResponse(json.dumps(data))
	elif not dnguser.totalmoney_int >= dngroute.totalmoney_int:
		data = {
			'code': '1',
			'msg': '您的累计充值不满足访问条件',
		}
		return HttpResponse(json.dumps(data))
	elif not dnguser.totalspend_int >= dngroute.totalspend_int:
		data = {
			'code': '1',
			'msg': '您的累计消费不满足访问条件',
		}
		return HttpResponse(json.dumps(data))
	elif not dnguser.spread_int >= dngroute.spread_int:
		data = {
			'code': '1',
			'msg': '您的推广人数不满足访问条件',
		}
		return HttpResponse(json.dumps(data))

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 开发者

	zd_list = dngadmin_common.dng_ziduan("映射的路径名替换")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------
	list_arry=models.映射的路径名替换.objects.filter().order_by ("-id")
	gongju = models.映射的路径名替换.objects.count()

	data = []
	for obj in list_arry:
		data.append(model_to_dict(obj))

	# 下面开始构造JSON格式
	datajson = """{"code":0,"msg":"成功","count":""" + str(gongju) + ""","data":""" + str(data) + """}"""

	datajson = datajson.replace('\'', '\"')  # 替换成AJAX可以解析得格式
	datajson = datajson.replace('True', '1')  # 替换成AJAX可以解析得格式
	datajson = datajson.replace('False', '0')  # 替换成AJAX可以解析得格式

	return HttpResponse(datajson)

@csrf_exempt
def 映射的路径名替换_api_post(request):
	# ----------------------------------------------------------
	#    通过路径获得栏目ID 》》》开始
	# ----------------------------------------------------------
	dngroute_uid = dngadmin_common.dng_ckurl(request)[0]
	get_url = dngadmin_common.dng_ckurl(request)[1]
	# ----------------------------------------------------------
	#    日记记录与COOKIE验证与权限 》》》开始
	# ----------------------------------------------------------
	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	geturl = request.META.get('QUERY_STRING')  # 获取域名后缀的URL
	mulu_url = request.path  # 获取不包含？号之前的映射路径
	# # # # # 获取api授权# # # # #
	UID = request.META.get('HTTP_UID')
	USERNAME = request.META.get('HTTP_USERNAME')
	COOKIE = request.META.get('HTTP_COOKIE')
	TOKEN = request.META.get('HTTP_TOKEN')


	if "dnguser_uid" in request.COOKIES and not TOKEN:  # 判断cookies有无，跳转
		cookie_user_uid = request.get_signed_cookie(key="dnguser_uid", default=None,
												salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_name = request.get_signed_cookie(key="dnguser_name", default=None,
												 salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie_echo = request.get_signed_cookie(key="dnguser_cookie_echo", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
		cookie_user_cookie = request.get_signed_cookie(key="dnguser_cookie", default=None,
												   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)

		cookie_pr = dngadmin_common.dng_yanzheng(cookie_user_uid, cookie_user_name, cookie_user_cookie,
												 cookie_user_cookie_echo)
		if cookie_pr:
			dnguser_uid =cookie_pr.uid_int #赋值ID
			dnguser_name = cookie_pr.username_str#赋值用户名
			dnguser_cookie=cookie_pr.cookie_str#赋值COOKIE记录
		else:
			return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('检测到非法登录'))

		if dngadmin_common.dng_anquan().tongshi_bool == False:  # 验证是否同时登录
			if dngadmin_common.dng_tongshi(uid=dnguser_uid, cookie=dnguser_cookie) == False:
				return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('不允许同时登录账号'))
	elif UID and USERNAME and COOKIE and TOKEN:  ####判断API用户

		cookie_pr = dngadmin_common.api_yanzheng(UID, USERNAME, TOKEN,COOKIE)
		if cookie_pr:
			dnguser_uid = cookie_pr.uid_int  # 赋值ID
			dnguser_name = cookie_pr.username_str  # 赋值用户名
			dnguser_cookie = cookie_pr.cookie_str  # 赋值COOKIE记录
		else:
			data = {
				'code': '1',
				'msg': '检测到非法登录',
			}
			return HttpResponse(json.dumps(data))

	else:
		data = {
			'code': '1',
			'msg': '请重新登录',
		}
		return HttpResponse(json.dumps(data))


	# ----------------------------------------------------------
	#    日记记录与COOKIE验证与权限《《《 结束
	# ----------------------------------------------------------
	# ----------------------------------------------------------
	#    判断页面权限开始》》》开始
	# ----------------------------------------------------------
	dnguser =dngadmin_common.dng_dnguser(dnguser_uid)
	group = dngadmin_common.dng_usergroup(gid=dnguser.group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()#查询路径取回本页面菜单信息
	dngadmin_common.dng_dngred(uid=dnguser_uid, title=dngroute.name_str, url=mulu_url, user=liulanqi, ip=ip)  # 日记记录函数

	if not dngroute.url_str in mulu_url: #判断URL统一

		data = {
			'code': '1',
			'msg': '您的访问与菜单映射不匹配',
		}
		return HttpResponse(json.dumps(data))


	elif not '|' + str(dngroute_uid) + '|' in group.menu_text:  # 判断菜单权限

		data = {

			'code': '1',

			'msg': '您没有访问这个菜单的权限',

		}

		return HttpResponse(json.dumps(data))

	elif not dnguser.integral_int >= dngroute.integral_int:

		data = {

			'code': '1',

			'msg': '您的积分不满足访问条件',

		}

		return HttpResponse(json.dumps(data))

	elif not dnguser.money_int >= dngroute.money_int:

		data = {

			'code': '1',

			'msg': '您的余额不满足访问条件',

		}

		return HttpResponse(json.dumps(data))

	elif not dnguser.totalmoney_int >= dngroute.totalmoney_int:

		data = {

			'code': '1',

			'msg': '您的累计充值不满足访问条件',

		}

		return HttpResponse(json.dumps(data))

	elif not dnguser.totalspend_int >= dngroute.totalspend_int:

		data = {

			'code': '1',

			'msg': '您的累计消费不满足访问条件',

		}

		return HttpResponse(json.dumps(data))

	elif not dnguser.spread_int >= dngroute.spread_int:

		data = {

			'code': '1',

			'msg': '您的推广人数不满足访问条件',

		}

		return HttpResponse(json.dumps(data))

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 开发者

	zd_list = dngadmin_common.dng_ziduan("映射的路径名替换") #获取对应表下所有字段值


	# 1⊙表单替换⊙1 #

	# 2⊙表单替换⊙2 #
	form = dngadmin_formcommon.form_add(zd_list, post_arry)#表单数据验算二次处理

	if update:
		if post0:

			# 3⊙表单替换⊙3 #

			data = {
				'code': '0',
				'msg': '修改成功',
			}
			return HttpResponse(json.dumps(data))

		else:


			# 4⊙表单替换⊙4 #

			data = {
				'code': '0',
				'msg': '新增成功',
			}
			return HttpResponse(json.dumps(data))

	else:

			data = {
				'code': '1',
				'msg': '您没有修改权限',
			}
			return HttpResponse(json.dumps(data))