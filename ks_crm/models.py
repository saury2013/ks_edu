from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=256,verbose_name="新闻标题")
    content = models.TextField(verbose_name="新闻内容")
    image = models.FileField(upload_to='news_image',null=True,blank=True)
    enabled = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['date']
        verbose_name = "新闻资讯"
        verbose_name_plural = "新闻资讯"

class Actions(models.Model):
    topic = models.CharField(max_length=256, verbose_name="活动主题")
    content = models.TextField(verbose_name="活动内容")
    start_time = models.DateField()
    end_time = models.DateField()
    image = models.FileField(upload_to='action_image')
    date = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=True)
    favourites = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "最新活动"
        verbose_name_plural = "最新活动"

class TeacherMaterials(models.Model):
    title = models.CharField(max_length=256, verbose_name="资料标题")
    intro = models.TextField(verbose_name="资料简介")
    file_path = models.FileField(upload_to='teacher_materials')
    date = models.DateTimeField(auto_now_add=True)
    download_amount = models.IntegerField(blank=True,null=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "讲义资料"
        verbose_name_plural = "讲义资料"

class FAQ(models.Model):
    question = models.TextField(verbose_name="常见问题")
    answer = models.TextField(verbose_name="回答")
    weight = models.SmallIntegerField(default=1,verbose_name="权重")
    useful =  models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "常见问题"
        verbose_name_plural = "常见问题"

class Course(models.Model):
    name = models.CharField(max_length=64, unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name="周期(月)")
    outline = models.TextField()
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程表"
        verbose_name_plural = "课程表"

class Branch(models.Model):
    '''校区'''
    name = models.CharField(max_length=128,unique=True)
    addr = models.CharField(max_length=128)
    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "校区"
        verbose_name_plural = "校区"


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        self.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self,email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user

    def profile_info_list(self,id):
        user = self.get(id=id)
        res = {key:value for key,value in user.__dict__.items() if not key.startswith('_')}
        res["course"] = [course.id for course in user.course.all()]
        res["role"] = user.role.name
        res["password"] = user.password
        return res

class UserProfile(AbstractBaseUser,PermissionsMixin):
    '''账号表'''
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    password = models.CharField(_('password'), max_length=128, help_text=mark_safe('''<a href='password/'>修改密码</a>'''))
    true_name = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    stu_num = models.IntegerField(blank=True, null=True)
    grade = models.CharField(max_length=32, default="")
    profession = models.CharField(max_length=32, blank=True, null=True)
    ID_num = models.IntegerField(blank=True, null=True)
    degree_choices = (('0', '专科'), ('1', '本科'))
    degree = models.SmallIntegerField(choices=degree_choices, default=0)
    gender_choices = (('0', '男'), ('1', '女'))
    gender = models.SmallIntegerField(choices=gender_choices, default=0)
    isno_choices = (('0', '是'), ('1', '否'))
    isteacher = models.SmallIntegerField(choices=isno_choices, default=0)
    ismakeup = models.SmallIntegerField(choices=isno_choices, default=0)
    role = models.ForeignKey("Role", blank=True, null=True,default=1)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    signature = models.CharField(max_length=255, blank=True, null=True)
    head_img = models.ImageField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    hobbies = models.CharField(max_length=255, blank=True, null=True)
    course = models.ManyToManyField("Course", blank=True)
    friends = models.ManyToManyField("self", blank=True)


    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return str(self.name)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_active

class Role(models.Model):
    '''角色表'''
    name = models.CharField(max_length=32,unique=True)
    menus = models.ManyToManyField("Menu",blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "角色"
        verbose_name_plural = "角色"

class Menu(models.Model):
    '''菜单'''
    name = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64)
    url_type_choices = ((0, 'alias'), (1, 'absolute_url'))
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0)
    icon = models.CharField(max_length=32,default="fa-flask")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "菜单"
        verbose_name_plural = "菜单"

class Comment(models.Model):
    article = models.ForeignKey("News",verbose_name=u"所属文章")
    user = models.ForeignKey("UserProfile")
    comment = models.TextField(null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "%s,%s" %(self.article,self.comment)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"

