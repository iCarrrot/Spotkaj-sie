# -*- coding: utf-8 -*-
"""
    Register models to admin panel
"""

from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """
    Class for chooses for question
    """
    model = Choice
    extra = 2
    verbose_name = 'Odpowiedzi'


class BaseQuestionAdmin(admin.ModelAdmin):
    """
    Class for base question
    """
    fieldsets = [
        (None, {'fields': ['question_text']})
    ]

    list_display = ('question_text', )
    verbose_name = 'Pytanie'


class QuestionAdmin(BaseQuestionAdmin):
    """
    Class for question
    """
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
