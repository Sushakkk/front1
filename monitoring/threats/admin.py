from django.contrib import admin
from .models import Threat
from .models import Request
from .models import RequestThreat

# Register your models here.
admin.site.register(Threat)
admin.site.register(Request)


@admin.register(RequestThreat)
class RequestThreatAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'threat_id')
    search_fields = ('request_id', 'threat_id')