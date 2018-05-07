from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from user_enum import role_choice, t_user_choice, validate_status_choice, t_photo_choice
from coresys.models import CoreAddressArea, CoreAddressCity, CoreAddressProvince
from django.conf import settings


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, pn, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not pn:
            raise ValueError('The phone number must be set')

        user = self.model(pn=pn, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, pn, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(pn, password, **extra_fields)

    def create_superuser(self, pn, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(pn, password, **extra_fields)


class UserBase(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), null=True)
    pn = models.CharField(_('phone number'), max_length=25, unique=True)
    role = models.IntegerField(_("user role"), choices=role_choice.choice, max_length=role_choice.MAX_LENGTH)
    register_date = models.DateTimeField(_("register date"), auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'pn'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('userbase')
        verbose_name_plural = _('usersbase')

    def get_full_name(self):
        return self.pn

    def get_short_name(self):
        return self.pn

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserValidate(models.Model):
    uid = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name="user_validate", db_index=True)
    contact = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    bankcard = models.CharField(max_length=255, null=True, blank=True)
    obank = models.CharField(max_length=255, null=True, blank=True)
    textno = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phonenum = models.CharField(max_length=25, null=True, blank=True)
    t_user = models.IntegerField(max_length=t_user_choice.MAX_LENGTH, choices=t_user_choice.choice)
    validate_status = models.IntegerField(max_length=validate_status_choice.MAX_LENGTH, choices=validate_status_choice.choice)


class UserValidatePhoto(models.Model):
    vid = models.ForeignKey(UserValidate, on_delete=models.CASCADE, related_name="validate_photo", db_index=True)
    path = models.ImageField(upload_to=settings.UPLOAD_VALIDATE_PHOTO)
    inuse = models.BooleanField(default=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    t_photo = models.IntegerField(max_length=t_photo_choice.MAX_LENGTH, choices=t_photo_choice.choice)


class UserValidateArea(models.Model):
    vid = models.OneToOneField(UserValidate, on_delete=models.CASCADE, related_name="validate_area", db_index=True)
    pid = models.ForeignKey(CoreAddressProvince, on_delete=models.SET_NULL, related_name="uv_province", db_index=False, null=True)
    cid = models.ForeignKey(CoreAddressCity, on_delete=models.SET_NULL, db_index=False, null=True)
    aid = models.ForeignKey(CoreAddressArea, on_delete=models.SET_NULL, db_index=False, null=True)


class UserAddressBook(models.Model):
    uid = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name="user_addressbook", db_index=True)
    aid = models.ForeignKey(CoreAddressArea, on_delete=models.SET_NULL, db_index=False, null=True, verbose_name=_("Area ID"))
    street = models.CharField(max_length=511, blank=True, null=True)
    contacts = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
