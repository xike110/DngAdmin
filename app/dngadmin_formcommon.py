from django.shortcuts import render  # 视图渲染模块
from django.http import HttpResponse  # 请求模块
from . import models  # 数据库操作模块
from django.db.models import Q  # 数据库逻辑模块
from django.db.models import Avg, Max, Min, Sum  # 数据库聚合计算模块
from datetime import datetime, timedelta  # Cookie 模块
from django.http import HttpResponse, HttpResponseRedirect  # 重定向模块
from django.shortcuts import render
import os
import sys
import json
from urllib import parse  # 转码
import re  # 正则模块
import random  # 随机模块
import hashlib  # 加密模块
from django.utils import timezone  # 时间处理模块
from datetime import datetime
import datetime  # 时间
import time  # 日期模块
from django.forms.models import model_to_dict

# def dng_form(app_name,verbose_name,list_int,choices,default):  # 组件判断
def form_form(zd_list,db_values_list):  # 组件判断

    html_list = []
    form_id =""
    form_str=""

    if not db_values_list:
        for zd_ming, verbose_name, list_int, choices, default in zip(zd_list[0], zd_list[1], zd_list[2],
                                                                           zd_list[3], zd_list[4]):

            zd_ming = str(zd_ming)
            verbose_name = str(verbose_name)
            list_int = str(list_int)
            # choices = str(choices)
            default = str(default)

            # zd_ming[1] = str(zd_ming[1])
            # zd_ming[2] = str(zd_ming[2])
            # zd_ming[3] = str(zd_ming[3])
            # zd_ming[4] = str(zd_ming[4])

            if "id" == zd_ming:


                form_id = '''<input type="hidden" name="''' + zd_ming + '''" value="''' + default + '''"> '''
                html_list.append(form_id)  # 默认值写入列表

            if "_id" in zd_ming:

                form_id = '''<div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>
                                <div class="col-sm-8">
                                    <input type="hidden" name="''' + zd_ming + '''" value="''' + default + '''" maxlength="200">
                                    <p class="form-control-static">''' + default + '''</p>
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_id)  # 默认值写入列表


            elif "_str" in zd_ming:


                form_str = '''
                            <div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>

                                <div class="col-sm-8">
                                    <input type="text" name="''' + zd_ming + '''" placeholder="请输入" value="''' + default + '''" class="form-control" minlength="1"
                                           maxlength="200" required>
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>
                            '''
                html_list.append(form_str)  # 默认值写入列表

            elif "_stop" in zd_ming:

                form_stop = '''<div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>

                                <div class="col-sm-4">
                                    <input type="hidden" name="''' + zd_ming + '''" value="''' + default + '''">
                                    <input type="text" disabled="" placeholder="''' + default + '''" maxlength="200" class="form-control">
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>
                                        '''
                html_list.append(form_stop)  # 默认值写入列表

            elif "_psd" in zd_ming:

                form_psd = '''<div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>

                                <div class="col-sm-8">
                                    <input type="password" class="form-control" name="''' + zd_ming + '''" required minlength="6" placeholder="输入密码"
                                           maxlength="30" aria-required="true">
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_psd)  # 默认值写入列表

            elif "_phone" in zd_ming:

                form_phone = '''<div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>
                                <div class="col-sm-8">
                                    <input type="text" name="''' + zd_ming + '''"  value="''' + default + '''" class="form-control" data-mask="19999999999" required placeholder="输入手机号">

                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_phone)  # 默认值写入列表

            elif "_email" in zd_ming:

                form_email = '''<div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>

                                <div class="col-sm-8">
                                    <input type="email" name="''' + zd_ming + '''"  value="''' + default + '''" placeholder="输入邮箱" class="form-control" maxlength="200"
                                           required>
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_email)  # 默认值写入列表

            elif "_entity" in zd_ming:

                form_entity = '''<div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>
                                <div class="col-sm-8">
                                    <input type="text" name="''' + zd_ming + '''"  value="''' + default + '''" placeholder="输入18位身份证，如果身份证包含X，联系管理员协助" class="form-control" data-mask="999999999999999999">

                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_entity)  # 默认值写入列表

            elif "_int" in zd_ming:

                form_int = '''<div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>
                                <div class="col-sm-8">
                                    <input type="text" name="''' + zd_ming + '''" class="form-control"  value="''' + default + '''" placeholder="只能输入数字" required  maxlength="9" onkeyup="this.value=this.value.replace(/[^0-9]+/,'');" />

                                </div>
                            </div>

                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_int)  # 默认值写入列表


            elif "_xiala" in zd_ming:


                xxzz_xiala = []
                for yz in choices:
                    if str(yz[1]) == default:
                        xxx = "<option selected >" + str(yz[1]) + "</option>"
                        xxzz_xiala.append(xxx)
                    else:
                        zzz = "<option>" + str(yz[1]) + "</option>"
                        xxzz_xiala.append(zzz)
                arry_xiala = "".join(xxzz_xiala)

                form_xiala = '''<div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>

                                <div class="col-sm-4">
                                    <select class="form-control m-b" name="''' + zd_ming + '''">
                                      ''' + arry_xiala + '''
                                    </select>
                                    </select>

                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_xiala)  # 默认值写入列表
            elif "_xuanze" in zd_ming:

                xxzz_xuanze = []
                for yz in choices:
                    if str(yz[1]) == default:
                        xxx = "<option selected >" + str(yz[1]) + "</option>"
                        xxzz_xuanze.append(xxx)
                    else:
                        zzz = "<option>" + str(yz[1]) + "</option>"
                        xxzz_xuanze.append(zzz)
                arry_xuanze = "".join(xxzz_xuanze)

                form_xuanze = '''<div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>


                                <div class="col-sm-4">
                                    <select class="form-control" multiple="" name="''' + zd_ming + '''">
                                        ''' + arry_xuanze + '''
                                    </select>
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_xuanze)  # 默认值写入列表

            elif "_shudanxuan" in zd_ming:


                xxzz_shudanxuan = []
                for yz in choices:
                    if str(yz[1]) == default:
                        xxx = '''<div class="i-checks">
                                        <input type="radio" name="''' + zd_ming + '''" id="radio" value="''' + str(
                            yz[1]) + '''" checked>
                                        <label class="badge badge-primary">''' + str(yz[1]) + '''</label>
                                        </div>
                                    <p></p>'''
                        xxzz_shudanxuan.append(xxx)
                    else:
                        zzz = '''<div class="i-checks">
                                        <input type="radio" name="''' + zd_ming + '''" id="radio" value="''' + str(
                            yz[1]) + '''" >
                                        <label class="badge badge-primary">''' + str(yz[1]) + '''</label>
                                        </div>
                                    <p></p>'''
                        xxzz_shudanxuan.append(zzz)
                arry_shudanxuan = "".join(xxzz_shudanxuan)

                form_shudanxuan = '''<div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>
                                <div class="col-sm-6">
                                    ''' + arry_shudanxuan + '''
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_shudanxuan)  # 默认值写入列表

            elif "_hengdanxuan" in zd_ming:


                xxzz_hengdanxuan = []
                for yz in choices:
                    if str(yz[1]) == default:
                        xxx = '''<div class="checkbox-inline i-checks">
                                        <input type="radio" id="inlineRadio" value="''' + str(
                            yz[1]) + '''" name="''' + zd_ming + '''" checked="">
                                        <label class="badge badge-success" for="inlineRadio1">''' + str(yz[1]) + '''</label>
                                    </div>'''
                        xxzz_hengdanxuan.append(xxx)
                    else:
                        zzz = '''<div class="checkbox-inline i-checks">
                                        <input type="radio" id="inlineRadio" value="''' + str(
                            yz[1]) + '''" name="''' + zd_ming + '''" >
                                        <label class="badge badge-success" for="inlineRadio1">''' + str(yz[1]) + '''</label>
                                    </div>'''
                        xxzz_hengdanxuan.append(zzz)
                arry_hengdanxuan = "".join(xxzz_hengdanxuan)

                form_hengdanxuan = '''<div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>

                                <div class="col-sm-10">

                                 ''' + arry_hengdanxuan + '''
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_hengdanxuan)  # 默认值写入列表

            elif "_bool" in zd_ming:

                # if  default == True:
                #     checked = "checked"
                # elif default == False:
                #     checked = ""
                # else:
                #     checked = ""
                if default:
                    checked = "checked"
                else:
                    checked = ""
                form_bool = '''<div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>

                                <div class="col-sm-8">

                                    <div class="onoffswitch">
                                        <input type="checkbox" name="''' + zd_ming + '''" ''' + checked + ''' class="onoffswitch-checkbox"
                                               id="''' + zd_ming + '''">
                                        <label class="onoffswitch-label" for="''' + zd_ming + '''">
                                            <span class="onoffswitch-inner"></span>
                                            <span class="onoffswitch-switch"></span>
                                        </label>
                                    </div>


                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_bool)  # 默认值写入列表


            elif "_years" in zd_ming:


                form_years = ''' <div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>
                                <div class="col-sm-10">
                                    <input type="text" name="''' + zd_ming + '''" id="hello" class="laydate-icon form-control layer-date"  value="''' + default + '''"  data-mask="9999-99-99">
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_years)  # 默认值写入列表


            elif "_taim" in zd_ming:


                form_taim = '''<div class="form-group">
                              <label class="col-sm-2 control-label">''' + verbose_name + '''</label>
                                <div class="col-sm-10">
                                    <input type="text" name="''' + zd_ming + '''" id="hello" class="laydate-icon form-control layer-date"  value="''' + default + '''"  data-mask="99:99:99">
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''

                html_list.append(form_taim)  # 默认值写入列表

            elif "_datetime" in zd_ming:


                form_datetime = ''' <div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>
                                <div class="col-sm-10">
                                    <input type="text" name="''' + zd_ming + '''" class="form-control layer-date" placeholder="YYYY-MM-DD hh:mm:ss"  value="''' + default + '''" data-mask="9999-99-99 99:99:99" onclick="laydate({istime: true, format: 'YYYY-MM-DD hh:mm:ss'})">
                                    <label class="laydate-icon"></label>
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_datetime)  # 默认值写入列表
            elif "_text" in zd_ming:

                form_text = '''<div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>
                                <div class="col-sm-8">
                                    <textarea placeholder="请输入内容" name="''' + zd_ming + '''" maxlength="10000" class="form-control"
                                              style="margin: 0px -15.9844px 0px 0px; height: 150px; width: 100%;"
                                              required="" aria-required="true">''' + default + '''</textarea>
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_text)  # 默认值写入列表
        return (html_list)

    else:

        for zd_ming,verbose_name,list_int,choices,default,dict in zip(zd_list[0],zd_list[1],zd_list[2],zd_list[3],zd_list[4],db_values_list[0]):

            zd_ming = str(zd_ming)
            verbose_name = str(verbose_name)
            list_int = str(list_int)
            #choices = str(choices)
            default = str(default)


            # zd_ming[1] = str(zd_ming[1])
            # zd_ming[2] = str(zd_ming[2])
            # zd_ming[3] = str(zd_ming[3])
            # zd_ming[4] = str(zd_ming[4])

            if "id" == zd_ming:

                if dict:
                    default = str(dict)
                else:
                    default = default
                form_id = '''<input type="hidden" name="'''+zd_ming+'''" value="'''+default+'''"> '''
                html_list.append(form_id)  # 默认值写入列表


            if "_id" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default
                form_id = '''<div class="form-group">
                                <label class="col-sm-2 control-label">'''+verbose_name+'''</label>
                                <div class="col-sm-8">
                                    <input type="hidden" name="'''+zd_ming+'''" value="'''+default+'''" maxlength="200">
                                    <p class="form-control-static">'''+default+'''</p>
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_id)  # 默认值写入列表


            elif "_str" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default

                form_str = '''
                            <div class="form-group">
                                <label class="col-sm-2 control-label">'''+verbose_name+'''</label>
    
                                <div class="col-sm-8">
                                    <input type="text" name="'''+zd_ming+'''" placeholder="请输入" value="'''+default+'''" class="form-control" minlength="1"
                                           maxlength="200" required>
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>
                            '''
                html_list.append(form_str)  # 默认值写入列表

            elif "_stop" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default
                form_stop = '''<div class="form-group">
                                <label class="col-sm-2 control-label">'''+verbose_name+'''</label>
    
                                <div class="col-sm-4">
                                    <input type="hidden" name="'''+zd_ming+'''" value="'''+default+'''">
                                    <input type="text" disabled="" placeholder="'''+default+'''" maxlength="200" class="form-control">
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>
                                        '''
                html_list.append(form_stop)  # 默认值写入列表

            elif "_psd" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default
                form_psd = '''<div class="form-group">
                                <label class="col-sm-2 control-label">'''+verbose_name+'''</label>
    
                                <div class="col-sm-8">
                                    <input type="password" class="form-control" name="'''+zd_ming+'''" required minlength="6" placeholder="输入密码"
                                           maxlength="30" aria-required="true">
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_psd)  # 默认值写入列表

            elif "_phone" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default
                form_phone = '''<div class="form-group">
                                <label class="col-sm-2 control-label">'''+verbose_name+'''</label>
                                <div class="col-sm-8">
                                    <input type="text" name="'''+zd_ming+'''"  value="'''+default+'''" class="form-control" data-mask="19999999999" required placeholder="输入手机号">
    
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_phone)  # 默认值写入列表

            elif "_email" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default
                form_email = '''<div class="form-group">
                                <label class="col-sm-2 control-label">'''+verbose_name+'''</label>
    
                                <div class="col-sm-8">
                                    <input type="email" name="'''+zd_ming+'''"  value="'''+default+'''" placeholder="输入邮箱" class="form-control" maxlength="200"
                                           required>
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_email)  # 默认值写入列表

            elif "_entity" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default
                form_entity = '''<div class="form-group">
                                <label class="col-sm-2 control-label">'''+verbose_name+'''</label>
                                <div class="col-sm-8">
                                    <input type="text" name="'''+zd_ming+'''"  value="'''+default+'''" placeholder="输入18位身份证，如果身份证包含X，联系管理员协助" class="form-control" data-mask="999999999999999999">
    
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_entity)  # 默认值写入列表

            elif "_int" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default
                form_int = '''<div class="form-group">
                                <label class="col-sm-2 control-label">'''+verbose_name+'''</label>
                                <div class="col-sm-8">
                                    <input type="text" name="'''+zd_ming+'''" class="form-control"  value="'''+default+'''" placeholder="只能输入数字" required  maxlength="9" onkeyup="this.value=this.value.replace(/[^0-9]+/,'');" />
    
                                </div>
                            </div>
    
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_int)  # 默认值写入列表


            elif "_xiala" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default

                xxzz_xiala = []
                for yz in choices:
                    if str(yz[1]) ==default:
                        xxx="<option selected >"+str(yz[1]) +"</option>"
                        xxzz_xiala.append(xxx)
                    else:
                        zzz = "<option>" + str(yz[1])+ "</option>"
                        xxzz_xiala.append(zzz)
                arry_xiala = "".join(xxzz_xiala)

                form_xiala = '''<div class="form-group">
                                <label class="col-sm-2 control-label">'''+verbose_name+'''</label>
    
                                <div class="col-sm-4">
                                    <select class="form-control m-b" name="'''+zd_ming+'''">
                                      '''+arry_xiala+'''
                                    </select>
                                    </select>
    
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_xiala)  # 默认值写入列表
            elif "_xuanze" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default
                xxzz_xuanze = []
                for yz in choices:
                    if str(yz[1]) == default:
                        xxx = "<option selected >" + str(yz[1]) + "</option>"
                        xxzz_xuanze.append(xxx)
                    else:
                        zzz = "<option>" + str(yz[1]) + "</option>"
                        xxzz_xuanze.append(zzz)
                arry_xuanze = "".join(xxzz_xuanze)

                form_xuanze = '''<div class="form-group">
                                <label class="col-sm-2 control-label">'''+verbose_name+'''</label>
    
    
                                <div class="col-sm-4">
                                    <select class="form-control" multiple="" name="'''+zd_ming+'''">
                                        '''+arry_xuanze+'''
                                    </select>
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_xuanze)  # 默认值写入列表

            elif "_shudanxuan" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default

                xxzz_shudanxuan = []
                for yz in choices:
                    if str(yz[1]) == default:
                        xxx = '''<div class="i-checks">
                                        <input type="radio" name="'''+zd_ming+'''" id="radio" value="'''+ str(yz[1]) +'''" checked>
                                        <label class="badge badge-primary">'''+ str(yz[1]) +'''</label>
                                        </div>
                                    <p></p>'''
                        xxzz_shudanxuan.append(xxx)
                    else:
                        zzz = '''<div class="i-checks">
                                        <input type="radio" name="'''+zd_ming+'''" id="radio" value="'''+ str(yz[1]) +'''" >
                                        <label class="badge badge-primary">'''+ str(yz[1]) +'''</label>
                                        </div>
                                    <p></p>'''
                        xxzz_shudanxuan.append(zzz)
                arry_shudanxuan = "".join(xxzz_shudanxuan)

                form_shudanxuan = '''<div class="form-group">
                                <label class="col-sm-2 control-label">'''+verbose_name+'''</label>
                                <div class="col-sm-6">
                                    '''+arry_shudanxuan+'''
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_shudanxuan)  # 默认值写入列表

            elif "_hengdanxuan" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default

                xxzz_hengdanxuan = []
                for yz in choices:
                    if str(yz[1]) == default:
                        xxx = '''<div class="checkbox-inline i-checks">
                                        <input type="radio" id="inlineRadio" value="'''+ str(yz[1]) +'''" name="'''+zd_ming+'''" checked="">
                                        <label class="badge badge-success" for="inlineRadio1">'''+ str(yz[1]) +'''</label>
                                    </div>'''
                        xxzz_hengdanxuan.append(xxx)
                    else:
                        zzz = '''<div class="checkbox-inline i-checks">
                                        <input type="radio" id="inlineRadio" value="'''+ str(yz[1]) +'''" name="'''+zd_ming+'''" >
                                        <label class="badge badge-success" for="inlineRadio1">'''+ str(yz[1]) +'''</label>
                                    </div>'''
                        xxzz_hengdanxuan.append(zzz)
                arry_hengdanxuan = "".join(xxzz_hengdanxuan)

                form_hengdanxuan = '''<div class="form-group">
                                <label class="col-sm-2 control-label">'''+verbose_name+'''</label>
    
                                <div class="col-sm-10">
    
                                 '''+arry_hengdanxuan+'''
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_hengdanxuan)  # 默认值写入列表

            elif "_bool" in zd_ming:
                if str(dict)=="True":
                    checked = "checked"

                elif str(dict)=="False":
                    checked = ""
                else:
                    if str(default)=="False":
                        checked = ""
                    elif str(default) == "False":
                        checked = ""
                    else:
                        checked = "checked"
                form_bool = '''<div class="form-group">
                                <label class="col-sm-2 control-label">'''+verbose_name+'''</label>
    
                                <div class="col-sm-8">
    
                                    <div class="onoffswitch">
                                        <input type="checkbox" name="'''+zd_ming+'''" '''+checked+''' class="onoffswitch-checkbox"
                                               id="''' + zd_ming + '''">
                                        <label class="onoffswitch-label" for="''' + zd_ming + '''">
                                            <span class="onoffswitch-inner"></span>
                                            <span class="onoffswitch-switch"></span>
                                        </label>
                                    </div>
    
    
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_bool)  # 默认值写入列表


            elif "_years" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default

                form_years = ''' <div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>
                                <div class="col-sm-10">
                                    <input type="text" name="''' + zd_ming + '''" id="hello" class="laydate-icon form-control layer-date"  value="''' + default + '''"  data-mask="9999-99-99">
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_years)  # 默认值写入列表


            elif "_taim" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default

                form_taim = '''<div class="form-group">
                              <label class="col-sm-2 control-label">''' + verbose_name + '''</label>
                                <div class="col-sm-10">
                                    <input type="text" name="''' + zd_ming + '''" id="hello" class="laydate-icon form-control layer-date"  value="''' + default + '''"  data-mask="99:99:99">
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''

                html_list.append(form_taim)  # 默认值写入列表

            elif "_datetime" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default

                form_datetime = ''' <div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>
                                <div class="col-sm-10">
                                    <input type="text" name="''' + zd_ming + '''" class="form-control layer-date" placeholder="YYYY-MM-DD hh:mm:ss"  value="''' + default + '''" data-mask="9999-99-99 99:99:99" onclick="laydate({istime: true, format: 'YYYY-MM-DD hh:mm:ss'})">
                                    <label class="laydate-icon"></label>
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_datetime)  # 默认值写入列表
            elif "_text" in zd_ming:
                if dict:
                    default = str(dict)
                else:
                    default = default

                form_text = '''<div class="form-group">
                                <label class="col-sm-2 control-label">''' + verbose_name + '''</label>
                                <div class="col-sm-8">
                                    <textarea placeholder="请输入内容" name="''' + zd_ming + '''" maxlength="10000" class="form-control"
                                              style="margin: 0px -15.9844px 0px 0px; height: 150px; width: 100%;"
                                              required="" aria-required="true">'''+default+'''</textarea>
                                </div>
                            </div>
                            <div class="hr-line-dashed"></div>'''
                html_list.append(form_text)  # 默认值写入列表
        return (html_list)


