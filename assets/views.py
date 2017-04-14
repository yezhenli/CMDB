#coding:utf-8
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response,render
from django.http import JsonResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from CMDB.views import login_valid
from User.models import User
from assets.models import *
import common
import html_helper
import datetime

# Create your views here.

def cabinet(request):
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    idc_list = IDC.objects.all()

    idc_type = request.GET.get("idc")
    if idc_type:
        cabinet_list = Cabinet.objects.filter(idc_id=idc_type)
    else:
        cabinet_list = Cabinet.objects.all()
    count = cabinet_list.count()

    return render_to_response("assets/cabinet.html", locals())

@login_valid
@csrf_exempt
def cabinet_add(request):
    '''机柜添加'''
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    idc_list = IDC.objects.all()
    if request.method == "POST" and request.POST:
        idc = request.POST.get("idc")
        name = request.POST.get("name")
        cabinet = Cabinet()
        cabinet.idc_id = idc
        cabinet.name = name
        cabinet.save()
        return HttpResponseRedirect("/assets/cabinet/", locals())
    else:
        return render_to_response("assets/cabinet_add.html", locals())

@login_valid
@csrf_exempt
def cabinet_change(request):
    '''修改机柜'''
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    idc_list = IDC.objects.all()
    if request.method == "GET" and request.GET:
        cabinet_id = request.GET.get("cabinet_id")
        global cabinet_id
        cabinet_obj = Cabinet.objects.get(id=cabinet_id)

    # 机架列表和个数
    rack_list = Rack.objects.filter(cabinet=cabinet_id)
    count = rack_list.count()

    # 修改并提交机柜或机架请求
    if request.method == "POST" and request.POST:
        # 如果POST请求中有“name”字段，表示的是机柜提交
        if request.POST.has_key("name"):
            idc = request.POST.get("idc")
            name = request.POST.get("name")
            cabinet = Cabinet.objects.get(id=cabinet_id)
            cabinet.idc_id = idc
            cabinet.name = name
            cabinet.save()
            return HttpResponseRedirect("/assets/cabinet/", locals())
        # 否则表示的是机架提交
        else:
            for i in xrange(1, 100):
                new_rack_name = request.POST.get("new_rack_name_"+str(i))
                if new_rack_name:
                    rack = Rack()
                    rack.cabinet_id = cabinet_id
                    rack.name = new_rack_name
                    rack.save()
                else:
                    break
            return HttpResponseRedirect("/assets/cabinet/", locals())

    else:
        return render_to_response("assets/cabinet_change.html", locals())

@login_valid
def asset_list(request,page):

    try:
        username = request.session.get("username")
        image = User.objects.get(username=username).photo
    except:
        pass
    per_item = common.try_int(request.COOKIES.get('page_num', 10), 10)
    page = common.try_int(page, 1)
    # 根据类型和状态进行数据过滤
    type = request.GET.get("type")
    status = request.GET.get("status")
    if type:
        asset_filter = Asset.objects.filter(asset_type=type)
    elif status:
        asset_filter = Asset.objects.filter(status=status)
    else:
        asset_filter = Asset.objects.all()
    count = asset_filter.count()
    page_obj = html_helper.PageInfo(page,count,per_item)
    # 每页显示的条目

    result = asset_filter.order_by('-id')[page_obj.start:page_obj.end]
    # 根据当前页和总页数获取html分页
    page_string = html_helper.Pager(page,page_obj.all_page_count)
    all_page_count = page_obj.all_page_count
    data = result

    response = render_to_response('assets/assets.html', locals())
    response.set_cookie('page_num',per_item)
    return response

@login_valid
@csrf_exempt
def asset_add(request):
    '''添加资产'''
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    manufactory_list = Manufactory.objects.all()
    contract_list = Contract.objects.all()
    business_unit_list = BusinessUnit.objects.all()
    username_list = User.objects.all()
    idc_list = IDC.objects.all()

    if request.method == "POST" and request.POST:
        type = request.POST.get("type")
        SN = request.POST.get("sn")
        type = request.POST.get("type")
        manufactory_id = request.POST.get("manufactory")
        management_ip = request.POST.get("management_ip")
        contract_id = request.POST.get("contract")
        trade_date = request.POST.get("trade_date")
        expire_date = request.POST.get("expire_date")
        price = request.POST.get("price")
        business_unit_id = request.POST.get("business_unit")
        admin_id = request.POST.get("admin")
        idc_id = request.POST.get("idc")
        status = request.POST.get("status")
        memo = request.POST.get("memo")
        asset = Asset()
        asset.asset_type = type
        asset.sn = SN
        asset.manufactory_id = manufactory_id
        asset.management_ip  = management_ip
        asset.contract_id = contract_id
        asset.trade_date = trade_date
        asset.expire_date = expire_date
        asset.price = price
        asset.business_unit_id = business_unit_id
        asset.admin_id = admin_id
        asset.idc_id = idc_id
        asset.status = status
        asset.memo = memo
        asset.save()
        return HttpResponseRedirect("/assets/asset_list/", locals())
    else:
        return render_to_response("assets/asset_add.html", locals())

