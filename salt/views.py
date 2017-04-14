#coding:utf-8
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from CMDB.views import login_valid
from CMDB.settings import FILE_FORMAT
from User.models import User
from salt.models import SaltServer,Minions,Module,Command,Result
from Api.salt_api import SaltApi
import json
import re
import os

# Create your views here.

@login_valid
@csrf_exempt
def execute(request, server_id):
    '''执行命令'''
    username = request.session.get("username")
    image = User.objects.get(username=username).photo

    server_list = SaltServer.objects.all()
    try:
        salt_server = SaltServer.objects.get(id=server_id)
    except:
        salt_server = SaltServer.objects.all()[0]
    minion_list = Minions.objects.filter(status='Accepted', salt_server=salt_server)
    module_list = Module.objects.filter(client='execution').order_by('name')

    return render_to_response('salt/execute.html', locals())


def execute_fun(request, server_id):
    if request.is_ajax() and request.method == "GET":
        sid = request.GET.get("id")
        client = request.GET.get('client')
        tgt_type = request.GET.get('tgt_type')
        tgt = request.GET.get('tgt', '')
        fun = request.GET.get('fun')
        arg = request.GET.get('arg', '')
        user = request.session.get('username')
        result = {"ret":""}
        if sid:
            r = Result.objects.get(id=sid)
            result["ret"] = json.loads(r.result)
        else:
            try:
                salt_server = SaltServer.objects.get(id=server_id)
                salt_api = SaltApi(url=salt_server.url, username=salt_server.username, password=salt_server.password)
                if re.search('runner',client) or re.search('wheel',client):
                    r = salt_api.saltCmd(client=client, fun=fun, arg=arg, tgt=tgt)
                else:
                    r = salt_api.saltCmd(client=client, tgt=tgt, fun=fun, arg=arg, expr_form=tgt_type)
                if re.search('async',client):
                    jid = r['return'][0]['jid']
                    result["ret"] = jid    #异步命令只返回JID，之后JS会调用jid_info
                    res = Result(client=client, minions=tgt, fun=fun, arg=arg, tgt_type=tgt_type,
                                 server=salt_server, user=user, result=json.dumps(jid))
                    res.save()
                else:
                    result["ret"] = r["return"][0]
                    res = Result(client=client, minions=tgt, fun=fun, arg=arg, tgt_type=tgt_type,
                                 server=salt_server, user=user, result=json.dumps(r["return"][0]))
                    res.save()
            except Exception,e:
                result["ret"] = {"Error": str(e)}

        return JsonResponse(result, safe=False)

@login_valid
@csrf_exempt
def command(request):
    '''命令管理'''
    module_name = request.GET.get('module_name')
    client = request.GET.get('client')

    cmd_list = Command.objects.order_by('cmd')
    module_list = Module.objects.order_by('client', 'name')

    if request.is_ajax() and client:
        if re.search('runner',client):
            client = 'runner'
        elif re.search('wheel',client):
            client = 'wheel'
        else:
            client = 'execution'

        if module_name:
            # 请求模块下的命令
            cmd_list = cmd_list.filter(module__name=module_name, module__client=client).order_by('-cmd')
            cmd_list = [cmd.cmd for cmd in cmd_list]
            return JsonResponse(cmd_list, safe=False)
        else:
            # 请求CLIENT下的模块
            module_list = module_list.filter(client=client)
            module_list = [module.name for module in module_list.order_by('-name')]
            return JsonResponse(module_list, safe=False)

