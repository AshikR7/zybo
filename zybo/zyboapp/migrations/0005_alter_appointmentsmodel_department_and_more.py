# Generated by Django 4.2.3 on 2023-08-02 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zyboapp', '0004_rename_name_departmentmodel_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentsmodel',
            name='department',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='appointmentsmodel',
            name='doctor',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='doctormodel',
            name='department',
            field=models.CharField(max_length=30),
        ),
    ]