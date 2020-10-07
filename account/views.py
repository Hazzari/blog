from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


# проверяет авторизирован ли пользователь.
@login_required
def dashboard(request):
    # после успешной авторизации пользователь будет перенаправлен на страницу куда он пытался попасть
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})
    # 'section' - с помощью нее мы можем узнать какой раздел сайта сейчас просматривает пользователь


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем пользователя в базе данных.
            Profile.objects.create(user=new_user)
            new_user.save()
            return render(request,
                          'account/registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/registration/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/registration/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})
# # Пример Обработчика Логина, но в джанго используются свои
# def user_login(request):
#     print(request.body)
#     if request.method == 'POST':
#         # Создаем объект формы
#         form = LoginForm(request.POST)
#         # Валидируем
#         if form.is_valid():
#             cd = form.cleaned_data
#             # Сверяем с базой данных. Функция возвращает обьект User,
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#             # если он успешно аутентифицирован
#             if user is not None:
#                 if user.is_active:
#                     # сохраняет текушего пользователя в сессии
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disable account')
#             else:
#                 return HttpResponse('Invalid login and password')
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form': form})
