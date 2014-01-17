from django.contrib import admin
from study_enrollment.models import RequirementList, Requirement, ActiveEnrollmentSet

class RequirementInline(admin.StackedInline):
    model = Requirement
    extra = 3

class RequirementListAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Version',          {'fields': ['version']}),
    ]
    inlines = [RequirementInline]

admin.site.register(RequirementList, RequirementListAdmin)

admin.site.register(ActiveEnrollmentSet)
