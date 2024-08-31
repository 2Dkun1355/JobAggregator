import asyncio
from threading import Thread

from django.http import HttpResponse
from django.utils.html import avoid_wrapping
from requests_html import AsyncHTMLSession
import requests

from api.serialisers import VacancySerializer
from customers.models import AdditionalUserFields, UserSearch
from job.models import RawVacancy, Vacancy
from job.parsers import DjinniParser, DouParser
from job.utils import generate_mock_data


def test_view(request):
    # test_parser()
    # test_api()

    # vacancy = Vacancy.objects.first()
    # print(vacancy)

    generate_mock_data()

    return HttpResponse("<h1>Successfully</h1>")


def test_api():
    url = 'https://swapi.dev/api/people/1/'
    response = requests.get(url)





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