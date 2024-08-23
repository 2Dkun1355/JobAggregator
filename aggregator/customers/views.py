import asyncio
from threading import Thread

from django.http import HttpResponse
from django.utils.html import avoid_wrapping
from requests_html import AsyncHTMLSession

from customers.models import AdditionalUserFields, UserSearch
from job.models import RawVacancy
from job.parsers import DjinniParser, DouParser


def test_view(request):
    obj = RawVacancy.objects.get(id=8)
    print(obj.id)
    parser = DjinniParser()
    parser.save_vacancy(obj)
    return HttpResponse("<h1>Successfully</h1>")
