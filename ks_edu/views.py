from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from ks_crm import models
from ks_crm.forms import RegisterForm
import time


def index(request):
    news = models.News.objects.all().order_by("-id")[:4]
    actions = models.Actions.objects.all().order_by("-id")[:4]
    courses = models.Course.objects.all().order_by("-id")
    questions = models.FAQ.objects.all().order_by("-id")
    materials = models.TeacherMaterials.objects.all().order_by("-id")[:10]

    return render(request,"front_desk/index.html",{"news":news,
                                                   "actions":actions,
                                                   "courses":courses,
                                                   "questions":questions,
                                                   "materials":materials})

def acc_register(request):
    errors = {}
    user = request.user
    if user.is_authenticated():
        return redirect("/crm/")
    context = {}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            u_name, pwd, user_email = form.save()
            new_user = authenticate(email=user_email, password=pwd)
            login(request, new_user)
            # if user_email and key:
            #     success, msg = send_user_mail(user_email, key)
            #     context = {'activation_msg': msg}
            #     return my_render_to_response(
            #         'yaksh/activation_status.html', context
            #     )
            return redirect("/crm/")
        else:
            error_list = form.errors
            return render(request,'register.html',{"error_list":error_list})
    else:
        return render(request,'register.html')

def acc_login(request):
    errors = {}
    user = request.user
    if user.is_authenticated():
        return redirect("/crm/")
    if request.method == "POST":
        _email = request.POST.get("email")
        _password = request.POST.get("password")

        user = authenticate(username=_email,password=_password)
        if user:
            login(request,user)
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            else:
                return redirect("/crm/")
        else:
            errors['error'] = "Wrong username or password!"
    return render(request,"login.html",{"errors":errors})

def acc_logout(request):
    logout(request)
    return redirect("/account/login/")

def acc_password_resetting(request):
    obj = request.user
    errors = {}
    if request.method == "POST":
        _password1 = request.POST.get("password1")
        _password2 = request.POST.get("password2")

        if _password1 == _password2:
            if len(_password1) > 5:
                obj.set_password(_password1)
                obj.save()
                user = authenticate(username=request.user.email, password=_password1)
                if user:
                    login(request, user)
                    next_url = request.GET.get("next")
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect("/crm/")
            else:
                errors['password_too_short'] = "must be more than 6 letters"
        else:
            errors['invalid_password'] = "two password must be same"

    return render(request,"password_resetting.html",{"errors":errors})

def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')


# def permission_denied(request):
#     return render(request, '403.html')






