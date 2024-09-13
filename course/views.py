from typing import Optional
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.views import View
from course.models import Category, Course, Customer, Comment, Video
from django.core.paginator import Paginator
from transliterate import translit
from django.db.models import Q
from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Count, Sum, Max, Min


# Create your views here.
class CourseListView(TemplateView):
    template_name = 'course/index.html'

    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        context = super().get_context_data(**kwargs)
        context['categories'] = categories
        return context


class CategoryDetail(View):
    """This class is used to display a category detail page with courses."""

    def get(self, request, _id: Optional[int] = None):
        categories = Category.objects.all()
        category = get_object_or_404(Category, id=_id)
        courses = Course.objects.filter(category_id=category)

        search = request.GET.get('search')

        if search:
            """Converts requests sent in Cyrillic into Latin"""
            latin = translit(search, 'ru', reversed=True)

            courses = courses.filter(Q(title__icontains=latin) | Q(description__icontains=latin))

        for course in courses:
            course.total_video_count = course.videos.aggregate(Count('id'))['id__count'] or 0
            course.total_duration = course.videos.aggregate(Sum('duration'))['duration__sum'] or 0
            course.average_rating = Comment.objects.filter(video_id__course_id=course).aggregate(Avg('rating'))[
                                        'rating__avg'] or 0
            course.comment_count = Comment.objects.count()
            course.student_count = Customer.objects.filter(course_id=course).count()

        context = {
            'categories': categories,
            'courses': courses
        }

        return render(request, 'course/category-detail.html', context)


class CourseDetailView(View):

    def get(self, request, _slug: Optional[int] = None):
        course = get_object_or_404(Course, slug=_slug)

        videos = Video.objects.filter(course_id=course)

        search = request.GET.get('search')
        if search:
            """Converts requests sent in Cyrillic into Latin"""
            latin = translit(search, 'ru', reversed=True)

            videos = videos.filter(Q(title__icontains=latin) | Q(description__icontains=latin))

        context = {
            'course': course,
            'videos': videos
        }

        return render(request, 'course/course-detail.html', context)


class VideoDetailView(DetailView):
    model = Video
    template_name = 'course/video-detail.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(video_id=self.object.pk).order_by('-rating')[:3]

        return context
