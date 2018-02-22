# -*- coding: utf-8 -*-
from datetime import date
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=date.min)
    end_time = models.DateTimeField(default=date.max)
    title = models.CharField('Tytuł', max_length=200)

    def __str__(self):
        return self.title

    def is_conflict(self, start_time, end_time):
        if start_time > end_time:
            return True
        if start_time > self.start_time and end_time < self.end_time:
            return False
        return True


class Event(models.Model):
    searching_start_time = models.DateTimeField(default=timezone.now)
    duration = models.FloatField(default=0)
    found_time = models.DateTimeField(null=True, blank=True, default=None)
    title = models.CharField('Tytuł', max_length=200)
    quantity = models.IntegerField(
        'Liczba osób', default=0, blank=False, null=False)

    def __str__(self):
        return self.title

    def is_found(self):
        return self.found_time is not None
