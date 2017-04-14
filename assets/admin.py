#coding:utf8
from django.contrib import admin

# Register your models here.

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from User.models import User
from assets import models
from cmdb_auth.models import auth_group


# Now register the new UserAdmin...
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
#admin.site.unregister(Group)
admin.site.register(models.Asset)
admin.site.register(models.Server)
admin.site.register(models.NetworkDevice)
admin.site.register(models.IDC)
admin.site.register(models.Cabinet)
admin.site.register(models.Rack)
admin.site.register(models.BusinessUnit)
admin.site.register(models.Contract)
admin.site.register(models.CPU)
admin.site.register(models.Disk)
admin.site.register(models.NIC)
admin.site.register(models.RAM)
admin.site.register(models.Manufactory)
admin.site.register(models.Software)
admin.site.register(models.EventLog)
admin.site.register(models.NewAssetApprovalZone)
admin.site.register(auth_group)
