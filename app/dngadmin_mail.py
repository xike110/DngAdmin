

# Create your views here.
from django.shortcuts import render #视图渲染模块
from django.http import HttpResponse  #请求模块
from . import models #数据库操作模块
from django.db.models import Q #数据库逻辑模块
from django.db.models import Avg,Max,Min,Sum #数据库聚合计算模块
from datetime import datetime,timedelta #Cookie 模块
from django.http import HttpResponse, HttpResponseRedirect #重定向模块
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import os
import sys
import json
import sqlite3
from urllib import parse#转码
import re #正则模块
import random#随机模块
import hashlib# 加密模块
from django.utils import timezone #时间处理模块
import datetime#时间
import time# 日期模块
from . import dngadmin_common #公共函数
from . import dngadmin_formcommon #表单组件模块



def mail(request):
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
	yuming_url = request.META.get('HTTP_HOST')  # 当前访问的域名
	geturl = request.META.get('QUERY_STRING')  # 获取域名后缀的URL
	mulu_url = request.path  # 获取不包含？号之前的映射路径
	tishi = request.GET.get('tishi') #提示
	jinggao = request.GET.get('jinggao')  # 警告
	yes = request.GET.get('yes')  # 警告


	if "dnguser_uid" in request.COOKIES :  # 判断cookies有无，跳转
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

	zd_list = dngadmin_common.dng_ziduan("mail")  # 获取对应表下所有字段值
	db_values_list = models.mail.objects.filter().values_list()  # 获取数据返回元组列表格式
	html_form = dngadmin_formcommon.form_form(zd_list, db_values_list)  # 获取表单前端组件组合


	return render(request,"dngadmin/mail.html",{
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
		"html_form":html_form,


		"yuming_url": yuming_url,








	})


def mail_post(request):
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
	# # # # # 获取api授权# # # # #
	UID = request.META.get('HTTP_UID')
	USERNAME = request.META.get('HTTP_USERNAME')
	COOKIE = request.META.get('HTTP_COOKIE')
	TOKEN = request.META.get('HTTP_TOKEN')


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
	elif UID and USERNAME and COOKIE and TOKEN:  ####判断API用户

		cookie_pr = dngadmin_common.api_yanzheng(UID, USERNAME, TOKEN,COOKIE)
		if cookie_pr:
			dnguser_uid = cookie_pr.uid_int  # 赋值ID
			dnguser_name = cookie_pr.username_str  # 赋值用户名
			dnguser_cookie = cookie_pr.cookie_str  # 赋值COOKIE记录
		else:
			return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('检测到非法登录'))

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

	zd_list = dngadmin_common.dng_ziduan("mail") #获取对应表下所有字段值


	
	post0 = request.POST.get('id', '')#ID
	
	post1 = request.POST.get('mail_id', '')#邮件ID
	
	post2 = request.POST.get('type_str', '')#邮件发送方式
	
	post3 = request.POST.get('host_str', '')#SMTP服务器
	
	post4 = request.POST.get('port_str', '')#SMTP端口
	
	post5 = request.POST.get('pass_str', '')#SMTP授权码
	
	post6 = request.POST.get('from_str', '')#发件人邮箱
	

	post_arry =[post0,post1,post2,post3,post4,post5,post6,]
	form = dngadmin_formcommon.form_add(zd_list, post_arry)#表单数据验算二次处理

	if update:
		if post0:

			
			models.mail.objects.filter(id=post0).update(id=form[0])#ID
	
			models.mail.objects.filter(id=post0).update(mail_id=form[1])#邮件ID
	
			models.mail.objects.filter(id=post0).update(type_str=form[2])#邮件发送方式
	
			models.mail.objects.filter(id=post0).update(host_str=form[3])#SMTP服务器
	
			models.mail.objects.filter(id=post0).update(port_str=form[4])#SMTP端口
	
			models.mail.objects.filter(id=post0).update(pass_str=form[5])#SMTP授权码
	
			models.mail.objects.filter(id=post0).update(from_str=form[6])#发件人邮箱

			# 连接数据库(如果不存在则创建)
			conn = sqlite3.connect('app/ssh/config.db')
			# 创建游标
			cursor = conn.cursor()
			# 更新ID = 3 的name值
			cursor.execute('UPDATE emil SET host_str=? WHERE id=?', (form[3], 1))
			cursor.execute('UPDATE emil SET port_str=? WHERE id=?', (form[4], 1))
			cursor.execute('UPDATE emil SET pass_str=? WHERE id=?', (form[5], 1))
			cursor.execute('UPDATE emil SET from_str=? WHERE id=?', (form[6], 1))
			# 提交事物
			conn.commit()
			# 关闭游标
			cursor.close()
			# 关闭连接
			conn.close()
	

			urlstr = parse.quote('修改成功')
			response = HttpResponseRedirect('/dngadmin/mail/?yes=' + urlstr)
			return response

		else:

			if form[1]:
				form[1] = int(form[1]) + 1
			else:
				form[1] = 1
			models.mail.objects.create(mail_id=form[1], type_str=form[2], host_str=form[3], port_str=form[4], pass_str=form[5], from_str=form[6], )  #新增数据库

			# 连接数据库(如果不存在则创建)
			conn = sqlite3.connect('app/ssh/config.db')
			# 创建游标
			cursor = conn.cursor()
			# 更新ID = 3 的name值
			cursor.execute('UPDATE emil SET host_str=? WHERE id=?', (form[3], 1))
			cursor.execute('UPDATE emil SET port_str=? WHERE id=?', (form[4], 1))
			cursor.execute('UPDATE emil SET pass_str=? WHERE id=?', (form[5], 1))
			cursor.execute('UPDATE emil SET from_str=? WHERE id=?', (form[6], 1))
			# 提交事物
			conn.commit()
			# 关闭游标
			cursor.close()
			# 关闭连接
			conn.close()

			urlstr = parse.quote('新增成功')
			response = HttpResponseRedirect('/dngadmin/mail/?yes=' + urlstr)
			return response

	else:
			urlstr = parse.quote('您没有修改权限')
			response = HttpResponseRedirect('/dngadmin/mail/?jinggao=' + urlstr)
			return response


