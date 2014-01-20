from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, check_password
from study_enrollment.models import ActiveEnrollmentSet, Requirement

def admin_pwd_changed(default_account):
    # If the password matches "study_admin", it hasn't been changed.
    if check_password('study_admin', default_account.password):
        return False
    else:
        return True

def get_requirements(enrollment_set):
    if not enrollment_set.req_list:
        return []
    else:
        return Requirement.objects.filter(req_list=enrollment_set.req_list)


def index(request):
    try:
        default_account = User.objects.get(username='study_admin')
    except User.DoesNotExist:
        return HttpResponse("If you're seeing this message, it's because " +
                            "the study_admin account doesn't exist -- " +
                            "probably because the initialize_data.yaml " +
                            "fixture hasn't been loaded.")
    if not admin_pwd_changed(default_account):
        return render(request, 'study_enrollment/system_needs_set_up.html')
    active_enrollment_set = ActiveEnrollmentSet.objects.all()
    if len(active_enrollment_set) != 1:
        return HttpResponse("Problem with database! One and only one ActiveEnrollmentSet should exist.")
    return render(request, 'study_enrollment/index.html')

def requirements(request):
    active_enrollment_set = ActiveEnrollmentSet.objects.all()
    if len(active_enrollment_set) != 1:
        return HttpResponse("Problem with database! One and only one ActiveEnrollmentSet should exist.")
    enrollment_set = active_enrollment_set[0]
    if enrollment_set.use_req_list:
        requirements = get_requirements(enrollment_set)
    else:
        return HttpResponseRedirect('/start')
    if request.method == 'POST':
        failed_questions = []
        for req in requirements:
            req_choices = req.requirementchoice_set.all()
            choice = req.requirementchoice_set.get(answer=request.POST[req.question])
            if not choice.is_eligible:
                failed_questions.append({'requirement': req, 'choice': choice})
        if failed_questions:
            return render(request, 'study_enrollment/not_eligible.html', { 'reqs_failed': failed_questions })
        else:
            return HttpResponse("Page for entering email to start enrollment process.")
    else:
        requirements = get_requirements(enrollment_set)
        if not requirements:
            return render(request, 'study_enrollment/requirements_need_set_up.html')
        else:
            requirement_choices = [req.requirementchoice_set.all() for req in requirements]
            req_items = [ {'requirement': requirements[x],
                           'req_choices': requirement_choices[x]}
                          for x in range(len(requirements)) ]
            return render(request, 'study_enrollment/requirements.html',
                          { 'req_items': req_items } )

def start(request):
    # TODO: Make sure user can't just jump to this without going through
    # the requirements page (if used).
    return HttpResponse("Page for entering email to start enrollment process.")
