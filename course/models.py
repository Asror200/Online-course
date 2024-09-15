from datetime import timedelta

from django.db import models
from user.models import Teacher, User
from django.template.defaultfilters import slugify


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category', blank=True, null=True)

    def __str__(self):
        return self.title


class Course(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    price = models.FloatField()
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='course', null=True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.SET_NULL, related_name='course', null=True)
    slug = models.SlugField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    @property
    def joined(self):
        return f'{self.created_at.day} {self.created_at.month} {self.created_at.year}'

    @property
    def student_count(self):
        return self.customer.aggregate(student_count=models.Count('id'))['student_count'] or 0

    @property
    def comment_count(self):
        return self.videos.aggregate(comment_count=models.Count('comments__id'))['comment_count'] or 0

    @property
    def average_rating(self):
        return self.videos.aggregate(
            average_rating=models.Avg('comments__rating'))['average_rating'] or 0

    @property
    def total_duration(self):
        total_duration = sum((video.duration for video in self.videos.all()), timedelta())

        total_seconds = int(total_duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f'{hours}h {minutes}m {seconds}s'


def __str__(self):
        return f'{self.title} , {self.description}'


class Video(BaseModel):
    title = models.CharField(max_length=100)
    duration = models.DurationField()
    file = models.FileField(upload_to='videos')
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='videos', null=True)

    def __str__(self):
        return f'{self.title}'


class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value,
                                              null=True, blank=True)
    content = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comments', null=True)
    video_id = models.ForeignKey(Video, on_delete=models.SET_NULL, related_name='comments', null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f'{self.video_id} - {self.user_id}'

    def get_replies(self):
        return self.replies.all()


class Customer(BaseModel):
    phone = models.CharField(max_length=20)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='customer', null=True)
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='customer', null=True)

    def __str__(self):
        return f'{self.phone} , {self.course_id}'


class Blog(BaseModel):
    title = models.CharField(max_length=100)
    body = models.TextField()
    image = models.ImageField(upload_to='blog')
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='blog', null=True)

    def __str__(self):
        return f'{self.title}, {self.category_id}'
