#coding:utf-8
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.template import RequestContext
from backend import util
from User.models import User
from cmdb_auth.models import auth_group,user_auth_cmdb
import hashlib
import time

# Create your views here.

def login_valid(func):
    '''
    判断用户是否登录的装饰器:
    '''
    def inner(request,*args,**kwargs):
        try:
            username = request.session.get('username')     # 尝试获取session
            return func(request,*args,**kwargs)         # 如果获取到执行被装饰的函数
        except KeyError,e:
            if repr(e) == "KeyError('username',)":
            # repr是将类当中魔术方法__repr__的结果返回回来
                err = "当前用户未登录请登录"
            else:
                err = str(e)
            url = "/404/"+err
            return HttpResponseRedirect(url)
    return inner

# 判断用户权限的装饰器
def perm_valid(permission):
    def wrapper(func):
        def inner(request,*args,**kwargs):
            try:
                username = request.session.get('username')
                user_obj = User.objects.get(username=username)
                # 获取当前的权限角色
                auth_group_list = user_obj.auth_group_set.all()
                # 根据权限角色获取所有权限名称
                permission_list = []
                for authGroup in auth_group_list:
                    # 获取当前用户的权限管理表
                    obj = user_auth_cmdb.objects.get(group_name=authGroup)
                    # 获取权限管理的所有属性
                    permissionList = obj._meta.get_all_field_names()
                    for i in permissionList:
                        if i not in permission_list:
                            # 排除id 和 group_name属性
                            if i == 'id' or i == 'group_name':
                                continue
                            # 如果属性值为真添加到权限列表
                            if user_auth_cmdb.objects.values(i).filter(group_name=authGroup):
                                permission_list.append(i)
                        else:
                            continue
                if permission in permission_list:
                    return func(request,*args,**kwargs)
                else:
                    return HttpResponseRedirect('/401/')
            except Exception as e:
                return HttpResponseRedirect('/401/')
        return inner
    return wrapper

@login_valid
@perm_valid("select_host")
def index(request):
    try:
        username = request.session.get("username")
        image = User.objects.get(username=username).photo
    except:
        pass

    return render_to_response("index.html", locals())

def login(request):

    if request.method == "POST" and request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if user_exist(username):
            if user_valid(username,password):
                request.session['username'] = username

                util.write_log('user').info('username %s login' % username)
                return redirect('/', RequestContext(request))

    return render_to_response('login.html', locals(), RequestContext(request))

# 用户登录
def forbidden(request,error):
    return render_to_response("404.html",locals())

# 用户权限禁止页面
def prohibit(request):
    return render_to_response("401.html",locals())

def hashpassword(password):
    '''
    此功能采用hash md5 加密的方式对登录密码进行加密
    '''
    hash = hashlib.md5()
    hash.update(password)
    return hash.hexdigest()

def user_exist(username):
    '''
    此功能用于验证用户名是否存在
    '''
    try:
        User.objects.get(username=username)
        return True
    except:
        return False

# 用户名和密码校验
def user_valid(username,password):
    try:
        user = User.objects.get(username=username)
        if user.password == hashpassword(password):
            last_login = time.strftime('%Y-%m-%d %H:%M:%S')
            user.last_login = last_login
            user.save()
            return True
        else:
            return False
    except:
        return False

# 用户注册
def register(request):

    if request.method == "POST" and request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_retry = request.POST.get("password_retry")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        photo = request.FILES.get("photo")
        join_date = time.strftime('%Y-%m-%d %H:%M:%S')
        # 如果两次密码输入正确
        if password == password_retry:
            # 将注册数据存入数据库
            user = User(
                username=username,
                password=hashpassword(password),
                email=email,
                phone=phone,
                photo=photo,
                join_date=join_date,
                is_lock='N',
                delete_flag='N'
            )
            user.save()
            util.write_log('user').info('create username [%s] successful!'% username)
            return HttpResponseRedirect('/login/', RequestContext(request))
        else:
            return render_to_response('register.html', locals(), RequestContext(request))
    else:
        return render_to_response('register.html', locals(), RequestContext(request))

@csrf_exempt
def user_register_exist(request):
    '''Check the username of register was exist or not'''
    result = {}
    true = True
    false = False
    if request.method == "POST" and request.POST:
        username = request.POST.get("username")
        try:
            obj = User.objects.get(username=username)
        except:
            obj = None
        if obj:
            result["valid"] = false
        else:
            result["valid"] = true
        return JsonResponse(result)
    else:
        return JsonResponse({"error":"The request method must be post!"})

# 用户退出
def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return redirect('/login')

