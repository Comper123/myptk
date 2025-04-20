from django.forms import CharField, PasswordInput, Form, ValidationError, TextInput
from . models import User
from django.contrib.auth import authenticate


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
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Неверное имя пользователя или пароль.")
            else:
                self.user_cache = user  # Сохраняем пользователя для дальнейшего использования

    def get_user(self):
        return self.user_cache  # Возвращаем аутентифицированного пользователя