@login_valid
def minions(request, server_id):
    '''客户端管理'''
    username = request.session.get("username")
    image = User.objects.get(username=username).photo

    server_list = SaltServer.objects.all()
    try:
        salt_server = server_list.get(id=server_id)
    except:  #id不存在时返回第一个
        salt_server = server_list[0]

    try:
        salt_api = SaltApi(url=salt_server.url, username=salt_server.username, password=salt_server.password)
        # 对所有key刷新minions表数据
        a,d,u,r = salt_api.listKeys()
        if a:
            for m in a:
                collect(salt_server.id, m, 'Accepted')
        if d:
            for m in d:
                collect(salt_server.id, m, 'Denied')
        if u:
            for m in u:
                collect(salt_server.id, m, 'Unaccepted')
        if r:
            for m in r:
                collect(salt_server.id, m, 'Rejected')
        # minion不存在对应的key时设为未知
        keys = []
        for s in [a,d,u,r]:
            for m in s:
                keys.append(m)
        minion_list = Minions.objects.filter(salt_server=salt_server)
        ms = []
        for m in minion_list:
            if m.minion not in keys:
                m.status = 'Unknown'
                m.save()
            grains = json.loads(m.grains)
            grains['ipv4'].remove('127.0.0.1')
            obj = {'id':m.id,'minion':m.minion,'ip':grains['ipv4'],'os':grains['os'],'status':m.status}
            ms.append(obj)
        minionList = ms
    except Exception,e:
        error = e
    return render_to_response('salt/minions.html', locals())

def minions_fun(request):
    '''客户端KEY接收、删除、显示信息'''
    id = request.GET.get('id', '')
    active = request.GET.get('active','')
    if request.is_ajax() and id and active:
        try:
            minion = Minions.objects.get(id=id)
            salt_server = SaltServer.objects.get(id=minion.salt_server.id)
            salt_api = SaltApi(url=salt_server.url, username=salt_server.username, password=salt_server.password)
            if active == 'delete':
                success = salt_api.deleteKey(minion)
                if success:
                    minion.status = 'Unknown'
                    minion.save()
                    result = u'KEY"%s"删除成功！' % minion.minion
                else:
                    result = u'KEY"%s"删除失败！' % minion.minion
            elif active == 'accept':
                success = salt_api.acceptKey(minion)
                if success:
                    collect(salt_server.id, minion, 'Accepted')
                    result = u'KEY"%s"接受成功！'%minion.minion
                else:
                    result = u'KEY"%s"接受失败！'%minion.minion
            elif active == 'grains':
                result = json.loads(minion.grains)
            elif active == 'pillar':
                result = json.loads(minion.pillar)
        except Exception,e:
            result = str(e)
        return JsonResponse(result)

def collect(server_id, minion, status):
    '''客户端信息收集'''
    try:
        salt_server = SaltServer.objects.get(id=server_id)
        salt_api = SaltApi(url=salt_server.url, username=salt_server.username, password=salt_server.password)
        Minions.objects.get_or_create(minion=minion, salt_server=salt_server)
        Minion = Minions.objects.get(minion=minion, salt_server=salt_server)

        if status == "Accepted":
            grains = salt_api.saltMinions(minion)['return'][0][minion]
            pillar = salt_api.saltCmd(tgt=minion, fun='pillar.items', client='local')['return'][0][minion]
            Minion.grains = json.dumps(grains)
            Minion.pillar = json.dumps(pillar)
        Minion.status = status
        Minion.save()
        result = True
    except Exception,e:
        result = str(e)
    return result

