from django.contrib import admin
from study_enrollment.models import RequirementList, Requirement, RequirementChoice, ActiveEnrollmentSet

class RequirementInline(admin.StackedInline):
    model = Requirement.req_list.through

class RequirementListAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Version',          {'fields': ['version']}),
    ]
    inlines = [RequirementInline]

class RequirementChoiceInline(admin.StackedInline):
    model = RequirementChoice
    extra = 3

class RequirementAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question',          {'fields': ['question']}),
    ]
    inlines = [RequirementChoiceInline]

admin.site.register(Requirement, RequirementAdmin)

admin.site.register(RequirementList, RequirementListAdmin)

admin.site.register(ActiveEnrollmentSet)
