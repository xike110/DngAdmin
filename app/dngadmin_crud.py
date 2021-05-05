

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



def crud(request):
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

	#zd_list = dngadmin_common.dng_ziduan("crud") #获取对应表下所有字段值

	#biaodan = dngadmin_common.dng_dnguser(uid=dnguser_uid)


	return render(request,"dngadmin/crud.html",{
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


		"yuming_url": yuming_url,








	})


def crud_post(request):
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

	#zd_list = dngadmin_common.dng_ziduan("crud")  # 获取对应表下所有字段值
	biaodan = dngadmin_common.dng_dnguser(uid=dnguser_uid)

	post0 = request.POST.get('list_common', '')
	post1 = request.POST.get('list_py', '')
	post2 = request.POST.get('list_html', '')
	post3 = request.POST.get('post_py', '')
	post4 = request.POST.get('post_html', '')
	post5 = request.POST.get('list_url', '')
	post5_zhushi = request.POST.get('list_url_zhushi', '')
	post6 = request.POST.get('post_url', '')
	post6_zhushi = request.POST.get('post_url_zhushi', '')

	if update:
		if post0:
			root = os.getcwd()  # 获取项目运行根目录
			root_py = os.path.abspath('app/dngadmin_common.py')  # 跟目录+py文件所在路径

			seo = open(root_py, "rb")  # 读取
			key = str(seo.read(), 'utf-8')  # read是读取命令 str 转换字符串和编码

			strinfo = re.compile('# ⊙1数据库模型替换1⊙')  # 正则替换前
			tihuan_post0 = '''if name == "'''+post0+'''":
        dbziduan = models.'''+post0+'''._meta.fields
    # ⊙1数据库模型替换1⊙'''
			keyseo = strinfo.sub(tihuan_post0, key)  # 正则替换后

			strinfo = re.compile('# ⊙2数据库模型替换2⊙')  # 正则替换前
			tihuan_post0 = '''if name == "''' + post0 + '''":
            params = models.''' + post0 + '''._meta.get_field(key).verbose_name
        # ⊙2数据库模型替换2⊙'''
			keyseo = strinfo.sub(tihuan_post0, keyseo)  # 正则替换后

			root_py2 = os.path.abspath('app/dngadmin_common.py')  # 跟目录+py文件所在路径
			kaobei2 = open(root_py2, "w")  # 写入
			kaobei2.write(keyseo)  # write是写入命令
			kaobei2.close()  # close()是关闭命令



			urlstr = parse.quote('参数' + post0 + '写入dngadmin_common.py成功')
			response = HttpResponseRedirect('/dngadmin/crud/?yes=' + urlstr)
			return response

		if post1:

			####构造字段数组###


			ida = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
				   28, 29, 30]
			db_list = dngadmin_common.dng_ziduan(post1)  # 获取对应表下所有字段值


			####开始构造⊙⊙⊙JSON函数-查⊙⊙⊙文本代码###


			json_list = zip(db_list[0], db_list[1], ida)  # [0]=例子：uid_int（字段值）  [1]=例子：会员id（字段备注） [2]=例子（数字列）
			json = []
			for json_arr in json_list:  # 遍历字符串，遍历输出

				json.append('''
			"''' + str(json_arr[0]) + '''" : str(key.''' + str(json_arr[0]) + '''), # ''' + str(json_arr[1]) + '''
			''')  # 循环写入空数组

			json = ''.join(json)
			json = json.replace('_time),', '_time.strftime("%Y-%m-%d %H:%M:%S")),')
			####开始构造⊙⊙⊙added函数-增⊙⊙⊙文本代码###


			added_list = zip(db_list[0], db_list[1], ida)  # [0]=例子：uid_int（字段值）  [1]=例子：会员id（字段备注） [2]=例子（数字列）
			added_a = []
			added_b = []
			for added_arr in added_list:  # 遍历字符串，遍历输出

				if str(added_arr[0]) =="id":
					continue  # 跳过本次循环

				added_a.append('''
	post'''+str(added_arr[2])+''' = request.POST.get(zd_list[0]['''+str(added_arr[2])+'''], '') #''' + str(added_arr[1]) + '''
	''')# 循环写入空数组

				added_b.append(str(added_arr[0]) +"=post"+str(added_arr[2])+", ")  # 循环写入空数组

			added_a = ''.join(added_a)
			added_b = ''.join(added_b)
			added_b =  "ok = models.映射的路径名替换.objects.create("+added_b+")  # 更新修改数据库"

			####开始构造⊙⊙⊙update函数-改⊙⊙⊙文本代码###


			update_list = zip(db_list[0], db_list[1], ida)  # [0]=例子：uid_int（字段值）  [1]=例子：会员id（字段备注） [2]=例子（数字列）
			update_a = []
			update_b = []
			for update_arr in update_list:  # 遍历字符串，遍历输出

				if str(update_arr[0]) == "id":
					continue  # 跳过本次循环

				update_a.append('''
	post''' + str(update_arr[2]) + ''' = request.POST.get(zd_list[0][''' + str(update_arr[2]) + '''], '') #''' + str(update_arr[1]) + '''
	''')  # 循环写入空数组

				update_b.append('''
		if post''' + str(update_arr[2]) + ''':
			models.映射的路径名替换.objects.filter(id=post0).update(''' + str(update_arr[0]) + '''=post''' + str(update_arr[2]) + ''')	
			''')  # 循环写入空数组

			update_a = ''.join(update_a)
			update_b = ''.join(update_b)


			####开始构造⊙⊙⊙search函数-搜⊙⊙⊙文本代码###
			search_list = zip(db_list[0], db_list[1], ida)  # [0]=例子：uid_int（字段值）  [1]=例子：会员id（字段备注） [2]=例子（数字列）
			search_a = []
			search_b = []
			search_c = []
			for search_arr in search_list:  # 遍历字符串，遍历输出

				if str(search_arr[0]) == "id":
					continue  # 跳过本次循环

				search_a.append('''
	post''' + str(search_arr[2]) + ''' = request.POST.get(zd_list[0][''' + str(search_arr[2]) + '''], '') #''' + str(search_arr[1]) + '''
	''')  # 循环写入空数组
				if str(search_arr[2]) == "1":
					if_bq="if"
				else:
					if_bq = "elif"
				search_b.append('''
	''' + if_bq + ''' post''' + str(search_arr[2]) + ''': 
		dngred = models.映射的路径名替换.objects.filter(''' + search_arr[0] + '''__contains=post''' + str(search_arr[2]) + ''').order_by('-id') #''' + str(search_arr[1]) + '''
	''')  # 循环写入空数组
				search_c.append('''
					 "''' + search_arr[0] + '''": str(key.''' + search_arr[0] + '''),  # ''' + search_arr[1])  # 循环写入空数组

			search_a = ''.join(search_a)
			search_b = ''.join(search_b)
			search_c = ''.join(search_c)
			####替换代码开始###


			root_py = os.path.abspath('app/dngadmin_demo_list.py')  # 跟目录+py文件所在路径

			seo = open(root_py, "rb")  # 读取
			key = str(seo.read(), 'utf-8')  # read是读取命令 str 转换字符串和编码

			###josn查看替换
			strinfo = re.compile('# ⊙json查看替换⊙ #')  # 正则替换前
			keyseo1 = strinfo.sub(json, key)  # 正则替换后
			###added新增替换
			strinfo = re.compile('# 1⊙added新增替换⊙1 #')  # 正则替换前
			keyseo2 = strinfo.sub(added_a, keyseo1)  # 正则替换后

			strinfo = re.compile('# 2⊙added新增替换⊙2 #')  # 正则替换前
			keyseo3 = strinfo.sub(added_b, keyseo2)  # 正则替换后
			###update更改替换
			strinfo = re.compile('# 1⊙update更改替换⊙1 #')  # 正则替换前
			keyseo4 = strinfo.sub(update_a, keyseo3)  # 正则替换后

			strinfo = re.compile('# 2⊙update更改替换⊙2 #')  # 正则替换前
			keyseo5 = strinfo.sub(update_b, keyseo4)  # 正则替换后
			###search搜索替换
			strinfo = re.compile('# 1⊙search搜索替换⊙1 #')  # 正则替换前
			keyseo6 = strinfo.sub(search_a, keyseo5)  # 正则替换后

			strinfo = re.compile('# 2⊙search搜索替换⊙2 #')  # 正则替换前
			keyseo7 = strinfo.sub(search_b, keyseo6)  # 正则替换后

			strinfo = re.compile('# 3⊙search搜索替换⊙3 #')  # 正则替换前
			keyseo8= strinfo.sub(search_c, keyseo7)  # 正则替换后
			###模型替换
			strinfo = re.compile('映射的路径名替换')  # 正则替换前
			keyseo9 = strinfo.sub(post1, keyseo8)  # 正则替换后

			root_py2 = os.path.abspath('app/dngadmin_' + post1 + '.py')  # 跟目录+py文件所在路径
			kaobei2 = open(root_py2, "w")  # 写入
			kaobei2.write(keyseo9)  # write是写入命令
			kaobei2.close()  # close()是关闭命令

			#return HttpResponse(search_c)
			urlstr = parse.quote('列表PY' + post1 + '构造成功')
			response = HttpResponseRedirect('/dngadmin/crud/?yes=' + urlstr)
			return response

		if post2:
			####构造字段数组###

			
			ida = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
				   28, 29, 30]
			db_list = dngadmin_common.dng_ziduan(post2)  # 获取对应表下所有字段值

			html_list = zip(db_list[0], db_list[1], ida)  # [0]=例子：uid_int（字段值）  [1]=例子：会员id（字段备注） [2]=例子（数字列）
			####开始构造⊙⊙⊙JSON函数-查⊙⊙⊙文本代码###
			list_html_a = []
			list_html_b = []
			list_html_c = []
			list_html_d = []
			for html_arr in html_list:  # 遍历字符串，遍历输出

				if str(html_arr[0]) == "id":
					continue  # 跳过本次循环

				list_html_a.append('''{% if zd_list.0.''' + str(html_arr[2]) + ''' %}

            <div class="layui-form-item">
                    <label class="layui-form-label">{{zd_list.1.''' + str(html_arr[2]) + '''}}</label>
                <div class="layui-input-block">
                    <input type="text" name="{{zd_list.0.''' + str(html_arr[2]) + '''}}" id="{{zd_list.0.''' + str(html_arr[2]) + '''}}"  required  lay-verify="required" autocomplete="off" placeholder="请输入{{zd_list.1.''' + str(html_arr[2]) + '''}}" class="layui-input">
                </div>
            </div>
            {% endif %}
            ''')
				if str(html_arr[2]) == "0":
					if_bq= "value=\"{{dnguser_uid}}\""
				else:
					if_bq = ""
				list_html_b.append('''{% if zd_list.0.''' + str(html_arr[2]) + ''' %}

            <div class="layui-form-item">
                                <label class="layui-form-label">{{zd_list.1.''' + str(html_arr[2]) + '''}}</label>
                            <div class="layui-input-block">
                                <input type="text" name="{{zd_list.0.''' + str(html_arr[2]) + '''}}" id="{{zd_list.0.''' + str(html_arr[2]) + '''}}"  ''' +if_bq + '''  required  lay-verify="required"  autocomplete="off" placeholder="请输入{{zd_list.1.''' + str(html_arr[2]) + '''}}" class="layui-input">
                            </div>
                        </div>
            {% endif %}
            ''')



			list_html_a = ''.join(list_html_a)

			list_html_b = ''.join(list_html_b)




			root_py = os.path.abspath('app/Templates/dngadmin/demo_list.html')  # 跟目录+py文件所在路径

			seo = open(root_py, "rb")  # 读取
			key = str(seo.read(), 'utf-8')  # read是读取命令 str 转换字符串和编码

			strinfo = re.compile('<!-- 1⊙HTML模板替换⊙1 -->')  # 正则替换前
			keyseo1 = strinfo.sub(list_html_a, key)  # 正则替换后


			strinfo = re.compile('<!-- 2⊙HTML模板替换⊙2 -->')  # 正则替换前
			keyseo2 = strinfo.sub(list_html_b, keyseo1)  # 正则替换后


			root_py2 = os.path.abspath('app/Templates/dngadmin/' + post2 + '.html')  # 跟目录+py文件所在路径
			kaobei2 = open(root_py2, "w")  # 写入
			kaobei2.write(keyseo2)  # write是写入命令
			kaobei2.close()  # close()是关闭命令

			urlstr = parse.quote('列表模板' + post2 + '构造成功')
			response = HttpResponseRedirect('/dngadmin/crud/?yes=' + urlstr)
			return response


		if post3:


			root = os.getcwd()  # 获取项目运行根目录
			root_py = os.path.abspath('app/dngadmin_demo_post.py')  # 跟目录+py文件所在路径

			seo = open(root_py, "rb")  # 读取
			key = str(seo.read(), 'utf-8')  # read是读取命令 str 转换字符串和编码

			strinfo = re.compile('映射的路径名替换')  # 正则替换前
			keyseo = strinfo.sub(post3, key)  # 正则替换后

			root_py2 = os.path.abspath('app/dngadmin_' + post3 + '.py')  # 跟目录+py文件所在路径
			kaobei2 = open(root_py2, "w")  # 写入
			kaobei2.write(keyseo)  # write是写入命令
			kaobei2.close()  # close()是关闭命令


			urlstr = parse.quote('表单Py文件' + post3 + '构造成功')
			response = HttpResponseRedirect('/dngadmin/crud/?yes=' + urlstr)
			return response

		if post4:
			root = os.getcwd()  # 获取项目运行根目录
			root_py = os.path.abspath('app/Templates/dngadmin/demo_post.html')  # 跟目录+py文件所在路径

			seo = open(root_py, "rb")  # 读取
			key = str(seo.read(), 'utf-8')  # read是读取命令 str 转换字符串和编码

			strinfo = re.compile('映射的路径名替换')  # 正则替换前
			keyseo = strinfo.sub(post4, key)  # 正则替换后

			root_py2 = os.path.abspath('app/Templates/dngadmin/'+post4+'.html')  # 跟目录+py文件所在路径
			kaobei2 = open(root_py2, "w")  # 写入
			kaobei2.write(keyseo)  # write是写入命令
			kaobei2.close()  # close()是关闭命令


			urlstr = parse.quote('模板' + post4 + '构造成功')
			response = HttpResponseRedirect('/dngadmin/crud/?yes=' + urlstr)
			return response
		if post5 and post5_zhushi:

			root = os.getcwd()  # 获取项目运行根目录
			root_py = os.path.abspath('app/dngadmin_urls.py')  # 跟目录+py文件所在路径

			seo = open(root_py, "rb")  # 读取
			key = str(seo.read(), 'utf-8')  # read是读取命令 str 转换字符串和编码

			strinfo = re.compile('# ⊙1映射替换1⊙')  # 正则替换前
			tihuan_post5 = '''from . import dngadmin_''' + post5 + '''   #''' + post5_zhushi + '''
# ⊙1映射替换1⊙'''
			keyseo = strinfo.sub(tihuan_post5, key)  # 正则替换后

			strinfo = re.compile('# ⊙2映射替换2⊙')  # 正则替换前
			tihuan_post5 = '''url(r'^''' + post5 + '''/', dngadmin_''' + post5 + '''.''' + post5 + '''),  # ''' + post5_zhushi + '''
	url(r'^''' + post5 + '''_json/', dngadmin_''' + post5 + '''.''' + post5 + '''_json),  # ''' + post5_zhushi + '''json
	url(r'^''' + post5 + '''_added/', dngadmin_''' + post5 + '''.''' + post5 + '''_added),  # ''' + post5_zhushi + '''新增
	url(r'^''' + post5 + '''_delete/', dngadmin_''' + post5 + '''.''' + post5 + '''_delete),  # ''' + post5_zhushi + '''删除
	url(r'^''' + post5 + '''_update/', dngadmin_''' + post5 + '''.''' + post5 + '''_update),  # ''' + post5_zhushi + '''更新修改
	url(r'^''' + post5 + '''_search/', dngadmin_''' + post5 + '''.''' + post5 + '''_search),  # ''' + post5_zhushi + '''搜索
	# ⊙2映射替换2⊙'''
			keyseo = strinfo.sub(tihuan_post5, keyseo)  # 正则替换后

			root_py2 = os.path.abspath('app/dngadmin_urls.py')  # 跟目录+py文件所在路径
			kaobei2 = open(root_py2, "w")  # 写入
			kaobei2.write(keyseo)  # write是写入命令
			kaobei2.close()  # close()是关闭命令

			urlstr = parse.quote('参数' + post5 + '表单映射写入成功')
			response = HttpResponseRedirect('/dngadmin/crud/?yes=' + urlstr)
			return response



			urlstr = parse.quote('参数' + post5 + '列表映射写入成功')
			response = HttpResponseRedirect('/dngadmin/crud/?yes=' + urlstr)
			return response

		if post6 and post6_zhushi:

			root = os.getcwd()  # 获取项目运行根目录
			root_py = os.path.abspath('app/dngadmin_urls.py')  # 跟目录+py文件所在路径

			seo = open(root_py, "rb")  # 读取
			key = str(seo.read(), 'utf-8')  # read是读取命令 str 转换字符串和编码

			strinfo = re.compile('# ⊙1映射替换1⊙')  # 正则替换前
			tihuan_post6 = '''from . import dngadmin_''' + post6 + '''   #''' + post6_zhushi + '''
# ⊙1映射替换1⊙'''
			keyseo = strinfo.sub(tihuan_post6, key)  # 正则替换后

			strinfo = re.compile('# ⊙2映射替换2⊙')  # 正则替换前
			tihuan_post6 = '''url(r'^''' + post6 + '''/', dngadmin_''' + post6 + '''.''' + post6 + '''),  # ''' + post6_zhushi + '''
	url(r'^''' + post6 + '''_post/', dngadmin_''' + post6 + '''.''' + post6 + '''_post),  # ''' + post6_zhushi + '''的post
	# ⊙2映射替换2⊙'''
			keyseo = strinfo.sub(tihuan_post6, keyseo)  # 正则替换后

			root_py2 = os.path.abspath('app/dngadmin_urls.py')  # 跟目录+py文件所在路径
			kaobei2 = open(root_py2, "w")  # 写入
			kaobei2.write(keyseo)  # write是写入命令
			kaobei2.close()  # close()是关闭命令

			urlstr = parse.quote('参数' + post6 + '表单映射写入成功')
			response = HttpResponseRedirect('/dngadmin/crud/?yes=' + urlstr)
			return response

	else:
		urlstr = parse.quote('您没有修改权限')
		response = HttpResponseRedirect('/dngadmin/crud/?jinggao=' + urlstr)
		return response



