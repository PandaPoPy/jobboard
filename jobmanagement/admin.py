from django.contrib import admin

from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter

from .models import User, CandidateUser, EnterpriseUser, Offer, Enterprise


class CandidateUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CandidateUser
        fields = ['username']


class EnterpriseUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = EnterpriseUser
        fields = ['username']


@admin.register(CandidateUser)
class CandidateUserAdmin(PolymorphicChildModelAdmin,UserAdmin):
    base_model = CandidateUser
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'skill', 'file')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': 'wide', 'fields': ('username', 'password1', 'password2')}),
    )
    add_form = CandidateUserCreationForm
    change_password_form = AdminPasswordChangeForm

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)


@admin.register(EnterpriseUser)
class EnterpriseUserAdmin(PolymorphicChildModelAdmin,UserAdmin):
    base_model = EnterpriseUser
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'enterprise')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': 'wide', 'fields': ('username', 'password1', 'password2', 'enterprise')}),
    )
    add_form = EnterpriseUserCreationForm
    change_password_form = AdminPasswordChangeForm

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)


@admin.register(User)
class MyUserAdmin(PolymorphicParentModelAdmin, UserAdmin):
    base_model = User
    child_models = (CandidateUser, EnterpriseUser)
    list_filter = (PolymorphicChildModelFilter,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'polymorphic_ctype')


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    fields = ['enterprise', 'title', 'start_date', 'duration', 'type', 'description', 'city', 'postcode', 'status', 'skill']


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    fields = ['name', 'logo']