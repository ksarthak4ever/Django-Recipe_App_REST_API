from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from core import models
from django.utils.translation import gettext as _ #this is the recommended convention for converting strings in our Python to human readable text and the reason we do this is just so it gets passed through the translation engine.


class UserAdmin(BaseUserAdmin): #making a little changes to BaseUserAdmin for Users page in django admin as made a custom User Model.
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    ) #fields we passing in the UserAdmin class i.e User in django admin for changing User details.https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets. Note if we had used ModelAdmin you won't need to set those field but you won't get the change password option.

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    ) #as UserAdmin by default takes an add_fieldsets which defines the fields that we include on the add page which is same as the create user page, here customized the fieldset to include our email,password1 and 2 so we can create new user in system with minimal data req,adding extra fields such as name etc. can be done in the edit page



admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)


    

   