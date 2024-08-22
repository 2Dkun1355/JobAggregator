import asyncio
from threading import Thread

from django.http import HttpResponse
from django.utils.html import avoid_wrapping
from requests_html import AsyncHTMLSession

from customers.models import AdditionalUserFields, UserSearch
from job.parsers import DjinniParser




def test_view(request):
    search = UserSearch.objects.first()
    parser = DjinniParser()
    parser.parse_detail_urls('22')
    return HttpResponse('11111')
