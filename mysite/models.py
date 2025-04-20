from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group


class User(AbstractUser):
    """Кастомная модель пользователя"""
    image = models.ImageField("Фото", upload_to="users-photos/", default="users-photos/default.png")
    

class Floor(models.Model):
    """Модель этажа"""
    name = models.IntegerField("Номер")
    image = models.ImageField("План", upload_to="floors/")
    description = models.TextField("Описание", null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Этажи"
        verbose_name_plural = "этаж"
        

class Room(models.Model):
    """Модель кабинета"""
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT, related_name="rooms")
    name = models.CharField("Номер", max_length=5)
    coords = models.TextField("Координаты")
    description = models.TextField("Описание", null=True, blank=True)
    # & Поле лаборанта
    assistant = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True, 
        related_name="myworkroom", # ? Можно перейти от объекта лаборанта по полю 'myroom'
        verbose_name="Лаборант кабинета"
    )
    # & Поле ответсвенного за кабинет преподавателя 
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="myroom", # ? Можно перейти от объекта учителя по полю 'myroom'
        verbose_name="Владелец кабинета"
    )
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # ? Установим ограничение на установку в качестве лаборантов только их
        if self.assistant:
            if not self.assistant.groups.filter(name="Лаборанты").exists():
                # Вызовем ошибку
                raise ValueError("Выбранный пользователь не состоит в группе лаборантов")
        
        # ? Установим ограничение на установку в качестве владельца только учителя
        if self.owner:
            if not self.owner.groups.filter(name="Учителя").exists():
                # Вызовем ошибку
                raise ValueError("Выбранный пользователь не состоит в группе учителей")
        
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Кабинеты"
        verbose_name_plural = "кабинет"