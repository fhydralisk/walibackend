from django.contrib import admin

from usersys.models import UserBase, UserValidate, UserValidateArea, UserValidatePhoto, UserSid
from backgroundsys.admin_site import admin_site
# Register your models here.

admin_site.register([UserBase, UserValidatePhoto, UserSid])