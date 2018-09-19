# -*- coding: utf-8 -*-
__author__ = 'Allen'

from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta
from django.core.exceptions import FieldDoesNotExist

register = template.Library()

@register.simple_tag
def render_question_choice(question_obj):

    ele = "<div class='question-choice'>"
    choices = question_obj.choices
    pid = question_obj.ps_id.ps_index
    q_index = question_obj.question_index
    qid = question_obj.id
    choice_name = "%s-%s-%s"%(pid,q_index,qid)
    print('choice_name',choice_name)
    choices_splited = choices.split("/")
    # print(choices.split("/"))

    if len(choices_splited) > 3:
        i = 1
        for choice in choices_splited:
            print(choice)
            if question_obj.ps_id.question_type.id == 2:
                op = "<div class='choice_box' style='margin-left: 40px'><input type='{}' value='{}' name='{}'>{}</div>".format('checkbox', chr(64+i), choice_name,choice.strip())
            else:
                op = "<div class='choice_box' style='margin-left: 40px'><input type='{}' value='{}' name='{}'>{}</div>".format('radio', chr(64+i), choice_name,choice.strip())
            i += 1
            ele += op
    else:
        ele += "<div class='choice_box' style='margin-left: 40px'><input type='radio' value='对' name='%s'>对</div> <div class='choice_box' style='margin-left: 40px'><input type='radio' value='错' name='%s'>错</div>" %(choice_name,choice_name)
    end_ele = '</div><div class="question-choice-answer" style="margin-left: 40px;padding-top: 10px">你的回答：<span id="{}" class="my-answer"></span></div>'.format(choice_name)

    return mark_safe(ele+end_ele)

@register.simple_tag
def render_question(question_obj):
    question_header = question_obj.question
    question_splited = question_header.split("/")
    column_num = len(question_splited)
    question_str = question_splited[0] + "&nbsp;[" + str(question_obj.question_score) + "]"
    i = 1
    while column_num > 1:
        sstr = "<br>&nbsp;" + question_splited[i]
        question_str += sstr
        column_num -= 1
        i += 1
    return mark_safe(question_str)