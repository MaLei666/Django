from django.db import models
from users.models import UserProfile

class DataList(models.Model):
    # id = models.AutoField(primary_key= True)
    question=models.CharField(verbose_name='问题标题', max_length=30)
    hot=models.CharField(verbose_name='问题热度', max_length=30)
    answer_count=models.IntegerField(verbose_name='回答数')


    class Meta:
        verbose_name = '知乎问题表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.question

class DataInfo(models.Model):

    question=models.ForeignKey(DataList,to_field='id',verbose_name='问题标题',on_delete=models.CASCADE)
    # question_text=models.CharField(verbose_name='问题标题',max_length=300)
    text=models.CharField(verbose_name='回答内容', max_length=3000)
    author=models.CharField(verbose_name='回答作者', max_length=30)
    voteup_count=models.IntegerField(verbose_name='赞同数量', )
    comment_count=models.IntegerField(verbose_name='评论数量', )
    update_time=models.DateTimeField(verbose_name='更新时间', max_length=30)

    class Meta:
        verbose_name = '回答详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.text