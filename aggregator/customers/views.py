import asyncio
from threading import Thread

from django.http import HttpResponse
from django.utils.html import avoid_wrapping
from requests_html import AsyncHTMLSession

from customers.models import AdditionalUserFields, UserSearch
from job.parsers import DjinniParser, DouParser


def test_view(request):
    user_search = UserSearch.objects.first()
    parser = DouParser()
    parser.run(user_search)
    return HttpResponse("<h1>Successfully</h1>")
