from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """커스텀 UserManager"""

    use_in_migrations = True

    def _create_user(self, user_id, name, birth, email, password, **extra_fields):
        """아이디, 비밀번호 등으로 user 생성"""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(user_id=user_id, name=name, birth=birth, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_id, name, birth, email, password=None, **extra_fields):
        """아이디, 비밀번호 등으로 user 생성"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_verified", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(user_id, name, birth, email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """email, password로 superuser 생성"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """커스텀 User Model"""

    username = None
    profile_image = models.ImageField(upload_to='profile_images', default='profile_images/default.png', null=True, blank=True)
    user_id = models.CharField(
        max_length=30,
        unique=True,
        default=True,
        validators=[
            RegexValidator(
                r'^[a-zA-Z0-9]*$',
                "아이디는 영문과 숫자로만 입력해주세요."
            )
        ])
    name = models.CharField(max_length=16, unique=False)
    birth = models.DateField(unique=False, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    is_verified = models.BooleanField(_("verified"), default=False)

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = []

    objects = UserManager()
