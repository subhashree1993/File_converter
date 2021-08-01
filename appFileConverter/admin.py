from django.contrib import admin
from .models import User
from .models import FileConvert
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('id','name','email','password')


@admin.register(FileConvert)
class UserAdmin(admin.ModelAdmin):
    list_display=('userId','fileName', 'originalFilePath', 'convertedFilePath','convertedFrom', 'convertedTo', 'requestedTime', 'conversionStatus')
