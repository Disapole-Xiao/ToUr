from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','password', 'user_interest')  
        # 仅包含 username 和 interest 字段，与 UserCreationForm 相比添加了 interest 字段
