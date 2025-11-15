from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='turma',
            field=models.CharField(max_length=50, null=True, blank=True, verbose_name='Turma'),
        ),
    ]
