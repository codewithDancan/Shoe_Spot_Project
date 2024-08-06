# Generated by Django 5.0.7 on 2024-08-06 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('FlutterWave', 'FlutterWave'), ('Card', 'Card')], default='FlutterWave', max_length=50),
        ),
    ]
