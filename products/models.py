from django.db import models
import jwt
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

USER_MODEL = settings.AUTH_USER_MODEL

"""Иницилизация емайл для пользователя"""
class UserManager(BaseUserManager):
    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Указанное имя пользователя должно быть установлено')

        if not email:
            raise ValueError('Данный адрес электронной почты должен быть установлен')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

"""Создание пользователя и получение jwt token"""
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(validators=[validators.validate_email], unique=True, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        # token = jwt.encode({'id': self.pk, 'exp': int(dt.strftime('%s')) }, settings.SECRET_KEY, algorithm='HS256')
        token = jwt.encode({
             'id': self.pk,
             'exp': dt.utcfromtimestamp(dt.timestamp())    #CHANGE HERE
    }, settings.SECRET_KEY, algorithm='HS256')
        return token
    
"""Модель компании"""
class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default='user')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

"""Модель сотрудника компании"""
class Custom(models.Model):
    user_company = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, default='user')
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return '{}/{}'.format(self.first_name, self.last_name)

"""ид пользователя и компании"""
class Purchase(TimeStampModel):
    user_id = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)

"""Модель авто компании"""
class Auto(models.Model):
    user_auto = models.ForeignKey(Custom, on_delete=models.SET_DEFAULT, default='user')
    user_company = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, default='user')
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    power = models.CharField(max_length=100)

    def __str__(self):
        return '{},{}'.format(self.brand,  self.model)


"""Модель офиса компании"""
class Office(models.Model):
    name_company = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, default='user')
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/', blank=True, null=True)

    def __str__(self):
        return self.name_company