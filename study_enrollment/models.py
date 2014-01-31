from django.db import models
from django.contrib.auth.models import User

class RequirementList(models.Model):
    """
    A model defining a set of Requirements

    Fields:
    version:  (CharField, 30 char max) Short string describing this list

    Requirements are defined by a ManyToMany relationship.
    To access them from the object, a filter can be used, e.g.
    requirements = Requirement.objects.filter(req_list=req_list)

    """
    version = models.CharField(max_length=30)

    def __unicode__(self):
        return self.version

class Requirement(models.Model):
    """
    A particular study reqirement

    Fields:
    req_list:    (ManyToMany) RequirementList
    question:    (CharField, 200 char max) String describing the requirement
                 question (e.g. "Are you at least 18 years of age?")
    explanation: (TextField) Text explaining the requirement.
                 (Provided to users if they fail to meet this requirement.)

    Answers are defined as RequirementChoice objects.
    To access them from this object, you can ask for the set, e.g.
    choices = requirement.requirementchoice_set.all()

    """
    # A question might get re-used in multiple versions of the requirement list
    req_list = models.ManyToManyField(RequirementList, blank=True)
    question = models.CharField(max_length=200)
    explanation = models.TextField(blank=True)

    def __unicode__(self):
        return self.question + ': ' + ', '.join([str(x) for x in self.requirementchoice_set.all()])

class RequirementChoice(models.Model):
    """
    A potential answer to a Requirement question

    Fields:
    requirement:  (ForeignKey) A Requirement
    answer:       (CharField, 200 char max) Answer to the requirement question
    is_eligible:  (BooleanField) True if this answer means the user is eligible

    """
    # Only map to one Requirement, because is_eligible depends on the Q/A combo.
    # e.g. a "Yes" for Q1 could mean eligible, but "Yes" to Q2 means ineligible.
    requirement = models.ForeignKey(Requirement)
    answer = models.CharField(max_length=200)
    is_eligible = models.BooleanField()

    def __unicode__(self):
        return str(self.answer) + ' (Eligible: ' + str(self.is_eligible) + ')'

class ModuleList(models.Model):
    """
    A model defining a set of EnrollmentModules

    Fields:
    version:  (CharField, 30 char max) Short string describing this list

    EnrollmentModules are defined by a ManyToMany relationship.
    To access them from the object, a filter can be used, e.g.
    modules = EnrollmentModule.objects.filter(module_list=module_list)

    """
    pass
    version = models.CharField(max_length=30)

    def __unicode__(self):
        return self.version

class EnrollmentModule(models.Model):
    """
    A module in an enrollment exam/lesson system.

    Fields:
    title:    (CharField, 120 char max) Title of this module
    content:  (TextField) Study material for this section.

    Questions for the module are defined as ModuleQuestion objects.
    To access them from this object, you can ask for the set, e.g.
    questions = enrollmentmodule.modulequestion_set.all()

    """
    # A module might get re-used in multiple versions of the module list
    module_list = models.ManyToManyField(ModuleList, blank=True)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

class ModuleQuestion(models.Model):
    """
    A module question.

    Fields:
    module_list:   (ManyToMany) ModuleList
    question:      (CharField, 300 char max) Question about material
                   (e.g. "What ingredients may be in our ice cream?")
    question_type: (CharField, 3 char max) choices are "all" or "one"
                   "all": "select all" presents a checkbox question; the user
                   must select all correct answers to pass the question.
                   "one": "select one" presents a radiobox question; the user
                   must select one correct answer to pass the question.

    Answers are defined as ModuleQuestionChoice objects.
    To access them from this object, you can ask for the set, e.g.
    choices = modulequestion.modulequestionchoice_set.all()

    """
    enrollment_module = models.ManyToManyField(EnrollmentModule, blank=True)
    question = models.CharField(max_length=300)
    question_type_choices = [('one', 'select one'),
                             ('all', 'select all')]
    question_type = models.CharField(max_length=3,
                                     choices=question_type_choices,
                                     default='one')

    def __unicode__(self):
        return self.question + ': ' + ', '.join([str(x) for x in self.modulequestionchoice_set.all()])

class ModuleQuestionChoice(models.Model):
    """
    A potential answer to a ModuleQuestion.

    Fields:
    question:    (ForeignKey) ModuleQuestion
    answer:      (CharField, 200 char max) Answer to question
    is_correct:  (BooleanField) True if this answer is correct

    """
    # Only map to one ModuleQuestion, because is_correct depends on the Q/A combo.
    # e.g. a "Yes" for Q1 could be correct, but "Yes" to Q2 means incorrect.
    question = models.ForeignKey(ModuleQuestion)
    answer = models.CharField(max_length=200)
    is_correct = models.BooleanField()

    def __unicode__(self):
        return str(self.answer) + ' (Correct: ' + str(self.is_correct) + ')'


class ActiveEnrollmentSet(models.Model):
    """
    The set of requirements, guides, and forms currently used by the system.
    One and only one of this object should exist on the site. This is initialized
    by the initialize_data fixture.

    Fields:
    req_list:        (ForeignKey) A RequirementList
    use_req_list:    (Boolean) Default is True. Set to False to not use any
                     requirement questions.
    module_list:     (ForeignKey) A ModuleList
    use_module_list: (Boolean) Default is True. Set to False to not use any
                     modules.

    """
    req_list = models.ForeignKey(RequirementList,
                                 null=True,
                                 blank=True)
    use_req_list = models.BooleanField(default=True)
    module_list = models.ForeignKey(ModuleList,
                                    null=True,
                                    blank=True)
    use_module_list = models.BooleanField(default=True)

class UserEnrollment(models.Model):
    """
    Tracks data regarding a particular User's study_enrollment data.

    Fields:
    user:         (ForeignKey) A User from Django's auth system
    is_eligible:  (Boolean) Set to True if a User passed Requirements

    """
    user = models.ForeignKey(User)
    is_eligible = models.BooleanField(default=False)
