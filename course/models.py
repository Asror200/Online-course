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

    def __str__(self):
        return self.title


class Course(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    price = models.FloatField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='course')
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='course')
    slug = models.SlugField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    @property
    def joined(self):
        return f'{self.created_at.day} {self.created_at.month} {self.created_at.year}'

    def __str__(self):
        return f'{self.title} , {self.description}'


class Video(BaseModel):
    title = models.CharField(max_length=100)
    duration = models.IntegerField()
    file = models.FileField(upload_to='videos')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')

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

    rating = models.PositiveSmallIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value)
    content = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.video_id} '


class Customer(BaseModel):
    phone = models.CharField(max_length=20)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='custom')

    def __str__(self):
        return f'{self.phone} , {self.course_id}'
