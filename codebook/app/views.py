"""
Definition of views.
"""

from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib.auth.models import User
from datetime import datetime
from .models import *
import requests, bs4
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'base.html',
        {

        }
    )
def profile(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login')
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    if not profile:
        return redirect('profile/complete')
    return render(request,"profile.html",{})


def addProfile(request):
    if request.user.is_authenticated() and request.POST:
        url = 'https://www.codechef.com/users/'+request.POST['codechef_handle']
        res = requests.get(url)
        Soup = bs4.BeautifulSoup(res.text)
        rating = Soup.select('.rating-table td')
        codechef_long_global,codechef_long_local = rating[4].getText().split('/')
        codechef_long_rating,r = rating[5].getText().split()
        codechef_short_global,codechef_short_local = rating[7].getText().split('/')
        codechef_short_rating,r = rating[8].getText().split()
        codechef_rank = CodechefRank(handle=request.POST['codechef_handle'],long_global = int(codechef_long_global),long_local = int(codechef_long_local),long_rating = float(codechef_long_rating), short_rating = float(codechef_short_rating),short_global = int(codechef_short_global),short_local = int(codechef_short_local))
        codechef_rank.save()
        #codeforces record fetch
        url = 'http://codeforces.com/profile/'+request.POST['codeforces_handle']
        res = requests.get(url)
        Soup = bs4.BeautifulSoup(res.text)
        rating = Soup.select('.info span')
        position = rating[0].getText()
        rating = int(rating[1].getText())
        codeforces_rank = CodeforcesRank(handle=request.POST['codeforces_handle'],
                                         rating = rating,
                                         position = position)
        codeforces_rank.save()
        #hackerrank record fetch
        url = 'https://www.hackerrank.com/'+request.POST['hackerrank_handle']
        res = requests.get(url)
        Soup = bs4.BeautifulSoup(res.text)
        score = Soup.select('#hacker-archive-score')
        try:
            institute = Institute.objects.get(name=request.POST['institute'])
        except Institute.DoesNotExist:
            institute = Institute(name=request.POST['institute'])
            institute.save()
        try:
            branch = Branch.objects.get(name=request.POST['branch'])
        except Branch.DoesNotExist:
            branch = Branch(name=request.POST['branch'])
            branch.save()
        profile = Profile(fname=request.POST['fname'],
                            lname = request.POST['lname'],
                            user = request.user,
                            institute = institute,
                            branch = branch,
                            year = request.POST['year'],
                            codechef_handle = request.POST['codechef_handle'],
                            codeforces_handle = request.POST['codeforces_handle'],
                            hackerrank_handle = request.POST['hackerrank_handle'],
                            codechef_rank = codechef_rank,
                            codeforces_rank = codeforces_rank,
                            hackerrank_rank= hackerrank_rank,
                            mobile_no = request.POST['mobile_no'],
                            dp = request.FILES['dp'])
        profile.save()

        #hackerrank_rank = HackerrankRank(handle=request.POST['hackerrank_handle'],
         #                                points = score[0].getText())
       # hackerrank_rank.save()
       # print (hackerrank_rank)


    return render(request,"addprofile.html",{})
