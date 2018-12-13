# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse

import bcrypt

from .models import User

def index(request):
    if 'first_name' not in request.session:
        request.session['first_name'] = ''
    if 'last_name' not in request.session:
        request.session['last_name'] = ''
    if 'email' not in request.session:
        request.session['email'] = ''
    return render(request, 'login/index.html')

def register(request):
    if request.method == 'POST':
        # FORM VALIDATION
        errors = User.objects.basic_validator(request)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect(reverse('login:index'))

        # CHECK IF EMAIL IS ALREADY IN DATABASE
        found_users = User.objects.filter(email=request.POST['email'])
        if found_users.count() > 0:
            messages.error(request, 'Email already taken', extra_tags='email')
            return redirect(reverse('login:index'))

        # ADD USER TO DATABASE
        pw_hashed = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
        new_user_id = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], pw=pw_hashed).id

        request.session['first_name'] = ''
        request.session['last_name'] = ''
        request.session['email'] = ''
        request.session['id'] = new_user_id

        return redirect(reverse('login:success'))
    else:
        return redirect(reverse('login:index'))

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        pw = request.POST['pw']
        request.session['login_email'] = email

        # FORM VALIDATION
        if len(email) < 1 or len(pw) < 1:
            messages.error(request, 'Email and/or password fields cannot be blank!')
            return redirect(reverse('login:index'))
        
        # USER LOGIN
        users = User.objects.filter(email=email)
        if len(users) < 1:
            messages.error(request, 'No user with that email!')
            return redirect(reverse('login:index'))
        for user in users:
            if bcrypt.checkpw(pw.encode(), user.pw.encode()):
                request.session['login_email'] = ''
                request.session['id'] = user.id
                return redirect(reverse('login:success'))
        messages.error(request, 'Wrong email/password combination!')
        return redirect(reverse('login:index'))
    else:
        return redirect(reverse('login:index'))

def success(request):
    context = {'first_name': User.objects.get(id=request.session['id']).first_name}
    return render(request, 'login/success.html', context)
