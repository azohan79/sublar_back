from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import UserRegisterForm
from .models import User, TeamPlacement
from .tokens import account_activation_token
from .utils import place_in_tree, build_tree
import logging
logger = logging.getLogger(__name__)

def register_view(request):
    # При POST берем код из POST, иначе из GET
    if request.method == "POST":
        ref_code = request.POST.get('referral_code')
    else:
        ref_code = request.GET.get('ref')

    if not ref_code:
        messages.error(request, "Регистрация невозможна без реферальной ссылки.")
        return redirect("login")

    logger.debug("DEBUG: ref_code = %s", ref_code)

    # Определение спонсора по реферальному коду
    sponsor = User.objects.filter(ref_link_1=ref_code).first() or \
              User.objects.filter(ref_link_2=ref_code).first()
    if not sponsor:
        messages.error(request, "Неверный реферальный код.")
        return redirect("login")
    logger.debug("DEBUG: sponsor = %s", sponsor)

    # Определение стороны регистрации
    side = 'L' if sponsor.ref_link_1 == ref_code else 'R'
    logger.debug("DEBUG: side = %s", side)

    # Далее – обработка POST и GET как раньше...
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            logger.debug("Форма валидна")
            try:
                # Создание пользователя
                user = form.save(commit=False)
                user.sponsor = sponsor
                user.save()
                logger.debug("Пользователь создан, id = %s", user.pk)
            except Exception as e:
                logger.error("Ошибка при сохранении пользователя: %s", e)
                messages.error(request, "Ошибка регистрации. Проверьте данные и попробуйте снова.")
                return render(request, "accounts/register.html", {"form": form, "sponsor": sponsor})

            # Размещение в бинарном дереве
            placement_ok, placement_msg, level = place_in_tree(sponsor, user, side)
            logger.debug("placement_ok = %s, placement_msg = %s, level = %s", placement_ok, placement_msg, level)
            if not placement_ok:
                messages.error(request, placement_msg)
                user.delete()
                return render(request, "accounts/register.html", {"form": form, "sponsor": sponsor})

            # Формирование ссылки активации
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            if isinstance(uid, bytes):
                uid = uid.decode()
            token = account_activation_token.make_token(user)
            activation_link = f"http://{current_site.domain}{reverse('activate', args=[uid, token])}"
            logger.debug("DEBUG: activation_link = %s", activation_link)

            # Отправка письма с подтверждением
            subject = "Подтверждение регистрации"
            message_body = (
                f"Здравствуйте, {user.full_name}!\n\n"
                f"Перейдите по ссылке для активации аккаунта:\n"
                f"{activation_link}\n\n"
                "Если вы не регистрировались на нашем сайте, проигнорируйте это письмо."
            )

            try:
                sent = send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                logger.debug("send_mail вернул: %s", sent)
                messages.success(request, "Регистрация прошла успешно! Проверьте почту для подтверждения.")
            except Exception as e:
                logger.error("Ошибка при отправке почты: %s", e)
                messages.error(request, "Ошибка при отправке письма с подтверждением.")

            return redirect("login")
        else:
            logger.debug("Ошибки формы: %s", form.errors)
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
            return render(request, "accounts/register.html", {"form": form, "sponsor": sponsor})
    else:
        form = UserRegisterForm(initial={'referral_code': ref_code})
        return render(request, "accounts/register.html", {"form": form, "sponsor": sponsor})




def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Ваш аккаунт успешно активирован! Теперь вы можете войти.")
        return redirect("login")
    else:
        messages.error(request, "Ссылка активации недействительна.")
        return redirect("accounts:register")

def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Неверный email или пароль.")
    return render(request, "accounts/login.html")

@login_required(login_url="login")
def dashboard_view(request):
    return render(request, "accounts/dashboard.html", {"user": request.user})

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")

def referral_register(request, referral_code):
    sponsor = User.objects.filter(ref_link_1=referral_code).first() or \
              User.objects.filter(ref_link_2=referral_code).first()
    if not sponsor:
        messages.error(request, "Неверный реферальный код.")
        return redirect("accounts:register")
    return redirect(f"{reverse('accounts:register')}?ref={referral_code}")

@login_required(login_url="login")
def team_view(request):
    user = request.user
    sponsor = user.sponsor  # или иным способом получаем спонсора
    direct_placements = user.placements_as_sponsor.all().order_by('side', 'created_at')
    tree = build_tree(user)  # строим дерево партнеров
    context = {
        'sponsor': sponsor,
        'direct_placements': direct_placements,
        'tree': tree,
    }
    return render(request, "accounts/team.html", context)

