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
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'base.html',
        {

        }
    )
@api_view(['GET'])
def user_list(request,format=None):
    user = User.objects.all()
    serializer = UserSerializer(user,many=True)
    return Response(serializer.data)
@api_view(['GET','POST'])
def institute_list(request,format=None):
    if request.method == 'GET':
        institutes = Institute.objects.all()
        serializer = InstituteSerializer(institutes,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = InstituteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def Institute_detail(request,pk,format=None):
    try:
        institute = Institute.objects.get(pk=pk)
    except Institute.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InstituteSerializer(institute)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = InstituteSerializer(institute,data=request.data)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serializer.data)
        return Response(serialzier.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        institute.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def profiledefault(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login')
    return redirect('/profile/'+str(request.user))
def profile(request,user):
    if not request.user.is_authenticated():
        return redirect('/accounts/login')
    try:
        try:
            useri = User.objects.get(username=user)
        except User.DoesNotExist:
            url = '/profile/'+str(request.user)
            return redirect(url)
        profile = Profile.objects.get(user=useri)
    except Profile.DoesNotExist:
        profile = None
    if not profile:
        return redirect('/profile/complete')
    context={
        "profile":profile
        }
    return render(request,"profile.html",context)


def addProfile(request):
    if request.user.is_authenticated() and request.POST:
        #codechef Rank Fetch
        try:
            codechef_rank = CodechefRank.objects.get(handle=request.POST['codechef_handle'])
        except CodechefRank.DoesNotExist:
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
        try:
            codeforces_rank = CodeforcesRank.objects.get(handle=request.POST['codechef_handle'])
        except CodeforcesRank.DoesNotExist:
            url = 'http://codeforces.com/profile/'+request.POST['codeforces_handle']
            res = requests.get(url)
            Soup = bs4.BeautifulSoup(res.text)
            rating = Soup.select('.info span')
            print(rating)
            position = rating[0].getText()
            rating = int(rating[1].getText())
            codeforces_rank = CodeforcesRank(handle=request.POST['codeforces_handle'],
                                             rating = rating,
                                             position = position)
            codeforces_rank.save()
        hackerrank_rank = None
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
                            dp = request.FILES['img'])
        profile.save()
        url = '/profile/'+request.user
        return redirect(url)

        #hackerrank_rank = HackerrankRank(handle=request.POST['hackerrank_handle'],
         #                                points = score[0].getText())
       # hackerrank_rank.save()
       # print (hackerrank_rank)


    return render(request,"addprofile.html",{})
# leaderboard
def leaderboard(request):
    profiles = Profile.objects.all()
    context = {
    'profiles':profiles
    }
    return render(request,"leaderboard.html",context)
