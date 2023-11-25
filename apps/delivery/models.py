from datetime import timedelta, datetime
from apps.user.models import CustomUser
from django.db import models


# region BASE FUNCTIONS AND CLASSES

# endregion

# region ДОСТАВКА
class TypeDelivery(models.Model):
    """
       Типы доставки
    """
    name_delivery = models.CharField(verbose_name='Тип доставки', max_length=50)
    code_delivery = models.CharField(verbose_name='Код доставки', max_length=50, help_text='', default="LS")
    duty = models.FloatField(verbose_name='Гос. пошлина у.е.', default=300)

    def __str__(self):
        return self.name_delivery

    class Meta:
        verbose_name = 'Варианты доставки'
        verbose_name_plural = 'Варианты доставки'


class DeliveryRate(models.Model):
    """
    Коэффициенты и цена в зависимости
    от веса и типа доставки
    """
    type_delivery = models.ForeignKey(TypeDelivery, on_delete=models.CASCADE)
    weight = models.FloatField(verbose_name='Вес тон.', default=0)
    rate = models.FloatField(verbose_name='Коэффициент', default=0)
    price = models.FloatField(verbose_name='Стоимость', default=0)

    class Meta:
        verbose_name = 'Стоимость доставки'
        verbose_name_plural = 'Стоимость доставки'

    def str(self):
        return f'{self.type_delivery}'
        # TODO: Исправить отображение в общем списке


# endregion

# region БАЗОВЫЕ ЦЕПИ

class BaseChain(models.Model):
    """
     Базовые цепи
    """
    GOST_ISO_DIN = (
        ('MGOST', 'M ГОСТ 588-81'),
        ('MISO1977', 'M ISO 1977'),
        ('MTISO1977', 'MT ISO 1977'),
        ('FVDIN', 'FV DIN'),
        ('FVТDIN', 'FVТ DIN'),
        ('FVCDIN', 'FVC DIN'),
        ('ZDIN', 'Z DIN'),
        ('ZEDIN', 'ZE DIN'),
        ('ZCDIN', 'ZC DIN'),
    )
    name_chains = models.CharField(verbose_name='Название цепи', max_length=50, help_text='')
    standard = models.CharField(verbose_name='Стандарт', max_length=13, choices=GOST_ISO_DIN)
    weight = models.FloatField(verbose_name='Вес', null=True)
    rate = models.FloatField(verbose_name='Коэффициент')

    class Meta:
        verbose_name = "Базовая цепь"
        verbose_name_plural = "Базовые цепи"

    def __str__(self):
        return self.name_chains


# endregion

# region БРЭНД ЦЕПИ И ВАРИАНТЫ ОБРАБОТКИ
class BrandChain(models.Model):
    """
     БРЭНД ЦЕПИ
    """
    name_brand = models.CharField(verbose_name='Брэнд', max_length=50, help_text='')

    class Meta:
        verbose_name = "Брэнд цепи"
        verbose_name_plural = "Брэнд цепи"

    def __str__(self):
        return self.name_brand


class OtherVariant(models.Model):
    """
     ВАРИАНТЫ ОБРАБОТКИ ЦЕПИ
    """
    TYPE_OF_PROCESSING = (

        ('NOP', 'без обработки'),
        ('ZN', 'оцинковка(ZN)'),
        ('NP', 'никелирование(NP)'),
        ('DR', 'горячая оцинковка(DR)'),
        ('GM', 'покрытие цепи геомет(GM)'),
        ('SS', 'нержавейка(SS)'),
    )

    brand = models.ForeignKey(BrandChain, on_delete=models.CASCADE, default=1)
    type_processing = models.CharField(verbose_name='Тип обработки цепи', max_length=30, help_text='',
                                       choices=TYPE_OF_PROCESSING, default='NOP')
    km_field = models.FloatField(verbose_name='Стоимость кг. дол. США', default=1)
    days = models.IntegerField(verbose_name='Дней на изготовление', help_text='', default=70)
    margin = models.FloatField(verbose_name='Маржа', default=1)

    def __str__(self):
        return f' {self.brand}-{self.type_processing}-{self.km_field}-{self.days}-{self.margin}'

    class Meta:
        verbose_name = 'Дополнительные варианты обработки'
        verbose_name_plural = 'Дополнительные варианты обработки'


# endregion

class Client(models.Model):
    # поля для клиента
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    note = models.TextField()
    unp = models.CharField(max_length=100)  # имя клиента
    email = models.EmailField()  # электронная почта клиента
    phone = models.CharField(max_length=20)  # телефон клиента
    address = models.TextField()  # адрес клиента

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'


class ContactClient(models.Model):  # наследуем от модели и базового класса
    # поля для контакта клиента

    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # ссылка на клиента
    name = models.CharField(max_length=100)
    note = models.TextField()
    role = models.CharField(max_length=50)
    email = models.EmailField()  # электронная почта контакта
    phone = models.CharField(max_length=20)  # телефон контакта

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Calculation(models.Model):
    """
        РАСЧЕТЫ ДОСТАВКИ
    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    type_delivery = models.ForeignKey(TypeDelivery, on_delete=models.CASCADE, default=None)
    contact_client = models.ForeignKey(ContactClient, on_delete=models.CASCADE, default=None)
    base_chain = models.ForeignKey(BaseChain, on_delete=models.CASCADE, default=0)
    brand = models.ForeignKey(BrandChain, on_delete=models.CASCADE, default=0)
    type_processing = models.ForeignKey(OtherVariant, on_delete=models.CASCADE, default=0)
    weight = models.IntegerField(verbose_name='Вес', default=1)
    days = models.IntegerField(verbose_name='Дней', default=1)
    created = models.DateTimeField(verbose_name='Дата расчета', default=datetime.now)

    data_delivery = models.DateField(verbose_name='Ориентировочная дата доставки',
                                     default=datetime.now)  # рассчитать автоматически

    class Meta:
        verbose_name = 'Расчет'
        verbose_name_plural = 'Расчеты'

    def save(self, *args, **kwargs):
        if self.days:  # Проверить, что days имеет значение, а не None
            self.data_delivery = datetime.now().date() + timedelta(days=self.days)  # Вычислить дата доставки
        super().save(*args, **kwargs)













