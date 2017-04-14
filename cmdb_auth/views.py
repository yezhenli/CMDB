#coding:utf-8
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,JsonResponse
from cmdb_auth.forms import auth_add,auth_add_user,cmdb_form
from User.models import User
from cmdb_auth.models import auth_group,user_auth_cmdb

# Create your views here.

def auth_index(request):
    '''角色首页'''
    username = request.session.get("username")
    image = User.objects.get(username=username).photo

    data = auth_group.objects.all().order_by("-date_time")
    count = data.count()
    group_user_count = {}

    for i in data:
        data_id = auth_group.objects.get(id=i.id)
        group_user_count[i.id] = data_id.group_user.all().count()

    return render_to_response("auth/index.html", locals())

@csrf_exempt
def cmdb_add(request):
    username = request.session.get("username")
    image = User.objects.get(username=username).photo

    # 添加角色
    if request.method == 'POST' and request.POST:
        group_name = request.POST.get("group_name")
        explanation = request.POST.get("explanation")
        enable = request.POST.get("enable")
        authGroup = auth_group()
        authGroup.group_name = group_name
        authGroup.explanation = explanation
        authGroup.enable = enable
        authGroup.save()
        return HttpResponseRedirect("/auth/cmdb", locals())

    return render_to_response("auth/cmdb_add.html", locals())

@csrf_exempt
def add_auth(request,gid):
    '''权限管理'''
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    group_obj = auth_group.objects.get(id=gid)
    try:
        group_data = user_auth_cmdb.objects.get(group_name=gid)
        data = auth_add(instance=group_data)
    except:
        data = auth_add()
    if request.method == 'POST':
        try:
            uf = auth_add(request.POST,instance=group_data)
        except:
            uf = auth_add(request.POST)
        if uf.is_valid():
            uf.save()
            return HttpResponseRedirect('/auth/cmdb/', locals())

    return render_to_response('auth/add_auth.html', locals())

@csrf_exempt
def add_group_user(request,gid):
    '''成员权限管理'''
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    group_obj = auth_group.objects.get(id=gid)
    if request.method == 'POST' and request.POST:
        # 添加用户权限
        if "groups_selected" in request.POST:
            groups_selected_List = request.POST.get("groups_selected")
            for uid in groups_selected_List:
                try:
                    user_obj = User.objects.get(id=uid)
                    group_obj.group_user.add(user_obj)
                    group_obj.save()
                except Exception,e:
                    print e
        # 删除用户权限
        if "groups" in request.POST:
            groups_List = request.POST.get("groups")
            for u_id in groups_List:
                try:
                    userObj = User.objects.get(id=u_id)
                    group_obj.group_user.remove(userObj)
                    group_obj.save()
                except Exception,e:
                    print e
        return HttpResponseRedirect('/auth/cmdb/', locals())

    data = auth_add_user(instance=group_obj)
    # 所有用户列表
    userall = User.objects.all()
    # 已被选中的用户列表
    all_user = group_obj.group_user.all()

    return render_to_response("auth/group_user.html", locals())

@csrf_exempt
def edit_auth(request,gid):
    ''''''
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    group_obj = auth_group.objects.get(id=gid)
    if request.method == "POST" and request.POST:
        group_name = request.POST.get("group_name")
        explanation = request.POST.get("explanation")
        enable = request.POST.get("enable")
        authGroup = auth_group.objects.get(id=gid)
        authGroup.group_name = group_name
        authGroup.explanation = explanation
        authGroup.enable = enable
        authGroup.save()
        return HttpResponseRedirect("/auth/cmdb", locals())
    return render_to_response('auth/cmdb_edit.html', locals())

@csrf_exempt
def delete_auth(request):
    '''ajax实现角色删除'''
    if request.method == "POST" and request.POST:
        rid = request.POST.get("rid")
        group_obj = auth_group.objects.get(id=rid)
        group_obj.enable = 0
        group_obj.save()
        return JsonResponse({"status":"ok"})
    else:
        return JsonResponse({"status":"The request method must be post!"})