# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
    verbose_name = 'Odpowiedzi'


class BaseQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']})
    ]

    list_display = ('question_text', )
    verbose_name = 'Pytanie'


class QuestionAdmin(BaseQuestionAdmin):
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
