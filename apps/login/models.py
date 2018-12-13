# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pw = request.POST['pw']
        pw_confirm = request.POST['pw_confirm']

        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['email'] = email

        errors = {}
        if len(first_name) < 2 or len(last_name) < 2 or not first_name.isalpha() or not last_name.isalpha():
            errors['names'] = 'First and last names must be at least 2 characters and only contain letters!'
        
        if len(email) < 1:
            errors['email'] = 'Email cannot be blank!'
        elif not EMAIL_REGEX.match(email):
            errors['email'] = 'Invalid email address!'
        
        if len(pw) < 8:
            errors['pw'] = 'Password must be at least 8 characters!'
        
        if pw != pw_confirm:
            errors['pw_confirm'] = 'Passwords don\'t match!'

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {}>".format(self.first_name, self.last_name)
