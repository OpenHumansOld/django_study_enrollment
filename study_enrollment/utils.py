from study_enrollment.settings import IS_ELIGIBLE_FLAG
from study_enrollment.models import ActiveEnrollmentSet, UserEnrollment


def transfer_eligibility_info(request):
    """
    If User is logged in and has session IS_ELIGIBLE_FLAG indicating requirements
    have been passed, store this more permanently in their UserEnrollment model.

    Input: request
    Returns: None

    """
    if request.user.is_authenticated():
        user_enrollment, _ = UserEnrollment.objects.get_or_create(user=request.user)
        if request.session.get(IS_ELIGIBLE_FLAG):
            user_enrollment.is_eligible = True
            user_enrollment.save()
            del request.session[IS_ELIGIBLE_FLAG]


def need_to_check_eligibility(request):
    """
    Returns True if eligibility requirements need to be checked for a user.

    Input: request
    Returns: Boolean

    """
    active_enrollment_set = ActiveEnrollmentSet.objects.all()[0]
    if not active_enrollment_set.use_req_list:
        return False
    elif request.user.is_authenticated():
        user_enrollment, _ = UserEnrollment.objects.get_or_create(user=request.user)
        # Make sure session eligibility flag gets transferred while we're here.
        transfer_eligibility_info(request)
        user_enrollment.save()
        if user_enrollment.is_eligible:
            return False
    elif request.session.get(IS_ELIGIBLE_FLAG):
        return False
    return True
