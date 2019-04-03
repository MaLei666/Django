# Generated by Django 2.0.6 on 2019-04-03 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys_inspect', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspectdevinfo',
            name='create_time',
            field=models.DateTimeField(auto_now=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='inspectdevinfo',
            name='dept_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='部门ID'),
        ),
        migrations.AlterField(
            model_name='inspectdevinfo',
            name='last_task_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='最后任务ID'),
        ),
        migrations.AlterField(
            model_name='inspectdevinfo',
            name='last_user_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='最后修改者ID'),
        ),
        migrations.AlterField(
            model_name='inspectdevinfo',
            name='prev_task_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='之前任务ID'),
        ),
        migrations.AlterField(
            model_name='inspectdevinfo',
            name='prev_user_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='之前修改者ID'),
        ),
        migrations.AlterField(
            model_name='inspectdevinfo',
            name='unit_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='部门ID'),
        ),
    ]
