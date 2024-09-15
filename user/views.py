from django.views.generic import View, TemplateView, CreateView, DetailView
from user.models import Teacher, User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from user.token import account_activation_token
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from user.forms import UserCreationForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from config.settings import EMAIL_DEFAULT_SENDER

# Create your views here.

""" This class displays Teachers"""


class TeacherView(TemplateView):
    template_name = 'user/teacher.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teachers = Teacher.objects.all()
        for teacher in teachers:
            teacher.courses = teacher.course.only('category_id__title')
        context['teachers'] = teachers
        return context


""" Authentication """


class LoginUserView(View):
    def get(self, request):
        return render(request, 'user/login-user.html')

    def post(self, request):
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(email=email, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('home')
            messages.error(request, 'Invalid email or password')
            return redirect('login')


class RegisterUserView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'user/register-user.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        subject = 'Activate your account.'
        message = render_to_string('user/acc_active_email.html', {
            'user': user,
            'domain': get_current_site(self.request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        send_mail(
            subject,
            message,
            EMAIL_DEFAULT_SENDER,
            [user.email],
            fail_silently=False,
        )

        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, 'A confirmation email has been sent to your email address.'
                                       ' Please confirm your email to complete the registration process.')

        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong. Please correct the errors below.')
        return super().form_invalid(form)


class LogoutView(View):
    """ This class is used to logout a user. """

    def get(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect(reverse_lazy('home'))


class ProfileView(DetailView):
    """
        This class displays a Teacher's or a User's profile
        when a Teacher is connected any User it will display a Teacher's profile or not it will display a User's profile
        In a Teacher's profile you can add new course, new video, new blog but in User's profile you can't
    """
    model = User
    template_name = 'user/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        try:
            teacher = Teacher.objects.get(user_id=user.id)

            context['teacher'] = teacher
        except Teacher.DoesNotExist:
            pass
        return context


class AccountActivationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Your account has been activated.')
            return redirect('home')
        else:
            return HttpResponse('Activation link is invalid!')


def forgot_password(request):
    """ When a user forgot its password this function is called.(but it works by default for now) """
    return render(request, 'user/forgot-password.html')