def form_add(zd_list,post_arry):#表单数据验算二次处理
    # 处理开关
    # 处理密码+MD5
    # 处理时间转码
    add_list = []
    list=zip(post_arry,zd_list[0])
    for key in list:

        if "_bool" in key[1]: #处理开关

            if key[0]=="on":
                cday_bool = True

            else:
                cday_bool = False
            add_list.append(cday_bool)  # 默认值写入列表



        elif "_psd" in key[1]:#处理密码

            cday_psd =hashlib.md5(key[0].encode(encoding='UTF-8')).hexdigest()  # MD5加密
            add_list.append(cday_psd)  # 默认值写入列表




        elif "_years" in key[1]:# 处理日期
            if ":"in key[0]:
                cday_years =datetime.datetime.strptime(key[0], '%Y-%m-%d %H:%M:%S')
                add_list.append(cday_years)  # 默认值写入列表
            elif not ":"in key[0]:
                cday_years = datetime.datetime.strptime(key[0], '%Y-%m-%d')
                add_list.append(cday_years)  # 默认值写入列表

        # elif "_taim" in key[1]:# 处理时间
        #
        #     cday_time = datetime.datetime.strptime(key[0], '%H:%M:%S %H:%M:%S')
        #     add_list.append(cday_time)  # 默认值写入列表



        elif "_datetime" in key[1]:  # 处理日期时间

            cday_datetime = datetime.datetime.strptime(key[0], '%Y-%m-%d %H:%M:%S')
            add_list.append(cday_datetime)  # 默认值写入列表
        else:
            add_list.append(key[0])  # 默认值写入列表

    return (add_list)