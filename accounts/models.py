from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, phone, password=None, referral_code=None, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        # Регистрация без реферального кода недопустима
        if not referral_code:
            raise ValueError(_('Registration is not possible without a referral code'))

        email = self.normalize_email(email)
        # Поиск спонсора по реферальной ссылке
        try:
            sponsor_user = self.get(ref_link_1=referral_code)
        except self.model.DoesNotExist:
            raise ValueError(_('Invalid referral code'))

        user = self.model(
            email=email,
            full_name=full_name,
            phone=phone,
            sponsor=sponsor_user,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        email = self.normalize_email(email)
        # Для суперпользователя спонсор может оставаться None
        user = self.model(
            email=email,
            full_name=full_name,
            phone=phone,
            sponsor=None,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    PARTNER_TYPES = [
        ('start', 'Start'),
        ('smart', 'Smart'),
        ('senior', 'Senior'),
        ('sovereign', 'Sovereign'),
        ('stellar', 'Stellar'),
    ]

    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPES, default='start')
    sponsor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    ref_link_1 = models.CharField(max_length=32, unique=True, default=get_random_string(32))
    ref_link_2 = models.CharField(max_length=32, unique=True, default=get_random_string(32))
    is_active = models.BooleanField(default=False)  # False until email confirmation
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Дополнительные поля:
    pv = models.IntegerField(default=0, verbose_name="PV (power value)")
    activity_status = models.BooleanField(default=False, verbose_name="Активность")
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Значение кошелька")
    binary_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Значение бинарного счета")
    QUALIFICATION_CHOICES = [(i, f"Status {i}") for i in range(10)]
    qualification = models.IntegerField(choices=QUALIFICATION_CHOICES, default=0, verbose_name="Квалификация")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone']

    def __str__(self):
        return self.email

class MenuItem(models.Model):
    MAIN_MENU_CHOICES = [
        ('home', 'Главная'),
        ('career', 'Моя карьера'),
        ('team', 'Моя команда'),
        ('promo', 'Промо и розыгрыши'),
        ('news', 'Новости и публикации'),
        ('ads', 'Рекламные материалы'),
        ('profile', 'Мой профиль'),
        ('orders', 'Мои заказы'),
        ('wallet', 'Мой кошелек'),
    ]
    FOOTER_MENU_CHOICES = [
        ('docs', 'Документы компании'),
        ('support', 'Поддержка'),
    ]
    title = models.CharField(max_length=100)  # Название пункта меню
    menu_type = models.CharField(max_length=10, choices=MAIN_MENU_CHOICES + FOOTER_MENU_CHOICES)
    is_main_menu = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class PortalSettings(models.Model):
    header_logo = models.ImageField(upload_to='portal/logo/', verbose_name=_("Логотип"))
    header_menu = models.ManyToManyField(
        MenuItem,
        blank=True,
        related_name="header_menu_items",
        verbose_name=_("Меню в хедере")
    )
    footer_menu = models.ManyToManyField(
        MenuItem,
        blank=True,
        related_name="footer_menu_items",
        verbose_name=_("Меню в футере")
    )

    class Meta:
        verbose_name = _("Настройка портала")
        verbose_name_plural = _("Настройки портала")

    def __str__(self):
        return "Настройки портала"

class MarketingPlan(models.Model):
    partner_types = models.TextField(
        verbose_name=_("Типы партнеров"),
        help_text=_("Введите типы партнеров через запятую (например: start, smart, senior, sovereign, stellar)")
    )
    qualification_types = models.TextField(
        verbose_name=_("Типы квалификаций"),
        help_text=_("Введите типы квалификаций через запятую (например: Status 0, Status 1, ..., Status 9)")
    )
    activity_period = models.CharField(
        max_length=255,
        verbose_name=_("Период активности"),
        help_text=_("Введите диапазон активности (например: 2025-01-01 до 2025-12-31)")
    )
    career = models.TextField(
        verbose_name=_("Карьера"),
        help_text=_("Описание карьеры"),
        blank=True,
        null=True
    )
    team = models.TextField(
        verbose_name=_("Команда"),
        help_text=_("Описание команды"),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("Маркетинговый план")
        verbose_name_plural = _("Маркетинговые планы")

    def __str__(self):
        return "Маркетинговый план"

class TeamPlacement(models.Model):
    """
    Модель для хранения бинарных связей в маркетинговой программе.
    Каждый пользователь (sponsor) может иметь по одной записи на каждой стороне.
    При регистрации, если нужное место занято, производится поиск в глубину (BFS).
    """
    SIDE_CHOICES = [
        ('L', 'Left'),
        ('R', 'Right'),
    ]
    sponsor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="placements_as_sponsor",
        help_text="Пользователь, под которым находится реферал"
    )
    child = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="placements_as_child",
        help_text="Реферал (новый пользователь)"
    )
    side = models.CharField(
        max_length=1,
        choices=SIDE_CHOICES,
        help_text="Сторона в бинарном дереве (L – левая, R – правая)"
    )
    level = models.PositiveIntegerField(
        default=1,
        help_text="Уровень (глубина) реферала в ветви относительно данного sponsor"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    marketing_activity = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.sponsor} → {self.child} ({self.get_side_display()})"
