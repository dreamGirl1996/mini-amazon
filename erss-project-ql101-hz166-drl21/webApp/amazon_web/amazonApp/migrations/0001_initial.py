# Generated by Django 3.0.5 on 2020-04-25 02:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AmazonProduct',
            fields=[
                ('prod_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(help_text='Product name', max_length=50, null=True)),
                ('product_desc', models.CharField(blank=True, help_text='Product description', max_length=50, null=True)),
            ],
            options={
                'ordering': ['product_name'],
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('wh_id', models.AutoField(primary_key=True, serialize=False)),
                ('wh_x', models.IntegerField(help_text='Warehouse address X', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(360)])),
                ('wh_y', models.IntegerField(help_text='Warehouse_address Y', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(360)])),
            ],
        ),
        migrations.CreateModel(
            name='WarehouseContents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_quantity', models.IntegerField(default=1, help_text='Quantity', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('prod_id', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='amazonApp.AmazonProduct')),
                ('wh_id', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='warehouse', to='amazonApp.Warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('ship_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(help_text='Product name', max_length=50, null=True)),
                ('ups_id', models.CharField(blank=True, help_text='Ups account', max_length=30, null=True)),
                ('truck_id', models.IntegerField(blank=True, help_text='truck this shipment goes on', null=True)),
                ('buyer_x', models.IntegerField(help_text='User address X', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(360)])),
                ('buyer_y', models.IntegerField(help_text='User address Y', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(360)])),
                ('order_created_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='Order created time', null=True)),
                ('product_num', models.IntegerField(default=1, help_text='How many products you want to buy?', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('status', models.CharField(choices=[('await_valid', 'await_valid'), ('val_req_sent', 'val_req_sent'), ('invalid', 'invalid'), ('pending', 'pending'), ('to pack', 'to pack'), ('ready', 'ready'), ('request_pickup', 'request_pickup'), ('request_noted', 'request_noted'), ('load', 'load'), ('loaded', 'loaded'), ('delivering', 'delivering'), ('delivered', 'delivered')], default='pending', help_text='Order status', max_length=20)),
                ('packed_wh', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='packed_wh', to='amazonApp.Warehouse')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AmazonUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ups_name', models.IntegerField(blank=True, help_text='Ups username', null=True)),
                ('ups_pass', models.CharField(blank=True, help_text='Ups password', max_length=50, null=True)),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
