from django.contrib import admin
from testing_system import models

# Register your models here.

admin.site.register(models.TestPaper)
admin.site.register(models.PaperStruct)
admin.site.register(models.QuestionLib)
admin.site.register(models.AnswerPaper)
admin.site.register(models.PaperType)
admin.site.register(models.QuestionType)