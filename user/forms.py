from django import forms
from user.models import User


class UserCreationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'image', 'date_of_birth')

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords must match')
        return password

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.data['password'])
        user.is_active = False
        user.is_superuser = True
        user.is_staff = True

        if commit:
            user.save()

        return user


