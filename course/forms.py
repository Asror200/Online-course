from django import forms
from course.models import Blog, Course, Video, Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'body', 'image', 'category_id']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'price', 'category_id', 'teacher_id', 'slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'duration', 'file', 'course_id']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rating', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'cols': 100}),
            'rating': forms.RadioSelect,
        }
