from django.contrib import admin
from django.utils.html import format_html
from course.models import Course, Customer, Comment, Category, Video, Blog
from course.admin_filter import JoinedDateFilter
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.unregister(Group)


@admin.register(Category)
class CategoryModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'get_image')
    search_fields = ('title',)
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


@admin.register(Course)
class CourseModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'category_id', 'teacher_id', 'get_image')
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


@admin.register(Video)
class VideoModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'duration', 'course_id')
    search_fields = ('title', 'course_id')
    list_filter = [JoinedDateFilter]

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="rounded-circle" style="width: 50px; height: 50px;" />',
                               obj.image.url)

        def file_link(self, obj):
            if obj.file:
                return format_html('<a href="{}" target="_blank">View File</a>', obj.file.url)
            return "No file"

        file_link.short_description = 'File'


@admin.register(Comment)
class CommentModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('rating', 'user_id', 'video_id', 'parent')
    search_fields = ('user_id', 'video_id')
    list_filter = [JoinedDateFilter]


@admin.register(Customer)
class CustomerModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('phone', 'user_id', 'course_id')
    search_fields = ('user_id', 'course_id')
    list_filter = [JoinedDateFilter]


@admin.register(Blog)
class BlogModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'body', 'get_image', 'category_id')
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
