#coding:utf-8
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from CMDB.views import login_valid
from monitor.models import ZabbixMonitor
from CMDB.settings import ZABBIX_URL
from Api import zabbix_api, zabbix_graph_api, salt_api
from User.models import User
from models import *
import json

# Create your views here.

@login_valid
def list(request):
    '''监控主机列表展示'''
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    try:
        host_id = request.GET.get("host_id")
        ava = request.GET.get("ava")
    except:
        host_id = ""
        ava = ""
    if host_id and ava:
        host_obj = Host.objects.get(id=host_id)
        if ava == "0":
            host_obj.available = 1
            host_obj.save()
        else:
            host_obj.available = 0
            host_obj.save()
    host = Host.objects.all()
    count = host.count()
    return render_to_response("monitor/list.html", locals())

@csrf_exempt
@login_valid
def draw(request):
    '''绘制监控图'''
    if request.method == "GET":
        username = request.session.get("username")
        image = User.objects.get(username=username).photo
        host_id = request.GET.get("host_id")
        global host_id
        host = Host.objects.get(id=host_id)
    if request.method == "POST" and request.POST:
        graph = request.POST.get("graph")
        if graph == "":
            return JsonResponse({"data":""})
        elif graph == "cpu_utilization":
            cpu_utilization_obj = CpuUtilization.objects.filter(host=host_id).order_by('-date')[0:30]
            data_list = []
            for num,cpu in enumerate(cpu_utilization_obj):
                cpu_dict = {}
                cpu_total_time = float(cpu.cpu_idle_time)+float(cpu.cpu_iowait_time)+float(cpu.cpu_user_time)+float(cpu.cpu_system_time)
                cpu_dict["cpu_iowait_time"] = round(float(cpu.cpu_iowait_time)/cpu_total_time*100,2)
                cpu_dict["cpu_system_time"] = round(float(cpu.cpu_system_time)/cpu_total_time*100,2)
                cpu_dict["cpu_idle_time"] = round(float(cpu.cpu_idle_time)/cpu_total_time*100,2)
                cpu_dict["cpu_user_time"] = round(float(cpu.cpu_user_time)/cpu_total_time*100,2)
                cpu_dict["year"] = cpu.date.strftime("%Y-%m-%d %H:%M:%S")
                data_list.append(cpu_dict)
            data_list.reverse()
            return JsonResponse({"result":data_list, "data":"cpu_utilization"})
        elif graph == "disk_space_usage":
            disk_usage_obj = DiskUsage.objects.filter(host=host_id).order_by('-date')[0]
            disk_dict = {}
            total_disk_space = float(disk_usage_obj.total_disk_space)
            free_disk_space = float(disk_usage_obj.free_disk_space)
            free_percent = round(free_disk_space/total_disk_space,2)
            used_percent = 1 - free_percent
            disk_dict["total_disk_space"] = round(total_disk_space/1024,2)
            disk_dict["free_disk_space"] = round(free_disk_space/1024,2)
            disk_dict["free_percent"] = free_percent
            disk_dict["used_percent"] = used_percent
            disk_dict["year"] = disk_usage_obj.date.strftime("%Y-%m-%d %H:%M:%S")
            return JsonResponse({"result":disk_dict, "data":"disk_space_usage"})
        elif graph == "memory_usage":
            memory_usage_obj = MemoryUsage.objects.filter(host=host_id).order_by('-date')[0:40]
            data_list = []
            for num,mem in enumerate(memory_usage_obj):
                mem_dict = {}
                mem_dict["available_memory"] = mem.available_memory
                mem_dict["year"] = mem.date.strftime("%Y-%m-%d %H:%M:%S")
                data_list.append(mem_dict)
            data_list.reverse()
            return JsonResponse({"result":data_list, "data":"memory_usage"})
        elif graph == "cpu_jumps":
            cpu_jumps_obj = CpuJumps.objects.filter(host=host_id).order_by('-date')[0:30]
            data_list = []
            for num, cpu_jumps in enumerate(cpu_jumps_obj):
                cpu_jumps_dict = {}
                cpu_jumps_dict["context_switchs_per_second"] = cpu_jumps.context_switchs_per_second
                cpu_jumps_dict["interrupts_per_second"] = cpu_jumps.interrupts_per_second
                cpu_jumps_dict["year"] = cpu_jumps.date.strftime("%Y-%m-%d %H:%M:%S")
                data_list.append(cpu_jumps_dict)
            data_list.reverse()
            return JsonResponse({"result": data_list, "data": "cpu_jumps"})

        else:
            return JsonResponse({"result":""})

    return render_to_response("monitor/draw.html", locals())

@csrf_exempt
def save(request):
    '''接收客户端采集的监控数据并存入数据库'''
    if request.method == "POST" and request.POST:
        ip = request.POST.get("IP").encode("utf-8")
        try:
            host = Host.objects.get(ip=ip)
        except Exception,e:
            print e
        else:
            disk_info = eval(request.POST.get("Disk").encode("utf-8"))
            cpu_info = eval(request.POST.get("CPU").encode("utf-8"))
            mem_info = eval(request.POST.get("Mem").encode("utf-8"))
            disk_obj = DiskUsage()
            disk_obj.host_id = host.id
            disk_obj.total_disk_space = disk_info["total"]
            disk_obj.free_disk_space = disk_info["free"]
            disk_obj.save()
            cpu_utilization = CpuUtilization()
            cpu_utilization.host_id = host.id
            cpu_utilization.cpu_idle_time = cpu_info["idle"]
            cpu_utilization.cpu_iowait_time = cpu_info["iowait"]
            cpu_utilization.cpu_system_time = cpu_info["system"]
            cpu_utilization.cpu_user_time = cpu_info["user"]
            cpu_utilization.save()
            cpu_jumps = CpuJumps()
            cpu_jumps.host_id = host.id
            cpu_jumps.context_switchs_per_second = cpu_info["context_switches"]
            cpu_jumps.interrupts_per_second = cpu_info["interrupts"]
            cpu_jumps.save()
            memory_usage = MemoryUsage()
            memory_usage.host_id = host.id
            memory_usage.available_memory = mem_info["mem"]["available"]
            memory_usage.total = mem_info["mem"]["total"]
            memory_usage.free = mem_info["mem"]["free"]
            memory_usage.percent = mem_info["mem"]["percent"]
            memory_usage.save()
    else:
        return JsonResponse({"error":"The request method must be post!"})
    return JsonResponse({"status":"success"})
