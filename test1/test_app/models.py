from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    # 多个choice对应一个question
    question = models.ForeignKey(Question, on_delete=models.CASCADE,verbose_name='question is')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