@login_valid
def file_remote(request, server_id):
    '''远程文件操作'''
    username = request.session.get("username")
    image = User.objects.get(username=username).photo
    server_list = SaltServer.objects.all()
    try:
        salt_server = SaltServer.objects.get(id=server_id)
    except:
        salt_server = server_list[0]
    context = {'server_list':server_list, 'salt_server':salt_server, 'username':username, 'image':image}
    # 返回在线minions
    try:
        salt_api = SaltApi(url=salt_server.url, username=salt_server.username, password=salt_server.password)
        result = salt_api.saltRun(client='runner', fun='manage.status')
        context['minions_up'] = result['return'][0]['up']
    except Exception,e:
        context['error'] = e

    # 返回请求的目录列表和文件
    if request.method == "GET" and request.GET:
        tgt = request.GET.get("tgt")
        path = request.GET.get("path","").replace("//", "/").encode("utf-8")
        if path != '/':
            path = path.rstrip('/')
        dir = None
        if tgt and path:
            try:
                # 目录存在时返回目录
                salt_api = SaltApi(url=salt_server.url, username=salt_server.username, password=salt_server.password)
                if salt_api.saltCmd(client='local', tgt=tgt, fun='file.directory_exists', arg=path)['return'][0][tgt]:
                    path_str = path.split('/')
                    if path_str[-1] == '..':    # 返回上层目录
                        if len(path_str) > 3:
                            dir = '/'.join(path_str[0:-2])
                        else:
                            dir = '/'
                    else:
                        dir = path
                    svn_info = salt_api.saltCmd(client='local', tgt=tgt, fun='svn.info', arg=dir, arg1='fmt=dict')['return'][0][tgt][0]
                    if isinstance(svn_info, dict):
                        context['svn'] = {'URL':svn_info['URL'],'Revision':svn_info['Revision'],'LastChangedRev':svn_info['Last Changed Rev'],'LastChangeDate':svn_info["Last Changed Date"][0:20]}

                # 文件存在时，返回文件内容，加上文件格式、大小限制
                elif salt_api.saltCmd(client='local', tgt=tgt, fun='file.file_exists', arg=path)['return'][0][tgt]:
                    if os.path.splitext(path)[1] in FILE_FORMAT:
                        stats = salt_api.saltCmd(client='local', tgt=tgt, fun='file.stats', arg=path)['return'][0][tgt]
                        if stats['size'] <= 1024000:
                            content = salt_api.saltCmd(client='local', tgt=tgt, fun='cmd.run', arg='cat '+path)['return'][0][tgt]
                            context['content'] = content
                            context['stats'] = stats
                        else:
                            context['error'] = u"文件大小超过1M，拒绝访问！"
                    else:
                        context['error'] = u"文件格式不允许访问，请检查setting.FILE_FORMAT！"
                    # 返回当前文件目录信息
                    path_str = path.rstrip('/').split('/')
                    if len(path_str) > 2:
                        dir = '/'.join(path_str[0:-1])
                    else:
                        dir = '/'
                    svn_info = salt_api.saltCmd(client='local', tgt=tgt, fun='svn.info', arg=dir, arg1='fmt=dict', arg2='targets=%s' % path_str[-1])['return'][0][tgt][0]
                    if isinstance(svn_info,dict):
                        context['svn']={'URL':svn_info['URL'],'Revision':svn_info['Revision'],'LastChangedRev':svn_info['Last Changed Rev'],'LastChangeDate':svn_info["Last Changed Date"][0:20]}
                else:
                    context['error'] = u"目标不存在或者不是目录或文件！"

                # 根据路径获取列表
                if dir:
                    dirs = salt_api.saltCmd(client='local', tgt=tgt, fun='file.readdir', arg=dir)['return'][0][tgt]
                    try:
                        dirs.remove('.')
                        dirs.remove('.svn')
                    except:
                        pass
                    if dir == '/':
                        dirs.remove('..')
                    context['dir'] = dir
                    context['dir_list'] = dirs
                    context['tgt'] = tgt

            except Exception,e:
                context['error'] = e

    return render_to_response("salt/file_remote.html", context)


def file_remote_create(request):
    '''远程文件创建'''
    if request.is_ajax() and request.method == "GET":
        tgt = request.GET.get('tgt')
        name = request.GET.get('name')
        path_r = request.GET.get('path') + '/' + name
        path = path_r.encode('utf-8')
        type = request.GET.get('type')
        server = request.GET.get('server')
        result = {}
        try:
            salt_server = SaltServer.objects.get(id=server)
            salt_api = SaltApi(url=salt_server.url, username=salt_server.username, password=salt_server.password)
            # 新建目录或文件
            if type == "Dir":
                if salt_api.saltCmd(client='local', tgt=tgt, fun='file.directory_exists', arg=path)['return'][0][tgt]:
                    result = {'ret': 0, 'msg': u'目录"%s"已存在！' % path_r}
                else:
                    try:
                        salt_api.saltCmd(client='local', tgt=tgt, fun='file.mkdir', arg=path)
                        result = {'ret': 1, 'msg': u'目录"%s"创建成功！' % path_r}
                    except:
                        result = {'ret': 0, 'msg': u'目录"%s"创建失败！' % path_r}
            elif type == "File":
                # 创建文件，文件不存在时创建，存在则刷新创建时间，内容不变，目录不存在时返回false
                if salt_api.saltCmd(client='local',tgt=tgt,fun='file.file_exists',arg=path)['return'][0][tgt]:
                    result = {'ret': 0, 'msg': u'文件"%s"已存在！' % path}
                elif salt_api.saltCmd(client='local',tgt=tgt,fun='file.touch',arg=path)['return'][0][tgt]:
                    result = {'ret': 1, 'msg': u'文件"%s"创建成功！' % path_r}
            else:
                result = {'ret': 0, 'msg': u'目标类型错误！'}
        except Exception,e:
            result = {'ret': 0, 'msg': u'错误：%s' % e}
        return JsonResponse(result, safe=False)


