from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userAccount', '0002_auto_20201023_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availability', to='userAccount.useraccount', unique=True),
        ),
    ]