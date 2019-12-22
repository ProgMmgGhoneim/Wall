from django.contrib import admin

from .models import Profile ,Wall
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user' , 'email_confirmed' )
    readonly_fields =('email_confirmed',)
    search_fields = ['email_confirmed']
    list_per_page =15


class WallAdmin(admin.ModelAdmin):
    my_field =('author','title','content','timestap','updated_data')
    list_display = my_field
    readonly_fields =('timestap','updated_data')
    search_fields = my_field
    list_per_page =15





admin.site.register(Profile ,ProfileAdmin)
admin.site.register(Wall ,WallAdmin)
