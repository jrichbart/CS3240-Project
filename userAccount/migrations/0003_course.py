# Generated by Django 3.2 on 2020-10-21 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userAccount', '0002_alter_useraccount_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mnemonic', models.CharField(max_length=4)),
                ('number', models.CharField(max_length=4)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userAccount.useraccount')),
            ],
        ),
    ]
