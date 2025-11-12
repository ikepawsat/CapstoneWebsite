from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import BostonQualifier

class BostonQualifierResource(resources.ModelResource):
    class Meta:
        model = BostonQualifier
        import_id_fields = ["resultId"]
        skip_unchanged = True
        report_skipped = True

@admin.register(BostonQualifier)
class BostonQualifierAdmin(ImportExportModelAdmin):
    resource_class = BostonQualifierResource
    pass
