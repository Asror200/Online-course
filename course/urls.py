from django.urls import path
from course import views

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),

    # Category
    path('courses/<int:_id>/', views.CategoryDetail.as_view(), name='category_detail'),

    # Course
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('course/<slug:_slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('add-new-course/', views.AddNewCourseView.as_view(), name='add_new_course'),
    path('edit-course/<int:pk>', views.EditCourseView.as_view(), name='edit_course'),

    # Video
    path('video/<int:pk>/', views.VideoDetailView.as_view(), name='video_detail'),
    path('add-new-video/', views.AddNewVideoView.as_view(), name='add_new_video'),
    path('edit-video/<int:pk>/', views.VideoUpdateView.as_view(), name='edite_video'),
    path('delete-video/<int:pk>/', views.VideoDeleteView.as_view(), name='delete_video'),

    # Blog
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('blog-detail/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog-list/', views.BlogListView.as_view(), name='blog_list'),
    path('add-new-blog/', views.AddNewBlogView.as_view(), name='add_new_blog'),

    path('edit-blog/<int:pk>/', views.BlogUpdateView.as_view(), name='edit_blog'),
    path('delete-blog/<int:pk>/', views.BlogDeleteView.as_view(), name='delete_blog'),

    # Comment
    path('add-new-comment/<int:_id>/', views.AddNewVideoView.as_view(), name='add_new_comment'),

    # import - export
    path('video/export-data/', views.ExportDataView.as_view(), name='export_data'),

    # About
    path('about', views.AboutView.as_view(), name='about'),

]
