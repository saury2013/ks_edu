from django.shortcuts import render,HttpResponse
from testing_system.models import TestPaper
from ks_crm.models import Actions,News,Course,UserProfile,FAQ
from datetime import datetime

# Create your views here.

def index(request):
    action_list = Actions.objects.all()[:4]
    return render(request,'ks_crm/index.html',{"action_list":action_list})

def stu_index(request):
    course_list = request.user.course.all()
    print("course_list:",course_list)
    return render(request, 'ks_crm/stu_index.html',{"course_list":course_list})

def testing_system(request):
    papaer_list = TestPaper.objects.all()
    return render(request, 'ks_crm/testing_system.html',{'papaer_list':papaer_list})

def lesson_video(request):
    return render(request, 'ks_crm/video.html')

def add_news(request):
    if request.method == 'POST':
        news_obj = News(
            title=request.POST.get("title"),
            enabled=request.POST.get("enabled"),
            content=request.POST.get("content"),
        )
        news_obj.save()
    return render(request, 'ks_crm/news_editors.html')

def add_action(request):
    if request.method == 'POST':
        action_obj = Actions(
            topic=request.POST.get("topic"),
            start_time=datetime.strptime(request.POST.get("start_time"), "%Y-%m-%d"),
            end_time=datetime.strptime(request.POST.get("end_time"), "%Y-%m-%d"),
            enabled=request.POST.get("enabled"),
            content=request.POST.get("content"),
        )
        action_obj.save()

    return render(request, 'ks_crm/action_editors.html')

def add_FAQ(request):
    faq_list = FAQ.objects.all()
    if request.method == "POST":
        faq_obj = FAQ(
            question=request.POST.get("question"),
            answer=request.POST.get("answer")
        )
        faq_obj.save()
    return render(request, 'ks_crm/faq.html',{"faq_list":faq_list})

def add_course(request):
    if request.method == 'POST':
        course_obj = Course(
            name=request.POST.get("name"),
            period=request.POST.get("period"),
            price=request.POST.get("price"),
            enabled=request.POST.get("enabled"),
            outline=request.POST.get("outline"),
        )
        course_obj.save()
    return render(request, 'ks_crm/course_editors.html')

from ks_edu import settings
import os

def image_upload(request,url_type):
    print(url_type)
    if url_type == 'action':

        temp_file_path = os.path.join(settings.MEDIA_ROOT, 'action_images')
        if not os.path.exists(temp_file_path):
            os.makedirs(temp_file_path, exist_ok=True)
        filename = ""
        for k, file_obj in request.FILES.items():
            filename = file_obj.name
            filepath = "%s/%s" % (temp_file_path, file_obj.name)
            with open(filepath, "wb") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
        return HttpResponse("/media/action_images/"+filename)
    elif url_type == 'head_img':
        print(request.FILES)
        temp_file_path = os.path.join(settings.MEDIA_ROOT, 'head_imgs')
        if not os.path.exists(temp_file_path):
            os.makedirs(temp_file_path, exist_ok=True)
        filename = ""
        for k, file_obj in request.FILES.items():
            filename = request.POST.get("filename")
            print("filename",filename)
            filepath = "%s/%s" % (temp_file_path, filename)
            with open(filepath, "wb") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
        head_img_url = "/media/head_imgs/" + filename
        UserProfile.objects.filter(id=request.user.id).update( head_img = head_img_url)
        return HttpResponse(head_img_url)

    return HttpResponse("ok")

def profile_modify(request):
    course_list = Course.objects.filter(enabled=True)
    if request.method == "POST":
        user_obj = UserProfile.objects.filter(id=request.user.id)
        print(user_obj)
        user_obj.update(
            name = request.POST.get("name"),
            phone = request.POST.get("phone"),
            address = request.POST.get("address"),
            hobbies = request.POST.get("hobbies"),
            signature = request.POST.get("signature"),
        )
        # course = Course.objects.get(name=request.POST.get("course"))
        course_list = request.POST.getlist("course")
        _user_obj = UserProfile.objects.get(id=request.user.id)
        for course_id in course_list:
            course = Course.objects.get(id=course_id)
            print("_user_obj.course:",_user_obj.course.all())
            _user_obj.course.add(course)
        print(request.POST.getlist("course"))


    return render(request,'ks_crm/profile_editors.html',{"course_list":course_list})

def skin_config(request):
    return render(request, "ks_crm/skin-config.html")

def test2(request):
    return render(request,'ks_crm/test2.html')