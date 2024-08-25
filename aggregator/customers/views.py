import asyncio
from threading import Thread

from django.http import HttpResponse
from django.utils.html import avoid_wrapping
from requests_html import AsyncHTMLSession

from customers.models import AdditionalUserFields, UserSearch
from job.models import RawVacancy
from job.parsers import DjinniParser, DouParser


def test_view(request):
    # test_parser()
    return HttpResponse("<h1>Successfully</h1>")


def test_parser():
    search = UserSearch.objects.first()
    djinni_parser = DjinniParser()
    dou_parser = DouParser()

    djinni_parser.run(search)
    dou_parser.run(search)
    raw_djinni_qs = RawVacancy.objects.filter(source='Djinni')
    raw_dou_qs = RawVacancy.objects.filter(source='DOU')

    for raw in raw_djinni_qs:
        djinni_parser.save_vacancy(raw)

    for raw in raw_dou_qs:
        dou_parser.save_vacancy(raw)