#coding:utf-8
from django.shortcuts import render,render_to_response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from backend import util
from CMDB.views import login_valid
from User.models import User
# Create your views here.

@login_valid
def userList(request):

    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    user_name = "用户列表"
    user_list = User.objects.all()
    count = user_list.count()
    return render_to_response("user/user_list.html",locals())

@csrf_exempt
def userDelete(request):

    if request.method == "POST" and request.POST:
        user_id = request.POST.get("user_id")
        user_obj = User.objects.get(id=user_id)
        username = user_obj.username
        user_obj.delete_flag = 'Y'
        user_obj.save()
        util.write_log('user').info('set the delete_flag of username [%s] to "Y" ')
        return JsonResponse({"status":"success"})
    else:
        return render_to_response('user/user_list.html')

def permissionList(request):
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    return render_to_response('user/permission_list.html', locals())

def profile(request):
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    return render_to_response("user/profile.html", locals())