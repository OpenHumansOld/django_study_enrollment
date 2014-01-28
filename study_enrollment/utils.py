from study_enrollment.settings import IS_ELIGIBLE_FLAG
from study_enrollment.models import ActiveEnrollmentSet, UserEnrollment


def transfer_eligibility_info(request):
    if request.user.is_authenticated():
        user_enrollment, _ = UserEnrollment.objects.get_or_create(user=request.user)
        if request.session.get(IS_ELIGIBLE_FLAG):
            user_enrollment.is_eligible = True
            user_enrollment.save()
            del request.session[IS_ELIGIBLE_FLAG]


def requirements_needed(request):
    active_enrollment_set = ActiveEnrollmentSet.objects.all()[0]
    if not active_enrollment_set.use_req_list:
        return False
    if request.user.is_authenticated():
        user_enrollment, _ = UserEnrollment.objects.get_or_create(user=request.user)
        transfer_eligibility_info(request)
        user_enrollment.save()
        print user_enrollment.is_eligible
        return not user_enrollment.is_eligible
    if request.session.get(IS_ELIGIBLE_FLAG):
        return False
    return True
