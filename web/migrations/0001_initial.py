# Generated by Django 3.0.2 on 2020-03-26 14:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('level', models.CharField(choices=[('National', 'Federal / National level'), ('Emirate', 'Emirate level (Abu Dhabi, Dubai, Sharjah, etc)'), ('Other', 'Other level')], default='Other', max_length=255)),
                ('sector', models.CharField(choices=[('Energy, Utilities, Agriculture', 'Energy, Utilities, Agriculture'), ('Safety and Security', 'Safety and Security'), ('Defense and Intelligence', 'Defense and Intelligence'), ('ICT', 'ICT'), ('Transportation', 'Transportation'), ('Government Administration', 'Government Administration'), ('Education', 'Education'), ('Media, Entertainment', 'Media, Entertainment'), ('Finance and Economy', 'Finance and Economy'), ('Special', 'Special'), ('Healthcare', 'Healthcare'), ('Manufacturing, Construction', 'Manufacturing, Construction'), ('Other', 'Other')], default='Other', max_length=255)),
                ('tier', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('type', models.CharField(choices=[('domain', 'domain'), ('ipv4', 'ipv4'), ('range4', 'range4'), ('netmask4', 'netmask4'), ('cidr4', 'cidr4'), ('ipv6', 'ipv6'), ('range6', 'range6'), ('cidr6', 'cidr6')], max_length=255)),
                ('start_ip', models.UUIDField(blank=True, null=True)),
                ('end_ip', models.UUIDField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='web.Org')),
            ],
        ),
    ]
