# Generated by Django 4.2.7 on 2023-12-10 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('delivery', '0018_calculation_price_calc_weight_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Страна')),
            ],
        ),
        migrations.RemoveField(
            model_name='client',
            name='address',
        ),
        migrations.RemoveField(
            model_name='client',
            name='note',
        ),
        migrations.RemoveField(
            model_name='contactclient',
            name='note',
        ),
        migrations.AddField(
            model_name='client',
            name='city',
            field=models.CharField(max_length=50, null=True, verbose_name='Город(нас. пункт)'),
        ),
        migrations.AddField(
            model_name='client',
            name='entrance',
            field=models.IntegerField(default=1, verbose_name='Подъезд'),
        ),
        migrations.AddField(
            model_name='client',
            name='floor',
            field=models.IntegerField(null=True, verbose_name='Этаж'),
        ),
        migrations.AddField(
            model_name='client',
            name='house_number',
            field=models.IntegerField(null=True, verbose_name='№ дома'),
        ),
        migrations.AddField(
            model_name='client',
            name='office',
            field=models.IntegerField(null=True, verbose_name='Офис'),
        ),
        migrations.AddField(
            model_name='client',
            name='quarter',
            field=models.IntegerField(null=True, verbose_name='Квартал'),
        ),
        migrations.AddField(
            model_name='client',
            name='region',
            field=models.CharField(max_length=50, null=True, verbose_name='Регион(область)'),
        ),
        migrations.AddField(
            model_name='client',
            name='street',
            field=models.CharField(max_length=50, null=True, verbose_name='Улица(проспект)'),
        ),
        migrations.AlterField(
            model_name='calculation',
            name='base_chain',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='delivery.basechain', verbose_name='Базовая цепь'),
        ),
        migrations.AlterField(
            model_name='calculation',
            name='client',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='delivery.client', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='calculation',
            name='type_delivery',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='delivery.typedelivery', verbose_name='Тип доставки'),
        ),
        migrations.AlterField(
            model_name='calculation',
            name='type_processing',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='delivery.othervariant', verbose_name='Тип обработки'),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(default=None, max_length=254, verbose_name='ЕМЕЙЛ'),
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='client',
            name='unp',
            field=models.CharField(max_length=100, verbose_name='УНП'),
        ),
        migrations.AlterField(
            model_name='client',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Менеджер'),
        ),
        migrations.AlterField(
            model_name='contactclient',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='delivery.client'),
        ),
        migrations.AddField(
            model_name='client',
            name='country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='delivery.country', verbose_name='Страна'),
        ),
    ]