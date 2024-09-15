from django.contrib import admin
from django.utils.html import format_html
from course.models import Course, Customer, Comment, Category, Video, Blog
from course.admin_filter import JoinedDateFilter
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.unregister(Group)
admin.site.register(Category)
admin.site.register(Blog)

@admin.register(Course)
class ProductModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'price', 'category_id', 'teacher_id', 'get_image', 'joined')
    search_fields = ('title', 'category_id')
    prepopulated_fields = {'slug': ('title',)}
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


admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Customer)
