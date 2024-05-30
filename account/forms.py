from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django import forms

from travel.models import Category
from .models import CustomUser

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'avatar', 'interests')  
        # 仅包含 username 和 interest 字段，与 UserCreationForm 相比添加了 interest 字段

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['avatar', 'username', 'email', 'interests']

    interests = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']