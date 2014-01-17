from django.db import models

class RequirementList(models.Model):
    version = models.CharField(max_length=30)

    def __unicode__(self):
        return self.version

class Requirement(models.Model):
    REQ_CHOICES = ( ('Y', 'Yes'), ('N', 'No'), )
    req_list = models.ForeignKey(RequirementList)
    question = models.CharField(max_length=200)
    explanation = models.TextField(blank=True)
    choice_needed = models.CharField(max_length=2,
                                     choices=REQ_CHOICES)


    def __unicode__(self):
        return self.question

class ActiveEnrollmentSet(models.Model):
    requirements = models.OneToOneField(RequirementList,
                                        null=True,
                                        blank=True)
