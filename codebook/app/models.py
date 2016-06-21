"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

class Institute(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
class Branch(models.Model):
    name = models.CharField(max_length = 20)
    def __str__(self):
        return self.name
class CodechefRank(models.Model):
    handle = models.CharField(max_length=100,unique=True)
    long_global = models.IntegerField(null=True)
    long_local = models.IntegerField(null=True)
    long_rating = models.FloatField(null=True)
    short_rating = models.FloatField(null=True)
    short_global = models.IntegerField(null=True)
    short_local = models.IntegerField(null=True)
    def __str__(self):
        return self.handle
class CodeforcesRank(models.Model):
    handle = models.CharField(max_length=100,unique=True)
    rating = models.IntegerField()
    position = models.CharField(max_length=20,null=True)
    def __str__(self):
        return self.handle
class HackerrankRank(models.Model):
    handle = models.CharField(max_length=100,unique=True)
    points = models.IntegerField()
    def __str__(self):
        return self.handle

class Profile(models.Model):
    fname = models.CharField(max_length = 20)
    lname = models.CharField(max_length = 20)
    user = models.ForeignKey(User, related_name='profile')
    institute = models.ForeignKey(Institute, related_name='profile')
    branch = models.ForeignKey(Branch, related_name='profile')
    year = models.IntegerField()
    codechef_handle = models.CharField(max_length =100,blank=True)
    codeforces_handle = models.CharField(max_length=100,blank=True)
    hackerrank_handle = models.CharField(max_length=100,blank=True)
    codechef_rank = models.ForeignKey(CodechefRank, related_name='profile',blank=True,null=True)
    codeforces_rank = models.ForeignKey(CodeforcesRank, related_name='profile',blank=True,null=True)
    hackerrank_rank = models.ForeignKey(HackerrankRank, related_name='profile',blank=True,null=True)
    mobile_no = models.CharField(max_length=10)
    dp = models.ImageField(upload_to = 'dp')
    def __str__(self):
        return self.fname+self.lname
