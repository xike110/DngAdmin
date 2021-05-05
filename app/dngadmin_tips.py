

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
def tips(request):#提示警告 分别有tishi  和 jinggao 两个GET参数
	yes     = request.GET.get('yes')  # GET参数
	jinggao = request.GET.get('jinggao')#GET参数
	tishi   = request.GET.get('tishi')#GET参数


	return render(request,"dngadmin/tips.html",{
			"title":"提示警告",
			"yes": yes,
			"jinggao":jinggao,
			"tishi":tishi,
		})
