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
        if not requirements:
            return render(request, 'study_enrollment/requirements_need_set_up.html')
        else:
            output = ', '.join([str(x) for x in requirements])
            return HttpResponse(output)
    else:
        return HttpResponseRedirect('/start')

def start(request):
    return HttpResponse("Page for entering email to start enrollment process.")
