from django.urls import path
from course import views
urlpatterns = [
    path('', views.CourseListView.as_view(), name='home'),
    path('courses/<int:_id>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('course/<slug:_slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('video/<int:pk>/', views.VideoDetailView.as_view(), name='video_detail'),
]
