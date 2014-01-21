from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, check_password
from django.views.generic.base import View
from study_enrollment.models import ActiveEnrollmentSet, Requirement


class BaseEnrollmentView(View):
    def admin_pwd_changed(self, default_account):
        # If the password matches "study_admin", it hasn't been changed.
        if check_password('study_admin', default_account.password):
            return False
        else:
            return True

    def dispatch(self, request, *args, **kwargs):
        try:
            default_account = User.objects.get(username='study_admin')
        except User.DoesNotExist:
            return HttpResponse("If you're seeing this message, it's because " +
                                "the study_admin account doesn't exist -- " +
                                "probably because the initialize_data.yaml " +
                                "fixture hasn't been loaded.")
        if not self.admin_pwd_changed(default_account):
            return render(request, 'study_enrollment/system_needs_set_up.html')
        active_enrollment_set = ActiveEnrollmentSet.objects.all()
        if len(active_enrollment_set) != 1:
            return HttpResponse("Problem with database! One and only one ActiveEnrollmentSet should exist.")
        self.enrollment_set = active_enrollment_set[0]
        if self.enrollment_set.use_req_list:
            self.requirements = Requirement.objects.filter(req_list=self.enrollment_set.req_list)
        # Remainder as in django.views.generic.base
        return super(BaseEnrollmentView, self).dispatch(request, *args, **kwargs)


class IndexView(BaseEnrollmentView):
    def get(self, request, *args, **kwargs):
        return render(request, 'study_enrollment/index.html')


class RequirementsView(BaseEnrollmentView):
    def get(self, request, *args, **kwargs):
        if not self.enrollment_set.use_req_list:
            return HttpResponseRedirect('/start')
        if not self.requirements:
            return render(request, 'study_enrollment/requirements_need_set_up.html')
        requirement_choices = [req.requirementchoice_set.all() for req in self.requirements]
        req_items = [ {'requirement': self.requirements[x],
                       'req_choices': requirement_choices[x]}
                      for x in range(len(self.requirements)) ]
        return render(request, 'study_enrollment/requirements.html',
                      { 'req_items': req_items } )

    def post(self, request, *args, **kwargs):
        if not self.enrollment_set.use_req_list:
            return HttpResponseRedirect('/start')
        failed_questions = []
        for req in self.requirements:
            req_choices = req.requirementchoice_set.all()
            choice = req.requirementchoice_set.get(answer=request.POST[req.question])
            if not choice.is_eligible:
                failed_questions.append({'requirement': req, 'choice': choice})
        if failed_questions:
            return render(request, 'study_enrollment/not_eligible.html', { 'reqs_failed': failed_questions })
        else:
            return HttpResponse("Page for entering email to start enrollment process.")


class StartView(BaseEnrollmentView):
    def get(self, request, *args, **kwargs):
        # TODO: Make sure user can't just jump to this without going through
        # the requirements page (if used).
        return HttpResponse("Page for entering email to start enrollment process.")
