from django.apps import AppConfig


class DiaryConfig(AppConfig):
    name = 'diary'


default_app_config = 'account.apps.AccountConfig'

class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    verbose_name = 'Account'

    # 添加以下行
    default_app_config = 'account.apps.AccountConfig'
