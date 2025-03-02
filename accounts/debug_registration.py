from accounts.models import User
from accounts.forms import UserRegisterForm
from accounts.utils import place_in_tree, build_tree
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from accounts.tokens import account_activation_token
from django.core.mail import send_mail
from django.conf import settings

# Шаг 1. Получаем спонсора по email
sponsor = User.objects.filter(email="9985585@gmail.com").first()
if sponsor is None:
    print("Спонсор с email 9985585@gmail.com не найден.")
else:
    print("Найден спонсор:", sponsor)
    print("Реферальный код спонсора (ref_link_1):", sponsor.ref_link_1)

# Шаг 2. Формируем данные для регистрации нового пользователя
data = {
    'full_name': 'Left User',
    'email': '9608490@gmail.com',
    'phone': '9876543210',
    'partner_type': 'start',
    'referral_code': sponsor.ref_link_1,
    'password1': 'StrongPassword123',
    'password2': 'StrongPassword123'
}

# Шаг 3. Имитируем заполнение формы регистрации
form = UserRegisterForm(data)
print("Форма валидна?", form.is_valid())
if not form.is_valid():
    print("Ошибки формы:", form.errors)
else:
    # Шаг 4. Создаем пользователя
    try:
        user = form.save(commit=False)
        user.sponsor = sponsor
        user.save()
        print("Пользователь создан, ID =", user.pk)
    except Exception as e:
        print("Ошибка при сохранении пользователя:", e)

    # Шаг 5. Определяем сторону регистрации (в данном случае всегда 'L')
    side = 'L'
    print("Сторона регистрации =", side)

    # Шаг 6. Размещаем пользователя в бинарном дереве
    placement_ok, placement_msg, level = place_in_tree(sponsor, user, side)
    print("Размещение:", placement_ok, placement_msg, "Уровень:", level)
    if not placement_ok:
        print("Ошибка размещения. Отмена регистрации.")
    else:
        # Шаг 7. Формируем активационную ссылку
        domain = "s1.sublar.kz"  # Ваш домен
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        if isinstance(uid, bytes):
            uid = uid.decode()
        token = account_activation_token.make_token(user)
        activation_path = reverse('activate', args=[uid, token])
        activation_link = f"http://{domain}{activation_path}"
        print("Активационная ссылка:", activation_link)

        # Шаг 8. Отправляем письмо с подтверждением
        subject = "Подтверждение регистрации"
        message_body = (
            f"Здравствуйте, {user.full_name}!\n\n"
            f"Перейдите по ссылке для активации аккаунта:\n"
            f"{activation_link}\n\n"
            "Если вы не регистрировались на нашем сайте, проигнорируйте это письмо."
        )
        try:
            sent = send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            print("send_mail вернул:", sent)
        except Exception as e:
            print("Ошибка при отправке почты:", e)
