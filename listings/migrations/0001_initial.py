# Generated by Django 3.2.24 on 2024-02-11 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(blank=True, null=True)),
                ('display_name', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=False)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lng', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('pin_code', models.CharField(default='', max_length=10)),
                ('address', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bedrooms', models.IntegerField()),
                ('bathrooms', models.IntegerField()),
                ('area', models.DecimalField(decimal_places=2, max_digits=10)),
                ('property_type', models.CharField(choices=[('apartment', 'Apartment'), ('house', 'House'), ('land', 'Land'), ('commercial', 'Commercial'), ('other', 'Other')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.city')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=500)),
                ('label', models.CharField(choices=[('front', 'Front View'), ('back', 'Back View'), ('bedroom', 'Bedroom'), ('kitchen', 'Kitchen'), ('living_room', 'Living Room'), ('bathroom', 'Bathroom'), ('others', 'Others')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='listings.property')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.location'),
        ),
    ]
