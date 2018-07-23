from django.shortcuts import render,HttpResponse,redirect
from testing_system.models import TestPaper
from ks_crm.models import Actions,News,Course,UserProfile,FAQ
from datetime import datetime
from ks_crm.forms import ProfileForm

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
        temp_file_path = os.path.join(settings.MEDIA_ROOT, 'head_imgs')
        if not os.path.exists(temp_file_path):
            os.makedirs(temp_file_path, exist_ok=True)
        filename = ""
        for k, file_obj in request.FILES.items():
            filename = request.POST.get("filename")
            # print("filename",filename)
            filepath = "%s/%s" % (temp_file_path, filename)
            with open(filepath, "wb") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
        head_img_url = "/head_imgs/" + filename
        old_img_url = request.user.head_img
        UserProfile.objects.filter(id=request.user.id).update( head_img = head_img_url)
        if old_img_url.url != '/media/head_imgs/sample.jpg':
            root_path = settings.MEDIA_ROOT.replace('\\','/')
            os.remove(os.path.join(root_path+str(old_img_url)))
        return HttpResponse(head_img_url)

    return HttpResponse("ok")

def profile_modify(request):
    user_info = UserProfile.objects.profile_info_list(id=request.user.id)
    # print("user list:",user_info)
    form = ProfileForm(user_info)
    course_list = Course.objects.filter(enabled=True)
    if request.method == "POST":
        form = ProfileForm(request.POST)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            print(form.cleaned_data['email'])
            user_obj = UserProfile.objects.filter(id=request.user.id)
            print(user_obj)
            print(request.POST.get("degree"),request.POST.get("ismakeup"))
            user_obj.update(
                name = form.cleaned_data["name"],
                nickname = form.cleaned_data["nickname"],
                stu_num = form.cleaned_data["stu_num"],
                grade = form.cleaned_data["grade"],
                degree = form.cleaned_data["degree"],
                isteacher = form.cleaned_data["isteacher"],
                ismakeup = form.cleaned_data["ismakeup"],
                gender = form.cleaned_data["gender"],
                profession = form.cleaned_data["profession"],
                signature = form.cleaned_data["signature"],
                address = form.cleaned_data["address"],
                hobbies = form.cleaned_data["hobbies"],
                phone = form.cleaned_data["phone"],
                ID_num = form.cleaned_data["ID_num"],
            )
            return redirect("/crm")
            # course = Course.objects.get(name=request.POST.get("course"))
            # course_list = request.POST.getlist("course")
            # _user_obj = UserProfile.objects.get(id=request.user.id)
            # for course_id in course_list:
            #     course = Course.objects.get(id=course_id)
            #     print("_user_obj.course:",_user_obj.course.all())
            #     _user_obj.course.add(course)
            # print(request.POST.getlist("course"))

    return render(request,'ks_crm/profile_editors.html',{"course_list":course_list,"form":form})

def skin_config(request):
    return render(request, "ks_crm/skin-config.html")

def test2(request):
    return render(request,'ks_crm/test2.html')
