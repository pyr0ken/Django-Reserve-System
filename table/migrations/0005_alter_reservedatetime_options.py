# Generated by Django 4.2.1 on 2023-06-02 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0004_alter_reservedatetime_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reservedatetime',
            options={'ordering': ['id'], 'verbose_name': 'روز رزرو', 'verbose_name_plural': 'روز های رزرو'},
        ),
    ]
