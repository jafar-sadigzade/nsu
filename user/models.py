from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('Username daxil etməlisiniz!'))

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superistifadəçi üçün is_staff aktiv olmalıdır!'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superistifadəçi üçün is_superuser aktiv olmalıdır!'))

        return self.create_user(username, password, **extra_fields)


def to_check_phone_length(number):
    if len(number) != 10:
        raise ValidationError(
            _(f"{number} uzunluğu düz deyil!")
        )


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        unique=True,
        db_index=True,
        max_length=50,
        help_text="Maksimum 50 simvol ola bilər"
    )
    email = models.EmailField(
        _("elektron poçt"),
        unique=True,
        db_index=True,
        help_text="Elektron poçtu düzgün daxil edin!"
    )
    first_name = models.CharField(
        _('Adınız'),
        max_length=50,
        help_text="Maksimum 50 simvol ola bilər!"
    )
    last_name = models.CharField(
        _('Soyadınız'),
        max_length=50,
        help_text="Maksimum 50 simvol ola bilər!"
    )
    father_name = models.CharField(
        _("Ata adınız"),
        max_length=50,
        help_text="Maksimum 50 simvol ola bilər!"
    )
    phone_number = models.CharField(
        _('Telefon nömrəsi'),
        max_length=10,
        unique=True,
        help_text="Nümunə 0701112233,\n digər heç bir forma qəbul edilməyəcək!",
        validators=[to_check_phone_length]
    )
    date_joined = models.DateTimeField(
        _("Qoşulma tarixi"),
        default=timezone.now,
        help_text="Dəyişmək mümkün deyil!"
    )
    is_staff = models.BooleanField(
        _("İşçi statusu"),
        default=False,
    )
    is_active = models.BooleanField(
        _("Hesab aktivlik statusu"),
        default=True
    )

    objects = CustomManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'İstifadəçi'
        verbose_name_plural = 'İstifadəçilər'
        indexes = [
            models.Index(fields=['username', 'email']),
        ]

    def __str__(self):
        return self.username
