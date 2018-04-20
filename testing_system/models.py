from django.db import models
from ks_crm.models import UserProfile

# Create your models here.
class TestPaper(models.Model):
    paper_topic = models.CharField(max_length=64)
    recorded = models.ForeignKey("ks_crm.UserProfile")
    total_score = models.IntegerField()
    quiz_time = models.IntegerField()
    enabled = models.BooleanField()
    recorded_date = models.DateTimeField(auto_now_add=True)
    paper_type = models.ForeignKey("PaperType")
    memo = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.paper_topic

    class Meta:
        verbose_name = "试卷"
        verbose_name_plural = "试卷"

class PaperStruct(models.Model):
    paper_id = models.ForeignKey("TestPaper")
    big_title = models.CharField(max_length=64)
    ps_index = models.SmallIntegerField()
    question_type = models.ForeignKey("QuestionType",default=1)

    def __str__(self):
        return '%s-%s'%(self.paper_id,self.ps_index)

    class Meta:
        verbose_name = "试卷结构"
        verbose_name_plural = "试卷结构"

class QuestionLib(models.Model):
    ps_id = models.ForeignKey("PaperStruct")
    question_index = models.SmallIntegerField()
    question = models.TextField()
    choices = models.CharField(max_length=255,null=True,blank=True)
    answer = models.TextField()
    question_score = models.SmallIntegerField()

    def __str__(self):
        return '%s-%s'%(self.ps_id,self.question_index)

    class Meta:
        verbose_name = "题库"
        verbose_name_plural = "题库"

class AnswerPaper(models.Model):
    student = models.ForeignKey("ks_crm.UserProfile")
    test_paper = models.ForeignKey("TestPaper")
    score = models.IntegerField()
    time_consuming = models.IntegerField()
    test_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return "stu:%s(%s)"%(self.student,self.test_paper)

    class Meta:
        verbose_name = "测试结果"
        verbose_name_plural = "测试结果"

class StuAnswer(models.Model):
    answer_paper = models.ForeignKey("AnswerPaper")
    ps_index = models.SmallIntegerField()
    question_index = models.SmallIntegerField()
    answer = models.TextField()
    score = models.IntegerField()

    def __str__(self):
        return "%s(%s-%s)"%(self.test_paper.title,self.ps_index,self.question_index)

    class Meta:
        verbose_name = "答题卡"
        verbose_name_plural = "答题卡"

class PaperType(models.Model):
    type_name = models.CharField(max_length=32)

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = "试卷科目"
        verbose_name_plural = "试卷科目"


class QuestionType(models.Model):
    type_name = models.CharField(max_length=32)

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = "试题类型"
        verbose_name_plural = "试题类型"
