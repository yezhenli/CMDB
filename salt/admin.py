from django.contrib import admin
from salt.models import *

# Register your models here.

admin.site.register(SaltServer)
admin.site.register(Module)
admin.site.register(Command)