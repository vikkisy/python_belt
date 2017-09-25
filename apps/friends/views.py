# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.messages import error
from django.contrib import messages
from models import User, Friend
import bcrypt

def index(request):
    context = {
        "users": User.objects.all()
    }
    return render(request, 'friends/index.html')

def process(request):
    errors = User.objects.reg_validate(request.POST)
    if errors:
        for err in errors:
            error(request, err)
        return redirect('/')
    else:
        new_user = User.objects.create(
        name=request.POST["name"],
        alias =  request.POST['alias'],
        email = request.POST['email'],
        birthday = request.POST['bday'],
        password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        )
        request.session['user_id'] = new_user.id
        return redirect('/success')

def login(request):
    errors = User.objects.log_validate(request.POST)
    if type(errors) == list:
        for error in errors:
            messages.error(request, error)
        return redirect('/')

    request.session['user_id'] = errors.id
    return redirect('/success')

def success(request):
    myself = User.objects.get(id=request.session['user_id'])
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "friends": User.objects.all(),
        "friendships": Friend.objects.filter(current=myself),
    }
    return render(request, 'friends/friends.html', context)

def add(request, friend_id):
    current = User.objects.get(id=request.session['user_id'])
    friend = User.objects.get(id=friend_id)
    Friend.objects.create(current=current, friend=friend)
    Friend.objects.create(friend=friend, current=current)
    return redirect('/success')

def user(request, friend_id):
    context = {
        "user": User.objects.get(id=friend_id)
    }
    return render(request, 'friends/user.html', context)

def remove(request, friend_id):
    current = User.objects.get(id=request.session['user_id'])
    friend = User.objects.get(id=friend_id)
    friendship1 = Friend.objects.filter(current=user, friend=friend)
    friendship2 = Friend.objects.filter(friend=friend, current=current)
    friendship1.delete()
    friendship2.delete()
    return redirect('/success')


# Create your views here.
