# MODELS
from datetime import timedelta, datetime

from django.http import HttpResponse, request

from apps.user.models import CustomUser
from django.db import models


# region ДОСТАВКА
class TypeDelivery(models.Model):
    """
       Типы доставки
    """
    name_delivery = models.CharField(verbose_name='Тип доставки', max_length=50)
    code_delivery = models.CharField(verbose_name='Код доставки', max_length=50, help_text='', default="LS")
    duty = models.FloatField(verbose_name='Гос. пошлина у.е.', default=300)
    days = models.IntegerField(verbose_name='Доставка в днях', default=0)

    def __str__(self):
        return f'{self.name_delivery}'

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
    km_field = models.FloatField(verbose_name='Коэффициенты стоимости цепей', default=1)
    days = models.IntegerField(verbose_name='Дней на изготовление', help_text='', default=70)
    margin = models.FloatField(verbose_name='Маржа', default=1)

    def __str__(self):
        return f' {self.brand}-{self.type_processing}'

    class Meta:
        verbose_name = 'Дополнительные варианты обработки'
        verbose_name_plural = 'Дополнительные варианты обработки'


# endregion


# region КОНТРАГЕНТ И КОНТАКТЫ
class Client(models.Model):
    # поля для клиента
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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


# endregion


# region РАСЧЕТЫ ДОСТАВКИ
class Calculation(models.Model):
    """
         ВЫПОЛНЕННЫЕ РАСЧЕТЫ ДОСТАВКИ
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=1)
    type_delivery = models.ForeignKey(TypeDelivery, on_delete=models.CASCADE, default=None)
    base_chain = models.ForeignKey(BaseChain, on_delete=models.CASCADE, default=0)
    type_processing = models.ForeignKey(OtherVariant, on_delete=models.CASCADE, default=0)
    weight = models.FloatField(verbose_name='Общий вес', default=0)
    days = models.IntegerField(verbose_name='Дней на доставку', default=0)
    created = models.DateTimeField(verbose_name='Дата расчета', default=datetime.now)
    quantity_chains_m=models.IntegerField(verbose_name='Количество цепи в метрах', default=0)
    price_1m= models.FloatField(verbose_name='Стоимость метра цепи с доставкой у.е.', default=0)
    price_full=models.FloatField(verbose_name='Полная стоимость у.е.', default=0)
    data_delivery = models.DateField(verbose_name='Ориентировочная дата доставки',
                                    default=datetime.now)  # рассчитать автоматически
    price_calc_weight=models.FloatField(verbose_name='Цена из модели "Стоимость доставки"', default=0)

    class Meta:
        verbose_name = 'Расчет'
        verbose_name_plural = 'Расчеты'

    def save(self, *args, **kwargs):
        """
               Вычисление примерной даты доставки и стоимости
               """
        # вес всего заказа в тонах
        self.weight = (self.base_chain.weight * self.quantity_chains_m) / 1000

        # для чтобы не забыть занес все данные в переменные
        max_sea, delivery_id_sea = 26, 2
        max_train, delivery_id_train = 24, 3
        max_auto, delivery_id_auto = 21, 4
        max_airplane, delivery_id_airplane = 5, 5
        # максимальные веса по доставкам и номер
        dict = {2:26,
                3:24,
                4:21,
                5:5}

        for type_delivery, weight in dict.items():
            if type_delivery == self.type_delivery and self.weight > weight:

                # остаток веса
                remaind_weight = self.weight - (self.weight // weight) * weight
                # цена доставки для остатка
                # получим цену по первому значению больше remained_weight
                price_delivery_remaind = DeliveryRate.objects.filter(weight__gt=remaind_weight,
                                         type_delivery_id=self.type_delivery).order_by('weight').first().price
                # цена за полный контейнер
                price_delivery_full_weight = DeliveryRate.objects.filter(weight__gt=remaind_weight,
                                         type_delivery_id=self.type_delivery).latest('weight').price
                # цена за несколько контейнеров
                price_delivery_full_weight *= self.weight // weight
                # цена за полные контейнеры + неполный
                price_weight_all = price_delivery_full_weight + price_delivery_remaind
                # цена за килограмм
                self.price_1m = ((((self.base_chain.weight * self.type_processing.km_field
                                    * self.quantity_chains_m)
                                   + price_weight_all) * self.base_chain.rate)
                                 / self.quantity_chains_m * self.type_processing.margin)
                # цена за весь заказ
                self.price_full = self.price_1m * self.quantity_chains_m
                # цена за доставку рассчитанная по
                self.price_calc_weight = price_weight_all
                self.days = self.type_processing.days + 15 + self.type_delivery.days  # 15 дней на договор
                # Вычислить датУ доставки
                if self.days:
                    self.data_delivery = datetime.now().date() + timedelta(days=self.days)

                super().save(*args, **kwargs)
        else:
            # цена за доставку
            price_delivery = DeliveryRate.objects.filter(weight__gt=self.weight,
                             type_delivery_id=self.type_delivery).order_by('weight').first().price
            # цена за 1 кг
            self.price_1m = ((((self.base_chain.weight * self.type_processing.km_field
                                * self.quantity_chains_m) + price_delivery) * self.base_chain.rate)
                             / self.quantity_chains_m * self.type_processing.margin)
            # цена за весь заказ
            self.price_full = self.price_1m * self.quantity_chains_m
            self.price_calc_weight = price_delivery
            self.days = self.type_processing.days + 15 + self.type_delivery.days  # 15 дней на договор
            # Вычислить датУ доставки
            if self.days:
                self.data_delivery = datetime.now().date() + timedelta(days=self.days)

            super().save(*args, **kwargs)


# endregion
