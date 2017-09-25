# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def reg_validate(self, postData):
        errors = []
        if len(postData['name']) < 2:
            errors.append("First name cannot be less than 2 characters")
        if len(postData['alias']) < 2:
            errors.append("Alias cannot be less than 2 characters")
        if not re.match(EMAIL_REGEX, postData['email']):
            errors.append("Invalid email")
        if len(postData["password"]) < 8:
            errors.append("Password must be at least 8 characters")
        if postData["password"] != postData["pw_confirm"]:
            errors.append("Passwords must match")
        if len(self.filter(email=postData['email'])) > 1:
            errors.append("That email already exists")
        if postData['bday'] == "mm/dd/yyy":
            errors.append("Date of birth cannot be empty")
        return errors

    def log_validate(self, postData):
        errors = []
        if len(postData['email_login']) <1:
            errors.append("Email cannot be blank")
        if len(postData['pw_login']) <1:
            errors.append("Password cannot be blank")
        if len(self.filter(email=postData['email_login'])) > 0:
            user = self.filter(email=postData["email_login"])[0]
            if not bcrypt.checkpw(postData["pw_login"].encode(), user.password.encode()):
                errors.append("email/password incorrect")
        else:
            errors.append("email/password incorrect")
            return errors
        if not errors:
            return user


class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {} {} {}>".format(self.name, self.alias, self.email, self.password)

class Friend(models.Model):
    current = models.ForeignKey(User, related_name="requests")
    friend = models.ForeignKey(User, related_name="requested")
    def __repr__(self):
        return "<Friend object: {} {} {} {}>".format(self.current, self.friend)

# Create your models here.
