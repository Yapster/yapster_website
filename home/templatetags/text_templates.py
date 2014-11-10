from django import template
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template.response import SimpleTemplateResponse
from django.template.loader import render_to_string
from home.models import *

register = template.Library()

@register.filter(name='get_text')
def access(arg):
    try:
        return TextWebsite.objects.get(name=arg).content
    except ObjectDoesNotExist:
        return ''