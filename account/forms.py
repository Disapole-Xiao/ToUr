from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'avatar', 'interests')  
        # 仅包含 username 和 interest 字段，与 UserCreationForm 相比添加了 interest 字段
