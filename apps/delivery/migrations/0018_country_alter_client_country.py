# Generated by Django 4.2.7 on 2023-12-08 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0017_remove_client_address_remove_contactclient_note_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Страна')),
            ],
        ),
        migrations.AlterField(
            model_name='client',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.country', verbose_name='Страна'),
        ),
    ]
