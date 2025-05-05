from django.forms import (
    CharField, 
    PasswordInput, 
    Form, 
    ValidationError, 
    TextInput,
    EmailInput,
    Select
)
from . models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group


class LoginForm(Form):
    username = CharField(widget=TextInput({'id': 'username',
                                           'autocomplete': "new-username"}), label="Имя пользователя", max_length=150)
    password = CharField(widget=PasswordInput({'id': 'password',
                                               'autocomplete': "new-password"}), label="Пароль")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
                
        if username and password:
            try:
                u = User.objects.get(username=username)
                if not(u.is_active) and u.last_login is None:
                    self.add_error('username', "Ваша заявка еще не подтверждена.")
                else:
                    # Сохраняем пользователя для дальнейшего использования
                    self.user_cache = authenticate(username=username, password=password)  
                    if not(self.user_cache):
                        self.add_error('password', "Неверный пароль.")  
            except (User.DoesNotExist):
                # Добавим ошибку
                self.add_error('username', "Такого пользователя не существует.")

    def get_user(self):
        return self.user_cache  # Возвращаем аутентифицированного пользователя
    
    
class RegisterForm(Form):
    username = CharField(widget=TextInput({'id': 'username', 'autocomplete': "new-username"}), label="Имя пользователя", max_length=150)
    email = CharField(widget=TextInput({'id': 'email', 'autocomplete': "new-email"}))
    firstName = CharField(widget=TextInput({'id': 'firstName', 'autocomplete': "new-firstName"}), label="Имя", max_length=150)
    lastName = CharField(widget=TextInput({'id': 'lastName', 'autocomplete': "new-lastName"}), label="Фамилия", max_length=150)
    password1 = CharField(widget=PasswordInput({'id': 'password', 'autocomplete': "new-password"}), label="Пароль")
    password2 = CharField(widget=PasswordInput({'id': 'repeatpassword', 'autocomplete': "new-password"}), label="Повторите пароль")
    role = CharField(widget=Select({'id': 'role'}, choices=(
        (0, "Тип пользователя"),
        (1, "Преподаватель"),
        (2, "Лаборант")
    )))
    
    def clean(self):
        cleaned_data = super().clean()
        # Проверяю совпадение паролей
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise ValidationError("Пароли не совпадают")
        
        # TODO: Сделать валидацию пароля1
        
        # TODO: Сделать валидацию email
        
        # Проверяю существование таких пользователей
        if User.objects.filter(username=cleaned_data.get('username')).exists():
            raise ValidationError("Пользователь с таким именем уже существует")
        
        # Проверяю что у меня выбран тип пользователя
        if cleaned_data.get("role") == 0:
            raise ValidationError("Не выбран тип пользователя")
        else:
            gr_name = ["Преподаватели", "Лаборанты"][int(cleaned_data.get("role")) - 1]
            
        user = User.objects.create_user(
            username=cleaned_data.get("username"),
            email=cleaned_data.get("email"),
            first_name=cleaned_data.get("firstName"),
            last_name=cleaned_data.get('lastName'),
            password=cleaned_data.get("password1"),
            is_active=False
        )
        # Добавим пользователя в группу
        user.groups.set(Group.objects.filter(name=gr_name))
        
        
        