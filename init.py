from home.models import *
from content_manager.models import *

TextWebsite.objects.init()
Library.objects.create(name="lol")
Library.objects.create(name="test")
Library.objects.create(name="what")

Yap.objects.create(name="mdr")
Yap.objects.create(name="foo")
Yap.objects.create(name="bar")