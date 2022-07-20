from django.contrib.auth.forms import AuthenticationForm


class SigninForm(AuthenticationForm):
   def confirm_login_allowed(self, user):
       pass
