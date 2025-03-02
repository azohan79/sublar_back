from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(label="ФИО", max_length=255)
    email = forms.EmailField(label="Email", required=True)
    phone = forms.CharField(label="Телефон", max_length=20)
    partner_type = forms.ChoiceField(
        label="Тип партнера",
        choices=[
            ('start', 'Start'),
            ('smart', 'Smart'),
            ('senior', 'Senior'),
            ('sovereign', 'Sovereign'),
            ('stellar', 'Stellar'),
        ],
        initial='start',
        widget=forms.HiddenInput(),
        required=False,
    )
    referral_code = forms.CharField(
        label="Реферальный код",
        max_length=32,
        required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        error_messages={'required': 'Обязательное поле. Регистрация невозможна без реферальной ссылки.'}
    )

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'partner_type', 'referral_code', 'password1', 'password2']

    def clean_partner_type(self):
        data = self.cleaned_data.get('partner_type')
        if not data:
            return 'start'
        return data

    def clean_referral_code(self):
        data = self.cleaned_data.get('referral_code')
        if not data:
            raise forms.ValidationError("Обязательное поле. Регистрация невозможна без реферальной ссылки.")
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Используем email как логин
        user.is_active = False  # Пользователь не активен до подтверждения через email
        user.partner_type = 'start'  # Задаём тип партнёра по умолчанию
        # Генерируем уникальные реферальные ссылки для нового пользователя
        user.ref_link_1 = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        user.ref_link_2 = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        if commit:
            user.save()
        return user