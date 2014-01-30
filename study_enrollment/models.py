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
    # A requirement question might get re-used in multiple requirement lists.
    req_list = models.ManyToManyField(RequirementList)
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

class ActiveEnrollmentSet(models.Model):
    """
    The set of requirements, guides, and forms currently used by the system.
    One and only one of this object should exist on the site. This is initialized
    by the initialize_data fixture.

    Fields:
    req_list:      (ForeignKey) A RequirementList
    use_req_list:  (Boolean) Default is True. Set to False to not use any
                   requirement questions.

    """
    req_list = models.ForeignKey(RequirementList,
                                 null=True,
                                 blank=True)
    use_req_list = models.BooleanField(default=True)

class UserEnrollment(models.Model):
    """
    Tracks data regarding a particular User's study_enrollment data.

    Fields:
    user:         (ForeignKey) A User from Django's auth system
    is_eligible:  (Boolean) Set to True if a User passed Requirements

    """
    user = models.ForeignKey(User)
    is_eligible = models.BooleanField(default=False)
