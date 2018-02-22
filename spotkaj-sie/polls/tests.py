"""
Tests for models
"""
import os
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.test import Client


class TestNonLoggedUser(TestCase):
    def test_wrong_user_user_profile(self):
        self.client.login(username='username1', password='password1')
        url = reverse('polls:user_profile')
        response = self.client.get(url)
        self.assertContains(response, "Error!")
    
    def test_wrong_user_event(self):
        self.client.login(username='username1', password='password1')
        url = reverse('polls:event')
        response = self.client.get(url)
        self.assertContains(response, "Error!")
    
    def test_wrong_user_new_event(self):
        self.client.login(username='username1', password='password1')
        response = self.client.get(reverse('polls:new_event',
                                           args=(0,)))
        self.assertContains(response, "Error!")
    
    def test_wrong_user_plans(self):
        self.client.login(username='username1', password='password1')
        url = reverse('polls:plans')
        response = self.client.get(url)
        self.assertContains(response, "Error!")
    
    def test_wrong_user_delete_events(self):
        self.client.login(username='username1', password='password1')
        url = reverse('polls:delete_events')
        response = self.client.get(url)
        self.assertContains(response, "Error!")
    
    def test_wrong_user_delete_plans(self):
        self.client.login(username='username1', password='password1')
        url = reverse('polls:delete_plans')
        response = self.client.get(url)
        self.assertContains(response, "Error!")
    
    def test_wrong_user_show_plans(self):
        self.client.login(username='username1', password='password1')
        url = reverse('polls:show_plans')
        response = self.client.get(url)
        self.assertContains(response, "Error!")
    
    def test_wrong_user_show_events(self):
        self.client.login(username='username1', password='password1')
        url = reverse('polls:show_events')
        response = self.client.get(url)
        self.assertContains(response, "Error!")
    


class TestLoggedUser(TestCase):
    def setUp(self):
        self.client.force_login(
            User.objects.get_or_create(username='testuser')[0])
    # def test_wrong_user(self):
    #     self.client.login(username='username1', password='password1')
    #     url = reverse('polls:user_profile')
    #     response = self.client.get(url)
        # self.assertContains(response, "Error!")
        # print(response.content)

    def test_correct_user(self):
        # user = User.objects.create(username='testuser')
        # user.set_password('12345')
        # user.save()

        # c = Client()
        # logged_in = c.login(username='testuser', password='12345')
        url = reverse('polls:user_profile')
        response = self.client.get(url)
        # self.assertContains(response, "Error!")
        # print(response.content, "\n\n\n\n")
