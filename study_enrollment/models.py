from django.db import models
from django.contrib.auth.models import User

class RequirementList(models.Model):
    version = models.CharField(max_length=30)

    def __unicode__(self):
        return self.version

class Requirement(models.Model):
    # A requirement question might get re-used in multiple requirement lists.
    req_list = models.ManyToManyField(RequirementList)
    question = models.CharField(max_length=200)
    explanation = models.TextField(blank=True)

    def __unicode__(self):
        return self.question + ': ' + ', '.join([str(x) for x in self.requirementchoice_set.all()])

class RequirementChoice(models.Model):
    # Only map to one Requirement, because is_eligible depends on the combination:
    # i.e. "Yes" can mean eligible for one question, and ineligible for another.
    requirement = models.ForeignKey(Requirement)
    answer = models.CharField(max_length=200)
    is_eligible = models.BooleanField()

    def __unicode__(self):
        return str(self.answer) + ' (Eligible: ' + str(self.is_eligible) + ')'

class ActiveEnrollmentSet(models.Model):
    req_list = models.ForeignKey(RequirementList,
                                 null=True,
                                 blank=True)
    use_req_list = models.BooleanField(default=True)

class UserEnrollment(models.Model):
    user = models.ForeignKey(User)
    is_eligible = models.BooleanField(default=False)
