from django.contrib import admin

from usersys.models import UserBase, UserValidate, UserValidateArea, UserValidatePhoto, UserSid

# Register your models here.

admin.site.register([UserBase, UserValidate, UserValidateArea, UserValidatePhoto, UserSid])
