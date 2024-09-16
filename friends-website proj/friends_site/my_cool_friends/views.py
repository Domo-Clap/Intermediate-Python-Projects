from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

friends_list = {

    "Austin": "Austin.html",
    "Moose": "Moose.html",
    "Ghosty": "Ghosty.html",
    "Grey": "Grey.html",
    "Matt": "Matt.html",
    "Keenan": "Keenan.html",
    "Connor": "Connor.html"

}


def home_page(request):
    return render(request, "my_cool_friends/homePage.html")


def friend_page(request, friendName):

    friendHtml = friends_list[friendName]

    try:
        return render(request, f"my_cool_friends/{friendHtml}")

    except:

        return HttpResponseNotFound("Could not find the friend you are talking about!")