@csrf_exempt
def mail_api_json(request):  #api查询

	# ----------------------------------------------------------
	#   判断页面权限》》》 开始
	# ----------------------------------------------------------

	dngroute_uid = dngadmin_common.dng_ckurl(request)[0]
	get_url = dngadmin_common.dng_ckurl(request)[1]

	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	if not ip:
		ip = request.META['REMOTE_ADDR']# 原生获取ip信息
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

	zd_list = dngadmin_common.dng_ziduan("mail")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------
	list_arry=models.mail.objects.filter().order_by ("-id")
	gongju = models.mail.objects.count()

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
def mail_api_post(request):
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

	elif not '|'+str(dngroute_uid)+'|'in group.menu_text: #判断菜单权限

		data = {
			'code': '1',
			'msg': '您没有访问这个菜单的权限',
		}
		return HttpResponse(json.dumps(data))

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

	zd_list = dngadmin_common.dng_ziduan("mail") #获取对应表下所有字段值


	
	post0 = request.POST.get('id', '')#ID
	
	post1 = request.POST.get('mail_id', '')#邮件ID
	
	post2 = request.POST.get('type_str', '')#邮件发送方式
	
	post3 = request.POST.get('host_str', '')#SMTP服务器
	
	post4 = request.POST.get('port_str', '')#SMTP端口
	
	post5 = request.POST.get('pass_str', '')#SMTP授权码
	
	post6 = request.POST.get('from_str', '')#发件人邮箱
	

	post_arry =[post0,post1,post2,post3,post4,post5,post6,]
	form = dngadmin_formcommon.form_add(zd_list, post_arry)#表单数据验算二次处理

	if update:
		if post0:

			
			models.mail.objects.filter(id=post0).update(id=form[0])#ID
	
			models.mail.objects.filter(id=post0).update(mail_id=form[1])#邮件ID
	
			models.mail.objects.filter(id=post0).update(type_str=form[2])#邮件发送方式
	
			models.mail.objects.filter(id=post0).update(host_str=form[3])#SMTP服务器
	
			models.mail.objects.filter(id=post0).update(port_str=form[4])#SMTP端口
	
			models.mail.objects.filter(id=post0).update(pass_str=form[5])#SMTP授权码
	
			models.mail.objects.filter(id=post0).update(from_str=form[6])#发件人邮箱
	

			data = {
				'code': '0',
				'msg': '修改成功',
			}
			return HttpResponse(json.dumps(data))

		else:


			models.mail.objects.create(mail_id=form[1], type_str=form[2], host_str=form[3], port_str=form[4], pass_str=form[5], from_str=form[6], )  #新增数据库

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