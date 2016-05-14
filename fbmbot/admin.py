from django.contrib import admin
from fbmbot.models import *

# Register your models here.
admin.site.register(BotUser)
admin.site.register(Item)
admin.site.register(Match)
admin.site.register(Log)