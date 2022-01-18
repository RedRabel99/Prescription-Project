from django.contrib import admin
from prescriptions.models import Prescription, PrescriptionSegment


# Register your models here.

class PrescriptionSegmentInline(admin.TabularInline):
    model = PrescriptionSegment


class PrescriptionAdmin(admin.ModelAdmin):
    inlines = [
        PrescriptionSegmentInline,
    ]


admin.site.register(Prescription, PrescriptionAdmin)
