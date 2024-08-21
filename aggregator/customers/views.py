from django.http import HttpResponse


from customers.models import AdditionalUserFields, UserSearch
from job.parsers import DjinniParser


def test_view(request):
    parser = DjinniParser()
    user_search = UserSearch.objects.first()
    print(user_search)
    url = parser.parse_detail_urls('')

    return HttpResponse('11111')