@login_valid
def server_list(request):
    username = request.session.get("username")
    image = User.objects.get(username=username).photo

    server_list = Server.objects.all()
    return render_to_response("assets/server.html", locals())

@login_valid
def rack(request):
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    cabinet_list = Cabinet.objects.all()
    type = request.GET.get("type")
    if type:
        rack_list = Rack.objects.filter(cabinet=type)
    else:
        rack_list = Rack.objects.all()
    count = rack_list.count()

    return render_to_response("assets/rack.html",locals())

@login_valid
@csrf_exempt
def rack_add(request):
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    cabinet_list = Cabinet.objects.all()
    if request.method == "POST" and request.POST:
        cabinet_id = request.POST.get("cabinet")
        name = request.POST.get("name")
        rack = Rack()
        rack.cabinet_id = cabinet_id
        rack.name = name
        rack.save()
        return HttpResponseRedirect("/assets/rack/", locals())
    else:
        return render_to_response("assets/rack_add.html", locals())

@login_valid
def idc(request):
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    idc_level_list = IDCLevel.objects.all()
    idc_level = request.GET.get("idc_level")
    print idc_level
    if idc_level:
        idc_list = IDC.objects.filter(type=idc_level)
    else:
        idc_list = IDC.objects.all()
    count = idc_list.count()
    return render_to_response('assets/idc.html',locals())

@login_valid
@csrf_exempt
def idc_add(request):
    '''增加机房'''
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    isp_list = ISP.objects.all()
    type_list = IDCLevel.objects.all()
    if request.method == "POST" and request.POST:
        name = request.POST.get("name")
        bandwidth = request.POST.get("bandwidth")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        operator = request.POST.get("operator")
        type = request.POST.get("type")
        contact = request.POST.get("contact")
        memo = request.POST.get("memo")
        idc = IDC()
        idc.name = name
        idc.bandwidth = bandwidth
        idc.address = address
        idc.phone = phone
        idc.operator_id = operator
        idc.type_id = type
        idc.contacts = contact
        idc.memo = memo
        idc.save()
        return HttpResponseRedirect("/assets/idc/", locals())
    else:
        return render_to_response("assets/idc_add.html", locals())

@login_valid
@csrf_exempt
def idc_change(request,idc_id):
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    idc_obj = IDC.objects.get(id=idc_id)
    isp_list = ISP.objects.all()
    type_list = IDCLevel.objects.all()
    if request.method == "POST" and request.POST:
        name = request.POST.get("name")
        bandwidth = request.POST.get("bandwidth")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        operator = request.POST.get("operator")
        type = request.POST.get("type")
        contact = request.POST.get("contact")
        memo = request.POST.get("memo")
        idc = IDC.objects.get(id=idc_id)
        idc.name = name
        idc.bandwidth = bandwidth
        idc.address = address
        idc.phone = phone
        idc.operator_id = operator
        idc.type_id = type
        idc.contacts = contact
        idc.memo = memo
        idc.save()
        return HttpResponseRedirect("/assets/idc/", locals())
    else:
        return render_to_response("assets/idc_change.html", locals())

@login_valid
def content(request,ids):

    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    if request.method == "GET":
        try:
            asset_obj = Asset.objects.get(id=ids)
        except ObjectDoesNotExist as e:
            return render(request, 'assets/assets_content.html', {'error': e})
        return render(request, 'assets/assets_content.html', locals())

@csrf_exempt
def entries(request):
    '''当改变页面显示的条目时，触发ajax'''
    result = {"status":"","page_num":""}
    if request.method == "POST" and request.POST:
        entries = request.POST.get("entries")
        result["page_num"] = entries
        result["status"] = "success"
        response = JsonResponse(result)
        response.set_cookie('page_num',entries)
        return response
    else:
        pass


@csrf_exempt
def type_change(request):
    '''处理资产类型改变 ajax请求'''
    if request.method == "POST" and request.POST:
        try:
            type = request.POST.get("type")
            result = Asset.objects.filter(asset_type=type)
        except:
            pass
        return render('assets/assets.html', locals())
    else:
        return JsonResponse({"error":"request method must be post"})