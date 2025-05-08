from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group


class User(AbstractUser):
    """Кастомная модель пользователя"""
    image = models.ImageField("Фото", upload_to="users-photos/", default="users-photos/default.png")
    
    def groups_display(self):
        return ", ".join([str(group) for group in self.groups.all()])
    
    def is_assistant(self):
        """Метод для проверки является ли пользователь лаборантом"""
        if self.groups.filter(name="Лаборанты").exists():
            return True
        return False

    def is_teacher(self):
        """Метод для проверки является ли пользователь преподавателем"""
        if self.groups.filter(name="Преподаватели").exists():
            return True
        return False


class Floor(models.Model):
    """Модель этажа"""
    name = models.IntegerField("Номер")
    image = models.ImageField("План", upload_to="floors/")
    description = models.TextField("Описание", null=True, blank=True)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = "этаж"
        verbose_name_plural = "Этажи"
        

class Room(models.Model):
    """Модель кабинета"""
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT, related_name="rooms")
    name = models.CharField("Номер", max_length=5, unique=True)
    coords = models.TextField("Координаты", max_length=250, null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    map_image = models.ImageField("План", null=True, blank=True, upload_to="roommaps/")
    
    # & Поле лаборанта
    assistant = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, 
        related_name="myworkroom", # ? Можно перейти от объекта лаборанта по полю 'myroom'
        verbose_name="Лаборант кабинета")
    # & Поле ответсвенного за кабинет преподавателя 
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
        related_name="myroom", # ? Можно перейти от объекта учителя по полю 'myroom'
        verbose_name="Владелец кабинета")
    
    # Размеры кабинета
    length = models.FloatField("Длина", null=True, blank=True)
    width = models.FloatField("Ширина", null=True, blank=True)
    height = models.FloatField("Высота", null=True, blank=True)
    
    # Прочие характеристики кабинета
    windows = models.IntegerField("Количество окон", null=True, blank=True)
    lamps = models.IntegerField("Количество ламп", null=True, blank=True)
    workspace_count = models.IntegerField("Количество рабочих мест", null=True, blank=True)
    
    def volume(self):
        """Метод определения объема"""
        return int(self.width * self.height * self.length)
    
    def area(self):
        """Метод вычисления площади"""
        return int(self.length * self.width)
    
    def __str__(self):
        """Метод строкового представления кабинета"""
        return self.name

    def save(self, *args, **kwargs):
        """Метод сохранения объекта кабинета"""
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
        verbose_name = "кабинет"
        verbose_name_plural = "Кабинеты"


class CabinetPhoto(models.Model):
    """Модель фотографии кабинета"""
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="images")
    image = models.ImageField("Фотография", upload_to="roomimages/")
    upload_at = models.DateField("Дата добавления", auto_now_add=True) # при создании добавляем дату обновления

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "фото кабитнета"
        verbose_name_plural = "Фото кабинетов"


class EquipmentMovementLog(models.Model):
    """Модель для логирования перемещения"""
    equipment = models.ForeignKey("Equipment", on_delete=models.CASCADE, related_name="movements")
    from_location = models.CharField(max_length=100, verbose_name="Откуда")
    to_location = models.CharField(max_length=100, verbose_name="Куда")
    moved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Кто переместил")
    moved_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата перемещения")
    notes = models.TextField(blank=True, verbose_name="Примечание")

    def __str__(self):
        return f"{self.equipment.inventory_number} перемещено из {self.from_location} в {self.to_location}"

    class Meta:
        ordering = ["-moved_at"]
        verbose_name = "Лог перемещения"
        verbose_name_plural = "Логи перемещения"


class EquipmentDiscardLog(models.Model):
    """Модель для логирования списания"""
    equipment = models.ForeignKey("Equipment", on_delete=models.CASCADE, related_name="discards")
    discard_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Кто списал")
    discard_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата списания")
    notes = models.TextField(blank=True, verbose_name="Примечание")

    def __str__(self):
        return f"{self.equipment.inventory_number} списано"

    class Meta:
        ordering = ["-discard_at"]
        verbose_name = "Лог списания"
        verbose_name_plural = "Логи списания"
        
        
class EquipmentType(models.Model):
    """Модель типа оборудования кабинета"""
    name = models.CharField("Название", max_length=100, unique=True) # Название оборудования пр. Компьютер / Ноутбук
    description = models.TextField("Описание", blank=True)
    attributes_schema = models.JSONField("Характеристики", default=dict) # Схема атрибутов типа оборудования
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Типы оборудования"
        verbose_name_plural = "Тип оборудования"

    
class Equipment(models.Model):
    """Модель оборудования"""
    STATUS_CHOICES = [
        ('working', "Исправен"),
        ('repair', "В ремонте"),
        ('broken', "Неисправен")
    ]
    type = models.ForeignKey(EquipmentType, on_delete=models.PROTECT, verbose_name="Тип оборудования")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Кабинет", related_name="equipments")
    inventory_number = models.CharField("Инвентарный номер", max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='working')
    # ^ Не активное оборудование = списанное (is_active=False -> Списанное оборудование)
    is_active = models.BooleanField("Состоит на учете", default=True)
    purchase_date = models.DateField("Дата покупки", null=True, blank=True)
    # & Характеристики оборудования в соответствии с типом оборудования
    attributes = models.JSONField("Характеристики", default=dict)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True)
    image = models.ImageField("Фотография", upload_to="equipmentimages/", default="equipmentimages/default.png")
    coords = models.CharField("Координаты", max_length=100, null=True, blank=True)
    
    def type_name(self):
        return self.type.name
    
    def __str__(self):
        return self.type.name + " " + self.inventory_number

    class Meta:
        verbose_name = "оборудование"
        verbose_name_plural = "🖥️ Оборудование"
    
    def save(self, *args, **kwargs):
        """Переопределим метод сохранения для добавления записи о перемещении"""
        # Если объект уже существует в БД и положение изменилось
        if self.pk:
            # Создаем лог перемещения
            old_equipment = Equipment.objects.get(pk=self.pk)
            if old_equipment.room != self.room:
                EquipmentMovementLog.objects.create(
                    equipment=self,
                    from_location=old_equipment.room,
                    to_location=self.room,
                    moved_by=kwargs.pop("moved_by", None),  # можно передать пользователя
                )
                
            # Создаем лог списания
            discard_by = kwargs.pop("discard_by", None)
            if discard_by is not None:
                EquipmentDiscardLog.objects.create(
                    equipment=self,
                    discard_by=discard_by,  # можно передать пользователя
                )
                
        # Наследовательное сохранение
        super().save(*args, **kwargs)
        