from django.shortcuts import render
from django.http import HttpResponse
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
    active_enrollment_set = ActiveEnrollmentSet.objects.all()
    try:
        default_account = User.objects.get(username='study_admin')
    except User.DoesNotExist:
        return HttpResponse("If you're seeing this message, it's because " +
                            "the study_admin account doesn't exist -- " +
                            "probably because the initialize_data.yaml " +
                            "fixture hasn't been loaded.")
    if not admin_pwd_changed(default_account):
        return HttpResponse("Welcome to django_study_enrollment! This system has to be set up. Please log in to /admin as study_admin (password: \"study_admin\") and change the password.")
    if len(active_enrollment_set) != 1:
        return HttpResponse("Problem with database! Only one ActiveEnrollmentSet should exist.")
    enrollment_set = active_enrollment_set[0]

    if enrollment_set.use_req_list:
        requirements = get_requirements(enrollment_set)
        if not requirements:
            return HttpResponse("Study requirements haven't been designated for the enrollment system!")
        else:
            output = ', '.join([str(x) for x in requirements])
            return HttpResponse(output)
    else:
        return HttpResponse("Default page if not req list is being used.")

