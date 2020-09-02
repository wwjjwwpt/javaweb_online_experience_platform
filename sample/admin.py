from django.contrib import admin
from .models import Springports,Mysqlports,CSpringports,CMysqlports
# Register your models here.

class sport(admin.ModelAdmin):
    list_display = ('port','user','port','time','state')
class csport(admin.ModelAdmin):
    list_display = ('id','port','user','time')

admin.site.register(Springports,sport)
admin.site.register(Mysqlports,sport)
admin.site.register(CSpringports,csport)
admin.site.register(CMysqlports,csport)