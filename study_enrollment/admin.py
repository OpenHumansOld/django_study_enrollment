from django.contrib import admin
from study_enrollment.models import *

# RequirementList admin with Requirements inline.

class RequirementInline(admin.StackedInline):
    model = Requirement.req_list.through

class RequirementListAdmin(admin.ModelAdmin):
    inlines = [RequirementInline]


# Requirement admin with RequirementChoices inline.

class RequirementChoiceInline(admin.StackedInline):
    model = RequirementChoice
    extra = 3

class RequirementAdmin(admin.ModelAdmin):
    inlines = [RequirementChoiceInline]


# Module list with EnrollmentModule inline.

class EnrollmentModuleInline(admin.StackedInline):
    model = EnrollmentModule.module_list.through

class ModuleListAdmin(admin.ModelAdmin):
    inlines = [EnrollmentModuleInline]


# EnrollmentModule with ModuleQuestions inline.

class ModuleQuestionInline(admin.StackedInline):
    model = ModuleQuestion.enrollment_module.through

class EnrollmentModuleAdmin(admin.ModelAdmin):
    inlines = [ModuleQuestionInline]


# ModuleQuestion with ModuleQuestionChoices inline.

class ModuleQuestionChoiceInline(admin.StackedInline):
    model = ModuleQuestionChoice
    extra = 3

class ModuleQuestionAdmin(admin.ModelAdmin):
    inlines = [ModuleQuestionChoiceInline]


admin.site.register(Requirement, RequirementAdmin)

admin.site.register(RequirementList, RequirementListAdmin)

admin.site.register(ModuleQuestion, ModuleQuestionAdmin)

admin.site.register(EnrollmentModule, EnrollmentModuleAdmin)

admin.site.register(ModuleList, ModuleListAdmin)

admin.site.register(ActiveEnrollmentSet)
