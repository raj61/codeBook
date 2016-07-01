"""
Definition of views.
"""

from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponseRedirect,HttpResponseNotModified
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


@api_view(['GET','POST'])
def profile_list(request,format=None):
    if request.method == 'GET':
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def profile_detail(request,pk,format=None):
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProfileSerializer(profile,data=request.data)
        if serialzier.is_valid():
            serialzier.save()
            return Response(serializer.data)
        return Response(serialzier.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        return redirect('/profile/complete/1')
    if request.POST:
        if request.POST['content'] == 'codechef':
            try:
                codechefUpdate(profile.codechef_handle,profile)
            except Exception,e:
                print (e)
                Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                codeforcesUpdate(profile.codeforces_handle,profile)
            except Exception,e:
                print (e)
                Response(status=status.HTTP_404_NOT_FOUND)
        # print (request.POST['content'])
        # codeforcesUpdate(profile.codeforces_handle,profile)
        return HttpResponseRedirect("/profile")
    # print ("Hello")
    context={
        "profile":profile
        }
    return render(request,"profile.html",context)
def codechefUpdate(codechef_handle,profile):
    url = 'https://www.codechef.com/users/'+codechef_handle
    res = requests.get(url)
    Soup = bs4.BeautifulSoup(res.text)
    rating = Soup.select('.rating-table td')
    codechef_long_global,codechef_long_local = rating[4].getText().split('/')
    codechef_long_rating,r = rating[5].getText().split()
    codechef_short_global,codechef_short_local = rating[7].getText().split('/')
    codechef_short_rating,r = rating[8].getText().split()
    try:
        codechef_rank = CodechefRank.objects.get(handle=codechef_handle)
        codechef_rank.long_global = int(codechef_long_global)
        codechef_rank.long_local = int(codechef_long_local)
        codechef_rank.long_rating = float(codechef_long_rating)
        codechef_rank.short_rating = float(codechef_short_rating)
        codechef_rank.short_global = int(codechef_short_global)
        codechef_rank.short_local = int(codechef_short_local)
    except CodechefRank.DoesNotExist:
        codechef_rank = CodechefRank(handle=codechef_handle,
                                            long_global = int(codechef_long_global),
                                            long_local = int(codechef_long_local),
                                            long_rating = float(codechef_long_rating),
                                             short_rating = float(codechef_short_rating),
                                             short_global = int(codechef_short_global),
                                             short_local = int(codechef_short_local))
        codechef_rank.save()
    profile.codechef_rank = codechef_rank
    profile.save()

def codeforcesUpdate(codeforces_handle,profile):
    url = 'http://codeforces.com/profile/'+codeforces_handle
    res = requests.get(url)
    Soup = bs4.BeautifulSoup(res.text)
    rating = Soup.select('.info span')
    # # print(rating)
    position = rating[0].getText()
    ratin = int(rating[1].getText())
    # print (ratin)
    try:
        codeforces_rank = CodeforcesRank.objects.get(handle=codeforces_handle)
        # print (codeforces_rank.rating)
        codeforces_rank.rating =  ratin
        # print (codeforces_rank.rating)
        codeforces_rank.position = position
        codeforces_rank.save()
    except CodechefRank.DoesNotExist:
        codeforces_rank = CodeforcesRank(handle=codeforces_handle,
                                         rating = ratin,
                                         position = position)
        codeforces_rank.save()
    profile.codeforces_rank = codeforces_rank





# not in use
def addProfile(request):
    if request.user.is_authenticated() and request.POST:
        #codechef Rank Fetch
        try:
            codechef_rank = CodechefRank.objects.get(handle=request.POST['codechef_handle'])
        except CodechefRank.DoesNotExist:
            codechefUpdate(request.POST['codechef_handle'],request.user.profile)
            # url = 'https://www.codechef.com/users/'+request.POST['codechef_handle']
            # res = requests.get(url)
            # Soup = bs4.BeautifulSoup(res.text)
            # rating = Soup.select('.rating-table td')
            # codechef_long_global,codechef_long_local = rating[4].getText().split('/')
            # codechef_long_rating,r = rating[5].getText().split()
            # codechef_short_global,codechef_short_local = rating[7].getText().split('/')
            # codechef_short_rating,r = rating[8].getText().split()
            # codechef_rank = CodechefRank(handle=request.POST['codechef_handle'],
            #                                     long_global = int(codechef_long_global),
            #                                     long_local = int(codechef_long_local),
            #                                     long_rating = float(codechef_long_rating),
            #                                      short_rating = float(codechef_short_rating),
            #                                      short_global = int(codechef_short_global),
            #                                      short_local = int(codechef_short_local))
            # codechef_rank.save()
        #codeforces record fetch
        try:
            codeforces_rank = CodeforcesRank.objects.get(handle=request.POST['codeforces_handle'])
        except CodeforcesRank.DoesNotExist:
            codeforcesUpdate(request.POST['codeforces_handle'],request.user.profile)
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
       # # print (hackerrank_rank)


    return render(request,"addprofile.html",{})
# leaderboard
def leaderboard(request):
    profiles = Profile.objects.all()
    context = {
    'profiles':profiles
    }
    return render(request,"leaderboard.html",context)

def filter(request):
    if request.method == 'POST':
        institute = request.POST.get("institute",None)
        branch = request.POST.get("branch",None)
        if institute and branch:
            profiles1 = Institute.objects.get(name = institute).profile.all()
            profiles = profiles1.filter(branch=Branch.objects.get(name=branch))

        elif institute:
            profiles = Profile.objects.filter(institute=Institute.objects.get(name=institute))
        elif  branch:
            profiles = Branch.objects.get(name = branch).profile.all()
        else:
            profiles = Profile.objects.all()
        context = {
        "profiles":profiles
        }
        return render(request,'leaderboard.html',context);
    return render(request,'filter.html',{});
def completeProfile(request):
    if request.POST:
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
                            mobile_no = request.POST['mobile_no'],
                            dp = request.FILES['img'])
        profile.save()
        context = {
        'profile':profile,
        'message':'Profile completed',
        }
        return render(request,"profile.html",context)

        #hackerrank_rank = HackerrankRank(handle=request.POST['hackerrank_handle'],
         #                                points = score[0].getText())
       # hackerrank_rank.save()
       # # print (hackerrank_rank)


    return render(request,"completeProfile1.html",{})
def addSite(request):
    if request.POST:
        if request.POST['codechef_handle']:
            profile = Profile.objects.get(user = request.user)
            codechefUpdate(request.POST['codechef_handle'],profile)
            # # print ("Hello"+profile)
        if request.POST['codeforces_handle']:
            codeforcesUpdate(request.POST['codeforces_handle'],request.user.profile)
        url = '/profile/'+str(request.user)
        return redirect(url)

    return render(request,"addSite.html",{})
