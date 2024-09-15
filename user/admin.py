from django.contrib import admin
from user.models import User, Teacher
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from user.admin_filter import JoinedDateFilter

# Register your models here.


@admin.register(User)
class UserModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('email', 'username', 'get_image', 'date_of_birth')
    search_fields = ('title', 'category_id')
    list_filter = [JoinedDateFilter]

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="rounded-circle" style="width: 50px; height: 50px;" />',
                               obj.image.url)
        return format_html('<img src="{}" class="rounded-circle" style="width: 50px; height: auto;" />',
                           'https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-'
                           'background-user-symbol-vector-illustration.jpg?s=1024x1024&w=is&k=20&c=-mUWsTSENkugJ3qs5cov'
                           'paj-bhYpxXY-v9RDpzsw504=')

    get_image.short_description = 'Image'


@admin.register(Teacher)
class TeacherModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('full_name', 'get_image')
    search_fields = ('title', 'category_id')
    list_filter = [JoinedDateFilter]

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="rounded-circle" style="width: 50px; height: 50px;" />',
                               obj.image.url)
        return format_html('<img src="{}" class="rounded-circle" style="width: 50px; height: auto;" />',
                           'https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-'
                           'background-user-symbol-vector-illustration.jpg?s=1024x1024&w=is&k=20&c=-mUWsTSENkugJ3qs5cov'
                           'paj-bhYpxXY-v9RDpzsw504=')

    get_image.short_description = 'Image'