def file_remote_rename(request):
    '''远程文件重命名'''
    if request.is_ajax() and request.method == "GET":
        tgt = request.GET.get('tgt')
        name = request.GET.get('name')
        path = request.GET.get('path', '').replace('//', '/').rstrip('/')
        server = request.GET.get('server')
        try:
            salt_server = SaltServer.objects.get(id=server)
            salt_api = SaltApi(url=salt_server.url, username=salt_server.username, password=salt_server.password)
            dst = '/'.join(path.split('/')[0:-1]) + '/' + name
            r = salt_api.saltCmd(client='local', tgt=tgt, fun='file.rename', arg1=path.encode('utf-8'), arg2=dst.encode('utf-8'))['return'][0][tgt]
            if r:
                result = {'ret': 1, 'msg': u'"%s"已成功重命名为"%s"！' % (path, dst), 'dst': dst.encode("utf-8")}
            else:
                result = {'ret': 0, 'msg': r}

        except Exception,e:
            result = {'ret': 0, 'msg': str(e)}
        return JsonResponse(result, safe=False)

def file_remote_write(request):
    '''写入文件内容'''
    if request.is_ajax() and request.method == "GET":
        tgt = request.GET.get('tgt')
        server = request.GET.get('server')
        path = request.GET.get('path')
        content = request.GET.get('content')
        try:
            salt_server = SaltServer.objects.get(id=server)
            salt_api = SaltApi(url=salt_server.url, username=salt_server.username, password=salt_server.password)
            # 判断文件是否存在
            if salt_api.saltCmd(client='local', tgt=tgt, fun='file.file_exists', arg=path)['return'][0][tgt]:
                r = salt_api.saltCmd(client='local', tgt=tgt, fun='file.write', arg1=path, arg2=content)['return'][0][tgt]
                if re.search('1', r):
                    result = u'文件%s修改成功！' % path
                else:
                    result = u'文件%s修改失败！' % path
            else:
                result = u"文件不存在"
        except Exception as e:
            result = str(e)
        return JsonResponse(result, safe=False)

def file_remote_delete(request):
    '''远程文件或目录删除'''
    if request.is_ajax() and request.method == "GET":
        tgt = request.GET.get('tgt')
        server = request.GET.get('server')
        path = request.GET.get('path')
        path_str = path.split('/')
        if len(path_str)>2:
            dir = '/'.join(path_str[0:-1])
        else:
            dir = '/'
        try:
            salt_server = SaltServer.objects.get(id=server)
            salt_api = SaltApi(url=salt_server.url, username=salt_server.username, password=salt_server.password)
            if salt_api.saltCmd(client='local', tgt=tgt, fun='file.remove',arg=path)['return'][0][tgt]:
                result = {'ret': 1, 'msg': u'目标"%s"删除成功！' % path, 'dir': dir}
            else:
                result = {'ret': 0, 'msg': u'目标"%s"删除失败！' % path}
        except Exception,e:
            result = {'ret': 0, 'msg': u'错误：%s' % e}
        return JsonResponse(result, safe=False)

@login_valid
def record(request):
    '''执行记录'''
    username = request.session.get("username")
    image = User.objects.get(username=username).photo

    minions_list = Minions.objects.all()

    minion = request.GET.get("minion")
    if minion:
        result_list = Result.objects.filter(minions=minion).order_by('-id')
    else:
        result_list = Result.objects.order_by('-id')
    count = result_list.count()
    return render_to_response("salt/records.html", locals())