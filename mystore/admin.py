from django.contrib import admin
from .models import StoreReport, StoreStatusLog, StoreTimezone, StoreTiming

# Register your models here.

admin.site.register(StoreReport)
admin.site.register(StoreTiming)
admin.site.register(StoreStatusLog)
admin.site.register(StoreTimezone)
