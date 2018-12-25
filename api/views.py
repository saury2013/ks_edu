import simplejson as json
from django.shortcuts import HttpResponse
from django.contrib.auth import login,authenticate,logout
from ks_crm import models

# Create your views here.
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

def course_list_api(request):
    course_list = models.Course.objects.all()
    courses = []
    for _course in course_list:
        course = {}d
        course['name'] = _course.name
        course['price'] = _course.price
        course['period'] = _course.period
        course['outline'] = _course.outline
        courses.append(course)
    return HttpResponse(json.dumps(courses), content_type="application/json")

def acc_login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        passwd = request.POST.get('passwd')
        user = authenticate(username=phone, password=passwd)
        if user:
            login(request, user)
            ss = request.session
            print(ss)
            return HttpResponse(json.dumps(ss), content_type="application/json")
    return HttpResponse(json.dumps({"is_active":False }), content_type="application/json")

