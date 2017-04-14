>Author：学神IT-1610-python-小小
# CMDB
>自动化运维系统（Django + Bootstrap + Saltstack），Github：https://github.com/yezhenli/CMDB/tree/master/CMDB

## Install guideline:
* 采集端操作系统：Centos 6.5
* Python版本：2.7.9 版本以上
* Django版本：1.9.0
* 安装第三方模块： pip install -r requirements.txt
* 采集端运行方法:采集端得脚本在Bin/python_send.py，本脚本需要传递两个位置参数，
  第一个参数为django运行服务器得ip地址，第二个参数为端口号(为避免数据传递失败，请使用默认8000端口)，
  运行方法 例如:python python_send.py 192.168.1.110 8000 
* Saltstack环境部署文档，参见 doc/deployment/saltstack.txt
* Mster端部署salt-api文档，参见 doc/deployment/saltapi.txt

## Project screenshots

##  目前已实现功能：

### CMDB资产管理：

>－资产管理: 资产列表展示、资产详细信息、资产查询、资产添加和删除
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/asset_list.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/asset_detail.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/asset_search1.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/asset_search2.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/asset_add.png)

>－机房管理：机房列表展示、查询和添加
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/idc.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/idc_search.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/idc_add.png)

>－监控平台：监控主机列表、监控图
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/monitor_list.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/graph01.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/graph02.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/graph03.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/graph04.png)

>－用户及权限：用户列表、角色列表、权限列表、权限分配、成员管理
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/user_list.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/role.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/permission_manage.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/staff_manage.png)

>－自动化运维管理：执行命令、Minions管理、远程文件、执行记录
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/execute1.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/minions.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/file_remote.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/file_remote_create.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/file_remote_write.png)
![](https://github.com/yezhenli/CMDB/blob/master/static/image/screen/records.png)
