

# Create your views here.
from django.shortcuts import render #视图渲染模块
from django.http import HttpResponse  #请求模块
from . import models #数据库操作模块
from django.db.models import Q #数据库逻辑模块
from django.db.models import Avg,Max,Min,Sum #数据库聚合计算模块
from datetime import datetime,timedelta #Cookie 模块
from django.http import HttpResponse, HttpResponseRedirect #重定向模块
from django.shortcuts import render
from django.forms.models import model_to_dict #结果转字典
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



def setup(request):
	# ----------------------------------------------------------
	#    通过路径获得栏目ID 》》》开始
	# ----------------------------------------------------------
	get_url = request.path
	get_url = get_url.split("/")  # 分割
	get_url = get_url[1] + "/" + get_url[2]
	if "_"in get_url:
		url = get_url.split("_")  # 分割
		get_url=url[0]
	uid=models.dngroute.objects.filter(url_str__contains=get_url).first()
	dngroute_uid = uid.uid_int
	# ----------------------------------------------------------
	#    日记记录与COOKIE验证与权限 》》》开始
	# ----------------------------------------------------------
	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	if not ip:
		ip = request.META['REMOTE_ADDR']# 原生获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	geturl = request.META.get('QUERY_STRING')  # 获取域名后缀的URL
	mulu_url = request.path  # 获取不包含？号之前的映射路径
	tishi = request.GET.get('tishi') #提示
	jinggao = request.GET.get('jinggao')  # 警告
	yes = request.GET.get('yes')  # 警告


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

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 开发者

	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------

	zd_list = dngadmin_common.dng_ziduan("setup") #获取对应表下所有字段值


	biaodan = dngadmin_common.dng_setup()
	# biao_list= model_to_dict(biaodan)
	# biao_list = list(biao_list)










	return render(request,"dngadmin/setup.html",{
		"title":dngroute.name_str,
		"edition": dngadmin_common.dng_setup().edition_str,  # 版本号
		"file": dngadmin_common.dng_setup().file_str,  # 备案号
		"tongue": dngadmin_common.dng_setup().statistics_text,  # 统计
		"added": added,#增
		"delete": delete,#删
		"update": update, #改
		"see": see, #开发者权限
		"tishi": tishi,
		"jinggao": jinggao,
		"yes": yes,
		"zd_list": zd_list,
		"biaodan": biaodan,






	})


def setup_post(request):
	# ----------------------------------------------------------
	#    通过路径获得栏目ID 》》》开始
	# ----------------------------------------------------------
	dngroute_uid = dngadmin_common.dng_ckurl(request)[0]
	get_url = dngadmin_common.dng_ckurl(request)[1]
	# ----------------------------------------------------------
	#    日记记录与COOKIE验证与权限 》》》开始
	# ----------------------------------------------------------
	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	if not ip:
		ip = request.META['REMOTE_ADDR']# 原生获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	geturl = request.META.get('QUERY_STRING')  # 获取域名后缀的URL
	mulu_url = request.path  # 获取不包含？号之前的映射路径



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

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 开发者

	zd_list = dngadmin_common.dng_ziduan("setup")  # 获取对应表下所有字段值
	tab = request.POST.get('tab', '')
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
	post14 = request.POST.get(zd_list[0][14], '')
	post15 = request.POST.get(zd_list[0][15], '')
	post16 = request.POST.get(zd_list[0][16], '')

	if tab =="1": #判断是不是后台设置提交
		if update:
			if not post1:
				urlstr = parse.quote(zd_list[1][1]+'不能为空')
				response = HttpResponseRedirect('/dngadmin/setup/?jinggao=' + urlstr)
				return response
			if not post2:
				urlstr = parse.quote(zd_list[1][2]+'不能为空')
				response = HttpResponseRedirect('/dngadmin/setup/?jinggao=' + urlstr)
				return response


			models.setup.objects.filter(id=1).update(setupname_str=post1,domain_str=post2,file_str=post3,edition_str=post4,statistics_text=post5)  # 更新修改数据库
			urlstr = parse.quote('修改成功')
			response = HttpResponseRedirect('/dngadmin/setup/?yes=' + urlstr)
			return response

		else:
			urlstr = parse.quote('您没有修改权限')
			response = HttpResponseRedirect('/dngadmin/setup/?jinggao=' + urlstr)
			return response


	elif tab =="2": #判断是不是表格提交

		if update:
			if not post6:
				urlstr = parse.quote(zd_list[1][6]+'不能为空')
				response = HttpResponseRedirect('/dngadmin/setup/?jinggao=' + urlstr)
				return response
			if not post7:
				urlstr = parse.quote(zd_list[1][7]+'不能为空')
				response = HttpResponseRedirect('/dngadmin/setup/?jinggao=' + urlstr)
				return response
			if not post8:
				urlstr = parse.quote(zd_list[1][8]+'不能为空')
				response = HttpResponseRedirect('/dngadmin/setup/?jinggao=' + urlstr)
				return response
			if not post9:
				urlstr = parse.quote(zd_list[1][9]+'不能为空')
				response = HttpResponseRedirect('/dngadmin/setup/?jinggao=' + urlstr)
				return response

			if post10 == 'on':
				post10 = True
			else:
				post10 = False



			if post13 == 'on':
				post13 = True
			else:
				post13 = False

			if post14 == 'on':
				post14 = 'exports'
			else:
				post14 = ''

			if post15 == 'on':
				post15 = 'print'
			else:
				post15 = ''
			if post16 == 'on':
				post16 = True
			else:
				post16 = False

			models.setup.objects.filter(id=1).update(inwidth_int=post6,wide_int=post7,high_int=post8,
													 limit_int=post9,toolbar_bool=post10,skinline_str=post11,
													 skinsize_str=post12,page_bool=post13,exports_str=post14,
													 print_str=post15,search_bool=post16)  # 更新修改数据库
			urlstr = parse.quote('修改成功')
			response = HttpResponseRedirect('/dngadmin/setup/?yes=' + urlstr)
			return response

		else:
			urlstr = parse.quote('您没有修改权限')
			response = HttpResponseRedirect('/dngadmin/setup/?jinggao=' + urlstr)
			return response