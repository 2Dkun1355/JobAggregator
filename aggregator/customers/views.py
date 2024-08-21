from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from customers.models import AdditionalUserFields


def test_view(request):
    additionals = AdditionalUserFields.objects.all()
    print(additionals)
    for add in additionals:
        print(add.user.is_staff)
    return HttpResponse(additionals)
