import datetime
import csv
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import FieldFile
from django.http import HttpResponse
from django.forms.models import model_to_dict
from typing import Optional
from django.views import View
from course.models import Category, Course, Comment, Video, Blog
from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from user.models import Teacher
from course.forms import CourseForm, BlogForm, VideoForm, CommentForm
from django.urls import reverse_lazy
from openpyxl import Workbook


# Create your views here.
""" this class displays the first page"""


class HomeListView(TemplateView):
    template_name = 'course/index.html'

    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        courses = Course.objects.all()
        teachers = Teacher.objects.all()
        blogs = Blog.objects.all().order_by('-created_at')[:6]
        for teacher in teachers:
            teacher.courses = teacher.course.only('category_id__title')
        context = super().get_context_data(**kwargs)
        context['categories'] = categories
        context['courses'] = courses
        context['teachers'] = teachers
        context['blogs'] = blogs
        return context


"""From here starts actions over Category"""


class CategoryDetail(View):

    def get(self, request, _id: Optional[int] = None):
        categories = Category.objects.all()
        category = get_object_or_404(Category, id=_id)
        courses = Course.objects.filter(category_id=category)

        paginator = Paginator(courses, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'categories': categories,
            'courses': page_obj
        }

        return render(request, 'course/category-detail.html', context)


"""From here starts actions over Course"""


class CourseListView(TemplateView):
    template_name = 'course/course.html'

    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        courses = Course.objects.all()

        paginator = Paginator(courses, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = super().get_context_data(**kwargs)

        context['categories'] = categories
        context['courses'] = page_obj
        return context


class CourseDetailView(View):

    def get(self, request, _slug: Optional[int] = None):
        course = get_object_or_404(Course, slug=_slug)

        videos = Video.objects.filter(course_id=course)
        categories = Category.objects.all()

        paginator = Paginator(videos, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'course': course,
            'videos': page_obj,
            'categories': categories,
        }

        return render(request, 'course/course-detail.html', context)


class AddNewCourseView(CreateView):
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('home')
    template_name = 'course/add-new-course.html'


class EditCourseView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/update.html'
    success_url = reverse_lazy('courses')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj


"""From here starts actions over Blog"""


class BlogView(ListView):
    model = Blog
    template_name = 'course/blog.html'
    context_object_name = 'blogs'
    paginate_by = 8

    def get_queryset(self):
        queryset = Blog.objects.all()
        category_id = self.request.GET.get('filter')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(
            num_blogs=Count('blog')
        )
        return context


class BlogListView(ListView):
    model = Blog
    template_name = 'course/blog-list.html'
    context_object_name = 'blogs'
    paginate_by = 8

    def get_queryset(self):
        queryset = Blog.objects.all()
        category_id = self.request.GET.get('filter')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(
            num_blogs=Count('blog')
        )
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'course/blog-detail.html'
    context_object_name = 'blog'


class AddNewBlogView(CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('home')
    template_name = 'course/add-new-blog.html'


class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'course/update.html'
    success_url = reverse_lazy('blog')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'course/delete_confirm/delete-confirm-blog.html'
    context_object_name = 'blog'
    success_url = reverse_lazy('blog')


"""From here starts actions over Videos"""


class AddNewVideoView(CreateView):
    model = Video
    form_class = VideoForm
    success_url = reverse_lazy('home')
    template_name = 'course/add-new-video.html'


class VideoUpdateView(UpdateView):
    model = Video
    form_class = VideoForm
    template_name = 'course/update.html'
    success_url = reverse_lazy('courses')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj


class VideoDeleteView(DeleteView):
    model = Video
    template_name = 'course/delete_confirm/delete-confirm-video.html'
    context_object_name = 'video'
    success_url = reverse_lazy('courses')


class VideoDetailView(DetailView):
    model = Video
    template_name = 'course/video-detail.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['categories'] = Category.objects.all()
        context['comments'] = Comment.objects.filter(video_id=self.object, parent__isnull=True).order_by('-rating')[:3]

        return context

    def post(self, request, *args, **kwargs):
        video = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video_id = video
            comment.user_id = request.user
            comment.save()
            return redirect('video_detail', pk=video.pk)
        return self.get(request, *args, **kwargs)


""" this class displays about us"""


class AboutView(TemplateView):
    template_name = 'course/about.html'


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, FieldFile):
            return obj.url if obj else None
        return super().default(obj)


class ExportDataView(View):
    """ This class is used to export data"""

    def get(self, request, *args, **kwargs):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        format = request.GET.get('format')

        if format == 'csv':
            return self.export_csv(date)

        elif format == 'json':
            return self.export_json(date)

        elif format == 'xlsx':
            return self.export_xlsx(date)

        else:
            return HttpResponse('Bad Request', status=400)

    def export_csv(self, date):
        meta = Video._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={Video._meta.object_name}-{date}.csv'

        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in Video.objects.all():
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def export_json(self, date):
        response = HttpResponse(content_type='application/json')
        videos = Video.objects.all()
        data = []

        for video in videos:
            video_dict = model_to_dict(video)
            if 'image_field' in video_dict:
                video_dict['image_field'] = video_dict['image_field'].url if video_dict['image_field'] else None
            data.append(video_dict)

        response.write(json.dumps(data, indent=4, cls=CustomJSONEncoder))
        response['Content-Disposition'] = f'attachment; filename=videos-{date}.json'

        return response

    def export_xlsx(self, date):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=videos-{date}.xlsx'

        wb = Workbook()
        ws = wb.active
        ws.title = 'Videos'

        meta = Video._meta
        field_names = [field.name for field in meta.fields]

        ws.append(field_names)

        for obj in Video.objects.all():
            ws.append([str(getattr(obj, field)) for field in field_names])  # Convert to string

        wb.save(response)
        return response
