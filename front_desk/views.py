from django.shortcuts import render
from ks_crm import models

# Create your views here.

def news(request,news_id):
    news_obj = models.News.objects.get(id=news_id)
    return render(request,"front_desk/article.html",{"news_obj":news_obj})
def actions(request,action_id):
    action = models.Actions.objects.get(id=action_id)
    print(action.topic,action.content)
    return render(request,"front_desk/actions.html",{"action":action})
def news_list(request):
    news_list = models.News.objects.all()
    return render(request, "front_desk/news_list.html", {"news_list": news_list})

def action_list(request):
    action_list = models.Actions.objects.all()
    return render(request, "front_desk/action_list.html", {"action_list": action_list})

def course_list(request):
    course_list = models.Course.objects.all()
    return render(request, "front_desk/course_list.html", {"course_list": course_list})

def material_list(request):
    material_list = models.TeacherMaterials.objects.all()
    return render(request, "front_desk/material_list.html", {"material_list": material_list})