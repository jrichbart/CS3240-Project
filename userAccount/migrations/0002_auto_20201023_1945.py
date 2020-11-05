from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userAccount', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='userAccount.useraccount'),
        ),
    ]