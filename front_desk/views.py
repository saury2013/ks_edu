from django.shortcuts import render,HttpResponse
from django.core import serializers
import simplejson as json
from ks_crm import models

# Create your views here.

def news(request,news_id):
    news_obj = models.News.objects.get(id=news_id)
    comment_list = news_obj.comment_set.select_related().all()
    return render(request,"front_desk/article.html",{"news_obj":news_obj,'comment_list':comment_list})
def actions(request,action_id):
    action = models.Actions.objects.get(id=action_id)
    print(action.topic,action.content)
    return render(request,"front_desk/actions.html",{"action":action})
def news_list(request):
    news_list = models.News.objects.all()
    return render(request, "front_desk/news_list.html", {"news_list": news_list})

def news_list_api(request):
    news_list = models.News.objects.all()
    res = []
    for _news in news_list:
        news = {}
        news['img'] = _news.image.url if _news.image else ''
        news['title'] = _news.title
        news['duration'] = _news.content
        news['date'] = _news.date.strftime('%Y-%m-%d')
        res.append(news)
    return HttpResponse(json.dumps(res), content_type="application/json")

def action_list(request):
    action_list = models.Actions.objects.all()
    return render(request, "front_desk/action_list.html", {"action_list": action_list})

def action_list_api(request):
    action_list = models.Actions.objects.all()
    res = []
    for _action in action_list:
        action = {}
        action['img'] = _action.image.url
        action['title'] = _action.topic
        action['duration'] = '%s-%s'%(_action.start_time,_action.end_time)
        action['date'] = _action.date.strftime('%Y-%m-%d')
        action['favourites'] = _action.favourites if _action.favourites else 0
        res.append(action)
    return HttpResponse(json.dumps(res), content_type="application/json")

def course_list(request):
    course_list = models.Course.objects.all()
    return render(request, "front_desk/course_list.html", {"course_list": course_list})

def course_list_api(request):
    course_list = models.Course.objects.all()
    courses = []
    for _course in course_list:
        course = {}
        course['name'] = _course.name
        course['price'] = _course.price
        course['period'] = _course.period
        course['outline'] = _course.outline
        courses.append(course)
    return HttpResponse(json.dumps(courses), content_type="application/json")

def material_list(request):
    material_list = models.TeacherMaterials.objects.all()
    return render(request, "front_desk/material_list.html", {"material_list": material_list})

def comment(request):

    print(request.POST)
    if request.method == 'POST':
        new_comment_obj = models.Comment(
            article_id=request.POST.get('article_id'),
            user_id=request.user.id,
            comment = request.POST.get('comment')
        )
        new_comment_obj.save()

    return HttpResponse("ok")

