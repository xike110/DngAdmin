

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
import os
import sys
import json
from urllib import parse#转码
import re #正则模块
import random#随机模块
import hashlib# 加密模块
from django.utils import timezone #时间处理模块
import datetime#时间
import time# 日期模块
from . import dngadmin_common #公共函数
from . import dngadmin_formcommon #表单组件模块



def formdemo(request):
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
	yuming_url = request.META.get('HTTP_HOST')  # 当前访问的域名
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

	zd_list = dngadmin_common.dng_ziduan("formdemo")  # 获取对应表下所有字段值
	db_values_list = models.formdemo.objects.filter().values_list()  # 获取数据返回元组列表格式
	html_form = dngadmin_formcommon.form_form(zd_list, db_values_list)  # 获取表单前端组件组合


	return render(request,"dngadmin/formdemo.html",{
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


def formdemo_post(request):
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

	zd_list = dngadmin_common.dng_ziduan("formdemo") #获取对应表下所有字段值


	
	post0 = request.POST.get('id', '')#ID
	
	post1 = request.POST.get('demoid_id', '')#表单ID
	
	post2 = request.POST.get('wenben_str', '')#文本框
	
	post3 = request.POST.get('jinyong_stop', '')#禁用框
	
	post4 = request.POST.get('mima_psd', '')#密码框
	
	post5 = request.POST.get('shouji_phone', '')#手机框
	
	post6 = request.POST.get('youjian_email', '')#邮件框
	
	post7 = request.POST.get('shenfen_entity', '')#身份证框
	
	post8 = request.POST.get('shuzi_int', '')#数字框
	
	post9 = request.POST.get('xuanze_xiala', '')#下拉框
	
	post10 = request.POST.get('xuanze_xuanze', '')#选择框
	
	post11 = request.POST.get('shu_shudanxuan', '')#竖单选框
	
	post12 = request.POST.get('heng_hengdanxuan', '')#横单选框
	
	post13 = request.POST.get('kaiguan_bool', '')#启动开关
	
	post14 = request.POST.get('riqi_years', '')#日期框
	
	post15 = request.POST.get('datetime_datetime', '')#日期时间框
	
	post16 = request.POST.get('fuwenben_text', '')#富文本框
	

	post_arry =[post0,post1,post2,post3,post4,post5,post6,post7,post8,post9,post10,post11,post12,post13,post14,post15,post16,]
	form = dngadmin_formcommon.form_add(zd_list, post_arry)#表单数据验算二次处理

	if update:
		if post0:

			
			models.formdemo.objects.filter(id=post0).update(id=form[0])#ID
	
			models.formdemo.objects.filter(id=post0).update(demoid_id=form[1])#表单ID
	
			models.formdemo.objects.filter(id=post0).update(wenben_str=form[2])#文本框
	
			models.formdemo.objects.filter(id=post0).update(jinyong_stop=form[3])#禁用框
	
			models.formdemo.objects.filter(id=post0).update(mima_psd=form[4])#密码框
	
			models.formdemo.objects.filter(id=post0).update(shouji_phone=form[5])#手机框
	
			models.formdemo.objects.filter(id=post0).update(youjian_email=form[6])#邮件框
	
			models.formdemo.objects.filter(id=post0).update(shenfen_entity=form[7])#身份证框
	
			models.formdemo.objects.filter(id=post0).update(shuzi_int=form[8])#数字框
	
			models.formdemo.objects.filter(id=post0).update(xuanze_xiala=form[9])#下拉框
	
			models.formdemo.objects.filter(id=post0).update(xuanze_xuanze=form[10])#选择框
	
			models.formdemo.objects.filter(id=post0).update(shu_shudanxuan=form[11])#竖单选框
	
			models.formdemo.objects.filter(id=post0).update(heng_hengdanxuan=form[12])#横单选框
	
			models.formdemo.objects.filter(id=post0).update(kaiguan_bool=form[13])#启动开关
	
			models.formdemo.objects.filter(id=post0).update(riqi_years=form[14])#日期框
	
			models.formdemo.objects.filter(id=post0).update(datetime_datetime=form[15])#日期时间框
	
			models.formdemo.objects.filter(id=post0).update(fuwenben_text=form[16])#富文本框
	

			urlstr = parse.quote('修改成功')
			response = HttpResponseRedirect('/dngadmin/formdemo/?yes=' + urlstr)
			return response

		else:

			if form[1]:
				form[1] = int(form[1]) + 1
			else:
				form[1] = 1
			models.formdemo.objects.create(demoid_id=form[1], wenben_str=form[2], jinyong_stop=form[3], mima_psd=form[4], shouji_phone=form[5], youjian_email=form[6], shenfen_entity=form[7], shuzi_int=form[8], xuanze_xiala=form[9], xuanze_xuanze=form[10], shu_shudanxuan=form[11], heng_hengdanxuan=form[12], kaiguan_bool=form[13], riqi_years=form[14], datetime_datetime=form[15], fuwenben_text=form[16], )  #新增数据库

			urlstr = parse.quote('新增成功')
			response = HttpResponseRedirect('/dngadmin/formdemo/?yes=' + urlstr)
			return response

	else:
			urlstr = parse.quote('您没有修改权限')
			response = HttpResponseRedirect('/dngadmin/formdemo/?jinggao=' + urlstr)
			return response


def formdemo_api_post(request):
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

	zd_list = dngadmin_common.dng_ziduan("formdemo") #获取对应表下所有字段值


	
	post0 = request.POST.get('id', '')#ID
	
	post1 = request.POST.get('demoid_id', '')#表单ID
	
	post2 = request.POST.get('wenben_str', '')#文本框
	
	post3 = request.POST.get('jinyong_stop', '')#禁用框
	
	post4 = request.POST.get('mima_psd', '')#密码框
	
	post5 = request.POST.get('shouji_phone', '')#手机框
	
	post6 = request.POST.get('youjian_email', '')#邮件框
	
	post7 = request.POST.get('shenfen_entity', '')#身份证框
	
	post8 = request.POST.get('shuzi_int', '')#数字框
	
	post9 = request.POST.get('xuanze_xiala', '')#下拉框
	
	post10 = request.POST.get('xuanze_xuanze', '')#选择框
	
	post11 = request.POST.get('shu_shudanxuan', '')#竖单选框
	
	post12 = request.POST.get('heng_hengdanxuan', '')#横单选框
	
	post13 = request.POST.get('kaiguan_bool', '')#启动开关
	
	post14 = request.POST.get('riqi_years', '')#日期框
	
	post15 = request.POST.get('datetime_datetime', '')#日期时间框
	
	post16 = request.POST.get('fuwenben_text', '')#富文本框
	

	post_arry =[post0,post1,post2,post3,post4,post5,post6,post7,post8,post9,post10,post11,post12,post13,post14,post15,post16,]
	form = dngadmin_formcommon.form_add(zd_list, post_arry)#表单数据验算二次处理

	if update:
		if post0:

			
			models.formdemo.objects.filter(id=post0).update(id=form[0])#ID
	
			models.formdemo.objects.filter(id=post0).update(demoid_id=form[1])#表单ID
	
			models.formdemo.objects.filter(id=post0).update(wenben_str=form[2])#文本框
	
			models.formdemo.objects.filter(id=post0).update(jinyong_stop=form[3])#禁用框
	
			models.formdemo.objects.filter(id=post0).update(mima_psd=form[4])#密码框
	
			models.formdemo.objects.filter(id=post0).update(shouji_phone=form[5])#手机框
	
			models.formdemo.objects.filter(id=post0).update(youjian_email=form[6])#邮件框
	
			models.formdemo.objects.filter(id=post0).update(shenfen_entity=form[7])#身份证框
	
			models.formdemo.objects.filter(id=post0).update(shuzi_int=form[8])#数字框
	
			models.formdemo.objects.filter(id=post0).update(xuanze_xiala=form[9])#下拉框
	
			models.formdemo.objects.filter(id=post0).update(xuanze_xuanze=form[10])#选择框
	
			models.formdemo.objects.filter(id=post0).update(shu_shudanxuan=form[11])#竖单选框
	
			models.formdemo.objects.filter(id=post0).update(heng_hengdanxuan=form[12])#横单选框
	
			models.formdemo.objects.filter(id=post0).update(kaiguan_bool=form[13])#启动开关
	
			models.formdemo.objects.filter(id=post0).update(riqi_years=form[14])#日期框
	
			models.formdemo.objects.filter(id=post0).update(datetime_datetime=form[15])#日期时间框
	
			models.formdemo.objects.filter(id=post0).update(fuwenben_text=form[16])#富文本框



			data = {
				'code': '0',
				'msg': '修改成功',
			}
			return HttpResponse(json.dumps(data))

		else:


			models.formdemo.objects.create(demoid_id=form[1], wenben_str=form[2], jinyong_stop=form[3], mima_psd=form[4], shouji_phone=form[5], youjian_email=form[6], shenfen_entity=form[7], shuzi_int=form[8], xuanze_xiala=form[9], xuanze_xuanze=form[10], shu_shudanxuan=form[11], heng_hengdanxuan=form[12], kaiguan_bool=form[13], riqi_years=form[14], datetime_datetime=form[15], fuwenben_text=form[16], )  #新增数据库

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



def formdemo_api_json(request):  #api查询

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

	dnguser =dngadmin_common.dng_dnguser(dnguser_uid)
	group = dngadmin_common.dng_usergroup(gid=dnguser.group_int)  # 获取会员组名称
	dngroute = models.dngroute.objects.filter(uid_int=dngroute_uid).first()  # 查询路径取回本页面菜单信息


	if not dngroute.url_str in mulu_url:  # 判断URL统一
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您的访问与菜单映射不匹配</h1></center><div>""")

	elif not '|' + str(dngroute_uid) + '|' in group.menu_text:  # 判断菜单权限
		return HttpResponse("""<BR><BR><BR><BR><BR><center><h1>您没有访问这个栏目的权限</h1></center><div>""")

	added = dngadmin_common.dng_zsgc(dngroute_uid, group.added_text)  # 增
	delete = dngadmin_common.dng_zsgc(dngroute_uid, group.delete_text)  # 删
	update = dngadmin_common.dng_zsgc(dngroute_uid, group.update_text)  # 改
	see = dngadmin_common.dng_zsgc(dngroute_uid, group.see_text)  # 开发者

	zd_list = dngadmin_common.dng_ziduan("formdemo")  # 获取对应表下所有字段值
	# ----------------------------------------------------------
	#   判断页面权限开始《《《 结束
	# ----------------------------------------------------------
	list_arry=models.formdemo.objects.filter().order_by ("-id")
	gongju = models.formdemo.objects.count()

	data = []
	for obj in list_arry:
		data.append(model_to_dict(obj))

	# 下面开始构造JSON格式
	datajson = """{"code":0,"msg":"成功","count":""" + str(gongju) + ""","data":""" + str(data) + """}"""

	datajson = datajson.replace('\'', '\"')  # 替换成AJAX可以解析得格式
	datajson = datajson.replace('True', '1')  # 替换成AJAX可以解析得格式
	datajson = datajson.replace('False', '0')  # 替换成AJAX可以解析得格式

	return HttpResponse(datajson)