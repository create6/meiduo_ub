# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-06-10 06:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('trade_id', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='支付宝流水号')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.OrderInfo', verbose_name='美多订单号')),
            ],
            options={
                'db_table': 'tb_payment',
            },
        ),
    ]
