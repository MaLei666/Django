# Generated by Django 2.0.6 on 2018-12-19 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider_data', '0011_auto_20181210_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopId', models.CharField(max_length=100, verbose_name='店铺id')),
                ('shopName', models.CharField(max_length=100, verbose_name='店铺名称')),
                ('review', models.CharField(blank=True, max_length=3000, null=True, verbose_name='评论')),
                ('review_recommend', models.CharField(blank=True, max_length=300, null=True, verbose_name='推荐菜')),
                ('review_time', models.DateTimeField(blank=True, max_length=300, null=True, verbose_name='评论时间')),
                ('update_time', models.DateTimeField(blank=True, max_length=300, null=True, verbose_name='更新时间')),
                ('now_page', models.IntegerField(verbose_name='页码')),
                ('re_no', models.IntegerField(verbose_name='索引')),
            ],
            options={
                'verbose_name': '大众点评店铺评论列表',
                'verbose_name_plural': '大众点评店铺评论列表',
            },
        ),
        migrations.RenameField(
            model_name='foodrank',
            old_name='rank',
            new_name='rank_num',
        ),
    ]