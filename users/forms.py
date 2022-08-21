import email
from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from users.models import DriverProfile

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


from django import forms
class CustomerProfileForm(forms.ModelForm):
    def clean(self):
        try:
            if self.cleaned_data['user'].user_type in [1, 3]:
                self.add_error('user', "This user is not a customer.")
        except Exception as e:
            print(e)
            raise forms.ValidationError('Something went wrong! Please try again.[CP-102]')
        return self.cleaned_data


class DriverProfileForm(forms.ModelForm):
    def clean(self):
        try:
            if self.cleaned_data['user'].user_type in [1, 2]:
                self.add_error('user', "This user is not a driver.")
            else:
                if DriverProfile.objects.filter(user=self.cleaned_data['user']).exists():
                    self.add_error('user', "Duplicate user entity.")
            if User.objects.filter(email=self.cleaned_data['email']).exists():
                self.add_error('email', "Driver Profile with this Email already exists.")

            # from django.db.models import Q
            # if User.objects.filter(Q(email=self.cleaned_data['email']) | Q(id=self.cleaned_data['user'].id)).exists():
            #     self.add_error('email', "Driver Profile with this Email already exists.")   

        except Exception as e:
            print(e)
            raise forms.ValidationError('Something went wrong! Please try again.[DP-102]')
        return self.cleaned_data
