from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from user_enum import role_choice, t_user_choice, validate_status_choice, t_photo_choice
from coresys.models import CoreAddressArea, CoreAddressCity, CoreAddressProvince
from base.util.misc_validators import validators
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
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(pn, password, **extra_fields)


class UserBase(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), null=True)
    # FIXME: This is an issue, pn field should not be unique.
    pn = models.CharField(_('phone number'), max_length=25, unique=True, validators=[
        validators.get_validator("phone number")
    ])
    role = models.IntegerField(_("user role"), choices=role_choice.choice)
    register_date = models.DateTimeField(_("register date"), auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'pn'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('userbase')
        verbose_name_plural = _('usersbase')
        unique_together = ('pn', 'role')

    def get_full_name(self):
        return self.pn

    def get_short_name(self):
        return self.pn

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


# TODO: Deal with the validator, it is unsafe to be here.
class UserValidate(models.Model):
    uid = models.OneToOneField(UserBase, on_delete=models.CASCADE, related_name="user_validate", db_index=True)
    contact = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    idcard_number = models.CharField(max_length=30, null=True, blank=True)
    bankcard = models.CharField(max_length=255, null=True, blank=True)
    obank = models.CharField(max_length=255, null=True, blank=True)
    texno = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phonenum = models.CharField(max_length=25, null=True, blank=True, validators=[
        validators.get_validator("phone number")
    ])
    t_user = models.IntegerField(choices=t_user_choice.choice, null=True, blank=True)
    validate_status = models.IntegerField(choices=validate_status_choice.choice)


class UserValidatePhoto(models.Model):
    vid = models.ForeignKey(UserValidate, on_delete=models.CASCADE, related_name="validate_photo", db_index=True)
    v_photo = models.ImageField(upload_to=settings.UPLOAD_VALIDATE_PHOTO)
    inuse = models.BooleanField(default=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    t_photo = models.IntegerField(choices=t_photo_choice.choice)


class UserValidateArea(models.Model):
    vid = models.ForeignKey(UserValidate, on_delete=models.CASCADE, related_name="validate_area", db_index=True)
    pid = models.ForeignKey(CoreAddressProvince, on_delete=models.SET_NULL, related_name="uv_province", db_index=False, null=True, blank=True)
    cid = models.ForeignKey(CoreAddressCity, on_delete=models.SET_NULL, db_index=False, null=True, blank=True)
    aid = models.ForeignKey(CoreAddressArea, on_delete=models.SET_NULL, db_index=False, null=True, blank=True)


class UserAddressBook(models.Model):
    uid = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name="user_addressbook", db_index=True)
    aid = models.ForeignKey(CoreAddressArea, on_delete=models.SET_NULL, db_index=False, null=True, verbose_name=_("Area ID"))
    street = models.CharField(max_length=511, blank=True, null=True)
    contacts = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
