from django.shortcuts import render,HttpResponse
from testing_system.models import PaperStruct,TestPaper,AnswerPaper,QuestionLib,PaperType,QuestionType,StuAnswer
from ks_crm.models import UserProfile
import os
import datetime
import json
from testing_system.excel_handler import excel_table_byname
from testing_system.text_match_handler import similarity_analysis


# Create your views here.

def tp_handler(paper_id):
    paper_struct = PaperStruct.objects.filter(paper_id=paper_id).order_by('ps_index')
    question_dict = {}
    for ps in paper_struct:
        question_dict[ps.big_title] = QuestionLib.objects.filter(ps_id=ps.id).order_by('question_index')
    return question_dict

def test_paper(request,paper_id):
    paper_obj = TestPaper.objects.filter(id=paper_id)[0]
    question_dict = tp_handler(paper_id)
    # print(paper_obj.paper_topic)
    return render(request,'testing_system/test_paper.html',{'paper_obj':paper_obj,'question_dict':question_dict})

def upload_test_paper(request):

    paper_types = PaperType.objects.all()

    if request.method == 'POST':

        if request.is_ajax():
            print("ajax post", request.FILES)
            from ks_edu import settings
            temp_file_path = os.path.join(settings.BASE_DIR, 'temp_upload')
            if not os.path.exists(temp_file_path):
                os.makedirs(temp_file_path, exist_ok=True)
            filename = ""
            for k, file_obj in request.FILES.items():
                filename = file_obj.name
                with open("%s/%s" % (temp_file_path, file_obj.name), "wb") as f:
                    for chunk in file_obj.chunks():
                        f.write(chunk)
            return HttpResponse(filename)


    return render(request,'testing_system/new_test_paper.html',{'paper_types':paper_types})

def save_test_paper(request):
    if request.method == 'POST':
        user_obj = UserProfile.objects.get(id=request.user.id)
        tp_obj = TestPaper(
            paper_topic=request.POST.get("paper_topic"),
            paper_type = PaperType.objects.get(type_name=request.POST.get("paper_type")),
            total_score = request.POST.get("total_score"),
            quiz_time = request.POST.get("quiz_time"),
            enabled = request.POST.get("enabled"),
            recorded=user_obj
        )
        tp_obj.save()

        filename = request.POST.get("up_filename")
        from ks_edu import settings
        file_path = os.path.join(settings.BASE_DIR,'temp_upload',filename)
        tables = excel_table_byname(file_path)
        pre_ps_index = 0
        _ps_id = 0
        for row in tables:
            print(row)
            _ps_index = int(row['ps_index'])
            if pre_ps_index != _ps_index:
                _big_title = row['big_title']
                ps_obj = PaperStruct(
                    paper_id=tp_obj,
                    ps_index=_ps_index,
                    question_type=QuestionType.objects.get(type_name=row['question_type']),
                    big_title=_big_title
                )
                ps_obj.save()
                pre_ps_index = _ps_index

            question_obj = QuestionLib(ps_id=ps_obj,
                                    question_index=int(row['question_index']),
                                    question = row['question'],
                                    choices = row['choices'],
                                    answer = row['answer'],
                                    question_score = int(row['question_score'])
            )
            question_obj.save()

        os.remove(file_path)

    return render(request,'testing_system/new_test_paper.html')

def check_answer(request):
    if request.is_ajax():
        stu_anwer = json.loads(request.body)
        print(stu_anwer)
        data = {}
        total_score = 0
        answer_list = []
        answer_paper_obj = AnswerPaper(
            student = request.user,
            test_paper = TestPaper.objects.get(id=stu_anwer['test_paper']),
            score = 0,
            time_consuming = stu_anwer['time_consuming'],
        )
        answer_paper_obj.save()
        for sub_stu_anwer in stu_anwer['stu_answer']:
            qid = sub_stu_anwer['qid']
            question_obj = QuestionLib.objects.get(id=qid)
            standard_answer = question_obj.answer
            if int(question_obj.ps_id.question_type.id) > 3:
                result_score = grade_test(question_obj,sub_stu_anwer['answer'])
            else:
                import difflib
                if difflib.SequenceMatcher(None, sub_stu_anwer['answer'], question_obj.answer).quick_ratio() == 1:
                    result_score = int(question_obj.question_score)
                else:
                    result_score = 0
            print("%s-%s-%s"%(sub_stu_anwer['ps_index'],sub_stu_anwer['question_index'],result_score))
            answer_dict = {}
            answer_dict['standard_answer'] = standard_answer
            answer_dict['result_score'] = result_score
            total_score += result_score
            answer_list.append(answer_dict)
            stu_anwer_obj = StuAnswer(
                answer_paper = answer_paper_obj,
                ps_index = sub_stu_anwer['ps_index'],
                question_index = sub_stu_anwer['question_index'],
                answer = sub_stu_anwer['answer'],
                score = result_score
            )
            stu_anwer_obj.save()

        data['answer_list'] = answer_list
        data['total_score'] = total_score
        AnswerPaper.objects.filter(id=answer_paper_obj.id).update(score=total_score)
    return HttpResponse(json.dumps(data))

def grade_test(question_obj,answer):
    standard_answer = question_obj.answer
    score = question_obj.question_score
    match_rate = float(similarity_analysis(standard_answer,answer))
    print(match_rate)
    #打分规则：
    #如果回答与标准答案匹配都在0.4以上才算有效答案
    #有效答案的匹配度低于0.7则再加0.1的匹配度，高于0.7则算全对
    if match_rate > 0.4:
        answer_score = score * round(match_rate+0.1 if match_rate<0.7 else 1.0, 2)
    else:
        answer_score = 0

    return int(answer_score)